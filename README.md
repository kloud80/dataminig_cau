# AI를 활용한 도시 빅데이터 분석 — 강의안

**스마트시티 AI · 데이터 분석 역량 강화를 위한 실습 세미나** · 4주 · 중앙대학교 도시공학과 Urban D&A 연구실

웹에서 바로 보기 → **https://kloud80.github.io/dataminig_cau/**

브라우저로 열고 `F` 를 누르면 전체화면입니다. 설치할 것은 없습니다.

수업 시작 전 안내 화면(QR + 커리큘럼) → **https://kloud80.github.io/dataminig_cau/중앙대26특강/qr.html**

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

## 주차

| 주 | 날짜 | 내용 | 쪽 |
|---|---|---|---|
| 1주차 | 9월 5일 | [데이터 분석과 기계학습](중앙대26특강/W01_데이터분석과_기계학습/present.html) | 95 |
| 2주차 | 9월 12일 | [시계열, 언어 모델, 에이전트](중앙대26특강/W02_시계열과_언어모델/present.html) | 178 |
| 3주차 | 9월 19일 | [이미지를 읽고, 찾고, 만든다](중앙대26특강/W03_이미지_읽기와_생성/present.html) | 150 |
| 4주차 | 10월 10일 | [주소 한 줄에서 3D 건물까지](중앙대26특강/W04_주소에서_3D건물까지/present.html) | 69 |

## 실습 노트북 — Colab 에서 바로 열기

링크를 누르면 Colab 이 이 저장소에서 노트북을 바로 엽니다. 위에서부터 셀을 실행하면 됩니다.
상단의 **드라이브에 사본 저장** 을 누르면 고친 내용이 내 드라이브에 남습니다.

### 3주차

