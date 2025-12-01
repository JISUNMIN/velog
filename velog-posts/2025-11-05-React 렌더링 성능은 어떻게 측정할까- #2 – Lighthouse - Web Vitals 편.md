> 지난 글에서는 **React DevTools Profiler**와 **Chrome Performance 탭**을 활용해  
> 렌더링 과정과 병목 구간을 직접 분석하는 방법을 살펴봤습니다.  
>
> 이번 글에서는 그 다음으로,  
> **Lighthouse**와 **Web Vitals**를 통해 페이지의 **로딩 성능**과 **사용자 체감 속도**를  
> 수치로 측정하고 검증하는 방법을 알아보겠습니다.

## 1️⃣ Lighthouse – 페이지 로딩 성능 점수로 확인

React 앱 전체의 **초기 로딩 속도와 사용자 체감 성능**을 자동으로 분석해주는 도구입니다.  
Next.js, CRA 등 어떤 환경에서도 측정 가능하며, 실제로 **SEO 평가**나 **사용자 경험(UX) 품질 검사**에도 활용됩니다.

### 🔍 사용 방법
1. 브라우저 DevTools → **Lighthouse 탭**  
2. **Categories** 항목에서 원하는 지표 선택  
   - 🚀 **Performance**: 로딩·렌더링 속도 중심 (프론트엔드 성능 측정용)  
   - ♿ **Accessibility**: 접근성 점검 (색상 대비, 키보드 탐색 등)  
   - 🧭 **Best Practices**: 웹 개발 시 지켜야 하는 안전하고 효율적인 표준 규칙 체크 항목으로 보안·이미지·HTTPS 등 웹 품질  
   - 🔍 **SEO**: 검색엔진 최적화 상태 확인  
3. **Mode 선택 (측정 방식)**  
   - **✅ Navigation (기본)**: 페이지 로드부터 완전히 렌더링될 때까지의 성능을 측정 → 가장 일반적인 사용 방식. FCP, LCP, TTI 같은 로딩 성능 지표 확인 시 사용  
   - **Timespan**: 특정 동작(예: 버튼 클릭, 탭 이동 등) 동안의 성능을 기록  →  사용자 상호작용이 많은 SPA 환경 테스트에 적합  
   - **Snapshot** : 현재 화면 상태만 빠르게 분석  
     → 정적인 페이지나 UI 상태(예: 대시보드) 점검 시 사용  
     
 4. **Device 선택 (테스트 환경)**  
   	- **✅ Mobile (기본)** : 모바일 네트워크 및 CPU 환경 기준으로 측정    →  실제 사용자 체감 속도에 가장 가깝게 평가됨  
  	 - **Desktop**: 데스크톱 기준 성능 (네트워크/CPU 제약 완화)  
     → 개발 환경에서 상대적인 성능 비교나 디버깅용으로 활용  
5. 모든 옵션 설정 후 **“Analyze page load”** 실행

