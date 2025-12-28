---
title: 정렬 알고리즘은 왜 배워야 할까?
published_date: 2022-01-29 15:35
tags: algorithm
meta_description: 그냥 가져다 쓰면 되지, 왜 머리 아프게 무슨 정렬, 무슨 정렬.. 다 배우는 걸까?
meta_image: https://images.velog.io/images/eddy_song/post/fbc3c2d7-b65b-4c98-b05a-9b22bad0d240/whatIsWater.jpeg
lang: ko
---

# 정렬 알고리즘은 왜 배워야 할까?

*by eddy_song*

알고리즘. 어느 개발자나 피해갈 수 없는 주제다.

그런데 알고리즘을 배우다 보면,
'정렬(Sorting)'을 아주 중요하게 다룬다.

교과서에서도 제일 먼저 나오는 게 정렬 알고리즘.
알고리즘 강의를 봐도 내용의 30-40% 정도가 정렬.

처음 알고리즘을 접했을 땐,
왜 이렇게 정렬을 중요하게 다루는지 의아했다.

> 흠, 정렬이 그렇게 중요한 건가...?

## 어디에나 있는 정렬

우리가 쓰는 소프트웨어를 생각해보자. 곳곳에 정렬이 들어가지 않은 곳이 없다.

- 내 메일 보관함은 도착 시간 기준으로 정렬돼있다.
- 배달앱을 켜면 음식점이 인기순, 판매량순, 배달빠른 순으로 정렬된다.
- 구글에 검색어를 입력하면 가장 관련있는 페이지 순으로 정렬된다.
- 지도 앱에서 음식점을 검색하면 가까운 거리 순으로 정렬된 결과를 보여준다.
- 페이스북은 내가 좋아할만한 게시물 순으로 뉴스피드를 정렬한다.
- 트위터 피드. 인스타 스토리... 손 아프니까 이하 생략.

그 외에 우리 눈에 보이지 않는 수많은 정렬까지.

정렬은 어디에나 있다.
스크롤 한번, 클릭 한번이 다 정렬이다.

다만 사용할 땐 우리가 의식하지 못할 뿐이다.
물이 뭐냐고 묻는 물고기처럼.

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-why-sorting-algorithm/assets/79b7a1eb752b4fab31eaea6d89a5c8b6e5dc74cb.jpg)

## 정렬은 큐레이션이다.

사실 소프트웨어의 일을 아주 단순하게 표현하면,
'데이터를 저장하고 가공해서 사용자에게 보여주는 것'이다.

사람이 받아들일 수 있는 데이터의 양은 정해져있다. 저장된 수많은 데이터 중에서, **가장 중요하고 유용한 것 몇 개를 골라내야 한다. 골라내려면 당연히 줄을 세워야 한다.**

**검색도 정렬과 관련이 있다.** 수많은 데이터 중에서 사용자가 원하는 무언가를 효율적으로 찾아낼 때도 정렬이 활용된다.

정보를 다루는 소프트웨어에서 정렬은 거의 숨쉬기다.
자주 실행되는 가장 기본적인 작업이다.

그러다보니 정렬 알고리즘을 잘 만드는 건,
컴퓨터 공학에서 아주아주 중요한 주제다.

## 더 빠르게 할 수 없을까?

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-why-sorting-algorithm/assets/32018c617cc5d599ebdb8bb0bdc9ff830843ded9.jpg)

앞에 이런 책들이 꽂혀있다고 하자.
자, 여러분이 이 책을 제목순으로 정렬해야 한다면 어떻게 할까?

일단 눈에 띄는 걸 아무거나 하나 집는다.

앞쪽부터 다른 책들을 하나씩 훑으면서
이 책보다 뒤에 와야 하는 책이 있으면 그 앞에 꽂는다.

다시 정렬되지 않은 책을 뽑아서,
같은 방법으로 다른 책들을 훑으면서 적절한 자리에 꽂는다.

뭐, 이건 쉽다. 초등학생이라도 시키면 쉽게 할 것 같다.

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-why-sorting-algorithm/assets/5172b65da12c9f3fd818d3e9e7f7ec9edca7db8c.jpg)

**문제는 효율성이다.**

이렇게 하면 총 몇 번을 해야 정렬될까?

n개의 책에 대해서 최대 n-1 번의 비교를 해야 하니까,
이걸 Big O로 표기하면 O(n^2)이다.

