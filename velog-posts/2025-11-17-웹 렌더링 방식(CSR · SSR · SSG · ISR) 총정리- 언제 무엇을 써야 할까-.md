<p>앞선 글에서 React와 Next.js의 큰 차이를 살펴봤습니다.<br />그중에서도 가장 중요한 핵심 개념이 바로 <strong>“페이지를 어디서, 언제 렌더링하느냐”</strong>입니다.</p>
<p>Next.js가 강력한 이유는 React가 기본적으로 제공하는 CSR 방식뿐 아니라
<strong>SSR, SSG, ISR까지 다양한 렌더링 전략을 페이지 단위로 선택할 수 있다는 점</strong>입니다.</p>
<p>이 글에서는 Next.js를 이해하는 데 반드시 필요한 네 가지 렌더링 방식 
— <strong>CSR / SSR / SSG / ISR</strong>의 개념과 특징, 장단점, 그리고 실제 사용 시나리오까지 정리해보겠습니다.</p>
<hr />
<h2 id="🌐-1-csr-client-side-rendering">🌐 1. CSR (Client Side Rendering)</h2>
<h3 id="🔹-개념">🔹 개념</h3>
<ul>
<li><strong>브라우저(클라이언트)</strong> 가 JS를 실행해서 화면을 그리는 방식입니다.</li>
<li>서버는 <code>index.html</code> (빈 HTML 껍데기)과 JS 파일만 내려주고,<br />브라우저가 JS를 실행하여 DOM을 생성합니다.</li>
<li>React·Vue 같은 <strong>SPA(Single Page Application)</strong> 구조에서 기본적으로 사용되는 방식입니다.</li>
</ul>
<hr />
<h3 id="⚙️-동작-흐름">⚙️ 동작 흐름</h3>
<ol>
<li>브라우저가 서버에서 <code>index.html</code>과 JS 번들을 다운로드</li>
<li>JS가 실행되면서 React/Vue가 DOM을 렌더링</li>
<li>페이지 이동은 서버 요청 없이 JS가 직접 DOM을 교체(SPA 라우팅)</li>
</ol>
<hr />
<h3 id="✅-장점">✅ 장점</h3>
<ul>
<li><strong>페이지 전환이 매우 빠름</strong><br />(서버에서 새 HTML을 받지 않고, JS가 DOM만 바꿔치기)</li>
<li><strong>클라이언트 상태 유지가 쉬움</strong><br />예: 포커스, 입력 상태, 스크롤 위치 등</li>
<li><strong>서버 부하가 적음 (HTML 렌더링 X)</strong>
서버는 단순 파일만 내려주면 되기 때문</li>
</ul>
<h3 id="⚠️-단점">⚠️ 단점</h3>
<ul>
<li><strong>초기 로딩이 느림</strong><br />→ JS 다운로드 → 실행 → 렌더링까지 시간이 걸림  </li>
<li><strong>SEO에 불리함</strong>  <ul>
<li>초기 HTML이 비어 있고, JS 실행 전에는 콘텐츠 없음</li>
<li>검색 엔진 봇이 JS를 제대로 실행하지 못하면 콘텐츠를 인식하지 못함</li>
<li>크롤링 비용이 높아 검색 노출에도 불리</li>
</ul>
</li>
<li><strong>JS 오류 시 화면 전체가 빈 상태로 남을 수 있음</strong></li>
</ul>
<hr />
<h3 id="사용-시점">사용 시점</h3>
<ul>
<li>내부 관리자 페이지(Admin)</li>
<li>로그인 후 접근하는 서비스 (SEO 중요하지 않은 곳)</li>
<li>실시간 데이터,인터랙션 많은 SPA (대시보드, 모니터링, 차트 시스템 등)</li>
</ul>
<p>실시간 차트/그래프/대시보드는 DOM 변경이 매우 빈번함</p>
<p>SSR/SSG는 서버에서 새 HTML을 계속 만들어야 해서 비효율적</p>
<p>CSR은 JS가 DOM을 곧바로 업데이트하여 실시간 반응성이 뛰어남</p>
<blockquote>
<h3 id="🤔-왜-실시간-대시보드-화면에는-csr이-잘-맞을까">🤔 왜 실시간 대시보드 화면에는 CSR이 잘 맞을까?</h3>
</blockquote>
<ul>
<li>실시간 차트/그래프/대시보드는 <strong>DOM 변경이 매우 빈번</strong>합니다.</li>
<li>SSR/SSG는 데이터가 바뀔 때마다 서버에서 새 HTML을 만들어야 해서 <strong>비효율적</strong>입니다.</li>
<li>CSR은 브라우저에서 JS가 직접 DOM을 업데이트하기 때문에<br /><strong>서버 왕복 없이 빠르게 화면을 갱신</strong>할 수 있습니다.<blockquote>
<p>특히 내부 대시보드나 모니터링 화면처럼<br />SEO보다 <strong>반응 속도와 사용성(UX)</strong>이 중요한 경우에 사용하면 좋습니다.</p>
</blockquote>
</li>
</ul>
<hr />
<h3 id="💻-예시">💻 예시</h3>
<pre><code class="language-tsx">// React (CSR)
function Page() {
    const [data, setData] = useState([]);
    useEffect(() =&gt; {
        fetch(&quot;/api/data&quot;)
            .then((r) =&gt; r.json())
            .then(setData);
    }, []);
    return (
        &lt;div&gt;
            {data.map((item) =&gt; (
                &lt;p&gt;{item}&lt;/p&gt;
            ))}
        &lt;/div&gt;
    );
}</code></pre>
<hr />
<h2 id="🖥-2-ssr-server-side-rendering">🖥 2. SSR (Server Side Rendering)</h2>
<h3 id="🔹-개념-1">🔹 개념</h3>
<ul>
<li><strong>서버가 HTML을 미리 만들어서 브라우저에 전달하는 방식</strong>입니다.</li>
<li>브라우저는 처음부터 완성된 HTML을 보기 때문에 초기 표시 속도가 빠릅니다. </li>
<li>HTML이 렌더링된 후 JS가 hydration을 수행하면서 앱이 상호작용 가능해집니다.</li>
</ul>
<blockquote>
<h3 id="hydration이란">hydration이란?</h3>
<p>SSR로 그려진 정적 HTML을 React 앱으로 “활성화”하는 과정
→ 이벤트, 상태, useEffect가 작동하게 되는 순간</p>
</blockquote>
<hr />
<h3 id="⚙️-동작-흐름-1">⚙️ 동작 흐름</h3>
<ol>
<li>클라이언트 요청 → 서버에서 해당 페이지 HTML 생성</li>
<li>브라우저는 HTML을 즉시 렌더링 (JS 실행 전에도 콘텐츠 표시)</li>
<li>JS가 로드되면 React가 기존 DOM과 연결되어 이벤트 활성화</li>
</ol>
<hr />
<h3 id="✅-장점-1">✅ 장점</h3>
<ul>
<li><strong>초기 표시 속도 빠름 (First Paint 빠름)</strong></li>
<li><strong>SEO에 유리</strong> (HTML에 실제 콘텐츠 포함)
서버에서 이미 완성된 HTML을 내려주므로 검색엔진이 즉시 크롤링 가능</li>
<li>서버에서 안전하게 데이터 패칭 가능
(비공개 API 호출, 인증 기반 요청 등)</li>
</ul>
<h3 id="⚠️-단점-1">⚠️ 단점</h3>
<ul>
<li>매 요청마다 서버에서 렌더링 수행 → <strong>서버 부하 증가</strong></li>
<li>페이지 전환 시 서버는 새 HTML 렌더링, 브라우저는 JS를 다시 실행</li>
<li>캐싱 전략이 복잡함</li>
<li>실시간 인터랙션이 많은 UI에는 적합하지 않음
(서버 렌더링을 반복하기엔 너무 무거움)</li>
</ul>
<hr />
<h3 id="사용-시점-1">사용 시점</h3>
<ul>
<li>SEO가 중요한 페이지 (블로그, 쇼핑몰 상품 상세 등)</li>
<li>첫 화면 로딩 속도가 중요한 페이지 (랜딩 페이지)</li>
<li>데이터가 자주 변경되지만 <strong>실시간 반영은 필요 없는 곳</strong></li>
</ul>
<hr />
<h3 id="💻-예시-nextjs">💻 예시 (Next.js)</h3>
<pre><code class="language-tsx">export async function getServerSideProps() {
    const res = await fetch(&quot;https://api.example.com/data&quot;);
    const data = await res.json();
    return { props: { data } };
}</code></pre>
<hr />
<h2 id="📝-csr-vs-ssr-핵심-정리">📝 CSR vs SSR 핵심 정리</h2>
<h3 id="🔹-csrclient-side-rendering">🔹 CSR(Client Side Rendering)</h3>
<ul>
<li>서버는 <code>비어 있는 HTML 껍데기(index.html)</code>와 <code>JS 파일</code>만 내려줍니다.</li>
<li>브라우저는 내려받은 JS를 실행해 <code>DOM을 직접 생성하여 화면을 채웁니다</code>.</li>
<li>이후 화면 변경(상태 변경, 라우팅 등)도 모두 <code>브라우저에서 JS가 즉시 DOM을 수정</code>하여 처리합니다.</li>
<li>즉, <strong>HTML 렌더링도 JS 실행도 모두 브라우저가 담당</strong>합니다.</li>
</ul>
<pre><code class="language-text">      사용자 요청
          ↓
┌──────────────────────────────┐
│      서버(Server)      │
│  - index.html (빈 껍데기)   │
│  - bundle.js (React 코드)  │
└──────────────────────────────┘
          ↓ HTML + JS 다운로드
          ↓
┌──────────────────────────────┐
│        브라우저(Browser)    │
│  1) JS 실행                │
│  2) JS가 DOM 생성          │
│  3) 화면 렌더링             │
│  4) 이후 변경도 JS가 DOM 업데이트│
└──────────────────────────────┘

