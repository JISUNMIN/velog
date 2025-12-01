React Query는 **서버 상태(server state)** 를 쉽게 관리할 수 있도록 도와주는 라이브러리로
API 호출, 데이터 캐싱, 자동 갱신, 에러 처리 등 서버와 주고받는 데이터를 편리하게 관리할 수 있게 함.

❓ 왜 React Query를 사용할까?

- API 데이터 fetching과 관련된 반복적인 로직을 줄일 수 있다.
- 서버 데이터 캐싱으로 불필요한 재요청을 줄여 성능 향상.
- 자동으로 데이터 최신화(refetching) 기능 제공.
- 로딩, 에러 상태 관리가 편리하다.
- 페이지 간 이동 시 서버 상태를 유지해 UX 개선.

#### 기본 사용법
📦 1. 설치
```
npm install @tanstack/react-query
```
⚙️ 2. QueryClient와 Provider 세팅
```
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <YourComponent />
    </QueryClientProvider>
  )
}
```
🪝 3. 커스텀 훅에 useQuery(데이터 조회),useMutation(데이터 변경:POST,PUT) 사용하기
```
const useLogin = () => {
  const router = useRouter();
  const { login } = useAuthStore();

  const { mutate: loginMutation, isPending } = useMutation({
    mutationFn: async (data: LoginFormInputs) => {
      const res = await axios.post(API_PATH, data);
      return res.data;
    },
    onSuccess: (result) => {
      login({ userId: result.userId });
      showToast({ type: ToastMode.SUCCESS, action: "SAVE" });

      router.replace("/dashboard/kanban");
    },
    onError: (error: any) => {
      const message =
        error.response?.data?.error || "서버와 통신 중 오류가 발생했습니다.";
      showToast({ type: ToastMode.ERROR, action: "SAVE", content: message });
      console.error(error);
    },
  });

  return {
    loginMutation,
    isPending,
  };
};
```
🧑‍💻 4. 컴포넌트에서 커스텀 훅 호출해 데이터 사용하기
```
export default function LoginForm() {
  const { loginMutation } = useLogin();
  
    const onSubmit = async (data: LoginFormInputs) => {
    loginMutation(data);
  };
 }

````

### 💡React Query 주요 함수 
주요 함수들인 useQuery, useMutation 등은 서버 상태(fetching, 캐싱, 업데이트)를 관리하는데 핵심 역할을 함

| 함수명                  | 역할                                   | 주요 옵션 및 특징                                                                                       | 간단 설명                               |
| -------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------ | ----------------------------------- |
| **useQuery**         | 서버에서 데이터를 가져오고 캐싱함                   | `queryKey`, `queryFn`, `enabled`, `staleTime`, `cacheTime`, `refetchOnWindowFocus`, `suspense` 등 | GET 요청 등 읽기 작업에 주로 사용               |
| **useMutation**      | 서버에 데이터를 생성, 수정, 삭제하는 작업 수행          | `mutationFn`, `onSuccess`, `onError`, `onSettled` 등                                              | POST, PUT, DELETE 요청 등 쓰기 작업에 주로 사용 |
| **useInfiniteQuery** | 페이지네이션 혹은 무한 스크롤 데이터 요청              | `getNextPageParam`, `getPreviousPageParam` 등                                                     | 여러 페이지 데이터(배치)를 불러올 때 사용            |
| **useQueries**       | 여러 개의 쿼리를 병렬로 실행                     | 배열 형태로 여러 `queryKey`, `queryFn`를 받음                                                              | 여러 독립된 쿼리를 동시에 요청할 때 사용             |
| **useIsFetching**    | 현재 fetch 중인 쿼리 개수를 알려줌               | 없음                                                                                               | 글로벌 로딩 상태 표시할 때 사용                  |
| **useQueryClient**   | QueryClient 인스턴스를 반환하여 수동으로 캐시 조작 가능 | 없음                                                                                               | 쿼리 무효화, 데이터 업데이트 등 직접 제어            |

**⭐ useQuery Client**는 데이터를 등록,수정,삭제(CUD)하고 난 후 데이터를 재 조회할때 사용
ex) 공지사항 등록 후 조회화면 진입 시 공지사항이 추가되야하는 경우 
useQuery로 불러온 list의 queryKey와 ueryClient.invalidateQueries에 넣어주는 queryKey의 값이 같아야 동작함
```
  const queryClient = useQueryClient();

  const {
    data: listData,
    isPending: isListPending,
    isFetching: isListFetching,
  } = useQuery<Response, Error>({
    queryKey: ['notice'],
    queryFn: async () => {
      const response = await Api.get<Response>(`${API_PATH}/retrieveList`, {
        config: {
          params: { countryDiv: countryDiv?.code },
        },
      });
      return response.data;
    },
    enabled: !noticeId,
  });

  
  const { mutate: registMutation } = useMutation<void, Error, Type>({
    mutationFn: async (data) => {
      await Api.post(`${API_PATH}/create`, {
        data,
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notice'] });
    },
    onError: () => {
    },
  });
```


###  🆚 React Query를 커스텀 훅에서 사용하는 방식 vs 컴포넌트 안에서 직접 사용하는 방식

#### 1. 커스텀 훅에서 React Query 사용하기
📁 hooks/useLogin.ts

```
import { useMutation } from '@tanstack/react-query';
import { toast } from 'react-toastify';

export function useLogin() {
  const { mutate: loginMutate, isPending, isError, error } = useMutation({
    mutationFn: async (data: LoginFormInputs) => {
      const res = await axios.post(API_PATH, data);
      return res.data;
    },
    onSuccess: (data) => {
      toast.success('로그인 성공!');
      // 예: token 저장, redirect 등
    },
    onError: (error) => {
      toast.error('로그인 실패');
    },
  });

  return { loginMutate, isPending, isError, error };
}

📁 pages/LoginPage.tsx

import { useLogin } from '@/hooks/useLogin';
import { useState } from 'react';

export default function LoginPage() {
  const { loginMutate, isPending } = useLogin();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {
    loginMutate({ email, password });
  };

  return (
    <div>
      <input value={email} onChange={(e) => setEmail(e.target.value)} />
      <input value={password} onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleLogin} disabled={isPending}>
        {isPending ? '로그인 중...' : '로그인'}
      </button>
    </div>
  );
}

```

✅ 장점 요약
- 컴포넌트는 UI에만 집중
- 로그인 로직, 에러처리, 토스트 등 분리
- 로그인 요청을 다른 컴포넌트에서도 재사용 가능

❌ 단점
- 복잡한 제어가 필요한 경우나 다양한 UI 상황에 대응해야 할 때는 단점이 생길 수 있음
: **동적 분기 처리 어려움(보안 방법 -절충안 2 참고), onSuccess, onError같은 핸들러를 직접 넘기기 어려움 (보안 방법 -절충안 1 참고)**

#### 2. 컴포넌트에서 직접 사용하는 방식
📁 pages/LoginPage.tsx
```
import { useMutation } from '@tanstack/react-query';
import { useState } from 'react';
import { toast } from 'react-toastify';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const { mutate: loginMutate, isPending } = useMutation({
    mutationFn: async (data: LoginFormInputs) => {
      const res = await axios.post(API_PATH, data);
      return res.data;
    },
    onSuccess: () => {
      toast.success('로그인 성공!');
    },
    onError: () => {
      toast.error('로그인 실패');
    },
  });

  const handleLogin = () => {
    loginMutate({ email, password });
  };

  return (
    <div>
      <input value={email} onChange={(e) => setEmail(e.target.value)} />
      <input value={password} onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleLogin} disabled={isPending}>
        {isPending ? '로그인 중...' : '로그인'}
      </button>
    </div>
  );
}

