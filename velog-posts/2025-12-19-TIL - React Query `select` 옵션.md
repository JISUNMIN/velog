<h2 id="상황">상황</h2>
<p>API 응답이 공통 래퍼 형태로 내려오는 경우,
실제 화면에서 필요한 데이터는 한 단계 더 들어가야 하는 상황이 자주 발생한다.</p>
<pre><code class="language-ts">export interface Result&lt;T&gt; {
  resultCode: string;
  resultData: T;
  resultMessage: string;
  status: string;
}</code></pre>
<p>여기서는 <code>resultData</code>만 필요한 상황</p>
<p>React query에서는 이러한 응답 구조를 <code>select</code> 옵션을 통해
원하는 형태로 변환할 수 있다.
보통 공통 래퍼 제거 할때 많이 사용한다고 한다.</p>
<h2 id="코드---select-사용">코드 - Select 사용</h2>
<pre><code class="language-ts">export const useGetMembershipMemo = (membershipId: number) =&gt; {
  return useQuery({
    queryKey: [MEMBERSHIP_QUERY_KEY.GET_MEMBERSHIP_MEMO, membershipId],
    queryFn: () =&gt; API.Membership.getMembershipMemo(membershipId),
    select: (data: Result&lt;{ membershipId: number; memo: string }&gt;) =&gt;
      data.resultData,
    enabled: Boolean(membershipId),
    retry: false,
  });
};</code></pre>
<ul>
<li>쿼리 응답 data는 resultData가 됨</li>
<li>캐시에 저장되는 데이터도 resultData 기준</li>
<li>타입이 단순화됨</li>
</ul>
<h2 id="코드---select-없이-처리하는-경우">코드 - select 없이 처리하는 경우</h2>
<pre><code class="language-ts">export const useGetMembershipMemo = (membershipId: number) =&gt; {
  const query = useQuery({
    queryKey: [MEMBERSHIP_QUERY_KEY.GET_MEMBERSHIP_MEMO, membershipId],
    queryFn: () =&gt; API.Membership.getMembershipMemo(membershipId),
    enabled: Boolean(membershipId),
    retry: false,
  });

  return query.resultData;
};</code></pre>
<ul>
<li>캐시에는 Result 전체가 저장됨</li>
<li>query의 결과값이 다필요한 경우(status나 resultCode등)에는 사용 할수 있음</li>
<li>타입이 복잡하게 유지됨</li>
</ul>
<hr />
<h2 id="정리">정리</h2>
<ul>
<li><p>Select를 사용하면 캐시에 변환된 데이터만 저장, 
React Query는 이 데이터를 기준으로 변경을 감지,
변경 감지 단위가 줄기 때문에 불필요한 리렌더를 줄일 수 있음</p>
</li>
<li><p>API 응답에 공통 래퍼가 있는 경우 권장되는 방식
다만 API 응답 전체 데이터가 필요한 경우에는 사용하지 않음</p>
</li>
</ul>
<p><strong>select는 단순한 데이터 가공이 아니라,
쿼리 캐시의 기준 데이터 구조를 정의하는 도구이다.</strong></p>