<p>앞의 글에서 알아본 <strong>CJS(CommonJS)</strong> 와 <strong>ESM(ECMAScript Module)</strong> 은<br />기본적으로 <strong>.js(.cjs, .mjs)</strong> 파일만 import(or require) 할 수 있습니다.</p>
<p>즉, 그 외의 CSS, JSON, JSX, 이미지 등의 파일은 import할 수 없다는것을 의미합니다.</p>
<p>그런데 생각해보면 우리는 <code>.jsx</code>나 <code>.css</code> 등을 import/ require 해서 쓰고 있습니다.
<strong>어떻게 된걸까요??</strong></p>
<p><strong>이글에서는 모듈 시스템의 한계와 번들러의 역할에 대해 알아보겠습니다.</strong></p>
<hr />
<h2 id="번들러란">번들러란?</h2>
<p>우리는 개발할 때 자연스럽게 <code>import</code> 와 <code>export</code> 를 사용합니다. 
이는 코드가 모듈 단위로 나누어져 있기 때문이죠. </p>
<p>현대 애플리케이션은 수백~수천 개의 파일로 구성되어 있습니다. 
이렇게 잘게 쪼개진 파일은 개발할 때는 유지보수에 유리하지만, 
<strong>배포 환경에서는 이러한 파일들을 효율적으로 로딩하기 위해 최적화가 필요합니다.</strong> </p>
<p>그래서 등장한 것이 바로 번들러(Bundler) 입니다. </p>
<p>번들러는 여러 파일을 하나(또는 여러 개)의 최적화된 파일로 묶어 네트워크 요청 수를 줄이고, 실행 성능을 높여줍니다.</p>
<blockquote>
<p>자세한 내용은<a href="https://velog.io/@sunmins/%EA%B0%9C%EB%B0%9C-%EC%9A%A9%EC%96%B4-%EC%82%AC%EC%A0%84-%EB%B2%88%EB%93%A4%EB%9F%ACBundler%EB%9E%80-1"> [개발 용어 사전] 번들러(Bundler)란? #1</a> 에서 확인하실수있습니다.</p>
</blockquote>
<h2 id="esm과-cjs는-기본적으로-js-만-내보내고-받아올-수-있음">ESM과 CJS는 기본적으로 <code>.js</code> 만 내보내고 받아올 수 있음</h2>
<p>또한 CSS·이미지·JSON·JSX 같은 파일을 <strong>JS 모듈처럼(JS 형태) 사용할 수 있도록 변환하는 역할도 합니다.</strong></p>
<p>JS 엔진(브라우저/Node)은 원래 다음 확장자만 모듈로 해석합니다:</p>
<ul>
<li><code>.js</code>  </li>
<li><code>.mjs</code>  </li>
<li><code>.cjs</code></li>
</ul>
<p>이 외 파일은 <strong>모듈로 해석할 수 없습니다.</strong></p>
<p>즉, 아래 문법은 원래 JS 엔진에서는 동작할 수 없습니다.
그렇다면 우리가 사용하던 </p>
<h3 id="esm-예시">ESM 예시</h3>
<pre><code class="language-js">import &quot;./styles.css&quot;;          // ❌ 원래 불가능
import data from &quot;./data.json&quot;; // ❌ 원래 불가능
import App from &quot;./App.jsx&quot;;    // ❌ 원래 불가능
import logo from &quot;./logo.png&quot;;  // ❌ 원래 불가능</code></pre>
<h3 id="cjs-예시">CJS 예시</h3>
<pre><code class="language-js">require(&quot;./styles.css&quot;);   // ❌ 원래 불가능
require(&quot;./data.json&quot;);    // ✔ Node에서는 JSON만 특수 케이스로 허용
require(&quot;./App.jsx&quot;);      // ❌ Node가 JSX 못 읽음
require(&quot;./image.png&quot;);    // ❌ 원래 불가능</code></pre>
<p>이런 문법들은 어떻게 사용할수 있는걸까요?
바로 번들러가 해당 파일들을 JS가 이해할 수 있는 형태로 변환해주기 때문에 가능합니다.
변환 과정을 살펴보겠습니다.</p>
<pre><code class="language-js">// CSS
import &quot;./styles.css&quot;;</code></pre>
<ol>
<li>번들러가 CSS 파일을 읽음</li>
<li>CSS 내용을 JS 코드로 변환하거나 <code>&lt;style&gt;</code>태그로 주입</li>
<li>브라우저에 적용됨</li>
</ol>
<pre><code class="language-js">// JSON
import data from &quot;./data.json&quot;;</code></pre>
<ul>
<li>번들러가 JSON을 JS 객체로 변환해 module로 만들어줌</li>
</ul>
<pre><code class="language-js">// JSX
import App from &quot;./App.jsx&quot;;</code></pre>
<ul>
<li>번들러 + 트랜스파일러가(Babel)가 JSX → JS로 컴파일
브라우저가 이해할 수 있는 코드로 바뀜</li>
</ul>
<pre><code class="language-js">// IMAGE
import logo from &quot;./logo.png&quot;;</code></pre>
<ul>
<li>번들러가 이미지 파일을 URL 형태, base64 등으로 변환
JS에서 사용할 수 있게 만듦</li>
</ul>
<h2 id="📌-한-줄-요약">📌 한 줄 요약</h2>
<blockquote>
<p><strong>ESM과 CJS는 원래 .js 파일만 import할 수 있다.
CSS/JSX/이미지/JSON을 import하는 기능은 ‘번들러가 만들어낸 확장 기능’이다.</strong></p>
</blockquote>