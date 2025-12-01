이번 글에서는 리액트 프로젝트에서 자주 사용하는 **Testing Library**와  
테스트 러너 **Vitest**의 개념, 설치 방법, 그리고 실제 사용 시점을 알아보겠습니다.

UI 개발 과정에서 테스트 코드를 작성해야 하는 이유와,  
Vitest와 Testing Library가 함께 어떤 역할을 수행하는지도 살펴보겠습니다.

---

## 왜 테스트 라이브러리를 써야 할까?

UI가 겉보기에는 정상적으로 보이더라도, 내부 로직이 잘못 동작하고 있을 수 있습니다.

예를 들어:

- 클릭 이벤트가 호출되지 않음  
- 상태 업데이트가 잘못됨  
- 조건부 UI가 예상과 다르게 표시됨  

> 테스트 코드는 이런 “눈에 보이지 않는 오류”를 잡아주는 **자동화된 안전망**입니다.

---


## 🤖 자동 테스트의 필요성

### 1️⃣ 수동 테스트는 단발성

- 직접 눌러봐야 함 
- 기능이 많을수록 반복이 늘어남
- 사람이 실수할 여지가 많음

### 2️⃣ 테스트 코드는 자동 확인 장치

```bash
npm run test
```

한 번 작성하면 커밋/배포 전마다 자동 검증됨.

### 3️⃣ 코드 수정이 다른 기능을 깨뜨릴 수 있음

UI는 같아 보이지만 내부 동작이 달라진 문제를 테스트는 찾아냄.

---

## ⚙️ 설치 방법

Testing Library와 Vitest는 함께 사용하는 경우가 많습니다.  
테스트 환경을 구성하기 위해서는 다음 세 가지 구성요소가 필요합니다.

| 구성 요소 | 역할 |
|------------|------|
| **Vitest** | 테스트 러너 (테스트 코드를 실행하고 결과를 평가) |
| **jsdom** | 브라우저 없이도 DOM 환경을 흉내 내는 가상 브라우저 |
| **Testing Library** | 사용자의 실제 행동을 시뮬레이션 |

### 설치 명령

```bash
npm install -D vitest jsdom @testing-library/react @testing-library/user-event
```

---

## 🤔 무엇을 테스트해야 할까? 
테스트를 작성할 때 많이 하는 오해 중 하나는  
"컴포넌트의 모든 동작을 100% 테스트해야 한다"는 생각입니다.  
하지만 실제로는 다음 원칙이 훨씬 중요합니다.

---

### ✔ 핵심 기능만 테스트하면 충분하다
- 사용자에게 중요한 기능  
- 비즈니스 로직이 영향을 받는 부분  
- 오류가 나면 큰 문제가 되는 기능  
- 상태 변화가 중요한 핵심 시나리오  

예를 들어 로그인 화면이라면:

- **아이디/비밀번호 입력 → 로그인 요청 호출됨** → ✔ 필수 테스트  
- 버튼에 특정 CSS 클래스가 있는가? → ❌ 비핵심  
- input blur 시 border 색이 바뀌는가? → ❌ 비핵심  

불필요한 테스트는 유지보수 비용만 증가시키므로 지양해야 합니다.

### ✔ 모든 페이지와 모든 컴포넌트를 테스트할 필요는 없다

React 프로젝트라고 해서 “페이지 개수 = 테스트 파일 개수”일 필요는 없습니다.  
중요한 점은 **페이지 단위가 아니라 기능 단위로 테스트 대상을 결정**하는 것입니다.

즉,

- 로직이 많다고 해서 페이지 전체를 테스트해야 하는 것이 아니고  
- 공통 컴포넌트(Button, Input 등)도 **단순 UI일 경우 테스트할 필요 없으며**  
- 복잡한 로직이나 중요한 기능이 담긴 부분만 테스트하면 충분합니다.

대부분의 비즈니스 로직은 페이지 안이 아니라  
**커스텀 훅(useXXX)이나 독립된 작은 컴포넌트**에 들어있기 때문에  
페이지 하나 전체를 테스트하는 대신,  
**핵심 로직이 있는 부분만 선택적으로 테스트**하는 것이 훨씬 효율적입니다.

프로젝트 페이지가 20개여도 테스트 파일은 5~8개만 있을 수도 있고,  
반대로 핵심 기능이 많다면 테스트가 늘어날 수도 있습니다.


---

# 테스트 도구 개념 정리

##  테스트 러너(Vitest)란?

테스트 러너(Test Runner) 는 테스트 코드를 실행하고 결과를 알려주는 도구입니다.

- 테스트 파일을 자동으로 찾고 실행  
- `test`, `expect` 같은 기본 테스트 문법 해석
- 통과/실패 여부 리포트  
- 테스트 환경(jsdom 등)과 연동 

