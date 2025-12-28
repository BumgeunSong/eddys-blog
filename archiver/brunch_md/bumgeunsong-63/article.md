---
title: 메커니즘 디자인 최적화로 푸는 토큰 모델 설계 (1)
published_date: 2018-10-16 00:00
tags: 토큰, 모델, 디자인
meta_description: 1편: 메커니즘 디자인의 기본 요소와 최적화
meta_image: https://img1.daumcdn.net/thumb/R1280x0.fjpg/?fname=http://t1.daumcdn.net/brunch/service/user/15UX/image/rMgI2S_HNcudVPTbTfJ9NlQAZwo.jpg
lang: ko
---

# 메커니즘 디자인 최적화로 푸는 토큰 모델 설계 (1)

블록체인에 관심을 갖고 계신 분들이라면, ‘토큰 이코노미' ‘토큰 모델'이라는 말을 한번쯤 들어보셨을 겁니다.

블록체인 기반 네트워크는 중앙 주체가 없습니다. 그래서 토큰이라는 매개체와 시장 원리를 사용해 개인들이 각자 자신의 이익을 추구하는 행동을 하더라도 전체 네트워크 성장으로 이어지도록 만드는 시스템이 필요합니다. 이것을 ‘토큰 모델'이라고 하며 탈중앙화 네트워크가 돌아갈 수 있게 하는 ‘보이지 않는 손' 역할을 합니다.

그런데 누구나 토큰 이코노미를 얘기하지만, 사실 좋은 토큰 모델이란 무엇이고 어떻게 좋은 토큰 모델을 설계할 수 있으며, 어떤 프로세스를 통해서 토큰 모델을 설계할 수 있는지에 대해서 말할 수 있는 사람은 거의 없습니다.

저는 실제로 Decon에서 다양한 토큰 모델 설계를 경험하면서 이 분야에 독자적인 이론적 기반이 정말 필요하다고 느꼈습니다.

# 왜 암호경제학은 새로운 이론적 기반이 필요한가?

왜 그럴까요? 암호경제학도 결국은 인터넷 서비스를 만들기 위한 것인데 왜 기존에 없었던 새로운 이론과 방법론이 필요할까요?

간단히 말하자면, **탈중앙화 네트워크의 설계는 기존의 비즈니스/서비스 기획과는 완전히 다른 성격을 가지고 있기 때문**입니다.

기존의 비즈니스 기획은 규칙(시장 환경)이 주어져있고, 기업들이 자신의 이익을 극대화하기 위해서 최선의 선택을 하는 것이 목표입니다.

![1\*sRXD3K6kDZ2pdNfNorgr6w.png](/Users/bumgeunsong/coding/writing-archiver/archiver/brunch_md/bumgeunsong-63/assets/4b38fd04d382c963cd50d931e963d61a3e1f3a04.png)

하지만 탈중앙화 네트워크의 설계는 역방향입니다. 각각의 주체들이 전략적이고 이기적으로 행동한다고 가정할 때, 설계자가 원하는 결과를 얻어내기 위해서 규칙을 설계하는 것이 탈중앙화 네트워크의 설계입니다.

![1\*ZqeVKQArw2_XCDPlYKJCTA.png](/Users/bumgeunsong/coding/writing-archiver/archiver/brunch_md/bumgeunsong-63/assets/d4f20be5a5609f6633ccf34800c448183983d419.png)

# 게임 이론과 메커니즘 디자인에서 단서를 찾다

경제학의 세부 분야 중, 게임 이론과 메커니즘 디자인이라는 분야가 있습니다. 게임 이론(Game theory)은 많이 알려져있듯이 주어진 게임의 규칙에서 최선의 전략을 찾는 것을 연구하는 이론입니다.

**메커니즘 디자인(Mechanism Design)**은 상대적으로 덜 알려져 있는데요. 메커니즘 디자인은 게임 이론과 반대로 **설계자가 원하는 결과를 정의하고 플레이어들이 그 결과를 향해 가도록 유도하는 게임을 만드는 이론**입니다.

뭔가 익숙한 말을 반복하고 있는 것 같지 않나요? 맞습니다. **토큰 모델 설계와 메커니즘 디자인은 굉장히 유사한 목표를 가지고 있습니다.**

