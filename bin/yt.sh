#!/bin/bash

# 인자가 없으면 사용법 출력
if [ $# -eq 0 ]; then
    echo "Usage: $0 <youtube-url>"
    exit 1
fi

# YouTube URL을 첫 번째 인자로 받음
youtube_url="$1"

# Python 스크립트 실행 후 결과를 받아서 클립보드에 복사
/Users/jake/llm-recipes/download-youtube-transcript/.venv/bin/python /Users/jake/llm-recipes/download-youtube-transcript/script.py "$youtube_url" | while read filename; do
osascript -e "tell application \"Finder\" to set the clipboard to (POSIX file \"${filename}\")"
done