즉, **테스트를 실제로 실행하는 엔진**입니다.
Vitest는 Vite 기반이라 실행 속도가 빠르고 개발 환경과 빠르게 맞물립니다.

---

## 🌐 jsdom이란?

jsdom은 브라우저 없이 DOM을 사용할 수 있게 해주는 가상 브라우저 환경입니다.

- `document`, `window`, `button`, `input` 같은 DOM API 사용 가능
- React 컴포넌트를 브라우저 없이 렌더링 가능  
- 클릭/입력 등 사용자 이벤트를 테스트 환경에서 그대로 재현  

즉, **테스트가 브라우저처럼 동작하도록 만들어주는 가짜 DOM 환경**입니다.
테스트 외에는 사용할 일이 거의 없습니다.

---

## 🧪 Testing Library란?

Testing Library는 **UI 테스트를 사용자 관점으로 진행하는 도구 모음**입니다.

주로 사용하는 것은 다음 패키지입니다:

```
@testing-library/react
```

Testing Library는 “사용자가 실제로 보는 기준”으로 테스트하는 것을 권장합니다.

---

### Testing Library 핵심 철학

> **“구현 세부가 아니라, 사용자 관점에서 테스트하라.”**

예:

```tsx
screen.getByRole("button", { name: "로그인" });
```

이 코드는 다음을 의미합니다:

- 사용자 눈에 버튼이 보여야 한다  
- 버튼의 접근성 role이 `button`이어야 한다  
- 버튼 텍스트가 "로그인"이어야 한다  

---

## 📚 Vitest 테스트 문법 정리

### ✔ describe — 테스트 그룹
`describe`는 **관련된 테스트들을 하나의 묶음(그룹)** 으로 관리하는 블록입니다.

```ts
describe("로그인 기능", () => { ... })
```
**언제 필요할까?**
- 기능별 / 컴포넌트별로 테스트를 그룹화할 때
- 테스트 결과 리포트가 더 읽기 쉬워짐
- 반복되는 초기화 작업을 beforeEach 등에 묶어 사용하기 좋음

**예:**
로그인 관련 테스트 3개, 회원가입 테스트 2개 식으로 묶으면 리포트가 훨씬 깔끔하게 정리됨.

### ✔ test / it — 개별 테스트 정의
`test()` 또는 `it()` 은 **하나의 동작을 검증하는 단위 테스트**를 정의합니다.

```ts
test("버튼 클릭 시 로그인 호출됨", () => {})
```
두 함수는 완전히 같은 기능이며, 취향/팀 컨벤션에 따라 선택하면 됩니다.

**언제 필요할까?**
- 특정 동작을 기대한 대로 수행하는지 테스트하고 싶을 때
- 하나의 test는 하나의 행동(기능) 을 검증해야 가장 좋은 테스트 구조가 됨

**예:**
- "버튼이 렌더링된다"
- "버튼 클릭 시 이벤트가 발생한다"
- "에러 메시지가 화면에 표시된다"
- 각각을 별도 test로 분리하는 것이 좋음.

### ✔ expect — 결과 검증
`expect()`는 테스트의 **결과를 검증하는 핵심 함수**입니다.
테스트가 통과하려면 expect 조건이 모두 true여야 합니다.

```ts
expect(value).toBe(10)                 // 값 비교
expect(fn).toHaveBeenCalled()          // 함수 호출 여부
expect(element).toBeInTheDocument()    // DOM 존재 여부
```
**자주 쓰는 매처(example matcher):**
- `.toBe()` → 값이 정확히 같은지
- `.toEqual()` → 객체/배열 비교
- `.toHaveBeenCalled()` → 함수가 호출되었는지
- `.toHaveBeenCalledWith()` → 특정 파라미터로 호출되었는지
- `.toBeInTheDocument()` → DOM 요소 존재 여부 (Testing Library matcher)

### ✔ vi.fn — Mock 함수
`vi.fn()`은 테스트에서 **가짜 함수(Mock)** 를 만들어주는 도구입니다.

```ts
const onLogin = vi.fn()

// 컴포넌트 실행
await userEvent.click(screen.getByRole("button"))

// onLogin이 호출됐는지 검증
expect(onLogin).toHaveBeenCalled()
expect(onLogin).toHaveBeenCalledWith({ id: "test", pw: "1234" })
```
**언제 필요할까?**
- 컴포넌트가 외부 함수(onClick, API 호출 등)를 호출하는지 확인할 때
- 실제 함수를 실행하고 싶지 않을 때 (API 요청, 네트워크 등)
- 함수를 몇 번 호출했는지, 어떤 값으로 호출했는지 검증할 때

