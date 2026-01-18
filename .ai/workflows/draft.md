# Workflow: Draft Generation

セクションの草稿を生成するワークフローです。

## Trigger

新しいセクションの執筆を開始する時

## Prerequisites

- [ ] `progress.md` で該当セクションを確認済み
- [ ] `plan.md` でセクションの目的を理解済み
- [ ] `style-guide.md` を確認済み

## Steps

### 1. Context Loading

以下の情報を収集：

```
@plan.md の該当セクションの説明
@style-guide.md の執筆ルール
@progress.md の現在の状況
```

### 2. Invoke Agent

以下のプロンプトでAIエージェントを起動：

```
あなたは『「楽しい」ソフトウェア工学の教科書 - デジタル・アルケミー：伝統の美学とAIで紡ぐ創造の地図』の執筆アシスタントです。

@agents.md の指示に従ってください。

以下のセクションの草稿を生成してください：

**セクション**: [章番号].[節番号] [タイトル]

**目的**:
[plan.mdから抽出したセクションの目的]

**要件**:
- @style-guide.md に従った文体・トーン
- @templates/section-template.md の構造に従う
- 文字数: 2000-4000文字
- コード例: 実行可能なもの
- AI時代の視点を含める

**コンテキスト**:
- 前のセクション: [前セクションの概要]
- 次のセクション: [次セクションの概要]

草稿を生成してください。
```

### 3. Agent Response Format

エージェントは以下の形式で応答：

```markdown
# [X.Y] [節タイトル]

[section-template.mdに従った内容]

---

**Meta Information**:
- 文字数: [count]
- 主要概念: [list]
- コード例数: [count]
- 必要な図: [list]
- AI詠唱例: [count]
```

### 4. Save Draft

生成された草稿を保存：

```bash
# ファイル名: chapters/partX/chapterYY/X-Y.md
# 例: chapters/part1/chapter01/1-1.md
```

### 5. Update Progress

`progress.md` を更新：

```
状態: ⬜ 未着手 → 🟨 AI草稿
```

## Output

- 草稿ファイル: `chapters/partX/chapterYY/X-Y.md`
- 更新された `progress.md`

## Next Steps

人間の著者による修正・追記（`review.md` ワークフローへ）

## Example

### Input

```
セクション: 1.1 隠れた願いを翻訳する
目的: ユーザーの曖昧な言葉から真の課題を見つけ出す「アクティブ・リスニング」の技術を学ぶ
```

### Expected Output

```markdown
# 1.1 隠れた願いを翻訳する

## 導入: 言葉の奥にある真実

あなたは、ユーザーから「もっと使いやすくしてほしい」と言われたことはありませんか？...

[section-templateに従った構成]

---

**Meta Information**:
- 文字数: 3200
- 主要概念: アクティブ・リスニング, 要求抽出, ペルソナ分析
- コード例数: 2
- 必要な図: ["要求抽出プロセス", "ユーザーインタビューの構造"]
- AI詠唱例: 2
```

## Quality Checklist

生成された草稿が以下を満たしているか確認：

- [ ] style-guide.mdに準拠
- [ ] section-template.mdの構造に従っている
- [ ] 文字数が適切（2000-4000文字）
- [ ] コード例が含まれている
- [ ] AI時代の視点が含まれている
- [ ] 前後のセクションとのつながりが考慮されている

## Troubleshooting

### 草稿が短すぎる場合

```
以下の要素を追加してボリュームを増やしてください：
- より詳細な実践例
- ステップバイステップのハンズオン
- よくある誤解とその解説
```

### 草稿が長すぎる場合

```
以下の基準で内容を絞り込んでください：
- 本質的な内容に集中
- 詳細は参考リソースに委譲
- 重複部分を削除
```

### 技術的に不正確な場合

```
以下の点を修正してください：
[具体的な誤りを指摘]
```

## Related Workflows

- `review.md` - 生成された草稿のレビュー
- `plan-next.md` - 次のタスクの決定
