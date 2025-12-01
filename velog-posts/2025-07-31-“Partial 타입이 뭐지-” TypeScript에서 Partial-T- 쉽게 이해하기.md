React나 TypeScript 개발을 하다 보면 `Partial<T>`라는 타입을 자주 볼 수 있습니다.
처음 보면 이름도 어렵고, 어떤 용도로 쓰이는지 헷갈릴 수 있습니다. 

이 글에서는 TypeScript의 유틸리티 타입 중 하나인 `Partial<T>`를 알아 보겠습니다.

---

## 🤔 Partial<T>란?

`Partial<T>`는 TypeScript가 제공하는 내장 유틸리티 타입으로,  
제네릭 타입 `T`의 모든 속성을 **선택적(optional)** 으로 바꿔주는 타입입니다.

즉, 원래 필수였던 속성들을 모두 ‘있어도 되고 없어도 되는’ 상태로 만들어 줍니다.

---

## 왜 필요할까?

예를 들어 사용자 정보를 담는 타입이 있습니다.

```ts
interface User {
  id: number;
  name: string;
  email: string;
  profileImage?: string;
}
```
`User` 타입은 `id`, `name`, `email`이 필수 속성이었습니다.
그런데 실제로는 모든 정보를 다 수정하지 않고, 일부 정보만 바꾸고 싶을 때가 있었습니다.

이럴 때 전체 User 객체를 다 넘기지 않고, 수정하려는 일부 속성만 넘기도록 도와주는 것이 `Partial<User>`입니다.
  
  ## Partial<User>가 되면?

```ts
type PartialUser = Partial<User>;
// 실제 타입은 이렇게 바뀌게 됩니다.
{
  id?: number;
  name?: string;
  email?: string;
  profileImage?: string;
}
  ```
  모든 필드가 선택적이 되었기 때문에, 필요한 속성만 골라서 전달할 수 있습니다.
  
  ## 실제 사용 예

```ts
function updateUser(userId: number, updates: Partial<User>) {
  // updates에는 user 정보 중 수정할 일부만 들어갈 수 있었습니다
  // 예를 들어 { name: "새 이름" } 또는 { profileImage: "url" } 형태가 가능했습니다
}
  
updateUser: (partialUser: Partial<User>) =>
  set((state) => ({
  user: state.user ? { ...state.user, ...partialUser } : null,
})),
  ```
  
Partial 덕분에 필요한 부분만 넘겨도 타입 오류 없이 사용할 수 있습니다.

## 📝 마무리

- `Partial<T>`는 타입 `T`의 모든 속성을 선택적(optional)으로 만들어 줍니다.  
- 일부만 수정하거나 업데이트할 때 매우 유용합니다.  
- React와 TypeScript를 함께 사용할 때 상태 업데이트 함수 등에 자주 사용합니다.  

---

- 하지만 `Partial<T>`는 타입 `T`의 모든 속성을 optional로 만들기 때문에,  
  특정 속성만 선택적으로 만들고 싶을 때는 적합하지 않습니다.  

- 특정 속성만 optional로 만들고 싶다면,  
  `Pick`이나 `Omit` 같은 유틸리티 타입과 조합하거나  
  직접 타입을 커스텀해서 사용하는 방법이 있습니다.

---

다음 글에서는 `Pick`과 `Omit`에 대해 알아보겠습니다.