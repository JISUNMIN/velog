## ❗문제 상황

로컬 환경에서는 Prisma와 Supabase를 이용한 Next.js API가 정상적으로 작동했습니다.  
하지만 Vercel에 배포된 프로덕션 환경에서는 API가 제대로 동작하지 않는 문제가 발생했습니다. 🤔

![](https://velog.velcdn.com/images/sunmins/post/65fafb45-43c8-4552-b32f-707e7c6872d3/image.png)![](https://velog.velcdn.com/images/sunmins/post/15fb0d72-50ca-45dc-ae27-71e4a4c0308b/image.png)


---

## ⚠️ 발생한 오류 메시지

```plaintext
Error [PrismaClientInitializationError]: 
Invalid prisma.user.findUnique() invocation:

error: Environment variable not found: DATABASE_URL.
  -->  schema.prisma:7
   | 
 6 |   provider  = "postgresql"
 7 |   url       = env("DATABASE_URL")
   | 

Validation Error Count: 1
    at <unknown> (-->  schema.prisma:7)
    at async l (.next/server/app/api/auth/login/route.js:1:824) {
  clientVersion: '6.9.0',
  errorCode: undefined,
  retryable: undefined
}
```
이 오류는 **Prisma가 DATABASE_URL 환경변수를 찾지 못해 발생한 문제**임을 알려줍니다.

## 원인 분석

문제의 원인은 환경변수 설정이었습니다.  
로컬에서는 `.env` 파일에 `DATABASE_URL`, `DIRECT_URL` 등 Supabase 관련 환경변수를 설정해 사용했지만,  
**Vercel 프로덕션 환경에서는 별도로 환경변수를 설정하지 않으면 이를 인식하지 못합니다.**

---

## 해결 방법

1. Vercel 대시보드에서 프로젝트를 선택합니다.  
2. **Settings** → **Environment Variables** 메뉴로 이동합니다.  
3. `DATABASE_URL`, `DIRECT_URL` 키와 실제 값을 각각 입력하고 저장합니다.  
4. 터미널에서 `vercel deploy` 명령어로 다시 배포합니다.  
   - 만약 `vercel` 명령어가 없다면, `npm i -g vercel` 로 설치하세요.
   
> npm i -g vercel: Vercel CLI를 전역으로 설치하는 명령어
 Vercel 배포 명령어인 vercel deploy 등을 터미널에서 사용하려면 CLI가 필요합니다.
이 명령어를 한 번 실행하면 시스템 어디서든 vercel 명령어를 사용할 수 있습니다.
   
 ![](https://velog.velcdn.com/images/sunmins/post/9f1678cf-6a09-471a-8f07-8634acdbf26a/image.png)
![](https://velog.velcdn.com/images/sunmins/post/3df7d18b-0b7b-412d-856f-96ff6d08bdca/image.png)



---

## 💡 결과

위 과정을 거치니 Vercel 배포 환경에서도 API가 정상적으로 작동하는 것을 확인할 수 있었습니다.


![](https://velog.velcdn.com/images/sunmins/post/bc8d4d3b-2c5d-4ff9-bdc6-08eca9f7694b/image.png)

---

## 🔍 정리

- Vercel 환경변수를 변경한 후에는 반드시 다시 배포해야 변경사항이 반영됩니다.  
- 배포 전에 환경변수가 정확히 입력되어 있는지 꼼꼼히 확인하는 것이 중요합니다.
