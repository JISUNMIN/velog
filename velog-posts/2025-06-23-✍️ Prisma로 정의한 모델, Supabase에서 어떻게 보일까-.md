## Prisma 모델을 Supabase에 마이그레이션하여 적용해보기

지난 장에서 정의한 Prisma 모델을 실제 Supabase 데이터베이스에 마이그레이션하여 적용(동기화)해보겠습니다.

이 과정을 통해 우리가 선언적으로 작성한 스키마가 실제 PostgreSQL 테이블로 어떻게 생성되는지 확인할 수 있고, Supabase의 Schema Visualizer를 통해 그 구조를 시각적으로 검토할 수 있습니다.

---

### 마이그레이션 하기 전의 모습입니다.
![](https://velog.velcdn.com/images/sunmins/post/78fbe7e0-2b62-4993-88e1-669e240ce1c4/image.png)

---

### 1. schema.prisma에 모델을 정의했습니다.
![](https://velog.velcdn.com/images/sunmins/post/06248ffc-19b5-4f12-87f2-666a818feed9/image.png)

---

### 2. 터미널에 `npx prisma migrate dev` 명령어를 입력해줍니다.  
그리고 `Enter a name for the new migration`이 나오면 커밋 메시지를 작성해줍니다.  
(필수는 아니지만 적는 것을 권장합니다.)
![](https://velog.velcdn.com/images/sunmins/post/6a82cf73-31f6-4e00-8291-c59b33bd7547/image.png)

---

### 3. 명령어가 실행되고 나면 Supabase의 Schema Visualizer를 통해 확인할 수 있습니다.
![](https://velog.velcdn.com/images/sunmins/post/4b728059-0137-4703-b08f-a97993f2e5c2/image.png)

---

### Schema Visualizer는 여기서 확인할 수 있습니다.
![](https://velog.velcdn.com/images/sunmins/post/5666fdf8-774d-41ba-bcad-014a4a2c3480/image.png)
