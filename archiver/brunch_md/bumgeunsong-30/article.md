---
title: 생각만으로 컴퓨터를 제어할 수 있다면?
published_date: 2017-08-15 00:00
tags: 인터페이스, 뇌, 컴퓨터
meta_description: 뇌-컴퓨터 인터페이스 Brain-Computer Interface (1)
meta_image: https://img1.daumcdn.net/thumb/R1280x0.fjpg/?fname=http://t1.daumcdn.net/brunch/service/user/15UX/image/_3Aa6dhCk0pCpr6eik5wXY_Zadk.jpg
lang: ko
---

# 생각만으로 컴퓨터를 제어할 수 있다면?

최근 물리학자 미치오 카쿠가 쓴 \<마음의 미래\>라는 책을 읽었다. 인간의 뇌와 마음에 관한 과학 연구들을 소개하는 책이다. 나는 ‘텔레파시’와 ‘염력’을 설명하는 부분이 인상적이었다. 텔레파시나 염력을 구현하려는 초기 단계의 연구를 소개하고 있었다. 아니, 우리가 히어로 영화나 SF 영화에서나 보던 텔레파시나 염력이 실제로 가능하다고?

![magneto.jpg](/Users/bumgeunsong/coding/writing-archiver/archiver/brunch_md/bumgeunsong-30/assets/7c14dc0b9d5050b1c0724a882e47f75fbbcc8739.jpg)

![Professor-X.jpg](/Users/bumgeunsong/coding/writing-archiver/archiver/brunch_md/bumgeunsong-30/assets/f331791ce68e01322e3f37fdfaeb976ef2640590.jpg)

생각만으로 상대에게 메시지를 전달하거나, 기계를 움직일 수 있게 하는 이 기술을 뇌-컴퓨터 인터페이스(Brain-Computer Interface, BCI)라고 한다. (Brain-Machine Interface라고도 한다.) 인터페이스(Interface)란 기계와 인간의 소통이 가능하도록 만든 매개체를 뜻한다. 우리가 평소에 사용하는 키보드, 마우스 등이 모두 ‘인터페이스’다. 그중에서도 BCI는 뇌에서 나오는 신호를 직접 읽어내 컴퓨터에 전달하는 기술로, 인터페이스의 끝판왕이라고 할 수 있다.

![마징가.jpg](/Users/bumgeunsong/coding/writing-archiver/archiver/brunch_md/bumgeunsong-30/assets/883379fe7a6add7ecc121e582ea86491c3c8b026.jpg)

BCI는 최근 뉴스에 많이 등장했다. 실리콘 밸리의 이슈 메이커이자 테슬라와 스페이스 X의 창업자인 일론 머스크가 ‘뉴럴링크 코퍼레이션’(Neuralink Corp)을 설립했기 때문이다. 이름에서 추측할 수 있듯이 뉴럴링크는 인간 뇌를 모니터링해서 생각을 읽고 저장하며, 다른 사람의 뇌로 전송하는 제품을 만들려는 회사다. 뉴럴링크는 아직 초기 단계의 회사이고 정확하게 무엇을 할 것인지는 아직 불분명하지만 BCI를 연구하는 학자들을 대거 채용하고 있으며 제품 초안도 어느 정도 확정된 것으로 월스트리트 저널이 보도했다.

<a href="https://www.wsj.com/articles/elon-musk-launches-neuralink-to-connect-brains-with-computers-1490642652" class="inner_wrap #opengraph" target="_blank"></a>

**Elon Musk Launches Neuralink to Connect Brains With Computers**

Billionaire entrepreneur Elon Musk wants to merge computers with human brains to help people keep up with machines.

https://www.wsj.com/articles/elon-musk-launches-neuralink-to-connect-brains-with-computers-1490642652

아직은 비현실적인 얘기로 들리지만, 이 일론 머스크라는 남자는 이미 여러 차례 비현실적인 아이디어를 현실로 만들어낸 사람이어서, 많은 사람이 BCI 기술에 대해서 관심을 두게 되었다.

