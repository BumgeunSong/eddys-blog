---
title: [Swift]  Value, Reference type에 관해 알아야 할 10가지
published_date: 2022-01-10 14:25
tags: swift
meta_description: 1. Value type은 '복사', Reference type은 '바로가기'다. (...) 
9. 꼭 `class`를 써야할 때만 써라.
meta_image: https://images.velog.io/images/eddy_song/post/5f74c63c-77fe-4b1e-a695-38f0bd526819/Value.001.png
lang: ko
---

# \[Swift\] Value, Reference type에 관해 알아야 할 10가지

*by eddy_song*

## 1. Value type은 '복사', Reference type은 '바로가기'다.

- Value type을 변수에 저장하면, 인스턴스 그 자체를 저장한다.
- Reference type을 변수에 저장하면, 인스턴스를 메모리(힙)에 저장하고, 그 메모리의 주소값을 변수에 저장한다.

이 둘의 차이는 할당을 했을 때 명확히 드러난다.

- Value type을 다른 변수에 할당하면, 인스턴스가 복사된다.
- Reference type을 다른 변수에 할당하면, 인스턴스이 아닌 주소값을 복사한다. 두 변수는 모두 같은 데이터를 가리키게 된다.

데스크탑의 폴더로 비유해보자.

- Value type은 복사해서 저장하기다. 폴더 전체를 복사해서 같은 폴더를 하나 더 저장한다.
- Reference type은 바로가기로 저장하기다. 해당 폴더를 가리키는 새로운 바로가기를 만들어서 저장한다.

## 2. Value type은 불변성이 있다.

Value type은 매번 복사되기 때문에 인스턴스의 데이터가 바뀌지 않는다. 저장된 인스턴스가 새로운 인스턴스로 바뀔 뿐이다. **Value type은 불변성(Immutability)이 있다.**

Reference type은 할당하면 여러 식별자가 같은 주소값을 가리키기 때문에, 코드의 다른 부분에서 데이터를 변경할 수 있다. **Reference type은 부수 효과(Side effect)가 생길 수 있다.  **

## 3. `'struct'`는 Value type, `'class'`는 Reference Type이다.

Swift에서는 `struct`, `enum`, `class` 3가지 키워드로 직접 타입을 만들 수 있다.

- `struct`와 `enum` 키워드로 생성한 모든 `type`은 Value type이 된다.
- `class` 키워드로 생성한 모든 type은 Reference type이 된다.

## 4. Swift에 이미 존재하는 타입은 기본적으로 Value type이다. (function/closure 제외)

Swift Standard library와 Foundation에 존재하는 거의 대부분 타입은 모두 Value type이다.

- Int, Float, Double, Bool, String, Array, Dictionary, Set, Tuple... 은 `struct`로 구현돼있다.
- 모두 value type이다.

딱 하나의 예외는 function, closure이다.

- 특정 변수에 저장한 function이나 closure를 다른 변수로 복사한다면, 데이터를 복사하지 않고 참조만 공유한다.

## 5. Collection은 Value type이면서, Reference type이기도 하다.

Collection 타입의 서브타입들 (Array, Dictionary, String 등)은 기본적으론 Value type이다. 하지만 내부 구현을 보면 둘이 섞여있다.

그 이유는 성능 때문이다.

- Array나 String은 많은 값을 내부에 포함하고 있다.
- 복사를 할 때마다 매번 이 값을 다 복사하면 시간이나 공간의 부담이 크다.

따라서 **Swift 컴파일러는 Copy-on-write 라는 방법을 쓴다.**

- A에 들어있던 Collection 값을 B라는 새로운 변수에 할당한다고 하자. 이 때 복사본을 만들지 않는다. Reference type처럼, 참조만 공유한다. Collection 내의 모든 값을 복사하는 부담이 줄어든다.
- 대신 B의 값에 변경이 발생하면, 잠깐 멈추고 새로운 복사본을 B에 만들어준다. 그리고 값을 변경한다.

Copy-on-write 방식 덕분에, **Reference type의 효율성과 Value type의 불변성을 둘 다 잡을 수 있다.**

- 할당은 많이 일어나지만, 변경은 그것보다 적게 일어난다. 복사의 비용을 줄일 수 있다.
- 만약 변경이 있으면 새로운 값을 복사한다. 원래 값은 변하지 않는다. 불변성도 유지할 수 있다.

## 6. 메모리에는 Text, Data, Stack, Heap 4가지 영역이 있다.

메모리는 긴 바이트의 리스트다. 이 바이트에는 순서대로 주소가 매겨져있다. 일반적으로 메모리를 4개의 영역으로 나눠서 활용한다.

![Memory](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-Swift-Value-Reference/assets/c41d101827218520478b32bac65faab2c3537905.png)

**Text 영역**은 앱이 실행해야 할 프로그램의 코드를 저장한다.

**Data 영역**은 프로그램의 전역 변수, 정적 변수를 저장한다. 어디서든 접근 가능하며, 프로세스가 끝날 때까지 유지되는 데이터다.

