# QuestForge 詳細仕様

書籍全体で使用するサンプルプロジェクト「QuestForge」の仕様定義

## 📖 概要

**QuestForge（クエストフォージ）**は、個人やチームのタスク・プロジェクト管理をRPGゲーム風に楽しくするシステムです。

### コアコンセプト

- **タスク = クエスト**: やるべきことを「冒険」として捉える
- **完了 = 経験値獲得**: 達成感を可視化
- **継続 = レベルアップ**: 成長を実感
- **協力 = パーティプレイ**: チームでの達成を楽しむ

---

## 🎯 主要機能（章ごとの展開）

### Phase 1: 基本機能（第1-2部）

#### 第1部で設計するもの

**1.1 要求分析**:
- ユーザー: 「タスク管理が続かない」「やる気が出ない」
- 真の課題: モチベーション維持、達成感の欠如、優先順位の迷い
- 解決策: ゲーミフィケーション、AI支援、可視化

**1.2 ドメインモデル**:
```
主要エンティティ:
- Quest（クエスト）: タスクそのもの
- Hero（ヒーロー）: ユーザー
- QuestCategory（カテゴリ）: クエストの種類
- Reward（報酬）: 経験値、バッジ
- Achievement（実績）: 達成記録
```

**1.3 AIとのブレスト**:
- どんな報酬が嬉しい？
- クエストのカテゴリは？
- 難易度の自動推定は可能？

**2.1-2.3 アーキテクチャ設計**:
- レイヤー構造（UI, Application, Domain, Infrastructure）
- Repository パターン
- クリーンアーキテクチャ

#### 第2部で実装するもの

**3.1 AI駆動実装**:
- Quest CRUD操作
- AIでビジネスロジックの実装
- バリデーションルール

**3.2 コパイロット活用**:
- テストデータ生成
- エッジケース処理
- ユーティリティ関数

**3.3 言語横断**:
- Python実装 → TypeScript変換（または逆）
- API仕様の自動生成

**4.1-4.3 リファクタリング**:
- コードの匂い検出（長いメソッド、重複など）
- AIによるリファクタリング提案
- 技術負債の可視化と返済

### Phase 2: ゲーム要素（第2部後半-第3部）

**追加機能**:
- 経験値・レベルシステム
- バッジ・称号
- ストリーク（連続達成日数）
- 統計ダッシュボード

### Phase 3: AI強化（第3部）

**5.1 TDD**:
- クエスト完了機能をTDDで実装
- 経験値計算のテスト
- ストリーク計算のテスト

**5.2 AIテスト生成**:
- エッジケースの自動生成
- 境界値テスト
- 異常系テスト

**5.3 カオスエンジニアリング**:
- データベース障害時の挙動
- ネットワーク遅延時の挙動

**6.1-6.3 デプロイと運用**:
- CI/CDパイプライン
- ログ監視
- ユーザーフィードバック収集

### Phase 4: チーム機能（第4部）

**7.1 チーム開発**:
- Party（パーティ）機能
- 共同クエスト
- リーダーボード

**7.2 Git協働**:
- フィーチャーブランチ戦略
- プルリクエストレビュー
- コンフリクト解決

**8.1-8.2 倫理と継続**:
- ゲーミフィケーションの適切な使い方
- 依存症にならない設計
- オープンソース化

---

## 📊 データモデル

### エンティティ定義

#### Quest（クエスト）

```python
class Quest:
    """クエスト（タスク）エンティティ"""

    id: UUID
    title: str  # タイトル
    description: str  # 説明
    category: QuestCategory  # カテゴリ
    difficulty: DifficultyLevel  # 難易度
    experience_points: int  # 獲得経験値
    status: QuestStatus  # ステータス
    hero_id: UUID  # 担当者
    due_date: datetime | None  # 期限
    created_at: datetime
    completed_at: datetime | None

    # ビジネスルール
    def complete(self) -> Reward
    def estimate_effort(self) -> timedelta
    def is_overdue(self) -> bool
```

#### Hero（ヒーロー）

