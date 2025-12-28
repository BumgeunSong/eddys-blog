---
title: 창시자 앨런 케이가 말하는, 객체 지향 프로그래밍의 본질
published_date: 2022-01-21 10:26
tags: object oriented
meta_description: 앨런 케이는 '객체 지향 프로그래밍'이라는 네이밍을 잘못 지었다고 인정했다.
meta_image: https://images.velog.io/images/eddy_song/post/d3feb83d-0679-4d37-b49f-b7cb49e0ee1b/Alan_Kay_hero.png
lang: ko
---

# 창시자 앨런 케이가 말하는, 객체 지향 프로그래밍의 본질

*by eddy_song*

> 앨런 케이의 젊은 시절 (출처: Quora)

지금은 1966년.
여기는 미국 유타대학교.

뭔가를 고민하고 있는 대학원생 앨런 케이에게 친구가 다가왔다.

**친구:** 앨런, 뭐하냐?

**앨런:** 말해도 모를 거 같은데? 🤪

**친구:** 허, 인성 보소...🤭 쉽게 설명해봐.

**앨런:** 난 소프트웨어를 구조화하는 방법을 연구하고 있어. 👨‍🏫

**친구:** 소프트웨어를 구조화...한다고? 😳

> *(이 대화는 알려진 사실을 기반으로 상상해본 픽션입니다)*

## 행동을 기준으로 코드를 묶었을 때

**앨런:** 응. 잘 봐봐. 여기 영화 티켓을 예매하는 프로그램이 있어.

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-alan-kay-OOP/assets/75e1f584dab83a4725777defc2c44072a87f32d6.jpg)

``` swift
var customerCash = 20000
var customerTicket = 0

var sellerCash = 0
var sellerTicket = 5
let ticketPrice = 10000

func canAfford() {
    if customerCash >= ticketPrice {
         sellTicket()
    } else {
        refuse()
    }
}

func sellTicket() {
    customerCash -= ticketPrice
    sellerCash += ticketPrice

    customerTicket += 1
    sellerTicket -= 1

    print("즐거운 관람 되세요!")
}

func refuse() {
    print("돈이 부족하시네요.")
    return
}

canAfford()
```

친구: 오... 근데 이거 무슨 언어야? 🤨

앨런: 60년뒤에 나오는 Swift라는 언어인데... 넌 몰라도 돼. 🤚

친구: 😳 ???

앨런: 암튼 여기를 보면 먼저 고객의 돈과 티켓을 설정해주지?
이게 프로그램에 사용되는 '데이터' 부분이야.

``` swift
var customerCash = 20000
var customerTicket = 0

var sellerCash = 0
var sellerTicket = 5
let ticketPrice = 10000
```

**앨런:** 그리고 이 데이터를 가지고 조건문, 반복문 등을 통해 일정한 절차를 수행하는 부분이 있어.
이걸 **'프로시져'**라고 불러.

``` swift
func canAfford() {
    if customerCash >= ticketPrice {
         sellTicket()
    } else {
        refuse()
    }
}

func sellTicket() {
    customerCash -= ticketPrice
    sellerCash += ticketPrice

    customerTicket += 1
    sellerTicket -= 1

    print("즐거운 관람 되세요!")
}

func refuse() {
    print("돈이 부족하시네요.")
    return
}
```

**친구:** 여기있는 `canAfford()`, `sellTicket()`, `refuse()`가 프로시져인 거네?

**앨런:** 그렇지. 행동을 기준으로 소프트웨어를 묶은 거야. sellTicket을 보면 고객의 돈을 줄이고 티켓을 추가해주지?

근데 이 행동을 하나의 함수로 묶어서 이름을 붙여줬어. sellTicket이라고.

이제 우리는 복잡하게 모든 코드를 쓸 필요 없이, sellTicket으로 이 코드를 묶어서 이해할 수 있지.

**친구:** 그건 뭐 설명 안해줘도 쉽네.

'고객의 돈을 빼고, 셀러의 돈을 더하고, 고객의 티켓을 추가하고, 셀러의 티켓을 추가하고, 인사를 한다.'

이건 너무 길고 복잡하잖아. 그러니까 그 행동을 그냥 '티켓을 판다'라는 행동으로 묶어준다는 거네.

**앨런:** 그렇지. 이런 방법을 '프로시져 추상화'라고 불러.
이게 요즘 가장 많이 쓰이는 프로그래밍 방식이야.

**친구:** 그래? 좋은 건가 보구만.

