<p>앞선 글에서는 <strong>웹 렌더링 방식(CSR · SSR · SSG · ISR)</strong> 의 개념과 차이를 정리했습니다.<br />이번 글에서는 그 내용을 바탕으로 <strong>Next.js에서 실제로 네 가지 렌더링 방식을 구현</strong>해보겠습니다.</p>
<p>Next.js는 13버전 이후 <strong>App Router</strong>가 공식 기준이며,<br />Pages Router는 레거시 구조지만 여전히 많은 프로젝트에서 사용되고 있습니다.
그래서 이번 문서에서는 <strong>App Router를 중심으로</strong>,  
<strong>Pages Router에서는 동일 방식이 어떻게 구현되었는지</strong> 간단한 참고 수준으로만 알아보겠습니다.</p>
<hr />
<h2 id="nextjs-렌더링-방식-결정-규칙app-router-기준">Next.js 렌더링 방식 결정 규칙(App Router 기준)</h2>
<p>Next.js(App Router)는 아래 규칙으로 렌더링 방식을 결정합니다.</p>
<table>
<thead>
<tr>
<th>규칙</th>
<th>렌더링 방식</th>
</tr>
</thead>
<tbody><tr>
<td><code>use client</code> 선언</td>
<td><strong>CSR</strong></td>
</tr>
<tr>
<td><code>fetch(..., { cache: &quot;no-store&quot; })</code> 또는 <code>dynamic=&quot;force-dynamic&quot;</code></td>
<td><strong>SSR</strong></td>
</tr>
<tr>
<td>정적 fetch (기본)</td>
<td><strong>SSG</strong></td>
</tr>
<tr>
<td><code>revalidate = N</code></td>
<td><strong>ISR</strong></td>
</tr>
</tbody></table>
<hr />
<h2 id="1-csr--ssr--ssg--isr-구현-app-router-기준">1. CSR / SSR / SSG / ISR 구현 (App Router 기준)</h2>
<h3 id="🌐-csr-client-side-rendering">🌐 CSR (Client Side Rendering)</h3>
<h4 id="✔-적용-조건">✔ 적용 조건</h4>
<ul>
<li>파일 상단에 <code>&quot;use client&quot;</code></li>
<li>브라우저에서 렌더링됨</li>
</ul>
<h4 id="✔-코드-예제">✔ 코드 예제</h4>
<pre><code class="language-tsx">&quot;use client&quot;;
import { useState, useEffect } from &quot;react&quot;;

export default function Page() {
  const [data, setData] = useState(null);

  useEffect(() =&gt; {
    fetch(&quot;/api/hello&quot;).then(r =&gt; r.json()).then(setData);
  }, []);

  return &lt;div&gt;CSR 데이터: {JSON.stringify(data)}&lt;/div&gt;;
}</code></pre>
<h4 id="✔-특징">✔ 특징</h4>
<ul>
<li>SEO 약함  </li>
<li>초기 렌더링 느릴 수 있음  </li>
<li>인터랙션 가장 빠름 (대시보드/관리자 페이지 최적)</li>
</ul>
<hr />
<h3 id="🖥-ssr-server-side-rendering">🖥 SSR (Server Side Rendering)</h3>
<h4 id="✔-적용-조건-1">✔ 적용 조건</h4>
<ul>
<li><code>dynamic = &quot;force-dynamic&quot;</code>  </li>
<li>또는 <code>cache: &quot;no-store&quot;</code></li>
</ul>
<h4 id="ssr이-되는이유">SSR이 되는이유:</h4>
<p><code>dynamic = &quot;force-dynamic&quot;</code>: <strong>이 페이지 전체를 &quot;동적 페이지&quot;로 강제</strong>, 내부 fetch가 캐싱되더라도 SSR로 처리됨
<code>no-store</code> : <strong>캐싱 금지</strong> -&gt; 매 요청 마다 fetch -&gt; 서버가 매번 렌더링</p>
<h4 id="✔-코드-예제-1">✔ 코드 예제</h4>
<pre><code class="language-tsx">export const dynamic = &quot;force-dynamic&quot;;

