# 프로젝트 안내 (Claude Code가 먼저 읽는 파일)

작품 등록·수정 규칙은 AGENTS.md에 있습니다 → @AGENTS.md

## 목표
개인 포트폴리오 웹사이트. 영상·모션·3D·사진 작업을 보여주는 용도.
- **비용 0원**: GitHub Pages 무료 배포. 서버·DB·유료 서비스·회원가입이 필요한 외부 서비스는 쓰지 않는다.
- **코드를 몰라도 운영 가능**: 주인은 "폴더에 사진·영상 + 짧은 메모"만 넣고 AI에게 등록을 맡긴다.
  그래서 콘텐츠는 전부 사람이 읽을 수 있는 텍스트 파일(.md)과 이미지 파일로만 관리한다.
- **디자인 방향**: 미니멀한 아티스트/스튜디오 포트폴리오.
  참고 사이트: nayeon-kim.com (Cargo로 만든 것으로 추정 — 왼쪽 위 이름, 그 아래 작품 목록, 오른쪽 썸네일 그리드, 모노스페이스 글꼴, 흰 배경),
  new-year.asia/work (WordPress — 작품 카드에 크레딧 표기).
  작품 이미지가 주인공이고 UI는 최대한 조용하게.

## 내린 결정과 이유
- Vercel + DB(Supabase 등) 방식은 검토 후 제외: 관리할 것이 많고 무료 한도를 신경 써야 함.
- Cargo 등 사이트 빌더는 무료 플랜 제약이 있어 제외.
- Jekyll(GitHub Pages 기본) 대신 **파이썬 표준 라이브러리만 쓰는 build.py**: 추가 설치 없이 윈도우/맥 어디서나 `python build.py`로 돌아가게 하기 위함.
  → **pip 패키지, npm, 프레임워크(React/Next.js 등)를 새로 들이지 말 것.** 꼭 필요하면 먼저 주인에게 이유와 함께 물어볼 것.
- 50MB 넘는 영상은 저장소에 넣지 않고 YouTube/Vimeo 임베드 (GitHub 파일 100MB 제한, 저장소 1GB 권장).
- 모든 링크는 상대 경로 → `아이디.github.io` 와 `아이디.github.io/저장소이름` 둘 다에서 동작해야 한다.

## 구조
```
site.md                 사이트 설정 (이름, 설명, instagram, email, lang, url)
pages/<slug>.md         일반 페이지 → /<slug>/   (about, contact 등. 같은 이름 폴더 pages/<slug>/ 에 이미지)
works/<slug>/info.md    작품 페이지 → /works/<slug>/  (+ 같은 폴더의 사진·영상)
_inbox/                 새 작품 재료 투입구 (git에 안 올라감)
assets/style.css        모든 디자인. 맨 위 :root 변수로 색·글꼴·간격 조정
build.py                .md → HTML 생성기 (_site/ 출력)
.github/workflows/deploy.yml   main에 push → 빌드 → GitHub Pages 배포
```
build.py 흐름: `parse_front_matter` → `render_block`(빈 줄로 나눈 블록 하나를 사진/영상/유튜브/텍스트로 변환)
→ `load_pages`, `load_works` → `page()`(공통 레이아웃: 왼쪽 이름+목록, 오른쪽 main) → `_site/`에 기록.

## 명령어
- 미리보기: `python build.py --serve` → http://localhost:8000 (맥/리눅스는 `python3`)
  - 파일을 고친 뒤엔 Ctrl+C 로 끄고 다시 실행해야 반영됨
- 빌드만: `python build.py` / 경고가 있으면 실패: `python build.py --strict`

## 개발 규칙
- 새 **페이지**(Contact, CV 등) = `pages/<slug>.md` 파일 하나 추가. build.py 수정 불필요.
- 새 **작품** = AGENTS.md 절차.
- 새 **블록 종류**(예: 사진 2장 나란히, 인스타 임베드)가 필요하면 `render_block`에 규칙 추가 + 해당 CSS 추가 + AGENTS.md "info.md 형식"에 사용법 한 줄 추가. 세 가지를 항상 같이 할 것.
- 레이아웃·사이드바 변경은 `page()` 함수, 메인 그리드는 `grid()`.
- 사용자 입력 텍스트는 반드시 `html.escape` / `inline()` 을 거쳐 출력.
- 변경 후에는 `python build.py` 실행해서 경고 없음 확인, 가능하면 데스크톱(1380px)·모바일(390px) 폭에서 가로 스크롤 없는지 확인.
- 주인은 코드를 모를 수 있음: 설명은 한국어, 쉬운 말로. 사용자가 요청한 저장소 변경은 작업 완료 후 commit + `main` push까지 바로 진행하고, 별도 허락을 다시 묻지 않는다. push 후 GitHub Actions가 GitHub Pages에 배포한다.
