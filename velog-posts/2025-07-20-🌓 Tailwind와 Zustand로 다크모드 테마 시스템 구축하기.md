프로젝트에서 다크모드가 필수적으로 필요할 것 같아 직접 구현하면서 정리해보았습니다.  
전역 상태 관리는 **Zustand**를 사용했고,  
스타일은 **Tailwind CSS**가 기본 제공하는 CSS 변수를 커스텀하여 라이트/다크 모드 전환을 쉽게 적용할 수 있도록 했습니다.  

- 전역 테마 상태는 `Zustand`로 관리
- 공통적으로 적용되는 스타일은 `CSS에서 태그에 직접 지정`
- 컴포넌트별로 세부 스타일이 필요한 경우는 `CSS 변수로 설정`
- Tailwind CSS 기반이지만, 스타일 일관성을 위해 커스터마이징된 변수와 전역 스타일 활용

---


## 1. Zustand로 전역 테마 상태 관리
```ts
// src/app/store/useThemeStore.ts
import { create } from "zustand";
import { persist } from "zustand/middleware";

type Theme = "light" | "dark";

interface ThemeState {
  theme: Theme;
  toggleTheme: () => void;
  setTheme: (theme: Theme) => void;
}

export const useThemeStore = create<ThemeState>()(
  persist(
    (set) => ({
      theme: "light",
      toggleTheme: () =>
        set((state) => ({ theme: state.theme === "light" ? "dark" : "light" })),
      setTheme: (theme) => set({ theme }),
    }),
    {
      name: "theme-storage", // localStorage key
    }
  )
);
```

## 다크모드 토글 컴포넌트 예시
```tsx
<button
  onClick={toggleTheme}
  className="btn-icon absolute top-4 right-4 p-2 rounded-full hover:bg-[var(--hover-bg)] transition"
>
  {theme === "light" ? <SunHigh size={24} /> : <Moon size={24} />}
</button>
```

 ## 2. CSS 변수 기반 테마 구성 (global.css)
Tailwind에서 제공하는 기본 스타일을 기반으로, 프로젝트에 맞게 커스텀하여 사용했습니다.
 
### 🌞 Light 모드
```css
:root {
  --background: #ecf1ef;
  --foreground: oklch(0.145 0 0);
  --hover-bg: oklch(0.92 0 0);
  ...
}

```
### 🌚 Dark 모드
```css
:root {
  --background: #111827;
  --foreground: oklch(0.985 0 0);
  --hover-bg: oklch(46.585% 0.00256 16.113);
  ...
}

```

### 🌐 글로벌 공통 스타일
태그별 스타일의 일관성을 유지하기 위해 전역적으로 공통 스타일을 지정했습니다.
```css
@layer base {
  * {
    @apply border-border outline-ring/50;
  }

  p, h2, h3, div {
    color: var(--foreground);
  }

  label {
    color: var(--text-base);
  }

  input {
    @apply flex-1 border-none bg-transparent p-0 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500;
  }

  body {
    background-color: var(--background);
  }
}

```

### @layer의 역할과 우선순위
Tailwind CSS에서 `@laye`r는 CSS를 기능별로 나누고 **우선순위를 제어하기 위한 구조**입니다.

| Layer               | 설명                                          | 우선순위 |
| ------------------- | ------------------------------------------- | ---- |
| `@layer base`       | 태그 자체에 스타일을 입히는 전역 스타일 (ex. h1, body, p)             | 낮음   |
| `@layer components` | 컴포넌트 단위의 스타일 (예: 버튼, 카드 등)                  | 중간   |
| `@layer utilities`  | 유틸리티 클래스 정의 (ex: animation, custom class 등) | 높음   |

우선순위: `utilities` > `components` > `base`

> 왜 utilities가 우선순위가 가장 높을까?
유틸리티 클래스는 "딱 한 기능"만 하는 정확한 스타일이기 때문에 가장 구체적인 스타일로 간주됩니다.
따라서 base나 components보다 더 나중에 적용되어 override(덮어쓰기) 할 수 있습니다.