메커니즘 디자인은 오랫동안 경제학자들 사이에서 연구되어왔고, 투표, 선거, 경매, 규제 등 다양한 제도/정책 설계에 활용되는 이론입니다. 그렇다면 기존 메커니즘 디자인 연구들을 활용해서 토큰 모델 설계를 체계화해볼 수는 없을까? 이런 의문에서 이 연구가 시작되었습니다.

# 메커니즘 디자인의 기초

이번 글에서는 메커니즘 디자인을 토큰 모델 설계에 적용하기에 앞서 알아야할 2가지, ‘메커니즘 디자인의 기초 개념’과 ‘메커니즘 최적화’를 설명드리겠습니다.

메커니즘은 다음과 같은 요소들로 구성되어 있습니다.

Agent : 메커니즘 내에서 전략적으로 상호작용하는 주체
Type: Agent i가 가지고 있는 사적인 정보
Decisions: 가능한 사회적 결과의 집합
Utility Function: Agent i가 특정 Decision에 대해 얻는 순효용
Decision Function: 각 Agent의 행동을 종합하는 결정 규칙
Transfer Function: Decision과 Type에 따라서 각 Agent가 받거나, 내야하는 돈
Social Choice Fucntion: Decision funtion과 Transfer function의 결합

Mechanism: 각 Agent들의 전략 집합과 Social choice function의 결합

물론 <a href="https://brunch.co.kr/@bumgeunsong#info" class="link" target="_blank"></a>

각 개념을 사례를 들어 설명해보겠습니다.

00마을에 쓰레기장을 지을지 말지 의사결정을 해야하는 상황이라고 해보겠습니다. 그렇다면 아까 말씀드린 요소들은 다음과 같이 설명할 수 있습니다.

**Agent**는 00마을에 사는 주민들입니다. 더 다양한 종류의 Agent가 있을 수도 있겠지만 여기서는 주민들로 하겠습니다.

00마을 사람들은 쓰레기장을 지었을 때 내가 느끼는 효용에 대한 정보를 가지고 있습니다. 이것을 **Type**이라고 합니다. 어떤 사람들은 쓰레기장을 지으면 이득이 되어서 선호할 수도 있고, 어떤 사람들은 극도로 싫어할 수도 있습니다. 하지만 이 사람들은 이런 정보를 솔직하게 노출하기 전에 먼저 어떻게 말하는(행동하는) 것이 자신에게 이득이 될지를 따져볼 겁니다.

가능한 사회적 결과의 집합은 ‘쓰레기장을 짓는다’ 혹은 ‘안 짓는다'입니다. 이것이 **Desicion**의 집합입니다. 물론 이것도 얼마든지 다양해질 수 있습니다만 여기서는 단순하게 가겠습니다.

그렇다면 쓰레기장에 대한 각기 다른 선호(type)을 가진 agent들이 실제 ‘쓰레기장이 지어진 결정'에 대해서 얻는 순효용이 있을 것입니다. 쓰레기장에 대한 자신의 효용과 자신이 쓰레기장 건설에 대해 부담해야하는 비용을 뺀 것, **Utility function**입니다.

![1\*zBskdMxiS_WpAm381Rfw2Q.png](/Users/bumgeunsong/coding/writing-archiver/archiver/brunch_md/bumgeunsong-63/assets/55dadd14de5ccae0ad9de530b110f1dc4def770f.png)

또 마을 주민들의 선호를 어떤 방식으로 반영해서 지을지 말지를 결정하는 규칙이 있을 겁니다. 예를 들면 단순히 찬성/반대 투표를 통해 다수결을 한다거나, 각 Agent의 총 효용을 측정하고 그것이 비용보다 크면 짓는다와 같은 의사결정 규칙이 있어야 합니다. 이것을 **Decision function**이라고 합니다.

쓰레기장이 지어졌다고 가정했을 때, 특정 Agent는 돈을 내고, 특정 Agent는 돈을 받는 규칙을 만들 수 있습니다. 예를 들면 ‘쓰레기장 건설에 찬성한 사람들은 n원을 반대한 사람들에게 준다'가 있습니다. 이 규칙을 **Transfer function**이라고 합니다. Transfer function은 각 주체들의 최종 Utility에 영향을 주기 때문에 상당히 중요합니다.

이 Decision function과 Transfer function을 합쳐서 **Social choice function**이라고 합니다.

