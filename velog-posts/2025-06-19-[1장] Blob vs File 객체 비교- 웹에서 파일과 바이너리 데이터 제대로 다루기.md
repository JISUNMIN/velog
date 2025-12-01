## 1. Blob이란?

- **Blob (Binary Large Object)**  
  - 브라우저 내장 Web API 객체로, 바이너리 원시 데이터를 담는 불변(immutable) 덩어리입니다.  
  - `new Blob()`으로 생성 가능하며, 파일과 달리 이름이나 수정일 등의 메타정보는 포함하지 않습니다.  
  - 크기(`size`), MIME 타입(`type`) 속성을 갖고 있습니다.  
  - `slice()`, `text()`, `stream()` 등의 다양한 메서드를 제공합니다.  
  - 예를 들어 JSON 문자열, 이미지 데이터 등을 Blob으로 감싸서 처리할 때 사용합니다.

### ❓ 바이너리 데이터란?

사람이 읽기 힘든 비문자 기반 데이터입니다.  
(예: 이미지, 영상, 실행파일 등)  
반면, 텍스트 데이터는 사람이 읽을 수 있는 문자로 이루어진 데이터입니다.

### 💡 왜 구분이 필요할까?

데이터를 전송하거나 저장할 때 처리 방식이 달라집니다.  
HTTP 요청 시 Content-Type을 데이터 형태에 따라 다르게 지정합니다.

| Content-Type               | 데이터 형태               | 용도                          | 예시                              |
|---------------------------|---------------------------|-----------------------------|----------------------------------|
| `text/plain`              | 텍스트                    | 순수 텍스트 데이터 전송          | 로그 전송, 테스트용 간단한 API         |
| `application/json`        | 텍스트 (JSON 형식)          | 구조화된 데이터 전송             | `{ "name": "민지", "age": 25 }`      |
| `application/octet-stream`| 바이너리                  | 일반적인 바이너리 파일 전송       | 이미지, PDF, 영상 등                 |
| `multipart/form-data`     | 혼합 (텍스트 + 바이너리)     | 폼 데이터 전송 시 (파일 포함)     | 회원가입 시 이름 + 프로필 사진 같이 보낼 때 |

> ❓ **불변 덩어리**란?  
> 한 번 생성되면 내부 데이터를 변경할 수 없는 것을 의미합니다.  
> Blob 객체는 생성된 이후 데이터를 수정할 수 없으며, 새로운 Blob을 복사하거나 잘라서 새로 만들어야 합니다.

> ❓ **MIME 타입(Multipurpose Internet Mail Extensions)**이란?  
> 인터넷에서 전송되는 데이터의 종류(형식)를 나타내는 문자열로, 서버가 클라이언트에게 데이터의 종류를 알려줍니다.  
> 예:  
> - `text/html` → HTML 문서로 해석  
> - `image/png` → PNG 이미지로 처리  
> - `application/json` → JSON 데이터로 파싱

---

### ✅ Blob 사용 예시

```js
// JSON 데이터를 Blob으로 만들기
const obj = { name: "ChatGPT", type: "AI" };
const jsonBlob = new Blob([JSON.stringify(obj)], { type: "application/json" });

// Blob을 텍스트로 읽기
jsonBlob.text().then(text => {
  console.log(text); // '{"name":"ChatGPT","type":"AI"}'
});

--------------------------------------------------------------------------

// 이미지 URL을 fetch하고 Blob으로 받아오기
fetch("https://example.com/photo.png")
  .then(res => res.blob())
  .then(blob => {
    // Blob을 이미지로 화면에 표시하기
    const imgUrl = URL.createObjectURL(blob);
    const img = document.createElement("img");
    img.src = imgUrl;
    document.body.appendChild(img);
  });

```

> ❓ createObjectURL란? URL.createObjectURL()은 브라우저 내장 함수로,
Blob이나 File 같은 바이너리 데이터를 가리키는 임시 URL(주소)을 만들어주는 기능입니다.
우리가 이미지, 동영상, 오디오 같은 바이너리 데이터를 서버에서 받거나 클라이언트에서 만들면,
그 데이터를 바로 `<img>` 태그 같은 곳에 직접 넣을 수 없습니다.
(예: img.src = blob 이런 식은 안 됨)
대신 이 바이너리 데이터를 가리키는 임시 URL을 만들어서 src에 넣으면 브라우저가 이를 인식해서 보여줍니다.



## 2. File이란?

- **File**  
  - Blob을 확장한 객체로, 파일 이름(`name`), 마지막 수정시간(`lastModified`) 등의 메타정보를 포함하고 있습니다.  
  - 주로 `<input type="file">`이나 드래그앤드롭으로 사용자 파일 선택 시 생성됩니다.  
  - Blob의 모든 메서드를 사용할 수 있습니다.  
  - 예를 들어 사용자가 업로드할 이미지 파일 객체로 활용됩니다.  

#### ✅ File이란 사용 예시
```.ts
// 사용자가 선택한 파일 처리
function FileUploader() {
  const handleFileChange = (e) => {
    const file = e.target.files[0]; // File 객체
    console.log(file.name);          // 파일명 출력
    console.log(file.size);          // 파일 크기 출력

    // File은 Blob이므로 blob 메서드 사용 가능
    file.text().then(content => {
      console.log("파일 내용:", content);
    });
  };

  return <input type="file" onChange={handleFileChange} />;
}
```


---

###  Blob과 File의 차이점

| 구분         | Blob                         | File                             |
| ------------ | ----------------------------|-------------------------------- |
| 생성        | `new Blob()`로 생성 가능     | 사용자 입력으로 생성 (파일 선택) |
| 메타정보    | 없음                        | 파일명, 수정일 등 포함            |
| 용도        | 일반 바이너리 데이터 처리     | 실제 파일 데이터 표현            |
| 상속 관계   | 독립 객체                    | Blob을 상속한 객체               |