페이스북도 가세했다. 최근에 뇌를 스캔해서 텍스트를 입력할 수 있게 만드는 기술을 개발 중이라고 밝혔다. 페이스북의 R&D 그룹 ‘Building 8’은 현재 손가락으로 하는 타이핑보다 5배 빠른, 1분에 100 단어를 타이핑할 수 있는 속도를 목표로 연구 중이라고 한다.

<a href="https://techcrunch.com/2017/04/19/facebook-brain-interface/" class="inner_wrap #opengraph" target="_blank"></a>

**Facebook is building brain-computer interfaces for typing and skin-hearing**

Today at F8, Facebook revealed it has a team of 60 engineers working on building a brain-computer interface that will let you type with just your mind without..

http://social.techcrunch.com/2017/04/19/facebook-brain-interface/

과연 BCI란 정확히 무엇이고, 어디까지 왔으며, 어떤 영향력을 가지고 있는 것일까? 이번 글에서는 아직은 멀게만 느껴지는 BCI라는 기술에 대해서 쉽게 설명하고, BCI가 우리 삶에 어떤 의미를 가지는지 얘기해보려고 한다. 먼저 BCI의 원리에 대해서 간단하게 알아보자.

## BCI의 원리와 종류

BCI가 가능한 이유는 우리 뇌가 전기로 신호를 주고받기 때문이다. 뇌에는 약 1조 개의 신경 세포(Neuron)가 있고, 이 세포들은 서로 모두 연결되어 있다. 우리가 어떤 생각을 하고, 몸을 움직이고, 감정을 느끼고, 기억을 떠올릴 때, 이 신경세포들은 특정한 전기 신호를 끊임없이 만들어낸다.

이 전기 흐름의 일부가 전자기파의 형태로 바깥으로 빠져나오는데, 이를 뇌파(brainwave), 혹은 뇌전도(EEG)라고 한다. 이 뇌파를 측정해서 신호를 해석해내는 것이 BCI의 기본적인 원리다.

대표적인 BCI는 3가지가 있다.

첫 번째는 우리가 잘 알고 있는 기능적 자기공명 영상(fMRI)이다. fMRI는 아주 정확하게 뇌의 구조와 반응을 볼 수 있고, 뇌에 무언가를 삽입할 필요가 없는 비침습 방식이다. 하지만 거대한 자기 코일을 사용하기 때문에 부피가 엄청나게 크고, 가격도 수십억 원에 달한다. 연구용으로 사용할 수는 있지만, 소비자들이 쓸 수 있는 인터페이스로 만들기에는 무리가 있다.

![MRI.jpeg](/Users/bumgeunsong/coding/writing-archiver/archiver/brunch_md/bumgeunsong-30/assets/3f2ff9ad592ca2f6b8ac0505f4e6e41ab316a4da.webp)

![MRI-brain.jpeg](/Users/bumgeunsong/coding/writing-archiver/archiver/brunch_md/bumgeunsong-30/assets/a209a3b92851f35c9e3f7bb0abeb9cc8ea26dc12.webp)

두 번째는 뇌파 스캐너(EEG)다. 전극 다발이 가득 달린 헬멧을 쓰면, 그 전극이 뇌에 흐르는 전류를 감지해 컴퓨터로 전송한다. 흔히 영화에서 거짓말 탐지를 할 때 사람 머리에 전극을 잔뜩 붙여놓는 바로 그 기계다. EEG는 편리하고 값이 싸서 일반인을 대상으로 상용화되기가 유리한 분야다. 문제는 해상도가 낮다는 것이다. 뇌에서 발생하는 전기신호는 두개골을 통과하면서 약해지기 때문에, 뇌파를 원래 형태 그대로 재현하기가 어렵다.

![EEG.jpg](/Users/bumgeunsong/coding/writing-archiver/archiver/brunch_md/bumgeunsong-30/assets/1b1df03aff6055151621b03c380df42d6a0ca786.jpg)

세 번째는 피질 전도(ECOG) 스캐너다. ECOG는 두개골을 거치지 않고 두뇌 신호를 직접 수신하기 때문에 해상도가 높다. 물론 그 말은 환자의 두개골 일부를 절개하고 뇌에 직접 전극을 연결한다는 뜻이다. 주로 환자들을 대상으로 시술해서 연구한 결과들이 나와 있다.

