<p><strong>CI/CD</strong>는 <strong>개발한 코드를 자동으로 빌드·테스트하고, 안정적으로 배포하기 위한 자동화 파이프라인</strong>을 의미합니다.</p>
<ul>
<li>CI → Continuous Integration (지속적 통합)  </li>
<li>CD → Continuous Delivery/Deployment (지속적 제공·지속적 배포)</li>
</ul>
<blockquote>
<p>“개발에서 배포까지 반복되는 작업을 자동화하여<br />빠르고 안정적으로 제품을 출시하는 방식”</p>
</blockquote>
<p>이라고 이해할 수 있습니다.</p>
<hr />
<h2 id="💡-왜-cicd가-필요할까">💡 왜 CI/CD가 필요할까?</h2>
<h3 id="1-사람이-하는-반복-작업을-자동으로-처리하기-위해">1) 사람이 하는 반복 작업을 자동으로 처리하기 위해</h3>
<p>빌드 → 테스트 → 배포 과정을<br />사람이 직접 하면:</p>
<ul>
<li>시간 오래 걸리고  </li>
<li>오류가 자주 발생하며  </li>
<li>팀원마다 방식이 달라서 혼란이 생김</li>
<li>환경 차이 때문에 로컬/서버 결과가 달라질 수 있음</li>
</ul>
<p>CI/CD를 적용하면:</p>
<ul>
<li>코드 push만 해도 자동 빌드  </li>
<li>작성해둔 테스트가 자동 실행되어 버그를 빠르게 발견  </li>
<li>배포 과정도 자동화되어 실수 없이 안정적으로 배포 가능</li>
</ul>
<p>➡ <strong>반복 작업을 자동화하여 개발 효율을 극대화</strong>합니다.</p>
<hr />
<h3 id="2-더-빠른-배포를-위해">2) 더 빠른 배포를 위해</h3>
<p>CI/CD가 없으면 배포가 느린 이유는<br />“개발자가 못 해서”가 아니라<br /><strong>사람이 해야 하는 절차가 많고, 그 과정마다 ‘대기 시간’이 생기기 때문</strong>입니다.</p>
<p>CI/CD가 없을 때는:</p>
<ul>
<li>개발자가 로컬에서 빌드  </li>
<li>개발자 수동 테스트  </li>
<li>테스트용 앱/서버를 QA팀에게 전달  </li>
<li>QA팀이 스테이징 환경에서 수동 테스트  </li>
<li>리뷰·병합 과정 대기  </li>
<li>운영팀이 프로덕션 배포 일정 맞춰 수동 배포<br />→ 모든 과정이 사람이 직접 움직여야 하므로 순차적으로만 진행됨<br />→ <strong>대기 시간이 계속 쌓여 며칠~몇 주가 걸리는 구조</strong></li>
</ul>
<p>⭐ CI/CD가 있으면:</p>
<ul>
<li>코드 commit → 자동 빌드  </li>
<li>자동 테스트로 기본 오류 즉시 발견  </li>
<li>자동으로 <strong>스테이징(QA) 환경</strong>에 배포되어 QA·기획자가 바로 검증 가능  </li>
<li>수동 테스트는 핵심 UX/기획 흐름 확인 정도로 축소  </li>
<li>스테이징에서 검증이 끝나면, <strong>사람이 배포 승인만 하면</strong> 프로덕션(prod) 배포는 CI/CD가 자동 처리<br />→ 사람의 대기 시간이 거의 사라짐<br />→ <strong>하루에도 여러 번 안정적으로 배포 가능</strong></li>
</ul>
<p>➡ <strong>빠른 사이클의 제품 개발에 필수적인 시스템</strong></p>
<blockquote>
<p><strong>스테이징(Staging) 환경</strong>: 스테이징은 개발(dev)과 운영(prod) 사이에 존재하는 <strong>중간 검증용 환경</strong>입니다.</p>
<p>일반적인 구성은 다음과 같습니다:
개발(dev) → 스테이징(staging / QA) → 운영(prod)
각 환경의 역할은 다음과 같습니다:</p>
<ul>
<li><strong>dev</strong><br />개발자가 로컬 또는 개발 서버에서 기능을 만들고 테스트하는 단계  </li>
<li><strong>staging(QA)</strong><br />운영(prod) 환경과 거의 동일하게 구성된 테스트용 환경 
QA, 기획, PM이 실제 사용자처럼 테스트하는 공간<br />UI/UX, 기획 흐름, 디바이스 테스트 등 <strong>사람이 직접 확인해야 하는 영역</strong>을 검증  </li>
<li><strong>prod</strong><br />실제 사용자가 쓰는 운영 환경
즉,   <strong>스테이징은 “운영 직전 모든 것을 최종 검증하는 안전한 중간 단계”입니다.</strong></li>
</ul>
</blockquote>
<hr />
<h3 id="3-팀-협업을-안정적으로-만들기-위해">3) 팀 협업을 안정적으로 만들기 위해</h3>
<p>여러 사람이 코드를 수정하면 문제가 생길 수 있지만<br />CI/CD는 이를 해결해줍니다.</p>
<p>자동으로:</p>
<ul>
<li>코드 스타일 체크  </li>
<li>테스트 실행  </li>
<li>품질 검증  </li>
<li>병합 전 문제 감지</li>
<li>환경을 통일된 상태로 유지  </li>
</ul>
<p>➡ <strong>협업 품질이 올라가고 코드 충돌이 줄어든다.</strong></p>
<hr />
<h2 id="cicd가-있으면-수동-테스트는-안-해도-될까">“CI/CD가 있으면 수동 테스트는 안 해도 될까?”</h2>
<p>아닙니다. 
<strong>CI/CD가 생긴다고 해서 개발자·QA의 수동 테스트가 사라지는 것은 아닙니다.</strong></p>
<p>CI/CD는:</p>
<ul>
<li>반복적인 유닛 테스트  </li>
<li>기본적인 리그레션 테스트  </li>
<li>빌드 안정성 체크  </li>
<li>자동 클릭 기반 E2E 테스트  </li>
</ul>
<blockquote>
<p>리그레션 테스트(Regression Test): 이전까지 잘 동작하던 기능이, 새로운 코드 때문에 망가지지 않았는지 확인하는 테스트</p>
</blockquote>
<blockquote>
<p>E2E테스트(End-to-End Test): 실제 사용자가 앱/웹을 사용 하는 것처럼 처음부터 끝까지 자동으로 실행하는 테스트
예시) </p>
</blockquote>
<ol>
<li>앱을 킨다</li>
<li>로그인 버튼 클릭</li>
<li>ID/PW 입력</li>
<li>홈으로 이동</li>
<li>장바구니에 상품 추가</li>
<li>결제 버튼 클릭</li>
<li>완료 페이지 표시되는지 확인</li>
</ol>
<p>등을 자동화해줄 뿐이고,</p>
<p>여전히 사람이 해야 하는 테스트가 존재합니다:</p>
<ul>
<li>UI/UX 자연스러운지 확인  </li>
<li>기획 의도와 맞는지  </li>
<li>신규 기능 흐름 검증  </li>
<li>여러 디바이스 감각 테스트  </li>
</ul>
<p>➡ <strong>CI/CD는 수동 테스트를 없애는 도구가 아니라,<br />반복적인 테스트를 자동화해 ‘사람이 해야 하는 테스트 범위를 줄여주는’도구입니다.</strong></p>
<hr />
<h2 id="🔍-ci와-cd는-어떻게-다를까">🔍 CI와 CD는 어떻게 다를까?</h2>
<h3 id="ci-지속적-통합--continuous-integration">CI (지속적 통합 / Continuous Integration)</h3>
<p>개발자가 코드를 push하면:</p>
<ul>
<li>자동 빌드  </li>
<li>자동 테스트  </li>
<li>자동 코드 품질 검사  </li>
<li>문제 있으면 즉시 알림  </li>
</ul>
<p>→ <strong>“코드를 팀 저장소에 안전하게 합치는 과정 자체를 자동화하는 단계”</strong></p>
<hr />
<h3 id="cd-지속적-배포--continuous-deployment-or-delivery">CD (지속적 배포 / Continuous Deployment or Delivery)</h3>
<p>CD는 “배포” 단계의 자동화 수준에 따라 두 가지 형태로 나뉩니다.</p>
<h4 id="continuous-delivery"><strong>Continuous Delivery</strong></h4>
<ul>
<li>자동 빌드 + 자동 테스트  </li>
<li>자동으로 <strong>스테이징(QA) 환경까지 배포</strong>  </li>
<li>QA·기획자가 스테이징에서 검증  </li>
<li><strong>운영(prod) 배포는 사람이 승인 버튼을 눌러 진행</strong><br />→ 가장 널리 사용되는 방식 (안전성 높음)</li>
</ul>
<h4 id="continuous-deployment"><strong>Continuous Deployment</strong></h4>
<ul>
<li>자동 빌드 + 자동 테스트  </li>
<li><strong>스테이징 배포 → 테스트 → 운영(prod) 배포까지 모두 자동</strong>  </li>
<li>수동 검증 단계 없이, 자동화 테스트와 모니터링이 통과되면 바로 prod에 배포<br />→ 테스트 자동화 수준이 높은 팀에서만 가능 (완전 자동 배포)</li>
</ul>
<p>→ <strong>“코드를 사용자에게 전달하는 준비/배포 과정을 자동화하는 단계”</strong></p>
<hr />
<h2 id="🧰-cicd에서-자주-사용되는-도구">🧰 CI/CD에서 자주 사용되는 도구</h2>
<h3 id="🌐-웹-프론트엔드">🌐 웹 프론트엔드</h3>
<ul>
<li><strong>GitHub Actions</strong> — 범용 CI/CD, 모든 프론트엔드에서 사용</li>
<li><strong>Vercel</strong> — Next.js·React 배포에 특화</li>
<li><strong>Netlify</strong> — 정적 사이트·SPA 자동 배포</li>
</ul>
<h3 id="📱-모바일-앱-react-native--ios--android">📱 모바일 앱 (React Native / iOS / Android)</h3>
<ul>
<li><strong>GitHub Actions</strong> — fastlane·EAS와 조합하여 모바일 빌드/배포 자동화</li>
<li><strong>Bitrise</strong> — 모바일 전용 CI/CD 플랫폼(가장 많이 사용)</li>
<li><strong>Expo EAS</strong> — Expo 프로젝트 전용 빌드·배포</li>
<li><strong>fastlane</strong> — iOS/Android 자동 배포 스크립트 표준</li>
</ul>
<h3 id="🖥-백엔드--서버">🖥 백엔드 / 서버</h3>
<ul>
<li><strong>GitHub Actions</strong> — 서버 테스트·도커 빌드·AWS 배포 자동화</li>
<li><strong>GitLab CI/CD</strong> — 기업에서 많이 쓰는 통합 솔루션</li>
<li><strong>Jenkins</strong> — 가장 오래된 커스텀형 CI/CD 도구</li>
</ul>
<hr />
<h2 id="📱-cicd-예시">📱 CI/CD 예시</h2>
<h3 id="✔-github-actions">✔ GitHub Actions</h3>
<p>코드를 push하면 자동으로:</p>
<ul>
<li>npm install  </li>
<li>테스트 실행  </li>
<li>lint 체크  </li>
<li>빌드  </li>
<li>Vercel, AWS ,S3등에 자동 배포  </li>
</ul>
<p>단, 이 모든 흐름은 <code>.github/workflows/*.yml</code> 파일에 <strong>개발자가 미리 작성한 스크립트</strong>가 있어야만 동작합니다.
즉, <strong>자동 배포가 아니라 “미리 정의한 작업을 GitHub가 자동으로 실행해주는 구조”</strong>입니다.</p>
<h3 id="✔-모바일-앱react-native에서의-cicd-활용-예시">✔ 모바일 앱(React Native)에서의 CI/CD 활용 예시</h3>
<ul>
<li>PR을 올리면 <strong>Expo EAS/Bitrise</strong>가 자동으로 빌드  </li>
<li>테스트 및 에러 여부 자동 검사  </li>
<li>빌드 성공 시 테스터에게 설치 가능한 beta 파일(IPA/APK) 자동 배포  </li>
</ul>
<h3 id="✔-jenkins젠킨스">✔ Jenkins(젠킨스)</h3>
<p>Jenkins는 <strong>가장 오래되고 강력한 CI/CD 서버 도구</strong>입니다.</p>
<ul>
<li>회사 내부 서버에 설치해서 사용  </li>
<li>Git push → Jenkins가 자동으로 빌드/테스트/배포  </li>
<li>스크립트(파이프라인)로 원하는 작업을 모두 커스터마이징 가능  </li>
<li>GitHub Actions처럼 YAML을 쓰기도 하고, UI로 단계 구성도 가능  </li>
</ul>
<p>→ <strong>대규모 서비스나 자체 인프라를 운영하는 기업에서 많이 사용하는 CI/CD 툴</strong></p>
<hr />
<h2 id="📌-한-줄-요약">📌 한 줄 요약</h2>
<blockquote>
<p><strong>CI/CD는 반복되는 빌드·테스트·배포를 자동화해 
빠르고 안정적으로 제품을 제공할 수 있게 만드는 핵심 개발 시스템이다.</strong></p>
</blockquote>