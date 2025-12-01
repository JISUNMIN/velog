<p>자바스크립트를 배우면서 헷갈리는 개념 중 하나가 <strong>비동기(Asynchronous)</strong>입니다.</p>
<ul>
<li>자바스크립트는 싱글 스레드라는데, 어떻게 동시에 여러 일을 처리하지?</li>
<li>Promise는 함수야? 객체야?</li>
<li>async/await는 Promise를 대체하는 건가?</li>
<li>async/await에서는 then/catch를 안 써도 되는 건가?</li>
</ul>
<p>이 글에서는  <strong>콜백 → Promise → async/await → 이벤트 루프(Microtask/Macrotask)</strong> 흐름과 함께<br />이 개념들이 실제로 어떻게 연결되어 있는지를 전체적으로 이해해보겠습니다.</p>
<hr />
<h2 id="1️⃣-싱글-스레드--한-번에-한-작업만-실행하는-언어">1️⃣ 싱글 스레드 — 한 번에 한 작업만 실행하는 언어</h2>
<p>자바스크립트는 <strong>싱글 스레드(single-thread)</strong> 언어입니다.<br />즉, 콜 스택 하나로 <strong>한 줄씩 순서대로만 실행</strong>합니다.</p>
<pre><code>한 줄 → 또 한 줄 → 또 한 줄</code></pre><p>그런데 실제로는</p>
<ul>
<li>서버 요청(fetch)</li>
<li>타이머(setTimeout)</li>
<li>클릭 이벤트</li>
<li>렌더링</li>
</ul>
<p>여러 일이 동시에 일어나는 것처럼 보입니다.</p>
<p>바로 이걸 가능하게 하는 것이 <strong>비동기 + 이벤트 루프(Event Loop)</strong> 입니다.</p>
<hr />
<h2 id="2️⃣-비동기asynchronous란">2️⃣ 비동기(Asynchronous)란?</h2>
<blockquote>
<p>오래 걸리는 작업을 <strong>기다리지 않고</strong>,    
JS는 다음 코드를 <strong>계속 실행하는 방식</strong></p>
</blockquote>
<p>예를 들어:</p>
<pre><code class="language-js">console.log(&quot;1&quot;);

setTimeout(() =&gt; {
  console.log(&quot;2&quot;);
}, 1000);

console.log(&quot;3&quot;);</code></pre>
<p>출력:</p>
<pre><code>1
3
2</code></pre><ul>
<li>setTimeout은 “1초 뒤 실행하세요”라고 브라우저에게 예약</li>
<li>JS는 다음 코드(3)를 바로 실행</li>
<li>1초 뒤 타이머가 준비되지만, <strong>Call Stack(동기 코드)이 끝난 뒤에야</strong> 실행됨</li>
</ul>
<hr />
<h2 id="3️⃣-콜백callback--비동기의-시작">3️⃣ 콜백(callback) — 비동기의 시작</h2>
<p>콜백은 <strong>나중에 실행될 함수를 넘기는 것</strong>입니다.</p>
<pre><code class="language-js">setTimeout(() =&gt; {
  console.log(&quot;타이머 완료&quot;);
}, 3000);</code></pre>
<ul>
<li>&quot;집 도착하면 전화해줘&quot; → 콜백 등록  </li>
<li>친구가 집 도착한 순간 전화 → 콜백 실행</li>
</ul>
<hr />
<h3 id="콜백-지옥callback-hell--promise가-등장한-이유">콜백 지옥(CallBack Hell) — Promise가 등장한 이유</h3>
<p>콜백을 많이 쓰다 보면 아래처럼 코드가 점점 중첩되는 문제가 발생합니다.</p>
<pre><code class="language-js">getUser(id, (user) =&gt; {
  getPosts(user.id, (posts) =&gt; {
    getComments(posts[0].id, (comments) =&gt; {
      save(comments, () =&gt; {
        console.log(&quot;완료&quot;);
      });
    });
  });
});
</code></pre>
<p>이런 코드를 콜백 지옥(CallBack Hell) 이라고 합니다.
문제가 되는 이유:</p>
<p>들여쓰기 지옥 (계단 모양 코딩)</p>
<ul>
<li>에러 처리가 매우 어려움</li>
<li>중간 단계에서 재사용 어려움</li>
<li>흐름 파악이 어려움</li>
<li>유지보수 거의 불가능</li>
</ul>
<p><strong>그래서 등장한 것이 Promise입니다.</strong></p>
<hr />
<p>Promise는 콜백 지옥을 해결하기 위해 ES6(2015)에서 등장했습니다.</p>
<p><strong>Promise는 비동기 작업을 객체로 다루는 방식을 제공하여
중첩되지 않고 체이닝 형태로 표현할 수 있습니다.</strong></p>
<pre><code class="language-js">getUser(id)
  .then(user =&gt; getPosts(user.id))
  .then(posts =&gt; getComments(posts[0].id))
  .then(comments =&gt; save(comments))
  .catch(err =&gt; console.error(err));</code></pre>
