"""CLIコマンド実装

コマンドラインインターフェースで使用するコマンドを定義します。
"""

import sys
from datetime import datetime, timedelta
from uuid import UUID

from ..domain.entities.quest import QuestCategory, DifficultyLevel
from ..application.use_cases import (
    CreateHeroUseCase,
    CreateHeroInput,
    CreateQuestUseCase,
    CreateQuestInput,
    StartQuestUseCase,
    StartQuestInput,
    CompleteQuestUseCase,
    CompleteQuestInput,
    ViewHeroProgressUseCase,
    ViewHeroProgressInput,
)
from ..domain.repositories.quest_repository import QuestRepository
from ..domain.repositories.hero_repository import HeroRepository


def safe_print(text: str) -> None:
    """安全に出力する（絵文字のエンコーディングエラーを回避）

    Args:
        text: 出力するテキスト
    """
    try:
        print(text)
    except UnicodeEncodeError:
        # 絵文字を?に置き換えて出力
        print(text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))


class QuestForgeCLI:
    """QuestForge CLIアプリケーション

    コマンドラインからQuestForgeを操作するためのインターフェースです。
    """

    def __init__(
        self,
        quest_repository: QuestRepository,
        hero_repository: HeroRepository,
    ):
        """初期化

        Args:
            quest_repository: クエストリポジトリ
            hero_repository: ヒーローリポジトリ
        """
        self.quest_repo = quest_repository
        self.hero_repo = hero_repository

    def create_hero(self, name: str, email: str) -> None:
        """ヒーローを作成する

        Args:
            name: ヒーロー名
            email: メールアドレス
        """
        use_case = CreateHeroUseCase(self.hero_repo)
        input_data = CreateHeroInput(name=name, email=email)

        try:
            output = use_case.execute(input_data)
            safe_print(f"✨ Hero created: {output.name}")
            safe_print(f"   ID: {output.hero_id}")
        except ValueError as e:
            safe_print(f"❌ Error: {e}")

    def create_quest(
        self,
        hero_id: UUID,
        title: str,
        description: str,
        category: str,
        difficulty: str,
        due_days: int | None = None,
    ) -> None:
        """クエストを作成する

        Args:
            hero_id: ヒーローID
            title: タイトル
            description: 説明
            category: カテゴリ（daily, weekly, epic, side）
            difficulty: 難易度（trivial, easy, normal, hard, epic）
            due_days: 期限（何日後か）
        """
        use_case = CreateQuestUseCase(self.quest_repo, self.hero_repo)

        # Enumに変換
        quest_category = QuestCategory[category.upper()]
        quest_difficulty = DifficultyLevel[difficulty.upper()]

        # 期限の計算
        due_date = None
        if due_days is not None:
            due_date = datetime.now() + timedelta(days=due_days)

        input_data = CreateQuestInput(
            title=title,
            description=description,
            category=quest_category,
            difficulty=quest_difficulty,
            hero_id=hero_id,
            due_date=due_date,
        )

        try:
            output = use_case.execute(input_data)
            safe_print(f"📋 Quest created: {title}")
            safe_print(f"   XP: {output.experience_points}")
            safe_print(f"   ID: {output.quest_id}")
        except ValueError as e:
            safe_print(f"❌ Error: {e}")

    def start_quest(self, quest_id: UUID) -> None:
        """クエストを開始する

        Args:
            quest_id: クエストID
        """
        use_case = StartQuestUseCase(self.quest_repo)
        input_data = StartQuestInput(quest_id=quest_id)

        try:
            output = use_case.execute(input_data)
            safe_print(f"⚔️  Quest started: {output.title}")
        except ValueError as e:
            safe_print(f"❌ Error: {e}")

    def complete_quest(self, quest_id: UUID) -> None:
        """クエストを完了する

        Args:
            quest_id: クエストID
        """
        use_case = CompleteQuestUseCase(self.quest_repo, self.hero_repo)
        input_data = CompleteQuestInput(quest_id=quest_id)

        try:
            output = use_case.execute(input_data)
            safe_print(f"✅ Quest completed!")
            safe_print(f"   {output.reward}")

            if output.leveled_up:
                safe_print(f"🎉 Level up! Now level {output.new_level}!")
        except ValueError as e:
            safe_print(f"❌ Error: {e}")

    def show_progress(self, hero_id: UUID) -> None:
        """ヒーローの進捗を表示する

        Args:
            hero_id: ヒーローID
        """
        use_case = ViewHeroProgressUseCase(self.hero_repo, self.quest_repo)
        input_data = ViewHeroProgressInput(hero_id=hero_id)

        try:
            output = use_case.execute(input_data)

            safe_print(f"\n{'='*50}")
            safe_print(f"⚔️  {output.hero_name}")
            safe_print(f"{'='*50}")
            safe_print(f"Level: {output.level}")
            safe_print(f"Total XP: {output.total_experience}")
            safe_print(f"Progress: {output.level_progress:.1%} to level {output.level + 1}")
            safe_print(f"XP needed: {output.exp_to_next_level}")
            safe_print(f"\n🔥 Streak: {output.current_streak} days (best: {output.best_streak})")
            safe_print(f"\n📊 Quests:")
            safe_print(f"  In Progress: {output.quests_in_progress}")
            safe_print(f"  Completed: {output.quests_completed}")
            safe_print(f"{'='*50}\n")
        except ValueError as e:
            safe_print(f"❌ Error: {e}")

    def list_quests(self, hero_id: UUID) -> None:
        """クエスト一覧を表示する

        Args:
            hero_id: ヒーローID
        """
        quests = self.quest_repo.find_by_hero_id(hero_id)

        if not quests:
            safe_print("No quests found.")
            return

        safe_print(f"\n{'='*50}")
        safe_print(f"📋 Quest List")
        safe_print(f"{'='*50}")

        for quest in quests:
            safe_print(f"{quest}")
            if quest.is_overdue():
                safe_print(f"   ⚠️  OVERDUE!")

        safe_print(f"{'='*50}\n")
