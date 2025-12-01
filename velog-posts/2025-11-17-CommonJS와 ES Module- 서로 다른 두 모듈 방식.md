<p>프로젝트를 들여다보면 <code>import</code>, <code>export</code>, <code>require</code>, <code>module.exports</code> 같은 문법이 섞여 있는 경우가 많습니다.</p>
<p><strong>&quot;CommonJS가 옛날 거고, ES Module이 요즘 방식이다&quot;</strong> 정도로만 알고 있었지만<br />정확히 <strong>무엇이 어떻게 다른지</strong>,  
그리고 <code>.js</code>, <code>.cjs</code>, <code>.mjs</code>가 <strong>왜 서로 다르게 동작하는지</strong> 한 번 정리해보겠습니다.</p>
<hr />
<h2 id="1️⃣-자바스크립트에서-모듈-시스템이란">1️⃣ 자바스크립트에서 “모듈 시스템”이란?</h2>
<p>자바스크립트 코드가 실행될 때, 파일끼리 기능을 나누고 가져오려면<br /><strong>모듈 시스템</strong>이라는 규칙이 필요합니다.</p>
<p>여기서 “파일을 나누고 가져온다”는 말은,<br />기능을 여러 파일로 분리해 작성하고 필요한 곳에서<br /><code>import</code>(또는 <code>require</code>)로 <strong>다른 파일의 기능을 불러와 사용하는 것</strong>을 의미합니다.</p>
<p>예를 들면:</p>
<pre><code class="language-js">// utils.js
export function add(a, b) { return a + b; }

// main.js
import { add } from &quot;./utils.js&quot;;
console.log(add(1, 2));</code></pre>
<p>모듈 시스템은 다음을 결정합니다.</p>
<ul>
<li><strong>이 파일을 어떻게 불러오는가?</strong> (<code>import</code>? or <code>require</code>?)</li>
<li><strong>누가 이 파일을 어떻게 해석하는가?</strong> (Node? or 브라우저?)</li>
<li><strong>코드를 언제 로딩할 것인가?</strong> (정적 로딩(정적)? or 런타임 로딩(동적)?)</li>
<li><strong>어떤 스코프에서 실행되는가?</strong> (파일 스코프)</li>
<li><strong>동적 import를 지원하는가?</strong></li>
</ul>
<p>이 규칙에 따라 자바스크립트는 두 가지 방식으로 발전했습니다.</p>
<ul>
<li><strong>CommonJS (CJS)</strong> — Node 초창기부터 쓰던 방식  </li>
<li><strong>ES Module (ESM)</strong> — 자바스크립트 공식 표준 모듈 방식</li>
</ul>
<hr />
<h2 id="2️⃣-commonjs-cjs--nodejs의-전통적인-모듈-시스템">2️⃣ CommonJS (CJS) — Node.js의 전통적인 모듈 시스템</h2>
<p>CommonJS는 Node.js에서 오랫동안 기본으로 사용되던 방식입니다.<br /><code>require</code>와 <code>module.exports</code> 문법을 사용합니다.</p>
<pre><code class="language-js">// 가져오기
const fs = require(&quot;fs&quot;);

