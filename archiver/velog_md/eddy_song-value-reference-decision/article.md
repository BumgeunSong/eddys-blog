---
title: 값이냐 참조냐, 그것이 문제로다
published_date: 2022-04-24 13:01
tags: swift
meta_description: 값 타입(Value type)과 참조 타입(Reference type)을 깊이 들여다보고, 나의 기준을 세워보자.
meta_image: https://velog.velcdn.com/images/eddy_song/post/b6693815-106a-40ef-aed0-61ca7f3f63c4/image.png
lang: ko
---

# 값이냐 참조냐, 그것이 문제로다

*by eddy_song*

# 값(Value)이냐 참조(Reference)냐

데이터 타입은 프로그램을 구성하는 기본 재료다. 소프트웨어가 건물이라고 치면 벽돌, 시멘트, 유리 같은 재료라고 해야할까?

집을 짓는 사람이라면 벽돌과 시멘트를 잘 알아야 하듯이 프로그래머라면 누구나 데이터 타입의 특성을 잘 알아야 한다.

오늘은 데이터 타입의 중요한 특성인 값과 참조의 차이를 얘기해보려고 한다. 많은 언어에서 입문자들이 꼭 배우게 되는 개념이다.

### \[간단 설명\] 값 타입과 참조 타입의 차이

**값 타입(Value type)**은 값 자체를 변수명과 함께 (스택에) 저장한다.

**참조 타입(Reference type)**은 값을 별도의 메모리 공간(힙)에 저장하고, 메모리의 주소를 변수명과 함께 (스택에) 저장한다.

우리가 쓰는 매일 쓰는 컴퓨터로 비유해서 말하자면, '파일로 저장'과 '링크로 저장'의 차이랄까?

예를 들어, 누군가 당신한테 이 글을 카톡으로 보내주었다.

**txt 파일로 보낸다면, 그건 값으로 저장해서 보낸 것이다.** txt 파일 자체를 복사해서 보낸 거니까.

**웹 링크로 보낸다면, 그건 참조로 저장해서 보낸 것이다.** 별도의 저장소에 데이터를 저장한 후 거기에 접근할 수 있는 주소를 보낸 거니까.

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-value-reference-decision/assets/8c203160f8b1b64497d78ba735f8b802b8ef8eac.png)
(출처: FIPE)

이 차이 때문에 참조 타입 데이터의 경우는 부수효과(Side effect)가 생기게 된다. 웹 링크로 여러 사람한테 파일을 보내줬는데 누군가 그걸 수정했다면? 그러면 다른 사람이 받은 파일에도 영향이 간다.

# Swift ♥️ Value

특히! Swift에서는 값 타입과 참조 타입이 더욱더 중요한 주제다.

Swift 값 타입은 다른 언어에 비해 **훨씬 더 기능이 강력**하기 때문이다.

다른 프로그래밍 언어에서 Value type은 대부분 숫자, 문자열, Boolean 등 간단한 값을 나타낼 때 쓴다. 메서드를 담은 클래스 등 복합적인 데이터는 대부분 참조 타입을 사용한다.

(예를 들면, Javascript의 값 타입은 Number, String, Boolean, Null, Undefined 같은 단순한 타입밖에 없다. '기본형(Primitive)'이라고 부른다.)

Swift에서는 `struct` 로 값 타입을 만든다. 하지만 `struct`는 숫자, 문자열 같은 간단한 데이터만 나타내지 않는다. 프로퍼티, 메서드를 가질 수 있다. 생성자, 프로토콜을 활용해 고급진 추상화와 다형성도 활용할 수 있다. 사실상 Struct로 모든 걸 할 수 있다.

Swift는 '값 타입을 더 많이 활용해라'라는 의도가 팍팍 들어가 있는 언어다. Swift의 기본 타입은 전부 다 값 타입(Function/Closure 제외)이라는 점이 그걸 잘 보여준다.

