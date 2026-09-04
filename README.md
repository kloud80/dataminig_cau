# 도시빅데이터와 머신러닝 — 강의안

웹에서 바로 보기 → **https://kloud80.github.io/dataminig_cau/**

브라우저로 열고 `F` 를 누르면 전체화면입니다. 설치할 것은 없습니다.

| 키 | 동작 |
|---|---|
| `←` `→` | 앞/뒤 슬라이드 |
| `O` | 목차 |
| `N` | 발표자 노트 |
| `F` | 전체화면 |
| `B` | 화면 가리기 |
| `?` | 도움말 |
| 숫자 + `Enter` | 해당 쪽으로 이동 |

주소창의 `#12` 로 위치가 유지되므로 새로고침해도 보던 자리에서 이어집니다.

## 구성 — 90슬라이드

| 구간 | 내용 | 쪽 |
|---|---|---|
| 1부 | 데이터 분석 기초 — 평균에서 다중회귀까지 | 1–53 |
| 전환 | statistics → heuristics | 54 |
| 2부 | 기계학습의 역사 — 기대와 겨울, 그리고 돌파 | 55–90 |

## 저장소 구조

```
present.html   발표용 뷰어 (이 파일 하나만 열면 된다)
_ds/           디자인시스템 — 폰트·색·타이포
uploads/       생성·가공한 이미지
assets/        원본 PPTX 에서 추출한 이미지
vendor/        차트 런타임 (React + 마운트 스크립트)
*.dc.html      슬라이드 원본 (single source of truth)
.dcpull/       빌드·검증 스크립트
docs/          자료 분석 및 작업 기록
```

## 고치고 다시 만들기

```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
.venv/Scripts/python -m playwright install chromium

.venv/Scripts/python build_present.py      # *.dc.html -> present.html
.venv/Scripts/python .dcpull/verify_all.py # 90쪽 전체 렌더 검증
.venv/Scripts/python build_pdf.py          # 배포용 PDF
```

슬라이드를 고칠 때는 `present.html` 이 아니라 **`*.dc.html` 을 고치고 다시 빌드**합니다.
자세한 것은 `CLAUDE.md`, 이관 방법은 `MOVE.md` 를 보세요.

## 웹 퍼블리싱 관련 주의

루트의 **`.nojekyll` 은 지우면 안 됩니다.** GitHub Pages 는 기본으로 Jekyll 을 돌리고,
Jekyll 은 `_` 로 시작하는 폴더를 무시합니다. 이 파일이 없으면 `_ds/` 가 통째로 404 가 되어
폰트와 색이 전부 사라집니다.

마찬가지로 **`vendor/` 가 빠지면 차트 25개가 조용히 사라집니다.** 그런 상태가 되면
슬라이드에 빨간 안내 상자가 뜨도록 해 두었습니다.
