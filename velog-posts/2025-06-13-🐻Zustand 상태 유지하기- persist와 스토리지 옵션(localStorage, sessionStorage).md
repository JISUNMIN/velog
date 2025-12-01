## persist란?
- **상태를 브라우저 저장소(localStorage, sessionStorage 등)에 자동으로 저장하고 복원해주는 미들웨어입니다.**
- persist는 상태를 localStorage 등에 저장해서 새로고침해도 상태가 유지되게 해줍니다.(**기본값: localStorage**)
- 두 번째 인자로 옵션 객체를 받는데, 여기서 name은 저장할 key 이름이며 상태별로 유니크한 값으로 지어야 합니다.

```
// counterStore.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface CounterState {
  count: number
  increase: () => void
  decrease: () => void
}

export const useCounterStore = create<CounterState>()(
  persist(
    (set) => ({
      count: 0,
      increase: () => set((state) => ({ count: state.count + 1 })),
      decrease: () => set((state) => ({ count: state.count - 1 })),
    }),
    {
      name: 'counter-storage', // localStorage에 저장될 key 이름
    }
  )
)
```

## ✅ sessionStorage로 저장하는 방법
```
    {
      name: 'counter-storage',
      storage: createJSONStorage(() => sessionStorage) // ✅ localStorage → sessionStorage로 변경
    }
 ```

## 🤔createJSONStorage란? 왜 필요할까?
Zustand에서 persist 미들웨어와 함께 쓸 수 있는 헬퍼 함수로,
localStorage나 sessionStorage 같은 string-only 스토리지에
자동으로 **JSON.stringify / JSON.parse**를 적용해주는 래퍼(wrapper) 함수입니다.
브라우저의 localStorage나 sessionStorage는 문자열(string)만 저장할 수 있기때문에,
```
sessionStorage.setItem('user', { name: 'minji' }) // ❌ 에러
sessionStorage.setItem('user', JSON.stringify({ name: 'minji' })) // ✅
```
기본적으로 `persist` 미들웨어가 내부에서 JSON 변환을 해주지만,
`sessionStorage` 같은 커스텀 저장소를 직접 사용할 때는 JSON 변환을 수동으로 처리해야 합니다.
이 과정을 안전하게 도와주는 함수가 바로 `createJSONStorage`입니다.

### ✅ storage 옵션별 차이점

| 값                      | 의미                          |
| ---------------------- | --------------------------- |
| `() => localStorage`   | 브라우저에 영구 저장 (기본값)           |
| `() => sessionStorage` | 탭을 닫으면 사라지는 임시 저장소 사용       |
| 커스텀 객체                 | 예: 쿠키, IndexedDB 등 직접 구현 가능 |


## 📝 마무리

`persist` 미들웨어는 **사용자의 상태를 브라우저 저장소에 자동 저장**해서 새로고침이나 탭 종료 후에도 상태를 유지해야 할 때 유용합니다.
로그인 정보, UI 상태, 장바구니 정보 등을 유지할 때 사용합니다.

> 참고) [새로고침해도 댓글 상태를 유지하고 싶다면?](https://velog.io/@sunmins/%EC%83%88%EB%A1%9C%EA%B3%A0%EC%B9%A8%ED%95%B4%EB%8F%84-%EB%8C%93%EA%B8%80-%EC%83%81%ED%83%9C%EB%A5%BC-%EC%9C%A0%EC%A7%80%ED%95%98%EA%B3%A0-%EC%8B%B6%EB%8B%A4%EB%A9%B4-useState-Zustand)

기본적으로 `localStorage`에 저장하지만, 휘발성 데이터가 필요할 땐 `sessionStorage`를 사용할 수 있습니다.
`createJSONStorage`를 활용하면 저장소가 문자열만 다루는 한계를 안전하게 처리할 수 있습니다.