## 행동을 기준으로 묶었을 때의 단점

**앨런:** 아니지, 아니지.
이 방식은 문제가 있어.

코드라는 건 이해하기 쉽고 변경하기도 쉬워야 돼.

이런 식으로 변경가능한 공유 데이터가 있으면, 프로그램이 조금만 복잡해져도
어떤 프로시져가 데이터를 건드렸는지 찾기가 매우 어려워.
다른 프로시져가 그걸 모르고 조작을 하다가 버그를 일으킨다구.

게다가 데이터 구조를 한번 바꾸면,
관련된 모든 코드를 수정해줘야 하지.

**친구:** 흠... 그렇겠네.
여기서 만약 `customerTicket`을 `String`으로
바꿨다고 하면 모든 함수를 수정해야겠어.

**앨런:** 그래. 이렇게 행동을 기준으로 묶으면 코드가 복잡해질수록,
코드를 바꾸기도 어렵고, 버그도 많이 생기게 돼.

**친구:** 그럼 넌 어떻게 할 건데?

## 세포로 이루어진 생물에서 영감을 받다

**앨런:** 그걸 고민 중이야.
근데 최근에 괜찮은 아이디어가 떠올랐거든? 들어봐.

너, 내가 학부 때 전공이 뭔 줄 알아?

**친구:** 전공? 너 공대생 아니었어?

**앨런:** 나 학부 때 생물학 전공이었어.

생물은 탐구해볼수록 정말 신비해. 단순하고 독립적인 세포들이,
물질을 주고받고 협력하면서, 결국에는 복잡한 생물체를 이루게 되어있거든.
죽기도 하고, 대체되기도 하면서 자기 자신보다 훨씬 복잡하고 큰 생명체를 만들지.

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-alan-kay-OOP/assets/4d573b27941a5286b65d3e94080c7fe512ef85f2.jpg)

**친구:** 세포라... 그렇지.

**앨런:** 또 내가 흥미로웠던 게, 아르파넷 프로젝트야.
컴퓨터와 컴퓨터끼리 정보를 주고받는 네트워크를 만드는 프로젝트인데.
거기서 정말 영감을 많이 받았어.

이게 미래에 세상을 바꾸게 될, '인터넷'의 원형이라고...!

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-alan-kay-OOP/assets/bfcb0703897b69f2fb5c5583f2fd5b963cfb6d8f.jpg)

**친구:** 인터넷..?? 또 뭔소리야 그건? 😳

**앨런:** 넌 몰라도 돼.

아무튼, 아르파넷에선 서로 독립된 컴퓨터들이 정해진 약속에 따라서 메시지를 주고받아.
네트워크를 만들지. 그게 모여서 거-대한 시스템이 되는 거야.

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-alan-kay-OOP/assets/74b5b817f1e547fd346d5217d63b9004122a0ac0.png)

**앨런:** 근데 생각해봐.

이게 마치 세포로 구성된 생물체와 비슷한 거 같지 않아?
작은 독립 개체들이 서로 연결되어서 더 커다란 시스템을 만드는 거.

> **소프트웨어도 이렇게 구조화할 순 없을까?**

**친구:** 소프트웨어를 생물체처럼 구성한다고?

**앨런:** 음, 그러니까 이런 식인 거야.

아까 여러 곳에서 접근할 수 있는 데이터가 있으면 코드의 질이 안 좋아진다고 했잖아?

흩어져있는 데이터와 로직을 하나의 그릇에 담아주는 거지.

