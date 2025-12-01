칸반 보드에서 여러 작업(Task)의 제목 등을 수정할 때,  
사용자가 키보드를 빠르게 입력하면 입력마다 서버 요청이 발생하여 **불필요하게 많은 API 호출**이 생깁니다.  
이를 방지하기 위해 `debounce`를 적용해 **사용자가 입력을 멈춘 뒤 한 번만 요청**하도록 개선했습니다.

---

## Debounce란 무엇일까?

**Debounce**는 짧은 시간 안에 여러 번 발생하는 이벤트 중 **마지막 이벤트만 처리**하도록  
실행을 지연시키는 함수 최적화 기법입니다.

예시:
- 입력할 때마다 서버에 요청을 보내면 과도한 요청이 발생
- `debounce`를 적용하면 **일정 시간 동안 입력이 없을 때** 마지막 값만 서버에 전송

**딜레이 시간(ms)** 은 직접 설정할 수 있습니다.

---


## 💡 사용한 이유

칸반 보드에서 여러 작업(Task)의 제목을 수정할 때,

- **입력할 때마다 API를 호출하면 너무 많은 요청이 발생**하여 서버에 부담이 됩니다.
- 그래서 사용자가 입력을 멈춘 후에 **마지막 값만 서버에 반영하도록 처리**해야 합니다.

---


## 🛠 적용: 하나의 debounce 함수로 관리

```tsx
const debouncedUpdate = useMemo(() =>
  debounce((taskId: number, newTitle: string) => {
    updateTaskMutate({ id: taskId, title: newTitle });
  }, 500),
  [updateTaskMutate]
);
```
- 모든 작업 수정 이벤트를 단일 debounce 함수로 처리
- 0.5초(500ms) 동안 입력이 없으면 서버 요청

### ⚠️  문제점
근데 여기서 또 문제가 발생합니다.
이 방식에서는 debounce 함수가 하나뿐이어서, 모든 작업 수정 이벤트가 같은 함수에서 처리됩니다.
결과적으로 마지막 작업만 서버에 반영되고 이전 작업은 무시됩니다.

```
task 1번 - "1"
task 2번 - "2"
task 3번 - "3"

```
→ 결과: **마지막인 task 3번만 저장, 나머지는 반영되지 않음.**

## 🔄 개선 방식: 작업별로 debounce 함수 분리

```tsx
const debouncedUpdateMap = useRef<Record<number, (title: string) => void>>({});

const debouncedUpdate = (taskId: number, newTitle: string) => {
  if (!debouncedUpdateMap.current[taskId]) {
    debouncedUpdateMap.current[taskId] = debounce((title: string) => {
      updateTaskMutate({ id: taskId, title });
    }, 500);
  }
  debouncedUpdateMap.current[taskId](newTitle);
};
```
- `useRef`를 사용해 `debouncedUpdateMap` 객체를 생성합니다.

- 이 객체는 각 작업(`taskId`)별로 별도의 debounce 함수를 저장하고 관리하는 역할을 합니다.

- 즉, `taskId`를 키(key)로 하여 debounce 함수를 값(value)으로 갖는 함수 저장소 역할을 하며,
**작업별로 별도의 debounce 함수를 생성하여 관리**합니다.
- **각 작업에 독립적으로 debounce가 적용**됩니다.

- 컴포넌트가 리렌더되어도 이 `ref` 객체는 초기화되지 않고 유지되어, 중복 생성 없이 재사용할 수 있습니다.
---

## 🆚 두 방식 비교

| 구분       | 하나의 debounce 함수 (기존) | 작업별 debounce 분리 (개선)    |
| -------- | -------------------- | ----------------------- |
| 함수 개수    | 1개                   | 작업 개수만큼 생성 (필요시)        |
| 서버 요청    | 마지막 수정 작업 1건만 반영     | 각 작업별 수정 내용 모두 반영       |
| 동시 수정 처리 | 제대로 처리 안됨            | 여러 작업 동시 수정 가능          |
| 메모리 관리   | 간단함                  | debounce 함수가 많아져서 관리 필요 |


## 📝마무리
여러 작업을 동시에 다룰 때는 **debounce도 작업별로 분리하는 게 안정적**입니다.  
하나의 debounce 함수에 모든 작업을 몰아넣으면 **수정 누락과 데이터 불일치**가 발생할 수 있습니다.
따라서, 작업별 debounce 관리로 **서버 요청 최적화와 데이터 일관성**을 동시에 확보할 수 있습니다.