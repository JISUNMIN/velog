React 프로젝트를 하다 보면 불필요한 리렌더링 때문에 성능 최적화를 고민하게 됩니다.
저도 input 한 글자를 입력할 때마다 모든 컴포넌트가 다시 렌더링되는 문제를 겪었습니다....😅
그때 React.memo, useMemo, useCallback을 알고는 있었지만, 이번에 더 깊이 찾아보면서 개선해 나가는 과정에서 이 도구들의 중요성을 제대로 알게 되었습니다.

이 글에서는 헷갈리기 쉬운 이 개념들을 예시와 함께 정리했습니다.



---

## 1. 🛡️ React.memo

### 역할
`React.memo`는 **props가 바뀌지 않으면 컴포넌트를 다시 안 그리게(리렌더링 안 하게)** 해줍니다.

### 기본 사용 예시

```tsx
const MyButton = ({ text }: { text: string }) => {
  console.log("MyButton 렌더링");
  return <button>{text}</button>;
};

export default React.memo(MyButton);
```

부모 컴포넌트가 렌더링돼도 `text` 값이 같으면 다시 렌더링되지 않습니다.

---

### ❗ React.memo만으로 막지 못하는 리렌더링 (shallow compare)
`React.memo`는 props가 이전과 같으면 리렌더링을 막아주지만,  
**비교 방식이 "얕은 비교(shallow compare)"** 라서 다음과 같은 특징이 있습니다.

- **🔹 원시 타입 (number, string, boolean)**  
  값 자체를 비교하기 때문에, 값이 같으면 리렌더링이 발생하지 않습니다.
- ** 🔸 참조 타입 (객체, 배열, 함수))**  
  렌더링될 때마다 새로운 참조(주소)가 생기므로 이전 값과 달라졌다고 판단 → **리렌더링 발생**

```tsx
<KanbanColumnHeader
  status="TODO"
  isDark={false}
  columnIndex={0}
  onCreateTask={() => {}}  // 매번 새로 만들어지는 함수
  options={{ filter: true }} // 매번 새 객체 생성
  tags={["urgent", "bug"]}  // 매번 새 배열 생성
/>
```

---

### ✨ 해결 방법

#### 1. 객체/배열은 useMemo로 참조 고정

```tsx
const options = useMemo(() => ({ filter: true }), []);
const tags = useMemo(() => ["urgent", "bug"], []);

<KanbanColumnHeader
  status="TODO"
  isDark={false}
  columnIndex={0}
  options={options}
  tags={tags}
/>
```

#### 2. 함수는 useCallback으로 참조 고정

```tsx
const handleCreateTask = useCallback(() => {
  console.log("task created");
}, []);

<KanbanColumnHeader onCreateTask={handleCreateTask} />
```

| 타입       | 비교 방식     | 문제점                      | 해결법                 |
| ---------- | ------------ | --------------------------- | ---------------------- |
| 원시타입   | 값 비교       | 없음                        | -                      |
| 객체/배열  | 참조 주소 비교 | 매번 새로운 참조라 리렌더링 | `useMemo`로 참조 고정  |
| 함수       | 참조 주소 비교 | 매번 새로운 함수 생성       | `useCallback`으로 고정 |

---

## 2. React.memo + 🔍비교 함수 (areEqual)

`React.memo` 두 번째 인자로 **비교 함수를 직접 작성**할 수 있습니다.

```tsx
const TaskItem = ({
  columnKey,
  itemIndex,
  task,
}: {
  columnKey: string;
  itemIndex: number;
  task: any;
}) => {
  console.log("TaskItem 렌더링");
  return <div>{task.title}</div>;
};

export default React.memo(TaskItem, (prev, next) => prev.task === next.task);
```

- **prev**: 이전 props
- **next**: 새로운 props

이렇게 하면 `task` 객체만 비교(얕은비교)해서 같으면 리렌더링 안 합니다.

복잡한 컴포넌트에서 **중요한 props만 비교하고 싶을 때** 유용합니다.
이 경우에도** task가 객체, 배열, 함수 등 참조 타입이라면, 매 렌더링마다 새로운 참조가 생성될 수 있습니다.**
**부모 컴포넌트에서 useMemo, useCallback, 혹은 React.memo로 참조를 고정해주어야 합니다.**
그렇지 않으면 비교 함수가 같지 않다고 판단해 자식 컴포넌트가 불필요하게 리렌더링됩니다.