그렇기 때문에 새로운 객체를 설계하는 상황에 더욱더 고민이 되는 것이다. 이걸 `struct`로 해서 값 타입으로 만들까? 아니면 `class`로 해서 참조 타입으로 만들까?

# 깊게 들어가기

이 질문은 단순 명료한 규칙으로 답이 갈리지 않는다. 그래서 '상황에 따라 적절히 쓰라'는 맞지만 도움 안 되는 조언들이 많다.

실제로 Swift 프로그래밍을 하다보면, 애매한 중간 지점을 만나게 된다. Class를 써야할 것 같은데 Struct로도 가능하다고 한다. 어떻게 적용해보면 또 다른 맥락에서는 예상치 못한 결과가 나오고.

struct와 class의 조합도 자주 쓰인다. 찾아보면 참조 타입인데 불변성을 가지기도 하고, 값 타입인데 Heap을 사용하기도 한다?

이제 머리가 아파지기 시작한다.

struct와 class에 대해서 [간단히 정리](https://velog.io/@eddy_song/Swift-Value-Reference)한 적이 있었다.

하지만 실제로 프로그래밍을 하면서 확신을 가지고 의사결정을 하려면, 나 스스로의 경험을 되돌아보면서 좀 더 깊게 파보고 기준을 세워야겠다는 생각이 들었다.

# 시멘틱과 메모리

짚고넘어가야할 중요한 점이 있다. 값 타입과 참조 타입을 볼 때 시멘틱(Semantic)과 메모리 할당(Memory Allocation)을 구분해야 한다.

**밸류 시멘틱 = 불변성이 있는가**

시멘틱은 쉽게 말해 '불변성 or 부수효과'의 관점이다. 할당했을 때 복사가 일어나서 부수 효과가 일어나지 않으면 밸류 시멘틱(Value semantic), 아니라면 레퍼런스 시멘틱(Reference semantic)이라고 한다.

**메모리 할당 = 어디에 저장되는가**

메모리 할당은 인스턴스가 어떤 메모리 영역에 저장되는가의 관점이다.

우리가 프로그래밍한 프로그램이 실제로 실행되면, 운영체제에서 메모리를 할당받아 프로세스가 된다. 이때 프로세스는 메모리를 4개의 영역으로 나눠서 사용한다.

Text와 Global은 컴파일된 코드와 전역 변수/데이터가 저장되는 곳이다. 이 두 영역은 어차피 프로세스를 실행하는 내내 사라지지 않고, 새로 추가되지도 않는 데이터다. 다시 말해 할당/해제라는 주기가 없다. 그냥 고정된 메모리 공간을 배정해준다.

Stack과 Heap은 할당/해제 주기가 있다. 이 둘은 각각 장단점이 있다.

**Stack의 장단점**

Stack은 Push, Pop을 통해 메모리를 할당/해제한다. 선형적인 데이터 구조다. 단순하고 효율적이다.

하지만 컴파일 타임에 스택에 필요한 메모리 크기를 미리 알 수 있어야 한다. 하나의 스택이 올라갔을 때 그 크기를 확정할 수 있어야, 다음 스택이 생길 때 할당할 메모리를 알 수 있다.

또 스택이 끝나면 해제되어 버린다. 데이터를 스택에 할당하면 다른 객체에서 데이터에 접근하기가 어렵다.

**Heap의 장단점**

Heap은 임의의 메모리 주소에 메모리를 할당/해제한다. 메모리 할당을 할 때 순차적인 탐색이 필요하다. 더 이상 사용하지 않는 데이터를 탐지하기 위해 참조 카운팅(Reference counting)을 해야 한다. Stack보다 할당/해제에 드는 오버헤드가 크다.

다만 Heap은 런타임에 메모리 할당 크기가 변할 수 있고, 여러 객체나 스코프에서 참조값을 통해 데이터에 접근이 가능하다.

우리는 주로 값 타입은 Stack을 쓰고, 참조 타입은 Heap을 쓴다고 배운다. 그렇지 않은 경우도 있다. 즉, 시멘틱의 관점에서는 '불변성'을 가지면서도, 실제 메모리는 힙을 사용할 수도 있다는 뜻이다.

# 불변성(Value semantic) + 힙 할당(Heap Allocation)

굳이 앞에서 시멘틱과 할당의 차이를 설명한 이유는 이 얘기를 하고 싶어서였다. Swift에는 불변성을 가지면서도 실제 구현에서는 Heap을 사용하는 경우가 꽤 있다.

## 1. Swift Collection type

Array, String과 같은 Collection type은 데이터를 Heap에 저장한다.

이렇게 해서 좋은 점은 2가지다.

미리 들어갈 원소의 양 (Capacity)를 확정해주지 않아도, 런 타임 시점에 유연하게 변할 수 있다. Stack을 쓴다면, 이미 할당해준 크기 이상으로 새로운 원소를 추가해줄 수는 없었을 것이다. 하지만 Heap을 사용하기 때문에 사전에 Array의 크기를 결정하지 않아도 런타임에 원소를 추가해주면 알아서 메모리 할당 공간을 늘어난다.

**Copy-on-write.** Collection 안에는 많은 양의 데이터가 들어갈 수 있는데, 이 데이터를 매번 복사하지 않아도 된다. A Array를 B Array로 복사할 때, A Array는 데이터가 담긴 메모리 주소값을 공유한다. 모든 원소를 복사하지 않는다.

하지만 Heap을 사용하더라도 Swift의 모든 Collection 타입은 불변성을 가진다. 왜냐하면 참조를 통해 데이터를 변경하는 작업이 있을 때는. 자동으로 데이터를 복사해서 변경하기 때문이다. 원본 데이터는 변하지 않는다.

**값 타입의 불변성과 참조 타입의 효율성을 동시에** 가져갈 수 있다.

## 2. struct 안의 class

Swift 기본 타입인 Collection 외에도, struct로 커스텀 타입을 만들었지만, 인스턴스 변수가 class로 만든 참조 타입인 경우가 있다.

즉, 해당 타입의 **인스턴스 자체는 Stack에 할당되지만, 내부의 프로퍼티는 Heap을 사용**한다.

이 때 잘 구분해줘야 하는 건, 내부 프로퍼티는 다른 참조에 의해서 부수효과가 발생할 수 있다는 점이다. 인스턴스가 let으로 선언한 struct하면 불변성을 가질 수 있다고 생각한다. 하지만 참조 타입 프로퍼티의 경우는 그것과 상관없이 값이 바뀔 수 있다.

즉, 완벽하게 불변성이 보장되지 않는다.

## 3. class/closure 안의 struct

반대 경우다. 참조 타입이 값 타입을 프로퍼티로 가진다. 이 경우 프로퍼티인 값 타입은 Heap에 저장된다.

프로퍼티에 담긴 데이터는 상위 타입이 살아있는 동안에는 계속 메모리에 존재해야 하는데, 상위 타입이 참조 타입이니까 당연히 스택이 끝나고 데이터가 게속 살아있어야 한다.

특히 closure를 쓸 때 많이 일어나는 상황이다. closure는 참조 타입이다. heap에 저장된다. closure는 내부에서 참조하는 변수를 '캡처'한다. 이 때 캡처하는 변수가 값 타입이라면 해당 값 타입은 복사가 되어서 closure 안, 그러니까 heap에 할당이 된다.

**캡쳐된 변수는 여전히 불변성을 가진다.** 즉 나중에 클로저에서 이 값을 변화시켜도, 캡처 이전의 변수에는 영향을 주지 않는다. **불변성(Value semantic)은 계속 가지고 있지만, 데이터의 저장은 Heap을 사용한다**.

## 4. Protocol type (existential type)

Swift에서는 프로토콜 자체를 타입으로 사용할 수 있다. (어려운 말로 existential type이라고 한다.)

프로토콜은 추상 타입이기 때문에 실제 인스턴스는 값 타입일 수도 있고, 참조 타입일 수도 있다. 런타임에 결정된다. 그렇다면 프로토콜 타입 자체는 값 타입인가, 참조 타입일까?

시멘틱은 내부의 구체 인스턴스에 따라 다르다. 안의 구체 인스턴스가 struct인 경우에는 불변성(Value semantic)을 유지하고, class라면 부수 효과가 생긴다.

``` swift
protocol MyCollection {
    var value: [Int] { get set }
}

struct MyArrayStruct: MyCollection {
    var value: [Int]

    init(_ value: [Int]) {
        self.value = value
    }
}

let myCollection: MyCollection = MyArrayStruct([1,2,3])
var myCollectionB = myCollection

myCollectionB.value[0] = 4

print(myCollection.value) // [1, 2, 3]
print(myCollectionB.value) // [4, 2, 3]
```

``` swift
protocol MyCollection {
    var value: [Int] { get set }
}

class MyArrayClass: MyCollection {
    var value: [Int]

    init(_ value: [Int]) {
        self.value = value
    }
}

let myCollection: MyCollection = MyArrayClass([1,2,3])
var myCollectionB = myCollection

myCollectionB.value[0] = 4

print(myCollection.value) // [4, 2, 3]
print(myCollectionB.value) // [4, 2, 3]
```

하지만 구체 인스턴스가 무엇이냐 따라 인스턴스의 크기는 런타임에 달라질 수가 있다.

MyCollection 프로토콜 타입 안에는 MyCollection을 따르기만 한다면, 매우 사이즈가 큰 struct가 들어올 수도 있고, 위에서 본 것처럼 간단한 struct가 들어올 수도 있다.

따라서 **프로토콜 타입은 구체 인스턴스를 저장할 때 Heap을 사용**하게 된다.

조금 더 정확히 말하면 값 타입인 Existential Container를 만든다. 그 안에 구체 타입 인스턴스에 대한 참조를 저장한다. Existential Container 안에는 프로토콜 타입이 다형성을 발휘하기 위한 몇 가지 요소들이 더 저장된다.

이 메커니즘을 설명하려면 별도의 글이 필요할 거 같다. 'Protocol type도 힙을 쓰는구나' 정도만 기억하자.

## 참조 타입 + 스택 할당

이 경우에는 내가 프로그래밍에서 직접 경험을 해보진 못했다. 하지만 Swift 컴파일러 수준에서 최적화를 하기 위해 참조 타입이라 하더라도 스택을 쓰는 경우가 있다고 한다.

참조 타입의 사이즈가 고정되어있거나, 컴파일러가 코드를 보고 생성 주기를 미리 예측할 수 있을 때. 참조 타입 데이터 저장을 스택에 한다고 한다.

🔗 [스위프트 타입별 메모리 분석 실험](https://medium.com/@jungkim/%EC%8A%A4%EC%9C%84%ED%94%84%ED%8A%B8-%ED%83%80%EC%9E%85%EB%B3%84-%EB%A9%94%EB%AA%A8%EB%A6%AC-%EB%B6%84%EC%84%9D-%EC%8B%A4%ED%97%98-4d89e1436fee)

# 그래서... 언제 struct를 쓰고, 언제 class를 써야하는데?

여기까지 왔으니 이제 본론을 꺼낼 때가 되었다.

앞서 말했듯이 보편적인 원칙은 없기 때문에, 각자 프로그래밍을 하면서 기준을 세워가는 과정인 거 같다.

마치 경조사에 많이 참석해보면서 축의금 수준을 적절히 배워가듯이... (음?)

내 경우에는 실제로 코딩을 해보면서 다음과 같은 기준을 세웠다.

> 1.  최대한 struct를 쓴다.
> 2.  Cocoa 프레임워크의 타입 계층, obj-c 런타임이 필요할 때는 class를 쓴다.
> 3.  고유성을 가진 데이터의 변경을 공유해야할 때는, class 안에 struct를 쓴다. (ex. Observer 패턴 구현)
> 4.  많은 양의 복사가 많이 일어나야 한다면, struct 안에 class를 쓴다.

## 최대한 Struct를 쓴다.

Swift가 값 타입을 괜히 사랑하는 게 아니다. 값 타입은 '불변성'이라는 엄청난 장점이 있다. 이 불변성은 프로그래머들이 골치 아파하는 문제를 미리 차단해준다.

**예측 가능성**
값 타입은 부수 효과가 없다. 관심사의 분리가 일어난다. 외부 코드를 다 이해하지 못해도, 특정 부분의 코드만 보고 결과를 예측할 수 있다.

**쓰레드 안전성**
멀티 스레드 환경에서 공유 데이터는 두통을 일으킨다. 동시에 접근하지 않도록 신경 써줘야 하기 때문이다. 하지만 값 타입은 그럴 필요가 없다. 멀티 스레드 환경에서 안전하고 간단하게 쓸 수 있다.

**테스트의 편리함**
참조 타입을 테스트하려면 외부의 영향을 제어하고 원하는 상태를 만들기 위해서 신경써줘야할 게 많다. 하지만 값 타입은 그저 값일 뿐이고 복사되기 때문에 환경을 고립시키고 테스트하기가 훨씬 쉽다.

🔗 [Encapsulating Domain Data, Logic and Business Rules With Value Types in Swift](https://khawerkhaliq.com/blog/swift-domain-logic-business-rules-value-types/)

이런 장점 뿐 아니라, 스택 사용 덕분에 할당/해제의 성능도 훨씬 효율적이다. 이러니 struct는 일단 기본으로 깔고 가는게 좋겠다는 결론을 내렸다.

상속을 쓸 수 없지 않냐고? Swift에서는 상속이 class를 쓰는 이유가 될 수 없다. 우리가 class 상속이 필요한 이유는 결국 다형성을 활용하기 위해서다. 하지만 swift에서는 프로토콜과 값 타입의 조합으로도 얼마든지 다형성을 만들어낼 수 있다.

심지어 프로토콜은 상속 메커니즘으로 할 수 있는 것을 다 할 수 있을 뿐만 아니라, extension과 generic을 사용한 더 고급진 기능까지 쓸 수 있기 때문에 대부분은 프로토콜을 쓰는 게 합리적이다. (그래서 swift가 Protocol-oriented라고 불린다.)

## Cocoa 프레임워크 계층이나 obj-c 런타임을 사용하는 경우, class를 쓴다.

하지만... swift가 없던 시절에 만들어진 iOS 프레임워크와 obj-c 런타임을 써야한다면 여기에는 방법이 없다. 이미 class로 만들어진 걸 어떻게 하겠는가.

UIKit을 서브클래싱한다거나, KVO 같은 메커니즘을 사용하고 싶다면 별수 없이 class를 써야 한다.

## 고유성을 가진 데이터의 변경을 공유해야할 때는, class 안에 struct를 쓴다.

이 부분이 내가 프로그래밍을 직접 하면서 가장 많이 부딪혔던 문제였다.

일단 struct로 시작해서 타입을 만들기 시작한다. 하지만 다른 객체가 특정 객체의 값을 관찰하고 공유받아야하는 경우가 많이 있다. 이 경우에는 struct가 뭔가 삐걱거리기 시작한다.

### 공유할 데이터가 struct일 때의 문제점: Closure를 통한 Observer pattern

가장 흔하게 쓰이는 예시가 바로 observer pattern이다. observer pattern을 직접 closure로 구현하는 경우에, 다음과 같은 코드를 짜게 된다.

``` swift
struct Observable <T> {
    typealias Listener = (T) -> Void
    var listener: Listener?

    var value: T {
        didSet {
            listener?(value)
        }
    }

    init(_ value: T) {
        self.value = value
    }

    mutating func bind(listener: Listener?) {
        self.listener = listener
    }
}
```

여기서 struct로 `Observable`을 구현하고 있다. 프로퍼티를 관찰하고 싶은 객체가 listener를 등록(bind)한다. 그 다음 Observable이 바뀔 때마다 value 값이 바뀌면 value를 넘겨주면 되지 않을까?

그런데 문제는 이 Observable를 변경할 때, '재할당'이 일어난다는 점이다. 간단히 보면 `mutating` 를 달았으니까 값이 변경되고, 그 변경이 잘 전파될 거 같다.

하지만 사실 이 mutating이 일어날 때, 인스턴스가 변하는 게 아니라, (값 타입은 변하지 않는다!) 새로운 인스턴스를 자기 자신(`self`)에게 할당하는 식으로 작동한다.

이 Observable이 변경되거나 전달될 때마다 복사와 재할당이 일어난다는 뜻이다. 우리가 원하는 것처럼 Observable 변수는 일관된 상태를 유지하는게 아니라 다 각각 따로 놀게 된다. Observer들은 일관성없는 값을 계속 전달받게 될 것이다.

### 공유할 데이터가 struct일 때의 문제점: Notification Center

두번째 예시는 notification center다.

공유할 데이터를 갖고 있는 Publisher를 `struct`로 구현했다. NotificationCenter를 사용해 observer로 등록하기 위해서 subscriber는 `class`로 구현했다.

`publisher.update()`를 해준다면, 자신의 값을 notification center에 포스팅하고, Subscriber는 그 알림을 받아 `"Got update!"`를 출력하게 될 것이다.

``` swift
struct Publisher {
    var value: Int

    func update() {
        NotificationCenter.default.post(name: Notification.Name("Update"), object: self)
    }
}

class Subscriber {
    var publisher = Publisher(value: 5)

    func listen() {
        NotificationCenter.default.addObserver(self, selector: #selector(getUpdate(_:)), name: Notification.Name("Update"), object: publisher)
    }

    @objc func getUpdate(_ notification: Notification) {
        print("Got update!")
    }
}
```

하지만 실제로 그 동작을 구현해보면 아무 일도 일어나지 않는다. 왜일까?

여기서 Subscriber는 `publisher`에게서 오는 이벤트를 관찰하고 있다. 하지만 publisher는 이벤트를 포스팅할 때 자기 자신(self)를 파라미터로 넘긴다. 파라미터로 넘긴다? 할당한다? 새로운 값을... 복사한다?

그렇다. Subscriber는 당연히 자기가 프로퍼티로 가진 `publisher`가 알림을 보내오리라 생각했지만, 실제 알림을 보낸 객체로 등록된 것은 복사된 또다른 `publisher` 다. 따라서 우리가 아무런 알림도 받을 수 없었다.

### 관찰하려면 '식별'할 수 있어야 한다.

이런 경우들을 겪고 나서, 곰곰히 생각해보았다. struct는 왜 데이터 공유가 이렇게 까다로운 것일까?

**우리가 '무언가'를 관찰하고 변경이 있을 때 그 값을 알게 되려면 (Observer pattern) 우리가 그 '무언가'를 식별할 수 있어야 한다.** 다시 말해, 그 '무언가'가 변경되는 값과 별개로 어떠한 **'고유성'**을 가져야한다.

생각해보면 단순히 숫자 4를 관찰할래. 라고 할 수는 없는 것이다. 우리가 원하는 어떤 정보는 고유하고, 그 정보 안에 담긴 값이 변하는 것을 관찰하는 것에 가깝다.

우리가 관찰해야할 데이터가 순수한 값 타입이라면, 문제가 생긴다. 값 타입에는 고유성이 없다. 값이 변경되었을 때는 그냥 새로운 값을 가진 인스턴스로 교체가 되어버릴 뿐이다.

관찰자 입장에서는 내가 관찰해야할 값이 무엇인지 식별할 수가 없는 것이다.

### 고유성이 필요한 값에는 class를 쓰자

따라서 Observer 패턴, 그러니까 어떤 데이터가 그 변경이 공유되고 식별될 수 있어야 하는 상황에서는 class를 쓰는 게 적합하다고 결론을 내렸다.

하지만 그렇다고 상위 타입을 다 class로 바꿀 필요는 없다. 식별가능해야하는 데이터만 고유성을 띄면 된다. 그 외의 프로퍼티나 비즈니스 로직까지 class에 담아서 부수효과의 범위를 키울 필요는 없다.

*공유해야 하는 데이터를 값 타입으로 유지하되, class로 감싸주자.* 이렇게 되면 해당 데이터의 고유성을 유지하면서 다른 객체가 관찰할 수 있도록 하되, 우리가 의도한 범위 이상의 부수효과를 만들지 않는 효과가 있다.

예를 들면 다음과 같은 wrapper 타입을 만들 수 있겠다.

``` swift
class Reference<Value> {
    var value: Value

    init(value: Value) {
        self.value = value
    }
}

let sharedData = Reference(value: data)
```

## 복사가 많이 일어나서 비효율적인 경우, struct 안에 class를 쓴다.

값 타입인데 안의 데이터가 굉장히 많거나, 복사가 많이 일어나는 데이터의 경우는 참조 타입의 장점을 활용한다. 복사를 최소화해서 성능을 최적화하는 것이다.

이 때는 struct 안에 참조 타입으로 별도의 저장소를 만들어준다.

참조 타입 안에 들어간 데이터는 struct가 여러번 복사되고 할당되어도 참조만 늘어나기 때문에 효율적으로 사용할 수 있다.

하지만 이 경우에는 순수한 값 타입의 불변성을 잃어버리기 때문에, 변경이 일어날 경우에는 복사하는 메커니즘을 구현해주는 게 좋다. (어디서 많이 들어본 Copy-on-write)

다만 여기서 주의할 점. 성능 측면에서 값 타입이 프로퍼티로 참조 타입을 2개 이상 가지고 있는 경우는 바람직하지 않다.

2개 이상의 참조 타입을 포함한 값 타입은 오히려 참조 타입보다도 메모리 측면에서 성능이 감소한다.

그 이유는 Struct가 계속해서 복사될 때마다, 참조 카운팅도 늘어나기 때문이다. 참조 카운팅이 계속 늘어나면 오버헤드도 커진다.

예를 들어 다음과 같이 프로퍼티로 클래스를 왕창 가지고 있는 2개의 타입이 있다고 해보자.

``` swift
struct HugeDynamicStruct {
    var emptyClass = EmptyClass()
    var emptyClass2 = EmptyClass()
    var emptyClass3 = EmptyClass()
    var emptyClass4 = EmptyClass()
    var emptyClass5 = EmptyClass()
    var emptyClass6 = EmptyClass()
    var emptyClass7 = EmptyClass()
    var emptyClass8 = EmptyClass()
    var emptyClass9 = EmptyClass()
    var emptyClass10 = EmptyClass()
}

class HugeClass {
    var emptyClass = EmptyClass()
    var emptyClass2 = EmptyClass()
    var emptyClass3 = EmptyClass()
    var emptyClass4 = EmptyClass()
    var emptyClass5 = EmptyClass()
    var emptyClass6 = EmptyClass()
    var emptyClass7 = EmptyClass()
    var emptyClass8 = EmptyClass()
    var emptyClass9 = EmptyClass()
    var emptyClass10 = EmptyClass()
}
```

(출처: <https://swiftrocks.com/memory-management-and-performance-of-value-types>)

이 경우 struct는 클래스보다도 성능이 훨씬 더 느려진다. struct는 할당 시 마다 참조가 복사되는 반면, class는 복사가 일어나지 않기 때문에 프로퍼티에 대한 참조 숫자는 일정하다. 이 오버헤드는 struct가 가진 프로퍼티 숫자에 따라서 기하급수적으로 늘어난다.

``` swift
func createABunchOfReferencesOfClass() {
    var array = [HugeClass]()
    let object = HugeClass()
    for _ in 0..<10_000_000 {
        array.append(object)
    }
}

func createABunchOfCopiesOfStruct() {
    var array = [HugeDynamicStruct]()
    let object = HugeDynamicStruct()
    for _ in 0..<10_000_000 {
        array.append(object)
    }
}

//Each object contains ten EmptyClasses

createABunchOfReferencesOfClass() // ~1.71 seconds
createABunchOfCopiesOfStruct() // ~5.1 seconds

//Each object now contains TWENTY EmptyClasses

createABunchOfReferencesOfClass() // ~1.75 seconds
createABunchOfCopiesOfStruct() // ~14.5 seconds
```

따라서 struct 안에 참조 타입, 힙을 사용하는 변수를 넣는 것은 가급적 숫자를 줄이면 좋다.

예를 들어, 아래의 타입은 힙을 사용하는 데이터 타입(String)을 2개 가지고 있다.

``` swift
struct Attachment {
    let fileURL: URL
    let uuid: String
    let mimeType: String

    init?(fileURL: URL, uuid: String, mimeType: String) {
        guard mimeType.isMimeTypeelse
        { return nil }

        self.fileURL = fileURL
        self.uuid = uuid
        self.mimeType = mimeType
    }
}
```

출처: [Understanding Swift Performance - WWDC16](https://developer.apple.com/videos/play/wwdc2016/416/)

이 경우 순수한 값 타입으로 프로퍼티를 바꿔주면, 성능에 도움이 된다.

``` swift
struct Attachment {
    let fileURL: URL
    let uuid: UUID
    let mimeType: MimeType

    init?(fileURL: URL, uuid: UUID, mimeType: String) {
        guard let mimeType = MimeType(rawValue: mimeType)
        else { return nil }

        self.fileURL = fileURL
        self.uuid = uuid
        self.mimeType = mimeType
    }
}
```

바꾸기가 어렵다면, 그 때는 아예 class를 쓰는 것도 방법이다.

대량의 데이터를 복사하지 않는 장점보다, 오히려 참조 카운팅에 드는 오버헤드가 더 커질 수도 있다는 점을 고려하자.

## 요약 정리

- '이 타입을 값으로 할거냐, 참조로 할거냐'는 Swift에서 꽤나 중요한 고민거리다.
- Swift는 값 타입이 무척 강력해서 더욱더 고민이 된다.
- 값 타입과 참조 타입을 볼 때 시멘틱(semantic)과 메모리 할당(memory allocation)을 구분해서 봐야 한다.
- 불변성을 가지면서도 힙에 저장되는 경우는 Swift Collection type, struct 안의 class, class/closure 안의 struct, Protocol type 등이 있다.

<!-- -->

- 내가 실제로 객체 설계와 코딩을 경험하면서 세운 기준은 다음과 같다.

1.  최대한 struct를 쓴다.
2.  Cocoa 프레임워크의 타입 계층, obj-c 런타임이 필요할 때는 class를 쓴다.
3.  고유성을 가진 데이터의 변경을 공유해야할 때는, class 안에 struct를 쓴다. (ex. Observer 패턴 구현)
4.  많은 양의 복사가 많이 일어나야 한다면, struct 안에 class를 쓴다.

## 참조 링크

🔗 [Understanding Swift Performance - WWDC16](https://developer.apple.com/videos/play/wwdc2016/416/)
🔗 [Memory Management and Performance of Value Types](https://swiftrocks.com/memory-management-and-performance-of-value-types)
🔗 [Encapsulating Domain Data, Logic and Business Rules With Value Types in Swift](https://khawerkhaliq.com/blog/swift-domain-logic-business-rules-value-types/)
🔗 [Combining value and reference types in Swift](https://www.swiftbysundell.com/articles/combining-value-and-reference-types-in-swift/)
