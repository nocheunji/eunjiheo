# 포트폴리오 사이트

왼쪽 위 이름, 그 아래 작품 목록, 오른쪽 썸네일 그리드 → 클릭하면 사진·영상·텍스트 상세 페이지.
GitHub Pages로 **무료** 배포됩니다. DB나 서버는 없어요.

---

## 처음 한 번만: 배포 설정 (15분)

1. **GitHub 가입** → 오른쪽 위 `+` → **New repository**
   - 이름: `내아이디.github.io` 로 하면 주소가 `https://내아이디.github.io` 가 돼요
     (다른 이름이면 `https://내아이디.github.io/저장소이름`)
   - **Public** 선택 → Create repository
2. 만들어진 저장소 화면에서 **uploading an existing file** 클릭 →
   이 폴더 안의 모든 파일·폴더를 끌어다 놓기 → **Commit changes**
   - `.github` 폴더처럼 점(.)으로 시작하는 폴더가 안 보이면: 맥은 Finder에서 `Cmd + Shift + .`, 윈도우는 탐색기 `보기 → 숨긴 항목` 체크
3. 저장소의 **Settings → Pages → Build and deployment → Source** 를 **GitHub Actions** 로 변경
4. **Actions** 탭에서 초록색 체크가 뜨면 완료 (1~2분). 주소로 접속해 보세요.
5. `site.md`(이름·이메일)와 `pages/about.md`(소개글)를 열어 연필 아이콘으로 고치고 Commit → 자동 반영

> 개인 도메인(예: `yourname.com`)은 나중에 Settings → Pages → Custom domain 에서 연결할 수 있어요. 도메인 구입비만 들어요.

---

## 작품 올리기 — 방법 1: AI에게 맡기기 (추천)

Claude 데스크톱 앱, Claude Code, Cursor 처럼 **내 컴퓨터 폴더를 열 수 있는 AI**를 쓰면 돼요.

1. 저장소를 내 컴퓨터로 받기 (GitHub Desktop 앱 → Clone repository 가 제일 쉬워요)
2. `_inbox/` 안에 작품 폴더를 만들고 사진·영상 + `메모.txt` (아무렇게나 적은 설명) 넣기
3. AI에게 이 폴더를 열어주고 **"_inbox에 있는 작품 등록해줘"**
4. AI가 파일 이름 정리, 사진 용량 줄이기, 설명 페이지 작성까지 하고 GitHub에 올려줘요

AI가 따라야 할 규칙은 `AGENTS.md` 에 다 적혀 있어서, 매번 설명할 필요가 없어요.

## 작품 올리기 — 방법 2: 직접 (github.com 웹에서)

1. 저장소에서 `works` 폴더 → **Add file → Upload files**
2. 파일 이름 입력칸에 `works/새작품-이름/` 처럼 적으면 새 폴더가 생겨요. 사진·영상 업로드
3. 같은 폴더에 **Add file → Create new file** → 이름 `info.md`, 내용은 아래처럼:

```
---
title: 작품 제목
category: 3D Graphics
year: 2026
date: 2026-10
---
작품 소개 한두 줄.

01.jpg

youtube: https://youtu.be/영상주소

02.jpg

Direction 내이름
```

빈 줄로 나눈 덩어리 하나가 화면의 한 칸이에요. 파일 이름만 쓰면 사진/영상, 나머지는 글.
자세한 규칙은 `AGENTS.md` 의 "info.md 형식" 참고.

---

## 알아두면 좋은 것

- **영상**: 50MB 넘는 영상은 유튜브나 비메오에 '일부 공개'로 올리고 주소만 적으세요. 페이지 안에서 바로 재생돼요.
  짧은 반복 클립은 `loop: clip.mp4` 로 쓰면 소리 없이 자동 반복돼요.
- **사진**: 한 장에 1~2MB 이하가 적당해요. 저장소 전체는 1GB 이하로 유지하는 게 좋아요.
- **순서**: 기본은 `date` 최신순. 맨 앞에 두고 싶으면 `order: 1`.
- **숨기기**: `hidden: true` 한 줄 추가.
- **디자인**: `assets/style.css` 맨 위 `:root` 의 색·글꼴·간격 숫자만 바꿔도 분위기가 바뀌어요.
- **새 페이지**: `pages/contact.md` 처럼 파일 하나 만들면 `/contact/` 페이지가 생기고 왼쪽 목록에 나와요.
- **샘플 지우기**: `works/sample-...` 폴더 3개는 예시라서 지워도 돼요.
- **내 컴퓨터에서 미리보기**: `python build.py --serve` (맥은 `python3`) → http://localhost:8000
