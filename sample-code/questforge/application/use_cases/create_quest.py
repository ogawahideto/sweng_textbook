"""クエスト作成ユースケース

新しいクエストを作成する業務処理を定義します。
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from ...domain.entities.quest import Quest, QuestCategory, DifficultyLevel
from ...domain.repositories.quest_repository import QuestRepository
from ...domain.repositories.hero_repository import HeroRepository


@dataclass
class CreateQuestInput:
    """クエスト作成の入力データ

    Attributes:
        title: クエストタイトル
        description: クエストの詳細説明
        category: カテゴリ
        difficulty: 難易度
        hero_id: 担当ヒーローのID
        due_date: 期限（オプション）
    """

    title: str
    description: str
    category: QuestCategory
    difficulty: DifficultyLevel
    hero_id: UUID
    due_date: datetime | None = None


@dataclass
class CreateQuestOutput:
    """クエスト作成の出力データ

    Attributes:
        quest_id: 作成されたクエストのID
        experience_points: 獲得できる経験値
    """

    quest_id: UUID
    experience_points: int


class CreateQuestUseCase:
    """クエスト作成ユースケース

    新しいクエストを作成し、データベースに保存します。

    Example:
        >>> quest_repo = InMemoryQuestRepository()
        >>> hero_repo = InMemoryHeroRepository()
        >>> use_case = CreateQuestUseCase(quest_repo, hero_repo)
        >>> input_data = CreateQuestInput(
        ...     title="第1章を書く",
        ...     description="要求工学の章を執筆",
        ...     category=QuestCategory.EPIC,
        ...     difficulty=DifficultyLevel.HARD,
        ...     hero_id=hero.id
        ... )
        >>> output = use_case.execute(input_data)
        >>> print(f"Quest created: {output.quest_id}")
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
        self.quest_repository = quest_repository
        self.hero_repository = hero_repository

    def execute(self, input_data: CreateQuestInput) -> CreateQuestOutput:
        """クエストを作成する

        Args:
            input_data: 作成するクエストの情報

        Returns:
            作成されたクエストの情報

        Raises:
            ValueError: ヒーローが存在しない場合
        """
        # ヒーローの存在確認
        hero = self.hero_repository.find_by_id(input_data.hero_id)
        if hero is None:
            raise ValueError(f"Hero not found: {input_data.hero_id}")

        # クエストを作成
        quest = Quest(
            title=input_data.title,
            description=input_data.description,
            category=input_data.category,
            difficulty=input_data.difficulty,
            hero_id=input_data.hero_id,
            due_date=input_data.due_date,
        )

        # 保存
        self.quest_repository.save(quest)

        return CreateQuestOutput(
            quest_id=quest.id,
            experience_points=quest.experience_points,
        )
