<p>이번 글에서는 
비동기를 공부하면서 <strong>가장 헷갈렸던 실행 흐름</strong>을  
예시 중심으로 정리해보겠습니다.</p>
<ul>
<li><strong>Promise는 왜 동기 코드보다 늦게 실행될까?</strong>  </li>
<li><strong>await은 왜 동기처럼 순차적으로 보일까?</strong></li>
<li><strong>둘의 실행 순서가 같을 때 / 달라질 때는 언제일까?</strong></li>
</ul>
<p>Promise 기반 비동기와 async/await의 실행 차이를<br />실제 코드 예시로 하나씩 풀어보겠습니다.</p>
<hr />
<h2 id="1️⃣-promise-기반-비동기--예약하고-동기-먼저-실행">1️⃣ Promise 기반 비동기 — “예약하고 동기 먼저 실행”</h2>
<p>Promise는 비동기 작업을 <strong>즉시 실행하는 것이 아니라</strong>,  
“작업이 끝나면 나중에 실행될 콜백을 예약”해두는 방식입니다.</p>
<h3 id="예시">예시</h3>
<pre><code class="language-js">getUser().then(user =&gt; {
  console.log(&quot;user:&quot;, user);
});

console.log(&quot;동기 코드&quot;);</code></pre>
<h3 id="실행-순서">실행 순서</h3>
<pre><code>동기 코드
user: {...}   ← 나중(Microtask) 실행</code></pre><h3 id="왜-이렇게-될까">왜 이렇게 될까?</h3>
<ul>
<li><code>getUser()</code>는 <strong>Promise를 반환하고 예약만 함</strong></li>
<li><code>then()</code> 콜백은 <strong>Microtask Queue에 등록</strong></li>
<li>JS 엔진은 <strong>동기 코드(<code>console.log</code>)를 먼저 실행</strong></li>
<li>이후 스택이 비면 이벤트 루프가 then 콜백을 실행함</li>
</ul>
<blockquote>
<p>Promise는 “비동기 등록만 하고, 동기 코드를 먼저 실행하는 방식”이다.</p>
</blockquote>
<hr />
<h2 id="2️⃣-asyncawait--비동기인데-순차적으로-보이는-코드">2️⃣ async/await — 비동기인데 순차적으로 보이는 코드</h2>
<p>같은 로직을 async/await으로 바꾸어 보겠습니다.</p>
<pre><code class="language-js">async function run() {
  const user = await getUser();  // 5초 걸린다고 가정
  console.log(&quot;user:&quot;, user);
}

run();
console.log(&quot;동기 코드&quot;);</code></pre>
<h3 id="실행-순서-1">실행 순서</h3>
<pre><code>동기 코드
user: {...}   ← getUser() 끝난 뒤 실행</code></pre><h3 id="왜-이렇게-될까-1">왜 이렇게 될까?</h3>
<ul>
<li><code>await</code>은 비동기지만 “해당 함수 내부 흐름만” 잠시 끊어놓는다</li>
<li>하지만 JS 엔진은 실제로 멈추지 않음</li>
<li>단지, await 아래의 코드만 나중에 재개됨</li>
</ul>
<p>즉, UI 렌더링·클릭 이벤트·타이머 등은 정상 동작합니다.</p>
<blockquote>
<p>await은 비동기지만, 그 async 함수 내부의 아래 코드는<br />앞 await이 끝날 때까지 실행되지 않아<br /><strong>동기처럼 순차적으로 보인다.</strong></p>
</blockquote>
<hr />
<h2 id="3️⃣-promise-vs-await-실행-흐름-비교">3️⃣ Promise vs await 실행 흐름 비교</h2>
<p>아래 두 코드는 결과는 같지만, 
<strong>내부 동작 방식(콜백 예약 방식 vs 함수 흐름 일시 중단 방식)</strong>이 다릅니다.</p>
<h3 id="🔵-promise-기반-콜백-예약-방식">🔵 Promise 기반 (콜백 예약 방식)</h3>
<pre><code class="language-js">getUser().then(user =&gt; {
  console.log(&quot;user:&quot;, user);
});