![ECOG.jpg](/Users/bumgeunsong/coding/writing-archiver/archiver/brunch_md/bumgeunsong-30/assets/3ae7703e83566ccd8faef5901604033a17eea731.jpg)

## BCI 관련 연구 결과

2011년 유타대학교 연구진은 ECOG를 뇌에 붙이고 환자에게 “Yes”, “No”, “Hello” 같은 간단한 단어를 말하게 했다. 그 단어를 말할 때 생기는 두뇌 신호를 컴퓨터에 저장한다. 이렇게 대략적인 ‘사전’을 작성하면, 환자가 머릿속으로 “Hello”를 생각하기만 해도 어떤 단어인지 알 수 있다. 이 연구팀은 76%에서 90%의 단어를 맞췄다고 한다.

버클리 대학교의 캘런트 박사 팀은 고해상도 MRI 기술을 개발해서 사람이 어떤 영상을 볼 때 뇌의 패턴을 기록했다. 그러고 나서 MRI로 측정한 뇌의 패턴과 실제로 그 사람이 본 영상의 관계를 추적하는 수학 공식을 개발했다. 예를 들어, 어떤 사람이 사과 그림을 보고, 뇌의 모양이 ABCD로 변했다. 이제 윤곽선이 조금 다른 사과 그림을 보여준다. 그때 뇌의 패턴이 BBCD가 되었다면, 패턴 B가 윤곽선 인식과 관련되어있음을 알 수 있다. 이런 식으로 계속해서 다른 그림과 영상을 보여주고 뇌의 패턴을 기록하면, 뇌의 패턴을 그림으로 변환시킬 수 있는 공식을 추론할 수 있다.

미치오 카쿠는 실제로 이 실험을 목격했는데, \<모나리자\>를 보고 나온 두뇌 신호를 입력하자, 컴퓨터가 여배우 Salma Hayek의 이미지를 찾아냈다고 한다. 물론 인간의 얼굴 식별 기준으로 보면 한참 못 미치지만, 컴퓨터가 골라낸 결과치고는 상당히 정확하다고 할 수 있다.

![monalisa.jpg](/Users/bumgeunsong/coding/writing-archiver/archiver/brunch_md/bumgeunsong-30/assets/fdb0ef73db258301e3d0f48c09c471d25e43cedd.jpg)

![salma-hayek1 (10).jpg](/Users/bumgeunsong/coding/writing-archiver/archiver/brunch_md/bumgeunsong-30/assets/de35f4907f6b41e0fa17ba20c5835fb1a29af1ef.jpg)

------------------------------------------------------------------------

# 현재 BCI 산업의 위치는?

BCI가 만약 정말로 실현된다면, 그 영향력은 엄청날 것이다. 하지만, 아직까지 BCI는 우리가 상상한 ‘텔레파시’나 ‘염력’을 구현하기에는 많이 부족하다. 연구실 안에서 고해상도 MRI를 사용해서 단어나 이미지를 판별하는 정도일 뿐이다.

하지만 일반인을 대상으로 한 BCI도 이미 나와 있다. 보급형 EEG 스캐너는 약 80달러 정도면 살 수 있다. 생긴 것도 의외로 기괴하지 않고 깔끔하게 생겼다. 이런 EEG 스캐너는 뇌파의 종류나 착용자의 감정 변화를 측정할 수 있다. 이를 활용해서 BCI를 상업화하려는 여러 시도들이 있었다. 현재 BCI 관련 산업은 어디까지 와있는지 한번 알아보자.

## 현재까지 상용화된 BCI들

실험실에만 존재하던 BCI는 2000년대 말부터 일반인을 대상으로 제품화되어 시장에 등장하기 시작했다. 기존의 EEG는 수많은 전극이 달려있고, 휴대성이 매우 떨어지고, 비싸다. 게다가 정확한 결과를 얻기 위해서는 머리카락을 자르거나 젤을 발라야 하는 문제도 있었다. (무엇보다 일상적으로 쓰고 다니기에는 너무 무섭게 생겼다…)

