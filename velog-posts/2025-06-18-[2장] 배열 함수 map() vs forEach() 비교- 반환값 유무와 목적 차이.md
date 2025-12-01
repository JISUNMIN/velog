### 비교

| 구분          | 함수 이름    | 반환값 종류         | 동작 방식                          | 활용 예시                   |
|-------------|------------|------------------|--------------------------------|--------------------------|
| 값 반환       | `map()`     | **배열 (새로운 배열)**   | 배열 요소를 변환하여 새로운 배열 생성    | 배열 요소 가공 및 변환용           |
| 부수 효과 수행 | `forEach()` |** undefined **       | 배열을 순회하며 부수 효과 수행           | 배열 순회하며 출력, 상태 변경 등      |

---

### 예시

```js
const arr = [1, 2, 3];

// map: 각 요소에 2를 곱해 새로운 배열 반환
const mapped = arr.map(x => x * 2); // [2, 4, 6]

-------------------------------------------------

// forEach: 각 요소를 콘솔에 출력, 반환값은 undefined
arr.forEach(x => console.log(x)); 

// forEach: 외부 변수에 누적해서 합 계산
let sum = 0;
arr.forEach(x => {
  sum += x;
});
console.log('sum:', sum); // sum: 6

// forEach: DOM에 리스트 항목 추가 (브라우저 환경에서 사용)
const ul = document.createElement('ul');
arr.forEach(x => {
  const li = document.createElement('li');
  li.textContent = `Value: ${x}`;
  ul.appendChild(li);
});
document.body.appendChild(ul);
```

### ✅ 요약 정리

**map()**은 **반환값(새 배열)이 필요할 때**, 데이터 변환용으로 사용

**forEach()**는 **반환값 필요 없고, 배열 순회하며 부수 효과를 내고자 할 때** 사용


