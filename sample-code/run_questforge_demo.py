"""QuestForgeデモスクリプト実行

questforgeパッケージのデモを実行します。
"""

import sys
import io
from pathlib import Path

# Windows環境でのUTF-8出力を有効化
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# questforgeパッケージの親ディレクトリをパスに追加
sample_code_path = Path(__file__).parent
sys.path.insert(0, str(sample_code_path))

from questforge.infrastructure.persistence.in_memory_quest_repository import InMemoryQuestRepository
from questforge.infrastructure.persistence.in_memory_hero_repository import InMemoryHeroRepository
from questforge.cli.commands import QuestForgeCLI


def main():
    """デモを実行する"""
    print("\n" + "="*60)
    print("🎮 QuestForge Demo - タスク管理をRPG風に！")
    print("="*60 + "\n")

    # リポジトリの初期化
    quest_repo = InMemoryQuestRepository()
    hero_repo = InMemoryHeroRepository()

    # CLIの初期化
    cli = QuestForgeCLI(quest_repo, hero_repo)

    # 1. ヒーローを作成
    print("Step 1: ヒーローを作成")
    print("-" * 60)
    cli.create_hero("Alice the Alchemist", "alice@example.com")

    # ヒーローIDを取得（実際のアプリではログインなどで管理）
    heroes = hero_repo.list_all()
    alice = heroes[0]

    print("\n")

    # 2. クエストを作成
    print("Step 2: クエストを作成")
    print("-" * 60)
    cli.create_quest(
        alice.id,
        title="プロローグを書く",
        description="教科書のプロローグを執筆する",
        category="epic",
        difficulty="normal",
        due_days=7,
    )

    cli.create_quest(
        alice.id,
        title="コードレビューをする",
        description="チームメンバーのPRをレビュー",
        category="daily",
        difficulty="easy",
        due_days=1,
    )

    cli.create_quest(
        alice.id,
        title="ドメインモデルを設計する",
        description="QuestForgeのドメインモデルを設計",
        category="epic",
        difficulty="hard",
        due_days=3,
    )

    print("\n")

    # 3. クエスト一覧を表示
    print("Step 3: クエスト一覧を確認")
    print("-" * 60)
    cli.list_quests(alice.id)

    # 4. クエストを開始
    print("Step 4: クエストを開始")
    print("-" * 60)
    quests = quest_repo.find_by_hero_id(alice.id)
    first_quest = quests[0]
    cli.start_quest(first_quest.id)

    print("\n")

    # 5. クエストを完了
    print("Step 5: クエストを完了")
    print("-" * 60)
    cli.complete_quest(first_quest.id)

    print("\n")

    # 6. もう1つクエストを完了してレベルアップ
    print("Step 6: さらにクエストを完了してレベルアップ！")
    print("-" * 60)
    second_quest = quests[1]
    cli.start_quest(second_quest.id)
    cli.complete_quest(second_quest.id)

    print("\n")

    # 7. 進捗を確認
    print("Step 7: 進捗を確認")
    print("-" * 60)
    cli.show_progress(alice.id)

    # 8. クエスト一覧を再確認
    print("Step 8: クエスト一覧を再確認")
    print("-" * 60)
    cli.list_quests(alice.id)

    print("\n" + "="*60)
    print("✨ Demo completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
