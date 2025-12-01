> Prisma Studio에서는 보였던 관계 데이터가 왜 코드에서는 안 보일까? 🤔 

## 🧩 문제 상황

Prisma Studio에서는 `Project` 데이터를 보면 아래처럼 나옵니다.

![](https://velog.velcdn.com/images/sunmins/post/2edf5a03-bee8-49b6-8ee1-5a1cab679e8f/image.png)


그런데 코드에서 조회하면?
```js
const projects = await prisma.project.findMany();
console.log(projects[0]);
```

👇 출력 결과는 이렇습니다:
```json
{
  "id": 1,
  "projectId": "project01",
  "progress": 0,
  "deadline": "2025-12-31T00:00:00.000Z",
  "managerId": 1
  // manager ❌
  // tasks ❌
}
```

👀 manager, tasks는 어디 갔을까요?


## 📌 원인

**Prisma는 기본적으로 관계(Relation) 필드를 자동으로 포함하지 않습니다.
우리가 project 안에 manager, tasks 같은 관계 데이터를 보고 싶다면 명시적으로 요청해야 합니다.**

## ✅ 해결 방법: include 옵션 사용
```js
const projects = await prisma.project.findMany({
  include: {
    manager: true,
    tasks: true,
  },
});

console.log(projects[0].manager); // ✅ 있음
console.log(projects[0].tasks);   // ✅ 있음
```

### 🎯 더 세부적으로 불러오고 싶다면?
include 안에 select도 같이 사용할 수 있습니다.

```js
const projects = await prisma.project.findMany({
  include: {
    manager: {
      select: {
        name: true,
        userId: true,
      },
    },
    tasks: true,
  },
});

```

## 📝 정리

| 구분                           | 설명                             |
| ---------------------------- | ------------------------------ |
| Prisma Studio                | 관계까지 자동으로 보여줌                  |
| 코드(`findMany`, `findUnique`) | 기본적으로 관계 X                     |
| 해결 방법                        | `include: { 관계명: true }` 옵션 사용 |

Prisma를 처음 쓸 때 많이 헷갈리는 부분 중 하나입니다.
Studio에서는 마치 자동으로 다 되는 것처럼 보여주지만,
실제 쿼리에서는 원하는 데이터는 직접 명시해줘야 합니다.

