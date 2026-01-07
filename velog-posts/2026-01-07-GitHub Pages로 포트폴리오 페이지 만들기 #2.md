<p><a href="https://velog.io/@sunmins/GitHub-Pages%EB%A1%9C-%ED%8F%AC%ED%8A%B8%ED%8F%B4%EB%A6%AC%EC%98%A4-%ED%8E%98%EC%9D%B4%EC%A7%80-%EB%A7%8C%EB%93%A4%EA%B8%B0-1-zbnfwll9">이전 글</a>에 이어서 이번 글에서는  </p>
<ul>
<li><strong>GitHub Pages에서 이미지 파일을 관리하는 방법</strong></li>
<li><strong>online code editor 대신 VS Code + Live Server를 사용하는 방법</strong></li>
</ul>
<p>을 중심으로 진행해 보겠습니다.</p>
<hr />
<h2 id="1-vs-code-live-server로-html-작성하기">1. VS Code Live Server로 HTML 작성하기</h2>
<p>이전 글에서는<br />online code editor를 사용해 HTML을 작성할 수 있다고 소개했었습니다. </p>
<p>이번에는 <strong>VS Code의 Live Server 확장</strong>을 이용해<br />로컬 환경에서 개발하는 방법을 알아보겠습니다.</p>
<h3 id="1-vs-code에서-새로운-폴더-생성">1) VS Code에서 새로운 폴더 생성</h3>
<p>먼저 작업할 폴더를 하나 생성합니다.<br />이 폴더가 포트폴리오 프로젝트의 루트가 됩니다.</p>
<h3 id="2-indexhtml-파일-생성">2) index.html 파일 생성</h3>
<p>생성한 폴더 안에 <code>index.html</code> 파일을 만들고<br />기본 HTML 구조를 작성합니다.</p>
<pre><code class="language-html">&lt;!DOCTYPE html&gt;
&lt;html lang=&quot;ko&quot;&gt;
&lt;head&gt;
  &lt;meta charset=&quot;UTF-8&quot; /&gt;
  &lt;title&gt;My Portfolio&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
  &lt;h1&gt;Hello Portfolio&lt;/h1&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>
<h3 id="3-live-server-확장-설치">3) Live Server 확장 설치</h3>
<p>VS Code 왼쪽 메뉴에서 <strong>Extensions</strong> 탭으로 이동한 뒤<br /><code>Live Server</code>를 검색해 설치합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/sunmins/post/3376940e-3d91-4983-a89a-d59c7026290e/image.png" /></p>
<h3 id="4-live-server-실행">4) Live Server 실행</h3>
<p><code>index.html</code> 파일을 우클릭한 후<br /><strong>Open with Live Server</strong>를 클릭합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/sunmins/post/82c6ad31-28ad-42bb-ad84-29af5e9e5ba0/image.png" /></p>
<h3 id="5-실행-화면-확인">5) 실행 화면 확인</h3>
<p>브라우저가 자동으로 열리면서<br />작성한 HTML 결과를 바로 확인할 수 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/sunmins/post/547db611-15ae-4202-84e1-2c7e5779af4d/image.png" /></p>
<p>online code editor와 VS Code Live Server 중<br />편한 방식을 선택하시면 됩니다.</p>
<p>저는 online editor 사용 중<br /><strong>자동 포맷이 되지 않는 점이 불편해서</strong><br />VS Code 환경으로 변경해 개발을 진행했습니다.</p>
<hr />
<h2 id="2-github-pages에-이미지-파일-추가하기">2. GitHub Pages에 이미지 파일 추가하기</h2>
<p>이제 포트폴리오에 사용할<br /><strong>이미지 파일을 GitHub Pages에 추가하는 방법</strong>을 알아보겠습니다.</p>
<h3 id="1-your_namegithubio-repository-이동">1) <code>[YOUR_NAME].github.io</code> Repository 이동</h3>
<p>GitHub에서 본인의 Pages Repository로 이동합니다.</p>
<h3 id="2-add-file-→-create-new-file-클릭">2) Add file → Create new file 클릭</h3>
<p>Code 탭에서<br /><strong>Add file → Create new file</strong>을 클릭합니다.</p>
<h3 id="3-폴더-구조-생성">3) 폴더 구조 생성</h3>
<p>파일명 입력창에 <code>/</code>를 사용하면<br />폴더(depth)를 생성할 수 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/sunmins/post/5a20e77b-fe78-4dcc-932f-ba01022e882f/image.png" /></p>
<h3 id="4-commit-change">4) Commit Change</h3>
<p>폴더 생성을 위해 임시 파일을 만든 뒤<br />Commit을 진행합니다.</p>
<h3 id="5-mock-파일-삭제">5) mock 파일 삭제</h3>
<p><code>example.txt</code>는 폴더 생성을 위한 mock 파일이므로<br />생성 후 삭제해 줍니다.</p>
<h3 id="6-이미지-업로드">6) 이미지 업로드</h3>
<p>다시 <strong>Add file → Upload files</strong>를 클릭합니다.</p>
<h3 id="7-이미지-업로드">7) 이미지 업로드</h3>
<p>이미지를 드래그하거나<br />파일 선택을 통해 업로드합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/sunmins/post/7d6142f0-230b-4ac1-b104-9f5ce62ec9c4/image.png" /></p>
<h3 id="8-업로드-확인">8) 업로드 확인</h3>
<p>이미지가 정상적으로 업로드된 것을 확인합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/sunmins/post/65985089-5d2e-418c-9327-3fd6c7d01f97/image.png" /></p>
<h3 id="9-html에서-이미지-경로-지정">9) HTML에서 이미지 경로 지정</h3>
<p>업로드한 경로에 맞게<br /><code>img</code> 태그의 <code>src</code>를 지정해 줍니다.</p>
<pre><code class="language-html">&lt;img src=&quot;assets/images/profile.png&quot; alt=&quot;profile&quot; /&gt;</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/sunmins/post/5a285807-b747-496d-8ae5-5830d1f285e7/image.png" /></p>
<h3 id="10-배포-결과-확인">10) 배포 결과 확인</h3>
<p>Commit 후<br />GitHub Pages 주소로 접속해 결과를 확인합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/sunmins/post/82e94654-526b-4c70-9433-bb0e94b19dec/image.png" /></p>
<blockquote>
<p><strong>참고</strong><br />gif 파일은 움직이는 이미지이기 때문에<br /><code>video</code> 태그가 아닌 <code>img</code> 태그를 사용합니다.</p>
</blockquote>
<hr />
<h2 id="마무리">마무리</h2>
<p>이후 기본 레이아웃이나 구성은<br />각자 원하는 형태로 자유롭게 작성하시면 됩니다.</p>
<p>다음 글에서는 포트폴리오에 적용하면 좋은 <strong>CSS 효과와 간단한 최적화 방법</strong>을 정리해 보겠습니다.<br />스크롤에 따라 텍스트가 자연스럽게 등장하는 애니메이션,<br />hover 시 강조 효과, 카드 UI 스타일링 등<br /><strong>실제로 바로 활용할 수 있는 예시들</strong>을 적용해 볼 예정입니다.</p>