✔ 페이지 이동 → JS가 DOM만 바꿔치기 (JS 라우팅)
✔ 서버에 HTML 다시 요청 ❌</code></pre>
<hr />
<h3 id="🔹-ssrserver-side-rendering">🔹 SSR(Server Side Rendering)</h3>
<ul>
<li>서버는 요청마다 <code>완성된 HTML을 직접 렌더링해서</code> 브라우저로 전달합니다.</li>
<li>브라우저는 전달된 <code>HTML을 즉시 화면에 그립니다.</code>(초기 표시 속도 빠름)</li>
<li>이어서 JS 파일이 로드되면 React가 기존 HTML과 연결되는데,<br />이 과정을 <code>hydration(하이드레이션)</code>이라고 합니다.<br />→ 정적인 HTML이 “상호작용 가능한 React 앱”으로 변환되는 단계입니다.</li>
<li><code>hydration이 끝난 순간, 이 페이지는 전형적인 React(CSR) 방식으로 동작합니다.</code> 
즉, 상태 변화나 UI 업데이트는 <code>서버가 HTML을 다시 보내는 것이 아니라  
브라우저에서 실행되는 JS가 직접 DOM을 업데이트합니다.</code></li>
<li>단, <code>페이지 전환(라우팅)</code>은 CSR의 JS 라우팅처럼 브라우저에서 처리되지 않고,<br /><code>서버에 다시 요청하여 새로운 HTML을 렌더링받는 방식으로 동작합니다.</code>  </li>
<li><ul>
<li>→ 새로운 HTML 응답 → 화면 렌더링 → JS 로드 → 다시 hydration<br />이 과정이 반복되기 때문에 CSR에 비해 비용이 더 큽니다.**</li>
</ul>
</li>
</ul>
<pre><code class="language-text">      사용자 요청
            ↓
