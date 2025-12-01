<h2 id="💬-학습을-시작하는-이유">💬 학습을 시작하는 이유</h2>
<p>새로 입사한 회사에서 기존에 <strong>Swift / Java로 개발된 네이티브 앱을 React Native로 전환하는 작업</strong>이 예정되어 있으며,<br />그 작업을 저 혼자(?) 진행할 수도 있는 상황입니다.</p>
<p>저는 기존에 <strong>React</strong>를 다룰 줄 알기 때문에<br />React Native 역시 비교적 빠르게 익힐 수 있다는 이야기를 많이 들어왔습니다.<br />하지만 실제로는 React와 공통점도 많지만 차이점 역시 적지 않다고 하여,<br />본격적인 실무에 투입되기 전 충분한 학습이 필요하다고 판단했습니다.</p>
<p>React Native는 React 문법을 그대로 사용할 수 있어 UI 개발 부분에서는<br />진입 장벽이 낮은 편이지만,<br />앱 개발 과정에서는 여전히 <strong>네이티브 코드(Swift, Java/Kotlin)</strong> 와<br />연동해야 하는 기능들이 존재합니다.<br />따라서 기본적인 네이티브 개발 구조와 개념 역시 학습할 필요가 있다고 합니다.</p>
<p>두렵기도 하지만, 어차피 React 개발자로서 모바일 앱 개발을 한다면<br />언젠가는 반드시 거쳐야 하는 관문이라고 생각했습니다.<br />차라리 이번 기회를 ** 럭키비키** 라고 받아들이며<br />앞으로 React Native 학습을 본격적으로 시작해보고자 합니다.</p>
<hr />
<h2 id="💡-궁금증">💡 궁금증</h2>
<p>저는 예전에는 <strong>Ionic(Angular 조합)으로 웹앱을 개발한 경험</strong>이 있습니다.<br />Ionic은 웹 기술로 앱을 만들 수 있을 뿐만 아니라 자체적인 <strong>모바일 UI 프레임워크</strong>도 제공하기 때문에,<br />당시에는 Angular + Ionic 조합으로 웹앱과 앱 형태의 프로젝트를 빠르게 만들 수 있었습니다.</p>
<p>그래서 자연스럽게  </p>
<ul>
<li>“React Native는 Ionic과 무엇이 다른지?”  </li>
<li>“React로는 앱을 만들 수 없는지?”  </li>
<li>“왜 모바일 앱 개발은 React Native를 사용하는지?”<br />와 같은 궁금증이 생겼습니다.</li>
</ul>
<p>특히 <strong>React, Ionic(하이브리드 앱), React Native(네이티브 앱)</strong> 의 차이를<br />정확히 이해하는 것이 전체적인 기술 방향을 잡는 데 중요하다고 판단하여<br />먼저 개념을 정리하고 학습을 이어가려 합니다.</p>
<p>또한,<br />React Native는 <strong>웹을 기본적으로 대응하지 못한다</strong>는 이야기를 들었고,<br />그렇다면 “Ionic처럼 웹과 앱을 동시에 만들 수는 없는지?”도 궁금했습니다.</p>
<p>아래에서는 이러한 궁금증을 해결하기 위해<br /><strong>Ionic / Capacitor / Cordova / React Native</strong> 개념을 정리하고<br />“웹앱을 앱으로 감싸는 방식”이 무엇인지도 설명하고자 합니다.</p>
<hr />
<h2 id="✔-1-웹앱을-앱으로-감싸는-방식이란">✔ 1. 웹앱을 앱으로 감싸는 방식이란?</h2>
<p>Ionic을 이해하기 위해 먼저 알아야 하는 개념입니다.</p>
<p>웹앱을 앱으로 감싸는 방식이란 쉽게 말해:</p>
<pre><code class="language-text">   [네이티브 앱 껍데기]
          ↓
      WebView
          ↓
   웹앱(React, Vue 등)
</code></pre>
<img height="30" src="https://velog.velcdn.com/images/sunmins/post/a4318591-0868-4b64-a407-a77f98e624e8/image.png" width="30%" />


