#!/usr/bin/env bash

# 순회할 대상 디렉터리
TARGET_DIRS=(
    "$HOME/projects"
    "$HOME/workspace"
    "/data/projects"
)

# 삭제할 디렉터리 이름
REMOVE_DIRS=(
    "node_modules"
    ".venv"
    "venv"
)

for target in "${TARGET_DIRS[@]}"; do
    if [[ ! -d "$target" ]]; then
        echo "[SKIP] 디렉터리가 없습니다: $target"
        continue
    fi

    echo "[SCAN] $target"

    for name in "${REMOVE_DIRS[@]}"; do
        find "$target" \
            -type d \
            -name "$name" \
            -prune \
            -print \
            -exec rm -rf -- {} +
    done
done
