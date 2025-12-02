<p><strong>트랜스파일러(Transpiler) / 컴파일러(Compiler)</strong>는  
코드를 실행 가능한 형태의 코드로 바꿔주는 도구입니다.</p>
<p>주로 다음 상황에서 사용됩니다:</p>
<ul>
<li><strong>TypeScript → JavaScript 변환</strong></li>
<li><strong>최신 JavaScript → 구형 브라우저 호환 JS로 변환 (Babel)</strong></li>
</ul>
<p>즉, 사람이 작성한 코드를<br /><strong>브라우저가 이해할 수 있는 형태로 ‘번역’하는 도구</strong>라고 볼 수 있습니다.</p>
<blockquote>
<p>“개발자가 쓰기 편한 언어를<br />브라우저가 이해할 수 있는 언어로 바꿔주는 번역기”</p>
</blockquote>
<p>참고로, <strong>트랜스파일러는 같은 수준의 언어끼리 변환(TypeScript → JavaScript, 최신 JS → 구형 JS)</strong>하고<br /><strong>컴파일러는 더 낮은 수준의 코드(Java → 바이트코드 등)로 변환</strong>하는 차이가 있습니다.<br />하지만 프론트엔드에서는 <strong>브라우저가 실행할 수 있는 형태의 JS만 필요하기 때문에</strong><br /><strong>두 도구의 개념적 차이가 크게 드러나지 않으며, 실질적으로 비슷한 역할을 수행합니다.</strong>
이 글에서는 프론트엔드에서 실제로 많이 사용되는 트랜스파일러를 중심으로 살펴보겠습니다.</p>
<hr />
<h2 id="💡-왜-트랜스파일러가-필요할까">💡 왜 트랜스파일러가 필요할까?</h2>
<h3 id="1-브라우저가-tsjsx를-직접-이해하지-못함">1) 브라우저가 TS/JSX를 직접 이해하지 못함</h3>
<p>React의 JSX, TypeScript의 타입 문법은<br />브라우저가 직접 실행할 수 없습니다.</p>
<pre><code class="language-ts">const add = (a: number, b: number): number =&gt; a + b;</code></pre>
<p>이 코드는 <strong>트랜스파일러(TypeScript Compiler, Babel)</strong> 을 거쳐<br />순수 JavaScript(타입·JSX가 제거된 표준 JS)로 변환되어야 실행 가능합니다.</p>
<p>참고로, TS Compiler(tsc)와 Babel은 상황에 따라 각각 혹은 함께 사용될 수 있습니다.</p>
<ul>
<li>어떤 프로젝트는 tsc만 사용하고</li>
<li>어떤 프로젝트는 Babel만 TS 변환을 처리하며</li>
<li>일부는 tsc는 타입 검사만, 실제 변환은 Babel이 담당하기도 합니다.</li>
</ul>
<p>또한 Webpack 환경에서는 <code>ts-loader</code>라는 용어도 자주 등장합니다.
<code>ts-loader</code>는 Webpack이 TypeScript 파일을 처리할 수 있도록 <strong>tsc를 연결해주는 로더이며,</strong>
실제로 TS → JS 변환을 수행하는 것은 항상 TypeScript Compiler(tsc) 입니다.</p>
<hr />
<h3 id="2-최신-js-기능을-오래된-브라우저에서-실행하려면-변환이-필요함">2) 최신 JS 기능을 오래된 브라우저에서 실행하려면 변환이 필요함</h3>
<p>Optional chaining(?.), Nullish(??) 같은 최신 문법은<br />구형 브라우저에서 동작하지 않습니다.</p>
<p>Babel은 이런 코드를 다음처럼 변환합니다:</p>
<pre><code class="language-js">user?.profile?.name ?? &quot;Guest&quot;;</code></pre>
<pre><code class="language-js">var _a, _b;
var name =
  ((_a = user) === null || _a === void 0
    ? void 0
    : (_b = user.profile) === null || _b === void 0
    ? void 0
    : _b.name) || &quot;Guest&quot;;</code></pre>
<p>덕분에 <strong>구형 브라우저에서도 안정적으로 실행</strong>됩니다.
이를 다운레벨링이라고 합니다.</p>
<blockquote>
<p> <strong>다운레벨링: 브라우저가 이해하지 못하는 최신 JavaScript 문법을
 오래된 브라우저에서도 돌아가도록 더 낮은 버전의 JavaScript로 변환하는 것</strong></p>