**Mechanism**은 크게 **설계자가 결정할 수 있는 Social choice function**과 **설계자가 통제할 수 없는 각 Agent들의 전략**으로 나누어지게 됩니다.

![1\*cwerH3_Fp-G3Pw2bK80FKw.png](/Users/bumgeunsong/coding/writing-archiver/archiver/brunch_md/bumgeunsong-63/assets/897a1dce9494df482f533210ce1cff00b92cf67c.png)

메커니즘 디자이너의 무기,

Decision function과 Transfer function

앞서 말씀드린 개념 중 가장 중요한 것은 바로 **Decision function과 Transfer function**입니다. 설계자는 각 Agent의 type(선호)를 알 수 없습니다. 하지만 이 결정규칙과 보상/처벌에 대한 규칙은 설정할 수 있습니다. 이를 이용해 원하는 결과를 이끌어내야 합니다.

**결정 규칙 (Decision function)**

Decision function은 사회적 결정을 내리는 규칙입니다. 굉장히 다양한 방식으로 설정할 수 있습니다. 쓰레기장 건설 메커니즘에서 2가지 예를 들어보겠습니다.

**1. 쓰레기장을 지을 때, 주민들에게 1인 1표를 주고 다수결에 의해서 결정한다.**

단순한 규칙입니다. 하지만 어떤 경우에는 소수의 사람들이 굉장히 큰 가치를 느끼고, 다수의 사람들은 미미한 ‘비선호’를 가지고 있을 수도 있습니다. 단순이 다수가 반대했다고 해서 짓지 않는다면 사회적 효용을 최대화하지 못할 수 있습니다.

**2. 주민들에게 각자 쓰레기장에 대해서 느끼는 가치(type)을 물어보고, type의 총합이 쓰레기장을 짓는 비용보다 크면 짓는다.**

1번 규칙보다 조금 더 발전되었습니다. 각 주체들이 찬성/반대가 아닌 자신의 가치를 이야기하고 그 총합이 비용보다 크면 짓는 방식입니다. 소수의 열렬한 찬성자가 있다면 반대자가 많아도 짓는 결정을 할 수 있습니다.

보상/처벌 규칙 (Transfer function)

Transfer function은 Agent의 행동에 따라서 받거나 내야하는 돈에 대한 규칙을 말합니다. 왜 Transfer function이라는 게 있을까요? 단순히 Decision function만 가지고는 각 주체들에게서 원하는 행동을 이끌어낼 수 없기 때문입니다.

예를 들어 Decision function이 앞서 언급한 2번으로 설정되어있다고 생각해봅시다. 5명의 Agent들이 존재하고 각 Agent의 Benefit과 Cost는 다음과 같은 상황입니다.

![1\*soJSy5Sgocy373FWC72R3A.png](/Users/bumgeunsong/coding/writing-archiver/archiver/brunch_md/bumgeunsong-63/assets/c5354a4e39c99bdcb24ecb9f8057a9dfdd810ec9.png)

여러분이 Benefit이 20인 Agent라고 생각해봅시다. 이 Agent는 ‘지어졌을 때' 순효용이 양수이기 때문에 쓰레기장이 지어지기를 원합니다.

쓰레기장이 지어지도록 하는 가장 쉬운 방법은 자신의 type을 과대보고하는 것입니다. 즉, 진짜로 느끼는 선호는 20이지만 200이라고 말하면 됩니다. 그러면 20이라고 말했을 때는 지어지지 않았을 쓰레기장이 지어지게 됩니다. 다른 사람들의 비선호를 모두 상쇄하고도 남기 때문이죠.

항상 각 개인들이 자신의 이득을 위해 거짓을 말할 수 있다고 가정해야 합니다. 이것을 방지하기 위해서 Transfer function을 추가해보겠습니다. Decision Function은 그대로 유지하되, 자신이 보고한 type에 근거하여 순효용이 양수이면 세금을 걷고, 그 세금을 순효용이 음수인 사람에게 보조금을 준다고 합시다.

이 경우 자신의 benefit이 20인데 200이라고 과대보고하면 그만큼의 세금을 내게 됩니다. 따라서 과대보고할 유인을 없앨 수 있습니다. Transfer function을 통해 정직하게 자신의 type을 보고하도록 유도하는 것입니다.

요약하자면, 메커니즘 설계자는 Decision function과 Transfer function이라는 2가지에 대한 결정 권한이 있고 이를 활용해서 사회적으로 더 나은 결과를 이끌어내게 됩니다.