### Blob vs File — 언제, 왜 쓰이나?

| 구분           | Blob                                  | File                                   |
|----------------|-------------------------------------|--------------------------------------|
| **정의**        | 바이너리 데이터를 담은 불변(immutable) 덩어리 | Blob에 파일명, 수정일 등 메타정보가 추가된 객체 |
| **주 사용처**    | 네트워크로부터 받은 데이터, 데이터 가공용<br>예: 이미지, 영상, JSON 문자열 등을 바이너리 형태로 처리할 때 | 사용자로부터 직접 선택한 파일 (input[type="file"], 드래그앤드롭) |
| **생성 방법**    | `new Blob([...])`로 직접 생성 가능       | 보통 사용자가 선택한 파일에서 생성되거나 Blob을 기반으로 생성 |
| **특징**        | 내용 변경 불가 (불변), 메타정보 없음     | 파일명, 마지막 수정일 등 메타정보 포함, Blob의 기능 모두 가짐 |
| **언제 사용하면 좋나?** | 서버에서 내려온 바이너리 데이터 처리, 임시 데이터 생성 등<br>예) canvas 이미지 → Blob → 업로드 | 파일 업로드를 위해 실제 ‘파일’ 객체가 필요할 때<br>예) URL에서 이미지 받아와서 File 객체로 변환 후 업로드 |
---


## fetch와 Blob이 함께 쓰이는 이유

```js
export const convertURLtoFile = async (url: string) => {
  const response = await fetch(url);          // 1. URL로 리소스 요청
  const data = await response.blob();         // 2. 응답을 Blob으로 변환 (바이너리 덩어리)
  
  const ext = url.split(".").pop();            // 3. 확장자 추출 (ex: jpg, png)
  const filename = url.split("/").pop();       // 4. 파일명 추출 (ex: image.jpg)
  
  const metadata = { type: `image/${ext}` };   // 5. MIME 타입 지정 (ex: image/jpg)
  
  return new File([data], filename!, metadata); // 6. Blob 데이터를 File 객체로 변환하여 반환
};

```

- `fetch()`는 네트워크에서 리소스를 가져오는 함수입니다.
- **`blob()` 함수는 Response 객체(네트워크 응답)에 붙어있는 메서드입니다.**
- **`fetch()`를 사용하지 않고 Blob을 만들고 싶다면, 직접 new Blob([string])처럼 생성해야 합니다.**
- 서버에서 받은 데이터는 **기본적으로 스트림 형태**라서 곧바로 파일이나 이미지로 사용하기 어렵습니다.
- `response.blob()` 메서드는 응답 스트림을 **바이너리 데이터 덩어리(Blob)로 변환**합니다.
- 이 Blob을 다시 `File` 객체로 만들면, 파일 업로드 API 등에 바로 쓸 수 있는 형태가 됩니다.

> 스트림(stream) 형태란? 데이터가 한꺼번이 아니라 작은 조각으로 연속 전달되는 방식

### 🤔 서버에서 받은 데이터가 왜 바로 File로 변환되지 않고 Blob으로 변환해야 할까?
서버가 보내주는 데이터는 보통 HTTP 응답 바디(Stream) 입니다.
이 스트림을 바로 File 객체로 만들 수 있는 API는 없고,
먼저 Blob(바이너리 덩어리)로 변환해야만 File 생성 시 넣을 수 있는 데이터가 됩니다.
File은 Blob을 기반으로 만들어진 객체로, File 생성자는 Blob 배열을 받아서 만들기 떄문입니다.
즉, **Blob이 바이너리 데이터의 '기본 단위' 역할을 하기 때문에, Blob으로 변환 후 File로 만드는 과정이 필요합니다.**

### 🤔 그럼 여기서는 왜 File로 변환했을까?

 > **일부 API나 라이브러리에서는 File 객체를 명시적으로 요구합니다.**
 파일 이름이 필요하거나, API나 라이브러리에서 File 객체를 요구한다면
File로 변환하는 것이 안전하고 명확합니다.



## ✅ 요약 정리

- **Blob**은 바이너리 원시 데이터 덩어리이며, 파일 메타정보가 없음
- **File**은 Blob의 확장 객체로 파일명, 수정일 등의 정보를 포함함
- **fetch()**는 네트워크 요청을 비동기 처리하는 브라우저 내장 함수이며, Promise 기반


| 객체명  | 역할 및 사용처                             | 반드시 file로 변환해야 하나?                   |
| ---- | ------------------------------------ | ------------------------------ |
| Blob | 바이너리 데이터 임시 저장, 렌더링, 전송 등 다양하게 활용 가능. 멀티미디어뿐 아니라 PDF, JSON, 캔버스 그래픽 등 다양한 바이너리 처리에 사용 | 아니요, Blob만으로도 충분히 의미 있고 많이 씁니다 |
| File | Blob에 파일명, 수정일 등 메타정보 포함한 객체. 주로 사용자 업로드 파일(멀티미디어, 문서 등) 처리에 사용 | 파일명, 수정일 등의 메타정보가 필요할 때만 변환           |

---

| 상황                  | Blob 사용 가능 여부            |
| ------------------- | ------------------------ |
| 이미지 편집 및 처리         | 가능                       |
| 이미지, 동영상, 문서 서버 전송 (업로드)     | 가능 (`FormData`에 Blob 넣기) |
| 파일명이나 수정일 등 메타정보 필요 | File 객체로 변환하는 게 좋음       |


### 🎯 둘 다 텍스트 파일 포함한 모든 데이터 처리 가능하고, 차이는 메타정보 유무와 주로 사용되는 상황 차이 정도



