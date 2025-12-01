<p>React, Vue, Angular 등 현대 프론트엔드 프레임워크들은<br />모두 <strong>SPA(Single Page Application)</strong> 방식을 기반으로 동작합니다.  </p>
<p>반면, 전통적인 웹사이트 즉, <strong>MPA(Multi Page Application)</strong> 는<br />브라우저가 페이지를 <strong>전부 새로 불러오는 구조</strong>로 작동합니다.  </p>
<p>이번 글에서는 <strong>React를 이해하기 전에</strong>,  
그 근간이 되는 <strong>SPA의 작동 원리와 MPA와의 차이</strong>를 정리해보겠습니다.  </p>
<blockquote>
<p>“왜 SPA는 새로고침 없이 화면이 바뀔까?”<br />“브라우저는 SPA와 MPA를 어떻게 다르게 처리할까?”  </p>
</blockquote>
<hr />
<h2 id="🌐-전통적인-브라우저-페이지-동작-mpa-방식">🌐 전통적인 브라우저 페이지 동작 (MPA 방식)</h2>
<p>과거 대부분의 웹사이트는 “페이지마다 별도의 HTML”로 구성되었습니다.
링크를 클릭하면 브라우저는 다음 과정을 거칩니다.</p>
<h3 id="🔹-페이지-전환-흐름">🔹 페이지 전환 흐름</h3>
<ol>
<li>사용자가 <code>&lt;a href=&quot;/about&quot;&gt;</code> 링크 클릭  </li>
<li>브라우저가 서버에 <strong>새 HTML 문서 요청</strong></li>
<li>서버는 <code>/about</code> 페이지의 HTML, JS, CSS를 응답</li>
<li>브라우저는 현재 페이지의 <strong>JS 런타임을 완전히 종료(unload)</strong>  </li>
<li>새 HTML 문서를 파싱하고, JS를 다시 실행하여 <strong>새 런타임 생성</strong></li>
</ol>
<p>즉, 한 페이지 이동마다:</p>
<ul>
<li>HTML → 새로 다운로드  </li>
<li>JS → 새로 실행  </li>
<li>메모리(import 캐시, 변수 등) → 전부 초기화  </li>
</ul>
<blockquote>
<p> MPA의 핵심: “<strong>페이지 이동 = 새 문서 로드</strong>”</p>
</blockquote>
<h3 id="💡-참고-캐시는-존재하지만-상태는-유지되지-않는다">💡 참고: 캐시는 존재하지만 ‘상태’는 유지되지 않는다</h3>
<p>MPA는 페이지를 이동할 때마다 <strong>현재 JS 런타임이 완전히 사라집니다.</strong><br />전역 변수, 이벤트 핸들러, 타이머 등이 모두 초기화되고<br />이전 페이지로 돌아가면 HTML과 JS를 다시 실행해야 합니다.  </p>
<p>다만, <strong>HTTP 캐시</strong> 덕분에 CSS·JS·이미지 등의 <strong>정적 리소스는 재다운로드하지 않을 수도 있습니다.</strong><br />하지만 이는 <strong>서버의 Cache-Control 설정이 있을 때만</strong> 가능합니다. </p>
<hr />
<h2 id="⚛️-spasingle-page-application의-원리">⚛️ SPA(Single Page Application)의 원리</h2>
<p>SPA는 이름 그대로 “한 개의 HTML 문서<code>(/index.html)</code>”로 동작하는 애플리케이션입니다.  </p>
<p>과거 MPA 방식에서는 페이지를 이동할 때마다
HTML을 다시 요청하고, JS 런타임을 새로 초기화해야 했습니다.
이로 인해 매번 <strong>렌더링 비용이 크고</strong>,
사용자 입장에서는 <strong>화면이 깜빡이거나 끊기는 UX 문제</strong>가 발생했습니다.</p>
<p>그래서 등장한 개념이 바로 SPA (Single Page Application) 입니다.
“한 번 로드된 런타임을 계속 유지하면서,
필요한 데이터만 바꿔서 화면을 갱신하자”라는 아이디어에서 시작되었습니다.</p>
<blockquote>
<p> SPA의 핵심: “<strong>페이지 이동 = JS가 DOM만 교체</strong>”</p>
</blockquote>
<h3 id="🔹-페이지-전환-흐름-spa">🔹 페이지 전환 흐름 (SPA)</h3>
<ol>
<li>첫 진입 시 <code>index.html</code> 단 하나의 문서 로드  </li>
<li>React/Vue가 <strong>JS로 라우팅을 관리</strong></li>
<li>사용자가 URL을 변경하면<br />→ 브라우저는 실제로 새 HTML을 요청하지 않고<br />→ JS가 <strong>DOM을 교체(Render)</strong> 하여 화면만 바꿈</li>
</ol>
<p>이때 React/Vue 같은 프레임워크는<br />현재 화면의 <strong>Virtual DOM(가상 DOM)</strong> 과<br />새로 렌더링해야 할 Virtual DOM을 <strong>비교(diff)</strong> 하여<br /><strong>달라진 부분만 실제 DOM에 반영(patch)</strong> 합니다.<br />즉, 페이지 전체를 다시 그리는 대신<br /><strong>변경된 요소만 효율적으로 교체</strong>하여 렌더링 성능을 극대화합니다</p>
<blockquote>
<p>즉, <strong>URL은 바뀌지만 문서는 그대로 유지</strong>되며,<br />JS 런타임(import 캐시, 상태, 메모리 등)도 그대로 유지됩니다.</p>
</blockquote>
<hr />
<h2 id="🧠-왜-spa는-빠를까">🧠 왜 SPA는 빠를까?</h2>
<ul>
<li>문서 전체를 새로 요청하지 않음  </li>
<li>CSS, JS, 이미지 등 이미 로드된 리소스를 재사용  </li>
<li>화면 갱신은 <strong>Virtual DOM / Diff 알고리즘</strong>으로 최소화  </li>
</ul>
<blockquote>
<p>따라서 SPA는 <strong>JS가 브라우저 안에서 일하는 양은 많지만</strong>,  
<strong>서버의 부담은 줄고</strong>, 네트워크와 렌더링 비용이 크게 감소합니다.<br />즉, “서버는 덜 일하고, 브라우저(JS)는 더 일하는 구조”입니다.</p>
</blockquote>
<h2 id="⚠️-spa의-단점">⚠️ SPA의 단점</h2>
<ul>
<li>첫 진입 시 <strong>JS 번들이 커서 초기 로딩이 느려질 수 있음</strong>  </li>
<li><strong>SEO(검색 엔진 최적화)</strong> 를 위해 서버 렌더링(SSR)이 필요  </li>
<li><strong>브라우저 메모리 점유율</strong>이 상대적으로 높아짐 </li>
</ul>
<hr />
<h2 id="🔍-mpa-vs-spa-구조-비교">🔍 MPA vs SPA 구조 비교</h2>
<table>
<thead>
<tr>
<th>항목</th>
<th>MPA (전통적인 웹)</th>
<th>SPA (React, Vue 등)</th>
</tr>
</thead>
<tbody><tr>
<td><strong>HTML 문서 수</strong></td>
<td>페이지마다 별도 문서 (/home.html, /about.html 등)</td>
<td>단 하나의 <code>index.html</code></td>
</tr>
<tr>
<td>*<em>페이지 이동 시 *</em></td>
<td>새 HTML 문서 요청 → 새로 렌더링(전체 새로고침)</td>
<td>같은 HTML 유지 -&gt; JS로 DOM 교체 (내용만 변경)</td>
</tr>
<tr>
<td><strong>JS 런타임</strong></td>
<td>페이지마다 새로 생성</td>
<td>한 번만 생성되어 계속 유지</td>
</tr>
<tr>
<td><strong>import 캐시</strong></td>
<td>이동 시 초기화됨</td>
<td>이동해도 유지됨</td>
</tr>
<tr>
<td><strong>속도 체감</strong></td>
<td>느림 (매번 전체 리로드)</td>
<td>빠름 (필요한 부분만 갱신)</td>
</tr>
<tr>
<td><strong>SEO</strong></td>
<td>유리</td>
<td>불리 (SSR로 보완 가능)</td>
</tr>
<tr>
<td><strong>UX 특징</strong></td>
<td>깜빡이며 새로고침</td>
<td>부드럽게 전환 (앱처럼)</td>
</tr>
</tbody></table>
<hr />
<h2 id="react-router의-동작-구조">React Router의 동작 구조</h2>
<p>전통적인 <code>&lt;a href=&quot;/about&quot;&gt;</code> 링크를 클릭하면<br />브라우저는 <strong>서버에 새 HTML 문서를 요청</strong>하고<br />현재 페이지를 완전히 <strong>리로드(unload)</strong> 합니다. </p>
<p>하지만 <strong>React Router</strong>는 이 기본 동작을 그대로 두지 않습니다.<br />대신 <code>&lt;a&gt;</code> 태그 클릭 시 발생하는 기본 동작(<code>document</code> 리로드)을<br /><strong>가로채서(<code>preventDefault</code>) 막고</strong>,  
“브라우저 주소창은 바꾸되, 실제로는 새 HTML을 요청하지 않는” 방식으로 작동합니다.</p>
<p>그 대신 내부적으로는 다음과 같은 과정을 거칩니다 👇  </p>
<ul>
<li>JS에서 <code>history.pushState()</code> 로 <strong>URL을 변경</strong></li>
<li>React가 “현재 경로에 맞는 컴포넌트를 렌더링할지” <strong>결정</strong>  </li>
<li><strong>DOM 일부만 갱신</strong>하여 화면을 새로 만듭니다  </li>
</ul>
<hr />
<h3 id="🔹-실제-동작-예시">🔹 실제 동작 예시</h3>
<pre><code class="language-tsx">&lt;Link to=&quot;/about&quot;&gt;About&lt;/Link&gt;</code></pre>
<p>이 코드를 클릭하면, 내부적으로는 다음과 같은 일이 일어납니다:</p>
<pre><code class="language-tsx">// 브라우저의 기본 페이지 이동을 막고
event.preventDefault();

