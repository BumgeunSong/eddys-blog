---
title: Collection View 비동기 로딩 에러 해결하기
tags: iOS, swift
meta_description: 콜렉션 뷰 안의 데이터를 독립적으로 reload하도록 만들면서 겪었던 삽질의 기록.
meta_image: https://velog.velcdn.com/images/eddy_song/post/c68f2d9f-01b6-46cd-be05-e028aaabeef0/image.png
lang: ko
---

# Collection View 비동기 로딩 에러 해결하기

*by eddy_song*

이번에 콜렉션 뷰로 프로젝트를 하면서 삽질했던 기록을 남기려고 한다. 예상하지 못한 문제들이 연속으로 터고, 그때마다 디버깅을 해야하는 영역? 접근법도 달라서 정말 골치가 아팠다.

하지만 지나고 보니 배운 게 많다. 의미있는 삽질이었다. 게다가 앞으로도 콜렉션 뷰(Collection view)의 비동기 로딩은 분명 써먹을 일이 많을테니.

정리가 깔끔하진 않지만, 기록 삼아 남겨둔다.

# 배경 설명

- 다양한 제품(음식)을 콜렉션 뷰로 보여주는 앱이다. 각각의 제품은 메인, 국물, 반찬이라는 카테고리(섹션)로 나뉘어져있다.
- 서버에 네트워크 요청을 보내서 제품의 데이터를 받아와야 한다.
- 그런데 API를 보면 전체 제품 데이터를 요청하는 게 아니라, 각 카테고리별로 데이터를 요청할 수 있도록 되어있다.
- 즉, API 요청을 따로 3번 해야 한다.
- 그 후 데이터 응답을 받아서 디코딩한 뒤에, 콜렉션 뷰의 데이터 소스 역할을 하는 ViewModel에 저장한다.
- ViewModel이 업데이트되면, View(Controller)는 콜렉션 뷰를 reload해서 데이터를 채워 그린다.

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-collection-view-reload/assets/cf12aa6711f365df2ea63cda2d86f97913408a23.png)

# 문제 1: 데이터 도착 완료 시점

- 처음에는 각 섹션의 데이터를 `CategorySectionViewModel`로 추상화했고, 이 데이터를 상위 뷰 모델에서 `Array<CategorySectionViewModel>`로 갖고 있도록 만들었다.
- 3개 섹션에 대한 데이터 응답이 모두 독립적으로 오게 된다.
- 따라서 어떤 데이터가 마지막에 도착하는지 알 수 없다.
- Collection View에서 언제 데이터를 reload 하게 해줘야할지가 애매했다.
- 각 데이터가 도착할 때마다 reload하는 건 무조건 3번 실행되기 때문에 비효율적이었다.

# 해결: Dispatch Group

- 여러 비동기 요청의 완료 시점을 알고, 그 뒤에 작업을 호출해야하는 상황이었다.
- 이럴 때 쓸 수 있는 게 바로 GCD의 `DispatchGroup`이다.

### Dispatch Group

- DispatchGroup을 쓰면 여러 비동기 작업을 묶어서 모니터링하고, 하나로 묶어서 관리할 수 있다.
- 더 쉽게 말하면, 여러가지 비동기 작업을 묶고, 모두 완료되는 시점에 특정 작업을 실행할 수 있게 해준다.
- 이 때 비동기 작업 안에 또 비동기 작업이 있다면, 그 작업의 완료를 알기 위해서 `enter()`와 `leave()`를 사용한다.
- enter가 실행된 만큼, leave가 실행되면 모든 작업이 완료된 것으로 본다.
- 이 때 `notify()`를 사용해서 완료 시 실행할 작업을 지정할 수 있다.

### 실제 코드

- 임시 배열에 CategorySection 데이터를 추가하고, Dispatch group을 사용해 모든 작업이 완료가 되면 콜렉션 뷰에서 reload를 하도록 만들었다.

