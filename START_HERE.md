# START HERE — 처음 시작하는 사람과 AI를 위한 안내

> **사람이 할 일:** ChatGPT(또는 Gemini) 새 대화를 열고, 이 파일(`START_HERE.md`)과 `AGENTS.md`를 첨부한 다음 아래 문장을 그대로 보내세요.
>
> ```
> 첨부한 START_HERE.md 를 끝까지 읽고, "AI에게" 규칙대로 나를 도와줘.
> 지금 상태: GitHub 가입과 빈 저장소 생성까지 했어. 저장소 주소는 (여기에 주소) 야.
> 1단계부터 하나씩 안내해줘.
> ```

---

## AI에게 (먼저 읽어주세요)

### 이 프로젝트
- 영상·모션·3D·사진 작업을 보여주는 **개인 포트폴리오 정적 사이트**예요.
- `.md` 텍스트 파일과 이미지만으로 관리하고, `build.py`(파이썬 표준 라이브러리만 사용)가 HTML을 만들어요.
- **GitHub Pages로 무료 배포**해요. `main` 브랜치에 파일이 올라오면 `.github/workflows/deploy.yml`이
  GitHub 서버에서 자동으로 `python3 build.py`를 실행하고 배포해요. **사용자 컴퓨터에 파이썬이나 git을 설치할 필요가 없어요.**

### 지금 상황
- 사용자는 코드를 모르는 사람이고, **웹 브라우저(github.com)만** 사용해요. 터미널·git 명령어는 쓰지 않아요.
- 너(AI)는 사용자의 컴퓨터나 GitHub에 직접 접근할 수 없어요. **사용자가 클릭할 위치를 정확히 알려주고, 결과를 확인받으며** 진행해 주세요.
- GitHub 가입과 **빈 저장소 생성까지 끝난 상태**예요. 사이트 파일 폴더는 사용자 컴퓨터에 있어요.

### 꼭 지킬 규칙
1. 한국어로, 쉬운 말로. **한 번에 한 단계씩** 안내하고, 사용자가 "됐어"라고 하면 다음 단계로 가요.
2. 이 문서의 방법(GitHub Actions 배포)만 사용하세요. Jekyll, "Deploy from a branch", Vercel, Netlify, React 같은 **다른 방식으로 바꾸자고 하지 마세요.**
3. `build.py`, `assets/`, `.github/`의 코드는 사용자가 요청하지 않으면 고치지 마세요.
4. 사용자가 알려주지 않은 사실(클라이언트, 날짜, 역할 등)은 지어내지 말고 물어보세요.
5. 문제가 생기면 추측하지 말고, 화면에 보이는 오류 문구나 스크린샷을 보내 달라고 하세요.
6. 작품 등록·수정의 자세한 규칙은 `AGENTS.md`에 있어요. 단, 거기 나오는 "파일 직접 열기, 사진 크기 줄이기, `build.py` 실행, commit/push" 같은 일은
   너가 직접 할 수 없으니 **사용자가 웹에서 할 수 있는 방법으로 바꿔서** 안내하세요 (아래 "작품 추가하기" 참고).

---

## 파일 구조 (요약)

```
site.md                 사이트 설정: 이름, 설명, instagram, email, url
pages/about.md          About 페이지 (pages/ 안의 .md 파일 하나 = 페이지 하나)
works/<폴더>/info.md     작품 하나 = 폴더 하나 (info.md + 사진·영상)
assets/style.css        디자인 (맨 위 :root 값으로 색·글꼴·간격 조정)
build.py                사이트 생성기 (건드리지 않음)
.github/workflows/deploy.yml   자동 배포 설정 (건드리지 않음)
AGENTS.md               작품 등록·수정 상세 규칙
_site/                  ← 미리보기용으로 만들어진 결과물. 업로드하지 않음
_inbox/                 ← 새 작품 재료 임시 보관함. 업로드하지 않음 (README.md는 올려도 됨)
```