서로 관련있는 데이터와, 프로시져를 독립된 하나의 개체로 묶어주는 거야.

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-alan-kay-OOP/assets/a1a4a8c686ec7658129ec9e01b4d631f62878f00.png)
*출처: [스파게티코드](https://m.blog.naver.com/atalanta16/220249264429)*

한 개체는 다른 개체가 관리하는 데이터를 건드릴 수 없어.
자기가 내부에 가지고 있는 코드는 다른 개체가 알지도 못하고, 접근할 수도 없지.

대신 이 개체들은 각자 **자기한테 주어진 역할**이 있어.

자기가 갖고 있는 데이터와 관련있는 작업만 직접 해.

연관성이 없는 다른 작업은,
그 작업을 맡고 있는 **다른 객체한테 '메시지'를 보내서 맡기게 되지.**

일종의 분업 구조인거야.

이렇게 하면 변경가능한 데이터를 공유하는 일은 없어지고,
독립된 개체가 서로 메시지를 주고받는 관계만 남아.

## 독립된 개체가 메시지를 통해 소통한다면

**친구:** 오... 신박한데?
이걸 아까 말했던 프로그램에 적용하면 어떻게 되는 거야?

**앨런:** 실제 예시를 볼까? 꼭 이런 방식으로 할 필요는 없지만... 한번 해보자.

먼저, '고객'이라는 하나의 독립 개체를 정의해.

``` swift
class Customer {
    init(cash: Int, ticket: [String: String]? = nil, seller: Seller) {
        self.cash = cash
        self.ticket = ticket
        self.seller = seller
    }

    private var cash: Int
    private var ticket: [String: String]?
    private let seller: Seller

    func askTicket() {
        seller.sellTicket(to: self)
    }

    func checkCashAmount() -> Int {
        return self.cash
    }

    func giveCash(amount: Int) {
        self.cash -= amount
    }

    func receiveTicket(ticket: [String: String]) {
        self.ticket = ticket
    }
}
```

**친구:** 아까는 고객이라는 주체는 없었는데 이번엔 'Customer'를 정의하고,
그 안에 고객과 관련한 데이터와 프로시져가 들어가 있네?

**앨런:** 그렇지.
여전히 프로시져 추상화도 같이 쓰이고 있지만,
데이터와 프로시져가 더 큰 단위로 한번 더 묶여져있는 거지.

그리고 이 부분이 아주 중요해.

`private`이라는 키워드를 써서,
**외부에서는 데이터를 건드릴 수 없게 해놨어.**

프로시져 추상화의 문제였던 공유 데이터를 없애버린 거야.

데이터를 조작할 수 있는 방법은,
Seller가 가진 메서드를 실행하는 방법밖엔 없어.

자, 다시 코드로 돌아가보자.

'Customer'가 있으니까, 다른 쪽에는 티켓을 파는 판매자 'Seller' 가 있을 거야.

``` swift
class Seller {
    init(cash: Int, ticket: [String: String], ticketPrice: Int) {
        self.cash = cash
        self.ticket = ticket
        self.ticketPrice = ticketPrice
    }

    private var cash: Int
    private var ticket: [String: String]
    private let ticketPrice: Int

    func sellTicket(to customer: Customer) {
        if customer.checkCashAmount() >= ticketPrice {
            customer.giveCash(amount: ticketPrice)
            self.cash += ticketPrice

            customer.receiveTicket(ticket: ticket)
            print("즐거운 관람 되세요!")
        } else {
            refuse()
        }
    }

    func refuse() {
        print("돈이 부족하시네요.")
        return
    }
}
```

**친구:** 그럼 여기서 **'메시지'**라는 건 뭐야?

**앨런:** `sellTicket()`의 코드를 잘 봐.
Seller가 `customer.giveCash()`와 `customer.receiveTicket()`을 통해 작업을 요청하지?
이게 바로 메시지를 보내는 부분이야.

Seller가 Customer 안에 있는 데이터를 자기가 직접 조작하지 않고,
Customer한테 돈을 달라, (`customer.giveCash()`)
티켓을 받아라 (`customer.receiveTicket()`)
메시지를 보내는 거지.

**친구:** 그래...? **내 눈에는 그냥 함수 호출 같은데.**

**앨런:** 그렇게 생겼지. 하지만 꼭 특정한 함수를 가리키는 건 아니야.
**메시지를 받은 쪽은 그걸 어떻게 처리할지를 직접 결정할 수 있도록** 만들 거거든.

`customer.giveCash(amount: ticketPrice)`는 무엇(What)을 하라는 메시지를 보냈을 뿐,
실제로 어떻게(How) 하라고 지시하는 건 아니야.

**친구:** 모양은 함수 호출과 비슷한데...

**함수 호출은 항상 같은 행동과 연결되는 반면,
메시지의 경우, 같은 메시지 처리하는 방법이 그때그때 달라질 수 있다는 건가?**

**앨런:** 바로 그렇지. 심지어 메시지를 다른 곳에 위임할 수도 있기 때문에,
'누가' 그걸 처리할지도 바뀔 수 있어.

그래서 함수 호출이 아니라
**'메시지를 통한 소통'**이라고 계속 말하는 거야.

이렇게 하면 Seller가 요청하는 코드를 수정하지 않아도,
실제 Customer 쪽에서의 동작을 바꿀 수 있지.

Seller는 그냥 얼마의 돈만 달라고 요청만 하는 거야.

Customer가 지갑에서 돈을 꺼내주든,
옆에 있는 친구한테 돈을 빌리든,
스마트폰으로 이체를 해주든...
그건 Customer가 알아서 하는 거지.

**친구:** 스...스마트폰? 😵‍💫 너 오늘 좀 이상한 거 같다.

**앨런:** 자, 그럼 이제 이 customer-seller 사이의 협력을 만들어볼까?

``` swift
let spiderManTicket = ["title": "Spider Man"]
let tom = Seller(cash: 0, ticket: spiderManTicket, ticketPrice: 15000)
let eddy = Customer(cash: 20000, ticket: nil, seller: tom)
```

필요한 데이터를 넣어서 `tom`이라는 이름의 Seller와
`eddy`라는 이름의 Customer를 생성해.

``` swift
eddy.askTicket() //  "즐거운 관람 되세요!"
print("한번 더보고 싶어요!")
eddy.askTicket() // "돈이 부족하시네요."
```

**친구:** 호오... 따져보면 아까 코드랑 결국 하는 일은 같지만
다른 방식으로 구조화가 되어있네.

완전히 새로운 방식이잖아.
이거 이름은 뭐라고 붙일 거야?

**앨런:** 흠... 나는 이 독립된 개체를 '오브젝트(Object)'라고 부르려고 해.

좀 있어보이는 말을 붙여야 내가 학위 따는데 도움이 될 테니까...
**객체 지향 프로그래밍(Object-oriented programming)** 어떨까?

------------------------------------------------------------------------

## 앨런 케이가 생각했던 객체 지향의 본질

이후 앨런 케이는 박사 과정을 졸업하고,
혁신의 요람으로 유명한 제록스 파크에 근무하게 된다.

그곳에서 객체 지향 프로그래밍을 할 수 있는 언어인 스몰톡(Smalltalk)을 공동 개발했다.
'객체 지향 프로그래밍(OOP)'라는 용어를 만들고 대중화시킨 인물이 되었다.

앞서 말했던 것처럼, 객체 지향이란 거대한 코끼리 같은 존재다.
앨런 케이와 스몰톡 이후에도 수많은 언어와 이론들이 나오면서 발전해왔다.

따라서 앨런 케이의 말이 꼭 정답이라고 할 수는 없다.

하지만 앨런 케이가 생각했던 객체 지향의 초기 아이디어는
우리가 객체 지향을 이해하는 아주 좋은 시작점이라고 생각한다.

그럼 라디오스타 식의 질문을 한번 날려보도록 하자.

> 앨런 케이에게... 객체 지향이란?

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-alan-kay-OOP/assets/9c0f6ec023e9a76023dde826a8dcd86b83ac5111.jpg)