┌──────────────────────────────┐
│          서버(Server)      │
│  - 요청마다 HTML 직접 렌더링 │
│  - 완성된 HTML 반환         │
│  - bundle.js (React 코드)  │
└──────────────────────────────┘
            ↓ HTML + JS 다운로드
            ↓
┌─────────────────────────────────────┐
│        브라우저(Browser)          │
│  1) HTML 즉시 렌더링(Fast FP)     │
│  2) hydration(React 연결)        │
│  3) 이후 UI 변경은 JS가 DOM 업데이트│
└─────────────────────────────────────┘</code></pre>
<p>단, 페이지 이동 시:</p>
<ul>
<li>사용자 → 서버에 새 요청</li>
<li>서버: 새 HTML 렌더링</li>
<li>브라우저: 새 JS 실행 → 다시 hydration</li>
</ul>
<p>✔ 페이지 전환마다 서버 렌더링 (서버 라우팅)
✔ 비용 ↑ (CSR보다 무거움)</p>
<h3 id="🔍-핵심-차이-한-줄-요약">🔍 핵심 차이 한 줄 요약</h3>
<ul>
<li><strong>CSR</strong>:  
HTML 생성도, 화면 업데이트도 <strong>모두 브라우저(JS)가 처리</strong><br />→ 빠른 인터랙션, SEO 약함</li>
<li><strong>SSR</strong>:  
초기 HTML은 <strong>서버가 렌더링</strong>, 동작 가능하게 만드는 것은 <strong>브라우저(JS)</strong><br />→ 초기 표시 빠름, SEO 강함, 페이지 전환 비용 큼</li>
</ul>
<hr />
<h2 id="🏗-3-ssg-static-site-generation">🏗 3. SSG (Static Site Generation)</h2>
<h3 id="🔹-개념-2">🔹 개념</h3>
<ul>
<li><strong>빌드 시점에 미리 HTML을 생성해두는 방식</strong>입니다.</li>
<li>사용자가 접속할 때마다 서버가 아니라 CDN에서 정적 HTML을 바로 전달합니다.</li>
</ul>
<blockquote>
<h3 id="cdn이란">CDN이란?</h3>
<p><strong>CDN(Content Delivery Network)</strong>은 전 세계에 퍼져 있는 캐시 서버 네트워크입니다.
정적 파일(HTML, JS, CSS, 이미지 등)을 미리 저장해두고,
사용자와 가장 가까운 서버에서 빠르게 파일을 전달해 줍니다.</p>
<p>예: 한국 사용자는 서울 CDN, 일본 사용자는 도쿄 CDN에서 파일 제공</p>
<p>SSG는 정적 HTML을 생성하므로 CDN과 궁합이 매우 좋음
→ 전 세계 어디서든 초고속 로딩 가능
→ 서버 부하도 거의 없음</p>
</blockquote>
<hr />
<h3 id="⚙️-동작-흐름-2">⚙️ 동작 흐름</h3>
<ol>
<li>빌드 시 <code>getStaticProps()</code>가 실행되어 API 데이터로 HTML 파일 생성</li>
<li>생성된 HTML은 서버나 CDN에 캐싱되어 요청 시 즉시 응답</li>
</ol>
<hr />
<h3 id="✅-장점-2">✅ 장점</h3>
<ul>
<li><strong>가장 빠른 응답 속도 (빌드 타임 생성)</strong></li>
<li><strong>서버 부하 없음</strong></li>
<li>CDN 캐싱으로 대규모 트래픽에도 안정적</li>
</ul>
<h3 id="⚠️-단점-2">⚠️ 단점</h3>
<ul>
<li>콘텐츠 업데이트 시 <strong>다시 빌드해야 함</strong></li>
<li>실시간 데이터 반영 어려움</li>
</ul>
<hr />
<h3 id="사용-시점-2">사용 시점</h3>
<ul>
<li>문서, 블로그, 마케팅 랜딩 페이지</li>
<li>자주 바뀌지 않는 콘텐츠 (회사 소개 페이지 (About), 서비스 소개 페이지, FAQ 등)</li>
<li><em>변경이 적을수록 SSG 효율은 극대화됨.*</em></li>
<li>SEO가 중요한 페이지 (블로그, 기술 문서 등) 
-&gt; SSR과 동일하게 SEO 강한데, SSR보다 훨씬 빠르고 가벼움</li>
<li><strong>트래픽이 많을 것이 예상되는 페이지</strong>(이벤트 랜딩 페이지, 할인/쿠폰 페이지)</li>
<li><blockquote>
<p>SSG는 HTML이 미리 만들어져 있고 CDN에서 캐싱되므로 트래픽 폭주에도 버틸 수 있음.</p>
</blockquote>
</li>
<li>최초 로딩 속도가 중요한 페이지</li>
<li><blockquote>
<p>SSR보다 빠름</p>
</blockquote>
</li>
</ul>
<hr />
<h3 id="🔎-ssg에서-api를-사용할-수-있는-경우-vs-부적합한-경우">🔎 SSG에서 API를 &quot;사용할 수 있는 경우&quot; vs &quot;부적합한 경우&quot;</h3>
<h3 id="✔-ssg에서도-api-호출이-가능한-경우-ssgcsr-조합">✔ SSG에서도 API 호출이 <strong>가능한 경우</strong> (SSG+CSR 조합)</h3>
<p><strong>데이터가 HTML 구조를 바꾸지 않을 때</strong></p>
<p>예:</p>
<ul>
<li>좋아요 수 / 조회수  </li>
<li>방문자 수  </li>
<li>현재 시간  </li>
<li>유저 정보(텍스트만 변경)</li>
</ul>
<p>HTML 구조는 그대로, <strong>값만 바뀌는 데이터</strong><br />페이지는 SSG로 만들고
바뀌는 값만 클라이언트(JS)에서 fetch로 갱신하면 됨
→ 즉, <strong>정적 페이지 + CSR로 값만 업데이트</strong></p>
<h3 id="예시-ssg--csr-조합">예시 (SSG + CSR 조합)</h3>
<h4 id="1-ssg로-정적-페이지-생성">1) SSG로 정적 페이지 생성</h4>
<pre><code class="language-tsx">// app/post/[id]/page.tsx  (SSG)
export const dynamic = &quot;force-static&quot;;

