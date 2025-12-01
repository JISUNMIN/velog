**Zustand**를 사용하면서 꼭 이해해야 할 중요한 개념인 **전체 상태 구독(Subscription)** 과 **선택 구독(Selector Subscription)** 의 차이, 그리고 각각을 언제 어떻게 활용하면 좋은지 알아보겠습니다.

---

##  Zustand 구독(Subscription)이란?

Zustand에서는 상태를 사용할 때 `useStore` 훅을 통해 상태를 **구독(subscribe)** 하게 됩니다.  
이 구독은 특정 상태가 변경되었을 때 React 컴포넌트를 다시 **렌더링** 하도록 합니다.

예를 들어 아래처럼 특정 상태를 선택해서 구독할 수 있습니다.

```ts
const newComment = useCommentStore((state) => state.newComment);
```

또는 아래처럼 store 전체를 구독하고 필요한 값만 구조분해할 수도 있습니다.

```ts
const { newComment, setNewComment } = useCommentStore();
```

이둘은 리렌더링과 트리거 방식에서 차이가 있습니다.

##  전체 상태 구독과 선택 구독의 차이

### ✅ 전체 상태 구독
```ts
const { newComment, otherState } = useCommentStore();

```
위 코드는 **store 전체 상태를 구독하**는 방식입니다.
이렇게 작성하면 `useCommentStore()` 내부에서 store 전체를 구독하게 되어,
**store 내 어떤 값이라도 바뀌면 컴포넌트가 무조건 리렌더링됩니다.**

예를 들어 `newComment`는 그대로인데 `otherState`만 바뀌어도 이 컴포넌트는 다시 렌더링됩니다.

즉, 상태가 많거나 자주 바뀌는 앱이라면 불필요한 렌더링이 많이 발생할 수 있어 성능 저하로 이어질 수 있습니다.

### ✅ 선택 구독 (Selector 구독)
```ts
const newComment = useCommentStore((state) => state.newComment);
```

위와 같이 특정 상태만 구독하면, Zustand는 해당 상태(`newComment`)가 변경될 때만 이 컴포넌트를 리렌더링합니다.
다른 상태(`otherState` 등)가 바뀌더라도 이 컴포넌트는 **렌더링되지 않습니다.**

즉, **필요한 상태만 구독함으로써 성능을 최적화**할 수 있습니다.


## 왜 선택 구독이 중요할까?
아래는 상태 예시입니다.
```ts
const useCommentStore = create((set) => ({
  newComment: "",
  otherState: 0,
  setNewComment: (comment) => set({ newComment: comment }),
  setOtherState: (val) => set({ otherState: val }),
}));

```

전체 상태 구독 컴포넌트
```ts
const { newComment } = useCommentStore();
```
이 코드는 구조분해를 통해 newComment만 사용하는 것처럼 보이지만,
실제로는 store 전체를 구독하고 있기 때문에 otherState가 변경돼도 컴포넌트가 리렌더링됩니다.

선택 구독 컴포넌트
```ts
const newComment = useCommentStore((state) => state.newComment);
```
이 코드는 `newCommen`t만 구독하고 있습니다.
따라서 `otherState`가 변경돼도 이 컴포넌트는 전혀 영향을 받지 않고 렌더링도 발생하지 않습니다.

### 언제 전체 상태 구독을 써야 할까?
다음과 같은 상황에서는 전체 상태 구독을 사용해도 충분하거나, 오히려 간편할 수 있습니다.

- 상태가 몇 개 없고 단순한 경우
- 하나의 컴포넌트가 store의 여러 상태를 동시에 사용해야 하는 경우
- 초기 개발 단계에서 빠르게 UI를 구현해야 하는 경우
- 성능보다는 개발 편의성이 더 중요할 때

### 언제 선택 구독을 써야 할까?
선택 구독은 아래와 같은 상황에서 사용하면 좋습니다.

- store의 상태가 많고 자주 변경되는 대형 앱
- 특정 컴포넌트가 store 내 일부 상태만 필요할 때
- 불필요한 렌더링을 줄여 성능 최적화가 필요한 경우
- 컴포넌트를 여러 개로 쪼개고, 각 컴포넌트가 자기한테 필요한 상태만 가져다 쓸 때

| 구분           | 설명                               | 추천 방식                                   |
| ------------ | -------------------------------- | --------------------------------------- |
| 🔸 **선택 구독** | `store` 안에 있는 값 중 **일부만** 사용할 때  | `useCommentStore(state => state.필요한값)`  |
| 🔸 **전체 구독** | `store`에 있는 값의 **거의 대부분**을 사용할 때 | `const { a, b, c } = useCommentStore()` |

## Zustand 구독한 상태를 자식 컴포넌트로 넘길 때 고려할 점
React 상태관리 라이브러리인 Zustand를 사용할 때,  
부모 컴포넌트에서 구독한 상태를 자식 컴포넌트로 넘기는 경우가 많습니다.  
이때 어떻게 상태를 구독하고 전달하는지에 따라 앱 성능과 리렌더링 패턴에 큰 차이가 생깁니다.

### 1. 부모에서 전체 상태를 구독하고 자식에게 넘기는 경우

```tsx
const Parent = () => {
  const { state1, state2, state3 } = useStore();

  return <Child state1={state1} state2={state2} />;
};
```
- 부모 컴포넌트는 store의 전체 상태를 구독합니다.
- state1, state2, state3 중 하나라도 변경되면 부모가 리렌더링되고,
- 이로 인해 자식 컴포넌트도 리렌더링 됩니다.

### ⚠️ 문제점 
자식이 사용하지 않는 상태(state3)가 변경되어도
부모와 자식 컴포넌트가 모두 리렌더링될 수 있어 불필요한 렌더링 발생합니다.

### 2. 부모에서 선택 구독으로 필요한 상태만 구독해서 자식에게 넘기는 경우

```tsx

const Parent = () => {
  const state1 = useStore((state) => state.state1);
  const state2 = useStore((state) => state.state2);
  const state3 = useStore((state) => state.state3);

  return (
    <>
      <ChildA state1={state1} state2={state2} />
      <ChildB state3={state3} />
    </>
  );
};
```
**state1이나 state2가 바뀌면 ChildA만 리렌더링**,
**state3가 바뀌면 ChildB만 리렌더링** 됩니다.

결론은 부모가 자식에게 상태를 props로 넘길 때는 **'선택 구독'**을 사용해야 불필요한 리렌더링을 줄일 수 있습니다. 

>참고 자식들이 독립적으로 상태를 직접 사용해야 하고, 리렌더링 분리가 중요한 경우에는
자식 컴포넌트에서 직접 Zustand 상태를 선택 구독해서 사용하는 방법도 있습니다.


## 📝 마치며


앱의 규모가 작거나 상태 변경이 드문 경우에는 전체 상태 구독만으로도 충분합니다.
하지만 앱이 커지거나 성능 최적화가 중요한 상황에서는 선택 구독을 통해 불필요한 렌더링을 줄이는 것이 중요합니다.

