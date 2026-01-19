"""ヒーロー進捗確認ユースケース

ヒーローの進捗情報を取得する業務処理を定義します。
"""

from dataclasses import dataclass
from uuid import UUID

from ...domain.repositories.hero_repository import HeroRepository
from ...domain.repositories.quest_repository import QuestRepository
from ...domain.entities.quest import QuestStatus


@dataclass
class ViewHeroProgressInput:
    """進捗確認の入力データ

    Attributes:
        hero_id: ヒーローID
    """

    hero_id: UUID


@dataclass
class ViewHeroProgressOutput:
    """進捗確認の出力データ

    Attributes:
        hero_name: ヒーロー名
        level: 現在のレベル
        total_experience: 累計経験値
        exp_to_next_level: 次のレベルまでに必要な経験値
        level_progress: レベル内進捗率（0.0〜1.0）
        current_streak: 現在の連続達成日数
        best_streak: 最高連続達成記録
        quests_in_progress: 進行中のクエスト数
        quests_completed: 完了したクエスト数
    """

    hero_name: str
    level: int
    total_experience: int
    exp_to_next_level: int
    level_progress: float
    current_streak: int
    best_streak: int
    quests_in_progress: int
    quests_completed: int


class ViewHeroProgressUseCase:
    """ヒーロー進捗確認ユースケース

    ヒーローの現在の状態と進捗を取得します。

    Example:
        >>> use_case = ViewHeroProgressUseCase(hero_repo, quest_repo)
        >>> input_data = ViewHeroProgressInput(hero_id=hero.id)
        >>> output = use_case.execute(input_data)
        >>> print(f"{output.hero_name} - Level {output.level}")
        >>> print(f"Progress: {output.level_progress:.1%}")
    """

    def __init__(
        self,
        hero_repository: HeroRepository,
        quest_repository: QuestRepository,
    ):
        """初期化

        Args:
            hero_repository: ヒーローリポジトリ
            quest_repository: クエストリポジトリ
        """
        self.hero_repository = hero_repository
        self.quest_repository = quest_repository

    def execute(self, input_data: ViewHeroProgressInput) -> ViewHeroProgressOutput:
        """ヒーローの進捗を取得する

        Args:
            input_data: ヒーローID

        Returns:
            ヒーローの進捗情報

        Raises:
            ValueError: ヒーローが存在しない場合
        """
        # ヒーローを取得
        hero = self.hero_repository.find_by_id(input_data.hero_id)
        if hero is None:
            raise ValueError(f"Hero not found: {input_data.hero_id}")

        # クエスト統計を取得
        in_progress_quests = self.quest_repository.find_by_status(
            hero.id, QuestStatus.IN_PROGRESS
        )
        completed_quests = self.quest_repository.find_by_status(
            hero.id, QuestStatus.COMPLETED
        )

        return ViewHeroProgressOutput(
            hero_name=hero.name,
            level=hero.level,
            total_experience=hero.total_experience,
            exp_to_next_level=hero.get_exp_to_next_level(),
            level_progress=hero.get_level_progress(),
            current_streak=hero.current_streak,
            best_streak=hero.best_streak,
            quests_in_progress=len(in_progress_quests),
            quests_completed=len(completed_quests),
        )
