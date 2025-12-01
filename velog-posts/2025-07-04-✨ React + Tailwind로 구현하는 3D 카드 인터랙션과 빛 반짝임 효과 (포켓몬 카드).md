React와 Tailwind CSS를 활용해, 마우스 움직임에 따라 카드가 3D로 회전하고 빛 반짝임 효과가 적용되는 인터랙티브 UI를 만드는 방법을 단계별로 정리해보겠습니다.

---

## 1. ref란 무엇인가?

React의 `ref`는 **DOM 요소를 직접 제어**할 수 있게 해주는 기능입니다.  
보통 UI 변경은 React 상태(state)를 통해 하지만,  
- 스크롤,  
- 애니메이션,  
- 마우스 위치 기반 이벤트 처리,  
- 직접 스타일 조작이 필요할 때는 `ref`를 사용해 DOM에 접근합니다.

예를 들어,  
```tsx
const containerRef = useRef(null);
const overlayRef = useRef(null);
```
이렇게 생성한 ref를 특정 DOM 요소에 연결하고, 이벤트 핸들러에서 직접 스타일을 변경하거나 위치를 계산할 수 있습니다.

## 2. getBoundingClientRect()를 활용한 마우스 좌표 계산
`getBoundingClientRect()`는 요소의 브라우저 화면 내 위치와 크기 정보를 알려주는 DOM API입니다.

```tsx
const rect = container.getBoundingClientRect();
const x = e.clientX - rect.left;
const y = e.clientY - rect.top;
```

- e.clientX, e.clientY는 전체 화면 기준 마우스 좌표
- rect.left, rect.top은 카드 요소의 화면 내 위치

이를 빼서 카드 내부 기준의 마우스 좌표를 계산할 수 있습니다.


## 3. 3D 회전과 빛 반짝임 오버레이 구조

카드는 다음과 같이 3개의 레이어로 구성합니다:

- **containerRef**가 붙은 카드 전체 영역 (3D 회전 transform을 적용하는 대상)
- **overlayRef**가 붙은 빛 반짝임 오버레이 (카드 위에 겹치는 효과 레이어)
- 실제 카드 내용 (텍스트, 이미지 등)

```tsx
<div ref={containerRef}>
  <div ref={overlayRef} className="absolute inset-0" />
  <div className="relative z-10">카드 내용</div>
</div>
```

## 4. 레이어 구조 및 스타일링

- **overlayRef 레이어**  
  - `absolute inset-0` 으로 부모 카드 영역을 꽉 채움  
  - `pointer-events-none` 속성으로 마우스 이벤트가 막히지 않도록 설정  
  - `mix-blend-mode: color-dodge` 로 빛 반짝임 효과 구현

- **카드 내용 레이어**  
  - `relative z-10` 를 주는 이유  
    - z-index가 제대로 작동하려면 position 속성이 필요  
    - `relative`가 없으면 `z-10`이 무시되어 오버레이에 카드 내용이 가려질 수 있음

---

## 5. 마우스 이벤트로 스타일 직접 제어하기

- `useEffect` 안에서 다음 이벤트 핸들러 등록

| 이벤트 종류     | 동작 설명                                             |
|--------------|--------------------------------------------------|
| `mousemove` | 마우스 위치를 계산하여 카드에 3D 회전 효과 적용 (transform)      |
| `mousemove` | 오버레이의 background-position을 변경해 빛 반짝임 위치 변경         |
| `mouseleave`| 카드와 오버레이를 원래 상태로 초기화                             |

- 이벤트는 `addEventListener` / `removeEventListener` 로 직접 등록하며,  
- `ref`로 얻은 DOM 요소에 직접 접근해 스타일 변경

---

## 주요 CSS 속성 설명

| 속성명                       | 설명                                                          |
|-----------------------------|-------------------------------------------------------------|
| `transform-style: preserve-3d` | 3D 변환을 위해 필수. 자식 요소가 3D 공간 안에서 변형 가능                        |
| `will-change: transform`       | 성능 최적화용. 브라우저에게 transform 스타일 변경 예상 알림                      |
| `absolute inset-0`             | 부모 요소를 기준으로 위치를 완전히 꽉 채움 (top:0, right:0, bottom:0, left:0)          |
| `pointer-events: none`         | 오버레이가 마우스 이벤트를 막지 않도록 설정. 뒤쪽 요소 클릭 가능                   |
| `mix-blend-mode: color-dodge`  | 빛이 반사되는 듯한 광택 효과를 내는 혼합 모드. 어두운 배경에서 효과가 강함           |
| `z-index`                     | 요소의 쌓임 순서를 지정. 높은 값일수록 앞에 보임                                  |
| `relative`                    | 위치 기준 컨텍스트 생성. 자식의 absolute 위치 지정 시 기준이 됨                   |
| `background-position`         | 배경 이미지나 그라디언트의 위치를 지정. 마우스 위치에 따라 움직여 반짝임 효과 구현 가능 |
| `background-size`             | 배경 이미지나 그라디언트 크기 지정. 크면 더 부드럽고 넓게 보임                      |
| `filter: brightness()`        | 요소 밝기를 조절. 1 이상은 밝아지고 1 이하로 내려가면 어두워짐                      |
| `filter: opacity()`           | 요소 투명도를 조절. 0은 완전 투명, 1은 불투명                                   |
| `transform: perspective()`    | 3D 원근감(깊이감)을 설정. 값이 작을수록 입체감이 강해짐                           |
| `transform: rotateX(deg)`      | X축(좌우축)을 기준으로 요소를 회전. 고개를 끄덕이는 듯한 상하 회전                 |
| `transform: rotateY(deg)`      | Y축(위아래축)을 기준으로 요소를 회전. 고개를 좌우로 흔드는 듯한 회전                |
| `background-position` (동적)   | 마우스 위치에 따라 배경 위치를 변경해 빛이 움직이는 듯한 효과 구현                   |
| `filter: drop-shadow()`        | 요소에 그림자 효과를 주어 입체감과 깊이감을 더함                                 |
| `transition`                  | CSS 속성 변화를 부드럽게 애니메이션 처리                                        |