즉, **Mock 함수는 컴포넌트의 동작을 관찰하는 카메라** 같은 역할을 합니다.

---

## 📚 Testing Library 문법 정리

Testing Library에서 가장 많이 사용하는 기능들을 정리하면 다음과 같습니다.

### ✔ render — 컴포넌트 렌더링

```tsx
render(<MyButton />);
expect(screen.getByRole("button")).toBeInTheDocument();
```

### ✔ screen — 렌더링된 화면 탐색

```tsx
screen.getByRole("button", { name: "저장" });
screen.getByLabelText("비밀번호");
```

### ✔ userEvent — 사용자 행동 시뮬레이션

```tsx
await userEvent.type(input, "test")
await userEvent.click(button)
```
---

## 📁 기본 파일 구조

```
src/
├─ components/
│  ├─ Button.tsx
│  └─ __tests__/Button.test.tsx
└─ App.tsx
```

---

## ⚙️ Vitest 설정

vitest.config.ts

```ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: "./src/setupTests.ts",
  },
});
```

---

## 🛠 실습: 로그인 폼 테스트 만들기

### 1. 로그인 컴포넌트 생성

`src/LoginForm.tsx`

```tsx
import { useState } from "react";

export default function LoginForm({ onLogin }) {
  const [id, setId] = useState("");
  const [pw, setPw] = useState("");

  const handleSubmit = () => {
    onLogin({ id, pw });
  };

  return (
    <div>
      <label>
        아이디
        <input value={id} onChange={(e) => setId(e.target.value)} />
      </label>

      <label>
        비밀번호
        <input value={pw} onChange={(e) => setPw(e.target.value)} />
      </label>

      <button onClick={handleSubmit}>로그인</button>
    </div>
  );
}
```

---

### 2. 테스트 파일 생성 및 코드 작성

`src/__tests__/LoginForm.test.tsx`

```tsx
// --- Vitest 문법 ---
import { describe, test, expect, vi } from "vitest";
// --- Testing Library 문법 ---
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import LoginForm from "../LoginForm";

// --- Vitest 문법 ---
describe("LoginForm", () => {
  test("아이디/비밀번호 입력 후 로그인 클릭 시 onLogin 호출됨", async () => {
    const onLogin = vi.fn();

    // --- Testing Library 문법 (컴포넌트 렌더링) ---
    render(<LoginForm onLogin={onLogin} />);

    // --- Testing Library + user-event 문법 (사용자 입력 시뮬레이션) ---
    await userEvent.type(screen.getByLabelText("아이디"), "sunmin");
    await userEvent.type(screen.getByLabelText("비밀번호"), "1234");
    // --- Testing Library 문법 (버튼 클릭) ---
    await userEvent.click(screen.getByRole("button", { name: "로그인" }));

     // --- Vitest 문법 (검증/단언) ---
    expect(onLogin).toHaveBeenCalledWith({
      id: "sunmin",
      pw: "1234",
    });
  });
});
```

### ⭐ Vitest vs Testing Library 역할 정리

| 구분 | 역할 | 테스트에서 하는 일 |
|------|------|---------------------------|
|  **Vitest** | "심판" 역할 | 테스트를 시작하고(`test`), 결과를 판단하고(`expect`), 기록함 |
| **Testing Library** | "플레이어" 역할 | 화면에 컴포넌트를 보여주고(`render`), 버튼 클릭/입력 같은 행동을 대신 해줌 |

### ❗ 왜 둘 다 필요할까?

- ✔ **Vitest만으로는 컴포넌트를 렌더링할 수 없습니다.**
- ✔ **Testing Library만으로는 테스트를 정의하거나 검증할 수 없습니다.**

따라서 **UI 테스트에서는 Vitest + Testing Library를 함께 섞어서** 사용합니다.

---

### 3. 테스트 실행

### Vitest 실행

```bash
npm run test
```

또는

```bash
npx vitest
```

### 실행 결과 예시

```
 PASS  src/__tests__/LoginForm.test.tsx
  LoginForm
    ✓ 아이디/비밀번호 입력 후 로그인 클릭 시 onLogin 호출됨 (95 ms)

Test Files  1 passed (1)
      Tests  1 passed (1)
   Start at  12:31:00
   Duration  0.50s
```

🟢 초록색 PASS가 뜨면 테스트 성공!  
🔴 FAIL이면 이유가 출력됨.

---


## 💡 정리
- **Vitest** → 테스트를 “실행하는 엔진”  
- **Testing Library** → UI를 “사용자처럼 조작·검증”하는 도구 
- **jsdom** → 브라우저 없이 DOM을 제공하는 “가상 브라우저”

세 가지를 결합하면 React UI를 안정적으로 테스트할 수 있습니다.
