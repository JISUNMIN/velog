<p>개발을 하다 보면 ‘서버’라는 단어가 참 모호하게 느껴질 때가 있습니다.  </p>
<p>백엔드 서버도 서버라고 하고, <code>npm start</code>로 띄운 로컬 개발 서버(프론트엔드 개발용 서버)도 서버라고 합니다.<br />같은 ‘서버’인데 하는 일은 완전히 다릅니다.  </p>
<p>저도 이 부분이 헷갈릴 때가 있어서, 이번 기회에 <strong>프론트엔드 개발 서버와 백엔드 서버의 구조적 차이</strong>,  
그리고 <strong>로컬과 배포 환경에서 이 서버들이 어떻게 대체되는지</strong>를 정리해보았습니다.</p>
<hr />
<h2 id="1️⃣-프론트엔드-개발-서버-development-server">1️⃣ 프론트엔드 개발 서버 (Development Server)</h2>
<blockquote>
<p> 코드 변경을 실시간 반영하고, 정적 리소스를 서빙하는 개발용 런타임 환경입니다.</p>
</blockquote>
<p>프론트엔드 개발에서 <code>npm start</code> 또는 <code>npm run dev</code> 명령어를 실행하면,<br />실제로는 브라우저가 서버를 띄우는 것이 아니라 <strong>프레임워크가 자체적으로 개발용 서버(Dev Server)</strong> 를 구동합니다.<br />이 서버는 정적 리소스와 빌드 결과물을 메모리에서 즉시 제공하며,<br />코드 변경 시 빠르게 반영되도록 최적화되어 있습니다.</p>
<h3 id="예시">예시</h3>
<pre><code class="language-bash">npm run dev
# 또는
npm start</code></pre>
<p>→ 브라우저가 자동으로 <code>http://localhost:3000</code>을 오픈합니다.</p>
<h3 id="🔍-localhost3000은-어디서-오는가">🔍 <code>localhost:3000</code>은 어디서 오는가?</h3>
<table>
<thead>
<tr>
<th>프레임워크</th>
<th>기본 포트</th>
<th>서버 종류</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td><strong>Create React App (CRA)</strong></td>
<td>3000</td>
<td>Webpack Dev Server</td>
<td>Webpack이 내장한 개발 서버로, HMR과 메모리 번들링 지원</td>
</tr>
<tr>
<td><strong>Vite</strong></td>
<td>5173 (또는 설정값)</td>
<td>Vite Dev Server</td>
<td>ESM 기반의 초고속 개발 서버, 즉시 빌드와 빠른 갱신 제공</td>
</tr>
<tr>
<td><strong>Next.js</strong></td>
<td>3000</td>
<td>Next Dev Server</td>
<td>SSR(서버사이드 렌더링) 및 API Routes까지 포함한 통합 개발 서버</td>
</tr>
</tbody></table>
<p>즉, <code>localhost:3000</code>은 브라우저가 띄우는 주소가 아니라<br /><strong>React, Vite, Next.js가 내부적으로 실행하는 개발 서버의 포트</strong>입니다.<br />이 서버는 코드 변경 시마다 메모리 상에서 새로 빌드된 HTML/CSS/JS를 즉시 서빙합니다.</p>
<blockquote>
<p>🔥 <strong>HMR (Hot Module Replacement)</strong><br />코드가 수정될 때 <strong>전체 페이지를 새로고침하지 않고</strong>,  
수정된 모듈(파일)만 교체해서 즉시 반영하는 기술</p>
</blockquote>
<hr />
<h3 id="프레임워크별-dev-server-구조-차이">프레임워크별 Dev Server 구조 차이</h3>
<p><code>npm start</code>나 <code>npm run dev</code> 명령어로 실행되는 개발 서버는<br />프레임워크마다 구조와 동작 방식이 다릅니다.</p>
<table>
<thead>
<tr>
<th>구분</th>
<th>Dev Server 제공 방식</th>
<th>내부 기술 스택</th>
<th>특징</th>
</tr>
</thead>
<tbody><tr>
<td><strong>Vite</strong></td>
<td>자체 Dev Server 내장</td>
<td>ESM + Rollup</td>
<td>브라우저가 모듈을 직접 가져가 실행하는 구조. 빠른 HMR과 즉시 반영이 가능.</td>
</tr>
<tr>
<td><strong>CRA (Webpack)</strong></td>
<td>Webpack Dev Server 사용</td>
<td>Webpack + Babel</td>
<td>모든 파일을 번들링해 메모리에 저장 후 제공. 안정적이지만 빌드 속도는 다소 느림.</td>
</tr>
<tr>
<td><strong>Next.js</strong></td>
<td>통합 Dev Server 제공</td>
<td>SWC + Node 서버</td>
<td>SSR(서버사이드 렌더링)과 API 라우트를 함께 처리. 프론트와 백엔드를 동시에 구동.</td>
</tr>
</tbody></table>
<p>📌 정리하자면,  </p>
<ul>
<li><strong>Vite</strong> → “가벼운 프론트엔드 전용 개발 서버”  </li>
<li><strong>CRA(Webpack)</strong> → “번들링 중심의 전통적인 개발 서버”  </li>
<li><strong>Next.js</strong> → “서버 렌더링 + API 통합형 개발 서버”</li>
</ul>
<hr />
<h3 id="❓-정적-리소스를-서빙한다는-의미">❓ 정적 리소스를 “서빙”한다는 의미</h3>
<p>“서빙(serving)”이란 브라우저의 요청에 대해 <strong>HTML, JS, CSS 등의 파일을 응답으로 전달</strong>하는 것을 의미합니다.<br />개발 서버는 디스크에 저장된 빌드 결과를 읽지 않고,<br /><strong>메모리에서 즉시 생성한 번들을 브라우저에 제공합니다.</strong></p>
<p>즉, 브라우저가 <code>http://localhost:3000</code>에 접근하면<br />Dev Server는 메모리 안의 최신 번들을 실시간으로 응답합니다.</p>
<hr />
<h3 id="❓-빌드-결과물을-어떻게-즉시-제공할까">❓ 빌드 결과물을 어떻게 “즉시 제공”할까?</h3>
<p>Vite, CRA(Webpack Dev Server), Next.js Dev Server는<br />코드 변경을 감지(watch)하고 변경된 부분만 <strong>메모리 내에서 부분적으로 다시 빌드</strong>합니다.<br />이 빌드 결과물은 파일로 저장되지 않고, <strong>in-memory filesystem</strong>에 유지됩니다.  </p>
<p>브라우저 요청이 들어오면 서버는<br />“메모리에 있는 최신 상태의 번들”을 즉시 꺼내서 응답합니다.<br />이 방식 덕분에 <code>npm start</code>만 실행해도 별도의 빌드나 배포 없이<br />즉시 앱이 동작합니다.</p>
<hr />
<h3 id="❓-실제-배포-없이도-동작하는-이유">❓ 실제 배포 없이도 동작하는 이유</h3>
<p>프론트엔드 개발 서버는 <strong>Nginx나 Vercel 같은 정적 파일 서버를 흉내내는 임시 서버</strong>입니다.<br />즉, 실제로는 빌드(<code>npm run build</code>)를 하지 않아도<br />개발 서버가 실시간 번들링과 리소스 제공 역할을 대신 수행합니다.</p>
<p>정리하면  </p>
<ul>
<li>코드 변경 → Dev Server가 자동 감지  </li>
<li>필요한 부분만 메모리에서 재번들  </li>
<li>최신 상태를 브라우저에 즉시 응답  </li>
<li>전체 리빌드나 배포 과정 없이도 “실시간 미리보기” 가능  </li>
</ul>
<hr />
<h3 id="🔁-개발-환경과-배포-환경의-차이">🔁 개발 환경과 배포 환경의 차이</h3>
<p>로컬 환경에서는 프론트엔드 개발 서버(예: Vite, CRA)가 직접 정적 파일을 제공합니다.<br />하지만 <strong>배포 환경에서는 이러한 로컬 서버가 존재하지 않습니다.</strong><br />빌드된 정적 파일(<code>dist</code>, <code>build</code> 폴더)을 실제 서버가 대신 제공합니다.</p>
<ul>
<li><strong>로컬 개발 환경</strong> → React/Vite/Next.js의 개발 서버(Dev Server)  </li>
<li><strong>배포 환경</strong> → Nginx, Vercel, Netlify 등에서 <strong>빌드 결과물(정적 파일)</strong> 을 서빙 </li>
<li><strong>API 서버</strong> → Express, NestJS, FastAPI 등의 백엔드 서버가 데이터 처리를 담당  </li>
</ul>
<hr />
<h3 id="🌐-환경별-서버-구조-비교">🌐 환경별 서버 구조 비교</h3>
<table>
<thead>
<tr>
<th>환경</th>
<th>프론트엔드 구성</th>
<th>백엔드 구성</th>
<th>주요 역할</th>
<th>인프라 예시</th>
</tr>
</thead>
<tbody><tr>
<td><strong>로컬(local)</strong></td>
<td>React/Vite/Next.js <strong>Dev Server</strong></td>
<td>Express/NestJS <strong>로컬 API 서버</strong></td>
<td>코드 수정 시 실시간 반영(HMR) + 로컬 데이터 테스트</td>
<td><code>localhost:3000</code>, <code>localhost:4000</code></td>
</tr>
<tr>
<td><strong>개발(dev)</strong></td>
<td>빌드된 정적 파일을 <strong>임시 정적 서버(Nginx, Cloud Run 등)</strong> 에 배포</td>
<td><strong>개발용 백엔드 서버</strong> (개발 DB 연동)</td>
<td>QA/테스트 환경 운영, 팀 단위 통합 테스트</td>
<td>AWS EC2, Cloud Run Dev, K8s Dev</td>
</tr>
<tr>
<td><strong>프로덕션(prod)</strong></td>
<td><strong>정적 파일 서버</strong> (Nginx/Vercel/S3/CloudFront) 에서 배포</td>
<td><strong>운영 백엔드 서버</strong> (실서비스 API)</td>
<td>실제 사용자 대상 서비스 제공</td>
<td>AWS EC2, ECS, CloudFront, K8s Prod</td>
</tr>
</tbody></table>
<hr />
<h2 id="2️⃣-백엔드-api-서버">2️⃣ 백엔드 API 서버</h2>
<blockquote>
<p>데이터 흐름의 실제 진입점이며, 비즈니스 로직과 데이터베이스를 관리합니다.</p>
</blockquote>
<p>클라이언트(브라우저)는 다음과 같은 방식으로 데이터를 요청합니다:</p>
<pre><code class="language-js">fetch('http://localhost:4000/api/users')
  .then(res =&gt; res.json())
  .then(console.log);</code></pre>
