![](https://velog.velcdn.com/images/sunmins/post/0d3b65eb-e615-4e8b-bcd1-c34518e1ba72/image.png)

프로젝트 목록을 드래그 앤 드롭으로 순서 변경할 수 있도록 구현하는 과정에서, @hello-pangea/dnd(구 react-beautiful-dnd)는 수평/수직 한 방향 정렬만을 지원해, 그리드 형태의 박스를 상하좌우로 이동시키는 데 제약이 있었습니다. 이러한 한계를 해결하기 위해, 여러 방향으로의 자유로운 이동과 유연한 그리드 레이아웃 지원이 가능한 @dnd-kit으로 라이브러리를 전환하게 되었습니다.

이에 따라 기존과 바뀐 구현 방식, 그리고 두 라이브러리 간의 차이점을 정리해 보았습니다.




---

## 🐼 @hello-pangea/dnd란?

이전 `react-beautiful-dnd`의 커뮤니티 포크로,  
React에서 리스트의 순서를 **간단하게 변경할 수 있도록 도와주는 라이브러리**입니다.

### ✅ 주요 특징
- 리스트 기반 UI 구현에 최적화됨
- 수직(`vertical`) 또는 수평(`horizontal`) **한 방향만 지원**
- React 컴포넌트 형태의 API (`<DragDropContext />`, `<Droppable />`, `<Draggable />`)
- 레이아웃이 변경되면 DnD 동작이 어색해질 수 있음

---

## 🧩 @hello-pangea/dnd 구성요소 역할 설명

| 구성요소               | 설명                                                                                                           |
| ------------------ | ------------------------------------------------------------------------------------------------------------ |
| `DragDropContext`  | **DnD 전체를 감싸는 최상위 컨테이너**<br>여기서 `onDragEnd` 같은 전역 이벤트를 설정함                                                   |
| `onDragEnd`        | 드래그 종료 시 호출되는 콜백 함수. <br>`source.index`, `destination.index`로 아이템 순서를 바꿈                                     |
| `Droppable`        | **드롭이 가능한 영역**을 의미함. <br>리스트 전체나 카드 영역을 감쌈                                                                   |
| `provided`         | 라이브러리가 내부에서 제공하는 ref와 props들을 전달해줌 <br>→ `ref={provided.innerRef}`, `{...provided.droppableProps}` 등         |
| `Draggable`        | 드래그 가능한 개별 아이템을 감쌈                                                                                           |
| `provided` (again) | `Draggable` 내부에서도 `provided`를 통해<br>드래그 핸들러와 ref를 바인딩함<br>`draggableProps`, `dragHandleProps`, `innerRef` 사용 |

---

## 📜 기존 코드: `@hello-pangea/dnd` 기반

기존에는 다음과 같은 구조로 Drag & Drop을 구현했습니다.

```tsx
const [editableProjects, setEditableProjects] = useState<any[]>([]);

const handleDragEnd = (result: any) => {
  if (!result.destination) return;
  const newItems = [...editableProjects];
  const [removed] = newItems.splice(result.source.index, 1);
  newItems.splice(result.destination.index, 0, removed);
  setEditableProjects(newItems);
};

<DragDropContext onDragEnd={handleDragEnd}>
  <Droppable droppableId="projects" direction="horizontal">
    {(provided) => (
      <div
        ref={provided.innerRef}
        {...provided.droppableProps}
        className={
          isEditing
            ? "flex gap-4 overflow-x-auto pb-2"
            : "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6"
        }
      >
        {editableProjects?.map((project, index) => (
          <Draggable
            key={project.id}
            draggableId={project.id.toString()}
            index={index}
            isDragDisabled={!isEditing}
          >
            {(provided) => (
              <div
                ref={provided.innerRef}
                {...provided.draggableProps}
                {...provided.dragHandleProps}
                className={
                  isEditing
                    ? "min-w-[270px] max-w-[270px] flex-shrink-0"
                    : ""
                }
              >
                <ProjectCard
                  project={project}
                  onClick={() => onClickProject(project.id)}
                />
              </div>
            )}
          </Draggable>
        ))}
        {provided.placeholder}
      </div>
    )}
  </Droppable>
</DragDropContext>
```
![](https://velog.velcdn.com/images/sunmins/post/7ffcd84f-1d95-463f-a94d-4cc79c4405fc/image.png)


---

## ⚠️ 문제점 
- `direction="vertical"`로 설정 시 상하 이동만 가능
- `direction="horizontal"`로 설정 시 좌우 이동만 가능
- 그리드 형태(`grid-cols-4`)에서는 상하/좌우 동시에 이동할 수 없음
- 편집 모드에서 한 줄만 보이게(`flex`) 바꾸는 식으로 UX를 우회했지만, 이 또한 어색하고 스크롤 UX가 불편함

---

## ✅ 대안: @dnd-kit 도입

### 📦 설치
```bash
npm install @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities
```

### ✨ 장점
- 그리드 레이아웃 유지하면서도 상하/좌우 자유롭게 드래그 가능
- sortable 전략을 통해 `arrayMove()`로 순서 변경 처리
- 커스터마이징이 더 유연하고 섬세함

---

## 🧩 dnd-kit이란?

`@dnd-kit`은 **modular하고 유연한 설계**를 가진 드래그 앤 드롭 라이브러리로,  
그리드, 커스텀 정렬, 멀티 드래그, 제스처 기반 제어 등 다양한 시나리오에 적합합니다.

> 📦 **"modular하다"는 무슨 뜻일까?**  
> 여러 개의 조각(모듈)들로 나뉘어 있고, 필요한 조각만 골라서 사용할 수 있는 구조를 말합니다.

`@dnd-kit`은 modular한 구조입니다.  
- `@dnd-kit/core` → DnD의 기본 기능만 제공  
- `@dnd-kit/sortable` → 리스트 정렬이 필요할 때만 추가  
- `@dnd-kit/accessibility` → 키보드 접근성 필요할 때만 추가  
- `@dnd-kit/modifiers` → 위치 제한이나 제약 조건이 필요할 때만 추가  
👉 즉, 필요한 기능만 골라 쓸 수 있습니다.

---

## 🧰 @dnd-kit 구성요소 역할 설명

### 📦 Core (@dnd-kit/core)

| 구성요소                      | 설명                                                                |
| ------------------------- | ----------------------------------------------------------------- |
| `DndContext`              | **DnD 기능을 제공하는 최상위 컨텍스트** <br>`onDragStart`, `onDragEnd` 등 이벤트 처리 |
| `useSensor`, `useSensors` | 어떤 입력 장치(마우스, 터치, 키보드 등)를 사용할지 정의<br>보통 `PointerSensor` 사용        |
| `closestCenter`           | **충돌 판별 전략** 중 하나. <br>드래그된 요소와 가장 가까운 요소를 기준으로 순서를 정함            |

### 📦 Sortable (@dnd-kit/sortable)

| 구성요소                  | 설명                                                                          |
| --------------------- | --------------------------------------------------------------------------- |
| `SortableContext`     | **정렬 가능한 아이템들의 그룹을 정의**<br> `items` 배열과 `strategy`(정렬 방식)를 지정함              |
| `rectSortingStrategy` | `grid`, `카드 정렬` 등에 적합한 정렬 방식<br>(가장 일반적으로 많이 사용됨)                           |
| `useSortable`         | 각 개별 아이템을 **정렬 가능하게 만드는 훅**<br>drag handle, style transform 등을 반환함          |
| `arrayMove`           | 배열 내에서 순서를 변경하는 유틸 함수<br>→ `setItems(arrayMove(items, oldIndex, newIndex))` |

---

## ✅ 주요 특징

- 상하/좌우 모두 자유롭게 이동 가능  
- 리스트, 그리드, 캔버스 등 다양한 레이아웃에 적합  
- 컴포넌트 기반이 아닌 **hook 중심의 설계**  
- 높은 유연성과 커스터마이징 가능성  

---

## 🧰 @dnd-kit 사용법 요약

### 1. 기본 구조
```tsx
<DndContext onDragEnd={handleDragEnd}>
  <SortableContext items={items} strategy={rectSortingStrategy}>
    <div className="grid grid-cols-4 gap-6">
      {items.map((item) => (
        <SortableItem key={item.id} id={item.id}>
          <ProjectCard project={item} />
        </SortableItem>
      ))}
    </div>
  </SortableContext>
</DndContext>
```

### 2. SortableItem 정의

```tsx
const SortableItem = ({ id, children }: { id: number; children: React.ReactNode }) => {
  const { attributes, listeners, setNodeRef, transform, transition } = useSortable({ id });
  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <div ref={setNodeRef} style={style} {...attributes} {...listeners}>
      {children}
    </div>
  );
};
```

| 이름              | 의미                             | 관계                         |
| --------------- | ------------------------------ | -------------------------- |
| `useSortable()` | 정렬 가능한 아이템을 만들기 위한 **훅(Hook)** | 내부 로직, 상태, 드래그 관련 props 제공 |
| `SortableItem`  | 이 훅을 **사용해서 실제로 UI를 구현한 컴포넌트** | 드래그 가능한 하나의 카드(아이템) 역할     |

`useSortable()`는 단독으로 UI를 만들 수 없고, 반환값을 받아서 div 같은 DOM에 직접 바인딩해줘야 합니다.  
그래서 이렇게 따로 분리해서 `SortableItem`이라는 컴포넌트로 만들어 둡니다.

```tsx
const SortableItem = ({ id, children }) => {
  const {
    setNodeRef,
    transform,
    transition,
    attributes,
    listeners,
  } = useSortable({ id }); // 👈 이게 핵심 로직

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <div
      ref={setNodeRef}        // 드래그 가능한 DOM 등록
      style={style}           // 움직일 때 트랜스폼 적용
      {...attributes}         // 접근성 관련 attr
      {...listeners}          // 드래그 이벤트 바인딩 (mousedown 등)
    >
      {children}
    </div>
  );
};
```

| 이름           | 역할 및 설명                                                                          |
| ------------ | -------------------------------------------------------------------------------- |
| `attributes` | 접근성(Attribute) 관련 props, 키보드 접근성 및 ARIA 속성을 관리해줍니다.                              |
| `listeners`  | 드래그 이벤트 핸들러들(mousedown, touchstart 등)을 포함하고 있어 이걸 해당 DOM에 붙여야 드래그가 가능합니다.        |
| `setNodeRef` | 드래그 대상 DOM 요소를 `useSortable`이 추적할 수 있게 참조를 연결하는 함수입니다.                           |
| `transform`  | 드래그 중인 아이템의 위치 변환 값(translateX, translateY 등)입니다. 이것을 스타일에 적용해야 자연스럽게 움직임이 보입니다. |
| `transition` | 위치 변경 애니메이션 관련 CSS 속성 값입니다.                                                      |


### 3. 순서 변경 처리

```tsx
const handleDragEnd = (event: DragEndEvent) => {
  const { active, over } = event;
  if (active.id !== over?.id) {
    const oldIndex = items.findIndex(i => i.id === active.id);
    const newIndex = items.findIndex(i => i.id === over.id);
    setItems(arrayMove(items, oldIndex, newIndex));
  }
};
```
- 드래그가 끝났을 때 호출되는 콜백 함수입니다.
- event 객체 안에 두 가지 중요한 정보가 있습니다:

| 이름       | 설명                                      |
| -------- | --------------------------------------- |
| `active` | 현재 드래그 중이던(드래그가 끝난) 아이템의 정보 (id, 데이터 등) |
| `over`   | 드롭 대상이 된(놓으려는 위치에 있는) 아이템의 정보         |

두 아이템의 id가 다르면 (즉, 위치가 바뀐 경우) 원래 배열에서 active.id의 위치(oldIndex)
새 위치가 된 over.id의 위치(newIndex)를 찾고 arrayMove 함수로 배열 내 순서를 변경하여 상태를 업데이트합니다.

---

## 🔁 전환 후 구현 코드 (요약)

```tsx
const SortableItem = ({
  id,
  children,
}: {
  id: number;
  children: React.ReactNode;
}) => {
  const { attributes, listeners, setNodeRef, transform, transition } =
    useSortable({ id });
  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };
  return (
    <div ref={setNodeRef} style={style} {...attributes} {...listeners}>
      {children}
    </div>
  );
};

const [editableProjects, setEditableProjects] = useState<any[]>([]);

const sensors = useSensors(
  useSensor(PointerSensor, { activationConstraint: { distance: 5 } })
);

const handleDragEnd = (event: any) => {
  const { active, over } = event;
  if (active.id !== over?.id) {
    const oldIndex = editableProjects.findIndex((p) => p.id === active.id);
    const newIndex = editableProjects.findIndex((p) => p.id === over.id);
      setEditableProjects((prev) => arrayMove(prev, oldIndex, newIndex));
  }
};

<DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
  <SortableContext items={editableProjects.map(p => p.id)} strategy={rectSortingStrategy}>
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      {editableProjects.map((project) => (
        <SortableItem key={project.id} id={project.id}>
          <ProjectCard
            project={project}
            onClick={() => onClickProject(project.id)}
          />
        </SortableItem>
      ))}
    </div>
  </SortableContext>
</DndContext>
```

![](https://velog.velcdn.com/images/sunmins/post/bd936779-3837-4b15-a5ad-611d26f6bb61/image.gif)



---

## ⚖️ 핵심 차이 요약

| 역할 / 기능  | `@hello-pangea/dnd`      | `@dnd-kit`                                               |
| -------- | ------------------------ | -------------------------------------------------------- |
| 최상위 컨텍스트 | `<DragDropContext>`      | `<DndContext>`                                           |
| 아이템 그룹   | `<Droppable>`            | `<SortableContext>`                                      |
| 아이템      | `<Draggable>`            | `useSortable()` 훅 + `SortableItem` 컴포넌트                  |
| 드래그 이벤트  | `onDragEnd(result)`      | `onDragEnd({ active, over })`                            |
| 방향 전략    | `direction="vertical"` 등 | `rectSortingStrategy`, `horizontalListSortingStrategy` 등 |
| 순서 변경    | 수동으로 배열 재정렬              | `arrayMove()` 활용                                         |

---

## 🆚 두 라이브러리 비교

| 항목          | @hello-pangea/dnd               | @dnd-kit                           |
| ----------- | ------------------------------- | ---------------------------------- |
| **설계 방식**   | 컴포넌트 기반 (`<DragDropContext />`) | 훅 기반 (`useSortable`, `DndContext`) |
| **정렬 방향**   | 단일 방향만 가능 (상하 또는 좌우)            | 상하/좌우 모두 가능 (자유로운 grid 이동)         |
| **grid 대응** | ❌ 제한적 (줄 바꿈 이동 불가)              | ✅ 완벽 대응 (`rectSortingStrategy`)    |
| **애니메이션**   | 내장된 기본 애니메이션                    | 직접 스타일 설정 필요 (더 커스터마이징 가능)         |
| **커스터마이징**  | 제한적                             | 매우 유연                              |
| **난이도**     | 쉬움 (초보자에게 적합)                   | 중간~높음 (학습 필요)                     |
| **대표 용도**   | 리스트, 칸반 보드                      | 그리드, 인터랙티브 UI, 자유 배치 등             |

---

## ✅ 결론

기존 DnD 구현에서는 그리드 형태로 아이템을 보여줄 수는 있지만, 드래그 방향이 한 방향(상하 또는 좌우)으로 제한되어 있었습니다. 이 때문에 자유로운 위치 변경이 어려웠고 UX에 한계가 있었습니다.

그래서 @dnd-kit으로 전환하게 되었는데, @dnd-kit은 그리드 형태에서도 상하좌우 자유롭게 이동할 수 있고, 다양한 커스터마이징이 가능해 보다 완성도 높은 UX를 제공할 수 있습니다.

- 단순하고** 한 방향(상하 또는 좌우) 이동만 필요한 경우**에는 사**용법이 더 쉽고 빠른 @hello-pangea/dnd (pandadnd, 구 react-beautiful-dnd)를 추천**합니다.
- **상하좌우 모두 자유롭게 이동해야 하거나, 세밀한 커스터마이징이 필요한 경우에는 @dnd-kit를 추**천합니다.
---

## 🧠 참고 링크

- [dnd-kit 공식 문서](https://docs.dndkit.com/)
- [@hello-pangea/dnd GitHub](https://github.com/hello-pangea/dnd)
