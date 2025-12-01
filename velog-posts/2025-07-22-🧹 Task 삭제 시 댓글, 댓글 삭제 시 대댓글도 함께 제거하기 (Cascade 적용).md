
댓글과 대댓글이 있는 시스템에서, 댓글이나 작업(Task)이 삭제될 때 관련 데이터가 제대로 정리되지 않는 문제를 발견하여 정리했습니다.
Prisma에서 이를 해결하는 방법을 소개합니다.

---


## ⚠️ 문제 상황
프로젝트에서 Task에 달린 댓글 기능을 구현했고, 댓글에는 대댓글(답글) 기능도 지원합니다.
데이터 모델은 Prisma에서 다음처럼 Comment가 자기 자신을 참조하는 구조(자기 참조 관계)로 만들었습니다.

이 구조에서는 다음과 같은 문제가 발생합니다:

1. ✅ task를 삭제해도 관련 댓글이 삭제되지 않음

2. ✅ 댓글을 삭제해도 관련 대댓글이 삭제되지 않음

이는 Prisma에서 자기 참조 관계(self-relation) 를 사용하는 경우, 명시적으로 onDelete: Cascade 를 지정하지 않으면 고아 상태(orphaned) 가 되어 버리기 때문입니다.


## 🔍 원인
기존 Prisma 모델에서는 onDelete: Cascade 옵션이 설정되어 있지 않아, 참조된 부모 엔티티(Task 또는 Comment)가 삭제되어도 자식 엔티티가 삭제되지 않았습니다.

```ts
model Comment {
  id              Int       @id @default(autoincrement())
  comment         String
  userId          Int
  taskId          Int
  parentCommentId Int?

  user            User      @relation(fields: [userId], references: [id])
  task            Task      @relation(fields: [taskId], references: [id]) 
  parentComment   Comment?  @relation("CommentToReplies", fields: [parentCommentId], references: [id]) 
  replies         Comment[] @relation("CommentToReplies")
}
```

## ✅ 해결 방법 – onDelete: Cascade 추가

Task가 삭제될 때 해당 댓글도 함께 삭제되고,
댓글이 삭제되면 대댓글도 자동으로 삭제되도록 하기 위해
아래처럼 `onDelete: Cascade`를 명시적으로 추가해줍니다.

```
model Comment {
  id              Int    @id @default(autoincrement())
  comment         String
  userId          Int
  taskId          Int
  parentCommentId Int?

  // ✅ 부모 댓글이 삭제되면 대댓글도 함께 삭제
  parentComment Comment?  @relation("CommentToReplies", fields: [parentCommentId], references: [id], onDelete: Cascade)
  replies       Comment[] @relation("CommentToReplies")

  user User @relation(fields: [userId], references: [id])
  // ✅ Task가 삭제되면 해당 댓글도 함께 삭제
  task Task @relation(fields: [taskId], references: [id], onDelete: Cascade)
}

```

✔️ Task 를 삭제하면, 그에 연결된 모든 Comment 들도 함께 삭제됩니다.
✔️ 댓글을 삭제하면, 해당 댓글의 대댓글들도 함께 삭제됩니다.


## 📝 마치며 
Prisma에서 onDelete: Cascade 를 명시하지 않으면, 관계된 레코드 삭제 시 에러가 발생하거나 고아 상태로 남을 수 있습니다.
특히 자기 참조(self-relation) 에서는 onDelete 를 반드시 명시해주는 것이 안전합니다.