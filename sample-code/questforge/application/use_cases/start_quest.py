"""クエスト開始ユースケース

クエストを開始状態にする業務処理を定義します。
"""

from dataclasses import dataclass
from uuid import UUID

from ...domain.repositories.quest_repository import QuestRepository


@dataclass
class StartQuestInput:
    """クエスト開始の入力データ

    Attributes:
        quest_id: 開始するクエストのID
    """

    quest_id: UUID


@dataclass
class StartQuestOutput:
    """クエスト開始の出力データ

    Attributes:
        quest_id: 開始したクエストのID
        title: クエストタイトル
    """

    quest_id: UUID
    title: str


class StartQuestUseCase:
    """クエスト開始ユースケース

    クエストのステータスをIN_PROGRESSに変更します。

    Example:
        >>> use_case = StartQuestUseCase(quest_repo)
        >>> input_data = StartQuestInput(quest_id=quest.id)
        >>> output = use_case.execute(input_data)
        >>> print(f"Started: {output.title}")
    """

    def __init__(self, quest_repository: QuestRepository):
        """初期化

        Args:
            quest_repository: クエストリポジトリ
        """
        self.quest_repository = quest_repository

    def execute(self, input_data: StartQuestInput) -> StartQuestOutput:
        """クエストを開始する

        Args:
            input_data: 開始するクエストの情報

        Returns:
            開始したクエストの情報

        Raises:
            ValueError: クエストが存在しない、または開始できない状態の場合
        """
        # クエストを取得
        quest = self.quest_repository.find_by_id(input_data.quest_id)
        if quest is None:
            raise ValueError(f"Quest not found: {input_data.quest_id}")

        # クエストを開始（エンティティ内でバリデーション）
        quest.start()

        # 保存
        self.quest_repository.save(quest)

        return StartQuestOutput(
            quest_id=quest.id,
            title=quest.title,
        )
