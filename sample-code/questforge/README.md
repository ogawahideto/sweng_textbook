# QuestForge

タスク管理をRPG風に楽しむアプリケーション

## 概要

QuestForgeは、日々のタスクを「クエスト」として管理し、完了すると経験値を獲得してレベルアップしていくタスク管理システムです。

## 特徴

- 🎮 **ゲーミフィケーション**: タスクをクエストとして扱い、完了すると経験値を獲得
- ⚔️ **レベルシステム**: 経験値を貯めてレベルアップ
- 🔥 **ストリーク**: 連続達成日数を記録してモチベーション維持
- 🏆 **バッジ**: 特定の条件を満たすと実績を獲得
- 📊 **進捗可視化**: レベル進捗や完了クエスト数を確認
- 💾 **データ永続化**: ヒーローとクエストはJSONファイルに自動保存

## アーキテクチャ

クリーンアーキテクチャとドメイン駆動設計を採用しています。

```
questforge/
├── domain/              # ドメイン層（ビジネスロジック）
│   ├── entities/        # エンティティ（Quest, Hero, Badge, Reward）
│   └── repositories/    # リポジトリインターフェース
├── application/         # アプリケーション層（ユースケース）
│   └── use_cases/       # ビジネスユースケース
├── infrastructure/      # インフラストラクチャ層（技術的詳細）
│   └── persistence/     # データ永続化実装
├── presentation/        # プレゼンテーション層（UI）
│   └── streamlit_app.py # Streamlit Web UI
└── cli/                 # コマンドラインインターフェース
```

## 使い方

### 🌐 Web GUI（推奨）

StreamlitベースのWeb UIで、視覚的に操作できます。

```bash
cd sample-code/questforge
pip install streamlit
python -m streamlit run presentation/streamlit_app.py
```

ブラウザで http://localhost:8501 を開くと、QuestForgeのWeb UIが表示されます。

**主な機能:**
- 🗺️ **RPGマップ**: レベルに応じて冒険の旅路を視覚化
  - スタート地点から王国まで8つのマイルストーン
  - 現在地は⚔️アイコンでバウンスアニメーション
  - 到達済みは✅、未到達は灰色表示
- 📊 リアルタイム進捗表示
- 🎯 ビジュアルなクエストカード
- ⚡ ワンクリックでクエスト開始/完了
- 📈 統計グラフの表示

### 💻 CLIデモの実行

コマンドライン版のデモも利用できます。

```bash
cd sample-code
python run_questforge_demo.py
```

### 📚 プログラムからの利用

```python
from infrastructure.persistence import InMemoryQuestRepository, InMemoryHeroRepository
from cli import QuestForgeCLI

# リポジトリの初期化
quest_repo = InMemoryQuestRepository()
hero_repo = InMemoryHeroRepository()

# CLIの初期化
cli = QuestForgeCLI(quest_repo, hero_repo)

# ヒーローを作成
cli.create_hero("Alice", "alice@example.com")

# ヒーローIDを取得
heroes = hero_repo.list_all()
alice = heroes[0]

# クエストを作成
cli.create_quest(
    alice.id,
    title="プロローグを書く",
    description="教科書のプロローグを執筆する",
    category="epic",
    difficulty="normal",
    due_days=7,
)

# クエストを開始・完了
quests = quest_repo.find_by_hero_id(alice.id)
quest = quests[0]
cli.start_quest(quest.id)
cli.complete_quest(quest.id)

# 進捗を確認
cli.show_progress(alice.id)
```

## 難易度と経験値

| 難易度 | 推定時間 | 経験値 |
|--------|----------|--------|
| TRIVIAL | 5分 | 10 XP |
| EASY | 30分 | 25 XP |
| NORMAL | 1-2時間 | 50 XP |
| HARD | 半日 | 100 XP |
| EPIC | 数日 | 250 XP |

## レベルシステム

レベルアップに必要な累計経験値は `100 × レベル^1.5` で計算されます。

- Level 1: 0 XP
- Level 2: 100 XP
- Level 3: 283 XP
- Level 4: 519 XP
- Level 5: 806 XP

## 教科書での活用

このサンプルプロジェクトは、『「楽しい」ソフトウェアエンジニアリング』の各章で以下のように使用されます。

- **第1章（要求工学）**: ユーザーストーリーとバックログ作成
- **第2章（設計）**: ドメインモデルとクリーンアーキテクチャ
- **第3章（実装）**: AIと共にコードを実装
- **第4章（テスト）**: TDD、単体テスト・統合テスト、デバッグ
- **第5章（リファクタリング）**: コードレビュー、技術負債の返済
- **第6章（デプロイと運用）**: CI/CD、セキュリティ、オブザーバビリティ
- **第7章（チーム開発）**: アジャイル、Git/GitHub
- **第8章（倫理）**: AI時代の創造性と責任

## ライセンス

MIT License
