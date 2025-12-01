<p>저번 글에서 Next.js의 CSR · SSR · SSG · ISR을 적용해보고 배포 흐름까지
알아보았습니다.
그런데 정리하다 보니 <strong>&quot;인터랙션은 CSR에서만 가능한데, SSR·SSG·ISR은
실무에서 언제 쓰는 걸까?&quot;</strong> 라는 의문이 생깁니다.</p>
<p>이번 글에서는 <strong>실무에서 어떻게 조합해 사용하는지</strong>,
그리고 <strong>컴포넌트 단위로 렌더링 전략을 선택하는 기준까지</strong> 모두 정리해봤습니다.</p>
<hr />
<h2 id="1-✔-인터랙션onclick-·-usestate-·-useeffect은-csr에서만-가능">1. ✔ 인터랙션(onClick · useState · useEffect)은 CSR에서만 가능</h2>
<p>Next.js(App Router 기준)에서 아래 기능들은 모두 <strong>Client Component(CSR)</strong>에서만 작동합니다.</p>
<ul>
<li>클릭(onClick)</li>
<li>입력(onChange)</li>
<li>상태관리(useState)</li>
<li>사이드이펙트(useEffect)</li>
<li>router.push() 등 클라이언트 라우팅</li>
<li>모달/드롭다운/폼 제출 등 모든 인터랙션</li>
</ul>
<p>즉, <strong>인터랙션 = 100% CSR</strong>
Server Component는 HTML을 만들어줄 뿐, 화면 위 동작은 모두 CSR에서
처리합니다.</p>
<hr />
<h2 id="2-✔-과거에는-페이지-단위로-렌더링-방식을-결정-pages-router">2. ✔ 과거에는 &quot;페이지 단위&quot;로 렌더링 방식을 결정 (Pages Router)</h2>
<p>Next.js 12(Pages Router)에서는 한 페이지에서 오직 하나의 렌더링 방식을
선택해야 했습니다.</p>
<table>
<thead>
<tr>
<th>페이지</th>
<th>렌더링 방식</th>
</tr>
</thead>
<tbody><tr>
<td>/order</td>
<td>SSR</td>
</tr>
<tr>
<td>/blog</td>
<td>SSG</td>
</tr>
<tr>
<td>/cart</td>
<td>SSR</td>
</tr>
</tbody></table>
<h4 id="⚠️-이-방식의-문제점">⚠️ 이 방식의 문제점:</h4>
<ul>
<li>페이지 안의 일부만 CSR/SSR/SSG 조합 불가능</li>
<li>작은 동적 요소 하나 때문에 페이지 전체가 CSR/SSR 처리됨</li>
<li>SEO/성능 최적화가 매우 제한적</li>
</ul>
<hr />
<h2 id="3-✔-현재는-컴포넌트-단위로-ssr-·-ssg-·-isr-·-csr을-조합-app-router">3. ✔ 현재는 &quot;컴포넌트 단위로 SSR · SSG · ISR · CSR을 조합&quot; (App Router)</h2>
<p>App Router의 핵심 철학:</p>
<blockquote>
<p><strong>&quot;렌더링 방식을 페이지 단위가 아니라 컴포넌트 단위로 조합한다.&quot;</strong></p>
</blockquote>
<h4 id="한-페이지-안에서-다음과-같이-조합">한 페이지 안에서 다음과 같이 조합:</h4>
<ul>
<li>상단 UI는 <strong>SSG</strong></li>
<li>중간의 동적 데이터 영역은 <strong>SSR</strong></li>
<li>버튼/입력/이벤트는 <strong>CSR</strong></li>
<li>일부 데이터는 <strong>ISR</strong> (변하지만 빈도 낮은 API)</li>
</ul>
<hr />
<h2 id="4-🏗-실습-주문-상세-페이지-구성하기">4. 🏗 실습: 주문 상세 페이지 구성하기</h2>
<h3 id="구성">구성</h3>
<ul>
<li><p><strong>Header</strong>: 변하지 않음 → <strong>SSG</strong><br />정적 생성 가능, 모든 사용자에게 동일하게 제공</p>
</li>
<li><p><strong>주문 상세 데이터</strong>: 로그인 필요 / 최신 데이터 → <strong>SSR</strong><br />사용자별 최신 데이터를 서버에서 바로 렌더링</p>
</li>
<li><p><strong>주문 확정 버튼</strong>: 클릭/라우팅 → <strong>CSR</strong><br />클라이언트에서 처리되는 사용자 인터랙션</p>
</li>
</ul>
<hr />
<h3 id="🟦-상단-헤더-영역---ssg-static">🟦 상단 헤더 영역 - SSG (Static)</h3>
<pre><code class="language-tsx">// app/order/Header.tsx
export default function OrderHeader() {
  return (
    &lt;header&gt;
      &lt;h1&gt;Order&lt;/h1&gt;
      &lt;p&gt;고객센터 000-0000&lt;/p&gt;
    &lt;/header&gt;
  );
}</code></pre>
<p>✔ 변하지 않는 정적 UI
✔ 빌드 시 생성 → CDN 캐시
✔ SEO에 유리
✔ 매우 빠름</p>
<hr />
<h3 id="🟩-주문-데이터-영역---ssr-server-component">🟩 주문 데이터 영역 - SSR (Server Component)</h3>
<pre><code class="language-tsx">// app/order/[id]/OrderDetail.tsx
import { cookies } from &quot;next/headers&quot;;

