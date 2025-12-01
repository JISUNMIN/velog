<p><strong>빌드 타임(Build Time)</strong>과 <strong>런타임(Runtime)</strong>은
프로그램이 실행되기 전에 준비되는 단계와
실제로 실행되는 단계를 구분해서 부르는 말입니다.</p>
<blockquote>
<p>코드가 실행되기 전의 문제 = 빌드 타임 문제
코드가 실제로 실행된 후의 문제 = 런타임 문제</p>
</blockquote>
<p>여기에 더해 <strong>컴파일 타임(Compile Time)</strong>이라는 용어도 있지만,<br />FE/Node 환경에서는 컴파일(트랜스파일) 과정이 빌드 과정 전체에 포함되므로<br />실무에서는 <strong>‘컴파일 타임’이라는 용어를 빌드 타임과 구분하지 않고</strong><br />주로 “빌드 타임 오류”, “빌드 에러”처럼 표현하는 경우가 많습니다</p>
<hr />
<h2 id="💡-실행-순서">💡 실행 순서</h2>
<p>프로그램이 실행되기 위해서는<br /><strong>코드를 준비(컴파일) → 실행 가능한 형태로 만들고(빌드) → 실제로 실행(런타임)</strong> 하는 과정이 필요합니다.</p>
<p>즉, 정확한 순서는 다음과 같습니다.</p>
<h3 id="1-컴파일compile"><strong>1. 컴파일(Compile)</strong></h3>
<p>코드를 기계가 이해할 수 있도록 <strong>변환하는 단계</strong></p>
<ul>
<li>✔ 코드 문법 검사  </li>
<li>✔ 타입 검사  </li>
<li>✔ TS → JS 변환  </li>
<li>✔ JSX → JS 변환  </li>
<li>✔ 최신 JS → 구버전 JS 변환(Babel)</li>
</ul>
<p>즉,</p>
<blockquote>
<p><strong>우리가 쓴 코드 → 실행 가능한 코드로 변환하는 과정</strong></p>
</blockquote>
<p>하지만 이 단계는 <strong>“코드만 변환”</strong>합니다.<br />CSS, 이미지, 폰트, 환경변수, 최적화는 전혀 포함되지 않습니다.</p>
<hr />
<h3 id="2-빌드build"><strong>2. 빌드(Build)</strong></h3>
<p>프로그램을 <strong>실행 가능한 완제품으로 조립·포장하는 단계</strong></p>
<p>컴파일된 코드만 있다고 바로 실행 가능한 것이 아니기 때문에,<br />빌드에서는 아래와 같은 작업들이 추가로 이루어집니다.</p>
<ul>
<li>JS 파일 번들링  </li>
<li>Tree-shaking / minify / 난독화  </li>
<li>CSS·이미지·폰트 등 정적 자원 처리  </li>
<li>환경변수(.env.production 등) 주입  </li>
<li>HTML/manifest 등 정적 파일 생성  </li>
<li>Docker일 경우 이미지 빌드  </li>
<li>최종적으로 <code>dist/</code>, <code>build/</code> 산출물 생성</li>
</ul>
<p>즉,</p>
<blockquote>
<p><strong>컴파일된 코드 + 모든 리소스를 실행 가능한 형태로 완성하는 과정</strong>
(= 번들링, 압축, 이미지 처리 등)</p>
</blockquote>
<hr />
<h3 id="3-런타임runtime"><strong>3. 런타임(Runtime)</strong></h3>
<p>준비된 프로그램이 <strong>실제로 실행되는 시점</strong></p>
<ul>
<li>브라우저에서 웹 앱이 동작  </li>
<li>서버가 API를 처리  </li>
<li>DB 통신  </li>
<li>React 컴포넌트 렌더  </li>
<li>사용자 입력 이벤트 처리  </li>
</ul>
<p>즉,</p>
<blockquote>
<p><strong>빌드가 끝난 뒤 실제로 프로그램이 돌아가는 순간</strong></p>
</blockquote>
<h3 id="순서-요약">순서 요약</h3>
<p><strong><code>컴파일 → 빌드 → 런타임</code></strong> </p>
<h3 id="예시">예시</h3>
<p>TypeScript 파일 .ts → .js
➡ 컴파일</p>
<p>여러 JS + CSS + 이미지 → dist/main.js, dist/index.html
➡ 빌드</p>
<blockquote>
<p>📁 dist/: <strong>배포용 완성본(산출물)</strong>을 모아놓는 폴더</p>
<p>dist/
 ├─ index.html
 ├─ assets/
 │   ├─ main-8273ds.js
 │   ├─ style-92af3d.css
 │   ├─ logo-23df91.svg
 │   └─ chunk-vendors-7ab91.js</p>
