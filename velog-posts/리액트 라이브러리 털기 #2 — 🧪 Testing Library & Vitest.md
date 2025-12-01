<p>이번 글에서는 리액트 프로젝트에서 자주 사용하는 <strong>Testing Library</strong>와  
테스트 러너 <strong>Vitest</strong>의 개념, 설치 방법, 그리고 실제 사용 시점을 알아보겠습니다.</p>
<p>UI 개발 과정에서 테스트 코드를 작성해야 하는 이유와,<br />Vitest와 Testing Library가 함께 어떤 역할을 수행하는지도 살펴보겠습니다.</p>
<hr />
<h2 id="왜-테스트-라이브러리를-써야-할까">왜 테스트 라이브러리를 써야 할까?</h2>
<p>UI가 겉보기에는 정상적으로 보이더라도, 내부 로직이 잘못 동작하고 있을 수 있습니다.</p>
<p>예를 들어:</p>
<ul>
<li>클릭 이벤트가 호출되지 않음  </li>
<li>상태 업데이트가 잘못됨  </li>
<li>조건부 UI가 예상과 다르게 표시됨  </li>
</ul>
<blockquote>
<p>테스트 코드는 이런 “눈에 보이지 않는 오류”를 잡아주는 <strong>자동화된 안전망</strong>입니다.</p>
</blockquote>
<hr />
<h2 id="🤖-자동-테스트의-필요성">🤖 자동 테스트의 필요성</h2>
<h3 id="1️⃣-수동-테스트는-단발성">1️⃣ 수동 테스트는 단발성</h3>
<ul>
<li>직접 눌러봐야 함 </li>
<li>기능이 많을수록 반복이 늘어남</li>
<li>사람이 실수할 여지가 많음</li>
</ul>
<h3 id="2️⃣-테스트-코드는-자동-확인-장치">2️⃣ 테스트 코드는 자동 확인 장치</h3>
<pre><code class="language-bash">npm run test</code></pre>
<p>한 번 작성하면 커밋/배포 전마다 자동 검증됨.</p>
<h3 id="3️⃣-코드-수정이-다른-기능을-깨뜨릴-수-있음">3️⃣ 코드 수정이 다른 기능을 깨뜨릴 수 있음</h3>
<p>UI는 같아 보이지만 내부 동작이 달라진 문제를 테스트는 찾아냄.</p>
<hr />
<h2 id="⚙️-설치-방법">⚙️ 설치 방법</h2>
<p>Testing Library와 Vitest는 함께 사용하는 경우가 많습니다.<br />테스트 환경을 구성하기 위해서는 다음 세 가지 구성요소가 필요합니다.</p>
<table>
<thead>
<tr>
<th>구성 요소</th>
<th>역할</th>
</tr>
</thead>
<tbody><tr>
<td><strong>Vitest</strong></td>
<td>테스트 러너 (테스트 코드를 실행하고 결과를 평가)</td>
</tr>
<tr>
<td><strong>jsdom</strong></td>
<td>브라우저 없이도 DOM 환경을 흉내 내는 가상 브라우저</td>
</tr>
<tr>
<td><strong>Testing Library</strong></td>
<td>사용자의 실제 행동을 시뮬레이션</td>
</tr>
</tbody></table>
<h3 id="설치-명령">설치 명령</h3>
<pre><code class="language-bash">npm install -D vitest jsdom @testing-library/react @testing-library/user-event</code></pre>
<hr />
<h2 id="🤔-무엇을-테스트해야-할까">🤔 무엇을 테스트해야 할까?</h2>
<p>테스트를 작성할 때 많이 하는 오해 중 하나는<br />&quot;컴포넌트의 모든 동작을 100% 테스트해야 한다&quot;는 생각입니다.<br />하지만 실제로는 다음 원칙이 훨씬 중요합니다.</p>
<hr />
<h3 id="✔-핵심-기능만-테스트하면-충분하다">✔ 핵심 기능만 테스트하면 충분하다</h3>
<ul>
<li>사용자에게 중요한 기능  </li>
<li>비즈니스 로직이 영향을 받는 부분  </li>
<li>오류가 나면 큰 문제가 되는 기능  </li>
<li>상태 변화가 중요한 핵심 시나리오  </li>
</ul>
<p>예를 들어 로그인 화면이라면:</p>
<ul>
<li><strong>아이디/비밀번호 입력 → 로그인 요청 호출됨</strong> → ✔ 필수 테스트  </li>
<li>버튼에 특정 CSS 클래스가 있는가? → ❌ 비핵심  </li>
<li>input blur 시 border 색이 바뀌는가? → ❌ 비핵심  </li>
</ul>
<p>불필요한 테스트는 유지보수 비용만 증가시키므로 지양해야 합니다.</p>
<h3 id="✔-모든-페이지와-모든-컴포넌트를-테스트할-필요는-없다">✔ 모든 페이지와 모든 컴포넌트를 테스트할 필요는 없다</h3>
<p>React 프로젝트라고 해서 “페이지 개수 = 테스트 파일 개수”일 필요는 없습니다.<br />중요한 점은 <strong>페이지 단위가 아니라 기능 단위로 테스트 대상을 결정</strong>하는 것입니다.</p>
<p>즉,</p>
<ul>
<li>로직이 많다고 해서 페이지 전체를 테스트해야 하는 것이 아니고  </li>
<li>공통 컴포넌트(Button, Input 등)도 <strong>단순 UI일 경우 테스트할 필요 없으며</strong>  </li>
<li>복잡한 로직이나 중요한 기능이 담긴 부분만 테스트하면 충분합니다.</li>
</ul>
<p>대부분의 비즈니스 로직은 페이지 안이 아니라<br /><strong>커스텀 훅(useXXX)이나 독립된 작은 컴포넌트</strong>에 들어있기 때문에<br />페이지 하나 전체를 테스트하는 대신,<br /><strong>핵심 로직이 있는 부분만 선택적으로 테스트</strong>하는 것이 훨씬 효율적입니다.</p>
<p>프로젝트 페이지가 20개여도 테스트 파일은 5~8개만 있을 수도 있고,<br />반대로 핵심 기능이 많다면 테스트가 늘어날 수도 있습니다.</p>
<hr />
<h1 id="테스트-도구-개념-정리">테스트 도구 개념 정리</h1>
<h2 id="테스트-러너vitest란">테스트 러너(Vitest)란?</h2>
<p>테스트 러너(Test Runner) 는 테스트 코드를 실행하고 결과를 알려주는 도구입니다.</p>
<ul>
<li>테스트 파일을 자동으로 찾고 실행  </li>
<li><code>test</code>, <code>expect</code> 같은 기본 테스트 문법 해석</li>
<li>통과/실패 여부 리포트  </li>
<li>테스트 환경(jsdom 등)과 연동 </li>
</ul>
<p>즉, <strong>테스트를 실제로 실행하는 엔진</strong>입니다.
Vitest는 Vite 기반이라 실행 속도가 빠르고 개발 환경과 빠르게 맞물립니다.</p>
<hr />
<h2 id="🌐-jsdom이란">🌐 jsdom이란?</h2>
<p>jsdom은 브라우저 없이 DOM을 사용할 수 있게 해주는 가상 브라우저 환경입니다.</p>
<ul>
<li><code>document</code>, <code>window</code>, <code>button</code>, <code>input</code> 같은 DOM API 사용 가능</li>
<li>React 컴포넌트를 브라우저 없이 렌더링 가능  </li>
<li>클릭/입력 등 사용자 이벤트를 테스트 환경에서 그대로 재현  </li>
</ul>
<p>즉, <strong>테스트가 브라우저처럼 동작하도록 만들어주는 가짜 DOM 환경</strong>입니다.
테스트 외에는 사용할 일이 거의 없습니다.</p>
<hr />
<h2 id="🧪-testing-library란">🧪 Testing Library란?</h2>
<p>Testing Library는 <strong>UI 테스트를 사용자 관점으로 진행하는 도구 모음</strong>입니다.</p>
<p>주로 사용하는 것은 다음 패키지입니다:</p>
<pre><code>@testing-library/react</code></pre><p>Testing Library는 “사용자가 실제로 보는 기준”으로 테스트하는 것을 권장합니다.</p>
<hr />
<h3 id="testing-library-핵심-철학">Testing Library 핵심 철학</h3>
<blockquote>
<p><strong>“구현 세부가 아니라, 사용자 관점에서 테스트하라.”</strong></p>
</blockquote>
<p>예:</p>
<pre><code class="language-tsx">screen.getByRole(&quot;button&quot;, { name: &quot;로그인&quot; });</code></pre>
<p>이 코드는 다음을 의미합니다:</p>
<ul>
<li>사용자 눈에 버튼이 보여야 한다  </li>
<li>버튼의 접근성 role이 <code>button</code>이어야 한다  </li>
<li>버튼 텍스트가 &quot;로그인&quot;이어야 한다  </li>
</ul>
<hr />
<h2 id="📚-vitest-테스트-문법-정리">📚 Vitest 테스트 문법 정리</h2>
<h3 id="✔-describe--테스트-그룹">✔ describe — 테스트 그룹</h3>
<p><code>describe</code>는 <strong>관련된 테스트들을 하나의 묶음(그룹)</strong> 으로 관리하는 블록입니다.</p>
<pre><code class="language-ts">describe(&quot;로그인 기능&quot;, () =&gt; { ... })</code></pre>
<p><strong>언제 필요할까?</strong></p>
<ul>
<li>기능별 / 컴포넌트별로 테스트를 그룹화할 때</li>
<li>테스트 결과 리포트가 더 읽기 쉬워짐</li>
<li>반복되는 초기화 작업을 beforeEach 등에 묶어 사용하기 좋음</li>
</ul>
<p><strong>예:</strong>
로그인 관련 테스트 3개, 회원가입 테스트 2개 식으로 묶으면 리포트가 훨씬 깔끔하게 정리됨.</p>
<h3 id="✔-test--it--개별-테스트-정의">✔ test / it — 개별 테스트 정의</h3>
<p><code>test()</code> 또는 <code>it()</code> 은 <strong>하나의 동작을 검증하는 단위 테스트</strong>를 정의합니다.</p>
<pre><code class="language-ts">test(&quot;버튼 클릭 시 로그인 호출됨&quot;, () =&gt; {})</code></pre>
<p>두 함수는 완전히 같은 기능이며, 취향/팀 컨벤션에 따라 선택하면 됩니다.</p>
<p><strong>언제 필요할까?</strong></p>
<ul>
<li>특정 동작을 기대한 대로 수행하는지 테스트하고 싶을 때</li>
<li>하나의 test는 하나의 행동(기능) 을 검증해야 가장 좋은 테스트 구조가 됨</li>
</ul>
<p><strong>예:</strong></p>
<ul>
<li>&quot;버튼이 렌더링된다&quot;</li>
<li>&quot;버튼 클릭 시 이벤트가 발생한다&quot;</li>
<li>&quot;에러 메시지가 화면에 표시된다&quot;</li>
<li>각각을 별도 test로 분리하는 것이 좋음.</li>
</ul>
<h3 id="✔-expect--결과-검증">✔ expect — 결과 검증</h3>
<p><code>expect()</code>는 테스트의 <strong>결과를 검증하는 핵심 함수</strong>입니다.
테스트가 통과하려면 expect 조건이 모두 true여야 합니다.</p>
<pre><code class="language-ts">expect(value).toBe(10)                 // 값 비교
expect(fn).toHaveBeenCalled()          // 함수 호출 여부
expect(element).toBeInTheDocument()    // DOM 존재 여부</code></pre>
<p><strong>자주 쓰는 매처(example matcher):</strong></p>
<ul>
<li><code>.toBe()</code> → 값이 정확히 같은지</li>
<li><code>.toEqual()</code> → 객체/배열 비교</li>
<li><code>.toHaveBeenCalled()</code> → 함수가 호출되었는지</li>
<li><code>.toHaveBeenCalledWith()</code> → 특정 파라미터로 호출되었는지</li>
<li><code>.toBeInTheDocument()</code> → DOM 요소 존재 여부 (Testing Library matcher)</li>
</ul>
<h3 id="✔-vifn--mock-함수">✔ vi.fn — Mock 함수</h3>
<p><code>vi.fn()</code>은 테스트에서 <strong>가짜 함수(Mock)</strong> 를 만들어주는 도구입니다.</p>
<pre><code class="language-ts">const onLogin = vi.fn()

