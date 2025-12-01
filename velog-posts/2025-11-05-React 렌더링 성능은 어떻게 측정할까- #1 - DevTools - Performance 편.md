>“렌더링 성능이 좋아졌다”는 말, 
어떤 기준으로 판단할 수 있을까요?
>
>성능 최적화를 했다면, 그 결과를 **수치**로 알 수 있어야 합니다. 
>
> 이번 글에서는 **React DevTools Profiler**와 **Chrome Performance 탭**을 활용해  
> 렌더링 과정과 병목 구간을 분석하는 방법을 정리했습니다.

---

## 1️⃣ React DevTools Profiler – 렌더링 원인과 시간 보기

React 프로젝트라면 가장 정확한 **렌더링 분석 도구**입니다.  
컴포넌트별로 **렌더링에 걸린 시간**, **렌더링 원인**, **횟수**를 시각적으로 확인할 수 있어요.

### 🔍 사용 방법
1. **React DevTools** 확장 프로그램 설치  
2. 브라우저 개발자 도구(DevTools) → **Profiler 탭** 클릭  
3. `Start profiling` → 페이지 조작 → `Stop profiling`  

이제 어떤 컴포넌트가, 몇 번, 왜 리렌더링됐는지를 한눈에 볼 수 있습니다.

![](https://velog.velcdn.com/images/sunmins/post/661ffece-b97f-4b9e-a19e-98f6401878f4/image.png)
![](https://velog.velcdn.com/images/sunmins/post/ae0f0ea7-ed8c-438b-a969-a45599abf0b5/image.png)
![](https://velog.velcdn.com/images/sunmins/post/e806b450-be91-4d1e-b311-96bf51681fbf/image.png)
![](https://velog.velcdn.com/images/sunmins/post/5d08b4c2-dbf9-41b4-9357-09d3b98f0c13/image.png)


### 📊 확인할 수 있는 것 (React 18 기준)
- **Priority** : 렌더링 작업의 우선순위 (Immediate = 즉시 렌더링, Low = 지연 가능)  
- **Committed at** : 이 렌더링이 DOM에 반영된 시점 (페이지 로드 후 시간)  
- **Render duration** : 렌더링에 걸린 실제 시간 (ms) – 10 ms 이하면 양호  
- **What caused this update** : `props` / `state` / `context` 변경 또는 익명 함수 콜백 등, 렌더링 트리거 원인  

💡 **Tip**  
`React.memo`, `useCallback`, `useMemo` 같은 최적화 전후로 **Render duration**을 비교하면  
“얼마나 빨라졌는지”를 수치로 확인할 수 있습니다.  
`What caused this update` 가 `anonymous` 로 표시되면 대부분 `onClick={() => setState()}` 처럼 익명 함수로 트리거된 렌더링입니다.

### 🧠 Profiler 그래프 읽는 법
- **색상**
  - ⚪️ **회색** → 이번 커밋에서 렌더링되지 않은 컴포넌트 (이전 렌더링 그대로 유지)  
  - 🟩 **연한 초록** → 매우 빠른 렌더링 (0~3ms 수준)  
  - 🟨 / 🟧 / 🟥 **노랑·주황·빨강** → 렌더링 시간이 길수록 색이 진해짐 (병목 가능성 높음)  
- **Commit 타임라인**
  - Profiler 상단의 세로 막대 그래프 영역  
  - 각 막대 = 한 번의 렌더링(Commit)  
  - `1/12`는 `“총 12번 중 현재 1번째 커밋(첫번째 커밋은 초기 렌더링)을 보고 있다”`는 의미  
  - 막대를 클릭하면 해당 시점에 렌더링된 컴포넌트를 아래 그래프에서 색상으로 확인 가능  
- **하이라이트 기능**
  - `Highlight updates when components render` 옵션은 Profiler 자체 기능은 아니지만,  
    DevTools의 실시간 렌더링 시각화 도구
  - 켜두면 렌더링이 발생할 때마다 UI가 깜빡이며 “어디가 자주 렌더링되는지” 즉시 확인 가능  

💡 **실무 활용 팁**
- 초기 렌더링이 느리면 → **코드 스플리팅** 또는 **Lazy Loading** 검토  
- 특정 컴포넌트의 `Render duration` 이 유독 크면 → **상태 분리** 또는 **props 구조 최적화**  
- 렌더링이 짧지만 자주 일어나면 → **불필요한 리렌더링** 의심 (`React.memo` / `useCallback` / `useMemo` 활용)  
- Provider·Context 구조라면 → **value 변경 범위 최소화** 또는 **소비자 컴포넌트 분리** 고려 
---

### 📘 용어 정리

- **[코드 스플리팅(Code Splitting)](ㅇㅇ)**  
  → 하나의 큰 JS 파일을 여러 조각으로 나눠, **필요할 때만 로드**하는 최적화 방법.  
  → React에서는 `React.lazy(() => import('./MyPage'))` 형태로 자주 사용.  
  → 불필요한 JS 로드를 줄여 **초기 렌더링 속도 개선**.

- **Lazy Loading (지연 로딩)**  
  → 이미지, 컴포넌트, 데이터 등을 **사용자가 실제로 볼 때만 불러오는 기법**.  
  → 예: `<img src="..." loading="lazy" />`  
  → 초기 로딩 부하 감소 → 사용자 체감 속도 향상.

- **소비자(Consumer) 컴포넌트 분리**  
  → `Context` 값을 실제로 **사용(`useContext`)하는 컴포넌트만 따로 분리하는 기법.**
  → value가 바뀌어도 해당 값을 쓰는 컴포넌트만 리렌더링되도록 해서 **불필요한 렌더링 최소화**.


 ```tsx
 // 소비자 컴포넌트 분리 
  const ThemeContext = createContext();

  function App() {
    const [theme, setTheme] = useState("light");

    return (
      <ThemeContext.Provider value={theme}>
        <Header />   {/* theme 안 씀 → 그대로 유지 */}
        <Content />  {/* theme 사용 → value 바뀌면 리렌더링 */}
      </ThemeContext.Provider>
    );
  }

  function Header() {
    console.log("Header 렌더링");
    return <h1>헤더</h1>;
  }

  function Content() {
    const theme = useContext(ThemeContext);
    console.log("Content 렌더링");
    return <div style={{ color: theme === "light" ? "black" : "white" }}>내용</div>;
  }
```


---

## 2️⃣ Chrome DevTools Performance – 브라우저 레벨 렌더링 분석

React 내부만 보는 게 아니라, **브라우저 전체 렌더링 과정**을 분석하고 싶을 때 사용합니다.  
JS 실행, 스타일 재계산, 페인트 등 렌더링 단계별 비용을 정확히 볼 수 있습니다.

### 🔍 사용 방법
1. DevTools → **Performance 탭**  
2. `Record` 버튼 클릭 후 페이지 조작  
3. `Stop` 후 Timeline 분석  

![](https://velog.velcdn.com/images/sunmins/post/8917837c-7e33-48df-b18b-d7c8698f27c9/image.png)
![](https://velog.velcdn.com/images/sunmins/post/320d6f2a-994f-4441-885d-348fe28b342f/image.png)
![](https://velog.velcdn.com/images/sunmins/post/b73d4c4a-45d6-4fe4-884d-7347ee14ea42/image.png)


### 📊 확인할 수 있는 것

Performance 탭은 세 영역으로 나뉘어 있으며,  
각 구간마다 React 렌더링 성능을 분석할 수 있는 핵심 정보가 다릅니다.



### 🟣 Main Thread (상단 타임라인)
페이지의 **렌더링과 스크립트 실행 흐름**을 시간 순서대로 보여주는 구간입니다.  
색상별 블록을 통해 브라우저가 어떤 작업에 시간을 쓰는지 확인할 수 있습니다.

- **Recalculate Style / Layout / Paint**  
  브라우저가 **스타일 계산(CSS Recalc), 레이아웃 재배치(Layout), 화면 그리기(Paint)** 를 수행하는 단계.  
  → 이 구간이 길거나 자주 반복되면 불필요한 DOM 업데이트나 스타일 재계산이 발생 중일 가능성이 높음.

- **Script(보라색)**  
  React 렌더링, 이벤트 처리, 상태 변경 등 JS 실행이 일어나는 부분.  
  → 긴 Script 블록이 이어지면 CPU 점유율이 높거나 불필요한 렌더링이 많음을 의미함.  
  💡 **참고:** 보라색 블록은 `Task`, `Function Call`, `Evaluate Script` 등으로 표시되며,  
  실제로는 모두 **JS 실행(Scripting)** 범주에 해당함.



### 🟢 Frames

- **FPS 그래프(Frames)**  
  FPS(Frames Per Second)는 **초당 렌더링되는 프레임 수**를 의미함.  
  상단 초록색 그래프가 **짧고 일정하게 유지될수록** 한 프레임을 빠르게 그린다는 뜻으로,  
  부드럽고 안정적인 렌더링 상태를 의미함.  
  반대로 프레임 간 간격이 불규칙하거나 그래프가 급격히 떨어질 경우,  
  프레임 드랍이나 렌더링 병목이 발생 중임을 뜻함.  
  💡 **기준:** 60fps(≈16.6ms/프레임)가 이상적이며, 33ms 이상이 소요되면  
  프레임 드랍이 체감될 수 있음.


### 📈 하단 탭 영역 (Summary / Bottom-up / Call Tree / Event Log)
Main Thread에서 특정 구간을 클릭하면 활성화되는 상세 분석 구간입니다.

| 탭 | 주요 기능 | 활용 포인트 |
|------|-------------|--------------|
| **Summary** | 선택 구간의 Script, Rendering, Painting 비율 요약 | 어떤 작업이 가장 많은 시간을 차지했는지 확인 |
| **Bottom-up** | 전체 실행 중 가장 비용이 큰 함수 순으로 정렬 | 병목 함수·컴포넌트 식별 |
| **Call Tree** | 함수 호출 계층 구조 표시 | React 렌더링 흐름(예: commitRoot, render 등) 추적 |
| **Event Log** | 타임라인 순 이벤트 목록 | 특정 시점에 어떤 이벤트가 실행됐는지 확인 |

💡 **분석 순서 팁:**  
1️⃣ **Frames**에서 프레임 드랍 구간을 확인 →  
2️⃣ **Main Thread**에서 해당 시점을 클릭 →  
3️⃣ **하단 Summary / Bottom-up / Call Tree** 탭에서 원인 추적.


### ⚡ 좌측 Insights (LCP / INP / CLS)
자동으로 계산된 **Core Web Vitals** 지표를 표시합니다.

- **LCP (Largest Contentful Paint)** → 주요 콘텐츠가 표시된 시점 (로딩 속도 지표, **2.5초 이하 권장**)  
- **INP (Interaction to Next Paint)** → 사용자 입력 후 반응 속도 (**200ms 이하 권장**)  
- **CLS (Cumulative Layout Shift)** → 레이아웃이 얼마나 이동했는지(시각적 안정성, **0.1 이하 권장**)

👉 **페이지 초기 로딩 성능과 사용자 체감 속도**를 확인하는 데 유용함.

---

💡 **Tip**
- **Layout / Paint 구간이 길다면** DOM 구조나 스타일 계산을 최소화  
- **Script 블록이 길다면** 렌더링 최적화(`React.memo`, `useCallback`) 또는 연산 분리(Web Worker) 고려  
- **LCP / CLS 수치가 나쁘다면** 이미지 최적화, Lazy Loading, 안정적인 레이아웃 설계 필요
---

## 3️⃣ Lighthouse – 페이지 로딩 성능 점수로 확인

React 앱 전체의 **초기 로딩 성능과 사용자 체감 속도**를 측정할 수 있는 자동화 도구입니다.  
Next.js, CRA 모두 측정 가능하며, 실제로 SEO와 사용자 경험 평가에도 쓰입니다.

### 🔍 사용 방법
1. DevTools → **Lighthouse 탭**  
2. Performance 체크 후 “Analyze page load” 실행  

### 📊 주요 지표
| 항목 | 의미 | 좋음 기준 |
|------|------|------------|
| **FCP** | 첫 콘텐츠가 표시되는 시간 | < 1.8초 |
| **LCP** | 가장 큰 콘텐츠가 표시되는 시간 | < 2.5초 |
| **TTI** | 사용자가 상호작용할 수 있게 되는 시점 | < 3.8초 |

💡 **Tip**  
이미지 최적화나 코드 스플리팅 적용 후 LCP가 개선되는 경우가 많습니다.  
Lighthouse 결과로 “성능이 실제로 개선됐는지”를 수치로 증명할 수 있습니다.

---

## 4️⃣ Web Vitals – 실제 사용자 기준의 체감 성능

Google이 제안한 **Web Vitals 지표**는, 실제 사용자의 브라우저 환경 기준으로  
“체감 성능이 좋은지”를 판단하는 지표입니다.  

Lighthouse가 테스트용 환경이라면, Web Vitals는 **실제 서비스 품질 확인용**이에요.

### 📊 주요 지표
| 항목 | 의미 | 좋음 기준 |
|------|------|------------|
| **LCP** | 주요 콘텐츠 표시 시간 | ≤ 2.5초 |
| **FID** | 첫 입력 반응 시간 | ≤ 100ms |
| **CLS** | 레이아웃 이동 정도 | ≤ 0.1 |

### 🔍 측정 방법
- Chrome 확장 프로그램 **Web Vitals** 설치  
- 브라우저 툴바에서 실시간 성능 지표 확인  

💡 **Tip**  
CLS가 높다면 레이아웃이 튀는 문제입니다.  
이미지 placeholder 비율을 고정하거나 Skeleton UI를 적용하면 개선됩니다.

---

## 💬 마무리

React의 렌더링 성능을 개선하려면  
**무엇이 느린지를 아는 것**이 첫 단계입니다.  

이번 글에서는  
- **React DevTools Profiler**로 컴포넌트별 렌더링 시간과 원인 분석,  
- **Performance 탭**으로 브라우저 렌더링 흐름(FPS, Layout, Paint 등) 파악하는 방법을 살펴봤습니다.

다음 글에서는 **Lighthouse**와 **Web Vitals**를 통해  
최적화 결과를 실제 수치로 검증하고,  
사용자 체감 속도까지 평가하는 방법을 알아보겠습니다.