```python
class Hero:
    """ヒーロー（ユーザー）エンティティ"""

    id: UUID
    name: str
    email: str
    level: int  # レベル
    total_experience: int  # 総経験値
    current_streak: int  # 連続達成日数
    badges: list[Badge]  # バッジ
    created_at: datetime

    # ビジネスルール
    def gain_experience(self, points: int) -> LevelUpResult
    def complete_quest(self, quest: Quest) -> Reward
    def calculate_level(self) -> int
```

#### QuestCategory（カテゴリ）

```python
class QuestCategory(Enum):
    """クエストカテゴリ"""
    DAILY = "daily"  # デイリークエスト
    WEEKLY = "weekly"  # ウィークリー
    EPIC = "epic"  # エピック（大規模）
    SIDE = "side"  # サイドクエスト
```

#### DifficultyLevel（難易度）

```python
class DifficultyLevel(Enum):
    """難易度レベル"""
    TRIVIAL = (1, 10)  # 簡単（経験値10）
    EASY = (2, 25)
    NORMAL = (3, 50)
    HARD = (4, 100)
    EPIC = (5, 250)

    def __init__(self, rank: int, exp: int):
        self.rank = rank
        self.base_exp = exp
```

#### QuestStatus（ステータス）

```python
class QuestStatus(Enum):
    """クエストステータス"""
    AVAILABLE = "available"  # 利用可能
    IN_PROGRESS = "in_progress"  # 進行中
    COMPLETED = "completed"  # 完了
    FAILED = "failed"  # 失敗
    CANCELLED = "cancelled"  # キャンセル
```

---

## 🏗 アーキテクチャ

### レイヤー構造

```
questforge/
├── presentation/      # UI層（CLI/Web）
│   ├── cli/          # コマンドラインインターフェース
│   └── web/          # Webインターフェース（オプション）
│
├── application/       # アプリケーション層
│   ├── use_cases/    # ユースケース
│   └── services/     # アプリケーションサービス
│
├── domain/           # ドメイン層
│   ├── entities/     # エンティティ
│   ├── value_objects/  # 値オブジェクト
│   └── repositories/   # リポジトリインターフェース
│
├── infrastructure/   # インフラ層
│   ├── persistence/  # データベース実装
│   ├── ai/          # AI統合
│   └── external/    # 外部API
│
└── tests/           # テスト
    ├── unit/
    ├── integration/
    └── e2e/
```

### 主要ユースケース

```python
# 第1-2部で実装
- CreateQuestUseCase: クエスト作成
- CompleteQuestUseCase: クエスト完了
- ListQuestsUseCase: クエスト一覧表示
- UpdateQuestUseCase: クエスト更新
- DeleteQuestUseCase: クエスト削除

# 第2部後半で追加
- GainExperienceUseCase: 経験値獲得
- CalculateLevelUseCase: レベル計算
- AwardBadgeUseCase: バッジ授与

# 第3部で追加
- GenerateQuestSuggestionsUseCase: AI提案
- PredictCompletionTimeUseCase: 完了時間予測
- AnalyzeProductivityUseCase: 生産性分析

# 第4部で追加
- CreatePartyUseCase: パーティ作成
- ShareQuestUseCase: クエスト共有
- CollaborateOnQuestUseCase: 共同作業
```

---

## 🤖 AI活用ポイント

### 各章でのAI活用例

**第1章（要求工学）**:
```
AIペルソナとの対話:
- 「タスク管理で困っていることは？」
- 「どんな報酬があったら嬉しい？」
- 「チーム機能で何が必要？」
```

**第2章（設計）**:
```
AIでパターン提案:
- 「このユースケースに適したデザインパターンは？」
- 「アーキテクチャの改善点は？」
```

**第3章（実装）**:
```
AIでコード生成:
- 「CompleteQuestUseCaseを実装して」
- 「経験値計算ロジックを生成して」
```

**第4章（リファクタリング）**:
```
AIでコードレビュー:
- 「このコードの問題点は？」
- 「よりエレガントな書き方は？」
```

**第5章（テスト）**:
```
AIでテスト生成:
- 「このメソッドのエッジケースは？」
- 「境界値テストを生成して」
```

**第6章（運用）**:
```
AIで異常検知:
- 「このログパターンは異常？」
- 「パフォーマンス改善の提案は？」
```

---

## 🎨 UI/UX（CLI版）

### コマンド例