// 컴포넌트 실행
await userEvent.click(screen.getByRole(&quot;button&quot;))

// onLogin이 호출됐는지 검증
expect(onLogin).toHaveBeenCalled()
expect(onLogin).toHaveBeenCalledWith({ id: &quot;test&quot;, pw: &quot;1234&quot; })</code></pre>
<p><strong>언제 필요할까?</strong></p>
<ul>
<li>컴포넌트가 외부 함수(onClick, API 호출 등)를 호출하는지 확인할 때</li>
<li>실제 함수를 실행하고 싶지 않을 때 (API 요청, 네트워크 등)</li>
<li>함수를 몇 번 호출했는지, 어떤 값으로 호출했는지 검증할 때</li>
</ul>
<p>즉, <strong>Mock 함수는 컴포넌트의 동작을 관찰하는 카메라</strong> 같은 역할을 합니다.</p>
<hr />
<h2 id="📚-testing-library-문법-정리">📚 Testing Library 문법 정리</h2>
<p>Testing Library에서 가장 많이 사용하는 기능들을 정리하면 다음과 같습니다.</p>
<h3 id="✔-render--컴포넌트-렌더링">✔ render — 컴포넌트 렌더링</h3>
<pre><code class="language-tsx">render(&lt;MyButton /&gt;);
expect(screen.getByRole(&quot;button&quot;)).toBeInTheDocument();</code></pre>
<h3 id="✔-screen--렌더링된-화면-탐색">✔ screen — 렌더링된 화면 탐색</h3>
<pre><code class="language-tsx">screen.getByRole(&quot;button&quot;, { name: &quot;저장&quot; });
screen.getByLabelText(&quot;비밀번호&quot;);</code></pre>
<h3 id="✔-userevent--사용자-행동-시뮬레이션">✔ userEvent — 사용자 행동 시뮬레이션</h3>
<pre><code class="language-tsx">await userEvent.type(input, &quot;test&quot;)
await userEvent.click(button)</code></pre>
<hr />
<h2 id="📁-기본-파일-구조">📁 기본 파일 구조</h2>
<pre><code>src/
├─ components/
│  ├─ Button.tsx
│  └─ __tests__/Button.test.tsx
└─ App.tsx</code></pre><hr />
<h2 id="⚙️-vitest-설정">⚙️ Vitest 설정</h2>
<p>vitest.config.ts</p>
<pre><code class="language-ts">import { defineConfig } from &quot;vitest/config&quot;;

