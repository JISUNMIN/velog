<h2 id="상황">상황</h2>
<p>영문화 작업을 진행하면서<br />기존에 <strong>상수 배열을 반환하던 함수</strong>에  
번역 함수 <code>t</code>를 주입하는 구조로 변경했다.</p>
<h3 id="변경-전">변경 전</h3>
<pre><code class="language-ts">export const discountOptions = () =&gt; [
  { label: &quot;할인액을 선택해주세요&quot;, value: -1 },
  ...
];</code></pre>
<h3 id="변경-후">변경 후</h3>
<pre><code class="language-ts">export const discountOptions = (t: TFunction) =&gt; [
  { label: t(&quot;할인액을 선택해주세요&quot;), value: -1 },
  ...
];</code></pre>
<p><code>t</code>를 매개변수로 받아 동적으로 번역하도록 수정한 것이다.</p>
<hr />
<h2 id="문제-발생">문제 발생</h2>
<p>함수 시그니처는 변경되었지만,<br />이를 사용하는 일부 컴포넌트에서는 <strong>기존 사용 방식이 그대로 남아 있었다.</strong></p>
<h3 id="기존-코드">기존 코드</h3>
<pre><code class="language-tsx">&lt;Select options={discountOptions} /&gt;</code></pre>
<h3 id="✅-변경-후-코드">✅ 변경 후 코드</h3>
<pre><code class="language-tsx">&lt;Select options={discountOptions(t)} /&gt;</code></pre>
<p>이로 인해 특정 화면에서 <strong>흰 화면이 발생하는 런타임 버그</strong>가 발생했다.</p>
<hr />
<h2 id="재발-가능성에-대한-우려">재발 가능성에 대한 우려</h2>
<p>이 문제를 수정하면서 다른 곳에도 같은 방식으로 수정되지 않은 코드가 남아 있지 않을까? 하는 생각이 들었다.
하지만 이런 사용처를 파일 하나하나 열어서 직접 확인하는 것은  비효율적이라고 생각했다.</p>
<p>그래서 <strong>코드를 자동으로 검사할 수 있는 방법</strong>을 찾아보았고,<br />대표적으로 다음 두 가지가 있다는 것을 알게 되었다.</p>
<ul>
<li><strong>ESLint</strong>: 코드 규칙, 패턴, 잠재적 문제를 검사</li>
<li><strong>TypeScript 타입 검사(typecheck)</strong>: 타입 불일치, 잘못된 값 전달을 검사</li>
</ul>
<p>먼저 ESLint를 사용해 검사를 진행해 보기로 했다.</p>
<hr />
<h2 id="eslint-검사-시도">ESLint 검사 시도</h2>
<pre><code class="language-json">{
  &quot;scripts&quot;: {
    &quot;lint&quot;: &quot;eslint .&quot;
  }
}</code></pre>
<pre><code class="language-bash">npm run lint</code></pre>
<hr />
<h2 id="eslint-결과">ESLint 결과</h2>
<p>실행 결과 다음과 같은 경고(warning)들이 출력되었다.</p>
<pre><code class="language-text">163:67  warning  Expected '===' and instead saw '=='  eqeqeq
181:9   warning  React Hook useCallback has missing dependencies  react-hooks/exhaustive-deps
...</code></pre>
<p>아마 기존 코드에서 작성된 문제로 보인다.
당장 기능에 치명적인 문제는 아니지만, 정리해야 될 부분으로 보인다.</p>
<hr />
<h2 id="eslint에서-error와-warning의-차이">ESLint에서 error와 warning의 차이</h2>
<p>ESLint에서 메시지는 크게 error와 warning으로 나뉜다.</p>
<h3 id="error">Error</h3>
<ul>
<li>반드시 수정해야 하는 문제</li>
<li>설정에 따라 빌드나 CI를 실패시킬 수 있음</li>
<li>대표적인 예:
  react-hooks/rules-of-hooks (React Hook 사용 규칙 위반)
  no-undef (정의되지 않은 변수 사용)
  no-unused-vars (사용하지 않는 변수)
  array-callback-return (map에서 return 누락)</li>
