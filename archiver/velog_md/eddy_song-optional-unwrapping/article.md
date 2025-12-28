---
title: 옵셔널(Optional)을 언박싱.. 아니 언래핑(Unwrapping) 해보자
published_date: 2022-01-16 13:16
tags: swift
meta_description: 옵셔널을 풀어서 값을 꺼내는 방법을 알아보자.
meta_image: https://images.velog.io/images/eddy_song/post/fea092eb-fe46-46d7-a2bc-be580a470c08/unboxing.webp
lang: ko
---

# 옵셔널(Optional)을 언박싱.. 아니 언래핑(Unwrapping) 해보자

*by eddy_song*

이제 우리는 옵셔널이 왜 필요한지 알았다.
옵셔널은 담아놓은 데이터에 '주의! 이 안에 nil 있을 수 있음'이라고 알려주는 포장지다.

옵셔널이 어떻게 구현되어있는지도 알았다.
옵셔널은 2개의 값(case)이 있는 enum으로 만들어져 있다.

이제 그럼, 옵셔널을 풀어서 안에 있는 값을 꺼내는 '언래핑(Unwrpping)' 방법을 알아보자.

말했듯이 Swift는 옵셔널을 바로 쓸 수 없도록 막는다.
옵셔널 타입의 인스턴스에 뭔가 하려면, 언래핑을 꼭 해줘야 한다.

Swift에는 옵셔널을 푸는 방법이 꽤나 많다.

크게 보면 안전하지 '않은' 방법 2개와, 안전한 방법 4개가 있다.

![unboxing](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-optional-unwrapping/assets/b6b38e472b5fa579d82280fb5ebf08ac56a17f4c.jpg)

> 박스 안에 든 것은 nil일까요, value일까요?

## 안전하지 않은 언래핑 방법

### 1. 강제 언래핑 Force Unwrapping (`!`)

옵셔널 타입의 값에 `!`를 붙여주면 안에 있는 값을 꺼낼 수 있다.

``` swift
let name: String? = "Eddy"
let unwrappedName = name!

print(unwrappedName) // "Eddy"
```

간단해서 좋아보인다. 하지만 만약 값이 `nil` 이라면?

``` swift
let name: String? = nil
let unwrappedName = name! // Unexpected Error
```

그 즉시 앱이 깨져버린다.

강제 언래핑이 위험한 이유다.

강제 언래핑은 값이 nil인지 아닌지 체크하지 않고, 바로 안에 있는 값을 꺼낸다.
만약 nil을 강제 언래핑하면, 프로그램 실행 중에 멈춰버린다.

따라서, 강제 언래핑은 쓰지 않는 것이 일반적이다.

이 옵셔널에 들어있는 값이 nil이 아니다! 라고 100% 확신할 수 있을 때만 쓸 수 있다.

하지만 내 생각이 틀렸을 수 있고, 코드는 계속 바뀐다. 예외 상황이 언제든 발생할 수 있다.

따라서 실무에서는 안 쓰는 것이 원칙이라고 많은 글에서 말한다.
(대부분의 경우 swift 코드에 느낌표가 있다면 부정적인 신호라고 봐도 무방하다.)

### 2. 암시적 언래핑 (Implicitly unwrapped optionals)

암시적 언래핑도 강제 언래핑과 비슷하게 nil인지 체크하지 않는다.
다만 차이점은 옵셔널 타입을 '선언'하는 시점에 타입 뒤에 ! 를 붙여준다는 점이다.

``` swift
let name: String! = "Taylor"
let nameCopy = name
```

이 때 name 상수는 `Optional<String>`이 맞다. 하지만 Swift 컴파일러가 언래핑을 강제하지 않는다.

실제로 nil 값을 가질 수 있는 옵셔널이지만, 옵셔널이 '아닌 것처럼' 쓸 수 있다.

타입 뒤에 붙은 !가 '이 타입은 옵셔널이 맞는데 꼭 체크 안해도 돼.' 라고 Swift 컴파일러에게 말하는 표시인 셈이다.

