# YouTube Transcript Tool

YouTube 동영상의 메타데이터와 자막을 JSON/텍스트 형식으로 추출하는 도구입니다.

## 기능

- YouTube 동영상의 메타데이터 추출 (제목, 채널, 업로드 날짜, 조회수 등)
- 다양한 언어의 자막 추출
- JSON 및 텍스트 형식 출력 지원
- 파일 저장 또는 표준 출력 지원
- 메타데이터만 추출하는 옵션

## 설치

### pipx 사용 (권장)

```bash
pipx install .
```

### pip 사용

```bash
pip install .
```

## 사용법

### 기본 사용법

```bash
# 영어 자막과 메타데이터를 텍스트 형식으로 출력
yt "https://www.youtube.com/watch?v=VIDEO_ID"

# 한국어 자막 추출
yt "https://www.youtube.com/watch?v=VIDEO_ID" -l ko

# JSON 형식으로 출력
yt "https://www.youtube.com/watch?v=VIDEO_ID" -f json

# 파일로 저장
yt "https://www.youtube.com/watch?v=VIDEO_ID" -o output.txt

# 메타데이터만 추출 (자막 제외)
yt "https://www.youtube.com/watch?v=VIDEO_ID" --metadata-only
```

### 명령어 옵션

- `-l, --language`: 자막 언어 코드 (기본값: en)
- `-f, --format`: 출력 형식 (json, text) (기본값: text)
- `-o, --output`: 출력 파일 경로 (지정하지 않으면 stdout으로 출력)
- `--metadata-only`: 메타데이터만 추출 (자막 제외)

### 지원하는 URL 형식

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `youtube.com/watch?v=VIDEO_ID`
- `youtu.be/VIDEO_ID`

## 출력 예시

### 텍스트 형식

```
제목: 예시 동영상 제목
채널: 예시 채널
업로드 날짜: 20231225
길이: 300초
조회수: 10000

--- 자막 ---
[00:00] 안녕하세요 여러분
[00:05] 오늘은 YouTube 자막 추출에 대해 알아보겠습니다
```

### JSON 형식

```json
{
  "video_id": "VIDEO_ID",
  "title": "예시 동영상 제목",
  "channel": "예시 채널",
  "upload_date": "20231225",
  "duration": 300,
  "view_count": 10000,
  "description": "동영상 설명...",
  "thumbnail": "https://...",
  "transcript": [
    {
      "start": 0.0,
      "duration": 3.5,
      "text": "안녕하세요 여러분"
    }
  ],
  "transcript_language": "ko"
}
```

## 의존성

- `youtube-transcript-api>=0.6.2`: YouTube 자막 API
- `yt-dlp>=2023.12.30`: YouTube 메타데이터 추출

## 요구사항

- Python 3.8 이상

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.