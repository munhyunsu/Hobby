#!/bin/bash

# 1. __MACOSX 디렉토리 재귀적 삭제
echo "Deleting __MACOSX directories..."
find . -type d -name "__MACOSX" -exec rm -rf {} +

# 2. .DS_Store 파일 재귀적 삭제 (대소문자 구분 없이)
echo "Deleting .DS_Store files..."
find . -type f -iname ".DS_Store" -delete

echo "Cleanup complete!"