<ul>
<li>깊은 중첩(콜백 지옥) 해결</li>
<li>then 체인으로 순서를 흐름처럼 표현</li>
<li>에러를 catch 하나로 처리 가능</li>
</ul>
<hr />
<p>하지만 Promise도 완벽하지 않았습니다.</p>
<h4 id="promise의-한계then-체인의-문제점">Promise의 한계(then 체인의 문제점)</h4>
<ul>
<li>then 체인이 길어지면 여전히 복잡함  </li>
<li>코드 흐름이 동기처럼 “위 → 아래”로 읽히지 않음  </li>
<li>예외 처리(catch)가 자연스럽지 않음  </li>
<li>순차 비동기 로직 작성 시 가독성이 떨어짐 </li>
</ul>
<p>여전히 <code>then → then → then</code>이라는 <strong>체인 지옥(then hell)</strong>이 생길 수 있습니다.
그래서 등장한 async/await (ES2017)이 등장했습니다.</p>
<h3 id="✅-asyncawait의-장점">✅ async/await의 장점</h3>
<ul>
<li>비동기 코드를 <strong>동기 코드처럼 자연스럽게</strong> 작성 가능  </li>
<li>코드 흐름이 “위 → 아래”로 읽혀 가독성이 극적으로 향상  </li>
<li>에러 처리도 <code>try/catch</code>로 자연스럽게 처리 가능  </li>
<li>복잡한 Promise 체인을 평평하게 만들 수 있음  </li>
</ul>
<pre><code class="language-js">async function load() {
  try {
    const user = await getUser(id);
    const posts = await getPosts(user.id);
    const comments = await getComments(posts[0].id);

    console.log(&quot;완료!&quot;);
  } catch (err) {
    console.error(err);
  }
}</code></pre>
<p>위 코드는 훨씬 읽기 좋고
비동기 흐름을 <strong>순서대로 표현</strong>할 수 있습니다.</p>
<hr />
<ul>
<li><strong>콜백 지옥(CallBack Hell)</strong> → Promise가 해결</li>
<li><strong>then 체인 지옥(Then Hell)</strong> → async/await이 해결</li>
</ul>
<hr />
<h2 id="4️⃣-promise--비동기-결과를-담는-객체">4️⃣ Promise — 비동기 결과를 담는 객체</h2>
<p>✔ Promise는 비동기 작업의 결과를 담는 객체이며, new Promise()로 만드는 “클래스 기반** 객체**”입니다.</p>
<pre><code class="language-js">const p = new Promise((resolve, reject) =&gt; {
  setTimeout(() =&gt; {
    resolve(&quot;성공&quot;);
  }, 1000);
});</code></pre>
<p>이때 실행되는 건 <strong>new Promise 내부 콜백 함수</strong>입니다.</p>
<p>Promise는 3가지 상태를 가집니다.</p>
<table>
<thead>
<tr>
<th>상태</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td>pending</td>
<td>대기 중</td>
</tr>
<tr>
<td>fulfilled</td>
<td>성공(resolve 호출)</td>
</tr>
<tr>
<td>rejected</td>
<td>실패(reject 호출)</td>
</tr>
</tbody></table>
<hr />
<h2 id="5️⃣-then--catch--promise-객체의-메서드">5️⃣ then / catch — Promise 객체의 “메서드”</h2>
<p>then과 catch는 <strong>Promise 객체가 가진 메서드(함수)</strong> 입니다.</p>
<pre><code class="language-js">p.then((value) =&gt; {
  console.log(&quot;성공:&quot;, value);
}).catch((err) =&gt; {
  console.log(&quot;실패:&quot;, err);
});</code></pre>
<p>p.them()은 “Promise 객체의 then() 함수를 호출한다”는 뜻입니다.</p>
<ul>
<li>then → 성공 시 실행(콜백)</li>
<li>catch → 실패 시 실행(콜백)</li>
</ul>
<hr />
<h2 id="6️⃣-microtask와-macrotask--비동기-우선순위의-핵심">6️⃣ Microtask와 Macrotask — 비동기 우선순위의 핵심</h2>
<p>자바스크립트 비동기는 아래 순서로 실행됩니다:</p>
<h3 id="동기-→-microtask-→-macrotask"><strong>동기 → Microtask → Macrotask</strong></h3>
<hr />
<h3 id="✔-microtask마이크로태스크">✔ Microtask(마이크로태스크)</h3>
<p>가장 우선적으로 실행되는 비동기 작업입니다.</p>
<p>대표:</p>
<ul>
<li><strong>Promise.then / catch / finally</strong></li>
<li>queueMicrotask()</li>
<li>MutationObserver</li>
</ul>
<hr />
<h3 id="✔-macrotask매크로태스크">✔ Macrotask(매크로태스크)</h3>
<p>Microtask 이후 실행되는 비동기 작업입니다.</p>
<p>대표:</p>
<ul>
<li><strong>setTimeout</strong></li>
<li>setInterval</li>
<li>setImmediate(Node)</li>
<li>I/O 작업</li>
<li>UI 이벤트</li>
</ul>
<hr />
<h3 id="예시">예시:</h3>
<pre><code class="language-js">console.log(&quot;1&quot;);