<p>이 요청은 Node.js(Express, NestJS), Python(Django, FastAPI), Go, Java(Spring) 등의<br />서버 애플리케이션이 처리합니다.</p>
<h3 id="특징">특징</h3>
<ul>
<li>RESTful 혹은 GraphQL 등의 API 인터페이스를 제공합니다.  </li>
<li>인증, 세션, 캐싱, 데이터베이스 I/O 등의 <strong>비즈니스 로직을 실행</strong>합니다.  </li>
<li>프론트엔드와는 별도의 포트에서 독립적으로 동작하며, 로컬 환경에서는 주로 <code>4000</code>, <code>5000</code> 등의 포트를 사용합니다.</li>
</ul>
<p>예를 들어 Express 기반의 서버는 다음과 같습니다.</p>
<pre><code class="language-js">app.get('/api/users', (req, res) =&gt; {
  res.json([{ id: 1, name: '선망쓰' }]);
});</code></pre>
<hr />
<h2 id="3️⃣-로컬-개발-환경의-구조적-흐름">3️⃣ 로컬 개발 환경의 구조적 흐름</h2>
<p>로컬 환경에서의 일반적인 요청 흐름은 다음과 같습니다.</p>
<pre><code>브라우저 (React App)
   │
   ├── GET /index.html  → 프론트엔드 개발 서버 (3000)
   └── GET /api/users   → 백엔드 API 서버 (4000)</code></pre><table>
