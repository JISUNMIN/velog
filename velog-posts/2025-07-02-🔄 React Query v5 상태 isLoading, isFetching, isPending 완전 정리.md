React Query를 쓰다 보면 헷갈리는 상태 값들이 있습니다.

특히 `isLoading`, `isFetching`, `isPending` 이 세 가지는 비슷하게 생겼지만, 의미도 다르고 쓰임도 다릅니다.  
이번 글에서는 `React Query v5 기준`으로 각각의 차이점과 실제로 어떤 상황에서 무엇을 써야 하는지 정리해보겠습니다.

---

## 💡 상태 요약 정리표

| 이름         | 주로 사용하는 훅 | 설명 |
|--------------|------------------|------|
| `isLoading`  | `useQuery`       | 캐시가 없고, 첫 데이터 fetch 중일 때 `true` |
| `isFetching` | `useQuery`       | 캐시 유무와 관계없이 fetch 중이면 `true` |
| `isPending`  | `useMutation`    | `mutate` 실행 중이면 `true` (`v5에서 새로 도입된 용어) |

---

## 📌 가장 많이 쓰이는 건?

실제로 가장 많이 쓰이는 건 **`isLoading`**입니다.  
왜냐하면, **데이터가 아예 없을 때 로딩 상태를 보여주기 적합 하기 때문입니다.**
또한, `isFetching`도  많이 쓰입니다.
특히 이미 화면에 데이터가 있는 상태에서 백그라운드로 데이터를 재요청하는 경우,
isFetching을 이용해 "새로고침 중" 표시나 UI 상태 변화를 관리하는 것이 일반적입니다.

```tsx
const { data, isLoading, isFetching } = useQuery(...);

// isLoading: 데이터가 없고, 첫 쿼리(fetch)가 진행 중인 상태입니다.
// 페이지 첫 진입 시 로딩 스피너나 스켈레톤 UI를 보여주기 적합합니다.
if (isLoading) return <Skeleton />;

// isFetching: 캐시된 데이터가 있어도, 백그라운드에서 refetch 중인 상태입니다.
// 기존 데이터를 보여주면서, '새로고침 중' 같은 표시를 할 떄 사용 합니다.
if (isFetching) return <RefreshingIndicator />;
```

## ⚠️  useMutation에서는 isLoading을 쓰지 않고, v5부터는 isPending을 사용해야 합니다.

### ✅ useQuery 예시
- **isLoding,isFetching 사용**
```tsx
const {
  data: listData,
  isLoading: isListLoading,
  isFetching: isListFetching,
} = useQuery<Project[], Error>({
  queryKey: ["projects", "list"],
  queryFn: async () => {
    const res = await axios.get<Project[]>(PROJECT_API_PATH);
    return res.data;
  },
  enabled: !targetId,
});
```

### ✅ useMutation 예시 (React Query v5)
- **isPending(=useQuery의 isLoading과 같음 v5부터 isLoading이 isPending으로 이름이 변경됨) 사용**

![](https://velog.velcdn.com/images/sunmins/post/f33f7706-0ac4-4bd3-9e4b-5ba2ed96d0a5/image.png)

```tsx
const { mutate: loginMutation, isPending } = useMutation<
  LoginResponse,
  AxiosError<{ error: string }>,
  LoginParams
>({
  mutationFn: async (data) => {
    const res = await axios.post(API_PATH, data);
    return res.data;
  },
  onSuccess: (result) => {
    const { userId, role } = result;
    login({ userId, role });
    router.replace("/projectlist");
  },
  onError: (error) => {
    const message =
      error.response?.data?.error || "서버와 통신 중 오류가 발생했습니다.";
    showToast({ type: ToastMode.ERROR, action: "SAVE", content: message });
  },
});

```

## 🤔 invalidateQueries를 쓸떄는 어떤 상태값을 써야할까?

### `invalidateQueries`란?

`invalidateQueries`는 React Query에서 특정 쿼리의 캐시를 무효화(삭제 또는 만료)시키고, 해당 쿼리를 다시 새로고침(fetch)하도록 요청하는 함수입니다.

즉, 서버 데이터가 변경되었을 가능성이 있을 때 기존 캐시를 신선하지 않다고 표시하고 최신 데이터를 다시 받아오도록 만드는 역할을 합니다.


### 언제 사용하나요?

- 데이터를 수정(create/update/delete)한 후, 최신 상태로 UI를 갱신해야 할 때 사용합니다.
- 예시
  - 게시글을 작성한 뒤 게시글 목록을 다시 불러올 때
  - 사용자 정보가 변경된 뒤 프로필 정보를 새로고침 할 때
 

```tsx
const queryClient = useQueryClient();

const mutation = useMutation(updatePost, {
  onSuccess: () => {
    // 게시글 수정 성공 후, "posts" 쿼리를 무효화하고 다시 불러오기
    queryClient.invalidateQueries(["posts"]);
  },
});


```
### 결론
invalidate로 데이터를 다시 불러올 때는 **isFetching** 상태를 주로 씁니다.
invalidateQueries를 호출하면 캐시된 데이터가 있어도 **백그라운드에서 데이터를 다시 가져오는 동작(refetch)**이 발생합니다.
이때는 이미 data가 있기 때문에 isLoading은 false이고,
isFetching이 true가 되어 "데이터가 새로고침 중"임을 나타냅니다.

---


## ✅ 요약 정리
- useQuery → isLoading, isFetching를 주로 사용
- React Query v5 기준에서 useQuery 훅에서는 isPending을 일반적으로 쓰지 않습니다.
- useMutation → isPending을 사용 (v5에서 isLoading → isPending으로 이름 변경)
- 로딩 UI에는 isLoading이 가장 일반적으로 많이 쓰임
- 데이터를 리패치 중인지 확인할 땐 isFetching
- 사용자 이벤트 기반 mutate 작업 중인지는 isPending