// 브라우저 주소(URL)만 변경
window.history.pushState({}, '', '/about');

// React가 해당 경로에 맞는 컴포넌트를 렌더링
render(&lt;AboutPage /&gt;);
</code></pre>
<h3 id="✅-결과적으로">✅ 결과적으로</h3>
<ul>
<li>HTML 문서는 새로 로드되지 않습니다.</li>
<li>브라우저의 URL과 React 렌더링 결과만 교체됩니다.</li>
<li>JS 런타임과 상태(state)는 그대로 유지됩니다.</li>
</ul>
<p>즉, React Router는 &quot;진짜 페이지 이동&quot;을 흉내 내되,
실제로는 JS가 URL만 바꾸고 컴포넌트를 교체하는 방식으로 동작합니다.</p>
<hr />
<h2 id="js-런타임-관점에서-본-차이">JS 런타임 관점에서 본 차이</h2>
<table>
<thead>
<tr>
<th>구분</th>
<th>브라우저 동작</th>
<th>JS 런타임</th>
<th>import 캐시</th>
</tr>
</thead>
<tbody><tr>
<td><strong>새로고침(F5)</strong></td>
<td>새 문서 로드</td>
<td>🔄 재시작</td>
<td>❌ 초기화</td>
</tr>
<tr>
<td><strong><code>&lt;a&gt;</code> 이동</strong></td>
<td>새 문서 로드</td>
<td>🔄 재시작</td>
<td>❌ 초기화</td>
</tr>
<tr>
<td><strong>React Router 내부 이동</strong></td>
<td>문서 그대로</td>
<td>✅ 유지</td>
<td>✅ 유지</td>
</tr>
</tbody></table>
<p>SPA 내부 라우팅은 JS 런타임이 끊기지 않기 때문에
<code>import()</code>로 불러온 청크 모듈, 전역 상태, Context 등도 그대로 유지됩니다.</p>
<h2 id="브라우저-입장에서-본-차이">브라우저 입장에서 본 차이</h2>
<pre><code class="language-text">MPA 방식
┌────────────────────────────┐
│ /home  -&gt; /about 이동    │
│ 1. /home JS 종료         │
│ 2. /about HTML 로드      │
│ 3. JS 새로 실행           │
└────────────────────────────┘</code></pre>
<pre><code class="language-text">SPA 방식
┌────────────────────────────┐
│ /home -&gt; /about 이동     │
│ 1. 같은 HTML 유지         │
│ 2. JS가 DOM만 교체        │
│ 3. 런타임 유지            │
└────────────────────────────┘ </code></pre>
<hr />
<h2 id="💬-결론">💬 결론</h2>
<blockquote>
<p><strong>MPA</strong>는 <strong>서버가 매번 새로운 HTML을 내려주는 구조</strong>로 단순하지만,
매 이동마다 <strong>JS 런타임이 새로 생성</strong>되어 느립니다.</p>
</blockquote>
<blockquote>
<p><strong>SPA</strong>는 <strong>서버가 한 번만 HTML을 내려주고</strong>,
이후에는 <strong>브라우저(JS)가 Virtual DOM을 통해 화면을 갱신</strong>하기 때문에
상태와 런타임이 유지되며 훨씬 빠르게 동작합니다</p>
</blockquote>