마찬가지로 nil인 경우에는 충돌이 일어나서 프로그램이 멈추게 된다.

아니 기껏 옵셔널로 만들어놓고 왜 이렇게 쓰는 걸까?

가끔 이런 옵셔널이 필요할 수 밖에 없는 때가 있다고 한다.

어떤 값이 처음에는 nil이지만, 우리가 그걸 다루려고 할 때는 무조건 nil인 상황이 있다.

이럴 때는 매번 언래핑을 하는 것보다 암시적 언래핑을 한 타입으로 선언하는 게 낫다.

안전성이 확실하다면, 편의성을 위해서 강제 nil 체크를 풀어줄 수 있다는 뜻이다.

대표적인 사례가 바로 인터페이스 빌더의 아웃렛(IBOutlet)이다.

``` swift
@IBOutlet var imageView: UIImageView!
```

인터페이스 빌더에서 아웃렛을 만들 때 실제 동작을 보자.

먼저, Vide controller 객체가 먼저 생성이 된다.
View Controller를 생성할 시기에는 Outlet이 nil이다.

하지만 View가 실제로 불러와지고 나면, Outlet에 값이 할당이 된다.
View Controller가 없어질 때까지 outlet의 값은 없어지지 않는다.

즉, 우리가 코딩을 할 때엔 Outlet에는 값이 '있다'는 것이 100% 확실하다.
그래서 UIKit은 알아서 IBoutlet을 암시적 언래핑한 옵셔널로 만들어놓는다.

애플 형님들이 '값 들어있는 거 확실하니까 걱정하지 말고 써'하면서
`!` 를 붙여줬구나... 하고 이해하면 된다.

## 안전한 언래핑 방법

안전한 방법과 아닌 방법의 차이는 당연하게도 '값이 nil인지 아닌지 체크하느냐' 여부다.
당연하게도 swift 코드를 쓸 때는 안전한 언래핑 방법을 사용해야 한다.

안전한 방법 4가지를 차례대로 알아보도록 하자.

### 1. 옵셔널 바인딩 (Optional Binding)

옵셔널 바인딩은, 다음 2가지가 합쳐진 것이다.

1\) nil인지 아닌지 체크하는 조건문,
2) (nil이 아니면) 선언한 변수명에 값을 대입하는 바인딩(Binding)

#### 1) `if let`

조건문의 if와 선언문의 let이 합쳐진 `if let`을 써준다.
가장 많이 쓰는 언래핑 방법이다.

``` swift
let name: String? = "Eddy"

if let unwrappedName = name {
    print("Hello, \(unwrappedName)!")
} else {
    print("Hello, anonymous!")
}
```

이 코드를 보면 = 연산자 오른쪽에 있는 `name`의 값을 먼저 확인하고,
해당값이 nil이 아닌 경우에, `unwrappedName`에 넣는다.
이 때 전체 식의 값은 `true`가 된다.

if문 블록 안에서, `unwrappedName`은 이제 옵셔널이 아닌 String 타입이 된다.
(물론 한번 옵셔널로 선언한 `name`은 여전히 옵셔널이다.)

만약 `name`이 nil이라면 아무것도 하지 않고, 식의 값이 `false`가 된다.
`else` 문이 실행된다.

#### 2) `guard let`

`guard let`도 `if let` 못지 않게 자주 쓰는 방법이다.

`guard let`으로 옵셔널 바인딩을 하면, guard 조건을 만족시키지 못하는 경우에 함수 실행을 종료시킨다.

guard의 결과가 false인 경우에는 return, break 등 현재 실행 흐름을 바꾸는 명령어를 넣어줘야 한다.

``` swift
func printName(_ name: String?) {
  guard let unwrappedName = name else {
      print("Hello, anonymous!")
      return
  }
  print("Hello, \(unwrappedName)!")
}
```

**if let이 성공적인 경우의 조건문**이라면,
**guard let은 실패하는 경우의 조건문**을 코딩해주는 것이라고 할 수 있다.