그런데 2011년에 Neurosky라는 회사가 처음으로 Mindwave라는 개인용 EEG를 출시했다. Node의 개수를 딱 1개로 줄이고, 젤이 필요 없는 Dry 방식이다. 블루투스를 지원해서 무선으로 사용할 수 있다. 디자인도 깔끔하게 생겨서 기괴한 수준에서는 많이 벗어났다. 처음으로 일반인들이 쓸 수 있는 EEG 스캐너가 만들어진 것이다. 가격은 약 100달러.

![mindwave_mobile_g02.jpg](/Users/bumgeunsong/coding/writing-archiver/archiver/brunch_md/bumgeunsong-30/assets/a23d8ac73865db820d1fe107e43df4ca50145ad2.jpg)

다만 전극의 개수가 딱 1개이기 때문에, 뇌의 전기 신호가 정확히 어느 부분에서 일어나는지 알 수가 없다. 대신 Mindwave는 뇌파의 파장(frequency)을 측정한다. 인간의 뇌에서 나오는 전기신호, 뇌파는 주파수와 진폭에 따라서 다음과 같이 나뉜다.

![brainbalance-04.jpg](/Users/bumgeunsong/coding/writing-archiver/archiver/brunch_md/bumgeunsong-30/assets/0e814e14a88f5d446503c16026bad836f043e367.jpg)

Mindwave는 뇌파의 종류에 따라서 현재 이 사람이 집중한 상태인지 아니면 긴장이 풀린 상태인지 등을 측정한다. Neurosky 홈페이지에 가보면 몇십 개나 되는 관련 어플리에케이션이 소개되어있는데 주로 집중력 향상 게임이나 명상 관련 프로그램이다. 주어지는 과제에 따라서 집중력을 몇 초 이상 유지한다거나, 명상을 하는 동안 나의 뇌파가 잘 진정되는지 체크해준다.

개인용 EEG는 수많은 파생 제품을 낳았다. Mattel이라는 장난감 회사는 Mindflex라는 장난감을 만들었다. EEG를 끼고 집중 상태를 유지하면 공이 떠오르고, 집중하지 않으면 다시 공이 내려온다. 이를 이용해 여러 가지 장애물을 통과시키는 게임이다. EEG에서 특정 뇌파를 감지하면 공 밑에서 나오는 팬(fan)이 작동한다. 비슷한 제품으로 스타워즈에서 제다이 기사들이 쓰는 포스(염력)에서 따온 force trainer라는 장난감이 나오기도 했다.

![mindflex-011.jpg](/Users/bumgeunsong/coding/writing-archiver/archiver/brunch_md/bumgeunsong-30/assets/c2ead6e4ca454dfc7e41647d8a8a615d05c15ec9.jpg)

2012년에 일본에서는 ‘네코미미’라는 EEG 스캐너 제품이 유행을 한번 끌었다. 네코미니는 ‘고양이 귀’라는 뜻인데, 말 그대로 고양이 귀가 달린 머리띠다. 이 머리띠를 착용하면 기분에 따라서 고양이 귀가 움직인다. 착용한 사람이 편안함을 느끼면 귀가 아래로 내려가고, 집중할 때는 귀가 쫑긋 서게 되고, 무언가에 흥미를 느낄 때는 양쪽 귀가 교차로 움직인다. 코스튬 문화가 발달한 일본이어서 그런지 파티용품이나 패션 아이템으로 큰 인기를 끌었다고 한다.

![necomimi-2.jpg](/Users/bumgeunsong/coding/writing-archiver/archiver/brunch_md/bumgeunsong-30/assets/cd2669f7ae23511c33f0951f4188ac19f9a77524.jpg)

## 대중화에 실패한 BCI

그런데 여전히 BCI 제품들은 대중들에게는 별다른 주목을 받지 못하고 있다. 방금 설명한 것과 유사한 장난감이나 아이템들이 매년 7-8종씩 출시되고 있지만, ‘오 신기한데?’ 이상의 가치를 주지 못하고 곧 1년 이내에 자취를 감추고 있다. (개인적으로 10만원짜리 고양이 귀가 유행이라도 끌었다는 것이 신기하다..)