| 노트북 | 내용 | 쪽 |
|---|---|---|
| [건물외벽학습.ipynb](https://colab.research.google.com/github/kloud80/dataminig_cau/blob/main/%EC%A4%91%EC%95%99%EB%8C%8026%ED%8A%B9%EA%B0%95/notebooks/%EA%B1%B4%EB%AC%BC%EC%99%B8%EB%B2%BD%ED%95%99%EC%8A%B5.ipynb) | CNN 으로 건물 외벽 사진 분류하기 | 21 |
| [거리뷰분할_DeepLab_SAM.ipynb](https://colab.research.google.com/github/kloud80/dataminig_cau/blob/main/%EC%A4%91%EC%95%99%EB%8C%8026%ED%8A%B9%EA%B0%95/notebooks/%EA%B1%B0%EB%A6%AC%EB%B7%B0%EB%B6%84%ED%95%A0_DeepLab_SAM.ipynb) | 거리 사진을 DeepLab · SAM 으로 분할하기 | 68 |
| [거리지표로_연구하기.ipynb](https://colab.research.google.com/github/kloud80/dataminig_cau/blob/main/%EC%A4%91%EC%95%99%EB%8C%8026%ED%8A%B9%EA%B0%95/notebooks/%EA%B1%B0%EB%A6%AC%EC%A7%80%ED%91%9C%EB%A1%9C_%EC%97%B0%EA%B5%AC%ED%95%98%EA%B8%B0.ipynb) | 사진 → 거리 지표 → 사람의 평가 → 회귀로 연구하기 | 74 |

### 4주차

| 노트북 | 내용 | 쪽 |
|---|---|---|
| [W04_1 주소에서 건물 외곽선까지](https://colab.research.google.com/github/kloud80/dataminig_cau/blob/main/%EC%A4%91%EC%95%99%EB%8C%8026%ED%8A%B9%EA%B0%95/notebooks/w04_colab/W04_1%20%EC%A3%BC%EC%86%8C%EC%97%90%EC%84%9C%20%EA%B1%B4%EB%AC%BC%20%EC%99%B8%EA%B3%BD%EC%84%A0%EA%B9%8C%EC%A7%80.ipynb) | 주소를 좌표로 바꾸고 건물 외곽선 받기 | 18 |
| [W04_2 건물 속성 모으기](https://colab.research.google.com/github/kloud80/dataminig_cau/blob/main/%EC%A4%91%EC%95%99%EB%8C%8026%ED%8A%B9%EA%B0%95/notebooks/w04_colab/W04_2%20%EA%B1%B4%EB%AC%BC%20%EC%86%8D%EC%84%B1%20%EB%AA%A8%EC%9C%BC%EA%B8%B0.ipynb) | 건축물대장·도로명주소로 높이·층수 모으기 | 18 |
| [W04_3 입면 분할과 LOD1 매스](https://colab.research.google.com/github/kloud80/dataminig_cau/blob/main/%EC%A4%91%EC%95%99%EB%8C%8026%ED%8A%B9%EA%B0%95/notebooks/w04_colab/W04_3%20%EC%9E%85%EB%A9%B4%20%EB%B6%84%ED%95%A0%EA%B3%BC%20LOD1%20%EB%A7%A4%EC%8A%A4.ipynb) | 외곽선을 입면으로 나누고 LOD1 매스 세우기 | 25 |
| [W04_4 위성영상으로 지붕 읽기](https://colab.research.google.com/github/kloud80/dataminig_cau/blob/main/%EC%A4%91%EC%95%99%EB%8C%8026%ED%8A%B9%EA%B0%95/notebooks/w04_colab/W04_4%20%EC%9C%84%EC%84%B1%EC%98%81%EC%83%81%EC%9C%BC%EB%A1%9C%20%EC%A7%80%EB%B6%95%20%EC%9D%BD%EA%B8%B0.ipynb) | 위성영상으로 지붕 읽기 — 기복변위 보정 | 25 |
| [W04_5 사진을 치수로 읽기 — BDS](https://colab.research.google.com/github/kloud80/dataminig_cau/blob/main/%EC%A4%91%EC%95%99%EB%8C%8026%ED%8A%B9%EA%B0%95/notebooks/w04_colab/W04_5%20%EC%82%AC%EC%A7%84%EC%9D%84%20%EC%B9%98%EC%88%98%EB%A1%9C%20%EC%9D%BD%EA%B8%B0%20%E2%80%94%20BDS.ipynb) | 사진을 비율로 판독해 치수로 — BDS | 46 |
| [W04_6 astra — 모델이 스크립트를 쓴다](https://colab.research.google.com/github/kloud80/dataminig_cau/blob/main/%EC%A4%91%EC%95%99%EB%8C%8026%ED%8A%B9%EA%B0%95/notebooks/w04_colab/W04_6%20astra%20%E2%80%94%20%EB%AA%A8%EB%8D%B8%EC%9D%B4%20%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8%EB%A5%BC%20%EC%93%B4%EB%8B%A4.ipynb) | astra — 모델이 쓴 스크립트를 검사하고 실행하기 | 64 |

4주차 노트북은 순서대로 이어지지만 하나씩 따로 돌려도 됩니다. 첫 셀이 필요한 실습 데이터
(`w04_colab/data/`, 약 1.5 MB)를 이 저장소에서 알아서 받아 옵니다.

**API 키가 없어도 끝까지 돕니다.** 키가 없으면 아이파크타워(영동대로 520)에 대해 실제
파이프라인이 낸 결과 파일을 읽어 이어 갑니다. 키를 쓰려면 Colab 왼쪽 **열쇠 아이콘(보안 비밀)** 에
`OPENAI_API_KEY` · `VWORLD_KEY` · `DATA_GO_KR_KEY` · `JUSO_KEY` 를 넣으세요. 노트북 안에 직접 적지 마세요.
5·6번에 사진을 넣을 때는 직접 찍었거나 공개 라이선스인 사진만 씁니다.

## 주차별 구성

### 1주차 — 95쪽

| 구간 | 내용 | 쪽 |
|---|---|---|
| 1부 | 데이터 분석 기초 — 평균에서 다중회귀까지 | 1–53 |
| 전환 | statistics → heuristics | 54 |
| 2부 | 기계학습의 역사 — 기대와 겨울, 그리고 돌파 | 55–95 |

직접 눌러 보는 슬라이드가 두 장 있습니다. **60쪽**은 단층 퍼셉트론이 가중치를
고쳐 가는 과정, **83쪽**은 순전파부터 역전파·가중치 갱신까지를 한 단계씩
계산해 보여 줍니다.

### 2주차 — 178쪽

| 구간 | 내용 | 쪽 |
|---|---|---|
| 1부 | 시계열 분석 — 백색잡음에서 Prophet 까지 | 1–20 |
| 2부 | 순환신경망 — RNN · LSTM · GRU | 22–50 |
| 3부 | 언어 모델과 어텐션 — Seq2Seq 에서 Transformer 까지 | 52–80 |
| 4부 | LLM 의 구조 — 무엇이 모델의 크기를 정하는가 | 82–103 |
| 5부 | LLM 은 세 번 학습된다 — Pre-training · SFT · RLHF | 105–128 |
| 6부 | 프롬프트와 증강 생성 — 프롬프트 · RAG · MCP | 130–159 |
| 7부 | 에이전틱 AI 와 하네스 엔지니어링 | 161–178 |

직접 눌러 보는 슬라이드가 셋입니다. **12쪽**은 사인과 코사인을 겹쳐 파형을
만들어 보고, **29쪽**은 RNN 이 다섯 걸음을 걷는 계산을 한 걸음씩 보여 주며,
**40쪽**은 LSTM 의 네 게이트를 하나씩 짚습니다. 표의 숫자는 모두 그 자리에서
계산된 값입니다.

### 3주차 — 150쪽

| 구간 | 내용 | 쪽 |
|---|---|---|
| 1–6부 | CNN 기초 — 이미지 데이터, 도시 데이터, 격자 데이터, 계보 | 1–42 |
| 전환 | 무엇이 있다에서 어디에 있다로 | 43 |
| 7–8부 | 탐지와 분할 — YOLO · U-Net · DeepLab · SAM | 44–78 |
| 전환 | 없던 이미지를 만든다 | 79 |
| 9–12부 | 생성 모델 — GAN · 오토인코더 · VAE · 확산 모델 | 80–127 |
| 전환 | 이미지와 글자 | 128 |
| 13–16부 | VLM 과 멀티모달 — CLIP · ViT · 지금 | 129–150 |

### 4주차 — 69쪽

주소 한 줄(`서울특별시 강남구 영동대로 520`)에서 출발해 공공데이터와 사진으로 3D 건물을
짓는 연구 파이프라인을 세 번의 설계 변경(v0.2 → v0.3 → v0.4)을 따라가며 봅니다.

| 구간 | 내용 | 쪽 |
|---|---|---|
| 1부 | 문제 — 주소 한 줄에서 3D 건물까지 | 5–9 |
| 2부 | 데이터 — 좌표, 외곽선, 건축물대장 · 실습 ① ② | 10–18 |
| 3부 | 기하 — 입면 나누기와 LOD1 매스 · 실습 ③ ④ | 19–25 |
| 4부 | v0.2 — 사진을 벽에 붙였다 | 26–32 |
| 5부 | v0.3 — 사진을 읽어 숫자(BDS)로 옮겼다 · 실습 ⑤ | 33–46 |
| 6부 | v0.4 astra — 모델이 직접 스크립트를 쓴다 · 실습 ⑥ | 47–64 |
| 7부 | 정리 — 4주를 한 장에 | 65–69 |

## 이 저장소에 들어 있는 것

발표에 필요한 것만 있습니다 — 주차별 폴더, 실습 노트북, 옛 주소를 그리로 넘기는 리다이렉트.

```
index.html                          루트 → 주차 목록 (위치가 붙어 있으면 1주차로)
중앙대26특강/
  index.html                        주차 목록
  qr.html                           수업 전 안내 화면 (QR + 커리큘럼)
  present.html                      1주차 때 나눠 준 주소 → 1주차로 넘김
  _ds/                              위 세 화면이 쓰는 디자인 시스템
  W01_데이터분석과_기계학습/          present.html  ·  assets/  uploads/  _ds/  vendor/
  W02_시계열과_언어모델/              present.html  ·  uploads/  _ds/  vendor/  SOURCE.md
  W03_이미지_읽기와_생성/             present.html  ·  uploads/  _ds/  vendor/
  W04_주소에서_3D건물까지/            present.html  ·  uploads/  _ds/  vendor/
  notebooks/
    *.ipynb                         3주차 실습 노트북
    w04_colab/                      4주차 실습 노트북 6개 + w04_tools.py + data/
```

각 주차 폴더는 자립형입니다. `present.html` 이 자산을 상대경로로 부르므로 폴더째
옮겨도 그대로 열립니다. 네트워크 없이도 같은 화면이 나옵니다.

덱 원본(`*.dc.html`)과 빌드 스크립트는 이 저장소에 올리지 않습니다. 2주차 원본이
어디 있는지는 `중앙대26특강/W02_시계열과_언어모델/SOURCE.md` 에 적어 두었습니다.