export default defineConfig({
  test: {
    environment: &quot;jsdom&quot;,
    globals: true,
    setupFiles: &quot;./src/setupTests.ts&quot;,
  },
});</code></pre>
<hr />
<h2 id="🛠-실습-로그인-폼-테스트-만들기">🛠 실습: 로그인 폼 테스트 만들기</h2>
<h3 id="1-로그인-컴포넌트-생성">1. 로그인 컴포넌트 생성</h3>
<p><code>src/LoginForm.tsx</code></p>
<pre><code class="language-tsx">import { useState } from &quot;react&quot;;

export default function LoginForm({ onLogin }) {
  const [id, setId] = useState(&quot;&quot;);
  const [pw, setPw] = useState(&quot;&quot;);

  const handleSubmit = () =&gt; {
    onLogin({ id, pw });
  };

  return (
    &lt;div&gt;
      &lt;label&gt;
        아이디
        &lt;input value={id} onChange={(e) =&gt; setId(e.target.value)} /&gt;
      &lt;/label&gt;

      &lt;label&gt;
        비밀번호
        &lt;input value={pw} onChange={(e) =&gt; setPw(e.target.value)} /&gt;
      &lt;/label&gt;

      &lt;button onClick={handleSubmit}&gt;로그인&lt;/button&gt;
    &lt;/div&gt;
  );
}</code></pre>
<hr />
<h3 id="2-테스트-파일-생성-및-코드-작성">2. 테스트 파일 생성 및 코드 작성</h3>
<p><code>src/__tests__/LoginForm.test.tsx</code></p>
<pre><code class="language-tsx">// --- Vitest 문법 ---
import { describe, test, expect, vi } from &quot;vitest&quot;;
// --- Testing Library 문법 ---
import { render, screen } from &quot;@testing-library/react&quot;;
import userEvent from &quot;@testing-library/user-event&quot;;
import LoginForm from &quot;../LoginForm&quot;;