이는 크게 봤을 때 IT 분야의 큰 화두인 ‘웨어러블’ 트렌드와도 관련이 있다. ‘웨어러블’은 내 몸에 착용해서 여러 가지 데이터를 얻어내고 앱을 통해 이를 활용할 수 있는 서비스로 애플 와치, 핏빗 등 다양한 서비스들이 나와서 사람들의 이목을 끌었다. 웨어러블 기기가 ‘넥스트 아이폰’이 될 거라고 말한 사람들도 많았다. 이들 역시 처음의 기대와 다르게 사람들이 정말 꼭 사야 할 만한 가치가 있는 건가?라는 질문에 확신을 주지 못하면서 아직까지는 ‘넥스트 아이폰’의 근처에도 가지 못했다.

BCI도 마찬가지 현상을 겪는 것으로 보인다. 집중력 향상 게임이나, 내 감정을 표현해주는 머리띠는 결국 “내 마음을 읽다니, 신기한걸?” 하고 끝이다. 그 가격대와, 머리띠를 머리에 쓰는 것을 감수할만한, 정말 생활에서 편리함을 느낄 수 있는 ‘킬러 앱’을 제공하지 못하기 때문이다. 사람은 자기 삶을 바꿀 수 있을 정도로 편리한 물건이 아니면 평소 쓰던 것을 바꾸려고 하지 않는다.

## 발전된 BCI를 내놓은 Emotiv

물론 개인용 BCI 기기는 계속 발전을 거듭하고 있다. 최근 Emotiv라는 회사가 더 발전된 형태의 EEG 스캐너를 출시해서 다시 주목을 받았다. EPOC라는 헤드셋인데, 기존 EEG 스캐너와 달리 전극이 14개 달려있다. 단지 뇌파의 종류만 파악할 수 있었던 기존의 EEG와 달리, 뇌에서 나타나는 신호 패턴을 꽤나 정확하게 보여준다 한다.

Emotiv가 밝힌 바에 따르면, 30개의 감정과 행동을 읽을 수 있다. 흥분, 긴장, 지루함, 몰입, 명상, 좌절 등의 감정뿐만 아니라, 윙크, 웃음, 충격, 미소, 찡그림 등의 얼굴 표정까지 인식한다. EEG를 적용할 수 있는 서비스의 범위가 더욱 넓어졌다. 예를 들면, 메신저의 EEG를 연결해서 내가 메시지를 타이핑할 때 어떤 감정을 느끼고, 어떤 표정을 짓는지를 의사소통할 수도 있겠다. (근데 왠지 쓰기 싫은 기능이다.) 아니면 내가 집에 들어왔을 때 내 집이 내 감정을 알아차리고 그에 맞는 음악을 미리 틀어놓을 수도 있다.

게다가 Emotiv는 EEG가 발생시키는 패턴의 원데이터(raw data)도 제공할 수 있기 때문에 프로그래밍을 하면 굉장히 다양한 방식으로 활용이 가능하다. 내가 본 영상에서는 시험자가 꽃이 피어나는 영상을 보게 한 뒤에, 그때 나타나는 뇌의 패턴을 기록하고, 그다음 실제 생각만으로 꽃을 피어나게 만드는 것을 보여주었다. 사람이 어느 정도 훈련을 거치면, 드론과 RC카 조종도 가능하다고 한다.

# 오류가 발생했습니다.

자바스크립트를 실행할 수 없습니다.

EEG를 통해서 ‘마음으로 하는 디제잉’을 시도한 프로젝트도 있다. 스미노프에서 지원한 ‘마인드튠즈Mindtunes’다. 출연자들은 모두 몸을 마음대로 움직일 수 없는 장애를 가지고 있다. 마인드튠즈는 이들의 뇌파를 캐치해서 음악으로 바꾸는 프로젝트다.

# 오류가 발생했습니다.

자바스크립트를 실행할 수 없습니다.

영상을 보면 생각처럼 머리로 무엇인가를 입력하는 게 쉽지 않다. 당연한 일이다. 머릿속에 일정한 생각이 계속 떠오르게 하는 게 쉽지 않다는 건 지금 우리도 당장 알 수 있는 사실이다. 하지만 시행착오를 거친 끝의 3명의 출연자들은 음악을 합주하는 데 성공한다. 몸이 불편해서 음악을 연주해볼 수 없었던 출연자들이 음악을 만들어내면서 함박웃음을 짓는 장면이 나온다. 감동적이다.

------------------------------------------------------------------------

