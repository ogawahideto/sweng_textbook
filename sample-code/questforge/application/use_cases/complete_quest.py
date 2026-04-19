"""クエスト完了ユースケース

クエストを完了し、ヒーローに経験値を付与する業務処理を定義します。
"""

from dataclasses import dataclass
from uuid import UUID

from ...domain.entities.reward import Reward
from ...domain.repositories.quest_repository import QuestRepository
from ...domain.repositories.hero_repository import HeroRepository


@dataclass
class CompleteQuestInput:
    """クエスト完了の入力データ

    Attributes:
        quest_id: 完了するクエストのID
    """

    quest_id: UUID


@dataclass
class CompleteQuestOutput:
    """クエスト完了の出力データ

    Attributes:
        reward: 獲得した報酬
        leveled_up: レベルアップしたか
        new_level: 新しいレベル
    """

    reward: Reward
    leveled_up: bool
    new_level: int


class CompleteQuestUseCase:
    """クエスト完了ユースケース

    クエストを完了し、ヒーローに経験値を付与します。
    レベルアップが発生した場合は、その情報も返します。

    Example:
        >>> use_case = CompleteQuestUseCase(quest_repo, hero_repo)
        >>> input_data = CompleteQuestInput(quest_id=quest.id)
        >>> output = use_case.execute(input_data)
        >>> if output.leveled_up:
        ...     print(f"Level up! Now level {output.new_level}")
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

    def execute(self, input_data: CompleteQuestInput) -> CompleteQuestOutput:
        """クエストを完了する

        Args:
            input_data: 完了するクエストの情報

        Returns:
            完了結果（報酬、レベルアップ情報）

        Raises:
            ValueError: クエストまたはヒーローが存在しない場合
        """
        # クエストを取得
        quest = self.quest_repository.find_by_id(input_data.quest_id)
        if quest is None:
            raise ValueError(f"Quest not found: {input_data.quest_id}")

        # ヒーローを取得
        hero = self.hero_repository.find_by_id(quest.hero_id)
        if hero is None:
            raise ValueError(f"Hero not found: {quest.hero_id}")

        # クエストを完了（経験値を計算）
        experience_points = quest.complete()

        # ヒーローに経験値を付与
        level_up_result = hero.gain_experience(experience_points)

        # 今日のクエスト完了を記録（ストリーク更新）
        hero.complete_quest_today()

        # 報酬を作成
        reward = Reward(
            experience_points=experience_points,
            quest_id=quest.id,
            hero_id=hero.id,
        )

        # 変更を保存
        self.quest_repository.save(quest)
        self.hero_repository.save(hero)

        return CompleteQuestOutput(
            reward=reward,
            leveled_up=level_up_result.leveled_up,
            new_level=level_up_result.new_level,
        )
