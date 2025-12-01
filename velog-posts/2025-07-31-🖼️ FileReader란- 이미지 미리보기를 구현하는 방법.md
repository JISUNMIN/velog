프로필 사진처럼 사용자가 업로드한 이미지를 화면에 바로 보여주고 싶을 때가 많습니다.  
선택한 파일은 서버에 보내기 위해 FormData로 전송하지만, 이 방법만으로는 즉시 미리보기가 어렵습니다.

그래서 **FileReader**를 사용해 파일을 base64 문자열로 변환한 뒤,  
이미지의 `src`에 넣어 화면에 바로 보여줍니다.

오늘은 프로필 사진 등 업로드 이미지의 즉시 미리보기를 구현하는 데 필요한 **FileReader**에 대해 알아보겠습니다.

---

## 📚 FileReader란?
**파일을 브라우저에서 읽어서** `string` **형식(주로 base64)으로 변환해주는 내장 객체**입니다.
변환된 이 문자열을 이미지의 src에 넣으면 브라우저가 그 파일을 이미지로 보여줍니다.


## FileReader의 역할

- 사용자가 `<input type="file" />`에서 선택한 파일을 자바스크립트에서 읽을 수 있도록 도와주는 API입니다.  
- 파일을 읽어 **데이터 URL(base64 인코딩된 문자열)**, 텍스트, 배열 버퍼 등으로 변환할 수 있습니다.  
- 이렇게 변환된 데이터를 이미지 `src`나 다른 UI에 바로 적용할 수 있습니다.

---


## ✅ FileReader의 주요 메서드와 동작 흐름

```tsx
const reader = new FileReader();

reader.onload = () => {
  // 파일 읽기가 완료되면 호출되는 콜백
  const dataUrl = reader.result; // base64 인코딩된 문자열 등 읽은 결과
  setCurrentProfileImage(dataUrl as string); // React 상태에 넣어 화면 업데이트
};

reader.readAsDataURL(file); // 파일을 base64 데이터 URL로 읽기 시작
```

### 💡 readAsDataURL의 역할

- 파일을 **base64 인코딩된 데이터 URL**로 읽도록 하는 메서드입니다.  
- 호출 시 파일 내용을 비동기 방식으로 읽고, 읽기가 완료되면 `onload` 이벤트가 발생합니다.  
- 결과(`reader.result`)는 `data:image/png;base64,...` 형태의 문자열이 됩니다.

### 💡 onload 이벤트를 정의하지 않으면?

- 파일 읽기 완료 시 콜백이 없기 때문에, 변환된 데이터를 받을 수 없습니다.  
- 따라서 화면에 미리보기를 표시할 수 없습니다.  
- `onload`는 읽기 완료 후 후속 작업을 위해 반드시 필요합니다.

### 💡 Base64란?

- 바이너리 데이터를 문자로 인코딩하는 방식 중 하나입니다.  
- 이미지를 텍스트 문자열로 변환해 HTML, CSS, JSON 등에 직접 넣을 수 있게 해줍니다.  
- 예: `data:image/png;base64,iVBORw0KGgoAAAANSUhEUg...` (이미지 파일 내용을 문자열로 표현한 것)

### FileReader 동작 흐름 요약

1. `new FileReader()`로 객체 생성  
2. `readAsDataURL(file)` 호출해 비동기 파일 읽기 시작  
3. 파일 읽기 완료 시 `onload` 이벤트 발생  
4. `reader.result`에 읽은 데이터(base64 문자열) 저장  
5. 결과를 React state 등에 넣어 이미지 미리보기 렌더링  

## 📋 FileReader 주요제공 메서드 비교

| 메서드명                       | 설명                           | 결과 타입                     | 사용 용도 예시             |
| -------------------------- | ---------------------------- | ------------------------- | -------------------- |
| `readAsDataURL(file)`      | 파일을 base64로 인코딩된 데이터 URL로 읽음 | `data:*/*;base64,...` 문자열 | 이미지 미리보기 등           |
| `readAsText(file)`         | 파일을 텍스트 문자열로 읽음              | 문자열                       | 텍스트 파일, CSV 등 텍스트 처리 |
| `readAsArrayBuffer(file)`  | 파일을 이진 배열 버퍼로 읽음             | `ArrayBuffer`             | 바이너리 데이터 처리, 파일 변환 시 |



---


## 🤔 왜 FileReader를 쓸까?
- 파일 업로드 시, **서버에 보내기 전에 사용자가 선택한 이미지를 바로 확인**할 수 있으면 UX가 훨씬 좋아집니다.
- 파일 자체를 서버로 보내기 전이라도 로컬에서 읽어 화면에 표시할 수 있기 때문입니다.

## React 예시 코드

```tsx
const onChangeProfileImage = (e: React.ChangeEvent<HTMLInputElement>) => {
  const file = e.target.files?.[0];
  if (!file) return;

  // 업로드할 파일 상태에 저장 (서버 전송 용도)
  setProfileImageFile(file);

  // FileReader를 사용해 이미지 미리보기용 데이터 읽기
  const reader = new FileReader();
  reader.onload = () => {
    setCurrentProfileImage(reader.result as string); // base64 문자열을 이미지 src에 설정
  };
  reader.readAsDataURL(file);
};
```

## 구현 화면 
![](https://velog.velcdn.com/images/sunmins/post/74b0f8a8-4d14-4ff2-b0af-600998f35d7f/image.png)



## 📝 정리
- FileReader는 브라우저 내장 객체로 파일을 읽어 base64 같은 문자열로 변환해 줍니다.
- React에서 이미지 업로드 후 즉시 미리보기를 구현할 때 필수적입니다.
- 비동기로 동작하므로 onload 이벤트를 꼭 활용해야 합니다.