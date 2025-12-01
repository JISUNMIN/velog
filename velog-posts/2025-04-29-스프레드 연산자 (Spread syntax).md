스프레드 연산자에 대해 알아보자🤔

형식: ... 
주요 사용: 배열이나 객체를 펼쳐서 복사하거나, 조건부로 키를 추가할때 
설명: ... 이런 형태를 써서 배열이나 객체의 값을 '펼쳐서' 다른 곳에 복사하거나, 조립하거나, 수정할 수 있게 해주는 문법

✅ 배열에서 사용 예시 
```
const arr1 = [1, 2, 3];
const arr2 = [...arr1, 4, 5];
console.log(arr2); // [1, 2, 3, 4, 5]
```
🚫 의도하지 않은 결과
```
const arr1 = [1, 2, 3];
const arr2 = [arr1, 4, 5];
console.log(arr2); 
//[
  [1, 2, 3],
  4,
  5
]
```


✅ 객체에서 사용 예시 

```
const obj1 = { a: 1, b: 2 };
const obj2 = { ...obj1, c: 3 };
console.log(obj2); // { a: 1, b: 2, c: 3 }
```

🚫 의도하지 않은 결과
```
const obj1 = { a: 1, b: 2 };
const obj2 = { obj1, c: 3 };
console.log(obj2); // { obj1: { a: 1, b: 2 }, c: 3 }
```

|잘못된 방식|결과 |왜 문제인가
|---|:---|:---:|
|{ obj1 }|obj1이라는 키를 가진 객체가 생김|a, b를 펼치고 싶은데 중첩됨|
|[arr1, 4, 5]|[ [1,2,3], 4,5 ] (2중 배열)|1,2,3을 한 줄로 놓고 싶은데 묶임|


언제 쓰는지❔

|상황|스프레드 연산자를 사용하는 이유
|---|:---
|객체를 복사 할때|원본 객체를 훼손하지 않고 새 객체를 만들기 위해|
|배열을 복사 할때|원본 배열을 그대로 두고 새로운 배열을 만들기 위해|
|여러 객체/배열을 합칠 때|Object.assign이나 Array.contat 대신 더 간단한 방법|
|조건부로 키를 추가할때|특정 값이 있을 때만 객체에 포함시키려고|
|컴포넌트로 props 넘길 때|컴포넌트에 props를 한번에 넘기려고|

⚠ 주의 할점
스프레드는 "얕은 복사(shallow copy)"이기 때문에 똑같은 키가 겹치면 뒤에 오는 값이 앞의 값을 덮어 쓰게 됨
```
const a = { value: 1 };
const b = { value: 2, other: 3 };
const c = {...a, ...b};
console.log(c); // { value: 2, other: 3 }
```

🔥 정리
spread 연산자(...)를 쓰면
"안에 있는 값들을 꺼내서
바깥쪽**(같은 depth)**에 쭉 펼친다"

#### 적용한 코드 
```
      const payload = {
        ...(data.originalContentId && { originalContentId: data.originalContentId }),
      };
```

spread를 쓰지 않았을 때
```
const paylod : any = {};
if(data.originalContentId) paylod.originalContentId = data.originalContentId;
```
