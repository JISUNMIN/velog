<p>이 문서에서는 웹 인증 과정에서 자주 등장해 헷갈리기 쉬운(제가 헷갈려요) <strong>JWT</strong>, <strong>Bearer</strong>, <strong>access_token</strong>, <strong>refresh_token</strong>,  
<strong>쿠키·localStorage·메모리 저장 방식</strong>, <strong>Session 방식</strong>, 그리고 <strong>세션 토큰</strong> 개념을 명확히 정리해봤습니다.</p>
<hr />
<h2 id="1-인증의-큰-흐름-이해하기">1. 인증의 큰 흐름 이해하기</h2>
<p>웹에서 로그인 관련 작업은 크게 두 단계로 나뉩니다.</p>
<ol>
<li><strong>Authentication (인증)</strong> — 👤 <strong>누구인지 확인하기</strong>: 사용자가 정말 그 사람인지 확인합니다.  </li>
<li><strong>Authorization &amp; Session 유지</strong> — 🔐 <strong>권한주고 유지하기</strong>: 인증된 사용자가 로그인 상태를 유지하고, 권한대로 행동할 수 있도록 관리합니다.</li>
</ol>
<p>이 두 단계 과정에서 아래 개념들이 자연스럽게 등장합니다:</p>
<ul>
<li>세션(session)  </li>
<li>쿠키(cookie)  </li>
<li>JWT(JSON Web Token)  </li>
<li>access_token / refresh_token  </li>
<li>저장 방식(localStorage, cookie, in-memory)  </li>
<li>Opaque Token  </li>
<li>id_token, API Key 등  </li>
</ul>
<hr />
<h2 id="2-jwtjson-web-token">2. JWT(JSON Web Token)</h2>
<h3 id="✔-무엇인가">✔ 무엇인가?</h3>
<p>JWT는 <strong>토큰의 모양(포맷)</strong> 입니다. 즉, “토큰이 어떤 구조로 생겼냐?”를 정의한 규격입니다. =&gt; <code>&quot;토큰이 어떤 모양인가&quot;</code></p>
<pre><code>xxxxx.yyyyy.zzzzz
Header.Payload.Signature</code></pre><h3 id="구조">구조</h3>
<ul>
<li><strong>Header</strong> — 어떤 알고리즘으로 서명했는지  </li>
<li><strong>Payload</strong> — 유저 정보, 권한, 만료 시간(exp) 등  </li>
<li><strong>Signature</strong> — 위조 방지를 위한 서명값  </li>
</ul>
<h3 id="✔-어디에-쓰는가">✔ 어디에 쓰는가?</h3>
<ul>
<li>access_token 용도로 가장 널리 사용됨  </li>
<li>서버가 상태를 저장하지 않는 <strong>Stateless 인증</strong>에 적합  <blockquote>
<p>Stateless = 서버가 아무 상태도 보관하지 않고, 요청마다 인증 정보를 다시 받아 확인하는 방식</p>
</blockquote>
</li>
</ul>
<h3 id="✔-어디에서-많이-쓰는가">✔ 어디에서 많이 쓰는가?</h3>
<ul>
<li>access_token 구현 방식으로 가장 널리 사용됨</li>
<li>클라이언트가 API 서버에 인증할 때 (웹·모바일 공통)</li>
<li>OAuth의 id_token  </li>
<li>서버가 상태를 저장하지 않는 Stateless 환경</li>
</ul>
<h3 id="✔-중요한-포인트">✔ 중요한 포인트</h3>
<ul>
<li>JWT는 <strong>암호화된 것이 아니라 서명(Signature)된 것</strong>이다.<br />→ payload는 Base64 디코딩하면 누구나 볼 수 있음  </li>
<li>민감한 정보 저장 금지  </li>
<li>JWT는 <strong>포맷</strong>일 뿐, *<em>저장 방식은 쿠키/스토리지/메모리 중 아무거나 사용 가능  *</em></li>
</ul>
<hr />
<h2 id="3-bearer">3. Bearer</h2>
<h3 id="✔-무엇인가-1">✔ 무엇인가?</h3>
<p>Bearer는 <strong>인증 토큰을 전송하는 방식(스킴)</strong> 입니다. =&gt; <code>&quot;전송 방식&quot;</code></p>
<pre><code>Authorization: Bearer &lt;token&gt;</code></pre><ul>
<li>JWT, Opaque Token, access_token 등 모든 종류의 토큰 전달 가능</li>
<li>토큰을 헤더에 넣어 보내기 위한 가장 표준적인 방식</li>
<li>API 인증에서 가장 흔하게 사용됨  </li>
</ul>
<h3 id="✔-어디에서-많이-쓰는가-1">✔ 어디에서 많이 쓰는가?</h3>
<p><strong>클라이언트가 서버 API에 인증 정보를 전달할 때 거의 표준처럼 사용됩니다.</strong></p>
<ul>
<li>REST API  </li>
<li>GraphQL API  </li>
<li>OAuth 기반 access_token 인증</li>
</ul>
<h3 id="🔗-jwt와-bearer의-관계">🔗 jwt와 Bearer의 관계</h3>
<p>Bearer는 <code>“전송 방식”</code>이라 JWT가 아닌 토큰도 얼마든지 실어 보낼 수 있다.
JWT는 Bearer에서 쓰이는 <code>여러 토큰 중 하나</code>일 뿐이다.</p>
<hr />
<h2 id="4-💾-token-저장-방식-쿠키-·-localstorage-·-메모리">4. 💾 Token &quot;저장 방식&quot; (쿠키 · localStorage · 메모리)</h2>
<h3 id="🍪-쿠키cookie">🍪 쿠키(Cookie)</h3>
<ul>
<li>서버가 <code>Set-Cookie</code> 로 내려주면 브라우저가 저장  </li>
<li>요청 시 자동 전송  </li>
<li><code>httpOnly</code>, <code>secure</code>, <code>sameSite</code> 옵션으로 보안 강화 가능  </li>
</ul>
<blockquote>
<p>🔐 <strong>httpOnly란?</strong><br />자바스크립트에서 쿠키를 읽지 못하도록 차단하는 옵션<br />→ refresh_token, session_id처럼 유출되면 위험한 값 보호에 필수</p>
</blockquote>
<blockquote>
<h4 id="왜-refresh_token--session_id-는-반드시-httponly-쿠키에-저장할까">왜 refresh_token / session_id 는 반드시 httpOnly 쿠키에 저장할까?</h4>
<p>이 두 값은 <strong>탈취되면 계정이 그대로 도난되는 ‘가장 위험한 토큰’</strong>이기 때문입니다.</p>
<table>
<thead>
<tr>
<th>항목</th>
<th>털렸을 때 위험도</th>
</tr>
</thead>
<tbody><tr>
<td>access_token</td>
<td>짧게 살아서 피해 제한적</td>
</tr>
<tr>
<td><strong>refresh_token</strong></td>
<td>새 access_token 무한 재발급 → 계정 장악</td>
</tr>
<tr>
<td><strong>session_id</strong></td>
<td>서버 세션 그대로 탈취 → 완전 도난</td>
</tr>
</tbody></table>
<p>즉, <strong>절대 JavaScript에서 읽히면 안 되는 토큰들</strong>입니다.</p>
<ul>
<li><p><strong>localStorage ❌</strong><br />→ JS로 읽힘 → XSS 공격에 그대로 노출</p>
</li>
<li><p><strong>httpOnly 쿠키 ⭕</strong><br />→ JS 접근 완전 차단<br />→ 브라우저가 자동 전송하므로 인증 흐름도 자연스러움
일반 쿠키는 JS에서 읽히기 때문에 XSS 공격에 취약합니다.</p>
</li>
</ul>
</blockquote>
<blockquote>
<h4 id="xsscross-site-scripting">XSS(Cross-Site Scripting)?</h4>
<p>사용자가 방문한 정상 사이트 안에서
공격자가 만든 악성 JS 코드가 실행되도록 속이는 공격</p>
</blockquote>
<pre><code>Set-Cookie: refresh_token=abcd; HttpOnly;</code></pre><p><strong>주로 어디에 쓰는가?</strong></p>
<ul>
<li>*<em>refresh_token 저장  *</em></li>
<li>*<em>session_id 저장 *</em> </li>
</ul>
<hr />
<h3 id="✔-localstorage--sessionstorage">✔ localStorage / sessionStorage</h3>
<ul>
<li>JS에서 직접 접근 가능한 저장소  </li>
<li>자동 전송 X → Bearer 헤더에 직접 넣어야 함  </li>
<li>원래는 일반 데이터 저장용  </li>
<li>XSS 취약  </li>
</ul>
<p><strong>주 사용처</strong>  </p>
<ul>
<li>일반 UI 설정값, Key-Value 데이터 저장 (예: 테마, 언어 설정, 필터 값 등)  </li>
<li>인증 정보 중 <strong>보안 중요도가 낮은 값</strong> 저장 시 (예: access_token — 단, 안전성은 떨어짐)  </li>
<li>간단한 SPA, 데모/프로토타입에서 임시 데이터 저장  </li>
</ul>
<hr />
<h3 id="🧠-메모리in-memory">🧠 메모리(In-Memory)</h3>
<ul>
<li>새로고침 시 사라지는 저장 방식  </li>
<li>XSS 위험을 줄이기 위해 access_token을 메모리에 저장하는 패턴 증가  </li>
</ul>
<blockquote>
<h4 id="인메모리란">인메모리란?</h4>
<p>React state, Context, Redux store, Zustand, 전역 JS 변수 등
런타임 메모리에만 들고 있는 상태를 의미</p>
</blockquote>
<p><strong>주 사용처</strong>  </p>
<ul>
<li>access_token 보관 (가장 권장되는 방식)    </li>
</ul>
<hr />
<h3 id="🤔-새로-고침하면-사라지는데-왜-사용할까">🤔 새로 고침하면 사라지는데 왜 사용할까?</h3>
<p><strong>일부러 사라지도록</strong> 설계한 것입니다.</p>
<h4 id="이유-xss-공격에서-안전">이유: XSS 공격에서 안전</h4>
<p>localStorage에 저장하면 스크립트로 쉽게 탈취됨:</p>
<pre><code class="language-js">localStorage.getItem(&quot;access_token&quot;)</code></pre>
<p>그러나 메모리는 페이지 Reload 시 사라져 지속적인 공격이 불가능.</p>
<hr />
<h3 id="그렇다면-새로고침-후에는-어떻게-로그인-상태를-유지할까">그렇다면 새로고침 후에는 어떻게 로그인 상태를 유지할까?</h3>
<p>인메모리에 있던 access_token은 새로고침 시 사라지기 때문에,
아무 로직도 없으면 사실상 “로그아웃&quot; 됩니다.</p>
<p>그래서 보통 앱에서 이런 흐름으로 구현합니다:</p>
<ol>
<li><p>앱이 처음 로드될 때(예: App 또는 Layout 마운트 시점에)
/auth/refresh 같은 토큰 재발급 API를 자동으로 한 번 호출합니다.</p>
</li>
<li><p>이때 브라우저가 알아서** refresh_token(httpOnly 쿠키)을 서버로 전송합니다.**</p>
</li>
<li><p><strong>서버는 refresh_token을 검증하고 새 access_token을 응답으로 내려줍니다.</strong></p>
</li>
<li><p>프론트는 받은 <strong>access_token을 다시 메모리에 저장합니다.</strong></p>
</li>
</ol>
<p>이렇게 하면, 유저 입장에서는 새로고침을 해도 로그인이 유지된 것처럼 보입니다.</p>
<hr />
<h4 id="✔-실제-권장-패턴">✔ 실제 권장 패턴</h4>
<ul>
<li>refresh_token → httpOnly 쿠키  </li>
<li>access_token → 메모리 보관  </li>
<li>access_token 만료 시 → refresh_token으로 재발급  </li>
</ul>
<hr />
<h2 id="5-access_token--refresh_token">5. access_token / refresh_token</h2>
<h3 id="🔑-access_token">🔑 access_token</h3>
<ul>
<li>짧게 사는 인증 토큰 (5분~1시간)  </li>
<li>보통 JWT  </li>
<li>Bearer로 API 인증  </li>
</ul>
<h3 id="🔑-refresh_token">🔑 refresh_token</h3>
<ul>
<li>access_token 재발급용  </li>
<li>오래 살기 때문에 보안 중요  </li>
<li>보통 <strong>랜덤 문자열(Opaque Token)</strong> + httpOnly 쿠키  </li>
</ul>
<p><strong>비유</strong>  </p>
<ul>
<li>access_token = 🚪 “문 앞에서 보여주는 출입증”  </li>
<li>refresh_token = 🎫 “출입증 재발급권”  </li>
</ul>
<hr />
<h2 id="6-session-방식-sessionstorage와-완전히-다름">6. Session 방식 (sessionStorage와 완전히 다름)</h2>
<p>세션(Session) 방식은 <strong>서버가 로그인 상태를 직접 기억</strong>하는 방식입니다.</p>
<h3 id="✔-작동-흐름">✔ 작동 흐름</h3>
<ol>
<li><p>로그인 성공 → 서버가 세션 생성  </p>
<pre><code>session_id → { userId: 1, role: 'admin' }</code></pre></li>
<li><p>session_id를 쿠키로 내려줌  </p>
<pre><code>Set-Cookie: session_id=xyz123; HttpOnly;</code></pre></li>
<li><p>브라우저가 요청마다 자동 전송  </p>
<pre><code>Cookie: session_id=xyz123</code></pre></li>
<li><p>서버는 이 session_id로 유저 정보 조회  </p>
</li>
</ol>
<blockquote>
<p>서버가 유저 상태를 저장하고,<br />브라우저는 <strong>session_id라는 열쇠</strong>만 들고 다니는 구조</p>
</blockquote>
<h3 id="✔-장점">✔ 장점</h3>
<ul>
<li>서버에서 강제 로그아웃 가능  </li>
<li>민감 정보가 서버에 있어 안전  </li>
</ul>
<h3 id="✔-단점">✔ 단점</h3>
<ul>
<li>서버가 상태를 저장해야 함 → 스케일링 비용  </li>
</ul>
<blockquote>
<h4 id="스케일링-비용이란">스케일링 비용이란?</h4>
<p>사용자 증가에 맞춰 서버를 확장할 때 필요한 추가 부담</p>
</blockquote>
<hr />
<h3 id="🚫-sessionstorage는-완전히-다른-개념입니다">🚫 sessionStorage는 완전히 다른 개념입니다.</h3>
<table>
<thead>
<tr>
<th>개념</th>
<th>저장 위치</th>
<th>목적</th>
<th>인증 여부</th>
</tr>
</thead>
<tbody><tr>
<td><strong>Session(서버 세션)</strong></td>
<td>서버</td>
<td>로그인 상태 유지</td>
<td>✔</td>
</tr>
<tr>
<td><strong>sessionStorage</strong></td>
<td>브라우저</td>
<td>일반 데이터 임시 저장</td>
<td>❌</td>
</tr>
</tbody></table>
<hr />
<h3 id="세션-방식은-어떻게-구현할까">세션 방식은 어떻게 구현할까?</h3>
<h4 id="✔-서버에서-하는-일">✔ 서버에서 하는 일</h4>
<ul>
<li>로그인 시 세션 저장  </li>
<li>session_id 쿠키 발급  </li>
<li>요청마다 session_id로 유저 조회  </li>
<li>로그아웃 시 세션 삭제  </li>
</ul>
<h4 id="✔-프론트에서-하는-일">✔ 프론트에서 하는 일</h4>
<pre><code class="language-js">fetch('/api/login', {
  method: 'POST',
  credentials: 'include'
});</code></pre>
<ul>
<li>쿠키 자동 전송 → 토큰 관리 불필요  </li>
<li>로그아웃 API만 호출하면 끝  </li>
</ul>
<hr />
<h2 id="7-opaque-token불투명-토큰">7. Opaque Token(불투명 토큰)</h2>
<p>Opaque Token은 <strong>의미를 알 수 없는 랜덤 문자열 토큰</strong>입니다.</p>
<p>예:</p>
<pre><code>4f8d1b28e92c4a6ca8948d91a3f8a0d7</code></pre><h3 id="✔-특징">✔ 특징</h3>
<ul>
<li>토큰 내부 정보를 알 수 없음  </li>
<li>반드시 서버 DB에 저장해 매칭해야 함  </li>
<li>refresh_token에서 가장 많이 사용됨  </li>
<li>OAuth2 기본 access_token 형태  </li>
</ul>
<h3 id="✔-왜-쓰는가">✔ 왜 쓰는가?</h3>
<ul>
<li>JWT처럼 내부 정보가 노출되지 않아 안전  </li>
<li>refresh_token처럼 “매우 민감한 토큰”에 적합  </li>
</ul>
<h3 id="✔-누가-발급하나">✔ 누가 발급하나?</h3>
<p><strong>백엔드 인증 서버</strong>가 직접 생성해 클라이언트에게 전달합니다.</p>
<ol>
<li>서버가 Opaque Token을 만든다</li>
<li>서버는 이 토큰을 DB/Redis 등 저장소에 저장한다</li>
<li>클라이언트는 이 문자열을 들고 다닌다</li>
<li>요청 올 때 서버는 DB에서 토큰을 찾아야 유저 확인 가능</li>
</ol>
<p>예)</p>
<pre><code>98de12ccf39a49dbb041a01bdac20345</code></pre><p>서버 DB에는 이렇게 저장됨:</p>
<pre><code>refresh_token -&gt; userId 123</code></pre><h3 id="✔-jwt는-왜-db가-필요-없을까">✔ JWT는 왜 DB가 필요 없을까?</h3>
<table>
<thead>
<tr>
<th>토큰 종류</th>
<th>서버에서 DB 필요?</th>
<th>이유</th>
</tr>
</thead>
<tbody><tr>
<td><strong>JWT</strong></td>
<td>❌ 필요 없음</td>
<td>토큰 안에 userId/exp/role 등이 다 들어있고 서명으로 검증 가능</td>
</tr>
<tr>
<td><strong>Opaque Token</strong></td>
<td>✔ 필요함</td>
<td>내부 정보 없음 → 서버가 저장한 정보와 매칭해야 함</td>
</tr>
</tbody></table>
<p>→ 그래서 refresh_token을 쓰면</p>
<p>노출됐을 때 내부 정보가 없으므로 안전</p>
<p>서버 DB에서 해당 토큰만 지우면 즉시 무효화 가능 (로그아웃 가능)</p>
<p>JWT refresh_token보다 훨씬 컨트롤이 쉬움</p>
<hr />
<h2 id="8-jwt-말고도-존재하는-중요한-토큰들">8. JWT 말고도 존재하는 중요한 토큰들</h2>
<h3 id="✔-세션-토큰session-id">✔ 세션 토큰(Session ID)</h3>
<ul>
<li>세션 방식에서 사용  </li>
<li>쿠키에 저장  </li>
<li>내부 정보는 서버에 있음  </li>
</ul>
<h3 id="✔-opaque-token">✔ Opaque Token</h3>
<ul>
<li>랜덤 문자열  </li>
<li>OAuth2 기본 토큰  </li>
<li>refresh_token에 주로 사용  </li>
</ul>
<h3 id="✔-oauth-토큰들">✔ OAuth 토큰들</h3>
<ul>
<li>access_token (opaque 또는 JWT)  </li>
<li>refresh_token (opaque)  </li>
<li>id_token (항상 JWT)  </li>
</ul>
<h3 id="✔-api-key">✔ API Key</h3>
<ul>
<li>외부 서비스 인증  </li>
</ul>
<h3 id="✔-id_token">✔ id_token</h3>
<ul>
<li>OAuth 로그인에서 사용자 프로필을 담는 JWT  </li>
</ul>
<hr />
<h2 id="✅-어떤-것을-어디에서-주로-쓸까">✅ 어떤 것을 어디에서 주로 쓸까?</h2>
<table>
<thead>
<tr>
<th>개념</th>
<th>역할</th>
<th>주로 쓰는 곳</th>
</tr>
</thead>
<tbody><tr>
<td><strong>JWT</strong></td>
<td>토큰 포맷(Stateless 인증에 적합)</td>
<td>API 인증, OAuth id_token</td>
</tr>
<tr>
<td><strong>access_token</strong></td>
<td>짧게 사는 인증 토큰</td>
<td>Bearer 헤더, 인메모리 저장</td>
</tr>
<tr>
<td><strong>refresh_token</strong></td>
<td>access_token 재발급</td>
<td>httpOnly 쿠키(서버 DB 검증)</td>
</tr>
<tr>
<td><strong>Bearer</strong></td>
<td>인증 전달 방식(헤더 스킴)</td>
<td>모든 API 인증 요청</td>
</tr>
<tr>
<td><strong>쿠키(httpOnly)</strong></td>
<td>민감 토큰 보관/자동 전송</td>
<td>refresh_token, session_id</td>
</tr>
<tr>
<td><strong>localStorage / sessionStorage</strong></td>
<td>JS 접근 가능 Key-Value 저장소</td>
<td>일반 UI 값, 낮은 보안 데이터</td>
</tr>
<tr>
<td><strong>메모리(In-Memory)</strong></td>
<td>JS 런타임 상태 저장</td>
<td>access_token 임시 보관</td>
</tr>
<tr>
<td><strong>세션(SessionID)</strong></td>
<td>서버가 상태 저장하는 인증 방식</td>
<td>SSR/전통 웹, 사내 시스템</td>
</tr>
<tr>
<td><strong>Opaque Token</strong></td>
<td>서버가 DB에 저장하는 랜덤 토큰</td>
<td>refresh_token, OAuth2 access_token</td>
</tr>
<tr>
<td><strong>API Key</strong></td>
<td>서비스/서버 간 인증</td>
<td>외부 API, 백엔드 통신</td>
</tr>
<tr>
<td><strong>id_token</strong></td>
<td>사용자 정보(JWT)</td>
<td>소셜 로그인(OAuth/OpenID Connect)</td>
</tr>
</tbody></table>
<hr />
<h2 id="📝-전체-인증-흐름-요약">📝 전체 인증 흐름 요약</h2>
<ol>
<li>사용자가 로그인 요청을 보냄  </li>
<li>서버는 다음 두 값을 생성함  <ul>
<li><strong>access_token (JWT, 짧은 수명)</strong>  </li>
<li><strong>refresh_token (Opaque Token, 장기 수명)</strong>  </li>
</ul>
</li>
<li>서버는 refresh_token을 <strong>httpOnly 쿠키</strong>로 내려 저장하게 함  </li>
<li>프론트는 access_token을 <strong>메모리(In-Memory)</strong> 등에 보관하여<br />API 요청 시 <strong>Bearer 헤더</strong>로 전송  </li>
<li>access_token이 만료되거나 새로고침으로 사라지면<br />프론트는 <code>/auth/refresh</code> 요청을 보내고<br />브라우저는 refresh_token 쿠키를 자동 전송  </li>
<li>서버는 refresh_token을 검증해 <strong>새로운 access_token을 재발급</strong>  </li>
<li>세션 기반 방식이라면, 서버는 session_id를 쿠키로 발급하고<br />이후 요청마다 자동으로 전송되는 session_id로 로그인 상태를 유지  </li>
</ol>
<p>→ 결과적으로 사용자는 새로고침을 하거나 access_token이 만료되더라도<br />   <strong>refresh_token(쿠키) 또는 session_id 덕분에 로그인 상태가 유지됨</strong></p>
<hr />