✅ 일급 객체 (First-Class Citizen)란?
프로그래밍 언어에서 **값처럼 다룰 수 있는 요소**를 말함. 즉, 변수에 할당하고, 함수의 인자로 넘기고, 반환값으로 받을 수 있는 대상

✔️ 일급 객체의 조건 3가지를 다 만족 해야함
- 변수에 할당할 수 있어야 한다
- 함수의 인자로 전달할 수 있어야 한다
- 함수의 반환값으로 사용할 수 있어야 한다


 📌 예시: 자바스크립트에서 함수는 일급 객체
 
 ```
 // 1. 변수에 할당
const sayHello = function() {
  console.log("Hello");
};

// 2. 함수의 인자로 전달
function execute(fn) {
  fn(); // sayHello 함수 실행
}
execute(sayHello);

// 3. 함수에서 반환
function createGreeter() {
  return function() {
    console.log("Hi!");
  };
}
const greeter = createGreeter();
greeter();

 ```
 
 ✅ 유사 개념: 고차 함수 (Higher-Order Function)
 - 고차 함수는 일급 객체 개념을 활용한 함수로 함수가** 다른 함수를 인자로 받거나 함수를 반환하면 고차 함수**
 
🎯정리
 일급 객체는 **값처럼 자유롭게 다룰 수 있는 대상**이고, JavaScript의 함수는 일급 객체임고차 함수는** 함수를 인자로 받거나 반환하는 함수**