``` swift
func fetch() {
    var tempStorage = [CategorySectionViewModel]()
    let dispatchGroup = DispatchGroup()

    for type in ProductType.allCases {

        // DispatchGroup에 작업 시작을 알린다.
        dispatchGroup.enter()

        categoryManager.fetchCategory(of: type) { category in
            let productCellVMs = category.product.compactMap { product in
                // productCellVM을 만든다.
            }
            // productCellVM을 배열로 가진 CategorySectionViewModel을 만든다.
            let categorySectionVM = CategorySectionViewModel(type: .main, productVM: productCellVMs)

            // 임시 저장소에 추가한다.
            tempStorage.append(categorySectionVM)

            // DispatchGroup에 작업 완료를 알린다.
            dispatchGroup.leave()
        }
    }
    // 모든 작업이 끝나면 oberverable에 데이터를 업데이트한다.
    // 즉, collection view reload를 실행시킨다.
    dispatchGroup.notify(queue: .global(), work: DispatchWorkItem {
        print("Every section data updated")
        cellViewModels.value = temp
    })
}
```

# 문제 2: 섹션별 독립적인 로딩

- 이렇게까지 하고 문제를 해결한 줄 알았다.
- 하지만 생각해보니 지금은 비동기적으로 네트워크 요청을 해놓고, 모든 네트워크 요청이 완료될 때까지 기다렸린다. 모든 데이터가 도착하면, 그 다음 UI 업데이트를 하고 있다.
- 그런데 '동시성'을 제대로 만족시키려면, 각 요청의 응답이 도착할 때마다 바로바로 UI 업데이트를 해서 사용자한테 보여줘야하지 않을까?
- 어느 한 섹션 데이터가 늦게 도착하더라도, 다른 데이터들은 사용자에게 보여질 수 있어야 한다.
- 그런데 하나의 콜렉션 뷰 안에 있는 데이터들을 어떻게 독립적으로 업데이트할 수 있지?
- 콜렉션 뷰를 업데이트하려면 `reloadData()`로 완전히 새로고침하는 수밖에 없는...

# 해결: reloadSection()

- ...줄 알았는데 아니었다.
- UICollectionView에는 지정한 섹션만 업데이트할 수 있도록 [reloadSection](https://developer.apple.com/documentation/uikit/uicollectionview/1618092-reloadsections)이라는 메서드가 있다.

``` swift
func reloadSections(_ sections: IndexSet)
```

- reloadSection을 사용해서 메인 요리, 반찬 요리, 국물 요리를 따로 따로 업데이트하도록 바꿨다.
- 각 섹션별 ViewModel을 나누고, 각 ViewModel에 지정된 섹션만 업데이트하는 reloadSection을 바인딩해주었다.

``` swift
CategoryType.allCases.forEach({ type in
    guard let categoryVM = viewModel.categoryVMs[type] else {return}

    categoryVM.bind { _ in
        DispatchQueue.main.async {
            self.mainCollectionView.reloadSections(IndexSet(integer: type.index))
        }
    }
})
```

# 문제 3: 밀림 현상

- 이제 모든 섹션이 독립적으로 업데이트된다.
- 하지만 앱을 실행시켜보니, 또다른 부자연스러운 현상이 일어난다.
- 3가지 섹션의 헤더가 화면에 한번 뜨고, 그 후에 시간차를 두고 셀이 로딩되면서 헤더가 아래로 쭉 밀리는 현상이 일어났다. 그 변화가 상당히 커서 눈에 거슬렸다.
- 왜 이런 일이 일어나지? 생각해봤다.
- 일단 콜렉션 뷰는 맨 처음에 전체 데이터를 한번 업데이트한다. 이 때 헤더는 네트워크가 아닌 사전에 지정된 텍스트이기 때문에 바로 로딩된다.
- 그 후 제품 데이터가 도착하면 섹션을 로딩한다. 이 과정에서 섹션 갯수가 늘어나기 때문에 추가되면서 2번째 3번째 헤더는 애니메이션과 함께 쭉- 내려가게 된다.

# 해결: Placeholder Cell

- 이 문제를 해결하기 위해서는 초기 로딩 시에 화면에 어느 정도 셀이 채워져있어야 했다.
- 그래야 셀이 업데이트되더라도 과도한 밀림 현상이 발생하지 않는다.
- 임시 이미지와 타이틀을 가진 placeholder를 만들어서 넣어주었다.
- 초반에는 이 placeholder 셀이 잠깐 등장하다가 데이터가 업데이트되면 바뀐다.
- 훨씬 더 자연스러워졌다!

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-collection-view-reload/assets/a830cf6aee766c5ca24b47f4cebe27bcc1530d66.gif)

