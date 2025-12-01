## Zustand란?
React 전역 상태 관리 라이브러리 중 하나입니다.
Flux구조(명확한 단계를 가진 구조, flux는 패턴임)를 따르지 않고 (단방향 데이터 흐름이라는 철학은 동일), 상태를 직접 정의하고 함수형으로 다루는 간단한 방식으로 설계합니다.

- redux가 Flux에서 영감을 받아 만들어짐

| 항목            | Flux                        | Zustand                  |
| ------------- | --------------------------- | ------------------------ |
| 데이터 흐름        | 단방향                         | 단방향                      |
| 상태 변경 방식      | Action → Dispatcher → Store | `set` 함수로 바로 변경          |
| Action 필요     | ✅ 반드시 필요                    | ❌ 불필요                    |
| Dispatcher 필요 | ✅ 필수                        | ❌ 없음                     |
| Store         | 상태 + 변경로직                   | 상태 + `set` 함수            |
| 복잡도           | 비교적 복잡                      | 매우 단순                    |
| 상태 추적         | 명시적 (Action Log 등)          | 선택적 (devtools 미들웨어 활용 시) |


## 특징
- Minimal API: 몇 줄의 코드로 상태 생성 가능
- Redux 대체재로 많이 사용됨
- Immer 또는 devtools, persist 등의 미들웨어 확장 지원

### ✅ 장점

| 항목               | 설명                                 |
| ---------------- | ---------------------------------- |
| 🪶 가볍다           | Core가 1kb 미만으로 매우 작음               |
| 🧠 간단한 API       | `create`, `set`, `get` 기반의 직관적인 구조 |
| ⚡ 빠른 성능          | React Context보다 훨씬 빠른 성능  📌 React Context context value가 바뀌면 전체 하위 컴포넌트가 리렌더링됨.Zustand는 내부적으로 useSyncExternalStore 기반으로 최적화되어 있어, 필요한 컴포넌트만 리렌더함.          |
| 📦 선택적 구독        | 필요한 state만 구독하여 리렌더 최소화 📌 Zustand의 핵심 기능 중 하나. 상태 중 특정 값만 구독 가능 (useStore(s => s.count)) ↔️ redux는 Reac-Redux의 useSelector로 간접 구현가능          |
| 🔌 미들웨어 지원       | devtools, persist, immer 등 확장 가능   |
| ♻️ SSR 지원        | Next.js에서도 사용 가능 상태를 싱글턴으로 관리하지 않고 요청마다createStore() 하면, SSR에서도 안정적으로 동작함 ✅ Next.js + Zustand 조합은 널리 사용됨.⚠️ 서버에서 store 인스턴스를 공유하면 안 되므로 주의 필요.                |
| 👀 TypeScript 지원 | 타입 친화적이며 자동완성 편리                   |


### ❌ 단점

| 항목           | 설명                                  |
| ------------ | ----------------------------------- |
| 🔍 구조화 부재    | Redux보다 자유도가 높기 때문에 규모가 커질수록 구조 관리 어려움 Redux는 slice 구조를 통해 상태를 논리적으로 나눌 수 있지만, Zustand는 자유롭게 코드를 작성하는 만큼 store가 거대해지고 엉키기 쉬움. 📌 예시: 한 파일에 여러 비즈니스 로직이 섞이거나, 상태가 store 내에서 중복됨.  |
| 📚 학습 자료 적음  | 공식 문서는 좋지만 커뮤니티 자료는 Redux보다 적음      |
| 🔁 상태 추적 어려움 | 상태 흐름이 분산될 경우 디버깅이 어려움 📌devtools 미들웨어가 있지만 기능이 제한되어 있음              |
| 🚧 동시성 이슈    | 복잡한 로직에서는 `set` 병렬 호출 주의 필요 📌 예시: set()이 비동기 병렬로 여러 번 호출되면, 나중에 호출된 값이 이전 상태를 덮어쓸 수 있음.         |


## 1️⃣ 설치
```
npm install zustand 
또는
yarn add zustand
```

## 2️⃣ 기본 사용 예제

```create<T>()``` 형태

```
// countStore.ts
import { create } from 'zustand'

interface CounterState {
  count: number
  increase: () => void
  decrease: () => void
}

export const useCounterStore = create<CounterState>((set) => ({
  count: 0,
  increase: () => set((state) => ({ count: state.count + 1 })),
  decrease: () => set((state) => ({ count: state.count - 1 })),
}))
```

❗️미들 웨어를 사용 할 경우 
```create<T>()(...)``` 형태의 커링 방식**으로 사용해야함
zustand의 middleware들이 고차 함수 이기 때문 (시리즈 고차 함수와 커링 이란? 참고)

```
// countStore.ts
import { create } from 'zustand'

interface CounterState {
  count: number
  increase: () => void
  decrease: () => void
}

export const useCounterStore = create<CounterState>()(
  persist(
    (set) => ({
      count: 0,
      increase: () => set((state) => ({ count: state.count + 1 })),
      decrease: () => set((state) => ({ count: state.count - 1 })),
    }),
    {
      name: 'counter-storage', // localStorage에 저장될 key 이름
    }
  )
)

```
호출부
```
// Counter.tsx
import { useCounterStore } from './countStore'

function Counter() {
  const { count, increase, decrease } = useCounterStore()

  return (
    <div>
      <button onClick={decrease}>-</button>
      <span>{count}</span>
      <button onClick={increase}>+</button>
    </div>
  )
}

```

✅ 기타 옵션 및 확장(middleware)

1. devtools: 브라우저의 확장 프로그램(Redux DevTools)에 액션 로그,상태 등을 보내줌(디버깅용)

####  Redux DevTools 확장 프로그램 설치하기
- Chrome 웹스토어 접속
- Redux DevTools 확장 프로그램 페이지로 이동
- 확장 프로그램 설치
- 오른쪽 상단에 있는 “Chrome에 추가” 버튼 클릭
- 설치 확인 팝업에서 “확장 프로그램 추가” 선택
- 설치 완료: Chrome 브라우저 오른쪽 상단에 Redux DevTools 아이콘이 생김

1. DevTools 적용
```tsx
import { create } from 'zustand'
import { devtools } from 'zustand/middleware'

const useStore = create(devtools((set) => ({
  count: 0,
  increase: () => set((state) => ({ count: state.count + 1 })),
})))
```

2. persist: 로컬 스토리지에 상태 저장
```tsx
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const useStore = create(persist(
  (set) => ({
    username: '',
    setUsername: (name: string) => set({ username: name }),
  }),
  {
    name: 'user-storage', // localStorage key
  }
))
```

3. immter : 불변성 관리 (mutate처럼 써도 내부적으로 불변성 유지)
```tsx
import { create } from 'zustand'
import { immer } from 'zustand/middleware/immer'

const useStore = create(immer((set) => ({
  user: { name: '', age: 0 },
  updateName: (name: string) =>
    set((state) => {
      state.user.name = name
    }),
})))
```
4.선택적 구독 : (Selector): 불필요한 리렌더를 방지하기 위해 필요한 값만 구독 가능
```tsx
선택적 구독을 한 경우: const count = useCounterStore((state) => state.count)
전체 상태 구독을 한 경우: const count= useCounterStore();
```