---

## 배포 순서

### 1단계 — 저장소 확인
- 저장소가 **Public**인지 확인해요. (무료 계정은 Public이어야 Pages를 쓸 수 있어요)
  저장소 → Settings → 맨 아래 Danger Zone → "Change repository visibility"에서 확인.
- 저장소 이름이 `아이디.github.io`면 사이트 주소는 `https://아이디.github.io`,
  다른 이름(예: `portfolio`)이면 `https://아이디.github.io/portfolio` 가 돼요. 둘 다 정상 동작해요.

### 2단계 — 파일 업로드
1. 저장소 첫 화면에서 **"uploading an existing file"** 링크(또는 **Add file → Upload files**)를 눌러요.
2. 컴퓨터에서 사이트 폴더를 **열고, 그 안에 있는 파일·폴더들을** 선택해서 끌어다 놓아요.
   - ⚠️ 바깥 폴더 자체를 끌어다 놓으면 안 돼요. 저장소 맨 위에 `build.py`, `site.md`가 바로 보여야 해요.
   - ⚠️ `_site` 폴더는 **빼고** 올려요. (`_inbox` 폴더도 README.md 말고 다른 파일이 있으면 빼요)
   - ⚠️ `.github` 폴더가 꼭 포함돼야 해요. 안 보이면 윈도우 탐색기 **보기 → 표시 → 숨긴 항목** 체크, 맥은 Finder에서 `Cmd + Shift + .`
   - Chrome이나 Edge 브라우저를 권장해요 (폴더째 끌어다 놓기가 잘 돼요).
3. 아래 **Commit changes** 버튼을 눌러요.
4. 확인: 저장소 첫 화면에 `.github`, `assets`, `pages`, `works`, `build.py`, `site.md` 등이 보이면 성공.
   - `.github` 폴더가 안 보이면 → 아래 "문제 해결 A" 참고.

### 3단계 — GitHub Pages 켜기 (제일 중요)
1. 저장소 → **Settings → Pages** (왼쪽 메뉴)
2. **Build and deployment → Source** 를 **GitHub Actions** 로 바꿔요.
   (기본값인 "Deploy from a branch"로 두면 안 돼요)

### 4단계 — 배포 확인
1. 저장소 위쪽 **Actions** 탭 → "Deploy portfolio" 작업을 봐요.
   - 초록 체크 ✅ 면 완료 (보통 1~2분).
   - 빨간 X ❌ 면: 2단계 업로드가 3단계보다 먼저라서 실패한 경우가 많아요.
     **Deploy portfolio** 클릭 → 오른쪽 **Run workflow** → **Run workflow** 를 눌러 다시 실행해요.
2. Settings → Pages 화면 위쪽에 나오는 주소(`https://...github.io/...`)로 접속해요.

### 5단계 — 기본 정보 바꾸기
지금은 예시 값이 들어 있어요. 저장소에서 파일을 열고 오른쪽 위 **연필 아이콘(Edit)** → 수정 → **Commit changes**.
수정할 때마다 1~2분 뒤 사이트에 자동 반영돼요.
- `site.md`: `name`(이름), `description`, `instagram`(아이디만), `email`,
  `url`(4단계의 사이트 주소. 예: `https://아이디.github.io` — 링크 공유 미리보기 이미지에 쓰여요)
- `pages/about.md`: 소개글
- `works/sample-...` 예시 작품 3개는 실제 작품을 올린 뒤 지워요 (폴더 안 파일을 열고 ··· 메뉴 → Delete file).

---

## 작품 추가하기 (웹에서)

AI는 `info.md` 내용을 써주고, 사용자는 파일을 올려요.

