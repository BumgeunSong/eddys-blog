---
title: Dynamic Dispatch를 알면 코드가 빨라진다
published_date: 2022-03-01 14:01
tags: iOS, object oriented, swift
meta_description: 다용도 드라이버와 일반 드라이버, 어떤 걸 써야할까?
meta_image: https://images.velog.io/images/eddy_song/post/8ffe6c44-0669-4dfb-8792-4a5c9bf1073b/Screen Shot 2022-03-01 at 10.59.51 PM.png
lang: ko
---

# Dynamic Dispatch를 알면 코드가 빨라진다

*by eddy_song*

> Swift의 성능을 높이려면 어떻게 해야할까?

이 질문에 빠지지 않고 나오는 키워드가 있다.
Dynamic Dispatch와 Static Dispatch다.

오늘은 이 **Dispatch**에 대해 정리해보려 한다.

## 메시지와 메서드: 다형성

[객체 지향 프로그래밍의 핵심](https://velog.io/@eddy_song/alan-kay-OOP) 중 하나는 특정한 객체에게 '메시지'를 보내도,
실제 그 메시지를 처리하는 객체, 메서드는 달라질 수 있다는 점이다.

덕분에 우리는 메시지를 보내는 객체의 코드를 전혀 바꾸지 않고도,
실제 동작 (메서드)를 런타임 시점에 바꿀 수 있다.

다시 말해, 같은 인터페이스에 대해서 다른 함수가 실행되도록 만들 수 있다.
코드 설계를 훨씬 유연하게 만들어준다.

이걸 '다형성'이라고 하고, 객체 지향 프로그래밍의 가장 슈퍼 파워 중 하나다.

그런데 아까 말한 내용을 다시 한번 보자.

하나의 '메시지'에 대해서 실행되는 '메서드'가 '그때그때' 다르다.

다른 말로 하면, 컴파일러가 코드를 해석할 때
어떤 인터페이스에 대해 보낸 메시지에 대해 정확히 어떤 메서드를 실행해야 할지 '그때그때' 찾아내야 한다는 말이 된다. ('그때그때'란 해당 코드가 실행되는 런타임 시점이다.)

예를 들어 `Human`이라는 클래스가 있고 안에는 sayHello라는 메서드가 있다.
그리고 `Human`을 상속한 여러 클래스 (`Student`, `Employee`) 등이 있다.

그렇다면 이 코드(메시지)는 어떤 메서드를 실행해야 할까?

``` null
eddy.sayHello()
```

정답은 '그때 그때 다르다'.

코드의 실행 맥락에 따라서 `eddy`라는 인스턴스는
`human`일 수도 있고,
`student`일 수도 있고,
`Employee`일 수도 있다.

그러니 `sayHello()`라는 메시지에 대해
어떤 클래스에 선언된 메서드가 실행될지는 저 코드만 봐서는 알 수가 없다.

## Dynamic Dispatch가 필요한 이유

Dispatch 얘기를 하기로 했는데 갑자기 메시지, 메서드로 시작하는 걸까?
'메시지와 메서드의 분리'를 구현하려면 Dynamic dispatch가 반드시 필요하기 때문이다.

여기서 잠깐 퀴즈,

Dispatch는 무슨 뜻일까?

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-dynamic-dispatch/assets/19f7f46b797a7834c581a5d9e6810576e396c899.png)
(물론 이게 가장 유명한 디스패치지만...;;)

**영어로 Dispatch는 '보내다'** 정도로 해석할 수 있다.
좀 더 정확하게는 (사람을) '파견하다', (물건을) '발송하다' 같은 느낌.

언론에서 dispatch라고 하면 (특파원을) '특파하다'라는 뜻이다.

그래서 디스패치가 디스패치다. ~~(연예인 집 앞으로 특파한다는 뜻)~~

프로그래밍에서의 Dispatch도 비슷한 맥락으로 해석할 수 있다.

어떤 객체가 다른 객체에게 **메시지**를 전송(`ex) Object.method()` )했을 때,
**그때 그때 상황에 맞게** (Dynamic)
그 메시지에 맞는 **메서드를 '보내준다'**(Dispatch)는 뜻이다.