</ul>
<h3 id="warning">Warning</h3>
<ul>
<li>당장은 동작하지만 권장되지 않는 코드</li>
<li>잠재적인 버그 가능성 존재</li>
</ul>
<hr />
<h2 id="eslint의-한계">ESLint의 한계</h2>
<p>ESLint는 <strong>코딩 규칙/스타일</strong>을 검사한다. </p>
<p>여러 경고와 에러가 출력되었지만,
내가 찾고 있던 에러는 나오지 않았다.</p>
<p>내가 찾고 있던 문제는 다음과 같은 유형이었다.</p>
<p>매개변수가 필요한 함수인데, 매개변수를 전달하지 않고 사용한 경우</p>
<p>이 문제를 다시 생각해보니,
이는 ESLint가 아닌 TypeScript 타입 시스템이 잡아야 하는 문제였다.
실제로 발생하는 에러는 아래와 같은 타입 에러였다.</p>
<pre><code class="language-text">Type '(t: TFunction) =&gt; { label: string; value: number; }[]'
is not assignable to type 'OptionGroupType[]'</code></pre>
<hr />
<h2 id="typescript-타입-검사">TypeScript 타입 검사</h2>
<p>그래서 다음으로 TypeScript 타입 검사를 실행해 보았다.</p>
<pre><code class="language-json">{
  &quot;scripts&quot;: {
    &quot;typecheck&quot;: &quot;tsc --noEmit&quot;
  }
}</code></pre>
<pre><code class="language-bash">npm run typecheck</code></pre>
<ul>
<li><code>--noEmit</code> 옵션은 타입 검사만 수행하고
<code>.js</code> 또는 <code>.d.ts</code> 같은 결과 파일을 생성하지 않는다.</li>
<li>만약 <code>tsc .</code>처럼 실행하면 검사 결과물 파일이 생성될 수 있다.</li>
</ul>
<hr />
<h2 id="typecheck-결과">typecheck 결과</h2>
<p>타입 검사를 실행하자, 기존에 인지하지 못했던 타입 에러들이 다수 발견되었다.</p>
<pre><code class="language-text">src/pages/Rental/Components/ContractForm.tsx:441:41 - error TS2322:
Type '(t: TFunction) =&gt; { label: string; value: number; }[]'
is not assignable to type 'OptionGroupType[]'.</code></pre>
<p>그리고 <strong>처음에 찾고자 했던 문제의 원인도 정확히 출력되었다.</strong></p>
<pre><code class="language-text">src/pages/Rental/Components/ContractForm.tsx:441:41 - error TS2322:
Type '(t: TFunction) =&gt; { label: string; value: number; }[]'
is not assignable to type 'OptionGroupType[]'.

441   options={discountOptions}</code></pre>
<p>이를 통해 매개변수가 누락된 모든 사용처를 쉽게 찾아 수정할 수 있었다.</p>
<hr />
<h2 id="정리">정리</h2>
<ul>
<li>ESLint: 코드 규칙, 스타일, 잠재적 버그 패턴 검사</li>
<li>TypeScript: 타입 불일치, 매개변수 누락, 구조적 문제 검사</li>
</ul>
<hr />
<p>코드를 자동으로 검사할 수 있게 해주는 도구로는<br /><strong>ESLint</strong>와 <strong>TypeScript typecheck</strong>가 있다.</p>
<p>처음에는 ESLint로 문제를 찾을 수 있을 거라 생각했지만,<br />이번 이슈의 핵심은 코드 규칙이 아니라 <strong>타입 불일치</strong>였다.</p>
<ul>
<li>ESLint는 코드 스타일과 규칙, 잠재적인 실수를 미리 알려주고</li>
<li>TypeScript typecheck는 타입 기준으로 코드의 구조적인 문제를 검사해 준다</li>
</ul>
<p>TypeScript typecheck로 누락된 사용처를 쉽게 찾아낼 수 있었고,<br />런타임 문제를 사전에 예방할 수 있었다.</p>