export default async function Page() {
  const data = await fetch(&quot;https://api.example.com&quot;, {
    cache: &quot;no-store&quot;,
  }).then(r =&gt; r.json());

  return &lt;div&gt;SSR 데이터: {data.title}&lt;/div&gt;;
}</code></pre>
<hr />
<h3 id="🏗-ssg-static-site-generation">🏗 SSG (Static Site Generation)</h3>
<h4 id="✔-적용-조건-2">✔ 적용 조건</h4>
<ul>
<li>서버 컴포넌트 기본 동작 (정적 fetch)</li>
<li><code>revalidate</code> 없음</li>
</ul>
<h4 id="ssg가-되는이유">SSG가 되는이유:</h4>
<p>기본적으로 캐시 = <code>force-cache</code>
빌드 타임(또는 최초 요청)에 한번 데이터를 가져옴, 그 결과를 <strong>캐싱해서 재사용</strong></p>
<h4 id="✔-코드-예제-2">✔ 코드 예제</h4>
<pre><code class="language-tsx">export const dynamic = &quot;force-static&quot;;

export default async function Page() {
  const post = await fetch(&quot;https://api.example.com/posts/1&quot;).then(r =&gt; r.json());
  return &lt;div&gt;SSG 데이터: {post.title}&lt;/div&gt;;
}</code></pre>
<h4 id="✔-특징-1">✔ 특징</h4>
<ul>
<li>빌드 시 HTML 생성됨</li>
<li>배포 후 서버 부하 0</li>
<li>데이터 변하면 <strong>재빌드 필요</strong></li>
</ul>
<hr />
<h3 id="🔁-isr-incremental-static-regeneration">🔁 ISR (Incremental Static Regeneration)</h3>
<h4 id="✔-적용-조건-3">✔ 적용 조건</h4>
<ul>
<li><code>export const revalidate = N</code></li>
</ul>
<h4 id="✔-코드-예제-3">✔ 코드 예제</h4>
<pre><code class="language-tsx">export const revalidate = 60; // 60초마다 재생성

export default async function Page() {
  const posts = await fetch(&quot;https://api.example.com/posts&quot;, {
    next: { revalidate: 60 },
  }).then(r =&gt; r.json());

  return &lt;div&gt;ISR 게시글 수: {posts.length}&lt;/div&gt;;
}</code></pre>
<hr />
<h2 id="📚-참고--pages-router에서는-어떻게-구현할까">📚 참고)  Pages Router에서는 어떻게 구현할까?</h2>
<p>App Router 이전에는 아래 방식으로 렌더링 방식을 결정했음.</p>
<table>
<thead>
<tr>
<th>렌더링 방식</th>
<th>Pages Router 방식</th>
</tr>
</thead>
<tbody><tr>
<td>CSR</td>
<td>모든 페이지 기본이 CSR</td>
</tr>
<tr>
<td>SSR</td>
<td><code>getServerSideProps()</code></td>
</tr>
<tr>
<td>SSG</td>
<td><code>getStaticProps()</code></td>
</tr>
<tr>
<td>ISR</td>
<td><code>getStaticProps()</code> + <code>revalidate</code></td>
</tr>
<tr>
<td>동적 정적 생성</td>
<td><code>getStaticPaths()</code></td>
</tr>
</tbody></table>
<h3 id="예시pages-router">예시(Pages Router)</h3>
<h4 id="✔-csr--기본-전체-csr-별도-함수-없음">✔ CSR — 기본 전체 CSR (별도 함수 없음)</h4>
<pre><code class="language-tsx">export default function Page() {
  return &lt;div&gt;여기는 CSR 페이지&lt;/div&gt;;
}</code></pre>
<h4 id="✔-ssr--getserversideprops">✔ SSR — getServerSideProps()</h4>
<pre><code class="language-tsx">export async function getServerSideProps() {
  const data = await fetch(&quot;https://api.example.com/data&quot;).then(r =&gt; r.json());
  return { props: { data } };
}

export default function Page({ data }) {
  return &lt;div&gt;SSR 데이터: {data.title}&lt;/div&gt;;
}</code></pre>
<h4 id="✔-ssg--getstaticprops">✔ SSG — getStaticProps()</h4>
<pre><code class="language-tsx">export async function getStaticProps() {
  const posts = await fetch(&quot;https://api.example.com/posts&quot;).then(r =&gt; r.json());
  return { props: { posts } };
}

export default function Page({ posts }) {
  return &lt;div&gt;SSG 데이터: {posts.length}&lt;/div&gt;;
}</code></pre>
<h4 id="✔-isr--getstaticprops--revalidate">✔ ISR — getStaticProps() + revalidate</h4>
<pre><code class="language-tsx">export async function getStaticProps() {
  const posts = await fetch(&quot;https://api.example.com/posts&quot;).then(r =&gt; r.json());
  return { props: { posts }, revalidate: 60 };
}</code></pre>
<hr />
<h2 id="app-router-vs-pages-router-구현-비교">App Router vs Pages Router 구현 비교</h2>
<table>
<thead>
<tr>
<th>항목</th>
<th>App Router</th>
<th>Pages Router</th>
</tr>
</thead>
<tbody><tr>
<td>CSR</td>
<td><code>&quot;use client&quot;</code></td>
<td>기본 CSR</td>
</tr>
<tr>
<td>SSR</td>
<td><code>cache: &quot;no-store&quot;</code> / <code>dynamic=&quot;force-dynamic&quot;</code></td>
<td><code>getServerSideProps()</code></td>
</tr>
<tr>
<td>SSG</td>
<td>기본 정적 fetch</td>
<td><code>getStaticProps()</code></td>
</tr>
<tr>
<td>ISR</td>
<td><code>revalidate = N</code></td>
<td><code>getStaticProps() + revalidate</code></td>
</tr>
<tr>
<td>서버 컴포넌트</td>
<td>기본 지원</td>
<td>없음</td>
</tr>
<tr>
<td>데이터 패칭</td>
<td>fetch 기반 캐싱 시스템</td>
<td>props 함수로 반환</td>
</tr>
<tr>
<td>파일 구조</td>
<td><code>app/page.tsx</code> 중심</td>
<td><code>pages/xxx.tsx</code> 중심</td>
</tr>
</tbody></table>
<hr />
<h2 id="2-빌드-후-어떤-파일이-생성되는가">2. 빌드 후 어떤 파일이 생성되는가?</h2>
<p>Next.js에서 next build를 실행하면 렌더링 방식에 따라 만들어지는 파일이 다릅니다.</p>
<table>
<thead>
<tr>
<th>방식</th>
<th>빌드 시 HTML 생성</th>
<th>빌드 시 JS 생성</th>
<th>HTML 생성 시점</th>
<th>JS 실행 위치</th>
<th>hydration 발생 여부</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td><strong>CSR</strong></td>
<td>⚠️ Shell 1개만 생성</td>
<td>✔ 클라이언트 JS</td>
<td>브라우저가 HTML 생성</td>
<td>클라이언트</td>
<td>❌ 없음 (초기 렌더)</td>
<td>SPA 방식. HTML은 브라우저에서 JS로 생성</td>
</tr>
<tr>
<td><strong>SSR</strong></td>
<td>❌ 없음</td>
<td>✔ 서버 JS + 클라이언트 JS</td>
<td>요청마다 서버 렌더링</td>
<td>서버 + 클라이언트</td>
<td>⚠️ 클라이언트 컴포넌트 있을 때만</td>
<td>SEO 좋음. 서버 비용 존재</td>
</tr>
<tr>
<td><strong>SSG</strong></td>
<td>✔ 페이지 수만큼 HTML 생성</td>
<td>✔ 클라이언트 JS + 서버 JS(빌드 타임)</td>
<td>빌드 타임</td>
<td>서버(HTML) + 클라이언트(JS)</td>
<td>⚠️ 클라이언트 컴포넌트 있을 때만</td>
<td>가장 빠른 초기 로딩. 데이터 변하면 재빌드</td>
</tr>
<tr>
<td><strong>ISR</strong></td>
<td>✔ 페이지 수만큼 HTML 생성</td>
<td>✔ 클라이언트 JS + 서버 JS</td>
<td>빌드 타임 + 재생성 시점</td>
<td>서버 + 클라이언트</td>
<td>⚠️ 클라이언트 컴포넌트 있을 때만</td>
<td>SSG + 자동 갱신. 실무에서 많이 사용</td>
</tr>
</tbody></table>
<ul>
<li><p>CSR: HTML은 루트 shell만 존재 / 모든 UI 생성은 브라우저에서 JS가 직접 처리<br />→ 클라이언트 JS만 사용</p>
</li>
<li><p>SSR: 빌드 시 HTML 없음 / 요청마다 서버 JS가 HTML을 즉석 생성<br />→ 서버 JS: HTML 생성<br />→ 클라이언트 JS: hydration</p>
</li>
<li><p>SSG: 빌드 타임에 모든 페이지 HTML 생성됨<br />→ 서버 JS: 빌드 타임에만 HTML 생성<br />→ 클라이언트 JS: hydration</p>
</li>
<li><p>ISR: SSG처럼 HTML 생성 + 일정 시간이 지나면 서버 JS가 새 HTML을 다시 생성<br />→ 서버 JS: 재생성 시점에 HTML 생성<br />→ 클라이언트 JS: hydration</p>
</li>
</ul>
<hr />
<h2 id="⚠️-use-client는-csr을-강제하는-것은-아님">⚠️ use client는 CSR을 “강제”하는 것은 아님</h2>
<p><code>use client</code>는 단순히
<strong>“이 컴포넌트는 브라우저에서 실행될 JS가 필요하다”</strong>는 의미일 뿐,
이 페이지 전체가 CSR이 된다는 뜻은 아닙니다.</p>
<p>페이지 전체가 &quot;use client&quot;면 → 전체 CSR</p>
<p>서버 컴포넌트 안에 &quot;use client&quot; 컴포넌트를 포함하면 → SSR + CSR 혼합 구조</p>
<p>즉,
<strong>use client = 클라이언트 컴포넌트 사용
CSR = 페이지 전체가 브라우저에서 렌더링</strong></p>
<p>이 둘은 다른 개념으로,
use client가 있다고 해서 그 페이지가 CSR만 되는 것은 아닙니다.</p>
<h3 id="예시">예시:</h3>
<p>1) 페이지 전체가 CSR인 경우</p>
<pre><code class="language-tsx">&quot;use client&quot;;

export default function Page() {
  return (
    &lt;div&gt;
      &lt;h1&gt;전체 CSR 페이지&lt;/h1&gt;
      &lt;button onClick={() =&gt; alert(&quot;click&quot;)}&gt;Click!&lt;/button&gt;
    &lt;/div&gt;
  );
}</code></pre>
<ul>
<li>맨 위 <code>&quot;use client&quot;</code> → 이 페이지 전체가 CSR</li>
<li>HTML은 빌드 시 생성되지 않음</li>
<li>브라우저가 JS로 화면을 그림</li>
</ul>
<p>2) SSR 페이지 안에 클라이언트 컴포넌트를 포함한 경우 (혼합 구조)</p>
<pre><code class="language-tsx">import Counter from &quot;./Counter&quot;; // 클라이언트 컴포넌트

export default function Page() {
  const data = await fetch(&quot;https://api.example.com&quot;, { cache: &quot;no-store&quot; })
    .then(res =&gt; res.json());

  return (
    &lt;div&gt;
      &lt;h1&gt;SSR로 렌더링된 데이터: {data.title}&lt;/h1&gt;
      &lt;Counter /&gt;   {/* 클라이언트 컴포넌트 */}
    &lt;/div&gt;
  );
}</code></pre>
<pre><code class="language-tsx">&quot;use client&quot;;

import { useState } from &quot;react&quot;;

export default function Counter() {
  const [n, setN] = useState(0);
  return &lt;button onClick={() =&gt; setN(n+1)}&gt;Count: {n}&lt;/button&gt;;
}
</code></pre>
<ul>
<li>페이지 전체는 SSR로 HTML을 만들어서 내려옴</li>
<li>하지만 <code>&lt;Counter /&gt;</code>만 클라이언트 JS가 붙어서(hydration)
브라우저에서 동작</li>
<li>원래 전체 CSR 방식에서는 hydration이 일어나지 않지만,
지금은 &quot;SSR로 생성된 HTML 위에 클라이언트 컴포넌트가 포함된 구조&quot;이기 때문에 hydration이 발생함</li>
</ul>
<hr />
<h2 id="3-배포-시-어떻게-동작할까">3. 배포 시 어떻게 동작할까?</h2>
<p>렌더링 방식(CSR / SSR / SSG / ISR)에 따라
어디에 배포하느냐에 따라 “실제로 어떻게 동작하는지”가 달라집니다.</p>
<p>아래는 가장 많이 쓰는 3가지 배포 환경 기준 정리입니다.</p>
<h3 id="✔-vercel에-배포할-때-nextjs-공식-추천">✔ Vercel에 배포할 때 (Next.js 공식 추천)</h3>
<p>Vercel은 <strong>Next.js를 만든 회사가 운영하는 공식 호스팅 플랫폼</strong>으로<br /><strong>CSR / SSR / SSG / ISR을 아무 설정 없이 지원</strong>합니다.</p>
<h3 id="렌더링-방식별-실제-동작">렌더링 방식별 실제 동작</h3>
<h4 id="①-csr"><strong>① CSR</strong></h4>
<ul>
<li>빌드 결과: JS 번들(<code>_next/static/...</code>) 위주</li>
<li>HTML은 빈 shell 형태</li>
<li>전 세계 Edge CDN에 JS가 배포됨</li>
<li>사용자가 접속하면:<ul>
<li>가장 가까운 Edge 서버에서 HTML shell + JS 응답</li>
<li>브라우저가 JS 실행 → React가 DOM 생성</li>
</ul>
</li>
</ul>
<hr />
<h4 id="②-ssr"><strong>② SSR</strong></h4>
<ul>
<li>SSR 페이지는 빌드 시 “서버리스 함수(Function)”로 컴파일됨</li>
<li>사용자가 <code>/product/1</code> 요청 시:<ul>
<li>해당 페이지의 서버리스 함수 실행</li>
<li>서버에서 즉석으로 HTML 생성하여 전송</li>
</ul>
</li>
<li>JS는 CDN에서 다운 → hydration 실행</li>
</ul>
<p>→ SEO 최강, 동적 페이지에 최적</p>
<hr />
<h4 id="③-isr"><strong>③ ISR</strong></h4>
<ul>
<li>최초 빌드 시 SSG와 동일하게 <strong>HTML + JS 생성 후 CDN에 배포</strong></li>
<li>이후 <code>revalidate: 60</code> 같은 설정에 따라 동작:</li>
</ul>
<h4 id="🔄-재생성-흐름">🔄 재생성 흐름</h4>
<ol>
<li>60초 안 → 기존 HTML 그대로 제공  </li>
<li>60초 후 첫 요청 발생 →  <ul>
<li>Vercel이 <strong>백그라운드에서 새 HTML 렌더링</strong></li>
<li>렌더링이 끝나면 CDN 파일을 새 버전으로 교체  </li>
</ul>
</li>
<li>다음 요청부턴 새 HTML 제공</li>
</ol>
<p>→ <strong>자동 최신화 + 초고속 초기 로딩</strong></p>
<hr />
<h4 id="④-ssg"><strong>④ SSG</strong></h4>
<ul>
<li>빌드 시 <strong>페이지별 완성된 HTML 생성</strong></li>
<li>정적 HTML + JS/CSS 모두 Edge CDN에 배포</li>
<li>사용자가 <code>/blog/1</code> 같은 페이지 요청 시:<ul>
<li><strong>CDN에서 완성 HTML 바로 제공</strong></li>
<li>이후 JS 로드 후 hydration</li>
</ul>
</li>
</ul>
<p>→ 초기 로딩 속도 최강</p>
<blockquote>
<p>페이지별로 렌더링 전략만 선택하면,<br /><strong>Vercel이 알아서 가장 효율적인 방식으로 배포/실행해준다.</strong></p>
</blockquote>
<hr />
<h3 id="✔-aws-s3--cloudfront에-배포할-때">✔ AWS S3 + CloudFront에 배포할 때</h3>
<p>S3 + CloudFront는 <strong>정적 호스팅(Static Hosting)</strong> 환경입니다.</p>
<p> 즉,<br /><strong>파일만 줄 수 있고 “HTML을 서버에서 만들어줄 수는 없음”.</strong></p>
<p>그래서:</p>
<ul>
<li><strong>CSR / SSG → 가능</strong></li>
<li><strong>ISR / SSR → 불가능(별도 서버 필요)</strong></li>
</ul>
<hr />
<h2 id="csr--ssg가-잘-맞는-이유">CSR / SSG가 잘 맞는 이유</h2>
<ol>
<li><p><code>next build</code> 후<br /><code>next export</code> 또는 <code>output: 'export'</code>로  
정적 파일을 추출한다.</p>
<p>생성되는 파일들:</p>
<ul>
<li>HTML</li>
<li>JS, CSS</li>
<li>이미지 등 정적 리소스</li>
</ul>
</li>
<li><p>이걸 S3에 올리고 CloudFront로 CDN 구성</p>
</li>
</ol>
<h4 id="🔍-어떻게-동작할까">🔍 어떻게 동작할까?</h4>
<ul>
<li><strong>S3 → 단순 파일 제공</strong></li>
<li><strong>CloudFront → 전 세계 CDN 캐싱</strong></li>
</ul>
<p>CSR:</p>
<ul>
<li>index.html + JS만 있으면 되므로 완벽하게 맞는 구조</li>
</ul>
<p>SSG:</p>
<ul>
<li>미리 만들어진 HTML 그대로 제공하므로 적합</li>
</ul>
<hr />
<h2 id="그럼-왜-ssr--isr은-안-되나">그럼 왜 SSR / ISR은 안 되나?</h2>
<p>SSR / ISR은 공통적으로<br /><strong>“HTML을 서버가 실시간 또는 주기적으로 생성”</strong>해야 합니다.</p>
<p>그러나</p>
<ul>
<li>S3는 “파일 창고”일 뿐, 서버처럼 JS를 실행해 HTML을 생성할 수 없습니다.</li>
</ul>
<h3 id="정리">정리:</h3>
<ul>
<li>CSR   → 브라우저가 렌더링   → 서버 필요 없음 → S3 가능</li>
<li>SSG   → 빌드 시 렌더링     → 서버 필요 없음 → S3 가능</li>
<li>SSR   → 요청마다 서버 렌더링 → 서버 필요함     → S3 불가능</li>
<li>ISR   → 조건 시 서버 렌더링 → 서버 필요함     → S3 불가능</li>
</ul>
<hr />
<h2 id="✔-node-서버-배포-next-start">✔ Node 서버 배포 (<code>next start</code>)</h2>
<p>가장 직접적인 방식(전통적 배포)입니다.</p>
<h3 id="배포-방식">배포 방식</h3>
<ol>
<li>서버/도커에 코드 업로드</li>
<li><code>next build</code></li>
<li><code>next start</code>로 Node 서버 실행</li>
<li>필요하면 Nginx 프록시 사용</li>
</ol>
<h3 id="이-경우-지원되는-방식">이 경우 지원되는 방식</h3>
<p>Node 서버 한 대가<br />CSR / SSR / SSG / ISR <strong>모두 처리</strong>한다.</p>
<p>예:</p>
<ul>
<li>CSR → 정적 JS 서빙</li>
<li>SSG → 빌드된 HTML 서빙</li>
<li>ISR → 주기적 HTML 재생성 로직 실행</li>
<li>SSR → 요청 시 React 서버 렌더링</li>
</ul>
<h3 id="장점">장점</h3>
<ul>
<li>모든 방식 100% 지원  </li>
<li>AWS/Fargate/EC2/온프레미스 등 어디든 배포 가능</li>
</ul>
<h3 id="단점">단점</h3>
<ul>
<li>서버 운영, 스케일링을 직접 해야 함<br />(Vercel과 가장 큰 차이점)</li>
</ul>
<hr />
<h2 id="정리-1">정리:</h2>
<p>⭐ Vercel → Next.js 쓰면 가장 많이 선택됨. 기능 100% 자동 처리. (표준)</p>
<p>Node 서버(next start) → 회사 정책상 외부 호스팅 불가하거나 내부망 서버 필요할 때.</p>
<p>S3+CloudFront → SSR/ISR 없는 정적 사이트일 때만 선택.</p>
<hr />
<h2 id="🧾-배포-환경별-렌더링-지원-정리">🧾 배포 환경별 렌더링 지원 정리</h2>
<table>
<thead>
<tr>
<th>환경</th>
<th>CSR</th>
<th>SSG</th>
<th>ISR</th>
<th>SSR</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td><strong>Vercel</strong></td>
<td>✔</td>
<td>✔</td>
<td>✔ (자동 지원)</td>
<td>✔ (서버리스)</td>
<td>Next 공식 호스팅, 설정 최소</td>
</tr>
<tr>
<td><strong>S3 + CloudFront</strong></td>
<td>✔</td>
<td>✔</td>
<td>❌ 별도 구현 필요</td>
<td>❌ 서버 필요</td>
<td>정적 호스팅 전용</td>
</tr>
<tr>
<td><strong>Node 서버(next start)</strong></td>
<td>✔</td>
<td>✔</td>
<td>✔</td>
<td>✔</td>
<td>100% 지원하지만 인프라 직접 관리</td>
</tr>
</tbody></table>
<hr />
<h2 id="✅-정리">✅ 정리</h2>
<p><strong>Next.js App Router에서 렌더링 방식은 코드로 결정 됩니다.</strong></p>
<ul>
<li><code>&quot;use client&quot;</code> → <strong>CSR</strong></li>
<li><code>fetch(..., { cache: &quot;no-store&quot; })</code><br />or <code>export const dynamic = &quot;force-dynamic&quot;</code> → <strong>SSR</strong></li>
<li>기본 fetch(정적) → <strong>SSG</strong></li>
<li><code>export const revalidate = N(n초)</code> → <strong>ISR</strong></li>
</ul>
<h3 id="그리고-어디에-배포하느냐에-따라-가능한-것도-달라집니다">그리고 “어디에 배포하느냐”에 따라 가능한 것도 달라집니다:</h3>
<ul>
<li><strong>Vercel</strong> → 4개 방식 모두 자동 지원 (가장 쉬움)</li>
<li><strong>S3 + CloudFront</strong> → CSR + SSG 전용</li>
<li><strong>Node 서버</strong> → 모든 방식 가능하지만 운영 난이도 ↑</li>
</ul>
<hr />
<h2 id="💬-결론">💬 결론</h2>
<p>이번 글에서는 Next.js에서 <strong>CSR · SSR · SSG · ISR을 실제 코드로 구현</strong>하며<br />각 방식이 어떤 기준으로 동작하는지 직접 확인해보았습니다.</p>
<p>실습을 해보니  <strong>페이지에 어떤 코드를 작성하느냐가 곧 렌더링 방식을 결정한다</strong>는 점을 확실히 이해할 수 있었습니다.</p>
<p>또한 렌더링 방식은 코드뿐 아니라<br /><strong>배포 환경에 따라 지원 여부가 달라진다</strong>는 점도 중요한 부분이었습니다.<br />실무에서는 페이지 성격에 맞게 여러 렌더링 방식을 자연스럽게 섞어 사용한다는 것도 알게 되었고,</p>
<ul>
<li>정적 페이지 → <strong>SSG / ISR</strong>  </li>
<li>동적·데이터 의존 페이지 → <strong>SSR</strong>  </li>
<li>사용자 중심 화면(마이페이지·관리자) → <strong>CSR</strong></li>
</ul>
<p>이런 패턴이 많이 쓰인다는 것도 확인할 수 있었습니다.</p>
<p>이전에는 “그냥 Vercel에 올리면 된다” 정도로만 생각했지만,<br />S3·CloudFront·Node 서버 같은 배포 환경을 비교해보면서<br /><strong>배포 구조에 따라 화면이 렌더링되는 방식 자체가 달라진다</strong>는 점을 새롭게 배웠습니다.</p>
<p>이번 글을 통해 렌더링과 배포 흐름을 전체적으로 정리할 수 있었고,<br />앞으로는 서버와 인프라 쪽도 함께 공부해야겠다는 생각이 들었습니다.</p>