즉, **Dynamic dispatch는 다형성을 구현하기 위한 핵심 기능**이다.
대부분의 객체 지향 언어에서 dynamic dispatch 메커니즘을 갖고 있다.

## Static dispatch

Static dispatch는 쉽게 말해,
Dynamic dispatch가 아닌 메서드 호출을 말한다.

우리가 별도로 다형성을 구현하지 않고,
`.`을 찍어서 프로퍼티, 메서드를 호출하면 Static dispatch다.

하나의 코드에 대해 항상 정해진 함수가 실행된다.

## 유연성이냐 성능이냐, 그것이 문제로다

Swift의 성능을 말할 때 Dynamic dispatch는 자주 등장하는 키워드다.

왜냐하면 Dynamic dispatch는 OOP의 핵심인 다형성을 만들어주지만,
굳이 다형성을 쓸 필요가 없을 때는 성능의 저하를 가져오기 때문이다.

코드를 실행하는 와중에 어떤 함수 호출을 보면 바로 그 함수로 점프하는 게 아니라,
정확히 어떤 함수로 가야할지 알아보고 점프를 해야한다. 성능에서 손해를 보게 된다.

예전에 [다형성을 다용도 드라이버에 비유한 적](https://velog.io/@eddy_song/alan-kay-OOP)이 있다.

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-dynamic-dispatch/assets/9fcb42fcfac546ca0e7d5027f4492d0cc8c1194e.png)

**다용도 드라이버는 일반 드라이버에 비해 훨씬 유연하다.**
드라이버 손잡이에 다양한 드라이버를 끼워서 그때그때 필요한 용도로 쓸 수 있다.

> 하지만 최대한 빨리 나사를 돌려야 한다면?

**당연히 일반 드라이버가 더 낫다.**

다용도 드라이버로 필요한 드라이버 찾아서 손잡이에 끼울 시간에,
일반 드라이버는 그냥 바로 사용하면 되니까.

**Dynamic dispatch와 Static dispatch도 어느 한쪽이 우월한 것은 아니다.**
다용도인 대신 약간 느린 드라이버와 빠르지만 기능은 하나인 드라이버의 차이일 뿐.

**다만 둘의 차이를 알고 상황에 따라서 잘 사용하면 되는 것!**

사실 개발자로서 알아야 하는 더 실제적인 지식은,

우리가 쓰는 코드의 **어느 부분이 Dynamic dispatch가 되고,
어느 부분이 Static dispatch가 되는지** 알아두는 것이다.

## Dynamic dispatch인 경우

Swift 컴파일러는
메시지와 메서드가 다를 가능성이 있으면 Dynamic dispatch를 한고,
그럴 가능성이 없으면 Static dispatch를 한다.

Swift에서 다형성을 구현할 수 있는 방법은 `protocol`, `class` 2가지다.
기본적으로 이 2가지 경우에 Dynamic dispatch를 하게 된다.

### 1. Protocol의 메서드/프로퍼티 사용

protocol을 사용하면 기본적으로 Dynamic dispatch를 실행한다.

Swift는 Protocol을 사용해 타입을 특정한 인터페이스로 묶어준다.
메시지를 보낼 때 해당 Protocol에 대해서 코드를 작성할 수 있다.

``` swift
// 프로토콜 정의
protocol canFly {
    func fly()
}
```

``` swift
// 프로토콜을 따르는 타입 정의
struct Bird(): canFly {
    func fly() { print("Bird is flying!") }
}
struct Dragon(): canFly {
    func fly() { print("Dragon is flying!") }
}
```

``` swift
func makeFly(canFly: canFly) {
    canFly.fly()
}
```

``` swift
func makeFly(Bird()) // "bird is flying!"
func makeFly(Dragon()) // "Dragon is flying!"
```

이렇게 프로토콜을 사용해서 메서드나 프로퍼티를 호출하는 경우,