> “OOP to me means *only* **messaging**, local retention and protection and **hiding of state-process**, and **extreme late-binding** of all things.”
> **- Alan Kay**

[2003년에 앨런 케이가 한 말](http://userpage.fu-berlin.de/~ram/pub/pub_jf47ht81Ht/doc_kay_oop_en?utm_source=pocket_mylist)이다.

풀어서 설명해보면,
앨런 케이가 생각하는 OOP의 본질은

1\) 메시징
2) 캡슐화
3) 동적 바인딩이다.

## 메시징, 캡슐화, 동적 바인딩이 합쳐질 때

앨런 케이는 소프트웨어를 정리하고 싶었다.

앨런 케이식 소프트웨어 정리법의 핵심은 3가지.

- 관련있는 데이터와 프로시져를 찾아서 묶고 다른 객체가 내부를 건드리지 못하게 한다. **(캡슐화)**

- 다른 객체의 데이터나 프로시져가 필요할 때는 메시지 요청한다. 메시지를 받는 객체는 스스로 처리 방법을 선택한다. **(메시징)**

- 메시지를 받는 객체는 그때 그때 달라질 수 있다. **(동적 바인딩)**

이 3가지가 합쳐지면 이런 효과가 나타난다.

### 1) 변경가능한 공유 데이터가 최소로 줄어든다.

- 관련있는 프로시져와 데이터를 묶은 다음, 다른 객체는 접근할 수 없게 하기 때문이다.
- 다른 객체의 상태를 알아내거나 바꾸려면, 해당 객체가 정해놓은 형식으로 메시지를 보내는 방식밖에 없다.
- 이걸 '캡슐화'라고 한다.

### 2) How(구현) 부분을 쉽게 바꿀 수 있다.