---

## 3. 💾 useMemo로 JSX나 값 메모이제이션

```tsx
const sidebar = useMemo(() => <KanbanSidebar />, []);
const trigger = useMemo(() => <SidebarTrigger />, []);
```

JSX도 결국 객체라서 매번 새로 만들면 참조가 바뀝니다.  
`useMemo`를 사용해 고정하면 불필요한 리렌더링을 방지할 수 있습니다.

또한, 무거운 계산식 결과를 저장해 **계산량을 줄이는 용도**로도 자주 씁니다.

하지만, 내부에 상태, 훅, 라우터, 데이터 페칭 등 동적인 요소가 포함된 컴포넌트는 매 렌더 시 최신 상태를 반영해야 하므로, JSX를 useMemo로 감싸는 것이 오히려 부작용이나 상태 반영 누락의 원인이 될 수 있어 주의해야 합니다.

일반적으로는 useMemo로 JSX를 메모이제이션하는 것보다, React.memo를 활용해 컴포넌트 자체의 재렌더링을 제어하는 편이 더 권장됩니다.

---

## useCallback

`useCallback`은 **함수를 메모이제이션**합니다.

주로 이벤트 핸들러나 effect 의존성에 넣을 함수에 사용합니다.

```tsx
const handleClick = useCallback(() => {
  console.log("clicked");
}, []);
```

---

## 실전 최적화 예시

### 🔄 최적화 전

```tsx
function App() {
  return (
    <KanbanColumnHeader
      status="TODO"
      isDark={false}
      columnIndex={0}
      onCreateTask={() => {}} // 새 함수
    />
  );
}
```

부모가 리렌더링될 때마다 `onCreateTask`가 새로 생성 → `KanbanColumnHeader`가 매번 리렌더링

### 🔄 최적화 후

```tsx
const handleCreateTask = useCallback((status, idx) => {
  console.log(status, idx);
}, []);

return (
  <KanbanColumnHeader
    status="TODO"
    isDark={false}
    columnIndex={0}
    onCreateTask={handleCreateTask}
  />
);
```

`onCreateTask` 참조가 고정 → props가 변하지 않아 자식은 다시 안 그림

---

## 📚 React.memo 사용 방법 정리

| 방법 | 설명 | 사용 여부 |
|------|------|-----------|
| 1. 별도 컴포넌트 정의 후 memo 감싸기 | `const Comp = (props) => {}; export default React.memo(Comp)` | 가장 일반적 |
| 2. memo에 비교 함수 넣기 | `export default React.memo(Comp, 비교함수)` | **세밀하게 제어 가능** |

---

## ✅ 핵심 정리

- **React.memo**  
  > "props가 같으면 다시 안 그리고 싶을때"

- **비교 함수 (prevProps, nextProps)**  
  > "내가 원하는 방식으로 비교할때"

- **useMemo**  
  > "값/JSX를 기억해두고 재사용할때"

- **useCallback**  
  > "함수 참조를 고정시킬때"

### 언제 사용해야 할까?
- **부모에서 자식으로 props로 함수/객체/배열을 넘길 때** → `useCallback`, `useMemo`
- **자식 컴포넌트 자체 최적화** → `React.memo`
- **불필요한 연산 최적화** → `useMemo`, `useCallback`

이렇게 최적화를 적용하면 불필요한 리렌더링을 줄이고 성능을 향상시킬 수 있습니다.


## 📝 마무리 
useMemo와 useCallback은 주로 자식 컴포넌트에 props로 객체, 배열, 함수 등을 넘길 때 참조를 고정해서 불필요한 자식 리렌더링을 막기 위해 많이 사용됩니다.

하지만 이 둘은 단지 자식에게 props를 넘길 때만 쓰이는 것이 아니라,  

- 부모 컴포넌트 내부에서 무거운 계산 결과를 메모이제이션해 성능을 최적화하거나,  
- 이벤트 핸들러 같은 함수를 매 렌더링마다 새로 만들지 않고 재사용하는 경우에도 매우 효과적입니다.

즉, useMemo와 useCallback은 자식 컴포넌트에 props로 넘길 때뿐만 아니라, 부모 컴포넌트 내에서 불필요한 계산이나 함수 재생성을 방지하는 데에도 널리 활용할 수 있습니다.