```
✅ 장점 요약
- 별도 훅 없이 간단하게 바로 요청 가능
- 컴포넌트 파일 하나로 빠르게 구현 가능

❌ 단점
- 로직이 컴포넌트에 섞여서 가독성 떨어짐
- 다른 페이지에서 똑같은 로그인 로직이 필요할 때 중복됨
- 토스트나 리디렉션 로직도 매번 써야 함

####  절충안 1: 옵션 인자로 콜백 주입 (onSuccess, onError 등)
```
// useLogin.ts
import { useMutation } from '@tanstack/react-query';
import { loginApi } from '@/apis/auth';

interface UseLoginOptions {
  onSuccess?: () => void;
  onError?: (error: unknown) => void;
}

export function useLogin(options?: UseLoginOptions) {
  return useMutation({
    mutationFn: loginApi,
    onSuccess: () => {
      console.log('로그인 성공');
      options?.onSuccess?.();
    },
    onError: (err) => {
      console.error('에러 발생');
      options?.onError?.(err);
    },
  });
}

// LoginPage.tsx
const { mutate: loginMutate, isPending } = useLogin({
  onSuccess: () => toast.success('로그인 성공!'),
  onError: () => toast.error('로그인 실패...'),
});

loginMutate({ id: 'abc', pw: '1234' });