- '메시지'를 받는 부분만 일관되게 유지한다면, 실제로 그걸 처리하는 코드는 바뀌어도 실행에 문제가 없다.
- '메시지를 보내는 것'은 메서드(함수)를 호출하는 것과 다르다.
- 다른 객체가 돈을 달라는 메시지를 보내면, 지갑에서 돈을 꺼내주든, 옆에 있는 친구한테 돈을 빌리든, 스마트폰으로 이체를 해주든 받는 객체가 알아서 결정한다.

### 3) 메시지를 실제로 처리하는 객체를 쉽게 바꿀 수 있다.

- 기능의 변경이 쉬워진다.

- 메시지를 보내는 코드는 컴파일 타임에 이미 결정되지만, 실제로 어떤 객체가 그 메시지를 받아서 처리할지는 런타임에 결정된다. 이걸 '동적 바인딩'이라고 한다.

- 비유하자면, **동적 바인딩은 다용도 드라이버 같은 느낌**이다. 손잡이와 드라이버의 연결 부분을 통일해준다. 그 다음 여러개의 드라이버를 만들어둔다. 새로운 드라이버를 구하지 않아도 그때 작업 중에 바꿔 끼워가면서 '다용도'를 만들어낼 수 있다.

  ![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-alan-kay-OOP/assets/5f8e3c9900831a59a5ba8868f74260fd7a96fdc8.png)

## 아메바 경영, 객체 지향 조직 관리

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-alan-kay-OOP/assets/a6a3f208831a8f3d9c327c7611743fc9389ddfc1.jpg)

이건 사족이지만,
'아메바 경영'이라는 말을 들어본 적 있는지?

일본에서 '경영의 신'이라 불리는 이나모리 가즈오의 경영 방법론으로 유명하다.
한 때 네이버가 적극적으로 도입하기도 했었고.

이 아메바 경영의 핵심도 객체 지향과 비슷했다.

거대한 대기업은 너무 느리고 복잡하다는 문제가 있다.

그래서 아메바 경영은 이렇게 한다.

- 기업의 조직을 '아메바'라는 **최소 구성 단위로 나눈다.**
- 기업 전체가 공유하던 '매출' '비용' 같은 **상태 데이터를 분리**한다.
- 각 아메바 조직이 따로 따로 수익성을 계산한다.
- 각 조직은 이제 하나의 소기업처럼, **다른 부서와 거래 관계**를 맺는다.

이런 식으로 거대한 기업도 주인 의식을 고취하고
혁신을 만들어낼 수 있다는 그런 방법론이다.

객체 지향 프로그래밍하고 너무 비슷하지 않은가?
다른 말로 '객체 지향 조직 관리'라고 불러도 될 거 같다.

🔗 [아메바 경영, 네이버가 일하는 방법](https://brunch.co.kr/@miraebookjoa/5)

## 앨런 케이가 생각한 본질이 '아닌' 것

앨런 케이는 후에 '객체 지향 프로그래밍'이라는
이름을 잘 못 지은 거 같다면서 유감을 표시했다.

> “I’m sorry that I long ago coined the term “objects” for this topic because it gets many people to focus on the lesser idea. The big idea is **messaging**.”
> -Alan Kay

'객체 지향'이라는 말을 쓰다보니, 너무 객체나 클래스에 초점이 가게 된다.
OOP의 본질을 흐리는 것 같다. 진짜 핵심은 '메시징'이다. 라고 직접 말했다.

확실히 '객체 지향'은 확실히 '객체'를 이해해야만 할 것 같은 느낌을 팍팍 주는 네이밍이다.
네이밍 실수를 인정하는 걸 보니, 역시 앨런 케이도 프로그래머였다.

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-alan-kay-OOP/assets/8825baf2d2698276fcfc08f9d9b4104305a05d71.png)

사실 여기서 내가 짚고 싶은 것은,
**앨런 케이가 꼽은 3가지에 클래스, 상속, 타입, 다형성 같은 말들이 없었다**는 거다.

우리는 객체 지향을 처음 배울 때 수많은 개념의 홍수를 맞닥뜨린다.
클래스, 상속, 다형성, 합성, 정적 타입, 응집도, 의존성, 결합도, SOLID...

앨런 케이 이후에 객체 지향의 이론과 방법론은 오랫동안 발전되고 축적되어왔다.

실제로 객체 지향을 가장 대중화시킨 것은 앨런 케이의 스몰톡이 아닌, C++과 JAVA였고,
많은 개발자들이 C++, JAVA를 배우면서 객체 지향을 배우게 된다.

