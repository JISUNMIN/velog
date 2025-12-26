<h2 id="상황">상황</h2>
<p>사이드바 메뉴에서<br /><code>t</code>를 사용해 영문화 로직을 적용했고, <code>translation.json</code>에도 해당 번역 문구가 존재했지만<br /><strong>특정 메뉴만 영어로 변경되지 않는 이슈</strong>가 발생했다.</p>
<p>다른 메뉴들은 모두 정상적으로 영어가 적용되고 있었기 때문에<br />처음에는 특정 키 자체의 문제로 보였다.</p>
<hr />
<h2 id="원인-분석">원인 분석</h2>
<p>언어 설정 문제인지 확인하기 위해 다음 로그를 출력했다.</p>
<pre><code class="language-ts">console.log(i18n.language);
console.log(t(&quot;교환기 배터리 교체 이력&quot;, { lng: &quot;en&quot; }));</code></pre>
<ul>
<li><code>i18n.language</code> → <code>en</code> (정상)</li>
<li><code>t(&quot;교환기 배터리 교체 이력&quot;, { lng: &quot;en&quot; })</code> → 한글 반환</li>
</ul>
<p>즉, 언어 설정은 정상이나<br /><strong>번역 키를 찾지 못하고 원문을 그대로 반환하는 상황</strong>이었다.</p>
<hr />
<p>해당 메뉴는 <code>MenuList</code> 함수에서 생성되고 있었고,<br />이 함수는 외부에서 전달받은 <code>t</code>를 사용하고 있었다.</p>
<pre><code class="language-ts">const MenuList: (t: TFunction) =&gt; Type.Menu[] = (t: TFunction) =&gt; {
  console.log(&quot;i18n.language =&quot;, i18n.language);
  console.log(&quot;t(en) =&quot;, t(&quot;교환기 배터리 교체 이력&quot;, { lng: &quot;en&quot; }));
};</code></pre>
<p><code>MenuList</code>를 호출하는 코드를 확인해보니 다음과 같았다.</p>
<pre><code class="language-ts">const DefaultLayout = ({ children }: LayoutDefaultProps) =&gt; {
  const { t } = useTranslation(&quot;menu&quot;);

  const commonMenu = MenuList(t);
};</code></pre>
<p>여기서 핵심은<br /><strong><code>useTranslation(&quot;menu&quot;)</code>를 사용하고 있었다는 점</strong>이다.</p>
<hr />
<p>다른 화면에서는 대부분 다음과 같이 사용하고 있었다.</p>
<pre><code class="language-ts">const { t } = useTranslation();</code></pre>
<p>이 방식은 i18next의 기본 namespace를 사용하며,<br />기본적으로 <code>translation.json</code>을 참조한다.</p>
<p>반면 메뉴 영역에서는:</p>
<pre><code class="language-ts">useTranslation(&quot;menu&quot;)</code></pre>
<p>를 사용하고 있었고, 이는 <strong><code>menu.json</code>만 조회</strong>한다.</p>
<p>실제로 <code>menu.json</code> 파일을 확인해보니<br /><code>&quot;교환기 배터리 교체 이력&quot;</code>에 대한 번역은 존재하지 않았고,<br />해당 키는 <code>translation.json</code>에만 정의되어 있었다.</p>
<p>그 결과:</p>
<ul>
<li><code>menu</code> namespace에서 키를 찾지 못했고</li>
<li>namespace 간 fallback 설정이 없었기 때문에</li>
<li>번역 실패 후 원문(한글)이 그대로 노출되었다</li>
</ul>
<hr />
<h3 id="i18n-설정-확인">i18n 설정 확인</h3>
<p>i18n 설정은 다음과 같은 구조였다.</p>
<pre><code class="language-ts">const resources = {
  en: {
    translation: en,
    menu: enMenu,
  },
  ko: {
    translation: ko,
    menu: koMenu,
  },
};</code></pre>
<p>여기서 중요한 점은:</p>
<ul>
<li><code>translation</code>, <code>menu</code>는 서로 다른 namespace</li>
<li><code>useTranslation(&quot;menu&quot;)</code>는 <code>menu.json</code>만 조회</li>
<li><code>translation</code>이 기본 namespace로 동작하는 이유는<br /><strong>i18next의 내부 기본값(defaultNS)이 &quot;translation&quot;이기 때문</strong></li>
</ul>
<p>즉,</p>
<pre><code class="language-ts">useTranslation()</code></pre>
<p>은 내부적으로 다음과 동일하게 동작한다.</p>
<pre><code class="language-ts">useTranslation(&quot;translation&quot;)</code></pre>
<p>이는 리소스 선언 순서 때문이 아니라,<br />i18next의 기본 설계에 따른 동작이다.</p>
<hr />
<h2 id="해결">해결</h2>
<p>메뉴에서 사용하는 문자열을 <code>menu.json</code>으로 이동하였다.</p>
<pre><code class="language-json">{
  &quot;교환기 배터리 교체 이력&quot;: &quot;Station Battery Swap&quot;
}</code></pre>
<hr />
<h2 id="궁금증">궁금증</h2>
<h3 id="namespace는-생략해도-괜찮을까">namespace는 생략해도 괜찮을까?</h3>
<p>문제는 없지만, <strong>명시적으로 namespace 사용하는 것을 권장</strong>한다.</p>
<h4 id="namespace-생략">namespace 생략</h4>
<pre><code class="language-ts">useTranslation();</code></pre>
<ul>
<li>기본 namespace(<code>translation</code>)에 의존</li>
<li>간결하지만 어떤 json을 쓰는지 알기 어려움</li>
</ul>
<h4 id="namespace-명시-권장">namespace 명시 (권장)</h4>
<pre><code class="language-ts">useTranslation(&quot;translation&quot;);
useTranslation(&quot;menu&quot;);</code></pre>
<ul>
<li>참조하는 리소스가 명확</li>
<li>namespace 관련 이슈 추적이 쉬움</li>
<li>팀 컨벤션 유지에 유리</li>
</ul>
<hr />
<h2 id="정리">정리</h2>
<ul>
<li><code>useTranslation(&quot;menu&quot;)</code>는 <code>menu.json</code>만 조회한다</li>
<li><code>translation.json</code>에 키가 있어도 자동 fallback 되지 않는다</li>
<li><code>useTranslation()</code>은 i18next 기본 설정에 의해<br /><code>translation</code> namespace를 사용한다</li>
<li>동작은 생략해도 문제없지만<br /><strong>유지보수와 가독성을 위해 namespace를 명시하는 것이 좋다</strong></li>
</ul>