setTimeout(() =&gt; console.log(&quot;타이머&quot;), 0);

Promise.resolve().then(() =&gt; console.log(&quot;프로미스&quot;));

console.log(&quot;2&quot;);</code></pre>
<p>실행 순서:</p>
<pre><code>1
2
프로미스   ← Microtask (Promise)
타이머      ← Macrotask (setTimeout)</code></pre><hr />
<h2 id="7️⃣-settimeout은-왜-정확히-3초-뒤-실행되지-않을까">7️⃣ setTimeout은 왜 “정확히 3초 뒤” 실행되지 않을까?</h2>
<p>저는 이렇게 생각했습니다.</p>
<blockquote>
<p>“setTimeout(3000)은 3초 뒤에 무조건 실행된다.”</p>
</blockquote>
<p>그러나 실제로는:</p>
<h3 id="✔-settimeout3초는">✔ setTimeout(3초)는</h3>
<p><strong>“3초 뒤 <em>실행할 준비가 된다</em>”</strong>는 뜻입니다.</p>
<p>실행 과정:</p>
<ol>
<li>3초가 지나면 콜백이 <strong>Macrotask Queue</strong>로 이동합니다.</li>
<li>하지만 <strong>Call Stack(동기 코드)</strong> 이 남아 있으면 절대 실행되지 않습니다.</li>
<li>따라서 실제 실행 시점은 다음과 같습니다.</li>
</ol>
<pre><code>실행 시점 = 3초 + 동기 코드가 끝나는 시간</code></pre><hr />
<h3 id="예시-1">예시</h3>
<pre><code class="language-js">console.log(&quot;1&quot;);

setTimeout(() =&gt; {
  console.log(&quot;타이머&quot;);
}, 3000);

for (let i = 0; i &lt; 1000000000; i++) {} // 무거운 동기 코드