‘좋은 메커니즘’의 조건

그렇다면 더 나은 결과, 더 나은 메커니즘이란 무엇일까요? 메커니즘 디자인을 연구하는 경제학자들은 다양한 관점에서 좋은 메커니즘의 조건을 정의합니다. 몇 가지 중요한 조건만 설명해보겠습니다.

**Efficiency**

메커니즘이 모든 agent의 효용의 합을 극대화시키는 선택을 하도록 만드는 경우

**Truthfulness**

모든 agent의 균형 전략이 정직하게 자신의 Type을 보고하는 것일때 (즉, 모든 agent가 거짓말을 할 유인이 없을 때)

**Budget Balanced**

Agent의 type이 바뀌더라도 메커니즘이 transfer function으로 얻는 수입이 일정할 때 (또는 항상 0 이상일 때; weak budget balanced)

**(Interim) Individual Rationality**

어떤 agent도 메커니즘에 참여했을 때 (평균적으로) 잃는 것이 없는 경우 (즉, agent들이 메커니즘에 참여할 유인이 있을 때)

**Tractability**

메커니즘의 결과를 다항 시간(polynomial) 내에 연산할 수 있을 때

여기까지 메커니즘 디자인의 기본 개념을 배워보았습니다. 이 내용은 설명을 위해 많은 단순화를 거치고 수학적인 표현들을 배제했기 때문에 조금 더 깊게 알고 싶으신 분은 다음의 링크를 참고해주세요.

Jackson, M. Mechanism theory <a href="https://web.stanford.edu/~jacksonm/mechtheo.pdf" class="link" target="_blank"></a>

(Coursera 강의) Advanced Game theory <a href="https://www.coursera.org/learn/game-theory-2/" class="link" target="_blank"></a>

Eric Maskin. Serious science — Mechanism design theory <a href="https://www.youtube.com/watch?v=Y645BrYSi74" class="link" target="_blank"></a>

(참고로 메커니즘 디자인을 깊게 들어가면 상당히 어렵습니다. Decon도 계속해서 내부 스터디를 통해 메커니즘 디자인 이론을 배워나가는 중입니다.)

**최적화 문제로 푸는 메커니즘 디자인**

여태까지 배운 개념들을 바탕으로 메커니즘 디자인을 최적화 문제로 정의할 수 있습니다.

최적화 문제란 제약 조건(Constraint)를 만족시키면서 목적 함수(objective)를 최대화하는 최적해(Solution)를 찾는 것을 말합니다. 같은 관점에서 메커니즘 설계도 3가지 부분으로 나눌 수 있습니다.

목적 함수(Objective)

목적 함수에는 다음과 같은 것들이 들어갈 수 있습니다.

메커니즘으로 발생하는 사회적 효용의 최대화

각 개인들이 내야하는 총비용의 최소화 (네트워크 상의 최적 경로 찾기)

메커니즘 설계자가 얻는 수입의 극대화 (경매자의 수입을 최대화하는 경매 제도)

제약 조건 (Constraint)

제약 조건에는 ‘좋은 메커니즘의 조건들’이 들어갈 수 있습니다.

각 개인이 이 메커니즘에 참여했을 때 얻는 효용의 기대값이 비용보다 커야 한다. (Individual Rationality)

메커니즘을 실행함으로써 얻는 수익이 0 이상이어야 한다 (Weak Budget Balance)

모든 주체가 서로 협력 관계를 유지할 유인이 없어야 한다 (No gain from Collusion)

솔루션 (Solution)

솔루션은 메커니즘 디자이너가 설정할 수 있는 Decision function과 Transfer function이 됩니다. 메커니즘 디자이너에게 주어진 문제는 Constraint를 만족하면서, Objective를 최대화하는 결정 규칙(Decision function)과 보상/처벌 규칙(Transfer function)을 찾는 것입니다.

메커니즘 디자인의 기본 개념과 메커니즘 최적화에 대해 알아보았습니다. 한 글에 나와야 하는 외계어의 총량을 초과한 것 같아서, 이번 글은 여기서 마무리합니다.

2편에서는 메커니즘 최적화의 구체적 예시를 살펴보고, 메커니즘 최적화를 활용해서 실제 토큰 모델 설계 프로세스를 정립해봅니다.
