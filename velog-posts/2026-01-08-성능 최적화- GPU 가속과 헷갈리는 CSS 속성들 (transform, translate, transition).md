<p>프론트엔드 개발을 하다 보면<br />렌더링 이후 애니메이션 효과나 크기 변화를 주어야 하는 경우가 자주 발생합니다.</p>
<p>이때 어떤 CSS 속성을 사용하느냐에 따라<br />CPU에 큰 부담을 줄 수도 있고,<br />GPU를 활용해 훨씬 부드러운 애니메이션을 만들 수도 있습니다.</p>
<p>이 글에서는<br />브라우저 렌더링 과정과 함께<br />성능 최적화 관점에서 자주 헷갈리는 CSS 속성들을 정리해봤습니다.</p>
<hr />
<h2 id="브라우저-렌더링-과정-요약">브라우저 렌더링 과정 요약</h2>
<p>브라우저 렌더링 과정을 간단히 설명하면 다음과 같습니다.</p>
<ol>
<li>HTML 파싱 → <strong>DOM 생성</strong></li>
<li>CSS 파싱 → <strong>CSSOM 생성</strong></li>
<li>DOM + CSSOM → <strong>Render Tree 생성</strong></li>
<li><strong>Layout (Reflow)</strong><br />각 요소가 화면에서 차지할 위치와 크기 계산</li>
<li><strong>Paint</strong><br />색상, 텍스트, 그림자 등 실제 픽셀을 그림</li>
<li><strong>Composite</strong><br />레이어를 합성하여 화면에 출력</li>
</ol>
<p>Render Tree
→ Layout
→ Paint
→ Composite
→ Rendering</p>
<hr />
<h2 id="reflow와-paint">Reflow와 Paint</h2>
<p>이 과정에서 자주 등장하는 용어가 <strong>Reflow(Layout)</strong>와 <strong>Paint</strong></p>
<ul>
<li><p><strong>Reflow(Layout)</strong><br />요소의 크기나 위치가 변경될 때 다시 계산되는 단계<br />→ CPU 사용량이 큼</p>
</li>
<li><p><strong>Paint</strong><br />색상, 텍스트, 테두리 등을 다시 그리는 단계<br />→ 역시 CPU 부담이 있음</p>
</li>
</ul>
<p>이 과정이 반복되면 CPU 부담이 커지고,<br />애니메이션이 끊겨 보일 수 있습니다.</p>
<p>자세한 설명은<br /><a href="https://velog.io/@sunmins/%EC%9B%B9-%EA%B0%9C%EB%B0%9C-%EC%8A%A4%ED%82%AC%EC%9D%84-%ED%95%9C-%EB%8B%A8%EA%B3%84-%EB%86%92%EC%97%AC%EC%A3%BC%EB%8A%94-%ED%94%84%EB%A1%A0%ED%8A%B8%EC%97%94%EB%93%9C-%EC%84%B1%EB%8A%A5-%EC%B5%9C%EC%A0%81%ED%99%94-%EA%B0%80%EC%9D%B4%EB%93%9C-poxhygb3">해당 글</a> 참고 바랍니다.</p>
<hr />
<h2 id="gpu-가속을-사용하는-css-속성">GPU 가속을 사용하는 CSS 속성</h2>
<p>렌더링 이후 애니메이션이나 상태 변화가 발생하면<br />브라우저는 기본적으로 다시 <strong>Layout → Paint → Composite</strong> 과정을 거칩니다.</p>
<p>하지만 일부 CSS 속성은<br />Layout과 Paint 단계를 건너뛰고<br /><strong>Composite 단계만 다시 수행</strong>하게 만들 수 있습니다.</p>
<p>이때 화면의 이동·합성 작업을<br />CPU가 아닌 <strong>GPU에서 처리하게 되는데</strong>,  
이러한 방식을 <strong>GPU 가속</strong>이라고 부릅니다.</p>
<p>GPU 가속이란, 다시 계산하고 다시 그리는 작업을 CPU 대신 GPU에게 맡겨  렌더링 성능을 최적화하고 화면을 더 부드럽게 만드는 방법입니다.</p>
<p>GPU는 이미 그려진 화면을 이동하거나 합성하는 작업을<br />CPU보다 훨씬 빠르게 처리할 수 있기 때문입니다.(Composite 단계가 CPU보다 압도적으로 빠름)</p>
<p>대표적인 GPU 가속 CSS 속성으로는<br /><strong><code>transform</code>과 <code>opacity</code></strong>가 있습니다.</p>
<hr />
<h2 id="1-transform">1. transform</h2>
<p><strong>의미:</strong> 변환하다, 바꾸다<br />요소의 <strong>모양이나 위치를 시각적으로 변경</strong>하는 속성</p>
<h3 id="transform으로-할-수-있는-것들">transform으로 할 수 있는 것들</h3>
<ul>
<li>이동: <code>translate</code></li>
<li>크기: <code>scale</code></li>
<li>회전: <code>rotate</code></li>
<li>기울기: <code>skew</code></li>
</ul>
<p>구조적으로 보면 다음과 같다.</p>
<p>transform
├─ translate
│ ├─ translateY: Y축으로 이동
│ └─ translateX: X축으로 이동
├─ scale
├─ rotate
└─ skew</p>
<pre><code class="language-css">
### 예시