Swift 컴파일러는 `canFly` 타입이
실제로 `Bird`인지 `Dragon`인지 찾기 위해서 Dynamic dispatch를 사용한다.

### 2. Class의 메서드/프로퍼티 사용

Class를 쓰면 기본적으로 Dynamic dispatch를 실행한다.
하위 클래스가 상속을 받거나 메서드를 오버라이딩했을 가능성이 있기 때문이다.

상위 클래스의 메서드/프로퍼티를 가리키는 건지,
하위 클래스의 메서드/프로퍼티를 가리키는 건지 알아내야 한다.

## Static dispatch인 경우

### 1. Value type (struct, enum)의 메서드/프로퍼티 사용

`struct`, `enum` 으로 선언했을 때는 static dispatch를 실행한다.
value type인 경우 기본적으로 static dispatch다.

왜냐? value type 인스턴스는 protocol, class와 다르게
메시지를 다른 객체에게 위임할 수 없기 때문이다.

즉, 메시지와 메서드가 다를 가능성이 없기 때문에 static dispatch로 처리한다.

### 2. Extension을 사용해 추가한 메서드 사용

Swift는 모든 타입에 Extension을 붙일 수 있다.

하지만 extension으로 새로운 기능을 추가할 수는 있지만,
그 안에서 이미 있는 메서드를 상속(override)를 할 수는 없다.

즉, 메시지-메서드가 다를 수 없다. (다형성을 사용할 수 없다.)

그래서 Protocol/Class에 extension을 붙여서 추가한 메서드는 Static dispatch로 실행한다.

> \[Quiz\] 다음 코드에서 isCute()와 canGetAngry() 중
> Static dispatch로 실행되는 메서드는 무엇일까?

``` swift
protocol Animal {
    func isCute() -> Bool { }
}
extension Animal {
    func canGetAngry() -> Bool { }
}
```

## 예외 상황

위에서 말한 내용을 다시 한번 정리해보자.

> Protocol, Class의 메서드/프로퍼티 사용 -\> Dynamic dispatch
> Struct, Enum, Extension의 메서드/프로퍼티 사용 -\> Static dispatch

이게 기본 원칙이다.

하지만 원칙이 있으면 항상 예외도 있는 법!

우리는 그렇지 않은 예외도 잘 알고 활용해야 한다.

### 1. Class에 Final, Private, Static 키워드를 사용

#### `final`

Swift에서는 class 선언부나, 메서드/프로퍼티 선언부에 final 키워드를 붙일 수 있다.
`final` 키워드를 붙이면 상속/오버라이드를 할 수 없다.

그렇다는 말은?

해당 클래스나 메서드에 대해 메시지를 보낼 때 다형성을 사용할 수 없다.
메시지-메서드가 달라질 가능성이 없는 것이다.

따라서 Class를 쓸 때는 기본적으로 Dynamic dispatch를 실행하지만,

final 키워드가 붙은 클래스의 메서드/프로퍼티일 때는,
컴파일러가 자동으로 Static dispatch를 쓴다.

> 다형성을 활용하지 않을 거라면, final을 써서 성능을 높이자!

#### `Private`

private 키워드가 붙으면, 메서드/프로퍼티는 선언부 내에서만 사용할 수 있다.

따라서 Class 선언하는 블록/파일 내에 오버라이딩이 없다면,
컴파일러가 알아서 final 키워드를 추론해서 붙여준다.

Static dispatch가 되면서 성능이 좋아진다.

#### `Static`

이건 너무 당연한 말이지만, static 키워드를 붙인 프로퍼티/메서드는 아예 인스턴스에서는 사용할 수 없다.

따라서 메시지-메서드가 달라질 가능성이 없고, static dispatch를 쓴다.

static이니까 당연히 static diaptch겠지? 하면 된다.

> 작성중...

### 2. Protocol + Extension을 사용해 구현을 추가

### 3. 전체 모듈 최적화 (Whole Module Optimization)을 사용

### 4. Class에 @objc, dynamic 키워드 사용

## Table dispatch와 Message dispatch

## 요약 정리
