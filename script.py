from youtube_transcript_api import YouTubeTranscriptApi
import re
import sys


def extract_video_id(url):
    """YouTube URL에서 비디오 ID를 추출합니다."""
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&\s]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^\s]+)'
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def download_subtitle(video_url, language='en'):
    """YouTube 동영상의 자막을 다운로드합니다."""
    try:
        video_id = extract_video_id(video_url)
        if not video_id:
            raise ValueError("올바른 YouTube URL이 아닙니다.")

        # 자막 가져오기
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])

        # 텍스트 파일로 저장
        for entry in transcript:
            start_time = int(entry['start'])
            text = entry['text'].replace('\n', ' ')
            minutes = start_time // 60
            seconds = start_time % 60
            print(f"[{minutes:02d}:{seconds:02d}] {text}")

    except Exception as e:
        print(f"오류가 발생했습니다: {str(e)}")
        return None


def main():
    if len(sys.argv) < 2:
        print("사용법: python script.py <YouTube URL> [언어코드]")
        print("예시: python script.py https://www.youtube.com/watch?v=xxxxx ko")
        return

    url = sys.argv[1].strip()
    language = sys.argv[2] if len(sys.argv) > 2 else 'en'

    download_subtitle(url, language)


if __name__ == "__main__":
    main()