guard let이 편리한 점은, **guard 블록이 끝나도 언래핑된 값을 사용할 수 있다는 점**이다.
(if let의 경우에는 if문 안에서만 값을 사용할 수 있었다.)

언래핑 이후의 코드가 긴 경우,
guard let을 쓰는 것이 인덴팅을 줄이고 좀 더 깔끔한 코드를 만든다.

------------------------------------------------------------------------

**옵셔널 바인딩 + 조건문**
옵셔널 바인딩을 하고나서 다른 조건문을 넣어주는 것도 가능하다.
옵셔널 바인딩과 다른 조건문이 모두 `true`일 때만 실행된다.

``` swift
if let unwrappedName = name, unwrappedName == "Eddy" {
    print("Hello, Eddy!")
}
```

------------------------------------------------------------------------

#### 3) while let

while 반복문과 let을 같이 쓸 수도 있다.

이 경우도 마찬가지로 값이 nil이 아니라면 주어진 변수명에 값을 대입하고,
while 문 안의 코드를 반복 실행한다.

``` swift
var currentNode: ListNode? = list
while let thisNode = currentNode
{
    currentNode = thisNode.next
}
```

if let이나 guard let에 비해 자주 쓰이지는 않는다.

### 2. nil 병합 연산자 (nil coalescing operator)

겉보기에 이름이 되게 어려운데, 별거 아니다.

옵셔널 뒤에 물음표 2개를 연속으로 사용한다.
그 뒤에 만약 옵셔널이 nil일 경우 대체할 수 있는 값을 지정한다.

``` swift
let name: String? = "Eddy Song"
print(name ?? "No name")
```

`name ?? "No name"`은

`name`이 `nil`이 아니면,
`name`을 언래핑한 값이 된다.

`name`이 `nil`이면,
`??` 뒤에 지정한 `"No name"`이 된다.

### 3. 옵셔널 체이닝 (Optional chaining)

옵셔널 값 안에 들어있는 프로퍼티 가져오거나, 메서드를 실행할 때 옵셔널 체이닝을 쓴다.

**여러 뎁스를 가지고 있는 값을 한번에 Optional 체크해서 가져올 수 있다**는 장점이 있다.

예를 들어, 부모 클래스 'Parent'와 자식 클래스 'Child'가 있다고 해보자.

``` swift
class Parent { var child: Child? }
class Child { var age: Int? }
```

``` swift
let john: Parent? = Parent(child: Child(age: 10))
```

이 때 child의 age 값을 가져오고 싶다면, 물음표(?)와 닷(dot)을 연속으로 써준다.

``` swift
let childAge = john?.child?.age
```

`?.`은 `?.` 앞에 있는 값이 nil인지 체크하고, nil이면 뒤를 보지 않고 nil을 반환한다.
앞에 있는 값이 nil이 아니라면, 다음 값을 체크한다.

왼쪽에서 오른쪽으로 nil을 체크해나가고, nil이 있으면 멈춘다.

다시 말하면, **`?` 뒤에 있는 것들은 `?` 앞에 있는 것들이 `nil`이 아니어야만 실행이 된다.**

여기서 **childAge는 무슨 타입이 될까?**
Parent와 Child가 nil이 아니라고 한다면, age까지 실행이 되었을 것이다.

옵셔널 체이닝의 마지막에는 ?를 붙일 수 없다.

하지만 age도 옵셔널 타입인데, 맨 마지막에는 ? 가 붙지 않았으므로
childAge는 여전히 옵셔널 타입이 된다.

------------------------------------------------------------------------

**옵셔널의 옵셔널, `Optional<Optional<T>>`...?**
옵셔널은 어떤 타입에 대해서도 만들 수 있으므로, 옵셔널의 옵셔널도 가능하다. (물론 그 이상의 중첩도 가능)
`Int??`나 `String??` 같은 방식으로 표시된다.

