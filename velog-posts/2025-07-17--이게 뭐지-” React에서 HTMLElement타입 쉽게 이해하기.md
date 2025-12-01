# 🤔 React에서 HTMLElement란 무엇일까요?
웹 개발이나 React에서 DOM 요소를 다룰 때, 요소 타입을 명시적으로 지정해주는 것이 중요합니다.  
이때 TypeScript에서 DOM 요소를 대표하는 기본 타입 중 하나가 바로 `HTMLElement`입니다.

---
## `HTMLElement` 기본 개념

- `HTMLElement`는 HTML 문서 내 모든 **HTML 요소의 공통 기본 타입**입니다.  
- `<div>`, `<span>`, `<button>` 같은 구체적인 태그들은 각각 `HTMLDivElement`, `HTMLSpanElement`, `HTMLButtonElement` 등 더 구체적인 타입이 존재합니다.  
- 이 모든 구체적 타입들의 **공통 부모 역할을 하는 것이 `HTMLElement`**입니다.

즉, 특정 태그에 구애받지 않고 모든 HTML 요소를 다루고 싶을 때 `HTMLElement`를 사용합니다.

## `HTMLElement` vs `any`

| 구분       | `any`                          | `HTMLElement`                       |
| ---------- | ------------------------------ | ---------------------------------- |
| 타입 안정성 | 없음, 모든 값 허용             | DOM 요소임을 보장하는 명확한 타입  |
| 타입 검사  | 무시                           | 엄격하게 DOM API를 가진 객체만 허용 |
| 사용 목적  | 임시, 빠른 개발 시             | 타입 안정성을 유지하며 DOM 요소 다룰 때 |

`any`는 타입 검사를 완전히 무시하는 자유 타입이고,  
`HTMLElement`는 **HTML 요소 전용으로 타입 안전성을 보장하는 타입**입니다.


## DOM 요소 타입별 비교

| 타입명                | 범위                                  | 구체성 정도          |
| ------------------ | ----------------------------------- | --------------- |
| `Element`          | 모든 DOM 요소 (HTML, SVG, MathML 등)     | 가장 일반적 (가장 넓음)  |
| `HTMLElement`      | 모든 HTML 요소                          | 중간 (HTML 요소 전부) |
| `HTMLDivElement` 등 | 특정 HTML 태그 요소 (`<div>`, `<button>`) | 가장 구체적          |

- `Element`는 **HTML뿐만 아니라 SVG, MathML 등 모든 종류의 DOM 요소**를 포함하는 가장 일반적인 타입입니다.  
- `HTMLElement`는 HTML 문서 내 모든** HTML 요소**를 포함하는 중간 단계 타입입니다.  
- `HTMLDivElement`, `HTMLButtonElement` 등은 **특정 태그**에 매우 구체화된 타입입니다.


## ⚙️ 사용 예시

```tsx
import React, { useRef, useEffect } from "react";

function Example() {
  // 모든 HTML 요소를 참조할 수 있는 ref
  const ref1 = useRef<HTMLElement | null>(null);

  // 오직 <div> 요소만 참조할 수 있는 ref
  const ref2 = useRef<HTMLDivElement | null>(null);

  // 오직 <button> 요소만 참조할 수 있는 ref
  const ref3 = useRef<HTMLButtonElement | null>(null);

  useEffect(() => {
    if (ref1.current) {
      console.log("ref1 current:", ref1.current.tagName);
    }
    if (ref2.current) {
      console.log("ref2 current:", ref2.current.tagName);
    }
    if (ref3.current) {
      console.log("ref3 current:", ref3.current.tagName);
    }
  }, []);

  return (
    <>
      <div ref={ref1}>모든 요소 가능한 ref1</div>
      <div ref={ref2}>오직 div만 가능한 ref2</div>
      <button ref={ref3}>오직 button만 가능한 ref3</button>
    </>
  );
}
```

## ✅ 요약 정리

- `any`는 타입 검사를 완전히 건너뛰는 자유로운 타입입니다.  
- `HTMLElement`는 HTML 요소임을 명확히 하면서 타입 안정성을 확보하는 중간 수준의 타입입니다.  
- DOM 요소를 다룰 때는 가능하면 `any` 대신 적절한 DOM 타입을 사용하는 것이 안전합니다.
- 상황에 맞게 Element → HTMLElement → 구체적 태그 타입 순으로 **구체적인 타입을 사용**하는 것이 좋습니다.