C++, JAVA의 핵심 아이디어가 클래스와 상속이기 때문에,
많은 교과서와 아티클이 객체 지향하면 클래스와 상속부터 언급하는 게 아닐까 싶다.

하지만 그건 객체 지향의 '필수 조건'이 아니다.
*(Javascript에는 클래스가 없지만, 객체 지향을 구현할 수 있는 이유.)*

당연히 이 수많은 이론들이 틀렸다고 말하는 게 아니다.
객체 지향을 '잘하려면' 결국은 잘 알아야 하는 개념들이다.

하지만 초보자 입장에서 너무 많은 것들이 들어오다보니 혼란스러울 수 밖에 없고,
최소한의 본질을 이해하는 게 가장 먼저라는 말을 하고 싶었다.

- 메시징.
- 캡슐화.
- 동적 바인딩.

객체 지향을 처음 이해할 때 나에게 도움이 됐던 것은
앨런 케이가 말한 객체 지향의 본질이었다.

딱 저 3개의 키워드만 들으면, 캡슐화되어있고 서로 호환가능한 세포들이
서로 메시지를 주고받으면서 더 큰 소프트웨어를 구성하는 모습이 떠오른다.

이건 독립된 컴퓨터들로 이뤄진 인터넷이나
서버-클라이언트 구조로 이뤄진 웹의 모습과도 되게 닮아있다.

([이 글](https://medium.com/javascript-scene/the-forgotten-history-of-oop-88d71b9b2d9f)에서는 객체 지향 프로그래밍이 아니라,
메시지 지향 프로그래밍(Message oriented Programming, MOP)
이라고 부르자고 말하기도 한다.)

어쨌든 내가 한번 이걸 이해하고 나자

그 동안 들었던 같은 수수께끼 같은 말의 뜻이 머리에 들어오기 시작했다.

> 아, 객체를 만들었다고 다가 아니라, 객체들이 어떻게 '협력'해서 전체를 이루는지가 더 중요하구나.

> 오... 결국 메시지를 누구할테 위임할지 결정해주는 게 타입 계층이구나.

> 객체에서 메시지를 수신하는 부분만 따로 떼어내서 정의한 게 인터페이스라고 하는 거군.

> 그때 그때 동적 바인딩을 해야 하니까, 객체의 생성과 사용을 분리하라는 거였네.

> 아, 객체를 묶고 이름을 지을 때 최대한 실제 세계와 비슷하게 만들면 더 이해하기 쉽겠네.
> 그래서 '도메인'이라는 말이 많이 나오는 거구나.

이런 식으로.

객체 지향이라는 코끼리를 설명해주던
수많은 사람들의 말이 조금씩 퍼즐 맞춰지는 느낌이랄까.

이 글을 읽는 분들도 그런 느낌을 조금이나마 받으셨으면 해서,
부족한 지식으로 긴 글을 써보았다.

## 요약 정리

- 1960년대에는 행동(프로시져)를 기준으로 코드를 정리했다.
- 이런 정리 방식은 변경하기가 어렵고, 버그를 유발했다.

<!-- -->

- 앨런 케이는 **세포와 컴퓨터 네트워크**에서 영감을 받아 객체 지향의 아이디어를 생각해냈다.
- **자기 데이터를 숨긴 독립된 객체들이, 메시지 소통을 통해서 소프트웨어를 구성하는 방식**이었다.

<!-- -->

- 앨런 케이는 객체 지향 프로그래밍의 본질이 **메시징, 캡슐화, 동적 바인딩**이라고 생각했다.
- 이 3가지 키워드를 가지고 객체 지향을 이해하면 훨씬 이해가 쉽다.

## 참고 자료

🔗 [Dr. Alan Kay on the Meaning of “Object-Oriented Programming”](https://www.purl.org/stefan_ram/pub/doc_kay_oop_en)
🔗 [The Forgotten History of OOP](https://medium.com/javascript-scene/the-forgotten-history-of-oop-88d71b9b2d9f)
🔗 [Alan Kay and OO Programming](https://ovid.github.io/articles/alan-kay-and-oo-programming.html)
🔗 [The Roots of Object Oriented Programming](http://mfadhel.com/lost-oop/)
🔗 [생활코딩 - 객체 지향 프로그래밍](https://opentutorials.org/course/743/6553)
🔗 [객체 지향 프로그래밍이 뭔가요?](https://www.yalco.kr/16_oodp/)

## 이전 글

👈 [객체 지향 프로그래밍을 이해하는 시작점](https://velog.io/@eddy_song/oop-starting-point)