export default async function OrderDetail({ id }) {
  const token = cookies().get(&quot;access_token&quot;)?.value;

  // try/catch 생략
  const order = await fetch(`https://example.com/api/orders/${id}`, {
    headers: { Authorization: `Bearer ${token}` },
    cache: &quot;no-store&quot;, // SSR
  }).then(res =&gt; res.json());

  return (
    &lt;section&gt;
      &lt;h2&gt;주문 상세&lt;/h2&gt;
      &lt;p&gt;상품명: {order.productName}&lt;/p&gt;
      &lt;p&gt;가격: {order.totalPrice}&lt;/p&gt;
      &lt;p&gt;배송지: {order.address}&lt;/p&gt;
    &lt;/section&gt;
  );
}</code></pre>
<p>✔ 유저별 데이터 필요
✔ 쿠키 인증 필요
✔ 최신 데이터 필요
✔ 요청마다 새로운 HTML 생성</p>
<hr />
<h3 id="4-3-🟨-주문-확정-버튼---csr-client-component">4-3. 🟨 주문 확정 버튼 - CSR (Client Component)</h3>
<pre><code class="language-tsx">// app/order/[id]/ConfirmOrderButton.tsx
&quot;use client&quot;;

import { useState, useEffect } from &quot;react&quot;;
import { useRouter } from &quot;next/navigation&quot;;

export default function ConfirmOrderButton({ orderId }) {
  const [loading, setLoading] = useState(false);
  const [time, setTime] = useState(&quot;&quot;); // 브라우저 렌더링 시간 표시
  const router = useRouter();

  useEffect(() =&gt; {
    setTime(new Date().toLocaleTimeString());
  }, []);

  const onConfirm = async () =&gt; {
    setLoading(true);
    await fetch(&quot;/api/order/confirm&quot;, {
      method: &quot;POST&quot;,
      headers: { &quot;Content-Type&quot;: &quot;application/json&quot; },
      body: JSON.stringify({ orderId }),
    });
    router.push(&quot;/order/success&quot;);
  };

  return (
    &lt;div&gt;
      &lt;button onClick={onConfirm} disabled={loading}&gt;
        {loading ? &quot;처리 중...&quot; : &quot;주문 확정하기&quot;}
      &lt;/button&gt;
      &lt;p&gt;브라우저 렌더링 시간: {time}&lt;/p&gt;
    &lt;/div&gt;
  );
}</code></pre>
<p>✔ onClick
✔ useState
✔ router.push()
✔ API 호출
-&gt; 인터랙션은 항상 CSR</p>
<hr />
<h3 id="4-4-🧱-전체-페이지-조합-ssg--ssr--csr">4-4. 🧱 전체 페이지 조합 (SSG + SSR + CSR)</h3>
<pre><code class="language-tsx">// app/order/[id]/page.tsx
import Header from &quot;../Header&quot;; 
import OrderDetail from &quot;./OrderDetail&quot;;
import ConfirmOrderButton from &quot;./ConfirmOrderButton&quot;;

