프로젝트를 진행하던 중, `Project` 모델 내의 필드명을 잘못 지정한 것을 발견했습니다.  
원래는 `projectName`으로 지정했어야 했지만, 실수로 `projectId`로 작성해 두었었습니다.

이에 따라 Prisma 모델을 다음과 같이 수정하였습니다.

---

## 기존 Prisma 모델

```prisma
model Project {
  id         Int     @id @default(autoincrement())
  projectId  String  @unique
  progress   Int
  deadline   DateTime
  managerId  Int

  manager    User     @relation("ProjectManager", fields: [managerId], references: [id])
  tasks      Task[]
}
```

## 수정된 Prisma 모델

```prisma
model Project {
  id           Int     @id @default(autoincrement())
  projectName  String  @unique
  progress     Int
  deadline     DateTime
  managerId    Int

  manager      User     @relation("ProjectManager", fields: [managerId], references: [id])
  tasks        Task[]
}

```

이후 다음 명령어를 통해 마이그레이션을 시도하였습니다.

```bsah
npx prisma migrate dev

```

## ❗ 에러 발생
하지만 다음과 같은 에러 메시지가 출력되었습니다.

⚠️ We found changes that cannot be executed:

  • Step 1 Added the required column `projectName` to the `Project` table without a default value. 
  
  
## 🔍 에러 원인
Prisma에서는 필드명을 변경하면 실제로는 기존 컬럼을 제거하고 새로운 컬럼을 생성하는 방식으로 처리하게 됩니다.
그런데 새로운 컬럼인 projectName이 NOT NULL 제약을 가지고 있었습니다.

따라서 Prisma는 기본값 없이 NOT NULL 컬럼을 추가할 수 없어 에러를 발생시킨 것이었습니다.

## 🛠 해결 방법

이 문제를 해결하기 위해 다음과 같은 절차를 따랐습니다.

---

### 1. `projectName` 필드를 nullable로 수정


![](https://velog.velcdn.com/images/sunmins/post/b7fdd48a-03dd-4cd3-92a6-2d384efdfd5e/image.png)



### 2. 마이그레이션 파일 생성 및 적용

```bash
npx prisma migrate dev --name change-projectid-to-projectname
```
![](https://velog.velcdn.com/images/sunmins/post/93c6bd4f-7772-4577-b12b-34ebcb9c5c52/image.png)


### 3. DB에서 기존 레코드에 projectName 값 채워 넣기
[prsima studio](https://velog.io/@sunmins/Prisma-Studio%EB%A1%9C-%ED%98%84%EC%9E%AC-DB-%ED%85%8C%EC%9D%B4%EB%B8%94-%ED%99%95%EC%9D%B8%ED%95%98%EA%B8%B0) 에서 변경하거나 [script file](https://velog.io/@sunmins/Prisma%EC%99%80-%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8-%EC%8B%A4%ED%96%89%EC%9C%BC%EB%A1%9C-%EC%B4%88%EA%B8%B0-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%B6%94%EA%B0%80%ED%95%98%EA%B8%B0)을 실행합니다.

### 4. 다시 Prisma 모델에서 NOT NULL 제약 추가
![업로드중..](blob:https://velog.io/9cfd03cc-6f8e-47e4-8188-65791f91063f)

### 5. 마이그레이션 재적용
```bash
npx prisma migrate dev --name make-projectname-not-null
````
![업로드중..](blob:https://velog.io/da05417e-dbaa-4d33-b1e9-dac4b9cdb6ad)



##  ✅ 마무리
이 문제는 Prisma가 필드명을 변경할 때 발생하는데,  
기존 데이터가 있는 테이블에 `NOT NULL` 컬럼을 기본값 없이 바로 추가하려 하면 오류가 납니다. 이는 데이터베이스가 기존 레코드에 어떤 값을 넣어야 할지 몰라서 발생하는 문제입니다.  

그래서 저는 위와 같이  
1) 먼저 `null` 값을 허용하도록 변경하고,  
2) 기존 데이터에 값을 채운 뒤,  
3) 다시 `NOT NULL` 제약조건을 추가하는 방식으로 해결했습니다.  

또는 `@default` 옵션으로 기본값을 지정하여 한 번에 처리하는 방법도 있습니다.  
 데이터베이스가 자동으로 기존 레코드에 기본값을 채워주기 때문에 데이터가 많을 경우, 이 방법이 더 효율적일 것 같습니다.