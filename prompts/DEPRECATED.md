# ⚠️ DEPRECATED

このディレクトリ (`prompts/`) は非推奨になりました。

## 新しい標準構造

標準的な `.ai/` ディレクトリを使用してください：

```
.ai/
├── agents.md              # AIエージェント定義
├── QUICKSTART.md         # クイックスタートガイド
├── context/              # プロジェクトコンテキスト
│   └── project.md
└── workflows/            # 標準ワークフロー
    ├── draft.md          # 草稿生成
    ├── review.md         # レビュー
    └── plan-next.md      # タスク計画
```

## マイグレーション

### 旧: `prompts/section-draft.md`
### 新: `.ai/workflows/draft.md`

より標準的で、AIツールとの統合が容易になっています。

## 使い方

詳細は以下を参照：

1. `.ai/QUICKSTART.md` - クイックスタート
2. `.ai/agents.md` - AIエージェントの使い方
3. `README.md` - 全体ガイド（更新済み）

---

**Note**: このディレクトリは将来削除される可能性があります。
新しい構造への移行を推奨します。
