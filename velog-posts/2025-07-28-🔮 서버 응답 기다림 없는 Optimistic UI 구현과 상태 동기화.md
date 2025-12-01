칸반 보드에서 작업을 생성하거나 수정할 때,  
서버 응답 시간이 길어 사용자가 답답함을 느꼈습니다.

특히 작업을 빠르게 연속 추가하거나 수정하는 경우,  
서버와 로컬 상태가 엇갈려 작업이 사라지거나 깜빡이는 문제도 있었습니다.

이를 해결하기 위해 **Optimistic UI**를 도입했습니다.
--- 


## 🔍 Optimistic UI란?

**Optimistic UI**는  
서버 응답을 기다리지 않고 **결과를 미리 UI에 반영**하는 기술입니다.

- 서버 요청이 성공할 것이라 **낙관적으로 가정**
- 즉시 UI 업데이트 → 빠른 피드백
- 응답 도착 후 실제 데이터로 동기화

##  ⚡ Optimistic UI가 자주 쓰이는 이유

### 언제 쓰이나?
- 네트워크 지연이 긴 환경
- **연속 클릭/입력**이 자주 발생하는 앱
- **실시간성이 중요한 서비스** (채팅, 댓글, 칸반 등)

### 왜 쓰이나?
- 서버 응답 대기 시간을 **숨겨서** 빠른 UX 제공
- **UI 깜빡임 없이** 자연스러운 동작
- 사용자 만족도와 앱 반응성 향상
---
## 🔄 기존 코드

기존에는 **서버 응답이 올 때까지 UI를 갱신하지 않고**,  
응답 후 React Query의 `invalidateQueries`로 데이터를 새로 불러왔습니다.
```tsx
// KanbanBoard.tsx
 const handleCreateTask = (
    columnKey: Status,
    columnIndex: number,
    orderType: "top" | "bottom" = "bottom"
  ) => {
    addTask(columnIndex, orderType);
    createTaskMutate({
      title: "",
      desc: "",
      status: columnKey,
      projectId: Number(projectId),
      userId: user?.id ?? 1,
      managerId: user?.id ?? 1,
      orderType,
    });
  };
```
```ts
  // useTask.ts
  const { mutate: createTaskMutate } = useMutation<
    void,
    Error,
    TaskCreateParams
  >({
    mutationFn: async (data) => {
      await axios.post(TASK_PROJECT_API_PATH, data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["projects", "list"] });
    },
    onError: () => {},
  });

//  useKanbanStore.ts
addTask: (index: number, orderType = "bottom") =>
  set((state) => {
    const columnKeys = Object.keys(state.columns) as Status[];
    const columnKey = columnKeys[index];
    if (!columnKey) return state;

    const newTask = { title: "", desc: "", assignees: [] };

    return {
      columns: {
        ...state.columns,
        [columnKey]: [...state.columns[columnKey], newTask],
      },
    };
  }),
```

## ⚠️문제점
- 서버 응답 전까지 UI가 변하지 않음 → 사용자가 느리다고 느낌
- `invalidateQueries`로 새로 데이터를 불러오는 동안
캐시가 비워지고 **UI가 깜빡이며 작업이 잠시 사라짐**
- 연속 작업 시 **로컬 상태와 서버 상태가 엇갈려 작업 누락 발생**

## 🔄 변경된 코드 (Optimistic UI 적용)
이번 구현에서는 **임시 키(tempId)를 활용한 Optimistic UI**를 적용했습니다.

1. **즉시 UI 반영**  
   tempId를 사용해 로컬 상태에 임시 작업을 생성
2. **서버 응답 후 동기화**  
   서버 응답이 오면 tempId로 찾은 임시 데이터를 실제 task 데이터로 교체
```tsx
// KanbanBoard.tsx
const handleCreateTask = (columnKey, columnIndex, orderType) => {
  const tempId = `temp-${Date.now()}`;
  addTask(columnIndex, orderType, tempId); // 1. 로컬에 즉시 반영

  createTaskMutate(
    {
      title: "",
      desc: "",
      status: columnKey,
      projectId: Number(projectId),
      userId: user?.id ?? 1,
      managerId: user?.id ?? 1,
      orderType,
    },
    {
      onSuccess: (realTask) => {
        // 2. 서버 응답 후 임시 작업을 실제 데이터로 교체
        replaceTempTask(columnKey, tempId, realTask);
      },
    }
  );
};
```
```ts
addTask: (index: number, orderType = "bottom", tempId?: string) =>
  set((state) => {
    const columnKeys = Object.keys(state.columns) as Status[];
    const columnKey = columnKeys[index];
    if (!columnKey) return state;

    const newTask = { id: tempId, title: "", desc: "", assignees: [] };

    const updatedColumn =
      orderType === "top"
        ? [newTask, ...state.columns[columnKey]]
        : [...state.columns[columnKey], newTask];

    return {
      columns: {
        ...state.columns,
        [columnKey]: updatedColumn,
      },
    };
  }),

replaceTempTask: (columnKey: Status, tempId: string, realTask: Task) =>
  set((state) => {
    const updatedColumn = state.columns[columnKey].map((t) =>
      t.id === tempId ? realTask : t
    );
    return {
      columns: {
        ...state.columns,
        [columnKey]: updatedColumn,
      },
    };
  }),
```

---

## React Query invalidateQueries 문제와 해결

### 기존 문제
- `invalidateQueries` → 서버 재요청 발생
- 캐시가 비워지며 **로딩 UI 깜빡임**
- Zustand와 React Query 간의 **데이터 불일치** 문제

### 해결
- `invalidateQueries` 대신, **응답 데이터를 store에 직접 반영**
- **Optimistic UI + 응답 동기화**를 통해 깜빡임 없이 최신 상태 유지
---


## 정리

결국 이번 변경의 핵심은 다음과 같습니다.

- `invalidateQueries`로 **매번 서버 데이터를 다시 불러오는 방식**을 제거하고,
- **임시 id(tempId)**를 사용해 store(Zustand)에 먼저 작업을 추가한 뒤
- **API 응답이 오면 tempId를 실제 id로 교체**하여 동기화
- 화면은 항상 **store 데이터를 기준으로 즉시 반영**하고,
- **새로고침 시 서버 데이터를 다시 동기화**하는 방식으로 개선했습니다.

## 📝 마무리

Optimistic UI는 **서버 응답을 기다리지 않고 즉시 UI를 업데이트**하여  
빠르고 부드러운 사용자 경험을 제공합니다.

반면, React Query의 `invalidateQueries`는 편리하지만  
**캐시 무효화로 인해 UI 깜빡임과 상태 불일치**가 발생할 수 있습니다.

이에 따라 React Query와 Zustand 같은 로컬 상태 관리 라이브러리를 함께 사용할 때는  
**로컬 상태(Zustand)에 Optimistic UI로 먼저 반영하고, 서버 응답으로 최종 동기화하는 방식**으로 구현했습니다.  
이 접근법을 통해 **UI 깜빡임 현상이 사라지고, 전반적인 사용성도 크게 향상**되었습니다.