// --- Vitest 문법 ---
describe(&quot;LoginForm&quot;, () =&gt; {
  test(&quot;아이디/비밀번호 입력 후 로그인 클릭 시 onLogin 호출됨&quot;, async () =&gt; {
    const onLogin = vi.fn();

    // --- Testing Library 문법 (컴포넌트 렌더링) ---
    render(&lt;LoginForm onLogin={onLogin} /&gt;);

    // --- Testing Library + user-event 문법 (사용자 입력 시뮬레이션) ---
    await userEvent.type(screen.getByLabelText(&quot;아이디&quot;), &quot;sunmin&quot;);
    await userEvent.type(screen.getByLabelText(&quot;비밀번호&quot;), &quot;1234&quot;);
    // --- Testing Library 문법 (버튼 클릭) ---
    await userEvent.click(screen.getByRole(&quot;button&quot;, { name: &quot;로그인&quot; }));

     // --- Vitest 문법 (검증/단언) ---
    expect(onLogin).toHaveBeenCalledWith({
      id: &quot;sunmin&quot;,
      pw: &quot;1234&quot;,
    });
  });
});</code></pre>
<h3 id="⭐-vitest-vs-testing-library-역할-정리">⭐ Vitest vs Testing Library 역할 정리</h3>
<table>
<thead>
<tr>
<th>구분</th>
<th>역할</th>
<th>테스트에서 하는 일</th>
</tr>
</thead>
<tbody><tr>
<td><strong>Vitest</strong></td>
<td>&quot;심판&quot; 역할</td>
<td>테스트를 시작하고(<code>test</code>), 결과를 판단하고(<code>expect</code>), 기록함</td>
</tr>
<tr>
<td><strong>Testing Library</strong></td>
<td>&quot;플레이어&quot; 역할</td>
<td>화면에 컴포넌트를 보여주고(<code>render</code>), 버튼 클릭/입력 같은 행동을 대신 해줌</td>
</tr>
</tbody></table>
<h3 id="❗-왜-둘-다-필요할까">❗ 왜 둘 다 필요할까?</h3>
<ul>
<li>✔ <strong>Vitest만으로는 컴포넌트를 렌더링할 수 없습니다.</strong></li>
<li>✔ <strong>Testing Library만으로는 테스트를 정의하거나 검증할 수 없습니다.</strong></li>
</ul>
<p>따라서 <strong>UI 테스트에서는 Vitest + Testing Library를 함께 섞어서</strong> 사용합니다.</p>
<hr />
<h3 id="3-테스트-실행">3. 테스트 실행</h3>
<h3 id="vitest-실행">Vitest 실행</h3>
<pre><code class="language-bash">npm run test</code></pre>
<p>또는</p>
<pre><code class="language-bash">npx vitest</code></pre>
<h3 id="실행-결과-예시">실행 결과 예시</h3>
<pre><code> PASS  src/__tests__/LoginForm.test.tsx
  LoginForm
    ✓ 아이디/비밀번호 입력 후 로그인 클릭 시 onLogin 호출됨 (95 ms)

Test Files  1 passed (1)
      Tests  1 passed (1)
   Start at  12:31:00
   Duration  0.50s</code></pre><p>🟢 초록색 PASS가 뜨면 테스트 성공!  
🔴 FAIL이면 이유가 출력됨.</p>
<hr />
<h2 id="💡-정리">💡 정리</h2>
<ul>
<li><strong>Vitest</strong> → 테스트를 “실행하는 엔진”  </li>
<li><strong>Testing Library</strong> → UI를 “사용자처럼 조작·검증”하는 도구 </li>
<li><strong>jsdom</strong> → 브라우저 없이 DOM을 제공하는 “가상 브라우저”</li>
</ul>
<p>세 가지를 결합하면 React UI를 안정적으로 테스트할 수 있습니다.</p>