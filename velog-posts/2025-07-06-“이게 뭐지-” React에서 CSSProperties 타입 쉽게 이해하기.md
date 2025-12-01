# 🤔 React에서 `CSSProperties`란 무엇일까요?

React로 개발할 때, 컴포넌트에 스타일을 주는 방법 중 하나는 인라인 스타일을 사용하는 것입니다.  
이때 스타일은 자바스크립트 객체 형태로 작성되는데, 이 객체가 어떤 모양이어야 하는지 TypeScript에서 미리 알려주는 타입이 바로 `CSSProperties`입니다.

---

##  인라인 스타일과 `CSSProperties`

```tsx
<div style={{ color: "red", backgroundColor: "blue", marginTop: 10 }}>
  스타일 적용된 div
</div>
```

위 코드에서 style에 넘긴 객체는 JavaScript 객체입니다.
하지만 TypeScript는 어떤 키가 유효하고, 값은 어떤 타입이어야 하는지 알 필요가 있습니다.
이 역할을 하는 것이 React.CSSProperties 타입입니다.

##  CSSProperties의 역할
스타일 프로퍼티 키와 값의 타입을 미리 정의해서, 오타나 잘못된 값을 컴파일 단계에서 잡아줍니다.
예를 들어 backgroundcolor처럼 오타가 있으면 타입 검사에서 에러가 납니다.
값도 "red"와 같이 문자열이나, 10같이 숫자(px 단위로 해석)로 적절히 타입 검사를 합니다.

## ⚙️ 사용법
```tsx
import React from "react";

const myStyle: React.CSSProperties = {
  color: "white",
  backgroundColor: "#333",
  padding: "10px 20px",
};

function MyComponent() {
  return <div style={myStyle}>안녕하세요!</div>;
}
```

## ✍️ 실전 예시: 직접 사용한 코드
```tsx

import { CSSProperties } from "react";

const overlayStyle: CSSProperties = {
  background: `
    linear-gradient(
      105deg,
      transparent 40%,
      rgba(255, 225, 130, 0.9) 45%,
      rgba(100, 200, 255, 0.9) 50%,
      transparent 54%
    )
  `,
  filter: "brightness(1.2) opacity(0.8)",
  backgroundSize: "150% 150%",
  backgroundPosition: "100%",
};

function Overlay() {
  return (
    <div
      ref={overlayRef}
      className="absolute inset-0 z-10 pointer-events-none mix-blend-color-dodge rounded-lg"
      style={overlayStyle}
    />
  );
}
```



### 🚫 타입 에러가 날 수 있는 몇 가지 상황
1. 잘못된 CSS 프로퍼티 이름 사용 시
```tsx
const myStyle: React.CSSProperties = {
  colr: "white", // 오타: color → colr
  backgroundColor: "#333",
};
```
2. 타입에 맞지 않는 값 사용 시
```tsx
const myStyle: React.CSSProperties = {
  color: 123, // 색상은 문자열이어야 하는데 숫자를 넣음
  backgroundColor: "#333",
};
```
3. 숫자에 단위가 필요한 속성에 숫자만 쓸 때 (단, padding은 숫자만 쓰면 px로 처리되지만, 문자열이 필요한 경우도 있음)
```tsx
const myStyle: React.CSSProperties = {
  padding: 10,          // OK, 10px로 해석
  margin: "10 20 30",   // 에러! 문자열이지만 단위가 없거나 부적절함
};

```
4. 지원하지 않는 CSS 속성 쓰기
```tsx
const myStyle: React.CSSProperties = {
  fakeProperty: "value", // 존재하지 않는 CSS 속성
};

```


## ⚠️ 주의할 점
CSS 속성 이름은 카멜케이스(camelCase) 로 작성해야 합니다. 예를 들어,

background-color → backgroundColor

font-size → fontSize

숫자값은 단위가 없는 경우 px로 자동 변환되지만, 단위가 필요한 경우 문자열로 작성해야 합니다.

## ✅ 요약 정리
**`React.CSSProperties`는 인라인 스타일(객체 형식)을 사용할 때  
올바른 CSS 속성명과 값의 타입을 검사하기 위해 React에서 정의한 타입입니다**.
