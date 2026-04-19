# QuestForge 実装概要

QuestForgeプロジェクトの実装状況をまとめたドキュメントです。

## 実装完了項目

### ✅ ドメイン層（Domain Layer）

**エンティティ（Entities）**

- [x] `Quest` - クエストエンティティ
  - クエストカテゴリ（DAILY, WEEKLY, EPIC, SIDE）
  - 難易度レベル（TRIVIAL, EASY, NORMAL, HARD, EPIC）
  - クエストステータス（AVAILABLE, IN_PROGRESS, COMPLETED, FAILED, CANCELLED）
  - ライフサイクルメソッド（start, complete, cancel, fail）
  - ボーナス経験値計算（期限前完了）

- [x] `Hero` - ヒーローエンティティ
  - レベルシステム（経験値 = 100 × レベル^1.5）
  - ストリーク管理（連続達成日数）
  - 経験値獲得とレベルアップ判定
  - レベル進捗率計算

- [x] `Reward` - 報酬エンティティ
  - 経験値付与
  - バッジ付与（オプション）

- [x] `Badge` - バッジエンティティ
  - レア度（common, rare, epic, legendary）
  - アイコン（絵文字）

**リポジトリインターフェース（Repository Interfaces）**

- [x] `QuestRepository` - クエストの永続化インターフェース
- [x] `HeroRepository` - ヒーローの永続化インターフェース
- [x] `BadgeRepository` - バッジの永続化インターフェース

### ✅ アプリケーション層（Application Layer）

**ユースケース（Use Cases）**

- [x] `CreateQuestUseCase` - クエスト作成
- [x] `StartQuestUseCase` - クエスト開始
- [x] `CompleteQuestUseCase` - クエスト完了（経験値付与、レベルアップ判定）
- [x] `CreateHeroUseCase` - ヒーロー作成
- [x] `ViewHeroProgressUseCase` - ヒーロー進捗確認

各ユースケースは以下の特徴を持ちます：
- Input/Outputデータ転送オブジェクト（DTO）
- ビジネスルールの適用
- エラーハンドリング（ValueError例外）
- リポジトリを通じたデータアクセス

### ✅ インフラストラクチャ層（Infrastructure Layer）

**永続化実装（Persistence）**

- [x] `InMemoryQuestRepository` - インメモリクエストリポジトリ
- [x] `InMemoryHeroRepository` - インメモリヒーローリポジトリ
- [x] `InMemoryBadgeRepository` - インメモリバッジリポジトリ
- [x] `JSONQuestRepository` - JSON永続化クエストリポジトリ
- [x] `JSONHeroRepository` - JSON永続化ヒーローリポジトリ
- [x] `JSONBadgeRepository` - JSON永続化バッジリポジトリ

**実装の種類:**
- **InMemory版**: テスト用の簡易実装。Pythonの辞書を使用。
- **JSON版**: 本番用の永続化実装。`data/`ディレクトリにJSONファイルとして保存。カスタムエンコーダーでUUID、datetime、Enumを処理。

### ✅ プレゼンテーション層（Presentation Layer）

**Streamlit Web UI**

- [x] `streamlit_app.py` - Streamlit Web インターフェース
  - ヒーロー管理（作成・選択）
  - クエスト一覧表示（フィルタリング機能付き）
  - クエスト作成フォーム
  - リアルタイム進捗表示
  - 統計ダッシュボード（完了率、難易度別グラフ）
  - カスタムCSS（グラデーション、カード表示）
  - レスポンシブデザイン

**主な機能:**
- 🗺️ **RPGマップビュー**
  - レベルに応じた8つのマイルストーン（スタート→森→山→城→神殿→火山→王国）
  - CSSアニメーション（バウンス効果）
  - グラデーション背景（空→草原）
  - 到達済み/現在地/未到達の視覚的区別
- セッション管理（st.session_state）
- タブ型インターフェース（Quest List / New Quest / Statistics）
- リアルタイム更新（st.rerun()）
- 難易度別の色分け表示
- ステータス別の絵文字アイコン
- プログレスバーでレベル進捗を視覚化

### ✅ インターフェース層（Interface Layer）

**CLI（Command Line Interface）**

- [x] `QuestForgeCLI` - コマンドラインインターフェース
  - `create_hero()` - ヒーロー作成
  - `create_quest()` - クエスト作成
  - `start_quest()` - クエスト開始
  - `complete_quest()` - クエスト完了
  - `show_progress()` - 進捗表示
  - `list_quests()` - クエスト一覧表示

**デモスクリプト**

- [x] `run_questforge_demo.py` - デモ実行スクリプト
  - Windows環境でのUTF-8出力対応
  - 8ステップのデモフロー
  - 絵文字を使った視覚的な出力

- [x] `run_questforge_gui.bat/.sh` - GUI起動スクリプト
  - Windows/Linux対応

## アーキテクチャ図