console.log(&quot;2&quot;);</code></pre>
<h3 id="실행-결과">실행 결과</h3>
<pre><code>1
(오래 걸리는 for문 실행 중)
2
타이머  ← 3초가 지나도 동기 코드가 끝나기 전에는 절대 실행되지 않음</code></pre><p>setTimeout의 시간은 <strong>“최소 지연 시간”</strong>입니다.<br />3초가 지난 뒤 <strong>가능한 가장 빠른 시점에 실행될 뿐</strong>입니다.</p>
<h2 id="8️⃣-async--await--promise를-쉽게-사용하는-문법">8️⃣ async / await — Promise를 쉽게 사용하는 문법</h2>
<p>async/await은 Promise를 대체하는 문법이 아니라
<strong>Promise 위에서 동작하는 문법</strong>입니다.</p>
<h3 id="✔-async-함수는-항상-promise를-반환합니다">✔ async 함수는 항상 Promise를 반환합니다.</h3>
<pre><code class="language-js">async function run() {
  return 123;
}

run(); // Promise&lt;123&gt;</code></pre>
<p>내부적으로 이렇게 변환합니다:</p>
<pre><code class="language-js">function run() {
  return new Promise((resolve) =&gt; resolve(123));
}</code></pre>
<h3 id="✔-await은-promisethen을-동기-코드처럼-보이게-합니다">✔ await은 Promise.then()을 “동기 코드처럼” 보이게 합니다.</h3>
<pre><code class="language-js">const data = await fetchData();</code></pre>
<p>아래코드와 동일합니다:</p>
<pre><code class="language-js">fetchData().then(data =&gt; ...)</code></pre>
<hr />
<h2 id="9️⃣-thencatch-vs-asyncawait">9️⃣ then/catch vs async/await</h2>
<p><strong>async/await = Promise 기반 문법</strong>
Promise 없이는 async/await도 존재할 수 없습니다.</p>
<h3 id="1-🔵-thencatch--promise-기본-문법">1) 🔵 then/catch — Promise 기본 문법</h3>
<p>then과 catch는 Promise 객체가 원래부터 가지고 있는 메서드입니다.<br /><strong>Promise then/catch는 “콜백을 등록하는 문법”이기 때문에
실행 흐름을 멈추지 않고, top-level(전역)에서도 그대로 사용 가능합니다.</strong></p>
<p>즉, 다음 코드는 함수 밖에서도 문제 없이 바로 실행됩니다.</p>
<pre><code class="language-js">  fetchUser()
    .then(user =&gt; {
      return fetchPosts(user.id);        
    })
    .then(posts =&gt; {
      return fetchComments(posts[0].id);  
    })
    .then(comments =&gt; {
      console.log(&quot;결과:&quot;, comments);     
    })
    .catch(error =&gt; {
      console.error(&quot;오류:&quot;, error);     
    });</code></pre>
<h3 id="🟢-2-asyncawait--promise를-더-쉽게-쓰는-문법">🟢 2) async/await — Promise를 더 쉽게 쓰는 문법</h3>
<p>async/await은 Promise를 더 읽기 좋게 바꾼 문법입니다.</p>
<p><code>await</code>은 “실행 흐름을 일시 중단(suspend)하는 것처럼 보이는 문법&quot;이기 때문에
이러한 중단은 전역(top-level)에서는 허용되지 않습니다.
즉, 반드시 <strong>async function 내부에서만 사용할 수 있습니다.</strong></p>
<p>왜냐하면 top-level 코드가 중단되면
스크립트 전체 로딩이 멈춰버리는 문제가 생기기 때문입니다.</p>
<p>그래서 async/await 코드는 아래처럼 반드시 함수로 감싸야 합니다:</p>
<pre><code class="language-js">async function load() {
  try {
    const user = await fetchUser();
    const posts = await fetchPosts(user.id);
    const comments = await fetchComments(posts[0].id);

    console.log(&quot;결과:&quot;, comments);
  } catch (err) {
    console.error(&quot;오류:&quot;, err);
  }
}</code></pre>
<h4 id="⚠️-예외-es-moduleesm에서는-top-level-await-허용">⚠️ 예외— ES Module(ESM)에서는 top-level await 허용</h4>
<p>모듈(<code>&lt;script type=&quot;module&quot;&gt;</code>) 환경에서는 top-level await 사용이 가능합니다.</p>
<pre><code class="language-js">// ESM 환경에서는 가능!
const user = await fetchUser();</code></pre>
<h3 id="3-async-함수는-항상-promise를-반환합니다">3) async 함수는 항상 Promise를 반환합니다.</h3>
<pre><code class="language-js">async function test() {
  return 123;
}