console.log(&quot;동기 코드&quot;);</code></pre>
<p><strong>실행 순서</strong></p>
<pre><code>동기 코드
user: ...</code></pre><hr />
<h3 id="🟢-await-기반-함수-흐름-일시-중단-방식">🟢 await 기반 (함수 흐름 일시 중단 방식)</h3>
<pre><code class="language-js">async function run() {
  const user = await getUser();
  console.log(&quot;user:&quot;, user);
}

run();
console.log(&quot;동기 코드&quot;);</code></pre>
<p><strong>실행 순서</strong></p>
<pre><code>동기 코드      ← 엔진은 멈추지 않음
user: ...      ← await 이후 코드</code></pre><hr />
<h2 id="4️⃣-promise-vs-await--실행-순서가-같을-때--달라질-때">4️⃣ Promise vs await — 실행 순서가 같을 때 / 달라질 때</h2>
<p>Promise와 async/await은 비슷해 보이지만,
await을 어디에서 사용하느냐에 따라 실행 순서는 완전히 달라집니다.</p>
<h3 id="✔-실행-순서가-완전히-같을-때">✔ 실행 순서가 완전히 같을 때</h3>
<h4 id="조건">조건</h4>
<ul>
<li><code>await</code>이 <strong>별도의 async 함수 내부</strong>에 있을 때  </li>
</ul>
<pre><code class="language-js">function Page() {
  async function load() {
    const user = await getUser();
    console.log(&quot;C:&quot;, user);
  }
  load();

  console.log(&quot;B&quot;);
}</code></pre>
<ul>
<li><code>await</code>은** load() 내부**에 있음</li>
<li>Page 함수 자체는 즉시 끝까지 실행됨 → 렌더링도 바로 일어남</li>
<li><code>getUser()</code> 완료 후 load()의 멈춘 지점부터 재개됨</li>
<li>동작은 Promise.then()과 완전히 동일함</li>
</ul>
<h3 id="✔-실행-순서가-달라질-때">✔ 실행 순서가 달라질 때</h3>
<h4 id="조건-1">조건</h4>
<ul>
<li><code>await</code>이 <strong>컴포넌트 최상단 / 함수 최상단</strong>에 있을 때</li>
</ul>
<pre><code class="language-js">async function Page() {
  console.log(&quot;A&quot;);
  await getUser();   // 여기서 전체 흐름이 중단됨
  console.log(&quot;B&quot;);
  return &lt;div&gt;안녕&lt;/div&gt;;
}</code></pre>
<ul>
<li>await 때문에 아래 코드(로그, return 등) 모두 실행되지 않음</li>
<li>JSX return 자체가 지연됨 → 렌더링 지연</li>
<li>렌더링이 안 되었기 때문에: UI가 비어 보임</li>
<li>await이 컴포넌트 최상단에 있으면 <strong>렌더링 자체가 await 이후로 미뤄진다.</strong></li>
</ul>
<hr />
<h3 id="✔-모듈-최상단await-vs-최상단promisethen">✔ 모듈 최상단(await) vs 최상단(Promise.then)</h3>
<h4 id="모듈-최상단await">모듈 최상단(await)</h4>
<pre><code class="language-js">console.log(&quot;A&quot;);
await getUser(); // 5초 걸린다고 가정
console.log(&quot;B&quot;);</code></pre>
<pre><code class="language-text">A
(5초 기다림 — 아래 코드 실행 일시 중단)
getUser 완료됨
B</code></pre>
<ul>
<li>코드 흐름 자체가 <code>await</code>에서 일시 중단</li>
<li>아래 줄(B)은 Promise resolve 후에 실행됨</li>
<li>동기적 순차 실행처럼 보임</li>
</ul>
<h4 id="모듈-최상단promisethen">모듈 최상단(Promise.then)</h4>
<pre><code class="language-js">console.log(&quot;A&quot;);

getUser().then(() =&gt; {
  console.log(&quot;B&quot;);
});

