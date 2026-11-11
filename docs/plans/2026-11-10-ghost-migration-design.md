# Ghost 이전 설계

작성일: 2026-11-10

## 배경

현재 블로그는 Next.js + Nextra + Keystatic이다. 글 920개가 `content/`에 있다.

해결하려는 문제:

1. Keystatic 에디터가 불편하다. 로컬 모드에서는 목록 로딩에 약 40초가 걸린다.
2. 현재 사이트는 아카이브 중심이다. 메인 블로그를 새로 구성하고 싶다.
3. 앞으로는 글을 시리즈로 쓰고 싶다. 단, 지금은 우선순위가 아니다.
4. 유지보수 공수를 줄이고 싶다. 본업이 아니다.
5. 주 1회 뉴스레터를 운영하고 싶다.

원칙: built-to-last, 그리고 independent. 닫힌 플랫폼에 묶이지 않는다.

## 결정

- 플랫폼: Ghost(Pro) Starter. 월 $18(연간 결제). 내 도메인을 지원한다(공식 가격 페이지 기준).
- 시작 방식: Ghost 기본 테마. 헤드리스는 필요해질 때 판단한다.
- 기존 글 920개: Ghost로 옮기지 않는다. 아카이브에 둔다.
- 시리즈: 지금은 하지 않는다. 시작할 때는 Ghost 태그로 한다. 참고 모델은 evan-moon.github.io. 홈에서는 시리즈 전용 구조가 보이지 않았고, 주제 태그, 인기글, 최신글 중심이었다.

기각한 대안:

- Substack, Beehiiv: 비용은 낮지만 닫힌 서비스다. 독립성이 약하다.
- Ghost 셀프 호스팅: 서버 운영 부담이 생긴다. 나중에 비용이 부담될 때의 탈출구로 남긴다.
- 처음부터 Next.js + Ghost API: 지금은 필요 이상이다.

## 구조

- `www.eddysong.com`: Ghost(Pro). 새 글과 뉴스레터.
- `archive.eddysong.com`: 현재 Nextra 사이트. 읽기 전용.
- 새 글은 Ghost 에디터에서만 쓴다.
- Ghost 내비게이션에 Archive 링크를 둔다.
- 아카이브 상단에 새 블로그 링크와 구독 링크를 둔다.

## 뉴스레터

- Ghost 내장 기능을 쓴다. 글 하나가 웹 게시와 이메일 발송을 겸한다.
- 주 1회 발행. 예약 발행을 쓴다.
- 발신 도메인의 SPF, DKIM은 Ghost 안내에 따라 DNS에 추가한다.
- 구독자는 Ghost 안에서 관리하고, CSV로 내보낼 수 있다.

## 이 레포의 변경

- 사이트 URL을 `archive.eddysong.com`으로 바꾼다. metadataBase, sitemap, robots, 소셜 카드가 대상이다.
- 비공개 그룹 글의 noindex는 유지한다.
- Keystatic을 제거한다. 설정 파일, `/keystatic` 라우트, API 라우트, 의존성, 환경 변수가 대상이다.
- #9의 Keystatic 브랜치 프리뷰를 정리한다.
- 상단에 새 블로그 링크와 구독 링크를 추가한다.

## 전환 순서

1. Ghost 가입(Starter).
2. Vercel에 `archive.eddysong.com`을 추가한다. 레포 변경 PR을 병합한다.
3. Ghost에 첫 글 몇 개를 발행한다. 뉴스레터 발신 DNS를 설정한다.
4. `www.eddysong.com`을 Ghost로 전환한다.
5. 옛 주소를 `archive.eddysong.com`으로 301 리다이렉트한다.

## 리스크

- 리다이렉트: Ghost redirects는 라우트보다 먼저 실행된다. `/(.*)` 전체 규칙을 걸면 새 Ghost 글이 아카이브로 튕긴다. 글 슬러그에서 개별 규칙 920개를 생성한다. 파일 형식은 구현 전에 Ghost 공식 문서로 확인한다.
- SEO: 도메인 전환 중 색인이 흔들릴 수 있다. 301과 sitemap을 `archive.` 기준으로 유지한다.
- 비공개 그룹 글: 전환 후에도 noindex가 유지되는지 확인한다.

## 확인된 것

- Starter는 Custom integration과 API 키를 막는다(HostLimitError). Admin API와 Content API 모두 해당한다. 헤드리스는 Publisher 이상에서만 가능하다.
- Starter에서 내 도메인 연결이 된다. Ghost가 요구하는 DNS는 `www` CNAME(`<site>.ghost.io`)과 apex A 레코드다.
- 도메인 DNS는 GoDaddy에 있다. Vercel 프로젝트 `writing-archiver`가 apex와 `www`를 쓰고 있었다.
- `archive.eddysong.com`은 Vercel에 추가하고 CNAME과 TXT(`_vercel`)로 검증을 마쳤다.

## 미확인

- Ghost 리다이렉트 파일의 정확한 형식과 규칙 수 제한.
- 인용문(`\>`) 20줄이 Ghost 초안에서 일반 문단으로 올라갔다. 그대로 둘지 정한다.