### linear-gradien
```css
linear-gradient(각도, 색상 위치1, 색상 위치2, ...)
```

deg: 그라디언트 방향(각도)을 의미
- 0도: 왼쪽 → 오른쪽
- 90도: 아래 → 위
- 105도: 대각선 방향

색상 뒤의 퍼센트(%): 해당 색상이 시작하거나 끝나는 위치

```css
linear-gradient(
  105deg,
  transparent 40%,
  rgba(255, 225, 130, 0.9) 45%,
  rgba(100, 200, 255, 0.9) 50%,
  transparent 54%
)
```

구간별 색상 변화

| 구간          | 색상 설명                                    |
| ----------- | ---------------------------------------- |
| 0% \~ 40%   | `transparent` (투명) 유지                    |
| 40% \~ 45%  | 투명 → `rgba(255, 225, 130, 0.9)` (점진적 변화) |
| 45% \~ 50%  | `rgba(100, 200, 255, 0.9)` 유지            |
| 50% \~ 54%  | `rgba(100, 200, 255, 0.9)` → 투명 (점진적 변화) |
| 54% \~ 100% | `transparent` (투명) 유지                    |






---

##  전체 흐름 정리

- 마우스가 카드 내부에서 움직이면  
  → 좌표 계산 → transform 스타일 변경 → 카드가 3D로 기울어짐  
  → 오버레이 배경 위치 변경 → 빛 반짝임 위치 조절

- 마우스가 카드 밖으로 나가면  
  → transform과 배경 위치 초기화 → 원래 상태로 돌아감

- 레이어 구조 덕분에  
  → 카드 내용과 빛 반짝임이 자연스럽게 겹쳐 보임  
  → 마우스 이벤트가 오버레이에 막히지 않음

---

## 구현 코드 예시

###  `useRef` 선언 및 `useEffect` 이벤트 등록

```tsx
const containerRef = useRef<HTMLDivElement>(null);
const overlayRef = useRef<HTMLDivElement>(null);

useEffect(() => {
  const container = containerRef.current;
  const overlay = overlayRef.current;
  if (!container || !overlay) return;

  const handleMouseMove = (e: MouseEvent) => {
    const rect = container.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const rotateY = (-1 / 5) * x + 20;
    const rotateX = (4 / 30) * y - 20;

    container.style.transform = `
      perspective(350px)
      rotateX(${rotateX}deg)
      rotateY(${rotateY}deg)
    `;

    overlay.style.backgroundPosition = `${x / 5}% ${y / 5}%`;
  };

  const handleMouseLeave = () => {
    container.style.transform = "";
    overlay.style.backgroundPosition = "";
  };

  container.addEventListener("mousemove", handleMouseMove);
  container.addEventListener("mouseleave", handleMouseLeave);

  return () => {
    container.removeEventListener("mousemove", handleMouseMove);
    container.removeEventListener("mouseleave", handleMouseLeave);
  };
}, []);
```
### JSX 구조
```tsx
return (
  <div
    ref={containerRef}
    onClick={onClick}
    className={`relative h-55 rounded-lg p-6 shadow-md cursor-pointer mb-3 border transition-all duration-100
      ${
        project.isPersonal
          ? "bg-gray-100 border-gray-300 hover:bg-gray-200 hover:border-gray-400 hover:scale-105"
          : "bg-white border-stone-300 hover:bg-gray-100 hover:border-stone-400 hover:scale-105"
      }
    `}
    style={{
      transformStyle: "preserve-3d",
      willChange: "transform",
    }}
  >
    <div
      ref={overlayRef}
      className="absolute inset-0 z-10 pointer-events-none mix-blend-color-dodge rounded-lg"
      style={{
        background:
          "linear-gradient(105deg, transparent 40%, rgba(255,219,112,0.8) 45%, rgba(132,50,255,0.6) 50%, transparent 54%)",
        filter: "brightness(1.2) opacity(0.8)",
        backgroundSize: "150% 150%",
        backgroundPosition: "100%",
      }}
    />
    <div className="relative z-10">
      <h3 className="text-xl font-semibold text-gray-800">
        {project.projectName}
      </h3>
      <div className="text-sm text-gray-600 flex gap-1.5 items-center">
        담당자: {project?.manager?.name}
        <Avatar>
          <AvatarImage src={project?.manager?.profileImage ?? ""} />
          <AvatarFallback>
            <IoPersonCircle className="w-8 h-8" />
          </AvatarFallback>
        </Avatar>
      </div>
      <p className="text-sm text-gray-600">진행률: {project.progress}%</p>
      {!project.isPersonal && (
        <p className="text-sm text-gray-600">
          마감일: {convertDateToString(new Date(project.deadline), "-")}
        </p>
      )}
      <Progress value={project.progress} className="mt-4" />
    </div>
  </div>
);
```

## 참고 사이트

>[코딩애플 - 카드 반짝이는 효과 영상](https://www.youtube.com/watch?v=YDCCauu4lIk&t=195s)
> [포켓몬 카드 Holo 카드 데모](https://poke-holo.simey.me/)