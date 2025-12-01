### 만들고자 한 프로젝트 관리 시스템 구조 요약

- 사용자(User)는 여러 프로젝트(Project)를 관리하거나 참여합니다.  
- 각 프로젝트(Project)는 여러 작업(Task)을 포함합니다.  
- 작업(Task)에는 여러 댓글(Comment)이 달릴 수 있습니다.

즉, **사용자 → 프로젝트 → 작업 → 댓글** 순으로 연결되는 기본적인 프로젝트 관리 시스템 구조입니다.

이번에 작성한 DB 스키마는 이러한 관계성을 고려하여 설계해봤습니다.  
추가로 보완할 부분이 있을 수 있으나, 초기 기획 단계라고 생각하시고 봐주시면 좋을 것 같습니다.



## 1. ERD 작성 및 SQL 생성

- ERD 작성 도구: **ERD Cloud**를 사용하여 데이터베이스 모델링을 진행했습니다.
![](https://velog.velcdn.com/images/sunmins/post/8c8b8767-48a1-4a01-8995-3ab0b673d9bb/image.png)





- ERD Cloud에서 작성 후, **Export** → **SQL Preview**를 통해 아래와 같은 SQL 스키마를 얻었습니다.
![](https://velog.velcdn.com/images/sunmins/post/81374baf-b94a-4898-a746-0d15dfb68ff4/image.png)



```sql
CREATE TABLE `user` (
	`id`	serial	NOT NULL,
	`userId`	string	NULL,
	`password`	string	NULL,
	`name`	string	NULL
);

CREATE TABLE `project` (
	`id`	serial	NOT NULL,
	`projectId`	string	NULL,
	`progress`	int	NULL,
	`deadline`	DateTime	NULL,
	`managerId`	serial	NOT NULL
);

CREATE TABLE `comment` (
	`id`	serial	NULL,
	`comment`	string	NULL,
	`user_id`	serial	NOT NULL,
	`task_id`	serial	NOT NULL
);

CREATE TABLE `task` (
	`id`	serial	NOT NULL,
	`title`	string	NULL,
	`desc`	string	NULL,
	`status`	string	NULL,
	`user_ id`	serial	NOT NULL,
	`projectId`	serial	NOT NULL,
	`manager_id`	serial	NOT NULL
);

ALTER TABLE `user` ADD CONSTRAINT `PK_USER` PRIMARY KEY (
	`id`
);

ALTER TABLE `project` ADD CONSTRAINT `PK_PROJECT` PRIMARY KEY (
	`id`
);

ALTER TABLE `task` ADD CONSTRAINT `PK_TASK` PRIMARY KEY (
	`id`
);


```


## 2. Prisma 모델로 변환하기
위 SQL 스키마를 참고하여 Prisma 모델 정의 시 자주 사용하는 속성들을 적용해 모델을 작성합니다.

주요 Prisma 속성
- @id: 기본 키 (Primary Key)
- @default(autoincrement()): 자동 증가 값
- @unique: 유니크 제약 조건
- ?: Optional 필드 (nullable 허용)
- 관계 필드 및 @relation 설정 등


## 3. Prisma 모델 작성 시도 정리
### 🧭 작성 단계 요약
### 1단계: 모든 field 정의
각 모델의 필드들을 먼저 정의하였음 (id, userId, title, desc 등).
### 2단계: 일대다 관계의 "다" 쪽 정의
Comment, Task 등의 모델에서 외래 키 필드 정의 (user_id, project_id, manager_id 등).
이 시점에는 관계 설정이 명확히 안 되어 있음.
### 3단계: 일대다 관계의 "일" 쪽 정의
관계를 명확히 지정하기 위해 @relation 속성을 사용하여 참조 연결.
그리고 참조를 하기 위해서는 작성하지 않은 외래키도 작성해야 하는것을 꺠닫고 추가하였음

1단계: 모든 필드 정의
```js
model User {
  id       Int    @id @default(autoincrement())
  userId   String @unique
  password String 
  name     String
}

model Project {
  id         Int    @id @default(autoincrement())
  projectId  String @unique
  progress   Int
  deadline   DateTime
  managerId  String
}

model Task {
  id         Int    @id @default(autoincrement())
  title      String
  desc       String
  status     String

  user_id    
  project_id 
  manager_id 
}

model Comment {
  id       Int    @id @default(autoincrement())
  comment  String

  user_id  
  task_id  
}

```
2단계: "다"쪽의 관계 정의 추가
```js
model User {
  id       Int    @id @default(autoincrement())
  userId   String @unique
  password String 
  name     String

  comments Comment[]
  projects Project[]
  tasks    Task[]
}

model Project {
  id         Int    @id @default(autoincrement())
  projectId  String @unique
  progress   Int
  deadline   DateTime
  managerId  String

  tasks Task[]
}

model Task {
  id         Int    @id @default(autoincrement())
  title      String
  desc       String
  status     String

  user_id    
  project_id 
  manager_id 

  comments Comment[] 
}

model Comment {
  id       Int    @id @default(autoincrement())
  comment  String

  user_id  
  task_id  
}


```

3단계: "일"쪽 관계 정의 추가

```js
model User {
  id       Int    @id @default(autoincrement())
  userId   String @unique
  password String 
  name     String

  comments Comment[]
  projects Project[]
  tasks    Task[]
}

model Project {
  id         Int    @id @default(autoincrement())
  projectId  String @unique 
  progress   Int
  deadline   DateTime
  managerId  String

  tasks   Task[]
  manager User @relation(fields: [managerId], references: [id]) 
}

model Task {
  id         Int    @id @default(autoincrement())
  title      String
  desc       String
  status     String
  projectId  Int
  userId     Int
  managerId  Int

  user    User    @relation(fields: [userId], references: [id])
  project Project @relation(fields: [projectId], references: [id])
  manager User    @relation(fields: [projectId], references: [id])

  comments Comment[]  
}

model Comment {
  id       Int    @id @default(autoincrement())
  comment  String
  userId   Int
  taskId   Int

  user User @relation(fields: [userId], references: [id])
  task Task @relation(fields: [taskId], references: [id])
}

```

## ❌ 주요 문제점 요약 

### 1. ❗ Ambiguous Relation: 동일 모델(User)에 대한 **다중 관계** 명시 안됨
**Task 모델에서 user와 manager 모두 User를 참조했지만, @relation("...") 명시가 없었음 → 에러 발생**

>Error: Ambiguous relation detected...
✅ 해결: @relation("TaskManager") 처럼 이름을 명시해야 Prisma가 구분 가능

### 2. ❗ Project의 managerId 필드 타입 불일치

>managerId String  // ❌ 초기에는 이렇게 되어 있었음
하지만 User.id는 Int이므로 타입 불일치 → 관계 설정 불가능

### 3. ❗ 잘못된 필드 연결
manager User @relation(fields: [projectId], references: [id])

>- manager 관계에 projectId를 사용해서 User를 참조하는 구조 → 논리적 오류
- managerId를 기준으로 관계 맺는 게 올바름


## 4. 🎯 Prisma 스키마 완성본


```js
model User {
  id            Int     @id @default(autoincrement())
  userId        String  @unique
  password      String
  name          String

  tasks         Task[]     @relation("AssignedUser")     // 내가 맡은 일
  managedTasks  Task[]     @relation("ManagingUser")     // 내가 관리하는 일
  comments      Comment[]
  projects      Project[]  @relation("ProjectManager")   // 내가 담당하는 프로젝트들
}

model Project {
  id         Int     @id @default(autoincrement())
  projectId  String  @unique
  progress   Int
  deadline   DateTime
  managerId  Int

  manager    User     @relation("ProjectManager", fields: [managerId], references: [id])
  tasks      Task[]
}

model Task {
  id         Int     @id @default(autoincrement())
  title      String
  desc       String
  status     String
  projectId  Int
  userId     Int
  managerId  Int

  user       User     @relation("AssignedUser", fields: [userId], references: [id])
  manager    User     @relation("ManagingUser", fields: [managerId], references: [id])
  project    Project  @relation(fields: [projectId], references: [id])
  comments   Comment[]
}

model Comment {
  id        Int     @id @default(autoincrement())
  comment   String
  userId    Int
  taskId    Int

  user      User    @relation(fields: [userId], references: [id])
  task      Task    @relation(fields: [taskId], references: [id])
}

```

> SQL을 토대로 만든 model 입니다. 필요에 따라 @unique 와 not Null를 추가했습니다.

## 📘Prisma 모델 변환 설명

### ✅ 기본 변환 규칙

- **serial → `Int @default(autoincrement())`**  
  SQL의 `serial` 타입은 Prisma에서 `Int @default(autoincrement())`로 변환됩니다.  
  → 자동 증가하는 정수형 기본 키를 의미합니다.

- **string NULL → `String?`**  
  SQL에서 `string NULL`로 정의된 필드는 Prisma에서는 `String?` (선택적 필드)로 처리합니다.  
  → 값이 없어도 되는 optional 필드입니다.

---

### ✅ 외래키 필드 및 관계 설정

- **기본 외래키 관계**  
  SQL의 외래키 필드는 Prisma에서 다음과 같이 표현됩니다:

  userId Int
  user   User @relation(fields: [userId], references: [id])
  → `userId`는 외래키 필드이며, 실제 관계는 `@relation`으로 정의됩니다.

### 📌 Comment 모델 예시  
`Comment`는 `User`와 `Task`를 참조합니다:

```prisma
model Comment {
  id       Int    @id @default(autoincrement())
  comment  String?
  userId   Int
  taskId   Int

  user     User @relation(fields: [userId], references: [id])
  task     Task @relation(fields: [taskId], references: [id])
}

```
### ✅ 필드명 매핑: `@map`

SQL에서는 종종 필드명이 `user_id`처럼 `snake_case`로 되어 있습니다.  
Prisma에서는 camelCase(`userId`)로 필드명을 바꾸되, 실제 DB 컬럼명과 매핑해주기 위해 `@map()`을 사용합니다.

예시:

```prisma
userId Int @map("user_id")
```

### ✅ 다중 관계(`@relation("...")`) 명시

Prisma에서는 하나의 모델이 **동일한 대상 모델을 두 번 이상 참조**하면 아래와 같은 에러가 발생합니다:

```text
Error validating model "Task": Ambiguous relation detected...
```
이를 해결하려면 각 관계에 명확한 이름을 명시해야 합니다.

예시:

```prisma
model Task {
  managerId Int
  userId    Int

  user    User @relation(fields: [userId], references: [id])
  manager User @relation("TaskManager", fields: [managerId], references: [id])
}

model User {
  tasksManaged Task[] @relation("TaskManager")
}
```
➡️ @relation("TaskManager")처럼 이름을 지정하면 Prisma가 관계를 명확하게 구분할 수 있습니다.

### ✅ 모델 구조 요약 예시
- User는 여러 Task, Comment, Project를 가질 수 있음
- Project는 한 명의 User(manager)를 가짐
- Task는 담당자(user)와 관리자(manager)를 각각 User로 가짐
→ 이때 **다중 관계 이름**이 필요함
- Comment는 User와 Task를 연결하는 관계 테이블 역할
  

## 🙋‍♀️  마무리
ERD와 SQL을 참고해 Prisma 모델로 바꾸면, 데이터베이스 구조를 코드로 쉽게 표현할 수 있습니다.  
SQL을 Prisma 문법으로 변환하는 연습을 하고, 잘못된 부분을 찾아 수정해가며 공부하면  Prisma 모델 설계 문법에 점점 익숙해질 거라고 생각합니다.