흔히 Dictionary에서 값을 가져올 때 자주 보게 된다.

Dictionary 타입을 \[String: Int\]로 선언한다 해도,
key 값에 대한 value 값을 요청하면, 돌아오는 결과값은 자동적으로 옵셔널 타입 `Int?`가 된다.
입력한 key 값에 대한 value 값의 검색은 실패할 가능성이 있기 때문이다. 'nil'일 수도 있다.
이런 경우에는 한번 언래핑을 하고 써야 한다.

Dictionary 타입 자체에 \[String: Int?\]처럼 옵셔널을 선언해주는 경우가 종종 있다.
이 경우 돌아오는 value 값은 `Int??`가 된다.

복잡해보이지만 별로 쫄 건 없다.
그냥 언래핑을 2번 해주고 사용하면 된다.

------------------------------------------------------------------------

### 4. 옵셔널 패턴 (Optional Pattern)

Swift에서 enum 타입은 패턴 매칭이라는 기능을 사용할 수 있다.

`if case - let` 을 사용하면,
enum 타입이 특정 값(case)에 해당 할 때,
associated value를 정해진 변수명에 대입할 수 있다.

음... 근데 뭔가 친숙하게 들리지 않는가?

옵셔널도 enum의 일종이기 때문에, 패턴 매칭으로 옵셔널 바인딩과 거의 똑같은 일을 할 수 있다.

``` swift
let someOptional: Int? = 42

if case .some(let x) = someOptional {
    print(x)
}
```

또는 똑같은 코드를 이렇게 쓸 수도 있다.

``` swift
let someOptional: Int? = 42

if case let x? = someOptional {
    print(x)
}
```

이걸 옵셔널 패턴이라고 한다.

근데 옵셔널 바인딩과 똑같아 보인다. 왜 굳이 옵셔널 패턴을 쓰는 걸까?

Swift 공식 문서에 보면, 이 둘의 차이는 반복문을 돌릴 때 나타난다고 한다.

``` swift
let capitals = ["Paris", "Rome", nil, "Madrid"]
for capital in capitals {
    guard let capital = capital else { return }
    print(capital)
}
```

옵셔널을 담은 컬렉션 타입에 대해서 for in 반복문을 돌린다.

이럴 때는 nil 값이라도 반복문이 모두 실행이 되고,
반복문 안에 옵셔널 바인딩을 해줘야 한다.

``` swift
let capitals = ["Paris", "Rome", nil, "Madrid"]
for case let capital? in capitals {
    print(capital)
}
// Paris
// Rome
// Madrid
```

하지만 case - let을 사용하면, nil인 경우 아예 반복문이 실행되지 않는다.
따라서 for 문 안에 따로 언래핑을 해줄 필요 없이, 값이 있는 요소들만 출력된다.

## 요약 정리

- 안전하지 않은 언래핑 방법 2가지
  - 강제 언래핑(Force Unwrapping),
  - 암시적 언래핑 (Implicitly unwrapped optionals)이 있다.
  - nil이 아닌 게 100% 확실할 때가 아니면 쓰지 말자.
- 안전한 언래핑 방법 4가지
  - 옵셔널 바인딩 (Optional Binding)은 조건문 형태로 nil을 체크하고 아닐 경우 값을 변수에 담을 수 있다.
  - nil 병합 연산자 (nil coalescing operator)는 nil일 때 대체할 값을 지정할 수 있다.
  - 옵셔널 체이닝 (Optional chaining)은 프로퍼티나 메서드 등 여러 뎁스를 가지는 값의 nil을 연속적으로 체크할 수 있다.
  - 옵셔널 패턴 (Optional Pattern)은 반복문을 쓸 때 더 깔끔하게 nil을 필터링할 수 있다.

## 관련 글

👈 [안전한 Swift의 비결, 옵셔널(Optional)](https://velog.io/@eddy_song/swift-optional)
👈 [옵셔널(Optional)은 어떻게 만들었을까](https://velog.io/@eddy_song/optional-under-the-hood)