![](https://velog.velcdn.com/images/sunmins/post/45be6f25-7554-4eef-8913-fe71ca666e27/image.png)
![](https://velog.velcdn.com/images/sunmins/post/2ba8d92f-2bd7-46c9-9347-eab6794ae40c/image.png)
![](https://velog.velcdn.com/images/sunmins/post/6992c53b-f50c-401c-bcff-c0f0ffe9d68e/image.png)





> 💡 **Tip:** 개발 중에는 “Performance”만 선택해도 충분하고,  
> 배포 전에는 **Performance + Best Practices** 정도를 함께 돌려보면 좋습니다.

---

### 📊 주요 지표
| 항목 | 의미 | 좋음 기준 |
|------|------|------------|
| **First Contentful Paint (FCP)** | 사용자가 **화면에서 첫 콘텐츠(텍스트·이미지 등)** 를 보는 시점 — “처음 뭔가 뜨는 순간” | < 1.8초 |
| **Largest Contentful Paint (LCP)** | 화면의 **가장 큰 콘텐츠(대표 이미지, 큰 텍스트 등)** 가 완전히 표시된 시점 — “주요 화면이 다 보이는 순간” | < 2.5초 |
| **Total Blocking Time (TBT)** | **화면은 떠 있지만, 브라우저가 너무 바빠서 사용자의 클릭이나 스크롤에 바로 반응하지 못한 시간의 합** — 페이지가 “멈춘 듯한 구간”을 수치로 보여줌 | < 200ms |

💡 **Tip**  
LCP는 이미지 용량, 폰트 로딩, JS 번들 크기의 영향을 많이 받습니다.
→ **이미지 최적화 / 코드 스플리팅 / Lazy Loading으로** 개선 가능
Lighthouse 결과로 “성능이 실제로 개선됐는지”를 수치로 증명할 수 있습니다.

---

## 2️⃣ Web Vitals – 실제 사용자 기준의 체감 성능

Google이 제안한 **Web Vitals 지표**는, 실제 사용자의 브라우저 환경 기준으로  
“체감 성능이 좋은지”를 판단하는 지표입니다.  

Lighthouse가 테스트용 환경이라면, Web Vitals는 **실제 서비스 품질 확인용**입니다.

**PageSpeed Insights**는 이 Web Vitals 데이터를 기반으로,  
추가로 **Lighthouse 실험실 결과**까지 함께 보여주는 도구입니다.  
즉, 실제 사용자 데이터(Field)와 테스트 데이터(Lab)를 한 번에 볼 수 있습니다.


### 🔍 두가지 측정 방법 
- **1. PageSpeed Insights**(https://pagespeed.web.dev)  
  → 실제 Chrome 사용자 데이터를 기반으로 Web Vitals 측정  
- **2. Chrome DevTools → Performance 탭**  
  → LCP, INP, CLS 이벤트가 타임라인에 직접 표시  
  
  ![](https://velog.velcdn.com/images/sunmins/post/05af743a-7d9f-459b-ac1d-55f459f6a89d/image.png)



### 📊 주요 핵심 지표
| 항목 | 의미 | 좋음 기준 |
|------|------|------------|
| **LCP (Largest Contentful Paint)** | 주요 콘텐츠가 화면에 완전히 표시되는 시간 | ≤ 2.5초 |
| **INP (Interaction to Next Paint)** | 사용자가 클릭·탭 등 입력 후 반응이 시각적으로 보이기까지 걸린 시간 (이전 FID 대체) | ≤ 200ms |
| **CLS (Cumulative Layout Shift)** | 페이지 내 요소가 예기치 않게 움직이는 정도 (시각적 안정성) | ≤ 0.1 |

### 🔁  **Field Data vs Lab Data **

- 상단 **Field Data (예: LCP, INP, CLS 등)**  
  → 실제 **Chrome 사용자의 브라우저 환경에서 자동 수집된 데이터**입니다.  
  실제 사용자들이 느낀 **체감 성능(UX 품질)**을 보여주며,  
  Google의 **Core Web Vitals 평가**에도 직접 반영됩니다.
  
- 하단 **Lab Data (예: FCP, LCP, TBT 등)**  
  → Google의 Lighthouse가 **가상 환경에서 페이지를 직접 로드해 측정한 결과**입니다.  
  개발 단계에서 **코드나 구조적 성능 문제를 점검할 때** 활용됩니다.

💡 **Tip**  
- **CLS**가 높다면 레이아웃이 튀는 문제입니다.  
  → 이미지 비율을 고정하거나 Skeleton UI를 적용하면 개선됩니다.
- **INP**는 클릭 반응 지연이 있는 UI(모달, 리스트 필터 등)에서 자주 높게 나옵니다.  
  → 이벤트 처리 로직 최적화나 Debounce 적용으로 개선할 수 있습니다.

---

##  🤔 언제, 무엇을 써야 할까?

### ⚛️ React DevTools Profiler  
**🔹 언제?**  
컴포넌트가 자주 리렌더링되거나, 특정 화면이 느릴 때  
**🔹 왜?**  
어떤 컴포넌트가 얼마나 자주, 왜 렌더링되는지 확인  
**🔹 예시:** “Header가 매번 리렌더링돼요” → Profiler로 원인 추적  

---

### ⚙️ Chrome Performance 탭  
**🔹 언제?**  
화면은 뜨는데 **스크롤이 끊기거나 클릭 반응이 느릴 때**  
**🔹 왜?**  
JS 실행, 레이아웃, 페인트 등 **브라우저 전체 병목 구간** 파악  
**🔹 예:** “버튼 클릭 후 반응이 늦어요” → Performance로 CPU 사용량 확인  

---

### 🚦 Lighthouse  
**🔹 언제?**  
배포 전, **페이지 로딩 속도나 성능 점수**를 수치로 보고 싶을 때  
**🔹 왜 씀?**  
FCP, LCP, TBT 등 **로딩 지표를 한눈에** 점수로 보여줌  
**🔹 예:** “이미지 최적화 후 성능이 좋아졌을까?” → Lighthouse 재측정  

---

### 📱 Web Vitals (PageSpeed Insights)  
**🔹 언제?**  
**운영 중인 서비스의 실제 사용자 체감 속도**를 알고 싶을 때  
**🔹 왜?**  
실제 크롬 사용자 데이터(LCP, INP, CLS)로 **현실 성능** 확인  
**🔹 예:** “사용자들이 ‘느리다’고 할 때” → PageSpeed Insights로 실데이터 확인  

---

### ✅ 정리

- 개발 중 느리다 → **Profiler / Performance**  
- 배포 전 속도 비교 → **Lighthouse**  
- 배포 후 실제 유저 체감 확인 → **Web Vitals**


---

## 💬 마무리

이번 글에서는  
- **Lighthouse**로 페이지 로딩 속도(FCP, LCP, TTI 등)를 점수화하고,  
- **Web Vitals**로 실제 사용자 기준의 체감 성능(LCP, FID, CLS)을 확인하는 방법을 살펴봤습니다.

글을 준비하며 저 역시 **React 성능 측정 도구**를 더 깊이 이해하게 되었습니다.  
예전엔 단순히 “느리면 최적화하자”는 생각이었지만, 이번엔 **각 도구의 사용 시점과 방법, 그리고 주요 지표의 의미**까지 명확히 정리할 수 있었습니다.  

앞으로는 기능 구현뿐 아니라,  
**렌더링과 로딩 속도까지 함께 고려하는 습관**을 가지려 합니다.