<thead>
<tr>
<th>구분</th>
<th>포트</th>
<th>역할</th>
<th>기술 예시</th>
</tr>
</thead>
<tbody><tr>
<td>프론트엔드 개발 서버</td>
<td>3000</td>
<td>정적 리소스 서빙, HMR 지원</td>
<td>Vite, CRA, Next.js</td>
</tr>
<tr>
<td>백엔드 API 서버</td>
<td>4000</td>
<td>비즈니스 로직, DB 처리</td>
<td>Express, NestJS, FastAPI</td>
</tr>
</tbody></table>
<hr />
<h2 id="4️⃣-cors와-proxy-설정">4️⃣ CORS와 Proxy 설정</h2>
<p>브라우저는 보안을 위해 “같은 출처(Same-Origin)” 정책을 따릅니다.  </p>
<p>로컬 개발 환경에서는</p>
<ul>
<li>프론트엔드 개발 서버(<code>localhost:3000</code>)  </li>
<li>백엔드 API 서버(<code>localhost:4000</code>)  </li>
</ul>
<p>이 <strong>서로 다른 포트에서 동작</strong>합니다.<br />브라우저는 이 둘을 <strong>다른 출처(Origin)</strong> 로 간주하기 때문에<br />이 경우 API 요청 시 <strong>CORS(Cross-Origin Resource Sharing)</strong> 에러가 발생할 수 있습니다.</p>
<p>이를 해결하기 위해 Vite, CRA, Webpack Dev Server 등은 <strong>Proxy 설정</strong>을 제공합니다.</p>
<pre><code class="language-js">// vite.config.js
export default {
  server: {
    proxy: {
      '/api': 'http://localhost:4000',
    },
  },
}</code></pre>
<p>즉, 브라우저는 여전히 <code>localhost:3000</code>에 요청을 보내지만,
Vite Dev Server가 이를 대신 <strong>백엔드로 전달(proxy pass)</strong> 합니다.</p>
<pre><code class="language-text">브라우저 (localhost:3000)
   │
   ├── 요청 → Dev Server(proxy)
   │         └── 요청 전달 → localhost:4000 (API 서버)
   │
   └── 응답 ← Dev Server ← 백엔드 서버</code></pre>