export default async function OrderPage({ params }) {
  return (
    &lt;main&gt;
      &lt;Header /&gt;
      &lt;OrderDetail id={params.id} /&gt;
      &lt;ConfirmOrderButton orderId={params.id} /&gt;
    &lt;/main&gt;
  );
}</code></pre>
<table>
<thead>
<tr>
<th>영역</th>
<th>방식</th>
<th>이유</th>
</tr>
</thead>
<tbody><tr>
<td>Header</td>
<td>SSG</td>
<td>변하지 않는 UI</td>
</tr>
<tr>
<td>OrderDetail</td>
<td>SSR</td>
<td>쿠키 인증 + 최신 데이터 필요</td>
</tr>
<tr>
<td>ConfirmOrderButton</td>
<td>CSR</td>
<td>사용자 인터랙션 필요</td>
</tr>
</tbody></table>
<hr />
<h2 id="4-5-실습-결과-예상-밖-동작">4-5. 실습 결과: 예상 밖 동작</h2>
<p><img alt="" src="https://velog.velcdn.com/images/sunmins/post/49493166-b648-4dff-b3cd-ac427513fef5/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/sunmins/post/94283eb9-1f9b-494d-a601-6529a2f84804/image.png" /></p>
<h3 id="nextjs-13-app-router에서-csr-컴포넌트의-동작-이해">Next.js 13 App Router에서 CSR 컴포넌트의 동작 이해</h3>
<p>실습 결과, 예상과 달랐습니다.<br />처음에는 CSR 컴포넌트가 서버에서는 완전히 빈 껍데기로 내려오고, 브라우저 JS가 실행되면서 태그와 내용을 모두 채운다고 생각했습니다.  </p>
<p>하지만 실제 Network → Document에서는 다음과 같이 나타났습니다:</p>
<pre><code class="language-tsx">&lt;p&gt;브라우저 렌더링 시간: &lt;/p&gt;</code></pre>
<ul>
<li>ConfirmOrderButton 같은 <strong>CSR 컴포넌트</strong>는 브라우저에서 JS가 실행되어야 상태 값(<code>time</code>)이 채워짐</li>
<li>태그는 서버에서 내려오고, <code>time</code> 값만 비어 있음</li>
</ul>
<p>즉, <strong>CSR이라고 해서 태그까지 모두 브라우저에서 그려지는 것이 아니라, 최소한의 DOM 구조는 서버에서 내려주고, 동적 값만 브라우저 JS가 채워주는 형태</strong> 였습니다.</p>
<hr />
<h3 id="이유">이유</h3>
<h4 id="1-app-router이기-때문에-최소-dom-구조를-내려줌">1. App Router이기 때문에 최소 DOM 구조를 내려줌</h4>
<ul>
<li>Page Router(CSR): 초기 HTML에는 <code>&lt;div id=&quot;__next&quot;&gt;&lt;/div&gt;</code> 정도만 내려오고, 실제 태그는 없음 → 브라우저 JS가 다 렌더링해야 함</li>
<li>App Router(CSR): 최소 DOM 구조(버튼, <code>&lt;p&gt;</code> 등)는 서버에서 내려주고, 동적 값만 브라우저가 채움 → 깜빡임 최소화, SEO/접근성 유지</li>
</ul>
<h4 id="2-동적-상태는-브라우저에서만-채워짐">2. 동적 상태는 브라우저에서만 채워짐</h4>
<ul>
<li><code>useState</code>와 <code>useEffect</code>에서 설정되는 값(<code>time</code>)은 브라우저가 JS를 실행할 때 채워짐</li>
<li>따라서 <code>&lt;p&gt;</code> 태그는 서버 HTML에 포함되지만, 내용은 빈 상태로 보임</li>
</ul>
<h4 id="3-seo접근성-및-레이아웃-안정성">3. SEO/접근성 및 레이아웃 안정성</h4>
<ul>
<li>최소한의 HTML 구조를 내려주므로, 스크린 리더나 초기 레이아웃에서도 UI가 유지됨</li>
</ul>
<h3 id="✔-정리">✔ 정리</h3>
<ul>
<li><p><strong>App Router</strong>: <strong>HTML 태그 구조는 서버에서 내려주고, 브라우저 JS가 동적 값만 채움</strong> → 초기 렌더링 안정성 높음
바뀐 이유: 초기 화면이 빈 화면으로 보이는 문제를 줄이고, 화면 깜빡임 최소화, SEO와 접근성을 개선하기 위해</p>
</li>
<li><p>Page Router: 서버에서 HTML 구조 거의 내려주지 않고, 브라우저 JS가 모든 것을 렌더링 → 초기 렌더링 시 빈 화면 가능성 있음</p>
</li>
</ul>
<hr />
<h2 id="5-✔-ssr-·-ssg-·-isr-·-csr을-섞는-기준">5. ✔ SSR · SSG · ISR · CSR을 섞는 기준</h2>
<p>아래는 실무에서 사용하는 <strong>의사결정 체크리스트</strong>입니다.</p>
<hr />
<h3 id="🟦-ssg-static-를-사용해야-하는-경우">🟦 SSG (Static) 를 사용해야 하는 경우</h3>
<p><strong>페이지 단위:</strong>  </p>
<ul>
<li>변하지 않는 정적인 페이지 (회사 소개, 제품 안내, 정적 블로그)  </li>
<li>SEO 중요 + 데이터가 거의 안 변함  </li>
<li>로그인 여부와 상관 없는 공개 페이지  </li>
<li>CDN 캐시로 초고속 로딩 필요  </li>
</ul>
<p><strong>컴포넌트 단위:</strong>  </p>
<ul>
<li>Header, Footer, 정적 배너, 안내 컴포넌트  </li>
<li>페이지 내 다른 동적 영역과 함께 섞어 사용 가능  </li>
</ul>
<p><strong>예시:</strong>  </p>
<ul>
<li>회사 소개 페이지 전체 → Header/Footer는 SSG, 게시판 목록은 ISR  </li>
</ul>
<hr />
<h3 id="🟩-ssr-을-사용해야-하는-경우">🟩 SSR 을 사용해야 하는 경우</h3>
<p><strong>페이지 단위:</strong>  </p>
<ul>
<li>로그인 사용자별 데이터를 렌더링해야 함  </li>
<li>요청마다 데이터가 달라짐 (주문 상세, 장바구니)  </li>
<li>*<em>쿠키 인증이 필요한 API *</em> </li>
<li>*<em>최신 데이터 필요 (재고, 가격)  *</em></li>
</ul>
<p><strong>컴포넌트 단위:</strong>  </p>
<ul>
<li>OrderDetail, MyPageContent, 결제 정보 영역 등  </li>
<li>페이지 전체를 SSR로 만들 필요 없이, 필요한 컴포넌트만 SSR  </li>
</ul>
<p><strong>예시:</strong>  </p>
<ul>
<li>주문 페이지 → Header는 SSG, 주문 상세 데이터는 SSR  </li>
</ul>
<hr />
<h3 id="🟨-csr-을-사용해야-하는-경우">🟨 CSR 을 사용해야 하는 경우</h3>
<p><strong>페이지 단위:</strong>  </p>
<ul>
<li>전체 페이지를 CSR로 만들 수 있지만, 보통 *<em>인터랙션 중심의 페이지에서만 전체 CSR 사용  *</em>
(예: SPA, 로그인 후 대시보드)</li>
</ul>
<p><strong>컴포넌트 단위:</strong>  </p>
<ul>
<li>*<em>버튼, 입력폼, 모달, 드롭다운, router.push, useState/useEffect  *</em></li>
<li>페이지 내 일부 UI만 CSR로 분리 가능  </li>
</ul>
<p><strong>예시:</strong>  </p>
<ul>
<li>주문 페이지 → 주문 확정 버튼, 장바구니 수량 변경 버튼, 필터 UI  </li>
</ul>
<hr />
<h3 id="🟪-isr을-사용해야-하는-경우">🟪 ISR을 사용해야 하는 경우</h3>
<p><strong>페이지 단위:</strong>  </p>
<ul>
<li>*<em>데이터가 변하긴 하지만 자주 변하지 않음  *</em></li>
<li>SEO가 중요하고 CSR로는 부족한 경우  </li>
<li>캐싱된 HTML을 주기적으로 재생성  </li>
</ul>
<p><strong>컴포넌트 단위:</strong>  </p>
<ul>
<li><strong>상품 목록, 블로그 글 목록, FAQ 리스트</strong> 등  </li>
<li>페이지 내 다른 컴포넌트는 SSG/SSR/CSR과 조합 가능  </li>
</ul>
<p><strong>예시:</strong>  </p>
<ul>
<li>블로그 메인 페이지 → Header/Footer는 SSG, 글 목록은 ISR, 검색/필터는 CSR  </li>
</ul>
<hr />
<h2 id="6-✔-컴포넌트-단위로-렌더링-방식을-나누는-이점">6. ✔ 컴포넌트 단위로 렌더링 방식을 나누는 이점</h2>
<h3 id="🔹-빠른-초기-로딩">🔹 빠른 초기 로딩</h3>
<ul>
<li>변하지 않는 UI는 <strong>SSG</strong>로 미리 빌드 → CDN 캐시 제공  </li>
<li>초기 HTML이 바로 보여져 사용자 경험 개선</li>
</ul>
<h3 id="🔹-안전하고-최신-데이터-제공">🔹 안전하고 최신 데이터 제공</h3>
<ul>
<li>사용자별 민감 데이터는 <strong>SSR</strong>에서 쿠키 인증 후 렌더링  </li>
<li>항상 최신 데이터 제공 가능</li>
</ul>
<h3 id="🔹-인터랙션-처리-용이">🔹 인터랙션 처리 용이</h3>
<ul>
<li>버튼, 모달, 입력폼 등 <strong>CSR</strong>에서만 처리 가능  </li>
<li>페이지 전체를 CSR로 만들 필요 없이 필요한 부분만 클라이언트에서 처리</li>
</ul>
<h3 id="🔹-js-번들-최적화">🔹 JS 번들 최적화</h3>
<ul>
<li>페이지 전체를 CSR로 만들지 않아 <strong>클라이언트 JS 부담 감소</strong>  </li>
<li>필요한 컴포넌트만 Client Component로 분리</li>
</ul>
<h3 id="🔹-seo-친화적">🔹 SEO 친화적</h3>
<ul>
<li>SSR/SSG로 생성된 HTML은 검색엔진에 최적화됨  </li>
<li>초기 로딩 시 컨텐츠가 바로 노출</li>
</ul>
<hr />
<h2 id="💬-결론">💬 결론</h2>
<ul>
<li><strong>인터랙션</strong>은 항상 <strong>CSR</strong>에서 처리  </li>
<li><strong>데이터 렌더링</strong>은 상황에 맞춰 <strong>SSR/SSG/ISR</strong> 선택  </li>
<li><strong>정적 UI</strong>는 <strong>SSG</strong> 활용  </li>
<li>한 페이지 안에서도 <strong>컴포넌트 단위로 SSG + SSR + CSR 조합</strong>  </li>
<li>실무에서는 <strong>페이지 전체보다 컴포넌트 단위 최적화</strong>가 표준 전략  </li>
</ul>
<p>이번 글에서 CSR, SSR, SSG, ISR을 알아보고 실습해본 이유는<br /><strong>결국 사용자가 체감하는 속도를 빠르게 하고, SEO까지 최적화하기 위해서</strong>입니다.<br />적절히 활용하면 <strong>페이지 로딩 속도 향상, 서버 부하 감소, 유지보수 효율</strong>에도 도움이 될 거 같습니다.</p>