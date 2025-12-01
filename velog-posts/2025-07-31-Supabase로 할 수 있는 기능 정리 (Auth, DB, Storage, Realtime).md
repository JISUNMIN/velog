이전글에서 **Supabase 클라이언트를 생성하는 방법**을 알아봤습니다.  
이번 글에서는 **이 클라이언트를 통해 어떤 기능들을 할 수 있는지** 살펴보겠습니다.

---

## Supabase 클라이언트 생성 예시

`createClient()`를 통해 Supabase 서비스에 접근할 수 있는 클라이언트를 생성했습니다.

```ts
// lib/supabase.ts
import { createClient } from "@supabase/supabase-js";

export const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY! // 서버 전용 키
);
```

---


## Supabase 주요 기능

### 1. 인증 (Auth)
- 이메일/비밀번호 기반 회원가입 및 로그인을 할 수 있습니다.
- 소셜 로그인(Google, GitHub 등 OAuth)을 지원합니다.
- 세션/토큰 관리 (자동 갱신)를 할 수 있습니다.
- 사용자 정보 관리를 할 수 있습니다.

### 2. 데이터베이스 (Database)
- **PostgreSQL** 기반 DB를 제공합니다.
- RESTful API 및 Realtime API를 자동으로 생성해 줍니다.
- 간단한 CRUD 작업은 Supabase 클라이언트로 직접 처리할 수 있습니다.
- 복잡한 로직은 Prisma 같은 ORM을 함께 사용해 관리했습니다.

### 3. 스토리지 (Storage)
- 이미지, 문서, 동영상 등 파일을 업로드/다운로드/삭제할 수 있습니다.
- 퍼블릭 URL을 발급할 수 있습니다.
- 폴더 구조를 관리할 수 있습니다.

### 4. 실시간 (Realtime)
- DB 변경 사항을 WebSocket 기반으로 실시간 구독할 수 있습니다.
- 채팅, 알림, 대시보드 등 실시간 기능을 구현할 수 있습니다.

---

## 사용 예시 

### 1. 인증 (로그인): supabase.auth  
```ts
const { data, error } = await supabase.auth.signInWithPassword({
  email: "test@example.com",
  password: "123456",
});

```

### 2. 스토리지 (파일 업로드): supabase.storage
```ts
const file = ...; // 업로드할 File 객체
const { error } = await supabase.storage
  .from("profile-images")
  .upload("example.png", file);
```

### 3. DB 쿼리 (CRUD): supabase.from()
```ts
const file = ...; // 업로드할 File 객체
const { error } = await supabase.storage
  .from("profile-images")
  .upload("example.png", file);
```

## 📝 정리

- **인증과 스토리지**  
  Supabase 클라이언트를 사용해 직접 처리합니다.
  (로그인, 회원가입, 세션 관리, 파일 업로드·다운로드 등이 가능한데 저의 경우 파일 업로드 기능을 사용했습니다.)

- **데이터베이스 쿼리**  
  단순 CRUD는 Supabase 클라이언트로 가능하지만,  
  복잡한 비즈니스 로직에서는 **Prisma 같은 ORM을 함께 사용하는 것이 일반적**입니다.

- **실시간 기능**  
  WebSocket 기반 실시간 데이터 구독이 가능하며,  
  이를 통해 채팅, 알림, 실시간 대시보드 등의 기능 구현이 가능합니다.

Supabase는 백엔드를 제공해주는 서비스입니다.  
인증, 데이터베이스, 스토리지, 실시간 기능 등을 API 형태로 쉽게 사용할 수 있어 빠른 개발이 가능합니다.

