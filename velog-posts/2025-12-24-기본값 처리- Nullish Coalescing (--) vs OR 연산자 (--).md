<p>개발을 하다 보면 아래와 같은 코드를 자주 볼 수 있습니다.</p>
<pre><code class="language-js">userData?.name || &quot;&quot;;
userData?.name ?? &quot;&quot;;</code></pre>
<p>두 코드는 비슷해 보이지만 <strong>동작 방식에는 중요한 차이</strong>가 있습니다.</p>
<hr />
<h2 id="-or-연산자"><code>||</code> (OR) 연산자</h2>
<p><code>||</code> 연산자는 <strong>왼쪽 값이 falsy이면</strong> 오른쪽 값을 반환</p>
<h3 id="falsy-값-목록">Falsy 값 목록</h3>
<p>아래 값들은 모두 <code>false</code>처럼 취급됩니다.</p>
<pre><code class="language-js">false
0
&quot;&quot;
null
undefined
NaN</code></pre>
<h3 id="예시">예시</h3>
<pre><code class="language-js">0 || &quot;default&quot;        // &quot;default&quot;
&quot;&quot; || &quot;default&quot;       // &quot;default&quot;
false || &quot;default&quot;    // &quot;default&quot;
null || &quot;default&quot;     // &quot;default&quot;</code></pre>
<hr />
<h2 id="-nullish-coalescing-연산자"><code>??</code> (Nullish Coalescing) 연산자</h2>
<p><code>??</code> 연산자는 <strong>왼쪽 값이 null 또는 undefined일 때만</strong> 오른쪽 값을 반환</p>
<p>즉, <strong>nullable 값만 체크</strong>합니다.</p>
<h3 id="nullable-값-목록">Nullable 값 목록</h3>
<pre><code class="language-js">null
undefined</code></pre>
<h3 id="예시-1">예시</h3>
<pre><code class="language-js">0 ?? &quot;default&quot;         // 0
&quot;&quot; ?? &quot;default&quot;        // &quot;&quot;
false ?? &quot;default&quot;     // false
null ?? &quot;default&quot;      // &quot;default&quot;
undefined ?? &quot;default&quot; // &quot;default&quot;</code></pre>
<hr />
<h2 id="문제가-될-수-있는-상황">문제가 될 수 있는 상황</h2>
<pre><code class="language-js">userData?.name || &quot;&quot;</code></pre>
<p>위 코드는 <code>userData.name</code>이  </p>
<ul>
<li><code>&quot;&quot;</code> (빈 문자열)</li>
<li><code>0</code></li>
</ul>
<p>인 경우에도 <strong>의도치 않게 빈 문자열로 대체</strong>될 수 있습니다.</p>
<pre><code class="language-js">userData?.name ?? &quot;&quot;</code></pre>
<p>이 코드는  </p>
<ul>
<li><code>null</code></li>
<li><code>undefined</code></li>
</ul>
<p>일 때만 대체되므로 <strong>보통 의도한 동작에 더 가깝습니다</strong>.</p>
<hr />
<h2 id="그렇다면--연산자는-언제-사용할까">그렇다면 <code>||</code> 연산자는 언제 사용할까?</h2>
<p><code>||</code> 연산자는<br />“값이 있느냐”보다는 <strong>“조건이 참이냐 거짓이냐”가 중요한 상황</strong>에서 사용합니다.</p>
<p>즉, 값이 <code>0</code>이든, 빈 문자열이든 상관없이<br /><strong>falsy라면 모두 같은 의미로 처리하고 싶을 때</strong> 적합합니다.</p>
<h3 id="조건문에서-or-조건이-필요할-때">조건문에서 OR 조건이 필요할 때</h3>
<pre><code class="language-js">if (isAdmin || isOwner) {
  // 둘 중 하나라도 true면 실행
}</code></pre>
<p>이 경우에 값의 내용이 무엇인지는 중요하지 않고,
하나라도 true인지 여부만 판단하면 되기 때문에 사용합니다.</p>
<h3 id="falsy-값은-모두-없다고-판단해도-될-때">falsy 값은 모두 “없다”고 판단해도 될 때</h3>
<pre><code class="language-js">const value = userInput || &quot;기본값&quot;;</code></pre>
<p>여기서 userInput이
&quot;&quot;, 0, false 라면, 사용자가 값을 제대로 입력하지 않았다고 판단하고 
무조건 기본값을 사용해도 되는 상황일 수 있습니다.
이런 경우는 의도에 맞기 때문에 사용할 수 있습니다.</p>
<hr />
<h2 id="결론">결론</h2>
<ul>
<li><strong>값이 없을 때만 기본값을 쓰고 싶다면</strong> → <code>??</code></li>
<li><strong>Falsy 값까지 전부 걸러도 된다면</strong> → <code>||</code></li>
</ul>
<p>대부분의 경우, 특히 <strong>데이터 렌더링에서는 <code>??</code> 연산자를 사용하는 것이 더 안전합니다.</strong></p>
<hr />
<h2 id="한-줄-요약">한 줄 요약</h2>
<blockquote>
<p><code>||</code>는 falsy 값 기준 ,<code>??</code>는 Nullish 값 기준이다.<br />0이나 빈 문자열이 정상 값으로 들어올 수 있다면 <code>??</code>연산자를 사용해야 한다.</p>
</blockquote>