# 문제 4: Invalid update 에러

- 하지만 아직 산은 끝나지 않았다.
- 실행은 잘 되긴 했지만, 그 때마다 다음과 같은 에러가 등장했다.

``` null
[UICollectionView] Performing reloadData as a fallback

Invalid update: invalid number of items in section 0.
The number of items contained in an existing section after the update (8)
must be equal to the number of items contained in that section before the update (5) (...)
```

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-collection-view-reload/assets/37666c84f899652493e0e46a8f0ed19fd9e6853f.jpg)
(뭔 소리야..?)

- 업데이트를 할 때, 현재 있는 셀의 개수와 업데이트할 셀의 개수가 다르다는 에러였다. 그래서 `reloadSection`이 실행되지 않고, fallback으로 `reloadData`가 실행되고 있었다.
- 그치만 당연히 현재 있는 셀 개수와 업데이트는 다른 거 아닌가?
- 미리 서버에서 데이터가 몇개 올지 알고 지정해줄 수는 없잖아??
- 도저히 이해가 안 되어서 구글 검색을 해봐도 비슷한 사례가 잘 나오지 않았다.
- 뷰를 업데이트하는 와중에 다른 스레드에서 데이터가 업데이트되어서 그런 걸까? 아니 그건 의도한 동작인데...

# 해결: Alamofire의 동작 방식

- 마지막 에러 해결은 많은 사람들에게 질문을 하고, 여러가지 가설을 세웠다 폐기하면서 며칠 간 고생을 했다.
- 하지만 해결책은 정말 예상 외의 어이없는 곳에서 등장했으니...

### Alamofire는 응답 처리를 메인 스레드에서 실행시킨다.

