유저 프로필 이미지를 저장할 공간이 필요해서 **Supabase Storage**를 사용해 보기로 했습니다.  
이 글에서는 **버킷을 생성하고 Public 설정하는 방법**까지만 다루고,  
API를 통한 업로드 구현은 다음 글에서 정리할 예정입니다.

---

## 1. Supabase Storage Bucket 만들기

Supabase는 AWS S3처럼 파일을 저장할 수 있는 **Storage** 기능을 제공합니다.  
이미지를 저장할 Bucket을 먼저 만들어야 합니다.

1. [https://supabase.com/dashboard/project/_/storage/buckets](https://supabase.com/dashboard/project/_/storage/buckets) 접속
2. 사용할 프로젝트 클릭
3. **New bucket** 버튼 클릭
4. 버킷 이름 입력 (예: `profile-images`)
5. **Public** 옵션 체크 (공개 여부)

![bucket 생성 과정](https://velog.velcdn.com/images/sunmins/post/e56e85d8-f6db-4032-96c9-518396329a04/image.png)

![버킷 이름 입력](https://velog.velcdn.com/images/sunmins/post/58ebd41a-ea75-451a-8030-cbda0773c584/image.png)


![Public 체크](https://velog.velcdn.com/images/sunmins/post/179a1956-6229-4a00-b297-ba65c823331a/image.png)

---

### Public vs Private

- **Public 버킷**  
  모든 사람이 URL로 접근 가능. 권한 없이 바로 접근할 수 있습니다.  
  (프로필 이미지나 썸네일 등 공개해도 되는 리소스에 적합)

- **Private 버킷**  
  Supabase Auth 토큰 또는 Signed URL을 이용해서만 접근 가능합니다.  
  (민감한 자료 보관용)

**프로필 이미지는 보통 Public으로 설정**합니다.

---

## 📝 마무리

다음글에서는   

- `@supabase/supabase-js` 설치  
- `.env.local`에 프로젝트 URL과 서비스 롤 키 설정  
- Next.js API Route에서 Supabase 클라이언트 초기화  
- Storage에 이미지 업로드 및 Public URL DB 저장  

을 정리하겠습니다

---

## 참고

- [Supabase Storage 공식 문서](https://supabase.com/docs/guides/storage)