1. **사용자 준비:** 사진·영상 파일 이름을 영문 소문자로 바꿔요. 예: `thumb.jpg`(목록 썸네일), `01.jpg`, `02.jpg`, `clip-01.mp4`
   - 한글·공백·대문자·특수문자 금지. **대소문자가 다르면 사진이 안 나와요** (`01.JPG` ≠ `01.jpg`).
   - 사진은 한 장 1~2MB 이하 권장 (너무 크면 사진 앱이나 온라인 리사이즈로 긴 변 2400px 정도로 줄이기).
   - 영상이 **50MB 넘으면 올리지 말고** 유튜브/비메오에 '일부 공개'로 올린 뒤 주소만 사용해요.
2. **AI:** 사용자에게 작품 정보(제목, 분류, 연도·월, 소개, 크레딧, 영상 주소)를 물어보고 `info.md` 전체 내용을 써줘요. 형식:
   ```
   ---
   title: 작품 제목
   category: Motion Graphics
   year: 2026
   date: 2026-10
   ---
   작품 소개 1~3문장. 짧고 담백하게.

   youtube: https://youtu.be/영상ID

   01.jpg

   02.jpg

   Client 클라이언트명
   Direction 이름
   ```
   - 빈 줄로 나눈 덩어리 하나 = 화면의 한 칸. 순서: 소개 → 대표 영상 → 사진 → 크레딧
   - 폴더 이름은 제목을 영문 소문자+하이픈으로 (예: `sunroof-2024-promotional-clips`)
   - 그 외 옵션(`order`, `hidden`, `loop:` 등)은 `AGENTS.md`의 "info.md 형식" 참고
3. **사용자 업로드:**
   - 먼저 새 폴더와 `info.md` 만들기: 저장소에서 **Add file → Create new file** → 이름칸에 `works/폴더이름/info.md` 입력
     (슬래시를 치면 폴더가 생겨요) → AI가 써준 내용 붙여넣기 → **Commit changes**
   - 그다음 `works/폴더이름/` 으로 들어가서 **Add file → Upload files** 로 사진·영상을 올리고 **Commit changes**
4. Actions 탭에서 ✅ 확인 후 사이트에서 확인.

### 자주 하는 수정
- 순서를 맨 앞으로: 해당 `info.md` 위쪽 정보에 `order: 1` 추가 (없으면 `date` 최신순)
- 작품 숨기기: `hidden: true` 추가 (지우는 것보다 이걸 먼저 권해요)
- 새 페이지(Contact, CV 등): `pages/contact.md` 파일 생성, 위쪽에 `title`과 `order`(목록 순서)
- 색·글꼴: `assets/style.css` 맨 위 `:root` 의 값만 바꿔요

---

## 문제 해결

**A. `.github` 폴더가 업로드되지 않았어요**
Add file → Create new file → 이름칸에 `.github/workflows/deploy.yml` 입력 (슬래시를 치면 폴더가 생겨요) →
사이트 폴더 안의 같은 파일을 메모장으로 열어 내용 전체를 복사해 붙여넣기 → Commit changes.

**B. 사이트 주소가 404예요**
- Settings → Pages의 Source가 **GitHub Actions**인지 확인
- Actions 탭이 ✅ 인지 확인. 방금 배포했다면 1~2분 기다린 뒤 새로고침

**C. Actions가 ❌ 예요**
- 실패한 작업 클릭 → 빨간 단계를 펼쳐서 오류 문구를 AI에게 보여주세요.
- "Get Pages site failed" / "Not Found" 류 → 3단계(Source = GitHub Actions)를 하고 Run workflow로 재실행

**D. 사진이 안 나와요 / 깨진 그림이 보여요**
- `info.md`에 적은 파일 이름과 실제 파일 이름이 **대소문자까지** 똑같은지 확인
- 사진이 그 작품 폴더(`works/폴더이름/`) 안에 있는지 확인

**E. 디자인(글꼴·배치)이 다 깨져 보여요**
- `assets` 폴더가 저장소 맨 위에 있는지 확인 (바깥 폴더째 올리면 이렇게 돼요 → 2단계 다시)
