React Query를 사용할 때 아래와 같은 코드를 자주 작성합니다.

```tsx
const App = () => {
  const queryClient = new QueryClient()
  return (
    <QueryClientProvider client={queryClient}>
      <Routes />
    </QueryClientProvider>
  )
}
```

겉보기에는 아무런 문제가 없어 보입니다.  
하지만 이 코드는 **App 컴포넌트가 리렌더링될 때마다 새로운 QueryClient 인스턴스가 생성되는 구조**입니다.  
지금은 문제가 드러나지 않더라도, 나중에는 **캐시 초기화나 불필요한 네트워크 요청**과 같은 문제가 발생할 수 있습니다.

---

## 💥 왜 문제가 되는가?

`QueryClient`는 React Query의 **쿼리 캐시와 전역 상태를 관리하는 핵심 객체**입니다.  
이 객체가 새로 만들어지면 내부에 저장된 캐시 데이터가 모두 사라집니다.

즉, `App`이 리렌더링될 때마다 `new QueryClient()`가 실행되면 다음과 같은 현상이 발생합니다.

- 기존 쿼리 캐시가 초기화됩니다.  
- 진행 중이던 fetching이 중단됩니다.  
- React Query Devtools 연결이 끊깁니다.  
- 화면이 순간적으로 로딩 상태로 깜빡입니다.

---

## 🤔 “App은 거의 리렌더링되지 않지 않나요?”

맞습니다.  
일반적으로 `App` 컴포넌트는 자주 리렌더링되지 않습니다.  
그러나 **절대 리렌더링되지 않는다는 보장은 없습니다.**

다음과 같은 상황에서는 `App`이 언제든 다시 렌더링될 수 있습니다.

| 상황 | 설명 |
|------|------|
| 🔄 App 내부에서 useState 사용 | 테마 변경, 모달 상태 제어 등 |
| 🔗 전역 상태 구독 | Recoil, Zustand, Redux 값 변경 시 |
| 🌐 Provider 값 변경 | i18next, ThemeProvider 등 컨텍스트 갱신 시 |
| 🚧 ErrorBoundary/Suspense 복구 | UI 전환 시 컴포넌트 재마운트 |
| 🧑‍💻 개발 환경 | React StrictMode의 이중 마운트, HMR(Hot Reload) |

위와 같은 상황이 발생하면,  
`App` 내부에서 새롭게 생성된 `QueryClient`로 인해 **캐시가 매번 초기화되는 문제**가 생깁니다.

---

## ✅ 올바른 방법: 싱글톤으로 분리하기

`QueryClient`는 애플리케이션 생명주기 전체에서 **한 번만 생성**하면 충분합니다.  
따라서 아래와 같이 별도의 파일로 분리하여 “싱글톤” 형태로 관리하는 것이 좋습니다.

```tsx
// queryClient.ts
import { QueryClient, QueryCache, MutationCache } from "@tanstack/react-query"

export const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: (error, query) => {
      console.warn("[Query Error]", query?.queryKey, error)
    },
  }),
  mutationCache: new MutationCache({
    onError: (error, variables, context, mutation) => {
      console.warn("[Mutation Error]", mutation?.options?.mutationKey, error)
    },
  }),
  defaultOptions: {
    queries: {
      retry: 1,
      staleTime: 5 * 60 * 1000,
      gcTime: 30 * 60 * 1000,
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: 0,
    },
  },
})
```

`App`에서는 위에서 생성한 `queryClient`를 주입하기만 하면 됩니다.

```tsx
import { QueryClientProvider } from "@tanstack/react-query"
import { queryClient } from "./queryClient"

const App = () => (
  <QueryClientProvider client={queryClient}>
    <Routes />
  </QueryClientProvider>
)

```

# 🧩 useRef를 이용한 대안

`QueryClient`를 외부 파일로 분리하기 어렵다면, **useRef**를 사용하여 컴포넌트 내부에서 한 번만 생성하도록 관리할 수도 있습니다.  
useRef는 React에서 컴포넌트 내에서 변경 가능한 참조값을 관리할 때 사용하는 Hook입니다.

---

## 🧠 [useRe](https://velog.io/@sunmins/React-Hook-useRef-%EC%A0%9C%EB%8C%80%EB%A1%9C-%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0)f란?
- **렌더링과 무관하게 값 유지**  
- **DOM 접근** 또는 **렌더링에 영향을 주지 않는 값**을 저장할 때 사용  
- 상태(`state`)와 달리 값이 변경되어도 렌더링을 트리거하지 않음

```tsx
const queryClientRef = useRef<QueryClient>()
if (!queryClientRef.current) {
  queryClientRef.current = new QueryClient()
}
```

이렇게 작성하면 `App`이 리렌더링되더라도 `QueryClient`가 새로 생성되지 않고 **처음 생성된 인스턴스가 그대로 유지**됩니다.

## ✅ 정리

| 방식                                        | 설명        | 결과               |
| ----------------------------------------- | --------- | ---------------- |
| ❌ `new QueryClient()`                     | 매 렌더마다 실행 | 🚨 캐시 초기화 (비효율적) |
| ⚠️ `useMemo(() => new QueryClient(), [])` | 의존성 주의 필요 | 재생성 가능성 존재       |
| ✅ `useRef` 또는 모듈 스코프 싱글톤                  | 한 번만 생성   | 안정적 / 권장 방식      |


React Query의 핵심은 **“지속적인 캐시 관리”**입니다.  
이를 안정적으로 유지하려면 **QueryClient는 애플리케이션 전체에서 한 번만 생성**되어야 합니다.

따라서,  
- App 내부에서 매번 새 인스턴스를 생성하지 말고,  
- **싱글톤 패턴** 또는 **useRef를 활용한 1회 생성 방식**으로 관리하는 것이 좋습니다.

일반적인 웹앱(CSR)에서는 **싱글톤 패턴**이 가장 안정적이고 권장됩니다.  
**useRef**는 독립된 컴포넌트 단위로 캐시를 관리해야 할 때 유용합니다.
(예: 테스트나 작은 위젯처럼, 다른 곳과 캐시를 공유할 필요가 없을 때)