#### `@layer base`
HTML 태그에 직접 적용되는 전역 스타일 정의
```css
@layer base {
  * {
    @apply border-border outline-ring/50;
  }

  p,
  h2,
  h3,
  div {
    color: var(--foreground);
  }

  label {
    color: var(--text-base);
  }

  button {
    cursor: pointer;
  }

  input {
    @apply flex-1 border-none bg-transparent p-0 focus:outline-none focus:ring-0 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500;
  }
}

```
#### `@layer components`
여러 유틸리티를 조합하여 컴포넌트 단위로 재사용할 수 있는 스타일 정의
```css
@layer components {
  .inputDivStyle {
    @apply flex items-center rounded-md px-3 py-2 text-sm text-gray-700 dark:text-gray-300 transition-colors duration-300 border border-gray-300 dark:border-gray-600 focus-within:border-2 focus-within:border-gray-700 dark:focus-within:border-blue-500;
    background-color: var(--input);
  }

  .cardStyle {
    @apply shadow-2xl rounded-lg border border-gray-200 dark:border-gray-700 transition-colors duration-300;
    background-color: var(--item-bg);
    box-shadow:
      0 -1px 4px rgba(0, 0, 0, 0.3),
      0 4px 6px rgba(0, 0, 0, 0.7); 
  }
}

```
#### `@layer utilities`
단일 기능 중심의 유틸리티 클래스 정의 (보통 하나의 동작에 특화됨)
```css
@layer utilities {
  .btn-fill-loading {
    @apply relative overflow-hidden bg-blue-600 text-white;
  }

  .scale-fade {
    @apply transform scale-95 opacity-0 transition-all duration-300;
  }
}

```

```tsx
<Button
  type="submit"
  className={cn(
    "bg-blue-600 text-white hover:bg-blue-700",
    isCreatePending && "btn-fill-loading"
  )}
  disabled={isListPending || isCreatePending || !isValid}
>
  {isCreatePending ? "생성 중..." : "확인"}
</Button>
```
isCreatePending이 true일 때 .btn-fill-loading 클래스가 추가되어 로딩 시의 스타일이 적용됩니다.


### 💡기타 핵심 개념
`@apply`
Tailwind 유틸리티 클래스를 CSS 안에서 재사용할 수 있도록 해주는 디렉티브입니다.
- **@apply 사용 시**

```css
.button {
  @apply px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600;
}
```
- **@apply 미사용시**
```css
.button {
  padding: 0.5rem 1rem;           /* px-4 py-2 */
  background-color: #3b82f6;      /* bg-blue-500 */
  color: white;                   /* text-white */
  border-radius: 0.25rem;         /* rounded */
}
```

즉,**Tailwind의 유틸리티 클래스**(예: bg-gray-500, text-white 등)를 **CSS 내부에서 직접 쓸 수 있게 해주는 문법**입니다.

`@keyframes`
CSS 애니메이션을 정의하는 문법입니다.
```css
@keyframes fillGradient {
  0%   { transform: translateX(-100%); opacity: 0.4; }
  50%  { transform: translateX(0%); opacity: 0.9; }
  100% { transform: translateX(100%); opacity: 0.4; }
}

```
### 애니메이션 가능한 대표 속성들

- `opacity`
- `transform`
- `color`
- `background-color`
- `width`
- `height`
- `top`
- `left`
- `margin`
- `padding`

> 참고: `@keyframes`에는 애니메이션이 가능한 CSS 속성만 사용해야 하며,  
> 애니메이션이 불가능한 속성을 넣으면 효과가 나타나지 않거나 무시됩니다.


## ✅ 요약 정리

- 전역 상태는 **Zustand**로 관리했고, Tailwind에서 기본 제공하는 **CSS 변수**를 `:root`와 `.dark`에 커스텀하여 라이트/다크 모드를 쉽게 전환했습니다.
- **Tailwind `@layer` 구조**의 base → components → utilities 순서의 스타일 우선순위를 반드시 이해하고 작업해야 합니다.  
  우선순위를 알아야 스타일이 적용되지 않는 이유를 쉽게 파악할 수 있습니다. 
- **@apply**를 활용해 Tailwind 클래스를 CSS 내에서 재사용하면 유지보수를 훨씬 쉽게 할 수 있습니다.  
- **애니메이션은 `@keyframes`와 함께, opacity, transform 등 애니메이션 가능한 속성만 사용해야 정상 작동합니다.**