</blockquote>
<ul>
<li>index.html → 브라우저가 첫 번째로 로드하는 파일</li>
<li>main.js → 앱의 JS 로직(번들링된 버전)</li>
<li>style.css → 모든 CSS가 압축되어 들어감</li>
<li>이미지/폰트 → 브라우저에서 필요한 리소스</li>
<li>chunk-vendors.js → 라이브러리들 분리해 둔 번들</li>
</ul>
<p>사용자가 브라우저에서 앱을 열고 버튼 클릭
➡ 런타임</p>
<hr />
<h2 id="💡-핵심-용어와-실행-순서">💡 핵심 용어와 실행 순서</h2>
<p>프로그램이 실행되기 위해서는<br /><strong>코드를 준비(컴파일) → 실행 가능한 형태로 만들고(빌드) → 실제로 실행(런타임)</strong> 하는 과정이 필요합니다.</p>
<p>즉, 정확한 순서는 다음과 같습니다.</p>
<hr />
<h3 id="1-컴파일compile-1">1. 컴파일(Compile)</h3>
<p>코드를 기계가 이해할 수 있도록 <strong>변환하는 단계</strong></p>
<ul>
<li>코드 문법 검사  </li>
<li>타입 검사  </li>
<li>TS → JS 변환  </li>
<li>JSX → JS 변환  </li>
<li>최신 JS → 구버전 JS 변환(Babel)</li>
</ul>
<blockquote>
<p><strong>우리가 쓴 코드 → 실행 가능한 코드로 변환하는 과정</strong><br />단, 이 단계는 “코드만 변환”하며 CSS/이미지/환경변수 처리는 포함되지 않음</p>
</blockquote>
<hr />
<h3 id="2-빌드build-1">2. 빌드(Build)</h3>
<p>프로그램을 <strong>실행 가능한 완제품으로 조립·포장하는 단계</strong></p>
<ul>
<li>JS 파일 번들링  </li>
<li>Tree-shaking / minify / 난독화  </li>
<li>CSS·이미지·폰트 등 정적 자원 처리  </li>
<li>환경변수(.env.production 등) 주입  </li>
<li>HTML/manifest 등 정적 파일 생성  </li>
<li>Docker일 경우 이미지 빌드  </li>
<li>최종적으로 <code>dist/</code>, <code>build/</code> 산출물 생성</li>
</ul>
<blockquote>
<p><strong>컴파일된 코드 + 모든 리소스를 실행 가능한 형태로 완성하는 과정</strong></p>
</blockquote>
<hr />
<h3 id="3-런타임runtime-1">3. 런타임(Runtime)</h3>
<p>준비된 프로그램이 <strong>실제로 실행되는 시점</strong></p>
<ul>
<li>브라우저에서 웹 앱이 동작  </li>
<li>서버가 API 요청 처리  </li>
<li>DB와 통신  </li>
<li>React 컴포넌트 렌더링  </li>
<li>사용자 입력 이벤트 처리</li>
</ul>
<blockquote>
<p><strong>빌드가 끝난 뒤 실제로 프로그램이 돌아가는 순간</strong></p>
</blockquote>
<hr />
<h3 id="✅-전체-실행-순서-요약">✅ 전체 실행 순서 요약</h3>
<p><strong><code>컴파일 → 빌드 → 런타임</code></strong><br />항상 이 순서가 맞습니다.</p>
<hr />
<h2 id="🤔-왜-fe-개발자들은-이-순서를-헷갈리기-쉬울까">🤔 왜 FE 개발자들은 이 순서를 헷갈리기 쉬울까?</h2>
<p>프론트엔드/Node 환경에서는 아래 3가지 이유 때문에<br />실제 순서가 잘 체감되지 않습니다.</p>
<hr />
<h3 id="1-과거-js는-빌드-없이-즉시-실행됐다">1) 과거 JS는 “빌드 없이” 즉시 실행됐다</h3>
<p>예전엔 JS 파일만 넣으면 바로 실행됐기 때문에 (개발은 편하지만, 성능은 매우 떨어짐)
“JS는 빌드가 없다 → 런타임이 먼저다”라는 인식이 생김.</p>
<hr />
<h3 id="2-dev-모드npm-run-dev는-전체-빌드를-하지-않는다">2) dev 모드(<code>npm run dev</code>)는 전체 빌드를 하지 않는다</h3>
<p>코드를 고치면 화면이 즉시 바뀌므로<br />마치 빌드/컴파일 없이 런타임이 먼저처럼 느껴짐.</p>
<ul>
<li>*<em>dev 서버는 빌드를 하지 않음  *</em></li>
<li>파일 변경 시 *<em>필요한 부분만 재컴파일(HMR: Hot Module Replacement)  *</em></li>
<li>런타임(개발 서버)은 계속 유지됨</li>
<li>dist 폴더 생성 하지 않음, 압축, 최적화, tree-shaking 모두 하지 않음</li>
<li><strong>코드를 즉시 실행하기 위한 변환(컴파일)만 수행</strong></li>
</ul>
<p>하지만 프로덕션 모드에서는<br />반드시 <strong>전체 빌드 → 배포</strong>가 필요합니다</p>
<hr />
<h3 id="3-fenode-생태계에서는-컴파일러가-눈에-보이지-않는다">3) FE/Node 생태계에서는 컴파일러가 눈에 보이지 않는다</h3>
<p>TypeScript 변환(tsc), Babel 트랜스파일링 같은 컴파일 단계와<br />Vite/Webpack의 번들링·최적화 같은 빌드 단계가<br />모두 <strong>빌드 명령 내부에서 자동으로 연속 실행</strong>됨.</p>
<p>그래서 컴파일 타임 개념이 드러나지 않아
전체 순서를 직관적으로 느끼기 어려움.</p>
<h3 id="요약">요약</h3>
<p>프론트엔드 환경에서는 많은 과정이 자동화되어 있고<br />개발 서버(dev server)가 항상 실행된 상태에서 작업하기 때문에</p>
<p>**실제 순서인 <code>컴파일 → 빌드 → 런타임</code>이 잘 체감되지 않습니다.</p>
<hr />
<h2 id="🔍-dev-모드-vs-prod-모드에서의-동작-차이">🔍 dev 모드 vs prod 모드에서의 동작 차이</h2>
<h3 id="✔-개발-모드-npm-run-dev">✔ 개발 모드 (<code>npm run dev</code>)</h3>
<ul>
<li>코드 수정 → 변경된 부분만 자동 재컴파일  </li>
<li>빌드는 하지 않음  </li>
<li>개발 서버(Runtime)는 계속 유지됨  </li>
<li>화면은 HMR(핫 리로드)로 빠르게 반영됨</li>
</ul>
<h3 id="✔-프로덕션-모드-npm-run-build-→-배포">✔ 프로덕션 모드 (<code>npm run build</code> → 배포)</h3>
<ul>
<li>전체 번들링 + 최적화 + 압축 필수  </li>
<li>코드 수정 시 자동 반영 없음  </li>
<li>반드시 다시 <strong>빌드 → 배포</strong>해야 함  </li>
<li>최종 실행(Runtime)은 유저 브라우저 또는 서버에서 발생</li>
</ul>
<hr />
<h2 id="📱-빌드-타임-문제-vs-런타임-문제">📱 빌드 타임 문제 vs 런타임 문제</h2>
<p>프로그램 개발 과정에서는<br /><strong>빌드 시점(Build Time)</strong>과 <strong>런타임(Runtime)</strong>에서<br />발생하는 문제의 종류가 완전히 다릅니다.<br />각 시점에 따라 해결해야 할 문제도 달라지므로 구분이 중요합니다.</p>
<hr />
<h3 id="🚧-빌드-타임build-time--실행되기-전에-발생하는-문제">🚧 빌드 타임(Build Time) — 실행되기 전에 발생하는 문제</h3>
<p>빌드 타임은 <strong>코드를 실행 가능한 형태로 만들기 위한 준비 단계</strong>입니다.<br />이 단계에서 발생하는 오류는 모두 “실행 전에 반드시 해결해야 하는 문제”입니다.</p>
<h4 id="📌-어떤-문제가-발생하는가">📌 어떤 문제가 발생하는가?</h4>
<ul>
<li>React/Vite/Webpack <strong>빌드 오류</strong></li>
<li>환경 변수(<code>.env.production</code>) 누락  </li>
<li>Docker <strong>이미지 빌드 실패</strong>  </li>
<li>번들링 중 <strong>모듈 export/import 불일치</strong>  </li>
<li>타입 에러, 문법 에러, 경로 오류  </li>
</ul>
<h4 id="🛠-언제-해결해야-하는가">🛠 언제 해결해야 하는가?</h4>
<p>➡ <strong>배포(빌드) 전에 반드시 해결해야 함.</strong><br />빌드가 실패하면 애플리케이션은 실행조차 되지 않음.</p>
<hr />
<h3 id="⚙️-런타임runtime--프로그램-실행-중-발생하는-문제">⚙️ 런타임(Runtime) — 프로그램 실행 중 발생하는 문제</h3>
<p>런타임은 브라우저나 서버에서<br /><strong>프로그램이 실제로 돌아가는 순간</strong>입니다.<br />사용자가 앱을 사용하는 중에 발생하는 문제들입니다.</p>
<h4 id="📌-어떤-문제가-발생하는가-1">📌 어떤 문제가 발생하는가?</h4>
<ul>
<li>JS null/undefined <strong>접근 오류</strong></li>
<li>서버 API <strong>요청 실패</strong></li>
<li>DB 장애, 네트워크 오류  </li>
<li>로그인/권한/토큰 등 <strong>인증 오류</strong></li>
<li>사용자 입력값 검증 실패  </li>
</ul>
<h4 id="🛠-언제-해결해야-하는가-1">🛠 언제 해결해야 하는가?</h4>
<p>➡ <strong>프로덕션 안정성과 사용자 경험을 위해 실행 중에 처리해야 함.</strong><br />예외 처리, 재시도 로직, 에러 UI 등이 대표적인 해결 방법.</p>
<p><strong>빌드 타임 문제는 실행 전에 막고, 런타임 문제는 실행 중 안정성을 확보하는 방향으로 해결해야 합니.</strong></p>
<hr />
<h3 id="🖥️-어디에서-에러가-나타날까">🖥️ 어디에서 에러가 나타날까?</h3>
<p>빌드 타임과 런타임은 <strong>에러가 표시되는 위치가 다릅니다.</strong></p>
<h4 id="빌드-타임">빌드 타임</h4>
<ul>
<li><strong>터미널(콘솔)</strong>에서 빨간 에러로 표시됨  </li>
<li>GitHub Actions/Jenkins 같은 <strong>CI/CD 로그</strong>에서 빌드 실패로 표시  </li>
<li>VS Code 등 <strong>IDE에서 사전 경고</strong>로 보이기도 함  </li>
</ul>
<h4 id="런타임-에러">런타임 에러</h4>
<ul>
<li><strong>브라우저 개발자도구(Console)</strong>에 바로 표시됨  </li>
<li>React 에러 바운더리 등을 통해 <strong>화면(UI)</strong>에 에러 메시지가 뜰 수도 있음  </li>
<li>서버(Node.js)라면 <strong>서버 로그</strong>(CloudWatch, Sentry 등)에 기록  </li>
<li>사용자가 실제로 앱을 쓰는 중에 발생</li>
</ul>
<hr />
<h2 id="📌-한-줄-요약">📌 한 줄 요약</h2>
<blockquote>
<p><strong>컴파일 타임</strong> → 코드 검사 및 변환<br /><strong>빌드 타임</strong> → 실행 가능한 완제품(dist) 생성<br /><strong>런타임</strong> → 실제 실행  </p>
<p><strong>실행 전 오류 = 빌드(컴파일 포함) 타임 오류</strong><br /><strong>실행 중 오류 = 런타임 오류</strong>이다.</p>
</blockquote>