(참고 🔗 [알고리즘의 시간 복잡도와 Big-O 쉽게 이해하기](https://blog.chulgil.me/algorithm/))

책의 수가 늘어날 수록,
해야하는 작업의 수가 매우 빠르게 증가한다.

방금 아주 대충 설명한 정렬 방법은
컴퓨터 공학에서 [삽입 정렬 (Insertion Sort)](https://gmlwjd9405.github.io/2018/05/06/algorithm-insertion-sort.html)이라고 부르는 방법이다.

쉽지만 느린 알고리즘에 속한다.
그 외에도 [버블 정렬](https://gmlwjd9405.github.io/2018/05/06/algorithm-bubble-sort.html), [선택 정렬](https://gmlwjd9405.github.io/2018/05/06/algorithm-selection-sort.html) 등이 쉽지만 느린 알고리즘이다.

**하지만 바쁘다 바빠 현대사회인이 여기서 만족할리 없다.**

> '이거보다 더 빠르게 할 수 없을까?'

세상에 존재하는 책이 몇 권인데...
50권 정렬하는데 2500번(에 가까운) 작업을 하고 있을 순 없다!

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-why-sorting-algorithm/assets/47661d74dec1022865c4e4dede961e394835b03c.jpg)

우리보다 먼저 살았던 컴퓨터 공학자, 소프트웨어 엔지니어들이 '이거보다 더 빠르게 할 수 없을까?'라며 온갖 잔머리와 테크닉을 짜냈다.

계속 새로운 정렬 방법을 시도했고, 결국 더 나은 방법을 발견해냈다.

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-why-sorting-algorithm/assets/0318d60a7a3382b31a6b56a2088e16ca5848bc46.jpg)

**그 결과, 오늘날 쓰이는 알고리즘 대부분은 O(n log n)!**

선형로그 시간 복잡도를 가진다.
O(n^2)보다 훨씬 더 빨라진 알고리즘이다.

이것보다 더 빠른 건 없냐고?
아쉽게도 일대일 비교를 통한 정렬에서 시간 복잡도는 O(n log n)이 한계다.
[수학적으로 확실히 증명](https://twinparadox.tistory.com/196)된 사실.

## 왜 정렬 알고리즘을 배워야 하는가?

그렇지만 나의 의문은 가시지 않았다.

> 좋아. 정렬이 중요하고 많이 쓴다는 건 알겠어.
> 근데 이걸 왜 꼭 배워야 해?

> 이미 훌륭한 사람들이 정렬 알고리즘 다 만들어놨고,
> 내가 쓰는 언어에 이미 내장된 정렬 함수 있고...

> 그냥 가져다 쓰면 되지
> 왜 머리 아프게 무슨 정렬, 무슨 정렬.. 다 배우는 걸까?

사실 맞다. 내가 정렬을 직접 구현해서 쓸 일은 거의 없을 거다.

하지만 유명한 책과 강의를 들으면서,
이 질문에 대한 답을 조금 들을 수 있었다.

## 정렬은 알고리즘을 배우는 가장 좋은 교재다

> *Sorting is a **natural laboratory for studying algorithm design paradigms**, since many useful techniques lead to interesting sorting algorithms.*
> *- The Algorithm Design Manual*

컴퓨터 공학에서 정렬을 잘 하는 건 너무 중요한 일이었다.

이걸 사용하면 더 빨라지지 않을까?
이 아이디어를 적용하면 더 안정적이지 않을까?

계속 이런 고민을 하다보니 정렬 알고리즘은
수많은 알고리즘 아이디어(잔머리)의 자연 집합소였다는 것이다.

- 특수한 자료구조를 쓰면 알고리즘을 더 빠르게 만들 수 있다든지,
- 무작위 난수를 사용해서 알고리즘을 좋게 만드는 방법이라든지,
- 문제를 바로 풀 수 있을 정도로 작게 쪼개는 방법이라든지,
- 인풋에 대한 가정이 있을 때 그걸 활용하는 방법이라든지.

그리고 이 알고리즘 중 무엇이 더 좋은가? 를 고민하다보면
각각의 알고리즘들을 평가하는 도구들도 자연스럽게 알게 된다.

- Big O 표기법은 물론이고,
- 평균적인 경우와 최악의 경우에 어떻게 성능이 달라지는지,
- 재귀 호출이 있을 때 복잡도는 어떻게 계산하는지,
- 왜 상황에 따라서 적절한 트레이드 오프가 필요한지

이런 아이디어들과 평가법은,
우리가 정렬 알고리즘을 직접 만들지 않아도,
개발을 하면서 맞닥뜨릴 **수많은 문제들에서 유용하게 쓰일 도구들**이다.

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-why-sorting-algorithm/assets/be7a2f91c42ed0d518325f4342421a7e21d3a9b8.png)

**다시 말해서,
정렬 알고리즘은 알고리즘을 배우는 가장 좋은 교재다.**

나도 사실 지루할 수 있는 정렬 알고리즘에 대해 굳이 글을 써야할까 망설이긴 했었다.

그러나 저 말 때문에 한번 확실히 정리하고 넘어가야겠다는 마음을 먹었다.

## 정렬에 쓰인 아이디어들을 알아보자

다양한 정렬의 구현을 설명하는 글은 이미 많기 때문에,
이 포스팅에서는 앞으로 각 정렬 알고리즘에서 어떤 아이디어가 쓰였고,
그걸 어떻게 평가할 수 있는지에 초점을 맞추려고 한다.

1.  [분할 정복을 활용한 합병 정렬 (Merge Sort)](https://velog.io/@eddy_song/merge-sort)
2.  [무작위(Random)를 활용한 퀵 정렬 (Quick Sort)](https://velog.io/@eddy_song/quick-sort)
3.  [자료구조를 활용한 힙 정렬 (Heap Sort)](https://velog.io/@eddy_song/heap-sort)