console.log(&quot;C&quot;);
</code></pre>
<pre><code class="language-text">A
C
B</code></pre>
<ul>
<li>then은 콜백만 예약</li>
<li>C는 절대 기다리지 않고 즉시 실행</li>
<li>B는 항상 Microtask로 “나중에” 실행됨</li>
</ul>
<blockquote>
<h4 id="최상단-await-→-아래-코드-실행이-실제로-늦춰짐">최상단 await → 아래 코드 실행이 실제로 늦춰짐</h4>
</blockquote>
<h4 id="최상단-then-→-아래-코드는-절대-기다리지-않음-완전-즉시-실행">최상단 then → 아래 코드는 절대 기다리지 않음 (완전 즉시 실행)</h4>
<hr />
<h2 id="5️⃣-동기-블로킹이-위험한-이유">5️⃣ 동기 블로킹이 위험한 이유</h2>
<p>만약 아래처럼 <strong>진짜 동기 코드</strong>가 오래 걸리면:</p>
<pre><code class="language-js">function block() {
  const start = Date.now();
  while (Date.now() - start &lt; 3000) {}
}

block();  
console.log(&quot;끝&quot;);</code></pre>
<h3 id="⚠️-문제점">⚠️ 문제점</h3>
<ul>
<li>렌더링 멈춤  </li>
<li>클릭 이벤트 안 됨  </li>
<li>스크롤도 안 됨  </li>
<li>브라우저 전체가 프리징됨</li>
</ul>
<p>반면 비동기/await 기반 코드는:</p>
<ul>
<li>UI 절대 안 멈춤  </li>
<li>클릭, 렌더링, 타이머 모두 정상 동작  </li>
<li>async 함수 내부 흐름만 중단된 것처럼 보임</li>
</ul>
<hr />
<h2 id="6️⃣-동기-블로킹-vs-최상단-await">6️⃣ 동기 블로킹 vs 최상단 await</h2>
<p>최상단 await과 동기 블로킹이 결국 “렌더링이 안 되는 것”처럼 보여<br />같은 동작이 아닌가? 라는 궁금증이 생겼습니다.</p>
<p>겉보기에는 둘 다 렌더링이 지연되는 것처럼 보이지만,<br />실제로는 <strong>다른 동작</strong>이 일어납니다.</p>
<hr />
<h3 id="1-동기-블로킹block은-스레드를-진짜로-멈춘다">1) 동기 블로킹(block)은 “스레드를 진짜로 멈춘다”</h3>
<pre><code class="language-js">function block() {
  const start = Date.now();
  while (Date.now() - start &lt; 3000) {}
}

