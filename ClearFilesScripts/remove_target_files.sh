#!/usr/bin/env bash

TARGET_DIRS=(
    "$HOME/projects"
    "$HOME/workspace"
)

REMOVE_DIRS=(
    "node_modules"
    ".venv"
    "venv"
)

targets=()

echo "삭제 대상 검색 중..."
echo

for target in "${TARGET_DIRS[@]}"; do
    if [[ ! -d "$target" ]]; then
        echo "[SKIP] 디렉터리가 없습니다: $target"
        continue
    fi

    find_args=()

    for name in "${REMOVE_DIRS[@]}"; do
        if ((${#find_args[@]} > 0)); then
            find_args+=(-o)
        fi

        find_args+=(-name "$name")
    done

    while IFS= read -r -d '' dir; do
        targets+=("$dir")
    done < <(
        find "$target" \
            -type d \
            \( "${find_args[@]}" \) \
            -prune \
            -print0
    )
done

echo
echo "========================================"
echo "삭제 예정 디렉터리"
echo "========================================"

if ((${#targets[@]} == 0)); then
    echo "삭제할 디렉터리가 없습니다."
    exit 0
fi

for dir in "${targets[@]}"; do
    echo "$dir"
done

echo
echo "총 ${#targets[@]}개의 디렉터리를 삭제합니다."
echo

read -r -p "정말 삭제하시겠습니까? [y/N] " answer

case "$answer" in
    y|Y)
        echo
        echo "삭제를 시작합니다..."

        for dir in "${targets[@]}"; do
            echo "[REMOVE] $dir"
            rm -rf -- "$dir"
        done

        echo
        echo "삭제 완료."
        ;;
    *)
        echo
        echo "취소했습니다."
        exit 0
        ;;
esac
