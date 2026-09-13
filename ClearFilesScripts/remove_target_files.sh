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
total_bytes=0

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
    # GNU du 기준: 바이트 단위 크기
    size_bytes=$(du -sb -- "$dir" 2>/dev/null | cut -f1)

    # 계산 실패 시 0 처리
    if [[ -z "$size_bytes" ]]; then
        size_bytes=0
    fi

    total_bytes=$((total_bytes + size_bytes))

    # 사람이 읽기 쉬운 형식
    size_human=$(du -sh -- "$dir" 2>/dev/null | cut -f1)

    printf "%8s  %s\n" "$size_human" "$dir"
done

echo
echo "========================================"
echo "요약"
echo "========================================"
echo "삭제 대상 : ${#targets[@]}개"

if command -v numfmt >/dev/null 2>&1; then
    total_human=$(numfmt --to=iec --suffix=B "$total_bytes")
    echo "총 용량   : $total_human"
else
    echo "총 용량   : $total_bytes bytes"
fi

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
