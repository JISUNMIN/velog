<p>이번 글에서는<br />웹 개발을 하면서 <strong>가장 자주 보지만 헷갈리기 쉬운 <code>window.addEventListener</code>와 이벤트 리스너</strong>를 예시 중심으로 정리해보았습니다.</p>
<ul>
<li><strong>내장 이벤트와 커스텀 이벤트는 무엇이 다를까?</strong>  </li>
<li><strong><code>useEffect</code>의 cleanup에서 왜 꼭 <code>removeEventListener</code>를 해야 할까?</strong>  </li>
<li><strong>왜 웹에서는 커스텀 이벤트를 잘 안 쓰는데, 앱(React Native)에서는 자주 쓸까?</strong>  </li>
</ul>
<hr />
<h2 id="1-windowaddeventlistener란">1. <code>window.addEventListener</code>란?</h2>
<ul>
<li><strong><code>window.addEventListener</code></strong><ul>
<li>브라우저가 제공하는 <strong>Web API</strong> 중 하나입니다.</li>
<li><code>window</code>, <code>document</code>, DOM 요소 등에 <strong>이벤트 리스너를 등록</strong>할 때 사용합니다.</li>
<li>“이런 이벤트가 발생하면, 이 콜백 함수를 실행해주세요”라는 의미입니다.</li>
</ul>
</li>
</ul>
<pre><code class="language-js">window.addEventListener(&quot;scroll&quot;, handleScroll);</code></pre>
<p>위 코드는 다음과 같은 뜻을 가집니다.</p>
<blockquote>
<p>“브라우저가 <code>scroll</code> 이벤트를 발생시키면, <code>handleScroll</code>을 실행해주세요.”</p>
</blockquote>
<p>즉, 이벤트의 <strong>정확한 발생 시점은 내가 제어할 수 없고</strong>,  
<strong>“발생했을 때 알려달라”</strong>고 브라우저에 미리 등록해두는 구조입니다.</p>
<h3 id="✔-addeventlistener-vs-이벤트-리스너listener">✔ addEventListener vs 이벤트 리스너(listener)</h3>
<ul>
<li><code>addEventListener</code> → 이벤트 리스너를 “등록하는 함수(행위)”</li>
<li><code>이벤트 리스너(listener)</code> → 이벤트 발생 시 실행될 “콜백 함수(대상)”</li>
</ul>
<p>즉, <strong>이벤트 리스너는 이벤트가 발생할 때 실행될 ‘콜백 함수’이고,
addEventListener는 그 리스너를 등록하는 함수</strong>입니다.</p>
<hr />
<h2 id="2-내장-이벤트built-in-event란">2. 내장 이벤트(Built-in Event)란?</h2>
<p>내장 이벤트는 <strong>브라우저가 스스로 발생시키는 이벤트</strong>입니다.<br />DOM 요소나 <code>window</code>·<code>document</code> 수준에서 자동으로 발생합니다.</p>
<h3 id="✔-대표적인-내장-이벤트들">✔ 대표적인 내장 이벤트들</h3>
<table>
<thead>
<tr>
<th>이벤트명</th>
<th>대상</th>
<th>설명</th>
<th>예시 사용처</th>
</tr>
</thead>
<tbody><tr>
<td><code>scroll</code></td>
<td>window, element</td>
<td>스크롤이 발생했을 때</td>
<td>무한스크롤, Top 버튼 표시</td>
</tr>
<tr>
<td><code>resize</code></td>
<td>window</td>
<td>창 크기가 변경되었을 때</td>
<td>반응형 레이아웃 처리</td>
</tr>
<tr>
<td><code>keydown</code>, <code>keyup</code></td>
<td>window, element</td>
<td>키보드 입력</td>
<td>단축키 기능, 게임 입력 처리</td>
</tr>
<tr>
<td><code>click</code></td>
<td>element</td>
<td>요소 클릭</td>
<td>버튼 클릭 처리</td>
</tr>
<tr>
<td><code>input</code>, <code>change</code></td>
<td>input 등</td>
<td>입력 값 변경</td>
<td>폼 입력 검증</td>
</tr>
<tr>
<td><code>visibilitychange</code></td>
<td>document</td>
<td>탭 전환(보임/숨김)</td>
<td>백그라운드 시 타이머 일시정지</td>
</tr>
<tr>
<td><code>online</code>, <code>offline</code></td>
<td>window</td>
<td>네트워크 연결/끊김</td>
<td>오프라인 안내 배너 표시</td>
</tr>
</tbody></table>
<p>이들은 모두 브라우저가 <strong>스스로 이벤트를 발생</strong>시키기 때문에
반드시 이벤트 리스너로 처리해야 합니다.</p>
<hr />
<h2 id="3-커스텀-이벤트custom-event란">3. 커스텀 이벤트(Custom Event)란?</h2>
<p>커스텀 이벤트는 <strong>브라우저가 아니라 개발자가 직접 만들어서 발생시키는 이벤트</strong>입니다.</p>
<h3 id="✔-기본-커스텀-이벤트-예시">✔ 기본 커스텀 이벤트 예시</h3>
<pre><code class="language-js">// 1. 이벤트 리스너 등록
function onRefresh() {
  console.log(&quot;refresh 이벤트 감지&quot;);
}
window.addEventListener(&quot;refresh&quot;, onRefresh);