// 내보내기
module.exports = {
  foo: 1,
  bar() {},
};</code></pre>
<h3 id="2-1️⃣-commonjs의-특징">2-1️⃣ CommonJS의 특징</h3>
<table>
<thead>
<tr>
<th>특징</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td><strong>동기적 로딩</strong></td>
<td><code>require()</code>를 호출하는 순간 파일을 실행하고 결과를 반환</td>
</tr>
<tr>
<td><strong>런타임 로딩</strong></td>
<td>if문 안에서도 <code>require</code> 가능</td>
</tr>
<tr>
<td><strong>캐싱</strong></td>
<td>한 번 실행된 모듈은 캐싱되어 두 번 실행되지 않음</td>
</tr>
<tr>
<td><strong>함수 스코프에서 실행됨</strong></td>
<td>파일이 내부적으로 하나의 래퍼 함수로 감싸진 상태에서 실행됨</td>
</tr>
<tr>
<td><strong>Node.js 기본 모듈 방식</strong></td>
<td>오래된 라이브러리 대부분 CJS 기반</td>
</tr>
</tbody></table>
<h3 id="2-2️⃣-require는-이렇게-동작합니다">2-2️⃣ require는 이렇게 동작합니다</h3>
<pre><code class="language-js">if (process.env.NODE_ENV === &quot;development&quot;) {
  const devTool = require(&quot;./devTool&quot;);
}</code></pre>
<p>이 코드는 <strong>CommonJS의 require가 런타임에 실행된다는 것</strong>을 보여주는 예시입니다.<br />여기서 <em>런타임 실행</em>이라는 말은,</p>
<blockquote>
<p><strong>코드를 실제로 실행하는 순간(require가 호출되는 그 순간)에 모듈을 불러온다</strong><br />는 뜻입니다.</p>
</blockquote>
<p>즉, <code>require()</code>는 함수처럼 동작하기 때문에</p>
<ul>
<li>조건문 안에서도 사용할 수 있고  </li>
<li>변수로 경로를 조합할 수도 있고  </li>
<li>실행 흐름에 따라 어떤 모듈을 불러올지 결정할 수도 있습니다.</li>
</ul>
<p>이런 동작 방식은 ES Module의 <code>import</code>와 큰 차이가 있습니다.</p>
<hr />
<h3 id="❗import로는-구현할-수-없습니다">❗<code>import</code>로는 구현할 수 없습니다.</h3>
<p>ES Module에서는 아래와 같은 코드는 <strong>문법 오류</strong>가 발생합니다.</p>
<pre><code class="language-js">if (something) {
  import x from &quot;./x.js&quot;;  // ❌ SyntaxError
}</code></pre>
<p>ES Module의 <code>import</code>는</p>
<ul>
<li>코드가 실제 실행되기 <strong>전</strong>(runtime 이전)</li>
<li>자바스크립트 엔진이 코드를 <strong>정적으로 분석하는 단계에서</strong></li>
<li>어떤 모듈을 불러올지** 미리 결정되어야 하기 때문**입니다.</li>
</ul>
<p>그래서 ES Module의 <code>import</code>는 <strong>반드시 파일 최상단(top-level)</strong> 에 위치해야 합니다.
<code>import</code>는 정적 로딩 방식이고,
<code>require</code>는 런타임 동적 로딩 방식이라는 차이가 여기에서 드러납니다.</p>
<p>이런 동작 방식은 ES Module의 import와 CommonJS의 require가 가지는 중요한 차이점입니다.</p>
<hr />
<h2 id="3️⃣-es-module-esm--공식-표준-모듈-방식">3️⃣ ES Module (ESM) — 공식 표준 모듈 방식</h2>
<p>ES Module은 브라우저와 Node에서 공식으로 사용하는 모듈 방식입니다.
<code>import</code>와 <code>export</code> 문법을 사용합니다.</p>
<pre><code class="language-js">// 가져오기
import fs from &quot;fs&quot;;

// 내보내기 (named export)
export const a = 1;