**Stack 영역**은 일시적인 데이터를 저장한다. 지역 변수와 파라미터가 저장된다. 우리가 함수를 호출할 때마다 Stack에 해당 함수에 해당하는 공간이 생긴다. 이 공간은 함수 실행이 끝나면 사라진다.

**Heap 영역**은 데이터를 지우기 전까지는 계속 유지되는 공간이다. Heap에 저장된 데이터는 반영구적으로 지속된다.

## 7. Value type은 Stack에, Reference type은 Heap에 저장된다.

**Value type의 인스턴스는 Stack에 저장된다.**

- 시스템은 현재 실행하는 스레드와 관련된 컨텍스트를 Stack에 저장한다.
- 스택 영역의 데이터는 CPU가 관리하고 최적화한다. 메모리에 빈 공간이 발생하지 않는다.
- **덕분에 Stack은 매우 빠르고 효율적이다.**

**Reference type의 인스턴스는 Heap에 저장된다.**

- 인스턴스 자체는 힙에 저장한다. 이 힙의 주소값을 식별자와 함께 스택에 저장한다. 이 주소값을 이용해 실행 중에 필요한 데이터를 가져올 수 있다.
- 스택과 다르게 힙에 있는 인스턴스가 더이상 필요 없어진 이후엔 직접 지워줘야 한다. 이 과정에서 힙을 검색하고, 빈 메모리를 다시 적절하게 삽입해줘야 하고, 무엇보다 동기화 문제를 막는 메커니즘을 구현해야 한다.
- **이 때문에 속도가 스택에 비해서 느리다.**

## 8. Value type이 Heap에, Reference type이 Stack에 저장되는 예외도 있다.

Swift의 구현을 자세히 들여다보면, 성능을 높이기 위해 예외 상황이 발생하기도 한다.

**Value type -\> Heap**

- Value type인 Array, Dictionary, Set, String 등은 최적화를 위해 Heap 공간을 같이 활용한다.

**Reference type -\> Stack**

- Stack은 전체 사이즈에 제한이 있고, 변수의 크기를 자유롭게 바꿀 수 없다는 특징이 있다.
- 따라서 Reference type 중에서도 크기가 고정이 되어있거나, 언제 지워야할지 컴파일러가 미리 예측할 수 있는 경우에는 가급적 Stack을 사용해서 성능을 향상시킨다.

## 9. 꼭 `'class'`를 써야할 때만 써라.

struct와 class를 쓰는 기준은 무엇일까?

간단하다. **가급적 Struct를 쓴다.** Struct가 훨씬 빠르고 안전하다.

꼭 class를 써야할 이유가 있을 때만 class를 쓴다.

1\) 고유성이 필요한 인스턴스일 때

- 레퍼런스 타입의 인스턴스는 ‘아이덴티티’를 가진다. 단순히 값이 같다고 해서 두 인스턴스가 같다고 할 수 없다. 밸류 타입의 인스턴스는 그냥 ‘값’이다. 두 값이 같으면 동일하다고 판단한다.
- 예를 들어, 위치값을 저장하는 position과 학생을 저장하는 ‘student’가 있다고 하자.
- 위치값에는 고유한 아이덴티티가 없다. x, y 값이 같으면 같다. 이 경우에는 struct가 적합하다.
- 반면 학생에게는 고유한 아이덴티티가 있다. 이름과 나이가 같다고 해서 똑같은 학생은 아니다. 이 경우에는 class가 적합하다.

2\) Objective-C와 호환성이 필요할 때

3\) 변경가능한 상태를 공유하는 것이 꼭 필요할 때

- 데이터의 상태를 계속 바꿔서 업데이트해야 할 때
- 예를 들어, Swift에서 Linked list를 구현하는 경우.

## 10. 상속이 필요하다면 `'class'`가 아니라 `'struct'` + `'protocol'`을 쓰자.

- struct는 class와 달리 상속을 할 수 없다. 따라서 상속이 필요할 때 class를 쓰면 되겠구나... 할 수도 있다.
- Swift에는 상속 말고도 타입 계층을 만들 수 있는 protocol이 있다.
- protocol은 상속보다 활용도가 높으며 Swift에서는 protocol을 사용하는 것을 더 권장한다. (Swift가 protocol-oriented language라고 불리는 이유다.)
- class와 상속보다는, struct과 protocol을 통해 타입 계층을 구현하자.

### 참조 링크

- [Value Types and Reference Types in Swift](https://www.vadimbulavin.com/value-types-and-reference-types-in-swift/)
- [Swift Apprentice](https://www.raywenderlich.com/books/swift-apprentice/v7.0/chapters/13-classes)
- [Swift의 Type과 메모리 저장 공간](https://sujinnaljin.medium.com/ios-swift%EC%9D%98-type%EA%B3%BC-%EB%A9%94%EB%AA%A8%EB%A6%AC-%EC%A0%80%EC%9E%A5-%EA%B3%B5%EA%B0%84-25555c69ccff)
- [Choosing Between Structures and Classes](https://developer.apple.com/documentation/swift/choosing_between_structures_and_classes)
- [Struct vs classes in Swift: The differences explained](https://www.avanderlee.com/swift/struct-class-differences/)