<p>즉, 네이티브 앱 하나를 만들고,<br />그 안에서 <strong>WebView(브라우저 같은 창)</strong> 를 띄워<br />내가 만든 웹앱의 URL 또는 빌드 파일을 넣는 방식입니다.</p>
<p>이렇게 하면 웹앱이 “앱처럼 보이도록” 만들 수 있고,<br />그 결과를 앱스토어에 배포할 수 있습니다.</p>
<p>이런 구조를 가능하게 해주는 기술이 바로 <strong>Cordova</strong>와 <strong>Capacitor</strong> 입니다.</p>
<blockquote>
<h3 id="webview">WebView:</h3>
<p>앱 안에서 웹 페이지를 보여줄수 있게 하는 &quot;작은 브라우저&quot;
OS가 제공하는 브라우저 렌더링 엔진</p>
</blockquote>
<hr />
<h2 id="2-⚙-cordova와-capacitor란">2. ⚙ Cordova와 Capacitor란?</h2>
<h3 id="🔧-cordova">🔧 Cordova</h3>
<ul>
<li>하이브리드 앱을 만들기 위한 <strong>가장 오래된 플랫폼</strong>  </li>
<li>웹앱을 WebView로 감싸서 앱스토어에 올릴 수 있게 해줌  </li>
<li>카메라, GPS 같은 네이티브 기능은 Cordova 플러그인을 통해 사용  </li>
<li>Ionic 1세대는 Cordova 기반으로 동작</li>
</ul>
<h3 id="⚡-capacitor">⚡ Capacitor</h3>
<ul>
<li>Cordova 이후 등장한 <strong>모던한 대체 기술</strong>  </li>
<li>Ionic 팀이 직접 개발  </li>
<li>웹앱을 앱으로 감싸는 구조는 동일하지만<ul>
<li>더 빠르고</li>
<li>네이티브 SDK와의 연동도 쉬움</li>
<li>플러그인 작성도 깔끔함  </li>
</ul>
</li>
<li>최근 Ionic 기반 앱은 거의 모두 Capacitor 사용</li>
</ul>
<p>즉,</p>
<p>Cordova = 구세대 WebView 기반 앱 플랫폼<br /><strong>Capacitor = Cordova의 개선판, Ionic 최신 버전의 표준</strong></p>
<blockquote>
<h4 id="플랫폼">플랫폼:</h4>
<p>앱을 실행할 수 있는 환경 + 그 환경에서 동작하도록 만들어주는 개발 도구 세트</p>
</blockquote>
<hr />
<h2 id="3-✔-ionic과-react-native의-차이">3. ✔ Ionic과 React Native의 차이</h2>
<p>React Native를 배우기 전에, 과거에 사용했던 Ionic과 비교하여<br />두 기술의 구조적 차이를 정리 했습니다.</p>
<h3 id="3-1-🌐-ionic">3-1. 🌐 Ionic</h3>
<ul>
<li>웹 기술(HTML, CSS, JavaScript)로 UI를 개발  </li>
<li>앱 내부에서 <strong>WebView</strong>를 띄워 웹앱을 실행  </li>
<li>웹앱을 네이티브 앱처럼 보이게 감싸는 <strong>하이브리드 앱 방식</strong>  </li>
<li>장점:** Web + Android + iOS 동시 대응**이 쉬움  </li>
<li>단점: 성능이 WebView 기반 → *<em>네이티브보다 느릴 수 있음  *</em></li>
<li>사용 기술: Ionic UI + Capacitor(또는 Cordova)</li>
<li><strong>추가로</strong>, Ionic은 자체적인 <strong>UI 프레임워크(모바일 UI 컴포넌트)</strong> 를 제공해<br />하나의 코드로 <strong>웹/앱/iOS/Android에서 각각 플랫폼에 맞는 스타일과 동작이 자동 적용</strong>됨  
→ &quot;한 UI로 여러 플랫폼&quot;에 최적화된 구조</li>
</ul>
<h3 id="3-2-📱-react-native">3-2. 📱 React Native</h3>
<ul>
<li>React 문법 사용  </li>
<li>렌더링은 <strong>웹 UI가 아니라 네이티브 UI 컴포넌트</strong>  </li>
<li>결과물은 웹뷰가 아니라 <strong>진짜 네이티브 앱</strong>  </li>
<li>네이티브 기능은 Bridge로 직접 접근  </li>
<li>장점: 성능, UX 모두 네이티브에 가까움</li>
<li><strong>네이티브 앱이면서 크로스 플랫폼 앱</strong><br />  → 한 번의 코드로 Android + iOS 모두 개발 가능  </li>
<li>단점: 기본적으로 <strong>웹 대응 불가</strong>,  
 Ionic과 달리 <strong>UI 프레임워크가 기본 제공되지 않고</strong><br />플랫폼별 스타일을 개발자가 직접 맞추거나<br />다양한 서드파티 UI 라이브러리를 사용해야 함<ul>