✅ 장점: 재사용성 유지하면서도 상황별 콜백 처리 가능
⚠️ 주의: 옵션 구조를 일관되게 유지해야 관리가 쉬움

```

####  절충안 2: 쿼리 조건부 실행 제어 (enabled, skip, lazy)
```
// useUser.ts
export function useUser(userId?: string, enabled = true) {
  return useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId!),
    enabled: !!userId && enabled, // userId 없으면 실행 안함
  });
}

// UserInfo.tsx
const userId = searchParams.get('userId');
const { data, isPending } = useUser(userId);

✅ 장점: 조건부 요청도 제어 가능
⚠️ 주의: enabled나 suspense, placeholderData 등 react-query를 잘 알아야 함(react-query에서 자주 쓰이는 옵션 참고)
```

####  절충안 3: 쿼리 함수 자체를 외부로 분리 (테스트 및 재사용성 강화)

```
// api/fetchUser.ts
export const fetchUser = async (userId: string) => {
  const res = await Api.get(`/users/${userId}`);
  return res.data;
};

// useUser.ts
import { useQuery } from '@tanstack/react-query';
import { fetchUser } from '@/api/fetchUser';


❌ useQuery(['user', userId], asyncFn, options) ← v4 스타일
✅ v5부터는 무조건 객체 형태로 인자를 넘겨야 합니다. 밑에 예제는 v5이상 부터 에러남
export function useUser(userId: string) {
  return useQuery(['user', userId], () => fetchUser(userId), {
    enabled: !!userId,
  });
}
```

#### 📋 react-query에서 자주 쓰이는 옵션

| 옵션명                    | 타입                       | 기본값                  | 설명                                      | 사용 예시 및 특징                                 |
| ---------------------- | ------------------------ | -------------------- | --------------------------------------- | ------------------------------------------ |
| `enabled`              | `boolean`                | `true`               | 쿼리 활성화 여부 설정<br> `false`면 자동 실행 안 함     | `enabled: !!userId`처럼 조건부 데이터 요청할 때 사용     |
| `staleTime`            | `number` (ms)            | `0`                  | 데이터 신선도 유지 시간<br> 이 시간 안에 재요청 없으면 캐시 사용 | `staleTime: 5 * 60 * 1000` (5분) 캐싱 강화      |
| `cacheTime`            | `number` (ms)            | `5 * 60 * 1000` (5분) | 데이터 캐시 유지 시간                            | 사용하지 않는 쿼리 캐시 삭제 시점 조정 가능                  |
| `refetchOnWindowFocus` | `boolean` 또는 `'always'`  | `true`               | 브라우저 창 다시 활성화 시 데이터 재요청 여부              | 사용자가 탭 전환 후 최신 데이터 필요할 때 유용                |
| `retry`                | `number` 또는 `boolean`    | `3`                  | 실패 시 재시도 횟수 또는 재시도 여부                   | `retry: false` 재시도 끄기, `retry: 1` 한 번만 재시도 |
| `suspense`             | `boolean`                | `false`              | React Suspense와 연동하여 로딩 처리              | `suspense: true` + `<Suspense>` 컴포넌트 필요    |
| `placeholderData`      | `T` (임시 데이터)             | `undefined`          | 데이터 로딩 중 보여줄 임시 데이터                     | `placeholderData: { name: '로딩중...' }`      |
| `initialData`          | `T`                      | `undefined`          | 쿼리 초기 데이터 (캐시에 저장됨)                     | 초기값 세팅용, 서버에서 SSR로 받은 초기 데이터 주입 가능         |
| `refetchInterval`      | `number` (ms) 또는 `false` | `false`              | 주기적 데이터 자동 재요청 간격                       | 실시간 데이터 필요 시 설정 (ex: 10000 = 10초마다 재요청)    |
| `onSuccess`            | `function`               | -                    | 쿼리 성공 시 콜백                              | 데이터 도착 후 추가 작업할 때 사용                       |
| `onError`              | `function`               | -                    | 쿼리 실패 시 콜백                              | 에러 처리 로직 구현 시 사용                           |