</blockquote>
<hr />
<h3 id="3-개발자가-쓰기-좋은-코드와-브라우저가-이해할-수-있는-코드는-다르기-때문">3) 개발자가 쓰기 좋은 코드와 브라우저가 이해할 수 있는 코드는 다르기 때문</h3>
<p>개발자는 TS, 최신 JS, JSX, Decorator 등을 쓰고 싶어 하고<br />브라우저는 <strong>순수 JavaScript만</strong> 실행할 수 있습니다.</p>
<p>트랜스파일러는 이 둘 사이의 <strong>번역기 역할</strong>을 담당합니다.</p>
<hr />
<h2 id="🛠-대표적인-트랜스파일러">🛠 대표적인 트랜스파일러</h2>
<h3 id="✔️-typescript-compiler-tsc">✔️ TypeScript Compiler (tsc)</h3>
<pre><code>TS → JS 변환 + 타입 검사</code></pre><ul>
<li>TS/JSX → JS 변환 (타입 검사 가능)
최신 JS → 구형 JS 변환 기능은 제한적  </li>
<li>번들 기능 없음 → Webpack/Vite/Rollup과 함께 사용</li>
</ul>
<h4 id="장점">장점</h4>
<ul>
<li><strong>정확한 타입 검사</strong></li>
<li>TS 문법 처리에 최적화</li>
</ul>
<h4 id="단점">단점</h4>
<ul>
<li><strong>최신 JS → 구형 JS 변환 기능이 약함</strong></li>
<li>변환 속도가 Babel/esbuild보다 느림</li>
<li>폴리필 자동 적용 없음</li>
</ul>
<hr />
<h3 id="✔️-babel">✔️ Babel</h3>
<pre><code>TS/JSX → JS 변환 + 최신 JS → 구형 JS 변환에 강함</code></pre><ul>
<li>TS/JSX → JS 변환 (타입은 제거만 함)</li>
<li>최신 ESNext 문법을 구형 브라우저 호환 JS로 변환</li>
<li>다양한 플러그인·프리셋을 지원</li>
<li>Webpack 환경에서 널리 사용</li>
</ul>
<h4 id="장점-1">장점</h4>
<ul>
<li><strong>브라우저 호환성 변환 최강 (ESNext → ES5 등)</strong></li>
<li>플러그인 생태계가 매우 풍부</li>
</ul>
<h4 id="단점-1">단점</h4>
<ul>
<li><strong>타입 검사 기능 없음</strong></li>
<li>변환 속도는 빠른 편이나 순수 변환 속도는 esbuild보다 느림</li>
</ul>
<p>👉 참고로, <strong>tsc와 Babel은 모두 TS → JS 변환이 가능하고, 최신 JS를 구형 JS로 변환하는 기능도 제공합니다.</strong><br />다만 두 도구의 강점은 다릅니다.</p>
<ul>
<li><strong><code>tsc</code>는 타입 검사와 TS 문법 처리에 유리하고</strong>, 최신 JS 변환 기능은 비교적 제한적입니다.  </li>
<li><strong><code>Babel</code>은 빠른 속도와 강력한 브라우저 호환성(최신 JS → 구형 JS 변환)</strong>에 최적화되어 있으며, 타입을 검사하지 않고 단순히 제거하는 방식으로 TS를 처리합니다.</li>
</ul>
<hr />
<h3 id="✔️-esbuild">✔️ esbuild</h3>
<pre><code> Go 기반  초고속 트랜스파일러 + 번들러</code></pre><ul>
<li>TS/JSX → JS 변환(타입은 제거만 함)</li>
<li>최신 JS → 구형 JS 변환 지원(target 옵션, Babel보다 단순)</li>
<li>개발 서버(HMR)에서 매우 빠르게 동작</li>
<li>번들러 기능 포함</li>
</ul>
<h4 id="장점-2">장점</h4>
<ul>
<li><strong>가장 빠른 TS/JSX 변환 속도</strong></li>
<li>dev 환경에 최적 (Vite가 빠른 이유)</li>
</ul>
<h4 id="단점-2">단점</h4>
<ul>
<li><strong>타입 검사 없음</strong></li>
<li>브라우저 호환성 변환은 Babel만큼 정교하지 않음</li>
<li>플러그인 생태계는 Babel 대비 적음</li>
</ul>
<hr />
<h2 id="✅-비교">✅ 비교</h2>
<table>
<thead>
<tr>
<th>도구</th>
<th>주요 역할</th>
<th>다운레벨링(최신 JS → 구형 JS)</th>
<th>특징 요약</th>
</tr>
</thead>
<tbody><tr>
<td><strong>tsc</strong></td>
<td>TS → JS 변환 + 타입 검사</td>
<td>제한적</td>
<td><strong>타입 검사 지원</strong>, TS 문법 처리에 최적화</td>
</tr>
<tr>
<td><strong>Babel</strong></td>
<td>TS/JSX → JS 변환 + 브라우저 호환성 변환</td>
<td><strong>매우 강함 (업계 최강)</strong></td>
<td>플러그인 생태계 풍부, Webpack과 가장 잘 맞음 (babel-loader)</td>
</tr>
<tr>
<td><strong>esbuild</strong></td>
<td>TS/JSX → JS 변환 + 번들링</td>
<td>지원하나 Babel보다 단순</td>
<td><strong>초고속 변환</strong>, Vite dev 서버 핵심</td>
</tr>
</tbody></table>
<h3 id="tsc">tsc</h3>
<p>→ TS → JS 변환 + <strong>타입 검사 강함.</strong> 다운레벨링은 약함.</p>
<h3 id="babel">Babel</h3>
<p>→ TS/JSX 변환 가능(타입 제거), <strong>브라우저 호환성 변환 최고</strong>.
= 모든 브라우저에서 실행 가능’하게 바꿔주는 능력이 가장 뛰어남.</p>
<h3 id="esbuild">esbuild</h3>
<p>→ <strong>초고속 변환</strong>, TS/JSX 변환 빠름. 다운레벨링 가능하지만 Babel보다 단순.</p>
<hr />
<h2 id="📌-한-줄-요약">📌 한 줄 요약</h2>
<blockquote>
<p><strong>트랜스파일러는 개발자가 쓰기 편한 코드(TS/JSX/최신 JS)를<br />브라우저가 실행할 수 있는 순수 JavaScript로 변환하는 “코드 번역기”이다.</strong></p>
</blockquote>