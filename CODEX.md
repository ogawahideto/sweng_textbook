# Codex CLI プロジェクト設定

このファイルは Codex CLI が本リポジトリで Claude Code と Gemini CLI と同一ポリシーで振る舞うための設定です。既存の Claude/Gemini の設定・ファイルには一切変更を加えません。

## マルチエージェント運用

本プロジェクトは複数エージェント（Claude Code / Gemini CLI / Codex CLI）で共同執筆します。Codex も下記の共通リソースとワークフローに厳密に従います。

### 共通リソース（必須参照）

| ファイル | 用途 |
|---|---|
| `.ai/agents.md` | エージェントの役割・振る舞い定義 |
| `.ai/workflows/draft.md` | 草稿生成手順 |
| `.ai/workflows/review.md` | レビュー手順 |
| `.ai/workflows/plan-next.md` | 次タスク決定手順 |
| `style-guide.md` | 執筆スタイル（トーン/用語/構成） |
| `plan.md` / `progress.md` | 企画・進捗の単一情報源 |

### タスク別 参照ルール（自動）

- セッション開始: `progress.md`, `.ai/agents.md`, 最新の `.ai/sessions/*.md`
- 草稿生成: `.ai/workflows/draft.md`, `style-guide.md`, `plan.md`, 対象章の既存ファイル
- レビュー: `.ai/workflows/review.md`, `style-guide.md`, 対象セクション
- 次タスク決定: `.ai/workflows/plan-next.md`, `progress.md`, `plan.md`

### 連携・運用ルール

1. `progress.md` を常に最新化（作業完了時に更新）
2. `.ai/sessions/YYYY-MM-DD.md` へ作業ログを追記（上書き禁止）
3. 論理単位で小さくコミット（revert 可能性を高める）
4. 齟齬時はログより実ファイル構造を優先

### コミットルール（共通）

- 1コミット = 1つの論理的変更。Conventional Commits を推奨（例: `docs:`/`feat:`/`fix:`/`refactor:`）。
- 例:
  - 良い: `docs: 3.1節に図の凡例を追加`
  - 避ける: `docs: 3.1追記とスタイル修正`（複数趣旨の混在）

## ポジティブ・ライティング方針（最重要）

従来の「課題起点」ではなく「可能性・価値起点」で記述します。技術的事実の厳密性は保持します。詳細は `style-guide.md` を参照。

- 使わない → 使う（例）
  - 危険です → 可能性が眠っています
  - 失敗する → 成功に近づく
  - 難しい → 奥深い／挑戦しがいがある
  - 罠 → コツ／ポイント

例外: 計算量や資源制約等の事実は明確に記述して可。

## ファイル構成（要点）

- 執筆: `chapters/`, `plan.md`, `progress.md`, `style-guide.md`, `templates/`
- サンプル: `sample-code/questforge/`（Python, Clean Architecture）
- エージェント共通設定: `.ai/agents.md`, `.ai/workflows/`, `.ai/commands/`, `.ai/sessions/`
- 図版: `assets/diagrams/`（章別ディレクトリ、SVG 推奨）

## ワークフロー（Codex 実装指針）

1. タスク着手前に該当ワークフローを読み込み実行
2. 生成物はテンプレート構造を遵守
3. 作業後に `progress.md` とセッションログを更新
4. 必要に応じて `.ai/commands/` のスキルを適用

### カスタムスキル（共通）

- `/session-log` セッションログ更新
- `/update-toc` 目次更新
- `/chapter-consistency` 章内整合性チェック
- `/positive-check` ネガ表現の検出と言い換え提案
- 詳細は `.ai/commands/` を参照

## セッションログ運用

- 場所: `.ai/sessions/YYYY-MM-DD.md`
- タイミング: セッション開始・区切り・終了時
- 追記形式で、概要/活動/更新ファイル/次の一手を簡潔に記録

## Codex 固有メモ

- Codex は Claude/Gemini と同一ポリシーを厳守。相違が生じる場合は `style-guide.md` と共通ワークフローを優先。
- 破壊的操作や設定変更は提案止まりとし、PR で合意形成。

---

この `CODEX.md` は Codex CLI の参照専用です。他エージェントの設定（`CLAUDE.md`, `GEMINI.md`）には手を加えません。
