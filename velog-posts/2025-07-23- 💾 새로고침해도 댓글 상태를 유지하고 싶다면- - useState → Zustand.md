기존에는 댓글 상태를 `useState`로 컴포넌트 내부에서 관리했습니다.  
하지만 저는 **새로고침**이나 **페이지 이동** 시에도 사용자가 입력한 댓글과 대댓글 열림/닫힘 상태가 유지되길 바랐습니다.  
사용성 측면에서 더 좋은 경험이라고 판단하여, 상태를 **Zustand 전역 구독 상태**로 분리하는 방법을 적용했고 그 방법을 소개합니다.

---

### 💡 왜 상태를 store로 분리했는가?
- **문제점**  
  - 컴포넌트 언마운트 또는 새로고침 시 `useState`로 관리한 상태가 초기화됨  
  - 사용자가 열어본 대댓글 패널이 사라지고 댓글도 초기화되어 불편함  

- **목표**  
  - 페이지 이동/새로고침에도 댓글 입력값과 대댓글 열림 상태를 **유지**  

따라서 [**`Zustand` + `persist`**](https://velog.io/@sunmins/Zustand-%EC%83%81%ED%83%9C-%EC%9C%A0%EC%A7%80%ED%95%98%EA%B8%B0-persist%EC%99%80-%EC%8A%A4%ED%86%A0%EB%A6%AC%EC%A7%80-%EC%98%B5%EC%85%98localStorage-sessionStorage)를 활용해 상태를 전역으로 분리했습니다.

###  🔄 변경 전 코드
```tsx
// CommentItem.tsx
const [showReplyMap, setShowReplyMap] = useState<Record<number, boolean>>({});
const toggleShowReply = (id: number) => {
  setReplyCollapseMap((prev) => ({
    ...prev,
    [id]: !prev[id],
  }));
};
```

### 🔄 변경된 코드 (Zustand 사용)
```ts
// useCommentStore.ts
import { create } from "zustand";
import { persist } from "zustand/middleware";

type CommentType = {
  id: string;
  content: string;
  parentId?: string;
  // 기타 필요한 필드들...
};

interface CommentState {
  comments: CommentType[];
  setComments: (comments: CommentType[]) => void;

  showReplyMap: Record<string, boolean>;
  toggleShowReply: (commentId: string) => void;
}

export const useCommentStore = create<CommentState>()(
  persist(
    (set) => ({
      comments: [],
      setComments: (comments) => set({ comments }),

      showReplyMap: {},
      toggleShowReply: (commentId) =>
        set((state) => ({
          showReplyMap: {
            ...state.showReplyMap,
            [commentId]: !state.showReplyMap[commentId],
          },
        })),
    }),
    {
      name: "comment-storage", 
    }
  )
);
```
```tsx
// CommentItem.tsx
import { useCommentStore } from "@/store/useCommentStore";

const comments = useCommentStore((state) => state.comments);
const showReplyMap = useCommentStore((state) => state.showReplyMap);
const toggleShowReply = useCommentStore((state) => state.toggleShowReply);

{comments.map((comment) => (
  <div key={comment.id}>
    <p>{comment.content}</p>

    <button onClick={() => toggleShowReply(comment.id)}>
      {showReplyMap[comment.id] ? "대댓글 닫기" : "대댓글 열기"}
    </button>

    {showReplyMap[comment.id] && <ReplyList parentId={comment.id} />}
  </div>
))}
```
### 적용 결과
- ✅ 페이지를 이동하거나 새로고침해도 댓글의 열림/닫힘 상태, 입력된 댓글이 유지됩니다.

## 📝마무리
컴포넌트 내부에서 UI 상태를 useState로 간단히 처리하는 것도 좋은 접근이지만,
**사용자가 설정한 UI 상태(예: 대댓글 열림 여부)**를 더 오래 유지해야 할 경우에는
전역 상태 관리로 관리할 수 있습니다.
다만, 너무 오래 저장하면 오래된 데이터가 쌓여 혼란을 줄 수 있으니 적절한 만료 정책이나 데이터 정리가 필요합니다.

