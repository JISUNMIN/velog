<p>React Hook Form은 많은 프로젝트에서 사용되고 있는 라이브러리입니다.<br />저도 프로젝트에서 폼 관리를 할 때, 각 컴포넌트에 React Hook Form을 붙일 수 있도록 구조를 만들어 사용했었습니다. </p>
<p>처음에는 어려운데 이걸 왜 쓰지? 라고 생각했지만, 직접 사용해 보니 신세계 였습니다. (useState 지옥에서 빠져나오게 해주는..)
그래서 React Hook Form을 알아보기 전에, 어떤 이점이 있어서 자주 사용되는지 먼저 살펴보겠습니다.</p>
<hr />
<h2 id="1-react-hook-form을-왜-쓸까">1. React Hook Form을 왜 쓸까?</h2>
<h3 id="1-성능이-좋다">1) 성능이 좋다</h3>
<ul>
<li><strong>Uncontrolled Component 기반</strong><ul>
<li>기본은 Uncontrolled Component</li>
<li>필요한 경우 <code>Controller</code>로 Controlled Component도 지원</li>
</ul>
</li>
<li>input 값 변경 시 전체 폼 리렌더링 하지 않음</li>
<li>필요한 필드만 리렌더링 </li>
</ul>
<p>대규모 폼, 검색 조건이 많은 화면에서 <strong>체감 성능 차이 큼</strong></p>
<hr />
<h4 id="uncontrolled-component">Uncontrolled Component</h4>
<ul>
<li>입력값의 <strong>source of truth는 DOM</strong></li>
<li><code>ref</code>를 통해 필요할 때만 접근</li>
<li>값 변경 시 React 리렌더링 없음</li>
<li>성능에 유리 (대규모 폼에 적합)</li>
</ul>
<pre><code class="language-tsx">&lt;input ref={inputRef} defaultValue=&quot;abc&quot; /&gt;</code></pre>
<ul>
<li><code>defaultValue</code> 사용</li>
<li>DOM이 처음 렌더링될 때만 값 세팅</li>
<li>이후 값 변경은 DOM 내부에서만 관리</li>
<li>React는 값 변경에 관여하지 않음</li>
</ul>
<hr />
<h4 id="controlled-component">Controlled Component</h4>
<ul>
<li>입력값의 <strong>source of truth는 React state</strong></li>
<li><code>useState</code>로 값 직접 관리</li>
<li>값 변경 → <code>setState</code> → 리렌더링 발생</li>
<li>로직 제어는 쉽지만 성능 부담 가능</li>
</ul>
<pre><code class="language-tsx">const [value, setValue] = useState(&quot;&quot;);

&lt;input
  value={value}
  onChange={(e) =&gt; setValue(e.target.value)}
/&gt;</code></pre>
<ul>
<li><code>value</code> 사용</li>
<li>input 값은 항상 state와 동기화</li>
<li>타이핑 시 React state가 변경되어야 화면도 변경됨</li>
</ul>
<p>잘못된 조합 ❌</p>
<ul>
<li><code>ref + value</code></li>
<li><code>useState + defaultValue</code></li>
</ul>
<hr />
<h3 id="2-코드가-단순하고-보일러플레이트가-적다">2) 코드가 단순하고 보일러플레이트가 적다</h3>
<blockquote>
<p><strong>보일러플레이트(Boilerplate)</strong><br />매번 비슷한 형태로 반복해서 작성해야 하는 코드를 의미</p>
</blockquote>
<pre><code class="language-tsx">const { register, handleSubmit } = useForm();

&lt;input {...register(&quot;email&quot;)} /&gt;</code></pre>
<ul>
<li><code>value / onChange</code> 직접 관리 불필요</li>
<li>반복적인 <code>useState</code> 선언에서 해방</li>
</ul>
<pre><code class="language-tsx">// useState 반복 예시
const [emailInput, setEmailInput] = useState();
const [passwordInput, setPasswordInput] = useState();
const [nameInput, setNameInput] = useState();</code></pre>
<hr />
<h3 id="3-유효성-검사validation가-강력하다">3) 유효성 검사(Validation)가 강력하다</h3>
<pre><code class="language-tsx">&lt;input
  {...register(&quot;email&quot;, {
    required: &quot;필수 값입니다&quot;,
    pattern: {
      value: /\S+@\S+\.\S+/,
      message: &quot;이메일 형식이 아닙니다&quot;,
    },
  })}
/&gt;</code></pre>
<ul>
<li>Yup / Zod 같은 스키마 검증 라이브러리와 궁합이 좋음</li>
<li><strong>비즈니스 로직과 UI 분리에 유리</strong></li>
</ul>
<hr />
<h3 id="4-기존-ui-라이브러리와-잘-연동됨">4) 기존 UI 라이브러리와 잘 연동됨</h3>
<ul>
<li>MUI, 사내 커스텀 Input 등과 잘 연동</li>
<li><code>Controller</code>를 사용해 Controlled Component도 문제없이 사용 가능</li>
</ul>
<pre><code class="language-tsx">&lt;Controller
  name=&quot;date&quot;
  control={control}
  render={({ field }) =&gt; &lt;DatePicker {...field} /&gt;}
/&gt;</code></pre>
<hr />
<h3 id="5-form-상태-관리가-체계적">5) Form 상태 관리가 체계적</h3>
<ul>
<li><code>dirty</code>, <code>touched</code>, <code>isValid</code>, <code>isSubmitting</code> 등 기본 제공</li>
<li>검색폼 / 입력폼 / 수정폼 공통 패턴 구성에 유리</li>
</ul>
<hr />
<h3 id="6-생태계--채택-현황">6) 생태계 &amp; 채택 현황</h3>
<ul>
<li>React 공식 문서 및 커뮤니티에서 적극 추천</li>
<li>대기업 및 스타트업 다수 사용<ul>
<li>Vercel</li>
<li>Netflix 등</li>
</ul>
</li>
</ul>
<hr />
<h2 id="2-점유율-사용량-지표">2. 점유율 (사용량 지표)</h2>
<ul>
<li><strong>주간 약 1,488만 번 다운로드</strong></li>
<li>npm 기준 Form 라이브러리 중 압도적 1위</li>
<li>주간 변동은 있으나 장기적으로는 우상향 추세</li>
</ul>
<p><img alt="react-hook-form downloads" src="https://velog.velcdn.com/images/sunmins/post/2fba9c2b-7764-472f-9020-c7eea1d1eb27/image.png" /></p>
<hr />
<h2 id="📝-정리">📝 정리</h2>
<p>이렇게 React Hook Form은 성능이 뛰어나고 사용하기 편리하며,<br />높은 사용량(점유율)을 바탕으로 많은 프로젝트에서 선택되고 있는 라이브러리입니다.<br />또한 보일러플레이트 코드가 적어 폼 관리 시 생산성을 높일 수 있다는 점도 큰 장점입니다.</p>
<p>다만 처음에는 개념이 낯설어 러닝 커브가 느껴질 수 있습니다.<br />그래서 이제 본격적으로 React Hook Form을 파보려고 합니다.<br />다음 글에서는 React Hook Form의 기본적인 사용법부터 시작해보겠습니다.</p>