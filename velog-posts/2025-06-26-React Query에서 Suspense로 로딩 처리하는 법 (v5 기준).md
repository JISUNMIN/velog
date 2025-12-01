React Query를 쓰다 보면 이런 로딩 처리 코드를 자주 작성하게 됩니다.

```tsx
const { data, isLoading } = useQuery(...);

if (isLoading) return <div>로딩 중...</div>;
```

하지만 React의 Suspense를 활용하면 위 조건문 없이도 훨씬 깔끔하게 로딩 처리를 할 수 있습니다.

---

## 🤔 Suspense를 쓰면 isLoading 체크를 안 해도 될까?

- `useSuspenseQuery`를 사용하면 데이터가 준비되지 않은 동안 React가 자동으로 fallback UI를 보여줍니다.
- 따라서 다음과 같은 코드가 불필요해집니다.

```tsx
if (!isLoading) return <div>로딩 중</div>;
```


## 💥 문제
 useQuery에 다음과 같이 suspense: true 옵션을 넣었더니…

```tsx
  const {
    data: listData,
    isPending: isListPending,
    isFetching: isListFetching,
  } = useQuery<Project[], Error>({
    queryKey: ["projects", "list"],
    queryFn: async () => {
      const res = await axios.get<Project[]>(PROJECT_API_PATH);
      return res.data;
    },
    enabled: !targetId,
    suspense: true,
  });

```
❗ React Query v5부터는 suspense 옵션이 제거되었습니다.



## ✅ 해결 방법: useSuspenseQuery 사용
React Query v5부터는 Suspense를 쓰고 싶다면 useSuspenseQuery() 훅을 사용해야 합니다.

```tsx

import { useSuspenseQuery } from "@tanstack/react-query";

 const {
    data: listData,
    isPending: isListPending,
    isFetching: isListFetching,
  } = useSuspenseQuery<Project[], Error>({
    queryKey: ["projects", "list"],
    queryFn: async () => {
      const res = await axios.get<Project[]>(PROJECT_API_PATH);
      return res.data;
    },
  });
```
그리고 해당 hook을 사용하는 컴포넌트를 반드시 <Suspense>로 감싸야 합니다:
 예시) ProjectList에서 listData를 사용한다고 할때

```tsx
import { Suspense } from "react";
import ProjectList from "./ProjectList";

export default function Page() {
  return (
    <Suspense fallback={<div>로딩 중...</div>}>
      <ProjectList />
    </Suspense>
  );
}
```


## ❓ 각기 다른 fallback UI를 쓰고 싶다면?

기본적으로 Suspense는 같은 fallback을 공유하지만,

```tsx
export default function Page() {
  return (
    <>
      <Suspense fallback={<div>📄 프로젝트 목록 불러오는 중...</div>}>
        <ProjectList />
      </Suspense>

      <Suspense fallback={<div>🧩 태스크 보드 불러오는 중...</div>}>
        <KanbanBoard />
      </Suspense>
    </>
  );
}
```

이렇게 컴포넌트별로 `<Suspense>`를 따로 감싸서 다른 fallback UI를 지정할 수 있습니다.



# ⚠️ `useSuspenseQuery`와 `enabled` 옵션 사용 관련 정리 (중요!)

- `useSuspenseQuery` 훅은 React Query의 Suspense 기능과 연동되어 동작합니다.  
- Suspense는 데이터가 준비될 때까지 UI를 대기시키는 방식으로, 쿼리가 반드시 실행되어야 정상적으로 작동합니다.  

---

### 그래서…

- `enabled` 옵션처럼 **쿼리 실행 여부를 제어하는 기능은 `useSuspenseQuery`에서 지원하지 않습니다.**  
 ### 즉, `useSuspenseQuery`를 쓸 때는 쿼리를 **항상 실행하는 상황**이어야 합니다.  

---

### 그렇지 않은 경우에는?

- 쿼리 실행을 조건에 따라 제어해야 한다면, Suspense 대신 일반적인 `useQuery`를 사용해야 합니다.  
- 이때는 `enabled` 옵션과 함께 `isLoading`, `isFetching` 상태를 이용해 로딩 처리를 직접 구현해야 합니다.  

---

### 요약

| 상황                             | 추천 사용법               |
| ------------------------------ | ------------------------ |
| 쿼리를 항상 실행해야 하는 경우    | `useSuspenseQuery` 사용 + Suspense로 감싸기  |
| 쿼리 실행 조건이 필요한 경우       | `useQuery` + `enabled` + `isLoading` 처리  |

---



### 🔗 참고 자료
>TanStack Query Docs - [useSuspenseQuery](https://tanstack.com/query/latest/docs/framework/react/reference/useSuspenseQuery)
 React Docs - [Suspense](https://react.dev/reference/react/Suspense)