// 기본 내보내기 (default export)
export default function () {
  console.log(&quot;hello&quot;);
}</code></pre>
<h3 id="3-1️⃣-export--export-default의-차이">3-1️⃣ export / export default의 차이</h3>
<p>ESM에서는 두 가지 방식으로 값을 내보낼 수 있습니다.</p>
<h4 id="🔵-named-export-export">🔵 Named Export (<code>export</code>)</h4>
<p>여러 개를 내보낼 수 있으며, 가져올 때 반드시 같은 이름을 사용해야 합니다.</p>
<pre><code class="language-js">// math.js
export const add = (a, b) =&gt; a + b;
export const subtract = (a, b) =&gt; a - b;</code></pre>
<pre><code class="language-js">// main.js
import { add, subtract } from &quot;./math.js&quot;;</code></pre>
<h4 id="🟢-default-export-export-default">🟢 Default Export (export default)</h4>
<p>파일당 하나만 존재하며, 가져오는 쪽에서 이름을 마음대로 정할 수 있습니다.</p>
<pre><code class="language-js">// hello.js
export default function () {
  console.log(&quot;hello&quot;);
}</code></pre>
<pre><code class="language-js">// main.js
import greet from &quot;./hello.js&quot;; // 이름을 자유롭게 설정 가능</code></pre>
<p>Named Export는 <strong>여러 개의 기능을 개별적으로 내보낼 때</strong>, 
Default Export는 <strong>파일의 대표 기능</strong>을 내보낼 때 유용합니다.</p>
<hr />
<h3 id="3-2️⃣-named-vs-default--왜-가져오는-방식이-다를까">3-2️⃣ Named vs Default — 왜 가져오는 방식이 다를까?</h3>
<p>ESM은 내부적으로 다음과 같이 동작합니다.</p>
<h4 id="1-named-export는-여러-값을-가진-객체처럼-동작합니다">1) Named Export는 “여러 값을 가진 객체처럼” 동작합니다.</h4>
<p>여러 개의 export가 가능하기 때문에, 모듈은 내부적으로 다음과 비슷한 구조를 가집니다:</p>
<pre><code class="language-js">{
  add: function,
  subtract: function
}</code></pre>
<p>따라서 가져올 때도 객체에서 필요한 속성만 꺼내오는 것처럼
<strong>구조 분해 import</strong>가 필요합니다.</p>
<pre><code class="language-js">import { add } from &quot;./math.js&quot;;</code></pre>
<p>✅ Named Export는 여러 개의 &quot;이름이 고정된 값&quot;을 내보내기 때문에<br />   가져올 때도 반드시 <code>{ 이름 }</code> 형태로 일치시켜야 합니다.</p>
<h4 id="2-default-export는-모듈의-대표값-하나를-의미합니다">2) Default Export는 “모듈의 대표값 하나”를 의미합니다.</h4>
<p>default export는 파일당 한 개이며, 내부적으로는 다음과 같이 표현됩니다:</p>
<pre><code class="language-js">{
  default: function() {}
}</code></pre>
<p>그래서 아래 두 코드는 완전히 같은 의미이며,</p>
<pre><code class="language-js">import { default as greet } from &quot;./hello.js&quot;;
import greet from &quot;./hello.js&quot;;  // 원하는 이름으로 불러오기 가능</code></pre>
<p><strong>가져올 때 이름을 자유롭게 지을 수 있는 것</strong>이 특징입니다.</p>
<p>✅ Default Export는 모듈의 &quot;대표값&quot;을 의미하며 하나만 존재하므로<br />   가져오는 쪽에서 어떤 이름으로든 자유롭게 매핑할 수 있습니다.</p>
<hr />
<h3 id="3-3️⃣-es-module-특징">3-3️⃣ ES Module 특징</h3>
<table>
<thead>
<tr>
<th>특징</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td><strong>정적 분석 가능</strong></td>
<td><code>import</code>는 파일 최상단에서만 가능하며 코드 실행 이전에 분석됨</td>
</tr>
<tr>
<td><strong>트리 쉐이킹 가능</strong></td>
<td>사용되지 않는 코드를 제거할 수 있어 번들 최적화에 유리</td>
</tr>
<tr>
<td><strong>top-level await 지원</strong></td>
<td>모듈 최상단에서 <code>await</code> 사용 가능</td>
</tr>
<tr>
<td><strong>모듈 스코프에서 실행됨</strong></td>
<td>파일이 함수로 감싸지지 않고 독립된 모듈 스코프에서 실행됨</td>
</tr>
<tr>
<td><strong>브라우저/Node 공식 표준</strong></td>
<td>modern JS의 기본 모듈 시스템</td>
</tr>
</tbody></table>
<h3 id="3-4️⃣-import는-이렇게-동작합니다">3-4️⃣ import는 이렇게 동작합니다</h3>
<pre><code class="language-js">import utils from &quot;./utils.js&quot;;</code></pre>
<p>이 코드는 <strong>ES Module의 정적 import가 실행 전에 로딩된다는 것</strong>을 보여줍니다.
<code>import</code> 구문은 CommonJS의 <code>require()</code>와 달리** 코드 실행 도중에 호출되는 함수가 아닙니다.**</p>
<p>즉, 정적 import는 다음과 같은 특징을 가집니다:</p>
<ul>
<li>항상 파일의 최상위(top-level) 에 존재해야 합니다.</li>
<li>조건문, 함수, 반복문 내부에서는 사용할 수 없습니다.</li>
<li>코드를 실행하기 전에 JS 엔진이 모듈을 미리 불러오고 의존성을 분석합니다.</li>
<li>이런 특성 덕분에 정적 분석과 트리 쉐이킹 최적화가 가능합니다.</li>
</ul>
<p>정적 import는 “실행되기 전에 이미 로딩된 상태”에서 코드가 시작된다고 보면 됩니다.</p>
<hr />
<h3 id="3-5️⃣-동적-로드는-import-사용">3-5️⃣ 동적 로드는 <code>import()</code> 사용</h3>
<pre><code class="language-js">if (condition) {
  const module = await import(&quot;./tool.js&quot;);
}</code></pre>
<p>이 코드는 <strong>ES Module</strong>의 <code>import()</code>가 런<strong>타임에 동적으로 모듈을 로딩한다는 것</strong>을 보여줍니다.
<code>import()</code>는 정적 import와 달리 <strong>비동기 함수처럼 실행될 때 호출</strong>됩니다.</p>
<p><code>import()</code>의 특징은 다음과 같습니다:</p>
<ul>
<li>조건문 안에서도 사용 가능</li>
<li>함수 안에서도 호출 가능</li>
<li>필요할 때만 모듈을 불러오는 lazy-loading 구현 가능</li>
<li>Promise 기반이므로 await로 값을 받을 수 있음</li>
</ul>
<p>정적 import는 top-level에서만 사용할 수 있지만,
<code>import()</code>는 실행 흐름에 따라 모듈을 불러오는 <strong>동적 로딩 방식</strong>입니다.</p>
<p>이 두 가지 방식 덕분에 ES Module은
“정적 로딩을 통한 최적화”와
“런타임 로딩을 통한 유연함”을 모두 가질 수 있습니다.</p>
<hr />
<h2 id="💡참고-핵심-개념-정리">💡참고: 핵심 개념 정리</h2>
<h3 id="🔍-정적-분석이-가능하다는-것은">🔍 정적 분석이 가능하다는 것은?</h3>
<p>ESM의 <code>import</code>는 <strong>항상 파일 최상단(top-level)</strong> 에 있어야 하며<br />브라우저나 Node.js가 <strong>코드를 실행하기 전에 미리 분석(파싱)</strong> 합니다.</p>
<p>즉,</p>
<ul>
<li>어떤 파일이 어떤 모듈을 import하는지</li>
<li>어떤 export가 사용되고 있는지</li>
<li>의존성 그래프가 어떻게 구성되는지</li>
</ul>
<p>이 모든 것을 <strong>실행되지 않아도 미리 알 수 있음</strong>.</p>
<hr />
<h3 id="🌲-트리-쉐이킹tree-shaking이란">🌲 트리 쉐이킹(Tree Shaking)이란?</h3>
<p>트리 쉐이킹은  </p>
<blockquote>
<p><strong>사용되지 않는(export 되었지만 import되지 않은) 코드를 번들에서 제거하는 최적화 기술</strong><br />을 의미합니다.</p>
</blockquote>
<p>예시:</p>
<pre><code class="language-js">// util.js
export function a() {}
export function b() {}
export function c() {}</code></pre>
<pre><code class="language-js">// main.js
import { a } from &quot;./util.js&quot;;</code></pre>
<p>이 경우 번들러는:</p>
<ul>
<li><code>a()</code>만 사용됨  </li>
<li><code>b()</code>, <code>c()</code>는 사용되지 않음 → 빌드 결과에서 제거됨</li>
</ul>
<p>즉,</p>
<p>✔ 파일은 커도<br />✔ 실제 사용되는 코드만 남아<br />✔ 결과적으로 <strong>번들 크기가 줄고 속도도 빨라짐</strong></p>
<blockquote>
<p>CommonJS(require)는 런타임 로딩 방식이기 때문에<br />이런 최적화가 사실상 <strong>불가능</strong>합니다.</p>
</blockquote>
<hr />
<h3 id="⏳-top-level-await란">⏳ top-level await란?</h3>
<p>기존 자바스크립트에서는 <code>await</code>를 반드시 <strong>async 함수 안에서만</strong> 사용할 수 있었음.<br />하지만 <strong>ESM에서는 모듈 최상단에서도 await 사용 가능</strong>합니다.</p>
<pre><code class="language-js">// data.js
const res = await fetch(&quot;/api/data&quot;);
export const data = await res.json();</code></pre>
<p>이렇게 하면:</p>
<ul>
<li>모듈이 실제 데이터를 다 받아올 때까지 이 파일을 import하는 다른 모듈도 로딩을 기다림</li>
</ul>
<p>즉,</p>
<p>✔ 초기 데이터 로딩
✔ 설정(config) 파일 로딩
✔ 환경(env) 값 로딩
✔ 비동기 준비 작업</p>
<p>이런 작업을 모듈 최상단에서 바로 처리할 수 있어 구조가 훨씬 깔끔해집니다.</p>
<blockquote>
<p>top-level await는 ESM에서만 가능하며
CommonJS(require)에서는 지원되지 않습니다.</p>
</blockquote>
<h2 id="4️⃣-nodejs는-어떻게-파일을-cjsesm으로-구분할까">4️⃣ Node.js는 어떻게 파일을 CJS/ESM으로 구분할까?</h2>
<p>Node.js가 모듈을 해석할 때 사용하는 기준은 크게 두 가지입니다.</p>
<ol>
<li><strong>파일 확장자 (.cjs, .mjs)</strong></li>
<li><strong>package.json의 <code>&quot;type&quot;</code> 설정</strong></li>
</ol>
<p>이 두 기준을 조합하여<br /><strong>“이 파일은 CJS인가? ESM인가?”</strong> 를 결정합니다.</p>
<hr />
<h2 id="확장자-기반-구분">확장자 기반 구분</h2>
<h3 id="cjs-→-commonjs-강제">.cjs → CommonJS 강제</h3>
<p><code>.cjs</code> 확장자는 Node에게<br /><strong>“이 파일은 CommonJS 방식으로 읽어라”</strong> 명확히 지시합니다.</p>
<pre><code class="language-js">// example.cjs
const fs = require(&quot;fs&quot;);