// 2. 이벤트 발생(emit)
window.dispatchEvent(new Event(&quot;refresh&quot;));</code></pre>
<p>위 예시는 <strong>브라우저 환경(웹)</strong>에서 사용하는 방식입니다.
브라우저에는 window 객체가 존재하므로, 이 객체에 이벤트를 등록하고(addEventListener),
직접 발생시키기(dispatchEvent)가 가능합니다.</p>
<hr />
<h2 id="4-웹에서는-커스텀-이벤트가-왜-잘-안-쓰일까">4. 웹에서는 커스텀 이벤트가 왜 잘 안 쓰일까?</h2>
<p>일반적인 React 웹 개발에서는 대부분의 UI 통신이
아래 방식으로 해결됩니다.</p>
<ul>
<li>부모 → 자식:** props**</li>
<li>자식 → 부모: <strong>콜백 함수(props callback)</strong></li>
<li>여러 곳에서 공유되는 데이터: <strong>Redux / Zustand / Context</strong></li>
</ul>
<p>이 구조만으로도 대부분의 데이터 흐름을 충분히 처리할 수 있습니다.</p>
<p>따라서, 웹(Web)에서는 커스텀 이벤트를 일부러 사용할 필요가 적기 때문에
실제 코드에서 자주 보이지 않습니다.</p>
<p>커스텀 이벤트는 특정 구조적 제약이 있을 때(전역 알림 등)만 제한적으로 사용됩니다</p>
<hr />
<h2 id="5-cleanup에서-removeeventlistener가-필요한-이유">5. cleanup에서 removeEventListener가 필요한 이유</h2>
<p>React에서는 <code>addEventListener</code>를 보통 아래처럼 <strong>useEffect 안에서 등록</strong>합니다.</p>
<pre><code class="language-js">useEffect(() =&gt; {
  function handleScroll() {
    console.log(&quot;스크롤!&quot;);
  }

  window.addEventListener(&quot;scroll&quot;, handleScroll);

  return () =&gt; {
    window.removeEventListener(&quot;scroll&quot;, handleScroll);
  };
}, []);</code></pre>
<p>그럼 질문이 생깁니다.</p>
<blockquote>
<p>“왜 굳이 return에서 removeEventListener를 해줘야 할까?”
“컴포넌트가 언마운트되면 자동으로 사라지는 거 아닐까?”</p>
</blockquote>
<p>아닙니다. 
<code>window.addEventListener</code>로 등록한 리스너는<br />React가 아니라 <strong>브라우저 전역(window)</strong> 에 등록됩니다.</p>
<p>따라서 컴포넌트가 사라져도 삭제되지 않습니다.
그래서 <strong>cleanup 함수</strong>가 필요합니다.</p>
<h3 id="✔-cleanup을-하지-않았을때-문제점">✔ cleanup을 하지 않았을때 문제점</h3>
<h4 id="1-이벤트-리스너가-중복-등록됨">1) 이벤트 리스너가 “중복 등록”됨</h4>
<p>컴포넌트가 리렌더링되거나 다시 마운트되면
같은 리스너가 window에 여러 번 추가됩니다.</p>
<h4 id="2-이벤트가-여러-번-실행되는-버그-발생">2) 이벤트가 여러 번 실행되는 버그 발생</h4>
<p>등록된 리스너가 3개면 클릭 시 3번 실행됩니다.</p>
<h4 id="3-메모리-누수-발생">3) 메모리 누수 발생</h4>
<p>컴포넌트가 이미 사라졌는데도
리스너가 계속 살아있어 메모리가 회수되지 못합니다.</p>
<hr />
<h2 id="6-함수-vs-addlistener-vs-windowaddeventlistener">6. 함수 vs addListener vs window.addEventListener</h2>
<p>어떤 것은 <strong>변수에 넣을 수 있고</strong>, 어떤 것은 <strong>넣어도 소용이 없습니다.</strong><br />그 차이를 정확하게 이해해야 이벤트 시스템을 제대로 사용할 수 있습니다.</p>
<h3 id="✔-1-일반-함수fn는-호출해야-실행된다">✔ 1) 일반 함수(fn)는 “호출해야 실행된다”</h3>
<pre><code class="language-js">const fn = () =&gt; console.log(&quot;hello&quot;);</code></pre>
<ul>
<li>fn(); // 직접 호출해야 실행됨</li>
<li>변수에 넣는다고 실행되지 않음</li>
<li>실행은 fn() 호출 시점에 일어남</li>
</ul>
<h3 id="✔-2-eventemitter의-addlistener는-호출--등록">✔ 2) EventEmitter의 addListener는 “호출 = 등록”</h3>
<pre><code class="language-js">const subscription = emitter.addListener(&quot;paymentSuccess&quot;, callback);</code></pre>
<p>이 코드가 실행되면:</p>
<ul>
<li><code>addListener()</code>가 호출됨</li>
<li>emitter 내부의 리스너 목록에 callback이 즉시 등록됨</li>
<li>등록된 리스너를 제거할 수 있는 subscription 객체 반환</li>
</ul>
<blockquote>
<p>addListener는 반환값을 변수에 넣었는지와 상관없이,
addListener(...) 라는 함수가 호출된 순간에 이미 등록이 완료됩니다.</p>
</blockquote>
<h3 id="✔3-windowaddeventlistener는-subscription을-반환하지-않는다">✔3) window.addEventListener는 subscription을 반환하지 않는다</h3>
<pre><code class="language-js">const sub = window.addEventListener(&quot;scroll&quot;, handler);

