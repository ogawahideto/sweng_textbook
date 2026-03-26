#!/bin/bash
# pre-commit-style-check.sh
#
# 書籍的可読性ルール（style-guide.md §書籍的可読性のルール）の
# 違反を検出してコミット前に警告を表示します。
# ※ コミットはブロックしません（警告のみ）
#
# インストール方法:
#   cp .ai/hooks/pre-commit-style-check.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit

# 色定義
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RESET='\033[0m'

# ステージ済みの .md ファイルを取得
STAGED_MD_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.md$')

if [ -z "$STAGED_MD_FILES" ]; then
    exit 0
fi

VIOLATIONS=0

echo ""
echo -e "${CYAN}📖 book-polish: 書籍的可読性チェックを実行中...${RESET}"
echo ""

for FILE in $STAGED_MD_FILES; do
    if [ ! -f "$FILE" ]; then
        continue
    fi

    FILE_VIOLATIONS=0
    MESSAGES=""

    # ルール①: 見出し密度チェック（H2内のH3が5個超）
    # 簡易チェック: ファイル全体のH3数が10個超で警告
    H3_COUNT=$(grep -c '^### ' "$FILE" 2>/dev/null || echo 0)
    H2_COUNT=$(grep -c '^## ' "$FILE" 2>/dev/null || echo 1)
    if [ "$H2_COUNT" -gt 0 ] && [ "$((H3_COUNT / H2_COUNT))" -ge 5 ]; then
        MESSAGES="${MESSAGES}\n  ① 見出し密度: H3が${H3_COUNT}個、H2が${H2_COUNT}個（平均${H3_COUNT}/${H2_COUNT}）"
        FILE_VIOLATIONS=$((FILE_VIOLATIONS + 1))
    fi

    # ルール②: 太字の過多チェック（1000字あたり**が15個超）
    BOLD_COUNT=$(grep -o '\*\*' "$FILE" | wc -l 2>/dev/null || echo 0)
    BOLD_PAIRS=$((BOLD_COUNT / 2))
    CHAR_COUNT=$(wc -m < "$FILE" 2>/dev/null || echo 1000)
    if [ "$CHAR_COUNT" -gt 0 ] && [ "$((BOLD_PAIRS * 1000 / CHAR_COUNT))" -gt 15 ]; then
        MESSAGES="${MESSAGES}\n  ② 太字の過多: 太字ペアが${BOLD_PAIRS}個 / ${CHAR_COUNT}字"
        FILE_VIOLATIONS=$((FILE_VIOLATIONS + 1))
    fi

    # ルール⑥: セクション末尾の順序チェック
    # 「さらに学ぶためのリソース」が「AIへの詠唱例」より前にある場合
    LEARN_LINE=$(grep -n '^## さらに学ぶ' "$FILE" | head -1 | cut -d: -f1)
    AI_LINE=$(grep -n '^## AIへの詠唱例' "$FILE" | head -1 | cut -d: -f1)
    if [ -n "$LEARN_LINE" ] && [ -n "$AI_LINE" ]; then
        if [ "$LEARN_LINE" -lt "$AI_LINE" ]; then
            MESSAGES="${MESSAGES}\n  ⑥ セクション末尾の順序: 「さらに学ぶ」(${LEARN_LINE}行)が「AIへの詠唱例」(${AI_LINE}行)より前"
            FILE_VIOLATIONS=$((FILE_VIOLATIONS + 1))
        fi
    fi

    # ルール⑦: コラムの上限チェック（>が15行以上連続）
    # awkでブロック長を計算
    MAX_BLOCK=$(awk '/^> /{c++;if(c>max)max=c} !/^> /{c=0} END{print max+0}' "$FILE" 2>/dev/null || echo 0)
    if [ "$MAX_BLOCK" -ge 15 ]; then
        MESSAGES="${MESSAGES}\n  ⑦ コラム超過: 引用ブロックが最大${MAX_BLOCK}行連続（推奨: 15行以内）"
        FILE_VIOLATIONS=$((FILE_VIOLATIONS + 1))
    fi

    # ルール⑧: 前節参照チェック
    CALLBACK_COUNT=$(grep -cE '^(前節で[はにもが]|ここまで[でに]|本節では|この節では)' "$FILE" 2>/dev/null || echo 0)
    if [ "$CALLBACK_COUNT" -gt 0 ]; then
        CALLBACK_LINES=$(grep -nE '^(前節で[はにもが]|ここまで[でに]|本節では|この節では)' "$FILE" | head -3 | awk -F: '{print $1}' | tr '\n' ',')
        MESSAGES="${MESSAGES}\n  ⑧ 前節参照: ${CALLBACK_COUNT}箇所（行番号: ${CALLBACK_LINES%,}）"
        FILE_VIOLATIONS=$((FILE_VIOLATIONS + 1))
    fi

    # ファイルに違反があれば表示
    if [ "$FILE_VIOLATIONS" -gt 0 ]; then
        echo -e "${YELLOW}  ⚠ $FILE${RESET}"
        echo -e "$MESSAGES"
        echo ""
        VIOLATIONS=$((VIOLATIONS + FILE_VIOLATIONS))
    fi
done

if [ "$VIOLATIONS" -gt 0 ]; then
    echo -e "${YELLOW}合計 ${VIOLATIONS} 件の可読性ルール違反が見つかりました。${RESET}"
    echo "  ※ コミットは続行されます。/book-polish で詳細を確認できます。"
    echo ""
else
    echo -e "  ✅ 可読性チェック: 違反なし"
    echo ""
fi

# 警告のみで、コミットはブロックしない
exit 0