```
┌─────────────────────────────────────────────────────────┐
│          Presentation Layer (Web UI)                    │
│  - Streamlit App (streamlit_app.py)                     │
│  - カスタムCSS、タブ型UI、リアルタイム更新                 │
└──────────────┬──────────────────────────────────────────┘
               │
               │  ┌─────────────────────────────────────┐
               ├──│   Interface Layer (CLI)             │
               │  │  - QuestForgeCLI                    │
               │  │  - デモスクリプト                      │
               │  └─────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│          Application Layer (Use Cases)                   │
│  - CreateQuestUseCase, StartQuestUseCase                 │
│  - CompleteQuestUseCase, ViewHeroProgressUseCase         │
│  - CreateHeroUseCase                                     │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│          Domain Layer (Entities & Interfaces)            │
│  - Quest, Hero, Badge, Reward (エンティティ)              │
│  - QuestRepository, HeroRepository (インターフェース)      │
└──────────────────────────────────────────────────────────┘
               ▲
               │
┌──────────────┴───────────────────────────────────────────┐
│          Infrastructure Layer (Persistence)              │
│  - InMemoryQuestRepository                               │
│  - InMemoryHeroRepository                                │
│  - InMemoryBadgeRepository                               │
└──────────────────────────────────────────────────────────┘
```

## 技術スタック

- **言語**: Python 3.11+
- **Web UI**: Streamlit 1.30+（インタラクティブWeb UI）
- **データクラス**: dataclasses（エンティティの定義）
- **型ヒント**: type hints（静的型チェック）
- **アーキテクチャ**: Clean Architecture
- **設計手法**: Domain-Driven Design (DDD)

## コード統計

```
ファイル数: 28+
コード行数: ~2,000行（コメント・docstring含む）

内訳:
- ドメインエンティティ: ~500行
- リポジトリインターフェース: ~150行
- ユースケース: ~400行
- インフラ実装: ~200行
- プレゼンテーション層（Streamlit UI）: ~400行
- CLI: ~200行
- デモ・ドキュメント: ~200行
```

## 実行方法

### Web GUI（推奨）

```bash
cd sample-code/questforge
pip install streamlit
python -m streamlit run presentation/streamlit_app.py
```

ブラウザで http://localhost:8501 を開くと、QuestForgeのWeb UIが起動します。

### CLIデモ

```bash
cd sample-code
python run_questforge_demo.py
```

## デモ出力例

```
============================================================
🎮 QuestForge Demo - タスク管理をRPG風に！
============================================================

Step 1: ヒーローを作成
✨ Hero created: Alice the Alchemist

Step 5: クエストを完了
✅ Quest completed!
   💎 +100 XP

Step 7: 進捗を確認
==================================================
⚔️  Alice the Alchemist
==================================================
Level: 1
Total XP: 150
Progress: 53.2% to level 2
XP needed: 132

🔥 Streak: 1 days (best: 1)

📊 Quests:
  In Progress: 0
  Completed: 2
==================================================
```

### Web GUI スクリーンショット機能

Streamlit Web UIでは以下の画面を提供しています：

1. **Quest List タブ**
   - クエスト一覧をカード形式で表示
   - ステータスによる色分け（青：Available / 黄：In Progress / 緑：Completed）
   - ワンクリックで開始・完了
   - ステータスフィルター機能

2. **New Quest タブ**
   - クエスト作成フォーム
   - カテゴリ・難易度の選択
   - 期限設定（日数指定）

3. **Statistics タブ**
   - 総クエスト数、完了数、進行中数
   - 完了率の表示
   - 難易度別のバーチャート

4. **Hero Stats パネル**（全画面共通）
   - ヒーロー名とレベル
   - 総経験値と進捗バー
   - ストリーク記録

## 次のステップ（未実装機能）

以下の機能は、書籍の後の章で実装予定です：

### 第3章: 実装
- [ ] AIエージェントとの協働による実装

### 第4章: テスト
- [ ] 単体テスト（pytest）
- [ ] テストカバレッジ測定
- [ ] モックとスタブの活用
- [ ] デバッグ手法

### 第5章: リファクタリング
- [ ] コードレビュープロセス
- [ ] 技術負債の返済

### 第6章: デプロイと運用
- [ ] CI/CDパイプライン
- [ ] セキュリティスキャン
- [ ] Docker化
- [ ] クラウドデプロイ

## 教科書での活用

QuestForgeは以下の章で実践例として登場します：

| 章 | 活用内容 |
|----|----------|
| 第1章 | 要求工学: ユーザーストーリー作成 |
| 第2章 | 設計: ドメインモデル設計、Clean Architecture |
| 第3章 | 実装: AIと共にコードを実装 |
| 第4章 | テスト: TDD、pytest、カバレッジ、デバッグ |
| 第5章 | リファクタリング: コードレビュー、技術負債の返済 |
| 第6章 | デプロイと運用: CI/CD、セキュリティ、オブザーバビリティ |
| 第7章 | チーム開発: アジャイル、Git/GitHub |
| 第8章 | 倫理: AI時代の創造性と責任 |

## ライセンス

MIT License

## 作成日・更新日

- 作成日: 2026-01-19
- 最終更新: 2026-01-19（Streamlit Web UI追加）