```bash
# クエスト作成
$ questforge quest create "プロローグを書く" --difficulty hard --category epic

# クエスト一覧
$ questforge quest list
┌────┬──────────────────┬──────────┬────────┬────────┐
│ ID │ Title            │ Category │ Diff   │ Status │
├────┼──────────────────┼──────────┼────────┼────────┤
│ 1  │ プロローグを書く │ epic     │ hard   │ done   │
│ 2  │ 第1章を書く      │ epic     │ hard   │ todo   │
└────┴──────────────────┴──────────┴────────┴────────┘

# クエスト完了
$ questforge quest complete 1
🎉 Quest completed!
💎 +100 XP
⭐ Level up! You are now level 5!
🏆 Badge unlocked: "First Epic Quest"

# ステータス表示
$ questforge hero status
Hero: Alice the Alchemist
Level: 5 (450/500 XP)
Streak: 7 days 🔥
Badges: 3
Completed Quests: 12

# AI提案
$ questforge ai suggest
🤖 Based on your pattern, here are suggested quests:
1. "Write Chapter 1 Section 1" (hard, +100 XP)
2. "Review and refactor code" (normal, +50 XP)
3. "Update progress.md" (easy, +25 XP)
```

---

## 📈 段階的な実装計画

### Milestone 1: MVP（第1-2部）
- ✅ Quest CRUD
- ✅ Basic Hero management
- ✅ Experience points system
- ✅ CLI interface

### Milestone 2: Gamification（第2部後半）
- ✅ Leveling system
- ✅ Badges and achievements
- ✅ Streak tracking
- ✅ Statistics dashboard

### Milestone 3: AI Integration（第3部）
- ✅ Quest suggestions
- ✅ Difficulty estimation
- ✅ Productivity analytics
- ✅ Smart reminders

### Milestone 4: Team Features（第4部）
- ✅ Party system
- ✅ Shared quests
- ✅ Leaderboard
- ✅ Collaboration tools

---

## 🛠 技術スタック

### Phase 1（第1-2部）
- **言語**: Python 3.11+
- **CLI**: Click または Typer
- **DB**: SQLite（シンプル）
- **ORM**: SQLAlchemy
- **テスト**: pytest

### Phase 2（第3部）
- **AI**: OpenAI API / Anthropic API
- **CI/CD**: GitHub Actions
- **Monitoring**: 簡易ログシステム

### Phase 3（第4部）
- **Web（オプション）**: FastAPI + React
- **Deploy**: Docker + Railway/Render

---

## 📝 サンプルデータ

### 初期シードデータ

```python
# ヒーロー
heroes = [
    Hero(name="Alice the Alchemist", email="alice@example.com"),
    Hero(name="Bob the Builder", email="bob@example.com"),
]

# クエスト例
quests = [
    Quest(
        title="Write the prologue",
        description="Complete the first section of the book",
        category=QuestCategory.EPIC,
        difficulty=DifficultyLevel.HARD,
        hero_id=heroes[0].id,
    ),
    Quest(
        title="Morning code review",
        description="Review yesterday's pull requests",
        category=QuestCategory.DAILY,
        difficulty=DifficultyLevel.EASY,
        hero_id=heroes[0].id,
    ),
]

# バッジ
badges = [
    Badge(name="First Quest", description="Complete your first quest"),
    Badge(name="Epic Hero", description="Complete 10 epic quests"),
    Badge(name="Week Warrior", description="7-day streak"),
]
```

---

## 🎯 学習目標との対応

この題材を通じて、読者は以下を学びます：

**第1部**:
- 要求の引き出し方
- ドメインモデリング
- クラス設計
- アーキテクチャパターン

**第2部**:
- AI支援コーディング
- リファクタリング技術
- コード品質の向上

**第3部**:
- TDD実践
- テスト戦略
- CI/CD構築
- 運用監視

**第4部**:
- チーム開発
- Git協働
- 継続的改善

---

## ✅ 次のアクション

1. [ ] ドメインモデルの実装開始
2. [ ] 初期ディレクトリ構造作成
3. [ ] 第1章で使用するコード例の準備
4. [ ] シードデータの作成

---

**Version**: 1.0
**Last Updated**: 2026-01-18
**Status**: Draft → Ready for Implementation
