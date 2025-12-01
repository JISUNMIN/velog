> **React Query의 전역 설정과 자동 refetch 메커니즘을 한눈에 정리**  
> `defaultOptions`로 전역 정책을 통일하고, `staleTime`으로 데이터 신선도를 제어하자!


## 🔧 defaultOptions란?

`React Query`의 **전역 동작 방식을 정의**하는 핵심 설정입니다.  
이를 통해 모든 `useQuery`와 `useMutation` 훅의 기본 동작을 **일관되게 관리**할 수 있습니다.

```tsx
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5분 동안 fresh
      cacheTime: 1000 * 60 * 10, // 10분간 메모리에 유지
      refetchOnWindowFocus: true,
    },
    mutations: {
      retry: 0,
      onError: (error) => {
        toast.error(error.message || "요청 처리 중 오류가 발생했습니다.");
      },
    },
  },
});
```

## 🧩 캐시 정책 설계

- **staleTime** → 데이터의 신선도 유지 시간 (ms)  
- **gcTime** → 사용되지 않는 캐시가 메모리에 남는 시간 (ms)  

> 서비스 성격에 따라 다르게 설계해야 함

| 서비스 유형 | 설정 예시 |
| ------------ | ---------- |
| 실시간 서비스 | `staleTime: 0` |
| 안정성 중심 서비스 | `staleTime: 1000 * 60 * 5` (5분) |

---

## ⚙️ Mutation 전역 설정

### 🔁 retry  
요청 실패 시 재시도 횟수  
⚠️ **Mutation은 중복 요청 위험이 있으므로 일반적으로 `retry: 0` 권장**

### ❌ onError  
전역 에러 핸들링 콜백

```tsx
onError: (error) => {
  toast.error(error.message || "요청 처리 중 오류가 발생했습니다.");
};
```
이 설정을 통해 전역적으로** 일관된 요청 관리**가 가능합니다.

# 🧠 staleTime이란?

> **`staleTime` = 데이터가 언제까지 신선하다고 볼지 결정하는 시간**

`staleTime`이 길면 자동 refetch가 덜 일어나고, 짧으면 자주 일어납니다.

```tsx
useQuery(['users'], fetchUsers, {
  staleTime: 1000 * 60 * 5, // 5분 동안 fresh
});
```


| 트리거 | 설명 | staleTime 영향 |
| ------- | ---- | --------------- |
| 1️⃣ 컴포넌트 마운트 | 같은 쿼리를 가진 컴포넌트 재마운트 시 | stale일 때만 refetch |
| 2️⃣ 윈도우 포커스 복귀 | 다른 탭 → 현재 탭으로 복귀 시 | stale일 때만 refetch |
| 3️⃣ 네트워크 재연결 | 오프라인 → 온라인 전환 시 | stale일 때만 refetch |
| 4️⃣ 수동 호출 | `refetch()` / `invalidateQueries()` | 항상 refetch |
| 5️⃣ 폴링 | `refetchInterval` 설정 시 | interval마다 refetch |

---

## 🚫 refetch가 일어나지 않는 경우

| 상황 | 이유 |
| ---- | ---- |
| 데이터가 아직 fresh 상태 | `staleTime` 안 지남 |
| focus 이동, 페이지 이동 없음 | 트리거 자체 없음 |
| `refetchOnWindowFocus`, `refetchOnMount` 꺼둠 | 명시적 비활성화 |

---

## 🪟 Focus 이동이란?

브라우저 탭이나 창을 다른 곳으로 갔다가 **다시 돌아오는 순간**을 말합니다.  
React Query는 이 이벤트를 감지해 **stale 상태인 쿼리만 자동 refetch**합니다.

---

## 📦 예시 시나리오

### 1️⃣ 실시간 데이터

```tsx
useQuery(['users'], fetchUsers, { staleTime: 0 });
```

- **fetch 직후 즉시 stale 페이지 재진입 / 탭 포커스 시 자동 refetch**
- 항상 최신 데이터를 유지하기 위한 기본 동작

---

## ⚙️ 안정적 데이터 관리 예시

```js
useQuery(['users'], fetchUsers, { 
  staleTime: 1000 * 60 * 5 // 5분 동안 fresh 유지
});
```

- **5분 동안 fresh 유지**
- **5분 안에는 refetch 없음**
- **5분 후 stale → 다음 트리거 시 refetch 발생**

---

## ✅ 정리

| 구분 | 설명 |
|------|------|
| **queries** | 데이터를 **어떻게 읽을 것인지** |
| **mutations** | 데이터를 **어떻게 변경할 것인지** |
| **defaultOptions** | `queries`와 `mutations`의 전역 설정 통일 |
| **staleTime** | 자동 refetch 빈도를 제어하는 핵심 옵션 |
| **주요 트리거** | 마운트, 포커스 복귀, 네트워크 복귀 |
| **강제 refetch** | `invalidateQueries()` 사용 |



> 🔄 **React Query는 데이터가 stale일 때만 자동 refetch한다.**  
> `staleTime`이 짧을수록 자주, 길수록 덜 새로고침된다.