console.log(sub); // undefined</code></pre>
<ul>
<li>window.addEventListener는 반환값이 없다(undefined)</li>
<li>DOM 이벤트 시스템은 EventEmitter 방식이 아님</li>
<li>삭제는 반드시 이렇게만 가능:
window.removeEventListener(&quot;scroll&quot;, handler);</li>
</ul>
<p>반환값이 없기 때문에 “subscription.remove()” 같은 패턴을 사용할 수 없음</p>
<hr />
<h4 id="요약">요약</h4>
<ul>
<li><p>EventEmitter.addListener는 반환값(subscription)이 있기 때문에
변수로 받을 수 있고 → subscription.remove()로 해지 가능</p>
</li>
<li><p>window.addEventListener는 반환값이 없기 때문에
변수에 넣어도 의미 없고 → 반드시 removeEventListener(handler)로 해지해야 한다.</p>
</li>
</ul>
<hr />
<h2 id="7-참고">7. 참고</h2>
<h3 id="7-1-앱react-native에서는-커스텀-이벤트가-왜-자주-쓰일까">7-1. 앱(React Native)에서는 커스텀 이벤트가 왜 자주 쓰일까?</h3>
<p>React Native 환경은 웹과 다르게 <strong>window / DOM이 없습니다.</strong><br />또한 iOS/Android 네이티브 환경과 상호작용하며<br />다양한 네이티브 이벤트가 발생합니다.</p>
<p>예: GPS 위치, BLE 데이터, 센서, 알림 등</p>
<p>웹에서는 <code>window.dispatchEvent()</code> 같은 Web API를 사용할 수 있지만,
React Native에는 <code>window</code> 자체가 없기 때문에 동일한 방식으로 커스텀 이벤트를 만들 수 없습니다.</p>
<p>대신 React Native에서는 <strong>네이티브 → JS 사이의 이벤트 전달을 위해 EventEmitter 패턴을 사용합니다.</strong></p>
<pre><code class="language-js">import EventEmitter from &quot;eventemitter3&quot;;