export default async function Page({ params }) {
  const post = await fetch(`https://api.example.com/post/${params.id}`)
    .then(r =&gt; r.json());

  return (
    &lt;div&gt;
      &lt;h1&gt;{post.title}&lt;/h1&gt;
      &lt;p&gt;{post.content}&lt;/p&gt;

      {/* 변하는 값은 CSR 컴포넌트로 갱신 */}
      &lt;ViewCount postId={params.id} /&gt;
    &lt;/div&gt;
  );
}
</code></pre>
<h4 id="2-csr로-값만-갱신">2) CSR로 값만 갱신</h4>
<pre><code class="language-tsx">&quot;use client&quot;;

import { useEffect, useState } from &quot;react&quot;;

export function ViewCount({ postId }) {
  const [count, setCount] = useState(null);

  useEffect(() =&gt; {
    fetch(`/api/views?id=${postId}`)
      .then(r =&gt; r.json())
      .then(data =&gt; setCount(data.views));
  }, [postId]);

  return &lt;div&gt;조회수: {count ?? &quot;로딩중...&quot;}&lt;/div&gt;;
}
</code></pre>
<hr />
<h3 id="❌-ssg에서-부적합한-경우">❌ SSG에서 <strong>부적합한 경우</strong></h3>
<p><strong>데이터가 HTML 구조를 바꾸는 경우</strong></p>
<p>예:</p>
<ul>
<li>게시판 글 추가  </li>
<li>댓글 추가/삭제  </li>
<li>상품 목록 변화  </li>
<li>검색 결과 목록</li>
</ul>
<p>→ DOM 요소 자체가 늘어나거나 줄어듦<br />→ 정적 HTML과 실제 데이터가 불일치<br />→ <strong>SSR / ISR / CSR이 적합</strong></p>
<h3 id="정리">정리:</h3>
<p><strong>값만 바뀌는 데이터</strong> → SSG + CSR 가능
구조가 바뀌는 데이터 → SSG 부적합 → SSR/ISR/CSR 사용</p>
<hr />
<h3 id="💻-예시-nextjs-1">💻 예시 (Next.js)</h3>
<pre><code class="language-tsx">export async function getStaticProps() {
    const res = await fetch(&quot;https://api.example.com/posts&quot;);
    const posts = await res.json();
    return { props: { posts } };
}</code></pre>
<hr />
<h2 id="🔁-4-isr-incremental-static-regeneration">🔁 4. ISR (Incremental Static Regeneration)</h2>
<h3 id="🔹-개념-3">🔹 개념</h3>
<ul>
<li><strong>SSG와 SSR의 하이브리드 방식</strong>으로,<br />정적 페이지를 일정 주기마다 자동으로 다시 생성해주는 기술입니다.</li>
<li><em>SSG처럼 미리 만들어둔 HTML을 사용하지만, 일정 시간이 지나면 자동으로 최신 버전으로 재생성되는 방식.*</em></li>
</ul>
<hr />
<h3 id="왜-isr이-필요한가">왜 ISR이 필요한가?</h3>
<p>SSG는 빠르고 안정적이지만 <strong>한 가지 큰 단점</strong>이 있습니다.</p>
<p><strong>&quot;데이터가 바뀌면 다시 빌드해야 한다&quot;</strong></p>
<ul>
<li>한 번 만들어진 HTML은 빌드 시점 데이터 그대로 고정됩니다.</li>
<li>시간이 지나면 페이지가 <strong>“오래된 정보”</strong>가 되어버립니다.</li>
</ul>
<p>예를 들어 이런 페이지들은 하루에도 수십 번 바뀝니다.</p>
<ul>
<li>쇼핑몰 상품 목록</li>
<li>게시판 목록</li>
<li>뉴스 기사 목록</li>
<li>최신 글 목록</li>
</ul>
<p>이런 페이지를 SSG로 만들면:</p>
<p>데이터가 바뀔 때마다 전체 빌드를 다시 해야 하고</p>
<p>트래픽이 많으면 “오래된 데이터”가 사용자에게 계속 보이게 됩니다. 
그래서 등장한 것이 ISR 입니다.</p>
<hr />
<h3 id="⚙️-동작-흐름-3">⚙️ 동작 흐름</h3>
<ol>
<li>최초 요청 시 SSG처럼 정적 HTML을 응답</li>
<li><code>revalidate</code> 시간이 지나면 백그라운드에서 새 HTML 생성</li>
<li>새 HTML이 준비되면 다음 요청부터 최신 버전 제공</li>
</ol>
<p>즉, <strong>“정해진 시간이 지난 후, 다음 요청이 들어올 때 새 페이지를 백그라운드에서 재생성하는 방식”.</strong></p>
<hr />
<h3 id="✅-장점-3">✅ 장점</h3>
<ul>
<li><strong>SSG처럼 빠른 초기 응답 속도</strong>
(정적 HTML이므로 렌더링 시간이 거의 없음)</li>
<li>** SSR처럼 최신 데이터 유지 가능**
(revalidate 주기마다 자동 업데이트)</li>
<li><strong>서버 부하 최소화</strong>
SSR처럼 모든 요청을 서버에서 렌더링하지 않기 때문에 훨씬 경제적</li>
<li>SEO에 유리함
초기 HTML이 항상 존재하기 때문에 검색엔진에 안정적으로 노출됨</li>
</ul>
<h3 id="⚠️-단점-3">⚠️ 단점</h3>
<ul>
<li><strong>완전 실시간은 아님</strong>
예: <code>revalidate = 60</code>이면 최대 60초 동안은 옛날 데이터일 수 있음</li>
<li>구현 복잡도 증가
캐시, stale-while-revalidate 전략 이해 필요</li>
<li>API가 매우 자주 변하는 시스템에는 적합하지 않을 수 있음</li>
</ul>
<hr />
<h3 id="사용-시점-3">사용 시점</h3>
<ul>
<li>뉴스, 쇼핑몰 상품 목록, 게시판 목록 등</li>
<li><strong>“자주 바뀌지만 즉시 반영될 필요는 없는” 콘텐츠</strong></li>
</ul>
<hr />
<h3 id="💻-예시-nextjs-2">💻 예시 (Next.js)</h3>
<pre><code class="language-tsx">export async function getStaticProps() {
    const res = await fetch(&quot;https://api.example.com/posts&quot;);
    const posts = await res.json();
    return {
        props: { posts },
        revalidate: 60, // 60초마다 새로 생성
    };
}</code></pre>
<hr />
<h2 id="📊-5-비교-요약">📊 5. 비교 요약</h2>
<p>아래는 네 가지 렌더링 방식(CSR, SSR, SSG, ISR)을
<strong>성능·서버 부하·SEO·데이터 최신성 관점에서 한눈에 비교한 표</strong>입니다.</p>
<table>
<thead>
<tr>
<th>구분</th>
<th>CSR</th>
<th>SSR</th>
<th>SSG</th>
<th>ISR</th>
</tr>
</thead>
<tbody><tr>
<td><strong>HTML 생성 시점</strong></td>
<td>브라우저</td>
<td>요청 시 서버</td>
<td>빌드 시</td>
<td>빌드 + 주기적 갱신</td>
</tr>
<tr>
<td><strong>서버 부하</strong></td>
<td>낮음</td>
<td>높음</td>
<td>없음</td>
<td>낮음</td>
</tr>
<tr>
<td><strong>초기 속도</strong></td>
<td>느림</td>
<td>빠름</td>
<td>매우 빠름</td>
<td>빠름</td>
</tr>
<tr>
<td><strong>SEO</strong></td>
<td>불리</td>
<td>유리</td>
<td>유리</td>
<td>유리</td>
</tr>
<tr>
<td><strong>데이터 최신성</strong></td>
<td>항상 최신</td>
<td>항상 최신</td>
<td>빌드 시점 기준</td>
<td>주기적 업데이트</td>
</tr>
<tr>
<td><strong>대표 예시</strong></td>
<td>CRA, Vite</td>
<td>Next.js(SSR)</td>
<td>Next.js(SSG)</td>
<td>Next.js(ISR)</td>
</tr>
</tbody></table>
<hr />
<h3 id="📝-각-방식의-핵심-요약">📝 각 방식의 핵심 요약</h3>
<ul>
<li>CSR: 최초 속도 느리지만, 사용 중 인터랙션은 가장 빠름 (SPA 특화)
→ 대시보드, 관리자 페이지, 로그인 이후 앱처럼 SEO 필요 없고 인터랙션 많은 서비스에 사용</li>
<li>SSR: 초기 화면 가장 빠르지만, 페이지 전환이 무거움 (매 요청 서버 호출)
SEO + 실시간 데이터 조합일 때 사용 (상품 상세, 검색 페이지 등)
→ 초기 로딩 중요 + 검색엔진 노출 필요한 페이지에 사용</li>
<li>SSG: 절대적으로 가장 빠름 + 가장 안정적 (정적 페이지이므로)
→ 랜딩 페이지/블로그/문서 같은 정적 콘텐츠에 최적화</li>
<li>ISR: “<strong>현대 프론트엔드가 가장 선호하는 방식</strong>” → 빠름 + 최신 + 서버 부하 적음의 조합
→ 실무에서 <strong>목록 페이지(뉴스·상품 리스트 등)</strong>에 매우 자주 사용됨</li>
</ul>
<hr />
<h2 id="🔀-react-vs-nextjs-렌더링-비교">🔀 React vs Next.js 렌더링 비교</h2>
<p>Next.js가 React보다 강력한 이유는 바로 <strong>다양한 렌더링 전략을 지원하기 때문</strong>입니다.</p>
<table>
<thead>
<tr>
<th>구분</th>
<th>React (CRA, Vite 등)</th>
<th>Next.js</th>
</tr>
</thead>
<tbody><tr>
<td><strong>기본 렌더링 방식</strong></td>
<td>CSR만 지원</td>
<td>CSR / SSR / SSG / ISR 모두 지원</td>
</tr>
<tr>
<td><strong>HTML 생성 주체</strong></td>
<td>브라우저(JS 실행)</td>
<td>서버 또는 빌드 타임</td>
</tr>
<tr>
<td><strong>SEO 대응</strong></td>
<td>불리 (빈 HTML)</td>
<td>유리 (SSR/SSG 지원)</td>
</tr>
<tr>
<td><strong>페이지 단위 설정</strong></td>
<td>불가능 (전체 CSR)</td>
<td>가능 (페이지별 방식 선택)</td>
</tr>
<tr>
<td><strong>대표 예시</strong></td>
<td>SPA 관리자, 내부 시스템</td>
<td>블로그, 커머스, 뉴스 등 다양한 서비스</td>
</tr>
</tbody></table>
<ul>
<li>React만 사용 → 무조건 CSR</li>
<li>Next.js 사용 → 페이지 단위로 CSR/SSR/SSG/ISR 선택 가능
즉, Next.js는 React의 렌더링 옵션을 확장한 프레임워크</li>
</ul>
<hr />
<h2 id="✅-언제-어떤-렌더링-방식을-써야-할까">✅ 언제 어떤 렌더링 방식을 써야 할까?</h2>
<table>
<thead>
<tr>
<th>상황</th>
<th>추천 렌더링 방식</th>
</tr>
</thead>
<tbody><tr>
<td>내부 대시보드, 관리자</td>
<td><strong>CSR</strong></td>
</tr>
<tr>
<td>블로그, 문서 사이트</td>
<td><strong>SSG</strong></td>
</tr>
<tr>
<td>뉴스, 쇼핑몰, 커뮤니티</td>
<td><strong>ISR</strong></td>
</tr>
<tr>
<td>SEO 중요 + 동적 페이지</td>
<td><strong>SSR</strong></td>
</tr>
</tbody></table>
<hr />
<h2 id="💬-결론">💬 결론</h2>
<p><strong>CSR은 브라우저 중심, SSR은 서버 중심, SSG는 정적 중심, ISR은 그 중간입니다.</strong>
Next.js의 강점은 <strong>페이지마다 가장 적합한 렌더링 방식을 선택해 조합할 수 있다는 점</strong>입니다.
즉, 단일 방식(CSR)에 머무르지 않고 클라이언트·서버·정적 렌더링을 상황에 맞게 활용할 수 있습니다.</p>
<p>React는 CSR만 가능하지만,
Next.js는 <strong>CSR, SSR, SSG, ISR을 페이지 단위로 선택하여 조합할 수 있는 프레임워크</strong>입니다.
서비스 성격에 따라 최적의 렌더링 방식을 설계하는 것이 Next.js의 가장 큰 장점입니다.</p>