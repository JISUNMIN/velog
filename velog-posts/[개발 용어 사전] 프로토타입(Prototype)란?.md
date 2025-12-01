<p><strong>프로토타입(Prototype)</strong>은  
<strong>“제품이 실제로 어떻게 보이고, 어떻게 동작할지 빠르게 확인하기 위해 만드는 예시 모델”</strong>입니다.<br />완성된 제품이 아니라, <strong>UI/UX 흐름·동작 방식·사용 경험을 미리 보여주기 위한 목적</strong>으로 제작됩니다.</p>
<blockquote>
<p>“기능은 완전하지 않아도 되고,<br />화면과 흐름을 먼저 확인하는 데 집중하는 단계”</p>
</blockquote>
<p>라고 이해할 수 있습니다.</p>
<hr />
<h2 id="💡-왜-프로토타입을-사용할까">💡 왜 프로토타입을 사용할까?</h2>
<h3 id="1-화면·동작-흐름을-빠르게-확인하기-위해">1) 화면·동작 흐름을 빠르게 확인하기 위해</h3>
<p>기획서나 문서만으로는 <strong>사용 흐름</strong>을 이해하기 어렵습니다.<br />프로토타입을 만들면:</p>
<ul>
<li>사용자가 어떤 화면을 거쳐서 이동하는지  </li>
<li>버튼을 누르면 어떤 인터랙션이 일어나는지  </li>
<li>실제로 써보면 어떤 어색한 부분이 있는지  </li>
</ul>
<p>등을 <strong>직접 체감하면서 검증</strong>할 수 있습니다.</p>
<hr />
<h3 id="2-개발-전에-ux-문제를-미리-발견하기-위해">2) 개발 전에 UX 문제를 미리 발견하기 위해</h3>
<p>초기 설계가 잘못되면<br />개발 이후 수정 비용이 폭발적으로 증가합니다.</p>
<p>프로토타입 단계에서 미리 테스트하면:</p>
<ul>
<li>UI 흐름 개선  </li>
<li>인터랙션 문제 발견  </li>
<li>사용자 불편 요소 제거  </li>
</ul>
<p>등을 빠르게 수정할 수 있어 <strong>리스크가 크게 줄어듭니다.</strong></p>
<hr />
<h3 id="3-이해관계자디자인·개발·기획·경영진를-설득하기-위해">3) 이해관계자(디자인·개발·기획·경영진)를 설득하기 위해</h3>
<p>프로토타입은 <strong>보여줄 수 있는 결과물</strong>이기 때문에<br />말로 설명하는 것보다 훨씬 설득력이 높습니다.</p>
<p>예:</p>
<ul>
<li>“이렇게 움직입니다”  </li>
<li>“이 버튼을 누르면 이런 화면으로 넘어갑니다”  </li>
</ul>
<p>이걸 실제로 클릭해보면서 회의하면<br />기획 이해도와 결정 속도가 훨씬 빨라집니다.</p>
<hr />
<h2 id="🔍-프로토타입의-특징">🔍 프로토타입의 특징</h2>
<h3 id="반쯤-작동하거나-일부만-작동해도-된다">반쯤 작동하거나, 일부만 작동해도 된다</h3>
<ul>
<li>전체 기능이 없어도 괜찮음  </li>
<li>실제 API 연결 없이 더미 데이터로도 충분  </li>
</ul>
<p>목적은 <strong>“사용 흐름을 보여주는 것”</strong>이지<br />기능 구현이 아닙니다.</p>
<h3 id="완성도보다-속도가-중요하다">완성도보다 속도가 중요하다</h3>
<ul>
<li>빠르게 만들고  </li>
<li>빠르게 테스트하고  </li>
<li>빠르게 수정하는 단계  </li>
</ul>
<p>그래서 <a href="https://www.figma.com/ko-kr/prototyping/">Figma</a>, <a href="https://www.protopie.io/?utm_source=google&amp;utm_medium=cpc&amp;utm_term=&amp;utm_campaign=ss-bf25-performancemax&amp;gad_source=1&amp;gad_campaignid=23211980367&amp;gbraid=0AAAAADdUE4Qda6GKyN75xkaRffcnMLH1U&amp;gclid=CjwKCAiA55rJBhByEiwAFkY1QAmEYIHonc8nlchtJxpBKcAAm_GnVvz8YE4HVqFLHiHzxpiZdO_n2RoCG2cQAvD_BwE">ProtoPie</a>, <a href="https://www.framer.com/">Framer</a> 같은 툴이 자주 사용됩니다.</p>
<h3 id="최종-제품과-100-일치할-필요-없음">최종 제품과 100% 일치할 필요 없음</h3>
<ul>
<li>디자인 방향성  </li>
<li>UX 흐름  </li>
<li>인터랙션 느낌  </li>
</ul>
<p>정도만 확인하면 됩니다.</p>
<h3 id="프로토타입은-보통-코드-없이-만든다">프로토타입은 보통 코드 없이 만든다</h3>
<p>프로토타입은 <strong>화면 흐름과 사용 경험을 빠르게 확인하는 것이 목적</strong>이기 때문에<br />대부분 Figma, ProtoPie, Framer 같은 도구로 <strong>코드 없이 제작</strong>합니다.<br />기능이 완전하지 않아도 되고, 클릭 흐름과 인터랙션만 보여줘도 충분합니다.</p>
<p>다만, <strong>성능·센서·실시간 반응 같은 기술적 특성을 검증해야 하는 경우</strong>에는<br />일부 기능만 넣은 <strong>코드 기반 프로토타입</strong>을 만들기도 합니다.</p>
<hr />
<h2 id="📱-프로토타입-예시">📱 프로토타입 예시</h2>
<h3 id="✔️-figma로-만드는-클릭형-화면-흐름">✔️ Figma로 만드는 클릭형 화면 흐름</h3>
<p>버튼을 누르면 다른 화면으로 넘어가는 형태로<br />전체 서비스 흐름을 재현 → <strong>프로토타입</strong></p>
<h3 id="✔️-더미-데이터를-넣어-만든-반쯤-완성된-데모-앱">✔️ 더미 데이터를 넣어 만든 반쯤 완성된 데모 앱</h3>
<p>실제 기능은 없지만<br />화면 이동과 버튼 동작은 구현된 버전 → <strong>프로토타입</strong></p>
<h3 id="✔️-경영진-설득용-인터랙션-데모">✔️ 경영진 설득용 인터랙션 데모</h3>
<p>애니메이션·전환 효과만 보여주기 위한 화면 → <strong>프로토타입</strong></p>
<hr />
<h2 id="📌-한-줄-요약">📌 한 줄 요약</h2>
<blockquote>
<p><strong>프로토타입은 제품의 ‘모양·흐름·사용 경험’을 빠르게 확인하고 검증하기 위해 만드는<br />가벼운 예시 모델이다.</strong></p>
</blockquote>