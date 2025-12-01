## 🎯 목표

이미지 URL을 `fetch`해서 `File` 객체로 변환하는 방법을 공유합니다.  
업로드된 이미지를 다시 불러와 편집하거나 FormData로 넘길 때 유용합니다.

## 🧪 코드 예시

```ts
export const convertURLtoFile = async (url: string) => {
  const response = await fetch(url);
  const data = await response.blob();
  const ext = url.split(".").pop(); // url 구조에 맞게 수정할 것
  const filename = url.split("/").pop(); // url 구조에 맞게 수정할 것
  const metadata = { type: `image/${ext}` };
  return new File([data], filename!, metadata);
};
```

이 함수는 이미지 URL을 받아 File 객체로 변환해줍니다.
예를 들어 React에서 이미지 미리보기를 보여주거나, 업로드를 다시 처리할 때 사용할 수 있습니다

### ✅ 활용 예
- React Hook Form 등에서 이미지 File을 다뤄야 할 때
- 이미지 리사이징, crop 등 편집 기능 후 다시 업로드할 때
- URL 기반 이미지 데이터를 다시 서버에 전송할 때.

### 🚨 그런데 CORS 에러가 발생한다면?
![](https://velog.velcdn.com/images/sunmins/post/abb740a4-b729-4627-9c6c-abc93ea5a637/image.png)

Access to fetch at 'https://s3.amazonaws.com/your-image.jpg' 
from origin 'http://localhost:3000' has been blocked by CORS policy:
No 'Access-Control-Allow-Origin' header is present...

이런 에러가 발생한다면 대부분 다음 중 하나입니다:

#### 1. ✅ S3에서 CORS 설정이 되어 있지 않은 경우
S3는 기본적으로 다른 도메인에서의 접근을 허용하지 않습니다.
아래와 같은 CORS 설정을 S3 버킷에 추가해야 합니다:

```.xml
<CORSConfiguration>
  <CORSRule>
    <AllowedOrigin>*</AllowedOrigin> <!-- 또는 특정 도메인 -->
    <AllowedMethod>GET</AllowedMethod>
    <AllowedHeader>*</AllowedHeader>
  </CORSRule>
</CORSConfiguration>
```
⚠️ 실제 운영환경에서는 * 대신 https://yourdomain.com과 같이 정확한 도메인을 명시하는 것이 좋습니다.

> ❓ **S3란 Amazon S3 (Simple Storage Service로 AWS에서 제공하는 클라우드 기반 파일 저장소** 입니다.
#### 📦 쉽게 말하면?
- 인터넷 상의 파일 저장소입니다.
- 이미지, 동영상, PDF, JSON 등 모든 종류의 파일을 저장할 수 있습니다.
- 우리가 흔히 말하는 "버킷(Bucket)"은 S3 안에 있는 폴더 같은 공간입니다.




#### 2. 🔒 S3 객체가 공개되지 않은 경우
해당 이미지 URL이 퍼블릭하게 열려있지 않거나, 프리사인 URL이 필요한 경우에도 CORS 문제가 발생할 수 있습니다.

- 브라우저에서 직접 URL을 열어 이미지가 뜨는지 확인
- 필요하다면 서버에서 Presigned URL을 생성해서 사용

>🔐 퍼블릭 vs 프라이빗
퍼블릭 S3: 아무나 URL로 접근 가능
**프라이빗 S3: 권한이 있어야 접근 가능
→ 이때 등장하는 게 Presigned URL (임시 접근 허용 토큰)**

>❓ Presigned URL이란, AWS 인증을 통과한 사용자가 일정 시간 동안만 해당 리소스에 접근할 수 있도록 만들어주는 **임시 접근용 URL**입니다.



### 🙋‍♀️ 프론트가 할 수 있는 건?
프론트엔드에서는 CORS 정책 자체를 **변경하거나 우회할 수 없습니다**.  
**CORS는 서버에서 허용해줘야만 정상 작동합니다. ** 
하지만 프론트는 어떤 요청에서 에러가 발생하는지를 명확히 분석하고,  
서버 담당자에게 적절한 조치를 요청하는 역할을 할 수 있습니다.

## 🔍 정리
- 이미지 URL을 fetch → blob → File로 변환 가능
- S3 또는 외부 서버 URL 사용 시 **CORS 정책에 주의**
- S3라면:
  - 버킷 CORS 설정 필요
  - 퍼블릭 또는 Presigned URL 사용 여부 확인