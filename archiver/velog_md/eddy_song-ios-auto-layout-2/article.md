---
title: 오토레이아웃 조건이 충돌하면 어떻게 하지?
published_date: 2022-02-09 14:19
tags: iOS, swift
meta_description: 오토레이아웃이 띄우는 에러와 해결 방법에 대해 알아보자.
meta_image: https://images.velog.io/images/eddy_song/post/ae5abc92-4c9c-4218-951a-1c500e55d9bb/Screen Shot 2022-02-15 at 12.21.00 AM.png
lang: ko
---

# 오토레이아웃 조건이 충돌하면 어떻게 하지?

*by eddy_song*

오토레이아웃은 '조건'을 가지고 위치와 크기를 계산하는 시스템이다.

교실에서 학생 자리를 정하는 비유를 다시 떠올려보자.

> 선생님 👩‍🏫 : 자, 각자 원하는 자리의 조건을 말해봐.

> 수철 🙋 : 선생님 저는 지수 옆에 앉아야 돼요.
> 지수 🙋🏻‍♀️: 선생님 전 에어컨 옆자리 앉을 거에요.
> 형식 🙍🏼‍♂️: 선생님 전 칠판에서 2줄이상 떨어지기 싫은데요.
> 진영 🤷🏻‍♂️: 선생님 지각해도 티 안 나게 맨 구석자리로 주세요.

이 조건들이 모두 잘 맞아떨어져서 학생들의 자리를 잘 정해줄 수도 있다.
하지만....

## 오토레이아웃이 에러를 띄울 때

이 **조건을 충분히 설정해주지 않거나,**

> 민정: 선생님, 저는 맨 앞자리만 아니면 아무데나 앉을래요.
> 선생님: (음... 아무데나? 그럼 정확히 어디에 앉혀야 하지?)

서로 **충돌하는 2개의 조건을 설정**했을 때는 에러가 뜨게 된다.

> 수철: 선생님, 저는 무조건 지수 옆에 앉고 싶어요!
> 지수: 선생님, 저 수철이랑 무조건 2자리 이상 띄워주세요.
> 선생님: (...😓)

물론 현실세계의 선생님이라면, 직접 충돌을 조정하거나, 자리를 지정해줄 수 있겠지만.

우리의 엔진은 그저 프로그램일 뿐이기 때문에, 우리가 명확히 모든 걸 지정해주지 않으면 에러를 띄운다.

만약 Xcode에서 인터페이스 빌더로 UI를 만들고 있다면, 다큐먼트 아웃라인(Document Outline)에 이런 빨간색 화살표가 뜨는 걸 볼 수 있다.

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-ios-auto-layout-2/assets/e68670f2a4c9f21180fa266bca39ca1128dc4839.png)

에러는 주로 2가지 중 하나에 해당한다.

- 조건이 부족해! 👉 **Ambiguous Layouts**
- 서로 다른 조건이 충돌해! 👉 **Unsatisfiable Layouts  **

### 1. 조건이 부족할 때 (Ambiguous Layouts)

조건을 간단한 방정식으로 바꿔서 생각해보자.

> y = x + 10

이 조건이 주어졌을 때
x, y의 값은 무엇일까?

... 🤷‍♂️

맞다. 알 수 없다. x + y = 10을 만족시키는
(x, y)에는 무한한 해가 존재한다.

방정식이 충분히 주어지지 않기 때문이다.

> y \>= x + 10
> y = 2x

이번에는 `y = 2x`를 추가하고,
위의 식을 부등식으로 바꿨다.

이 때 x, y는?

... 🤷‍♀️

이것도 알 수 없다.
저 두 식을 만족시키는 x, y 값이 매우 많다.

이렇게 조건이 충분히 주어지지 않아서
오토레이아웃 엔진이 값을 구할 수 없을 때
`Ambiguous Layouts` 에러를 띄운다.

인터페이스 빌더에서 `Missing Constraints`나,
`Constraints Ambiguity` 같은 메시지가 뜨면
조건이 충분히 주어지지 않았다는 것을 알 수 있다.

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-ios-auto-layout-2/assets/59c9b0d33b75a9a91f87fa765b7bc82f6ac21c0f.png)

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-ios-auto-layout-2/assets/d0fdbeb80fb54122c63a5aec240c5cc560e95363.png)

혹은 코드로 UI를 만들고 있다면,
잘못 설정된 뷰에 `hasAmbiguousLayout` 프로퍼티를 확인해보면 된다.

> 이 에러가 뜨면 어떻게 해결해야하지?

쉽게 말하면, 필요한 조건을 더 정해줘야 한다.

먼저 X축/Y축 한 축을 정하고,
각 뷰에서 계산이 안 되는 속성이 있는지 찾아본다.

- X축 속성 (Leading, Trailing, CenterX, Width) 중 2개 이상.
- Y축 속성 (Top, Bottom, CenterY, Height)이 2개 이상.

하나의 뷰에 이 둘이 명확히 정해져야 크기와 위치를 계산할 수 있다.

