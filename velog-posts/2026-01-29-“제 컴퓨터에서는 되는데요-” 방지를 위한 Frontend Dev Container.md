<p>개발을 하다 보면 이런 말을 자주 하고 들을수 있습니다..</p>
<blockquote>
<p>제 컴퓨터에서는 되는데요??</p>
</blockquote>
<p>이런 문제가 발생하는 이유는 보통 개발자마다 아래 환경이 다르기 때문입니다.</p>
<ul>
<li>Node.js 버전 차이</li>
<li>라이브러리 설치 상태 차이</li>
<li>VS Code 확장 프로그램 차이</li>
<li>OS 설정 차이</li>
</ul>
<p>이런 문제를 줄이기 위해<br /><strong>VS Code Dev Container 기반으로 개발 환경을 표준화</strong>하는 방법을 정리했습니다.
Dev Container를 사용하면 개발자가 모두 동일한 환경에서 프로젝트를 실행할 수 있습니다.</p>
<hr />
<h2 id="✅-사전-준비">✅ 사전 준비</h2>
<p>Dev Container는 Docker 기반으로 동작하므로 아래 설치가 필요합니다.</p>
<ul>
<li>Docker Desktop 설치</li>
<li>VS Code Dev Containers 확장 설치</li>
</ul>
<p>저는 Windows 환경 기준으로 설명합니다.</p>
<hr />
<h2 id="1-docker-desktop-설치">1) Docker Desktop 설치</h2>
<p>Dev Container는 컨테이너 환경에서 실행되기 때문에<br />먼저 Docker Desktop 설치가 필요합니다.</p>
<hr />
<h3 id="windows-edition-확인하기">Windows Edition 확인하기</h3>
<p>Windows는 에디션에 따라 Docker 실행 방식이 달라집니다.</p>
<table>
<thead>
<tr>
<th>에디션</th>
<th>지원 방식</th>
</tr>
</thead>
<tbody><tr>
<td>Windows Pro / Enterprise / Education</td>
<td>Hyper-V 또는 WSL2 가능</td>
</tr>
<tr>
<td>Windows Home</td>
<td>WSL2 필수</td>
</tr>
</tbody></table>
<hr />
<h3 id="wsl2-기반-엔진-vs-hyper-v-기반-엔진">WSL2 기반 엔진 vs Hyper-V 기반 엔진</h3>
<h4 id="✅-wsl2-기반-엔진">✅ WSL2 기반 엔진</h4>
<ul>
<li>Windows Subsystem for Linux 2를 활용</li>
<li>가볍고 성능이 좋음</li>
<li>Windows Home에서도 사용 가능</li>
</ul>
<h4 id="✅-hyper-v-기반-엔진">✅ Hyper-V 기반 엔진</h4>
<ul>
<li>Windows의 가상화 기술(Hyper-V)을 활용</li>
<li>Pro 이상에서만 사용 가능</li>
</ul>
<p>요즘은 대부분 <strong>WSL2 기반 엔진을 권장</strong>합니다.</p>
<hr />
<h3 id="docker-desktop-다운로드">Docker Desktop 다운로드</h3>
<p>공식 사이트에서 설치합니다.</p>
<p><a href="https://www.docker.com/products/docker-desktop/">https://www.docker.com/products/docker-desktop/</a></p>
<p>Download for Windows 클릭 후 설치하면 됩니다.</p>
<hr />
<h3 id="docker-설정-확인">Docker 설정 확인</h3>
<p>Docker Desktop 실행 후 설정에서 아래 옵션이 체크되어 있는지 확인합니다.</p>
<h4 id="settings-→-general">Settings → General</h4>
<ul>
<li>Use the WSL 2 based engine 체크</li>
</ul>
<h4 id="settings-→-resources-→-wsl-integration">Settings → Resources → WSL Integration</h4>
<ul>
<li>Enable integration with my default WSL distro 체크</li>
</ul>
<p>설정 후 Apply &amp; Restart 버튼을 눌러줍니다.</p>
<blockquote>
<p>참고 블로그<br /><a href="https://m.blog.naver.com/islove8587/223434132894">https://m.blog.naver.com/islove8587/223434132894</a></p>
</blockquote>
<hr />
<h2 id="2-vs-code-dev-containers-확장-설치">2) VS Code Dev Containers 확장 설치</h2>
<p>이제 Docker를 VS Code에서 사용하기 위해 확장 프로그램을 설치합니다.</p>
<p>확장 검색창에 아래를 입력합니다.</p>
<ul>
<li><strong>Dev Containers</strong></li>
</ul>
<p>설치하면 VS Code에서 컨테이너 기반 개발이 가능해집니다.</p>
<hr />
<h2 id="3-devcontainerjson-생성하기">3) devcontainer.json 생성하기</h2>
<p>Dev Container는 <code>.devcontainer/devcontainer.json</code> 파일로 설정합니다.</p>
<p>자동 생성 방법은 다음과 같습니다.</p>
<hr />
<h3 id="설정-파일-자동-생성">설정 파일 자동 생성</h3>
<ol>
<li><code>Ctrl + Shift + P</code> 실행  </li>
<li><code>Dev Containers: Add Dev Container Configuration Files</code> 선택  </li>
<li><code>Add configuration to workspace</code> 선택  </li>
<li>개발 환경 선택 (예: Node.js &amp; TypeScript)  </li>
<li>이미지 선택 (예: bookworm)</li>
</ol>
<p>그러면 아래 파일이 생성됩니다.</p>
<hr />
<h3 id="기본-devcontainerjson-예시">기본 devcontainer.json 예시</h3>
<pre><code class="language-json">{
  &quot;name&quot;: &quot;Node.js &amp; TypeScript&quot;,
  &quot;image&quot;: &quot;mcr.microsoft.com/devcontainers/typescript-node:1-24-bookworm&quot;
}</code></pre>
<hr />
<h2 id="4-실제-프로젝트용-설정-예시">4) 실제 프로젝트용 설정 예시</h2>
<p>저는 아래처럼 Node 버전 고정 + 확장 자동 설치까지 설정했습니다.</p>
<pre><code class="language-json">{
  &quot;name&quot;: &quot;Node.js &amp; TypeScript&quot;,

  &quot;image&quot;: &quot;mcr.microsoft.com/devcontainers/typescript-node:1-22-bookworm&quot;,

  &quot;features&quot;: {
    &quot;ghcr.io/devcontainers/features/node:1&quot;: {
      &quot;version&quot;: &quot;22&quot;
    }
  },

  &quot;postCreateCommand&quot;: &quot;yarn install&quot;,

  &quot;customizations&quot;: {
    &quot;vscode&quot;: {
      &quot;extensions&quot;: [
        &quot;esbenp.prettier-vscode&quot;,
        &quot;dbaeumer.vscode-eslint&quot;,
        &quot;eamodio.gitlens&quot;,
        &quot;orta.vscode-jest&quot;,
        &quot;vitest.explorer&quot;,
        &quot;styled-components.vscode-styled-components&quot;
      ],
      &quot;settings&quot;: {
        &quot;typescript.tsdk&quot;: &quot;node_modules/typescript/lib&quot;
      }
    }
  }
}</code></pre>
<h3 id="dev-container-설정-항목-설명">Dev Container 설정 항목 설명</h3>
<h4 id="✅-name">✅ name</h4>
<p>Dev Container 이름입니다.<br />VS Code에서 컨테이너를 구분할 때 표시됩니다.</p>
<hr />
<h4 id="✅-image">✅ image</h4>
<p>컨테이너에서 사용할 기본 OS + Node 환경입니다.</p>
<p>예:</p>
<ul>
<li>Debian Bookworm 기반  </li>
<li>Node.js 개발 환경 포함  </li>
</ul>
<hr />
<h4 id="✅-features">✅ features</h4>
<p>추가 기능 설치 옵션입니다.<br />여기서는 Node.js 버전을 고정했습니다.</p>
<pre><code class="language-json">&quot;features&quot;: {
  &quot;ghcr.io/devcontainers/features/node:1&quot;: {
    &quot;version&quot;: &quot;22&quot;
  }
}</code></pre>
<p>→ 팀원 모두 동일한 Node 버전을 사용하게 됩니다.</p>
<h4 id="✅-postcreatecommand">✅ postCreateCommand</h4>
<p>컨테이너가 처음 생성될 때 자동 실행되는 명령어입니다.</p>
<pre><code class="language-json">&quot;postCreateCommand&quot;: &quot;yarn install&quot;</code></pre>
<p>컨테이너 생성 후 의존성이 자동 설치됩니다.</p>
<h4 id="✅-customizationsvscodeextensions">✅ customizations.vscode.extensions</h4>
<p>Dev Container 실행 시 자동으로 설치될 VS Code 확장 목록입니다.</p>
<p>→ 개발자마다 확장 차이로 생기는 문제를 줄일 수 있습니다.</p>
<h4 id="✅-customizationsvscodesettings">✅ customizations.vscode.settings</h4>
<p>컨테이너 내부에서 TypeScript 경로를 명확히 지정할 수 있습니다.</p>
<p>&quot;typescript.tsdk&quot;: &quot;node_modules/typescript/lib&quot;</p>
<hr />
<p>그 외의 설정에 대한 설명이 해당 링크에서 확인할수있습니다.</p>
<blockquote>
<p><a href="https://containers.dev/implementors/json_reference/">https://containers.dev/implementors/json_reference/</a></p>
</blockquote>
<hr />
<h2 id="5-dev-container-실행-방법">5) Dev Container 실행 방법</h2>
<p>프로젝트를 VS Code로 연 후</p>
<p><code>Ctrl + Shift + P</code> 실행 → 아래 명령 사용</p>
<hr />
<h3 id="reopen-in-container">Reopen in Container</h3>
<ul>
<li>기존 컨테이너가 있을 때 빠르게 실행</li>
</ul>
<hr />
<h3 id="rebuild-and-reopen-in-container">Rebuild and Reopen in Container</h3>
<ul>
<li>설정을 변경했거나</li>
<li>의존성이 꼬였을 때</li>
<li>컨테이너를 새로 만들고 싶을 때 사용</li>
</ul>
<hr />
<h2 id="6-컨테이너-실행-시-자동-수행되는-작업">6) 컨테이너 실행 시 자동 수행되는 작업</h2>
<p>컨테이너 최초 실행 시 아래가 자동으로 수행됩니다.</p>
<ul>
<li>컨테이너 이미지 다운로드 및 빌드</li>
<li>VS Code 확장 자동 설치</li>
<li><code>yarn install</code> 자동 실행</li>
</ul>
<hr />
<h2 id="7-컨테이너-내부에서-개발-실행">7) 컨테이너 내부에서 개발 실행</h2>
<p>VS Code 터미널에서 실행합니다.</p>
<pre><code class="language-bash">yarn dev</code></pre>
<p>빌드</p>
<pre><code class="language-bash">yarn build</code></pre>
<p>테스트</p>
<pre><code class="language-bash">yarn test</code></pre>
<hr />
<h2 id="⚠️-자주-발생하는-문제">⚠️ 자주 발생하는 문제</h2>
<hr />
<h3 id="docker-desktop이-실행-중인지-확인">Docker Desktop이 실행 중인지 확인</h3>
<p>Dev Container가 실행되지 않으면<br />Docker Desktop이 켜져 있는지 확인합니다.</p>
<hr />
<h3 id="의존성-설치가-꼬였을-때">의존성 설치가 꼬였을 때</h3>
<p>컨테이너를 다시 빌드하면 해결됩니다.</p>
<pre><code class="language-bash">Dev Containers: Rebuild and Reopen</code></pre>
<hr />
<h3 id="사내-vpn-사용-시-설치-무한-로딩">사내 VPN 사용 시 설치 무한 로딩</h3>
<p>VPN 환경에서는 네트워크 연결 문제로<br /><code>yarn install</code>이 무한 대기할 수 있습니다.</p>
<hr />
<h2 id="마무리">마무리</h2>
<p>Dev Container를 사용하면 팀원 모두 동일한 Node 환경과 VS Code 확장 설정을 통일할 수 있습니다.</p>
<p>다만 프론트엔드만 적용하면 Docker의 장점이 크게 체감되지 않을 수 있습니다.<br />Docker는 <code>docker-compose</code>를 통해 프론트, 백엔드 API 서버, DB 등을 함께 구성하고 한 번에 실행할 때 더 큰 효과를 발휘합니다.</p>
<p>다음에는 간단한 예제 형태로라도 DB와 API 서버까지 함께 연결해 구성해보며 Docker의 장점을 더 제대로 활용해볼 예정입니다.</p>