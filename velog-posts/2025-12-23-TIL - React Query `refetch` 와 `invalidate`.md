<h2 id="상황">상황</h2>
<p>데이터 저장 후 <strong>화면에 최신 데이터가 반영되지 않는다</strong>는 이슈가 있었다.<br />기존 코드를 살펴보니 mutation 이후 다음과 같은 코드가 있었다.</p>
<pre><code class="language-ts">const saveMemo = () =&gt; {
  mutate(
    {
      serialNo: clickedMarkerId.bike as string,
      memo: memo,
      manager: managerId || &quot;&quot;,
    },
    {
      onSuccess: () =&gt; {
        openAlert({
          title: &quot;SUCCESS&quot;,
          type: &quot;primary&quot;,
          body: t(&quot;메모 저장이 완료되었습니다.&quot;),
        });
        refetchBikeMemo();
      },
      onError: (error: Error) =&gt; {
        throw new Error(error.message);
      },
    }
  );
};</code></pre>
<p>메모 저장 후 <code>refetchBikeMemo()</code>를 호출해<br />데이터를 다시 가져오도록 되어 있었다.</p>
<p>해당 쿼리는 다음과 같은 형태였다.</p>
<pre><code class="language-ts">export const useGetGoodsMemo = (serialNo: string) =&gt; {
  return useQuery({
    queryKey: [ASSETS_QUERY_KEY.GET_GOODS_MEMO, serialNo],
    queryFn: () =&gt;
      apis.Assets.getGoodsMemo(serialNo).then(res =&gt; successHandler(res)),
  });
};</code></pre>
<hr />
<h2 id="궁금증">궁금증</h2>
<p>React Query를 계속 사용해 왔지만
mutation 이후에는 항상 <code>invalidateQueries</code>만 사용해왔고
<code>refetch</code>를 직접 호출한 경험은 거의 없었다.</p>
<p>그래서 <code>refetch</code>는 정확히 뭐고 <code>invalidateQueries</code>랑 뭐가 다른지 궁금했다.</p>
<h3 id="refetch">refetch</h3>
<p><code>refetch</code>는 <code>useQuery</code>의 return 값에 포함된 함수로,
<strong>해당 querykey를 사용하는 쿼리만 즉시 다시 요청</strong>한다.</p>
<pre><code class="language-ts">const { refetch } = useQuery(...);