block();</code></pre>
<h4 id="✔-스레드-상태-동기-블로킹">✔ 스레드 상태 (동기 블로킹)</h4>
<ul>
<li>JS 메인 스레드 <strong>완전히 멈춤</strong></li>
<li>콜스택이 비지 않아 <strong>이벤트 루프 정지</strong></li>
<li>렌더링 엔진도 멈춤 → UI 업데이트 불가</li>
<li>클릭 / 스크롤 / 타이머 모두 정지</li>
<li>브라우저 전체가 얼어붙음(프리징)</li>
</ul>
<p>즉,</p>
<blockquote>
<p><strong>브라우저가 3초 동안 아예 죽어버린다.</strong></p>
</blockquote>
<p>동기 블로킹은<br /><strong>CPU를 점유해 스레드를 막아버리는 ‘진짜 멈춤’</strong>입니다.</p>
<hr />
<h3 id="2-최상단-await은-스레드는-멀쩡하고-return만-늦어진다">2) 최상단 await은 “스레드는 멀쩡하고, return만 늦어진다”</h3>
<pre><code class="language-js">async function Page() {
  console.log(&quot;A&quot;);
  await getUser();   // 5초 걸린다고 가정
  console.log(&quot;B&quot;);
  return &lt;div&gt;안녕&lt;/div&gt;;
}</code></pre>
<h4 id="✔-스레드-상태-최상단-await">✔ 스레드 상태 (최상단 await)</h4>
<ul>
<li>스레드는 멈추지 않음</li>
<li><strong>JS 엔진 정상 동작</strong></li>
<li>이벤트 루프도 정상</li>
<li>렌더링 엔진도 멀쩡함</li>
<li>클릭 / 타이머 등 비동기 작업도 정상 작동</li>
</ul>
<h4 id="✔-그런데-렌더링이-왜-안-될까">✔ 그런데 렌더링이 왜 안 될까?</h4>
<ul>
<li>컴포넌트는 JSX를 return해야 렌더링됨</li>
<li>하지만 await 때문에 return 아래 코드가 실행되지 않음</li>
<li>그래서 리턴이 늦어져 렌더링만 지연되는 것</li>
</ul>
<p>즉,</p>
<blockquote>
<p><strong>브라우저는 멀쩡한데, 컴포넌트가 렌더링할 JSX를 아직 못 준 상태.</strong></p>
</blockquote>
<table>
<thead>
<tr>
<th>구분</th>
<th>동기 블로킹(block)</th>
<th>최상단 await</th>
</tr>
</thead>
<tbody><tr>
<td>스레드</td>
<td>❌ 완전 멈춤</td>
<td>✔ 정상 작동</td>
</tr>
<tr>
<td>이벤트 루프</td>
<td>❌ 멈춤</td>
<td>✔ 정상</td>
</tr>
<tr>
<td>렌더링 엔진</td>
<td>❌ 멈춤</td>
<td>✔ 작동하지만 return 지연</td>
</tr>
<tr>
<td>클릭/스크롤</td>
<td>❌ 불가</td>
<td>✔ 렌더링만 되면 가능</td>
</tr>
<tr>
<td>화면이 안 보이는 이유</td>
<td>스레드 자체가 죽어서</td>
<td>return이 늦어서 렌더링 못함</td>
</tr>
<tr>
<td>위험성</td>
<td>매우 높음 (프리징)</td>
<td>리턴 늦음(프리징 아님)</td>
</tr>
</tbody></table>
<hr />
<h2 id="정리">정리</h2>
<h3 id="✔-promise-then">✔ Promise (then)</h3>
<ul>
<li>비동기 작업을 “예약”만 함  </li>
<li>동기 코드를 먼저 실행  </li>
<li>콜백은 Microtask Queue에서 나중에 실행  </li>
<li>UI 절대 안 멈춤</li>
<li>렌더링·클릭 이벤트와 완전히 병렬처럼 동작함  </li>
</ul>
<h3 id="✔-async--await">✔ async + await</h3>
<ul>
<li>Promise 기반 비동기  </li>
<li><strong>async 함수 내부에서만</strong> 순차 처리가 발생  </li>
<li>await이 끝나야 아래 줄 실행됨  </li>
<li>UI는 절대 안 멈춤 </li>
<li>실제로 스레드를 멈추는 것이 아니라,<br /><strong>그 async 함수의 실행 흐름만 잠깐 끊었다가 나중에 재개</strong>되는 구조  </li>
</ul>
<blockquote>
<p>await은 스레드를 멈추는 것이 아니라<br />“해당 async 함수 흐름만 나중에 재개”시키는 장치다.</p>
</blockquote>
<h3 id="✔-동기-블로킹과는-전혀-다름-스레드를-멈추지-않음">✔ 동기 블로킹과는 전혀 다름 (스레드를 멈추지 않음)</h3>
<ul>
<li>동기 블로킹(block)은 <strong>JS 스레드를 완전히 멈춰서</strong><br />렌더링, 클릭, 스크롤 등 모든 UI가 먹통이 됨.  </li>
<li>반면 await은 <strong>스레드를 멈추지 않고</strong>,  
단지 해당 async 함수의 *<em>아래 코드 실행만 잠시 멈춤<br />즉, 화면이 늦게 뜨더라도 *</em>브라우저는 정상적으로 동작.</li>
</ul>
<hr />
<h2 id="💬결론">💬결론</h2>
<p>Promise는 비동기 작업을 “예약”해두고 동기 코드를 먼저 실행하며,<br />await은 그 비동기 작업을 마치 “동기적 순차 흐름”처럼 보이게 만드는 문법입니다.<br /><strong>하지만 실제 엔진은 절대 멈추지 않습니다.</strong>
<strong>await을 어디에 쓰느냐에 따라 Promise와 완전히 같아지기도,
전혀 다르게 동작하기도 합니다.</strong></p>