const emitter = new EventEmitter();

// 1. 이벤트 리스너 등록
emitter.on(&quot;refresh&quot;, () =&gt; {
  console.log(&quot;refresh 이벤트 감지!&quot;);
});

// 2. 이벤트 발생
emitter.emit(&quot;refresh&quot;);
</code></pre>
<h3 id="72-앱에서는-왜-emit이-더-자주-나올까">7.2 앱에서는 왜 emit이 더 자주 나올까?</h3>
<p>웹에서는 대부분의 변화가 React 트리 안에서 발생하지만,
앱에서는 React 트리 밖에서(네이티브/OS에서) 변화가 발생합니다.</p>
<h4 id="🟢-웹에서-발생하는-변화-react-내부에서-해결-가능">🟢 웹에서 발생하는 변화 (React 내부에서 해결 가능)</h4>
<ul>
<li>버튼 클릭 → refetch()</li>
<li>라우트 변경 → useEffect로 감지</li>
<li>폼 제출 → mutation 후 invalidateQueries</li>
<li>UI 내에서 값 변화 → 상태 변화로 자동 반영</li>
</ul>
<p>→ props / state / React Query만으로 충분, 별도의 emit 필요 없음</p>
<hr />
<h4 id="🔵-rn에서는-react-바깥-세상에서-이벤트가-자주-발생">🔵 RN에서는 “React 바깥 세상”에서 이벤트가 자주 발생</h4>
<p>예를 들어:</p>
<ul>
<li>Push 알림에서 “결제 완료됨” 신호 수신</li>
<li>네이티브 결제 SDK가 성공/실패 이벤트 발생</li>
<li>PS가 백그라운드에서 위치 업데이트</li>
<li>BLE(Bluetooth Low Energy) 센서가 주기적으로 데이터 전송</li>
<li>앱 포그라운드/백그라운드 전환 이벤트 발생</li>
</ul>
<p>이런 건 모두 <strong>JS 안이 아니라 OS/Native 모듈이 발생시키는 사건</strong>입니다.</p>
<p>그래서 RN에서는</p>
<p>네이티브가 emit → JS가 addListener로 받고 → React Query로 데이터 refetch
라는 패턴이 자주 등장합니다.</p>
<pre><code class="language-ts">// 네이티브에서 &quot;paymentSuccess&quot; 이벤트 emit
emitter.addListener(&quot;paymentSuccess&quot;, () =&gt; {
  queryClient.invalidateQueries([&quot;payments&quot;]);
});</code></pre>
<ul>
<li>서버 데이터 관리 → React Query</li>
<li>네이티브 이벤트 전달 → EventEmitter</li>
<li>둘을 분리하고 필요한 곳만 연결</li>
</ul>
<hr />
<h2 id="💬-요약-정리">💬 요약 정리</h2>
<ul>
<li>내장 이벤트는 브라우저가 자동으로 발생시키는 이벤트입니다.  </li>
<li>커스텀 이벤트는 직접 생성하여 간접 호출이 필요할 때 사용합니다.  </li>
<li>React에서는 cleanup에서 반드시 <code>removeEventListener</code>를 수행해야 합니다.  </li>
<li>웹에서는 props/state/상태관리만으로 충분하기 때문에 커스텀 이벤트를 자주 쓰지 않습니다.</li>
<li>React Native는 네이티브 세계(OS)에서 발생하는 이벤트가 많기 때문에
EventEmitter 기반의 이벤트 구독(addListener)이 자주 등장합니다.</li>
<li>addEventListener/addListener는 호출되는 순간 “등록”이 끝납니다.</li>
</ul>