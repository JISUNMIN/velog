Prisma를 사용하다 보니 schema.prisma 파일이 자동으로 포맷팅되지 않는 것을 발견했습니다.
Prisma extension도 설치했고, 기본 저장 포맷 설정도 되어 있는데 왜 그런 걸까요?
이번 글에서는 VSCode에서 Prisma schema 파일 자동 포맷팅을 적용하는 방법을 정리해보겠습니다.

---

## 1. 🔌 Prisma 확장 설치하기 

- VSCode 마켓플레이스에서 공식 **Prisma 확장(Prisma)** 을 반드시 설치하세요.  
- 이 확장은 Prisma 파일에 대한 구문 강조, 자동 완성, 그리고 자동 포맷팅 기능을 제공합니다.

---

## 2. ⚙️ Prisma 파일 자동 포맷터 지정하기

- VSCode 기본 포맷터가 Prettier 등 다른 포맷터로 되어 있을 수 있어, Prisma 파일에 대해 별도로 Prisma 확장 포맷터를 지정해야 합니다.

- `settings.json`에 다음 설정을 추가하세요.

```json
{
  "[prisma]": {
    "editor.defaultFormatter": "Prisma.prisma"
  },
  "editor.formatOnSave": true
}
```

- [prisma] 부분은 .prisma 파일 확장자에만 해당 포맷터를 적용한다는 의미입니다.
- editor.formatOnSave는 저장 시 자동으로 포맷팅되도록 하는 설정입니다.


## 적용 전 / 적용 후
<div style="display: flex; gap: 10px;">
  <img src="https://velog.velcdn.com/images/sunmins/post/e196c88b-2b08-4fbe-a54a-399fbaf0c5da/image.png" alt="적용 전" width="45%" />
  <img src="https://velog.velcdn.com/images/sunmins/post/9dd8fc67-daed-4ba4-aed2-9f50abe522aa/image.png" alt="적용 후" width="45%" />
</div>



## 3. ▶️ 명령어로 포맷팅하기(필요시) 

터미널에서 수동으로 Prisma 스키마를 포맷할 수도 있습니다.

```bash
npx prisma format
```

이 명령어는 프로젝트 루트의 schema.prisma 파일을 찾아 자동으로 포맷팅해줍니다.

## ✅ 마무리
Prisma 확장이 반드시 설치되어 있어야 VSCode 내에서 포맷팅이 정상 작동합니다.

Prettier 같은 다른 포맷터가 설치되어 있으면 Prisma 파일이 제대로 포맷되지 않을 수 있으니 위 설정을 적용하시면 됩니다.

저장 시 자동 포맷팅이 안 된다면, editor.formatOnSave 설정과 [prisma] 파일의 기본 포맷터가 Prisma 확장인지 확인 필요합니다.