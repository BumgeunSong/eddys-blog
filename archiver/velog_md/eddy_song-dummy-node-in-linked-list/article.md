---
title: Linked list 추가, 삭제를 구현할 때 유용한 Dummy Node
published_date: 2022-01-11 14:35
tags: algorithm, data structure
meta_description: 연결 리스트(Linked list) 알고리즘을 구현할 때 유용한 간단한 트릭을 소개한다.
meta_image: https://images.velog.io/images/eddy_song/post/0cc91ef9-fd8f-4ffd-b545-2ebb4b8fe3d1/dummy.png
lang: ko
---

# Linked list 추가, 삭제를 구현할 때 유용한 Dummy Node

*by eddy_song*

연결 리스트(Linked list) 알고리즘을 구현할 때 유용한 간단한 트릭을 소개한다.

## 연결 리스트(Linked list)

연결 리스트(Linked List)는 데이터와, 포인터를 가지는 노드를 연결한 형태의 자료 구조다.
연결 리스트는 배열(Array)에 비해서 삽입과 삭제가 빠르다는 게 장점이다.

> 연결 리스트는 2가지 종류가 있다.
> 다음을 가리키는 포인터 하나만 가지는 단일 연결 리스트(Singly linked list).
> 각각 이전과 다음을 가리키는 포인터 2개를 가지는 이중 연결 리스트(Doubly linked list).
> 여기서는 단일 연결 리스트를 설명한다.

![singly-linked-list](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-dummy-node-in-linked-list/assets/6087a5df1b896186f45c69a9e5facff89f5f32bd.png)

## 연결 리스트의 노드를 삭제하는 알고리즘

연결 리스트의 '삽입'과 '삭제'를 구현하다보면 번거로운 경우가 생긴다.

예를 들어, 이런 알고리즘을 구현한다고 해보자.

> Linked list의 Head가 주어진다.
> `value`라는 인자가 주어진다.
> Linked list에서 `value`와 같은 값을 가진 노드를 삭제한다.
> Linked list를 반환한다.

이 알고리즘을 구현하는 건 어렵지 않다. `pointer` 를 head로 설정한다. `pointer.next` 노드의 값을 확인한다.
만약 값이 `value`와 같다면, `pointer.next`를 `pointer.next.next`에 할당한다.
원래 있던 `pointer.next`가 사라진다.

``` swift
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     public var val: Int
 *     public var next: ListNode?
 *     public init() { self.val = 0; self.next = nil; }
 *     public init(_ val: Int) { self.val = val; self.next = nil; }
 *     public init(_ val: Int, _ next: ListNode?) { self.val = val; self.next = next; }
 * }
 */

func delete(_ head: ListNode?, _ value: Int) -> ListNode? {
  var pointer = head

  while pointer?.next != nil {
    if pointer?.next?.val == value {
      pointer?.next = pointer?.next?.next
      break
    }
    pointer = pointer?.next
  }

  return head
}
```

## Head를 삭제하거나 추가하게 될 때

그러나 위의 알고리즘에는 문제가 있다.

만약 head가 `value`와 같은 값을 가진 노드라면?

당연히 head를 삭제해야 한다. 하지만 head는 `pointer.next`에 해당하지 않는다.
**head를 삭제하려면, 별도의 조건문으로 처리를 해줘야 한다.**

아마 이런 식으로 해결할 수 있을 것이다.

``` swift
func delete(_ head: ListNode?, _ value: Int) -> ListNode? {
  var pointer = head

  // head를 삭제해야 할 때
  if head?.val == value {
    head = head?.next
  }

  while pointer?.next != nil {
    if pointer?.next?.val == value {
      pointer?.next = pointer?.next?.next
      break
    }
    pointer = pointer?.next
  }

  return head
}
```

이건 새로운 노드를 추가할 때도 마찬가지다.
새로 추가할 노드가 head 자리에 와야한다면, 똑같이 조건문으로 예외 처리를 해줘야 한다.

노드의 추가/삭제를 포함하는 알고리즘은 굉장히 많을 수 있다.
**그때마다 head를 다루는 조건문을 써줘야 한다는 건 다소 번거롭다.**

## Dummy Node를 head로 설정하기

이 때 코드를 간단하게 만들 수 있는 트릭이 있다.
Dummy Node를 사용하면, head를 다루는 조건문을 쓰지 않아도 된다.

``` swift
func delete(_ head: ListNode?, _ value: Int) -> ListNode? {

  // dummy node를 생성하고 head에 연결한다.
  let dummy = ListNode(0, head)
  var pointer = dummy

  while pointer?.next != nil {
    if pointer?.next?.val == value {
      pointer?.next = pointer?.next?.next
      break
    }
    pointer = pointer?.next
  }

  return dummy.next
}
```

먼저, dummy node를 하나 만든다. 말 그대로 잠깐 자리만 맡아줄 가짜 데이터다.
그리고 **`dummy`의 포인터(`next`)가 head를 가리키게 한다.**

이제 `pointer`를 `dummy`에 두고 연결 리스트를 탐색한다.

![dummy](/Users/bumgeunsong/coding/writing-archiver/archiver/velog_md/eddy_song-dummy-node-in-linked-list/assets/43e30cdd43fe19181a842048a19415f92b3153e7.png)

`dummy`로 head를 만들어줬기 때문에, 진짜 head는 맨 앞이 아닌 중간 노드처럼 다룰 수 있다.
따라서 별도의 조건문을 만들지 않고, 중간 노드를 삭제/삽입하는 알고리즘을 똑같이 적용한다.

조작을 끝낸 이후에는 **head 대신, `dummy.next`를 반환한다.**
이렇게 하면 dummy node는 사라지고, dummy의 포인터가 가리키는 곳, 즉 **원래의 head를 반환**하다.