<li>단, <em>React Native Web</em>을 사용하면 대응 가능하지만 Ionic처럼 완전 동일한 코드는 아님</li>
</ul>
</li>
</ul>
<blockquote>
<h3 id="브리지bridge"><strong>브리지(Bridge)</strong></h3>
</blockquote>
<ul>
<li>JavaScript 코드(React Native)와 네이티브 코드(Swift·Kotlin)를 연결해주는 통신 다리
React Native 앱은 두 가지 세계로 구성:<ol>
<li>JavaScript 세계 (React 코드)</li>
<li>Native 세계 (iOS Swift / Android Kotlin)
이 둘은 서로 말이 다름 (언어도 다르고 환경도 다름) 그래서 <strong>서로 데이터를 주고받을 통역사(Bridge)</strong> 가 필요</li>
</ol>
</li>
</ul>
<blockquote>
<h3 id="크로스-플랫폼cross-platform"><strong>크로스 플랫폼(Cross-Platform)</strong></h3>
</blockquote>
<ul>
<li>하나의 코드로 Android + iOS 모두 개발 가능  </li>
<li>대표 기술: <strong>React Native, Flutter, Unity</strong>  </li>
<li><strong>네이티브 앱 수준의 성능</strong> 제공  </li>
<li>구조는 네이티브 기반이지만 여러 플랫폼을 동시에 지원하는 방식  </li>
</ul>
<blockquote>
<h3 id="하이브리드-앱hybrid-app"><strong>하이브리드 앱(Hybrid App)</strong></h3>
</blockquote>
<ul>
<li>웹 기술(HTML/CSS/JS)로 만든 웹앱을 WebView로 감싸는 방식  </li>
<li>대표 기술: <strong>Ionic, Cordova, Capacitor 기반 앱</strong>  </li>
<li>웹 기반 + 네이티브 껍데기 = Hybrid  </li>
<li>빠르게 Web + App 만들 수 있으나 성능은 네이티브보다 낮을 수 있음</li>
</ul>
<h3 id="정리">정리:</h3>
<p><strong>Ionic = 웹앱을 앱처럼 감싸는 하이브리드 앱</strong><br /><strong>React Native = 네이티브 UI로 동작하는 실제 모바일 앱</strong></p>
<hr />
<h2 id="4❓-react-native로는-웹-대응이-가능한가">4.❓ React Native로는 웹 대응이 가능한가?</h2>
<p><strong>기본적으로는 안 됩니다.</strong></p>
<p>React Native는 웹 기술이 아니라 네이티브 UI를 렌더링하기 때문에<br />웹 브라우저는 그걸 이해하지 못합니다.</p>
<p>하지만 예외적으로:</p>
<ul>
<li><strong>React Native Web</strong></li>
<li><strong>Expo Web</strong></li>
<li><strong>Next.js + React Native Web</strong></li>
</ul>
<p>같은 조합을 사용하면 웹 대응이 가능합니다.</p>
<p>다만 Ionic처럼 “한 코드로 웹 + 앱 완벽 대응”은 어렵고,<br />추가 세팅과 코드 분리가 어느 정도 필요합니다.</p>
<hr />
<h2 id="💬-결론">💬 결론</h2>
<p>React 개발자로서 모바일 앱 개발을 해야 한다면,<br /><strong>React Native는 가장 자연스럽고 쉬운 선택지</strong>라고 생각합니다.<br />회사 입장에서도 Android 개발자와 iOS 개발자를 각각 두는 것보다,<br />하나의 코드베이스로 두 플랫폼을 모두 커버할 수 있는<br />이런 <strong>크로스 플랫폼</strong> 앱 개발 방식을 더 선호하는 추세인 것 같습니다.</p>
<p>웹 기술을 그대로 앱에 포장하는 Ionic 방식도 분명한 장점이 있지만,<br />실제 서비스 <strong>품질, 성능, 확장성, 유지보수</strong>와 같은 실무 요소를 고려하면<br /><strong>React Native가 훨씬 안정적이고, 업계에서도 널리 사용되는 표준 기술</strong>이라고 합니다.</p>
<p>이러한 점들을 종합적으로 고려해볼 때,<br />React 개발자인 저에게 React Native는 가장 적합한 모바일 개발 기술이라 판단되어
앞으로 본격적으로 학습을 진행해보려고 합니다. 렛츠고 ~</p>