refetch();</code></pre>
<ul>
<li>완전히 동일한 queryKey를 사용하는 쿼리만 갱신</li>
<li>현재 마운트된 컴포넌트 범위에서만 동작 </li>
<li>페이지 새로고침시에는 최신 데이터 반영</li>
<li>같은 querykey를 쓰더라도 언마운트 되어있을 시 갱신 불가</li>
</ul>
<p><strong>즉, refetch는 &quot;이 쿼리 하나만 다시 가져올 건데,
현재 켜져 있는 페이지에서만 갱신해&quot; 라는 의미</strong></p>
<p>이 때문에 mutation 이후 데이터 정합성을 맞추는 용도로는
적합하지 않다.</p>
<h3 id="invalidatequeries">invalidateQueries</h3>
<p><code>invalidateQueries</code>는 특정 queryKey를 stale(오래된 상태)로 표시한다.</p>
<pre><code class="language-ts">queryClient.invalidateQueries({
  queryKey: ['user'],
});</code></pre>
<ul>
<li>queryKey prefix 매칭 지원</li>
<li>현재 마운트된 쿼리는 즉시 refetch, 마운트되지 않은 쿼리는 이후 페이지 진입 시 최신 데이터로 요청</li>
<li>진입하지 않은 페이지는 요청을 안보내기 떄문에, 불필요한 API 요청을 막아 성능적으로 유리</li>
</ul>
<pre><code class="language-ts">// queryKey prefix 매칭 지원
invalidateQueries({ queryKey: ['user'] });</code></pre>
<p>위 코드로 밑줄의 쿼리들이 모두 무효화된다. (prefix가 같으면 같이 무효화 시킴)</p>
<pre><code class="language-ts">['user']
['user', userId]</code></pre>
<p><strong>즉, invalidate는 &quot;이 데이터를 쓰는 모든 화면은 
이제 오래됬으니 갱신해라&quot; 라는 의미</strong></p>
<hr />
<h3 id="refetch는-언제-사용하는가">refetch는 언제 사용하는가?</h3>
<p>그렇다면 refetch는 왜 존재할까?
주요 사용 사례를 알아봤다.</p>
<ul>
<li>새로고침 버튼: 지금 화면만 갱신</li>
<li>enabled: false 상태에서 수동 조회: 수동 호출할때(검색 버튼)</li>
<li>다른 화면 데이터와 상관없는 화면 UI갱신: 현재 화면에서만 필요한 통계,데이터등  </li>
</ul>
<p>즉,</p>
<p><strong>mutation 실행 이후에는 거의 사용하지 않으며</strong>,  
<strong>해당 페이지의 데이터만 갱신하거나 쿼리를 수동으로 실행해야 하는 경우에만
제한적으로 사용한다.</strong></p>
<hr />
<h2 id="해결">해결</h2>
<p>처음에는 같은 페이지에서 메모를 저장했음에도 화면이 갱신되지 않아<br /><code>refetch</code> 또는 <code>invalidateQueries</code> 사용 방식의 문제라고 판단했다.</p>
<p>하지만 실제 원인은 <strong>화면이 참조하고 있는 쿼리 데이터가 달랐다.</strong></p>
<pre><code class="language-ts">const { data, isFetching } = useGetBikeInfo(clickedMarkerId.bike as string);
const { data: bikeMemo, refetch: refetchBikeMemo } = useGetGoodsMemo(clickedMarkerId.bike as string);</code></pre>
<p>useGetGoodsMemo는 메모 전용 API를 호출하는 쿼리이며<br />queryKey는 <code>[GET_GOODS_MEMO, serialNo]</code> 형태였다.</p>
<p>하지만 화면에서는 메모를<br /><code>useGetBikeInfo</code>(전체 데이터) 안에 포함된 <code>memo</code> 값을 사용하고 있었다.</p>
<p>이로 인해:</p>
<ul>
<li><code>refetchBikeMemo()</code>를 호출해도</li>
<li>메모 전용 쿼리만 갱신되고</li>
<li>실제 화면이 참조하는 <code>bikeInfo.memo</code>는 갱신되지 않아</li>
<li>UI가 변경되지 않는 것처럼 보였다.</li>
</ul>
<p>따라서 <code>refetch</code>나 <code>invalidateQueries</code>를 변경하는 것이 아니라,<br /><strong>메모 표시 기준 데이터를 메모 전용 쿼리(<code>useGetGoodsMemo</code>)의 결과로 통일</strong>하는 방식으로 수정했다.</p>
<pre><code class="language-ts">// 변경 전
memo={data?.memo || &quot;&quot;}
// 변경 후
memo={bikeMemo?.memo ?? &quot;&quot;}
</code></pre>
<p>또 다른 해결 방법으로는, 메모 저장 성공 이후
invalidateQueries로 전체 데이터 쿼리까지 무효화하여
전체 데이터를 다시 받아오게 만드는 방법도 고려할 수 있었다.</p>
<p>하지만 이 방식은 메모 변경처럼 일부 필드만 바뀐 상황에서도 전체 데이터를 요청하게 되어
불필요한 네트워크 요청이나 리렌더가 발생할 수 있다고 판단하여 사용하지 않았다.</p>
<hr />
<h2 id="정리">정리</h2>
<ul>
<li><code>refetch</code>는 <strong>해당 queryKey 하나만 즉시 다시 요청</strong>한다</li>
<li>mutation 이후 <code>refetch</code>를 사용하면 화면 간 데이터 불일치가 발생할 수 있다</li>
<li><code>invalidateQueries</code>는 queryKey prefix 기준으로 쿼리를 무효화한다</li>
<li>mutation 이후 데이터 갱신에는 <code>invalidateQueries</code>가 권장된다</li>
</ul>
<blockquote>
<p><strong>서버 데이터가 변경되는 경우에는 <code>invalidateQueries</code>를 기본으로 사용한다</strong></p>
</blockquote>
<ul>
<li>하지만 해당 데이터 갱신 이슈의 원인은 <code>refetch</code> / <code>invalidateQueries</code> 사용 방식이 아니라<br /><strong>화면이 참조하는 쿼리 데이터와 갱신 대상 쿼리가 달랐기 때문</strong>이었다.</li>
</ul>