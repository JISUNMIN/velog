API 호출 시 `The table public.User does not exist in the current database` 라는 에러를 만난다면, Prisma가 `User` 테이블을 데이터베이스에서 찾지 못하고 있다는 의미입니다.

다음과 같은 순서로 문제를 해결할 수 있습니다.

---

## 1. Prisma Studio로 현재 DB 상태 확인

```bash
npx prisma studio
```
이 명령어를 실행하면 브라우저가 열리고, 현재 데이터베이스에 존재하는 테이블 목록과 그 안의 데이터들을 시각적으로 확인할 수 있습니다.

👉 User 테이블이 없다면, 다음 단계로 넘어가 마이그레이션을 통해 테이블을 생성해야 합니다.

![](https://velog.velcdn.com/images/sunmins/post/b916632d-84f6-4a4e-973b-6bb3473fe76b/image.png)


## 2. Prisma와 DB 스키마 동기화 확인

저의 경우, 테이블은 Supabase에 존재했고, Prisma의 `schema.prisma` 파일에도 `model User`가 동일하게 정의되어 있었습니다.

하지만 Supabase에서 직접 추가한 레코드는 Prisma Studio에서 보이지 않았는데, 그 이유는 Prisma가 DB 스키마 변경 사항을 자동으로 감지하지 않기 때문입니다.

즉, Supabase DB에서 직접 데이터를 추가하거나 테이블 구조가 변경되었을 때, Prisma는 이를 자동으로 반영하지 않습니다.

---

## 3. 해결 방법: Prisma 스키마 수동 동기화

Prisma가 데이터베이스와 동기화되도록 다음 명령어를 실행해 주세요.

```bash
npx prisma db pull

이 명령어는 현재 데이터베이스의 구조를 Prisma 스키마 파일로 가져와 동기화를 진행합니다.
```

---

- Supabase에 `User` 테이블과 관련 필드가 존재하지만, Prisma가 이를 인식하지 못하는 경우가 있습니다.
- Prisma는 데이터베이스 구조 변경을 자동으로 감지하지 않으므로, 수동으로 명령어를 실행해야 합니다.
- 다음 명령어를 실행하여 현재 DB 구조를 Prisma 스키마 파일에 반영합니다.

```bash
npx prisma db pull
```

명령어 실행이 완료되면, Prisma Studio에서 최신 DB 구조와 데이터를 확인할 수 있습니다.

![](https://velog.velcdn.com/images/sunmins/post/1367de4d-8788-41cf-b45d-83f403fa18fa/image.png)


## Prisma vs Supabase 데이터 추가 권장 방식

### 1. Supabase 직접 데이터 추가
- 초기 테스트나 간단한 데이터 입력에 적합
- 빠르고 편리하지만, **Prisma 스키마와 불일치 가능성 있음**

### 2. Prisma를 통한 데이터 추가
- 운영 중인 애플리케이션에서 권장
- 타입 안정성 보장, 유지보수 용이
- 코드 내에서 일관된 데이터 관리 가능

---

## 결론
운영 환경에서는 **Prisma 클라이언트를 통해 데이터 추가**하는 것이 권장됩니다.  
초기 세팅이나 간단한 테스트 시에는 Supabase 콘솔 직접 입력도 괜찮습니다.
다만 위에 알아본 바와 같이 **Prsima 스키마 불일치**에 신경써야 합니다.

