from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
import re
import sys
import json
import argparse
from datetime import datetime


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


def extract_metadata(video_url):
    """yt-dlp를 사용하여 YouTube 동영상의 메타데이터를 추출합니다."""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return {
                'video_id': info.get('id'),
                'title': info.get('title'),
                'channel': info.get('uploader') or info.get('channel'),
                'upload_date': info.get('upload_date'),
                'duration': info.get('duration'),
                'view_count': info.get('view_count'),
                'description': info.get('description'),
                'thumbnail': info.get('thumbnail')
            }
    except Exception as e:
        print(f"메타데이터 추출 오류: {str(e)}", file=sys.stderr)
        return None


def get_transcript(video_url, language='en'):
    """YouTube 동영상의 자막을 가져옵니다."""
    try:
        video_id = extract_video_id(video_url)
        if not video_id:
            raise ValueError("올바른 YouTube URL이 아닙니다.")

        # 자막 가져오기
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id, languages=[language])
        
        # fetch 결과를 dict 형태로 변환
        transcript_list = []
        for snippet in transcript.snippets:
            transcript_list.append({
                'start': snippet.start,
                'duration': snippet.duration,
                'text': snippet.text
            })
        return transcript_list

    except Exception as e:
        print(f"자막 추출 오류: {str(e)}", file=sys.stderr)
        return None


def combine_data(video_url, language='en', metadata_only=False):
    """메타데이터와 자막을 통합합니다."""
    metadata = extract_metadata(video_url)
    if not metadata:
        return None
        
    result = metadata.copy()
    
    if not metadata_only:
        transcript = get_transcript(video_url, language)
        if transcript:
            result['transcript'] = transcript
            result['transcript_language'] = language
        else:
            result['transcript'] = None
            result['transcript_language'] = language
    
    return result


def print_text_format(data, language='en'):
    """기존 텍스트 형식으로 출력합니다."""
    print(f"제목: {data.get('title', 'N/A')}")
    print(f"채널: {data.get('channel', 'N/A')}")
    print(f"업로드 날짜: {data.get('upload_date', 'N/A')}")
    print(f"길이: {data.get('duration', 'N/A')}초")
    print(f"조회수: {data.get('view_count', 'N/A')}")
    print("\n--- 자막 ---")
    
    transcript = data.get('transcript')
    if transcript:
        for snippet in transcript:
            start_time = int(snippet['start'])
            text = snippet['text'].replace('\n', ' ')
            minutes = start_time // 60
            seconds = start_time % 60
            print(f"[{minutes:02d}:{seconds:02d}] {text}")
    else:
        print("자막을 가져올 수 없습니다.")


def main():
    parser = argparse.ArgumentParser(description='YouTube 동영상의 메타데이터와 자막을 가져옵니다.')
    parser.add_argument('url', help='YouTube 동영상 URL')
    parser.add_argument('-l', '--language', default='en', help='자막 언어 코드 (기본값: en)')
    parser.add_argument('-f', '--format', choices=['json', 'text'], default='text', help='출력 형식 (기본값: text)')
    parser.add_argument('-o', '--output', help='출력 파일 경로 (지정하지 않으면 stdout으로 출력)')
    parser.add_argument('--metadata-only', action='store_true', help='메타데이터만 가져오기 (자막 제외)')
    
    args = parser.parse_args()
    
    # 데이터 추출
    data = combine_data(args.url, args.language, args.metadata_only)
    if not data:
        print("데이터를 가져올 수 없습니다.", file=sys.stderr)
        sys.exit(1)
    
    # 출력 처리
    if args.format == 'json':
        output_content = json.dumps(data, ensure_ascii=False, indent=2)
    else:
        # 텍스트 형식으로 출력하기 위해 문자열로 변환
        import io
        import contextlib
        
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            print_text_format(data, args.language)
        output_content = f.getvalue()
    
    # 파일 또는 stdout으로 출력
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_content)
        print(f"결과가 {args.output}에 저장되었습니다.")
    else:
        if args.format == 'json':
            print(output_content)
        else:
            print_text_format(data, args.language)


if __name__ == "__main__":
    main()