- 이 프로젝트에서는 네트워크 요청을 위해 서드파티 라이브러리인 `Alamofire`를 선택해서 쓰고 있었다.
- 즉, 메인 요리, 국물 요리, 반찬 요리 데이터를 최종 요청하고, 그 응답 데이터를 파싱해서 전달해주는 역할은 Alamofire가 맡고 있었다.
- 우리는 네트워크 요청을 하는 거니까, 당연히 Alamofire에 보낸 코드(response handler)는 백그라운드 스레드에서 실행될 거라고 가정하고 있었다. (URLSession의 response handler는 백그라운드에서 실행된다.)
- 하지만 알고보니 Alamofire는 (네트워크 요청은 비동기로 하지만) [response handler를 메인 스레드에서 실행하도록 동작](https://stackoverflow.com/questions/41725511/alamofire-network-calls-not-being-run-in-background-thread)하고 있었다.

### 데이터 업데이트 시점과 UI 업데이트 시점의 불일치

- 나는 'UI 업데이트는 백그라운드에서 실행하면 안되지! ㅎㅎ 그 정도는 나도 안다구' 이러면서, reloadSection 코드를 Main DispatchQueue에 비동기로 요청하고 있었다.

``` swift
CategoryType.allCases.forEach({ type in
    guard let categoryVM = viewModel.categoryVMs[type] else {return}

    categoryVM.bind { _ in
        DispatchQueue.main.async {
            self.mainCollectionView.reloadSections(IndexSet(integer: type.index))
        }
    }
})
```

(아까 나왔던 코드)

- 이미 저 코드는 메인 스레드에서 실행되고 있었는데, 업데이트 작업을 한번더 main.async로 보내고 있었던 거였다.
- 따라서 만약 그전에 이미 메인 큐에 들어가있는 작업이 존재한다면, 데이터 업데이트 후에 바로 UI를 업데이트하는 게 아니었다.
- 데이터 업데이트 - (이미 들어가 있는 작업) - UI 업데이트 순으로 실행이 되고 있었다.
- 이걸 알고난 후, 각각의 실행 시점과 스레드를 찍어보니 다음과 같았다.

``` zsh
✅ Data Updated: side (main thread: true)
✅ Data Updated: main (main thread: true)

▶️ Start Reload Section: side (main thread: true)

2022-05-03 10:39:01.869036+0900 SideDishApp[98453:9502835] [UICollectionView] Performing reloadData as a fallback

— Invalid update: invalid number of items in section 0. The number of items contained in an existing section after the update (8) must be equal to the number of items contained in that section before the update (5), plus or minus the number of items inserted or deleted from that section (0 inserted, 0 deleted) and plus or minus the number of items moved into or out of that section (0 moved in, 0 moved out).

Collection view: <UICollectionView: 0x141039400; frame = (0 91; 390 719); clipsToBounds = YES; autoresize = RM+BM; gestureRecognizers = <NSArray: 0x600002d7f060>; layer = <CALayer: 0x600002398d60>; contentOffset: {0, 0}; contentSize: {390, 1138}; adjustedContentInset: {0, 0, 0, 0}; layout: <UICollectionViewCompositionalLayout: 0x14021abe0>; dataSource: <SideDishApp.MainViewController: 0x13d716b40>>

⏹ End Reload Section: side (main thread: true)

▶️ Start Reload Section: main (main thread: true)
⏹ End Reload Section: main (main thread: true)

✅ Data Updated: soup (main thread: true)

▶️ Start Reload Section: soup (main thread: true)
⏹ End Reload Section: soup (main thread: true)
```

- `side` 데이터가 업데이트 되고난 후, 뷰의 `reload` 가 바로 일어나는 게 아니라, `main` 데이터가 업데이트되고 있다.
- 메인 스레드에서 다시 한번 비동기 호출을 하고 있기 때문에, reload를 실행하지 않고 바로 다음 작업으로 이어진 것이다.
- 그 다음을 보면, `side` 데이터로 뷰를 업데이트하는 시점에 에러가 발생한다.
- '메인 스레드에서 비동기 호출'을 했기 때문에, 데이터 소스의 업데이트와 UI 업데이트 시점이 불일치한다.
- 이것 때문에 계속해서 `reloadSection`이 제대로 실행되지 않았던 거였다!

![](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-collection-view-reload/assets/c16874f9f9784b0752c034b3df70da66ba8b24c7.jpg)

### UI 업데이트를 현재 스레드에서 즉시 실행

- 원인을 알고 나니 문제 해결은 간단했다.
- UI 업데이트 코드에서 `DispatchQueue.main.async` 를 지워주었다.
- 현재 스레드가 어차피 메인 스레드이니까 UI 업데이트여도 문제가 되지 않는다.
- 그러자 다음과 같이 실행되었고 에러 메시지가 사라졌다.

``` zsh
✅ Data Updated: soup (main thread: true)
▶️ Start Reload Section: soup (main thread: true)
⏹ End Reload Section: soup (main thread: true)

✅ Data Updated: side (main thread: true)
▶️ Start Reload Section: side (main thread: true)
⏹ End Reload Section: side (main thread: true)

✅ Data Updated: main (main thread: true)
▶️ Start Reload Section: main (main thread: true)
⏹ End Reload Section: main (main thread: true)
```

- 데이터 업데이트와 UI 업데이트가 순서대로 잘 실행되는 걸 볼 수 있다!
