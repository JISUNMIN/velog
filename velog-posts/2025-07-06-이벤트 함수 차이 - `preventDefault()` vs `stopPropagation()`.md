프론트엔드 개발을 하다 보면 `e.preventDefault()`와 `e.stopPropagation()`을 자주 볼수있는데, 저 역시 헷갈렸던 부분이라, 정리해보았습니다.

---

## ✋ `e.preventDefault()` – 브라우저의 기본 동작 막기

`preventDefault()`는 **브라우저의 기본 동작을 차단**할 때 사용합니다.

예시)
- `<a>`태그 클릭시 페이지 이동
- `<form>` 제출 시 페이지 새로 고침

### ✅ 예제

```jsx
const handleLinkClick = (e) => {
  e.preventDefault(); // a 태그 기본 이동 막기
  console.log("링크 클릭 시 페이지 이동 막음");
};

return (
  <a href="https://example.com" onClick={handleLinkClick}>
    이동하지 않는 링크
  </a>
);
```

## 🫧🚫 e.stopPropagation() – 이벤트 전파 차단 (버블링 방지)
`stopPropagation()`은 이벤트가 부모 요소로 전파되는 것을 막는 역할을 합니다.

자식 요소에서 이벤트가 발생해도
부모 요소에서 해당 이벤트 핸들러가 실행되지 않도록 막을 수 있습니다.
**e.stopPropagation()은 이벤트를 발생시킨 자식 요소에서 호출해야 효과가 있습니다.**

### ✅ 예제
```jsx
const handleParentClick = () => {
  console.log("부모 요소 클릭됨");
};

const handleChildClick = (e) => {
  e.stopPropagation(); // ✅ 부모로 이벤트 전파 막기
  console.log("자식 요소 클릭됨");
};

return (
  <div onClick={handleParentClick} style={{ padding: "20px", background: "#eee" }}>
    <button onClick={handleChildClick}>자식 버튼</button>
  </div>
);

```

##  ✍️ 실전 예시: 직접 사용한 코드
### 🔥 문제 상황
```tsx
<div ref={containerRef} onClick={onClick}>
  <ActionDropdownMenu ... />
</div>
```
아래와 같은 구조에서 ActionDropdownMenu에서 메뉴 항목을 클릭했는데, 부모 div의 onClick도 같이 실행되는 문제가 발생 했습니다.

### 💡 사용 코드
```tsx
<div ref={containerRef} onClick={onClick}>
  <ActionDropdownMenu ... />
</div>


export function ActionDropdownMenu({
...
}: ActionDropdownMenuProps) {
  return (
    <DropdownMenu open={open} onOpenChange={setOpen}>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="sm">
          <MoreVertical />
        </Button>
      </DropdownMenuTrigger>

      {/* ✅ 여기서 이벤트 전파 차단 */}
      <DropdownMenuContent
        onClick={(e) => e.stopPropagation()}
        align="end"
        className="w-[200px]"
      >
        {/* 아이템들 렌더링 */}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
```
onClick={(e) => e.stopPropagation()}를 통해 이벤트가 부모 div로 전파되지 않도록 막아줍니다.
그래서 부모 요소의 onClick은 호출되지 않고, 드롭다운 내부 기능만 안전하게 실행됩니다.


### 🧩 왜 자식에서 막아야 할까요?
브라우저 이벤트는 기본적으로 버블링 방식으로 동작합니다.
즉, 자식 → 부모로 이벤트가 전파되기 때문에, 자식에서 막아야 부모로 가지 않습니다.

- 자식에서 stopPropagation() ⭕
- 부모에서 stopPropagation() ❌ (이미 이벤트가 전파된 후라 무의미)


## 📌 어떤 상황에 써야 할까?

| 상황                                       | 사용 함수               |
| ---------------------------------------- | ------------------- |
| form 제출 막고 커스텀 처리하고 싶을 때                 | `preventDefault()`  |
| 자식 요소에서 발생한 클릭 이벤트가 부모까지 전달되지 않게 하고 싶을 때 | `stopPropagation()` |



## 마무리
기본 동작을 막고 싶은 건지(preventDefault()), 이벤트 전파(stopPropagation())를 막고 싶은 건지 목적에 따라 정확하게 구분해서 사용해야 합니다.
이 두 가지는 프론트엔드 개발에서 아주 자주 사용하는 필수 함수입니다.