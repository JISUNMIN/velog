## 1. REST API란?
- **REST API**는 "웹에서 정보를 주고받는 규칙"
- 우리가 인터넷에서 **주소(URL)**를 치면 서버에 요청을 보내고, 서버는 그에 맞는 **데이터**를 돌려줍니다.  
- 이때 주고받는 방식에 일정한 약속을 만든 게 **REST API**

---

## 2. 핵심 개념
- **자원(Resource)** : 정보를 뜻함 (예: 사용자, 게시글, 상품 등)  
- **주소(URL)** : 자원이 있는 위치 URI 형식 (예: `/users/1`)  
- **행동(Method)** : 무엇을 할지 정하는 동사 (GET, POST, PUT, DELETE)  

---

## 3. HTTP 메서드 쉽게 이해하기
| 메서드  | 뜻 | 예시 |
|---------|-----|------|
| GET     | 가져오기 | `GET /users` → 사용자 목록 보기 |
| POST    | 새로 만들기 | `POST /users` → 새 사용자 등록 |
| PUT     | 전체 바꾸기 | `PUT /users/1` → 1번 사용자 정보 싹 다 바꾸기 |
| PATCH   | 일부만 바꾸기 | `PATCH /users/1` → 1번 사용자 이름만 수정 |
| DELETE  | 삭제하기 | `DELETE /users/1` → 1번 사용자 삭제 |

👉 정리하면, **URI(주소)는 "무엇"을, 메서드는 "어떻게"를 나타냄**  

---

## 4. 예시
🛒 쇼핑몰 서비스 서비스

- `GET /products` → 상품 목록 보기  
- `POST /products` → 새 상품 등록  
- `GET /products/10` → 10번 상품 상세 보기  
- `PUT /products/10` → 10번 상품 정보 수정  
- `DELETE /products/10` → 10번 상품 삭제  

---

## 5. 왜 쓰는 걸까?
- **규칙이 단순**해서 누구나 이해하기 쉽고  
- **표준화**되어 있어서 다양한 서비스(앱, 웹, IoT 등)에서 쉽게 사용 가능합니다. 
- 그래서 오늘날 대부분의 앱과 웹 서비스가 **REST API**를 사용합니다.

---

## 6. RESTful API란?
- **REST 원칙을 잘 지켜서 만든 API**를 말합니다.  
- 즉, 주소(URI)에는 자원(Resource)만 표현하고, 행동(Method)은 HTTP 메서드(GET, POST 등)로만 구분하는 방식입니다.  
- 모든 REST API가 RESTful한 것은 아니며, RESTful하지 않은 경우는 규칙을 어기고 주소에 동사 같은 행동이 들어갑니다. 

### 예시 비교
❌ REST API지만 RESTful하지 않은 경우: **URI에 동사가 들어감**
```
POST /getUserInfo → URL에 "get"이라는 행동이 들어가 있음 ❌
GET /updateUser → URL에 "update"라는 행동이 들어가 있음 ❌
```
✅ RESTful API: **URI에 자원만 가리키고 있음**
```
GET /users/1 → 1번 사용자 정보 조회
PUT /users/1 → 1번 사용자 정보 수정
DELETE /users/1 → 1번 사용자 삭제
```

👉 정리하면, RESTful 여부가 갈리는 핵심은 **URL(자원 표현 방식)**을 잘지켰느냐의 차이
Method는 이미 정해진 동작 규칙이 있어서 RESTful 여부가 갈리지 않음.

- **REST API**: REST 스타일을 참고해서 만든 API (규칙 일부만 지켜도 됨)
- **RESTful API**: REST 원칙을 충실히 따른 API (자원=URL, 동작=Method)

그래서 "모든 RESTful API는 REST API이지만, 모든 REST API가 RESTful한 건 아니다"라는 말이 나온 것입니다.
