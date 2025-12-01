##  ✅ useRef란?

`seRef`는 리액트에서 컴포넌트 내에서 변경 가능한 참조값을 관리할 때 사용하는 Hook입니다.  
주로 **DOM 요소에 직접 접근**하거나, **렌더링과 무관하게 유지해야 할 값을 저장**할 때 사용합니다.

**`useRef`를 사용하면 컴포넌트가 다시 렌더링되어도 값이 초기화되지 않고 유지**되기 때문에, 상태(state)와 달리 렌더링 트리거 없이 값 관리가 가능합니다.

## 🧾 useRef 타입 선언 
```tsx
const itemRef = useRef<HTMLElement | null>(null);
```
- useRef에 들어가는 타입은 보통 참조하려는 DOM 요소의 타입을 지정합니다. 예를 들어, `<div>`를 참조한다면 `HTMLDivElement | null` 타입을 씁니다.
- 타입을 지정하지 않으면 useRef()는 기본적으로 `MutableRefObject<undefined>` 타입이 되어 타입 안전성이 떨어질 수 있습니다.
- 초기값으로는 `null`을 넣어주는 것이 일반적입니다.

> [HTMLElement](https://velog.io/@sunmins/%EC%9D%B4%EA%B2%8C-%EB%AD%90%EC%A7%80-React%EC%97%90%EC%84%9C-HTMLElement%ED%83%80%EC%9E%85-%EC%89%BD%EA%B2%8C-%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0)란? HTML 문서 내 모든 요소들의 공통 기본 타입니다. 
> `<div>`,`<span>`,`<button>` 같은 구체적인 HTML 태그들은 각각 더 구체적인 타입(`HTMLDivElement, HTMLSpanElement, HTMLButtonElement`)을 가집니다.
이 모든 구체적 타입들의 공통 부모 역할을 하는 게 HTMLElement입니다.

## 🧩 useRef 사용법

### useRef 한 곳에 쓰일 때

```tsx
const itemRef = useRef<HTMLDivElement | null>(null);

return (
  <div ref={itemRef}>
    {/* ...*/}
  </div>
);

```
- 특정 한 곳의 DOM 요소에 접근할 때는 ref에 직접 useRef로 만든 객체를 넘겨줍니다.
- 렌더링 후 itemRef.current를 통해 해당 DOM 요소에 접근할 수 있습니다.

### useRef를 반복문에서 여러 개 쓸 때

```tsx
const itemRefs = useRef<(HTMLDivElement | null)[]>([]);

return (
  <>
    {items.map((item, index) => (
      <div
        key={item.id}
        ref={(el) => (itemRefs.current[index] = el)}
      >
        {/* ... */}
      </div>
    ))}
  </>
);
```
- 여러 개의 DOM요소를 각각 참고해야 할 때, 배열 형태의 useRef를 만듭니다.
- 초기값을 빈 배열`[]`로 주고, 각 요소의 ref를 콜백 함수로 받아 `itemRefs.current[index]`에 할당합니다.
- 이렇게 하면 `itemRefs.current` 배열에 각 DOM 요소가 순서대로 저장되어 필요할 때 참고할 수 있습니다.

## itemRefs와 itemRefs.current의 타입과 구조
- itemRefs는 useRef Hook으로 생성된 Ref 객체입니다.
- useRef가 반환하는 값은 `{ current: T }` 형태의 객체입니다. 따라서 itemRefs는 객체이고, itemRefs.current가 실제 우리가 관리하는 값입니다.

```tsx
const itemRefs = useRef<(HTMLDivElement | null)[]>([]);
```

- `itemRefs`는 `{ current: (HTMLDivElement | null)[] }` 타입이고,
- `itemRefs.curren`는 배열 타입 `(HTMLDivElement | null)[]`입니다.

반면, 단일 요소를 참조할 때

```tsx
const itemRef = useRef<HTMLDivElement | null>(null);
```

- `itemRef`는 `{ current: HTMLDivElement | null }` 타입 객체이고,
- `itemRef.current`는 `단일 DOM 요소 또는 null` 타입입니다.

| 변수명     | 타입 설명                                    | current 타입                            |
|------------|----------------------------------------------|----------------------------------------|
| itemRef    | { current: HTMLDivElement &#124; null }      | HTMLDivElement &#124; null (단일 DOM 요소)  |
| itemRefs   | { current: (HTMLDivElement &#124; null)[] }  | (HTMLDivElement &#124; null)[] (DOM 요소 배열) |

## ✍️ 정리
- useRef는 DOM 요소뿐 아니라, 렌더링과 상관없는 임의의 값을 저장하는 데도 활용됩니다.
- ref.current의 변경은 컴포넌트를 다시 렌더링하지 않습니다.
- 단일 요소: const ref = useRef<HTMLElement | null>(null)
- 여러 요소: const refs = useRef<(HTMLElement | null)[]>([])
- 접근 방식: ref.current, refs.current[index]