```css
transform: translateY(10px) scale(1.1);</code></pre>
<ul>
<li>Y축으로 10px 이동</li>
<li>1.1배 확대</li>
<li>여러속성을 동시에 사용 가능</li>
</ul>
<p>transform 속성은 Layout -&gt; Paint -&gt; Composite 단계에서
Layout,Paint를 생략하고 Composite 단계만 재수행 하게됨.</p>
<hr />
<h3 id="transition이란-transform과의-차이">transition이란? (transform과의 차이)</h3>
<h4 id="transition의-의미">transition의 의미</h4>
<p><strong>전환, 변화 과정</strong></p>
<p>transition은 애니메이션 그 자체가 아니라<br /><strong>상태가 바뀔 때 그 변화 과정을 부드럽게 만들어주는 규칙</strong></p>
<p>속성의 변화를 감시한다고 해서<br /><strong>속성 감지자</strong>라고 생각하면 이해하기 쉽습니다.</p>
<hr />
<h4 id="문법">문법</h4>
<pre><code class="language-css">transition: A 0.3s, B 0.3s;</code></pre>
<p>위 코드는 아래와 같은 의미</p>
<pre><code class="language-css">/* transform과 opacity 이 두 속성만 감시 */
transition-property: transform, opacity;

/* 지속 시간 */
transition-duration: 0.3s, 0.3s;

/* 속도 곡선 */
transition-timing-function: ease, ease;
</code></pre>
<h4 id="속도-유형-timing-function">속도 유형 (timing-function)</h4>
<ul>
<li>linear
일정한 속도 (기계적인 느낌)</li>
<li>ease (default)
자연스러운 가속과 감속</li>
<li>ease-in
시작이 느림</li>
<li>ease-out
끝이 느림</li>
<li>ease-in-out
시작과 끝이 모두 느림</li>
</ul>
<h4 id="예시">예시</h4>
<pre><code class="language-css">이 요소에서 transform 값에 변화가 생기면
0.35초 동안,
**끝이 부드럽게 멈추는 방식(ease-out)**으로 변화시켜라.

.box {
  transform: translateY(10px);
  transition: transform 0.35s ease-out;
}

.box:hover {
  transform: translateY(0);
}</code></pre>
<hr />
<h2 id="2-opacity">2. opacity</h2>
<pre><code class="language-css">opacity: 0;
opacity: 1;</code></pre>
<ul>
<li>0 → 완전히 투명 (안 보임)</li>
<li>1 → 완전히 보임</li>
</ul>
<p>이미 그려진 걸 “얼마나 투명하게 보여줄지”만 바꿈
Composite 단계만 다시 수행</p>
<h3 id="❗-주의할점">❗ 주의할점</h3>
<p>opacity는 보이기만 안보이게 할뿐입니다.
그래서 클릭이 가능하고, 포커스가 되며 DOM에 존재합니다.</p>
<p>그래서 보통 이렇게 같이 사용합니다.</p>
<pre><code class="language-css">opacity: 0;
pointer-events: none;</code></pre>
<hr />
<h2 id="정리">정리</h2>
<p><img alt="" src="https://velog.velcdn.com/images/sunmins/post/8555b22a-00cb-4c6d-a0f9-d6da3ee82408/image.png" /></p>
<p>transform → 요소의 위치·크기·회전 등의 ‘상태(결과)’를 정의하는 속성
translate → transform 안에 있는 축 이동 함수
transition → 상태(결과)가 바뀔 때, 그 변화 과정을 애니메이션처럼 만들어주는 규칙
opacity: 투명도를 조절하는 속성</p>
<h2 id="transform과-cpu-사용-css-속성-비교">transform과 CPU 사용 CSS 속성 비교</h2>
<table>
<thead>
<tr>
<th>하고 싶은 것</th>
<th>❌ Bad (CPU 부담)</th>
<th>✅ Good (GPU 가속)</th>
</tr>
</thead>
<tbody><tr>
<td>이동</td>
<td><code>top / left</code> (좌표 자체 변경)</td>
<td><code>transform: translate</code></td>
</tr>
<tr>
<td>크기 변경</td>
<td><code>width / height</code> (박스 크기 변경)</td>
<td><code>transform: scale</code></td>
</tr>
<tr>
<td>숨김/표시</td>
<td><code>display / visibility</code></td>
<td><code>opacity</code></td>
</tr>
<tr>
<td>접기/펼치기</td>
<td><code>height</code></td>
<td><code>scaleY</code></td>
</tr>
</tbody></table>
<hr />
<h2 id="예시-비교">예시 비교</h2>
<h3 id="❌-bad-reflow-발생">❌ Bad (Reflow 발생)</h3>
<pre><code class="language-css">.box {
  width: 0;
  transition: width 0.3s;
}

.box.open {
  width: 200px;
}</code></pre>
<ul>
<li>Layout 단계부터 다시 실행</li>
<li>CPU 부담 큼</li>
</ul>
<h3 id="✅-good-gpu-가속">✅ Good (GPU 가속)</h3>
<pre><code class="language-css">.box {
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s;
}

.box.open {
  transform: scaleX(1);
}</code></pre>
<ul>
<li>Layout / Paint 없이 Composite만 수행</li>
<li>부드러운 애니메이션</li>
</ul>
<hr />
<h2 id="마무리">마무리</h2>
<p>이번 글에서는 <strong>GPU 가속</strong>의 개념과 그 필요성에 대해 정리해 보았습니다.
GPU 가속은 화면을 다시 계산하고 그리는 작업을 CPU 대신 GPU에게 맡겨  렌더링 성능을 향상시키는 방식입니다.</p>
<p>또한 헷갈리기 쉬운 <strong>transform, translate, transition</strong>의 차이점을 구분하며<br />각 속성이 어떤 역할을 하는지 살펴보았습니다.</p>
<p>마지막으로 <strong>transform과 opacity</strong>처럼 GPU 가속이 가능한 CSS 속성과<br /><code>width</code>, <code>display</code> 등 CPU 부담이 큰 속성을 비교해 았습니다.</p>
<p>이처럼 CSS 속성 선택은 단순한 스타일링을 넘어<br /><strong>렌더링 성능과 사용자 경험에 직접적인 영향을 줄 수 있습니다.</strong></p>