<p>이제 <code>fetch('/api/users')</code> 요청은 Dev Server가 대신 <code>localhost:4000/api/users</code>로 전달하므로,<br />브라우저는 같은 Origin으로 인식하고 CORS 문제가 사라집니다.</p>
<blockquote>
<p>🚫 <strong>CORS</strong>: <strong>CORS(Cross-Origin Resource Sharing)</strong> 는<br />브라우저가 다른 출처의 리소스 요청을 제한하는 보안 정책입니다.<br />예를 들어,<br />React 앱(<code>http://localhost:3000</code>)이 API 서버(<code>http://localhost:4000</code>)에 요청을 보내면,<br />브라우저는 기본적으로 이를 차단합니다.</p>
<pre><code class="language-text">Access to fetch at 'http://localhost:4000/api/users
'from origin 'http://localhost:3000' has been blocked by CORS policy.</code></pre>
</blockquote>
<pre><code>이는 해커가 악의적으로 다른 사이트의 데이터를 훔쳐보는 것을 방지하기 위한  
**브라우저 차원의 보안 장치**입니다.


&gt; 🔁 Proxy(프록시):**프록시(proxy)** 는 “대신 요청을 전달해주는 중간 서버”입니다.  
프론트엔드 개발 서버가 브라우저와 백엔드 서버 사이에서  
**요청을 대신 중계하는 역할**을 합니다.
&gt;즉,
1. 브라우저는 `localhost:3000/api/users`로 요청을 보냅니다.  
2. Dev Server(Vite, CRA 등)가 그 요청을 받아 내부적으로  
   `localhost:4000/api/users`로 전달합니다.  
3. 브라우저는 “같은 Origin으로 요청했다”고 생각하기 때문에 CORS를 우회할 수 있습니다.

---

### 🤔 Proxy 설정은 언제 필요할까?
Proxy 설정은 항상 필요한 것이 아니라,
**프론트엔드와 백엔드의 Origin(출처)이 다를 때만 필요**합니다.

| 환경            | 프론트엔드          | 백엔드               | Origin 관계 | CORS     | Proxy 필요 여부        |
| ------------- | -------------- | ----------------- | --------- | -------- | ------------------ |
| **로컬(local)** | localhost:3000 | localhost:4000    | 다름        | ✅ 발생     | ✅ 필요               |
| **개발(dev)**   | dev.myapp.com  | api.dev.myapp.com | 다름        | ⚙️ 발생 가능 | ⚙️ 필요 (또는 CORS 허용) |
| **배포(prod)**  | myapp.com      | myapp.com/api     | 같음        | ❌ 없음     | ❌ 불필요              |


---

## 5️⃣ 프로덕션 환경의 구성

빌드 후(`npm run build`)에는 개발 서버가 사라지고,  
정적 파일(`index.html`, `main.js`, `style.css`)이 **빌드 산출물(dist 폴더)**로 생성됩니다.
</code></pre><p>📦 dist/
 ┣ index.html
 ┣ assets/
 ┃ ┣ main.js
 ┃ ┗ style.css</p>
<pre><code>
이 파일들은 Nginx, Vercel, Netlify, AWS S3 등에서  
**정적 자원으로 서빙**됩니다.
</code></pre><p>브라우저
  │
  ├── HTML/JS/CSS 요청 → Nginx (Static Server)
  └── API 요청 → Express / NestJS (Backend Server)</p>
<pre><code>
이 시점에서 Dev Server는 완전히 사라지고,  
**정적 파일 서버**가 그 역할을 대신합니다.



---

## 6️⃣ 요약

| 구분                | 목적     | 역할              | 응답 형태         | 대표 기술                   |
| ----------------- | ------ | --------------- | ------------- | ----------------------- |
| **Dev Server**    | 개발 환경용 | 실시간 빌드/HMR      | HTML, JS, CSS | Vite, CRA, Next.js      |
| **API Server**    | 데이터 처리 | 비즈니스 로직, DB I/O | JSON          | Express, NestJS, Django |
| **Static Server** | 배포 환경  | 정적 리소스 서빙       | HTML, JS, CSS | Nginx, Vercel, S3       |

---

## 💬 결론

프론트엔드 개발 서버(Dev Server)는 **개발 효율을 위한 임시 런타임 환경**으로,  
코드 변경을 실시간으로 반영하지만 **빌드 결과물을 직접 제공하지 않습니다.**

빌드 후에는 Dev Server가 사라지고,  
**정적 파일 서버(Static Server)** 가 그 역할을 대신해  
HTML, JS, CSS 등의 자산을 사용자에게 제공합니다.  

한편, **API 서버(API Server)** 는  
데이터베이스와 비즈니스 로직을 처리하며  
개발/배포 환경 모두에서 지속적으로 동작합니다.

---

&gt; “서버”라는 단어는 같지만, 역할과 수명은 다릅니다.  
&gt; - **Dev Server** → 개발 생산성을 위한 도구  
&gt; - **Static Server** → 사용자에게 화면을 제공하는 프론트엔드 서버  
&gt; - **API Server** → 서비스 로직과 데이터를 책임지는 핵심 서버  

&gt; **개발 환경에서는 Dev Server와 API Server가 분리되어 공존하지만,**  
&gt; **배포된 환경에서는 Static Server와 API Server만 남아 실제 서비스를 구성합니다.**
</code></pre>