test().then(v =&gt; console.log(v)); // 123</code></pre>
<p>아래 코드와 동일합니다.</p>
<pre><code class="language-js">function test() {
  return new Promise(resolve =&gt; resolve(123));
}
</code></pre>
<h3 id="4-같은-기능을-두-문법으로-비교">4) 같은 기능을 두 문법으로 비교</h3>
<p>✔ Promise 방식
Promise는 top-level에서도 바로 실행할 수 있습니다.</p>
<pre><code class="language-js">getData()
  .then(data =&gt; process(data))
  .then(result =&gt; save(result))
  .catch(error =&gt; console.error(error));</code></pre>
<p>✔ async/await 방식
<code>await</code>은 async 함수 안에서만 가능하기 때문에
같은 기능을 구현하려면 반드시 함수를 만들어야 합니다.</p>
<pre><code class="language-js">async function run() {
  try {
    const data = await getData();
    const result = await process(data);
    await save(result);
  } catch (error) {
    console.error(error);
  }
}</code></pre>
<table>
<thead>
<tr>
<th>개념</th>
<th>의미</th>
</tr>
</thead>
<tbody><tr>
<td>then/catch</td>
<td>Promise 객체의 메서드 (top-level에서 바로 사용 가능)</td>
</tr>
<tr>
<td>async/await</td>
<td>Promise를 더 쉽게 사용하는 문법 (반드시 함수 안에서만 사용 가능)</td>
</tr>
<tr>
<td>await</td>
<td>then과 동일한 역할(비동기 결과를 기다림)</td>
</tr>
<tr>
<td>try/catch</td>
<td>catch와 동일한 역할(에러 처리)</td>
</tr>
<tr>
<td>async 함수</td>
<td>항상 Promise를 반환함</td>
</tr>
</tbody></table>
<hr />
<h2 id="🔟-thencatch-방식-vs-asyncawait-방식-비교">🔟 then/catch 방식 vs async/await 방식 비교</h2>
<h3 id="thencatch-버전">then/catch 버전</h3>
<pre><code class="language-js">getUser()
  .then((user) =&gt; getPosts(user.id))
  .then((posts) =&gt; getComments(posts[0].id))
  .then((comments) =&gt; console.log(comments))
  .catch(console.error);</code></pre>
<h3 id="asyncawait-버전">async/await 버전</h3>
<pre><code class="language-js">async function load() {
  try {
    const user = await getUser();
    const posts = await getPosts(user.id);
    const comments = await getComments(posts[0].id);

    console.log(comments);
  } catch (e) {
    console.error(e);
  }
}</code></pre>
<hr />
<h2 id="💬-정리">💬 정리</h2>
<ul>
<li>JS는 싱글 스레드</li>
<li>오래 걸리는 작업은 브라우저가 대신 기다림(비동기)</li>
<li>Promise는 비동기 결과를 담는 객체</li>
<li>then/catch는 Promise의 공식 메서드</li>
<li>async/await은 Promise를 더 읽기 좋은 문법</li>
<li>then/await이 “나중에 실행”되는 이유 = Microtask Queue + Event Loop</li>
<li>setTimeout은 정확한 시간이 아니라 “최소 지연 시간”</li>
</ul>
<p>결국 JS의 모든 비동기 로직은<br /><strong>Promise + 이벤트 루프</strong> 위에서 돌아가는 구조입니다.</p>