속성 조건을 정했다 하더라도,
만약 관계를 맺고 있는 다른 뷰의 크기나 위치가 정해지지 않았다면
조건이 부족하다고 뜰 수 있다.

### 2. 조건이 충돌할 때 (Unsatisfiable Layouts)

이번에는 이런 방정식이 3개 주어진다.

> y = x + 20
> 2y + x = 4
> y = 6 - x

이 방정식에는 '해가 없다'
이 3개의 식을 모두 만족시키는 x, y가 없다.

오토레이아웃에서 이런 상태가 되면,
'Conflicting Constraints' 라는 오류를 띄운다.

충돌하는 조건이 있어서 뷰의 위치와 크기를 계산할 수 없다는 뜻이다.

이 때 다큐먼트 아웃라인에서는
서로 양립할 수 없는 모든 식들을 보여준다.

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-ios-auto-layout-2/assets/7563256efcb5b769bf9447a3238221679c250b02.png)

> 이 에러가 뜨면 어떻게 해결해야하지?

해결 방법은 간단한데, 일단 중요하지 않은 조건부터
하나씩 삭제해나가면서 에러가 사라지는지 본다.

코드로 UI를 만들었다면, 흔한 실수는 `translatesAutoresizingMaskIntoConstraints` 를 `false` 로 해제해주지 않는 것이다. 이러면 `Confliciting Constraints`가 뜬다.

AutoresizingMask는 오토레이아웃이 나오기 전, iOS에서 뷰의 위치와 크기를 설정하는 방법이었다. 인터페이스 빌더를 쓸 때는 자동으로 false가 된다.

코드로 쓸 때에는 false를 명시적으로 지정해줘야 오토레이아웃이 작동한다.

아니면 '우선순위(Priority)'라는 걸 활용할 수도 있다.

## 조건 우선순위 (Priority)

각 조건에는 1-1000까지 숫자로 된 우선순위가 부여돼 있다.

만약 서로 충돌하는 조건이 있다면, 우선순위 숫자가 높은 것부터 우선 적용한다.

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-ios-auto-layout-2/assets/fb5ab4e5fc575b26cbf30f4b07ccf7ac3280449e.png)

디폴트 값은 1000이다. 1000이 설정돼있으면, 충돌은 할지언정 절대 포기할 수 없는 필수 조건이라는 뜻이다. 충돌 시 1이라도 낮은 쪽은 오토레이아웃에서 반영되지 않는다.

> 그런데 우선순위는 왜 있는 걸까?

서로 충돌하는 두 조건이 굳이 필요한 경우가 있을까?
`X = 50` 이라는 조건 `X = 100`이라는 조건이 충돌한다면 한쪽을 지우면 되지 않나?

우선순위가 필요한 이유는 조건이 꼭 `=`가 아니기 대문이다.
우선순위는 부등식이 될 수도 있다.

예를 들어보자.

> 조건 1
> A.width = 0.3 \* Superview.width (`priority` = 1000)
> 조건 2
> A.width \>= 150 (`priority` = 1000)

이 경우 둘의 우선순위가 같고, Superview 사이즈가 500보다 작다면 충돌이 일어날 것이다.

하지만 A 뷰의 크기를 상위 뷰의 30%로 하고 싶으면서, 동시에 상위 뷰가 150 이하로 작아지는 상황에서는 최소 크기를 유지하고 싶다면?

저 두 조건이 모두 필요하다.
그럴 때 이렇게 부등식에 우선순위를 높여준다.

> 조건 1
> A.width = 0.3 \* Superview.width (`priority` = 750)
> 조건 2
> A.width \>= 150 (`priority` = 1000)

이렇게 하면, 상위 뷰가 500보다 클 때는 상위 뷰의 30% 크기로 늘어난다.
동시에 500보다 작을 때는 150이하로 줄어들지 않고 150을 유지한다.

이런 상황들이 꽤나 많이 일어나기 때문에,
충돌 가능성이 있는 조건들은 우선순위를 잘 설정해줘야 한다.

## 요약 정리

- **조건이 부족하면** Ambiguous Layouts 에러가 뜬다.
- 이 때는 **X/Y축에 2개 이상의 조건**이 설정됐는지 확인한다. 조건을 건 **다른 뷰의 속성이 명확하게 정해졌는지** 체크한다. 빠진 조건을 추가한다.
- **충돌하는 조건**이 있으면 Unsatisfiable Layouts 에러가 뜬다.
- 중요하지 않은 조건을 삭제하고, 공존해야 하는 조건이라면 **우선순위**를 정해준다.

## 다음 글

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-ios-auto-layout-2/assets/a45e14f7c2fd80f4739503e57a8ee35298034063.png)

Label을 하나 만들고, Top과 Leading에 조건을 정해주었다.
Bottom과 Trailing은 주지 않았다.

어...? 분명 조건을 부족하게 설정했는데, 오토레이아웃이 에러를 뱉지 않는다.
왜 이러지?

그 비밀은 다음 글에서 알아보도록 하자.