module.exports = { hello: &quot;world&quot; };</code></pre>
<hr />
<h3 id="mjs-→-es-module-강제">.mjs → ES Module 강제</h3>
<p><code>.mjs</code>는 Node에게<br /><strong>“이 파일은 ES Module로 읽어라”</strong> 라고 명확히 지시합니다.</p>
<pre><code class="language-js">// example.mjs
import fs from &quot;fs&quot;;

export const hello = &quot;world&quot;;</code></pre>
<hr />
<h3 id="js-파일은-packagejson-type-설정을-따른다">.js 파일은 package.json &quot;type&quot; 설정을 따른다</h3>
<p>Node는 <code>.js</code> 파일이 CJS인지 ESM인지 <strong>자동으로 판단하지 않습니다.</strong><br />따라서 <code>package.json</code>의 <code>&quot;type&quot;</code> 값을 기준으로 해석합니다.</p>
<hr />
<h2 id="packagejson-type별-동작">package.json &quot;type&quot;별 동작</h2>
<h3 id="🔹-type이-commonjs-이거나-없으면">🔹 type이 <code>&quot;commonjs&quot;</code> 이거나 없으면</h3>
<pre><code class="language-json">{
  &quot;type&quot;: &quot;commonjs&quot;
}</code></pre>
<ul>
<li><code>.js</code> → CommonJS</li>
<li><code>.cjs</code> → CommonJS</li>
<li><code>.mjs</code> → ES Module</li>
</ul>
<h3 id="🔹-type이-module이면">🔹 type이 <code>&quot;module&quot;</code>이면</h3>
<ul>
<li><code>.js</code> → ES Module</li>
<li><code>.cjs</code> → CommonJS</li>
<li><code>.mjs</code> → ES Module</li>
</ul>
<table>
<thead>
<tr>
<th>package.json</th>
<th>.js</th>
<th>.cjs</th>
<th>.mjs</th>
</tr>
</thead>
<tbody><tr>
<td>없음 / <code>&quot;commonjs&quot;</code></td>
<td>CJS</td>
<td>CJS</td>
<td>ESM</td>
</tr>
<tr>
<td><code>&quot;module&quot;</code></td>
<td>ESM</td>
<td>CJS</td>
<td>ESM</td>
</tr>
</tbody></table>
<hr />
<h2 id="🤔-왜-cjs--mjs를-따로-사용할까">🤔 왜 .cjs / .mjs를 따로 사용할까?</h2>
<p><strong>package.json의 &quot;type&quot; 설정은 프로젝트 전체의 기본값만 결정</strong>합니다.
하지만 실제 개발에서는 파일 단위로 CJS와 ESM을 섞어서 사용해야 하는 상황이 자주 발생합니다.</p>
<p>그래서 .cjs / .mjs 확장자가 필요합니다.</p>
<h3 id="esm-프로젝트인데-require가-꼭-필요한-경우">ESM 프로젝트인데 require가 꼭 필요한 경우</h3>
<p>예:</p>
<ul>
<li>오래된 라이브러리가 CommonJS(require)만 제공</li>
<li>런타임 동적 로딩(require)이 필요한 경우</li>
</ul>
<p>이런 경우 .cjs로 강제 처리해야 합니다.</p>
<hr />
<h3 id="cjs-프로젝트인데-import가-필요한-경우">CJS 프로젝트인데 import가 필요한 경우</h3>
<p>예:</p>
<ul>
<li>top-level await 사용</li>
<li>import-only 패키지 사용</li>
<li>최신 문법을 부분적으로 적용하고 싶을 때</li>
</ul>
<p>이런 경우 .mjs로 강제 처리합니다.</p>
<hr />
<h3 id="라이브러리-배포-시-cjs--esm-둘-다-제공해야-하기-때문">라이브러리 배포 시 CJS + ESM 둘 다 제공해야 하기 때문</h3>
<p>npm 패키지들은 보통 이렇게 배포합니다:</p>
<pre><code class="language-bash">dist/index.cjs   ← CommonJS 버전  
dist/index.mjs   ← ES Module 버전</code></pre>
<p>Node 구버전 생태계(CJS)와
최신 번들러·브라우저 환경(ESM)을 모두 지원하기 위함입니다.</p>
<h3 id="✅-정리">✅ 정리</h3>
<ul>
<li><code>&quot;type&quot;</code>은 기본 규칙 설정</li>
<li><code>.cjs</code>, .<code>mjs</code>는 개별 파일 규칙 강제</li>
</ul>
<hr />
<h2 id="5️⃣-typescript는-어떻게-모듈이-결정될까">5️⃣ TypeScript는 어떻게 모듈이 결정될까?</h2>
<p>TypeScript는 <strong>언어 계층</strong>,  
CJS/ESM은 <strong>실행 환경(빌드 결과)</strong>에서 결정됩니다.</p>
<p>즉, TS 파일에서 <code>import/export</code> 문법을 사용하더라도<br />최종적으로 컴파일된 JS 결과물은 <strong>CJS가 될 수도, ESM이 될 수도 있습니다.</strong></p>
<hr />
<h3 id="📘-tsconfigjson-설정">📘 tsconfig.json 설정</h3>
<pre><code class="language-json">{
  &quot;compilerOptions&quot;: {
    &quot;module&quot;: &quot;CommonJS&quot;
    // &quot;module&quot;: &quot;ESNext&quot; → ESM 출력
  }
}</code></pre>
<p>정리하면:</p>
<ul>
<li>TypeScript → 문법을 제공</li>
<li>JavaScript 결과물 → 환경 설정에 따라 CJS 또는 ESM으로 결정됨</li>
</ul>
<h2 id="6️⃣-commonjs-vs-es-module--무엇을-써야-할까">6️⃣ CommonJS vs ES Module — 무엇을 써야 할까?</h2>
<table>
<thead>
<tr>
<th>상황</th>
<th>추천</th>
</tr>
</thead>
<tbody><tr>
<td><strong>프론트엔드</strong></td>
<td>ES Module</td>
</tr>
<tr>
<td><strong>Node 최신 프로젝트</strong></td>
<td>ES Module 권장</td>
</tr>
<tr>
<td><strong>기존 레거시 Node 프로젝트</strong></td>
<td>CommonJS 유지</td>
</tr>
<tr>
<td><strong>라이브러리 제작</strong></td>
<td>CJS + ESM 둘 다 제공</td>
</tr>
</tbody></table>
<hr />
<h2 id="✅-정리-1">✅ 정리</h2>
<ul>
<li><p><strong>CommonJS(CJS)</strong><br />→ 런타임 기반 모듈 로딩<br />→ <code>require</code>, <code>module.exports</code><br />→ 오래된 Node 생태계에서 널리 사용</p>
</li>
<li><p><strong>ES Module(ESM)</strong><br />→ 정적 분석 기반 공식 표준<br />→ <code>import</code>, <code>export</code><br />→ 브라우저 &amp; 최신 Node 기본 모듈 방식</p>
</li>
</ul>
<hr />
<h2 id="💬-마무리">💬 마무리</h2>
<p>CommonJS와 ES Module은 단순히 “예전 방식과 최신 방식의 차이” 정도로만 알고 있었는데,
이번에 정리하면서 자바스크립트가 파일을:</p>
<ul>
<li>어떻게 해석하고  </li>
<li>언제 로딩하며  </li>
<li>어떤 스코프에서 실행하는지  </li>
</ul>
<p>를 결정하는 <strong>근본적인 동작 원리</strong>라는 것을 확실히 이해하게 되었습니다.</p>
<p>또한 </p>
<ul>
<li><code>&quot;type&quot;</code> 설정은 프로젝트 전체의 기본 동작 방식을 지정하고,</li>
<li><code>.cjs / .mj</code>s는 파일 개별적으로 동작 방식을 강제할 수 있다는 점,</li>
<li>실제 개발에서는 두 방식이 혼용되는 이유 </li>
</ul>
<p>까지 이해하게 되어, 앞으로 어떤 상황에서 CommonJS와 ESM을 선택해야 할지 명확해졌습니다.</p>