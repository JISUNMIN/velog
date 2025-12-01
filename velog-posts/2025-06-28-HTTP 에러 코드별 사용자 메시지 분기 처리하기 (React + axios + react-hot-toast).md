### 회원가입 API 에러 상태(status)에 따라 Toast 메시지 처리하기

API를 호출할 때, 서버에서 내려주는 HTTP status code에 따라 다른 에러 메시지를 사용자에게 보여주고 싶다면, 아래와 같이 구현할 수 있습니다.  
저는 `alert` 대신 [🍞 react-hot-toast](https://react-hot-toast.com/) 와 toast에서 자주 쓰이는 메시지를 정리해놓은 상수 `TOAST_MESSAGES`를 활용하여 구현했습니다.

---

![](https://velog.velcdn.com/images/sunmins/post/ea24c436-317e-4459-86a7-509dea486fe8/image.png)

## 🖥️ 서버 코드 예시 (Next.js API Route)

```ts
export async function POST(req: NextRequest) {
  try {
    const { userId, password, name } = (await req.json()) as CreateParams;

    // 필수값 누락
    if (!userId || !password || !name) {
      return NextResponse.json({ error: "필수 항목이 누락되었습니다." }, { status: 400 });
    }

    // 중복 아이디 확인
    const existUser = await prisma.user.findUnique({ where: { userId } });
    if (existUser) {
      return NextResponse.json({ error: "이미 사용중인 아이디입니다." }, { status: 409 });
    }

    // 회원가입 진행
    const hashed = await bcrypt.hash(password, 10);
    const user = await prisma.user.create({
      data: { userId, password: hashed, name },
    });

    return NextResponse.json({ userId: user.userId, name: user.name }, { status: 201 });
  } catch (error) {
    console.error("회원가입 에러:", error);
    return NextResponse.json({ error: "서버 오류가 발생했습니다." }, { status: 500 });
  }
}
```

## 📊 처리 가능한 에러 코드 정리

성공일 때는 status 코드에 따라 분기할 필요 없이 `onSuccess`에서 처리하면 됩니다.  
에러의 경우, 다음과 같은 status 코드에 따라 메시지를 분기하여 사용자에게 안내합니다:

| Status | 의미                    | 설명                                      |
|--------|-------------------------|-------------------------------------------|
| 400    | Bad Request             | 필수값 누락 (client validation 누락 등)   |
| 409    | Conflict                | 이미 존재하는 유저 ID                    |
| 500    | Internal Server Error   | 서버 내부 에러                           |

---

## 💻 클라이언트에서의 처리 (React + React Query + Axios)

```tsx
  const { mutate: createMutate } = useMutation<void, AxiosError, CreateParams>({
    mutationFn: async (data) => {
      await axios.post(API_PATH, data);
    },
    onSuccess: () => {
      showToast({
        type: ToastMode.SUCCESS,
        action: "REGISTER",
      });
      router.replace("/auth/login");
    },
    onError: (error) => {
      const status = error?.response?.status;

      switch (status) {
        case 400:
          showToast({
            type: ToastMode.ERROR,
            action: "REGISTER",
            content: "필수값이 누락되었습니다.",
          });
          break;
        case 409:
          showToast({
            type: ToastMode.ERROR,
            action: "ISEXIST",
          });
          break;
        case 500:
        default:
          showToast({
            type: ToastMode.ERROR,
            action: "REGISTER",
            content: "서버 오류가 발생했습니다.",
          });
          break;
      }
    },
  });

```
## 메시지 구현 화면
![](https://velog.velcdn.com/images/sunmins/post/14e1481b-5656-4a43-b37d-b11ac76d343e/image.png)


## 🧠 구현 포인트 정리

- **400**: 프론트엔드에서 유효성 검사를 하더라도, 서버에서도 필수값 검사를 수행해야 합니다.
- **409**: 중복된 유저 ID로 인한 회원가입 실패를 사용자에게 명확하게 전달합니다.
- **500**: 예상치 못한 서버 오류에 대한 안내 메시지를 표시합니다.
- `axios`의 에러 객체는 `error.response.status`를 통해 HTTP 상태 코드에 접근할 수 있습니다.