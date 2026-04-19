"""クエストリポジトリインターフェース

データの永続化方法に依存しない、抽象的なデータアクセスインターフェースを定義します。
"""

from abc import ABC, abstractmethod
from uuid import UUID

from ..entities.quest import Quest, QuestStatus


class QuestRepository(ABC):
    """クエストリポジトリインターフェース

    クエストの永続化を抽象化します。
    実装はインフラストラクチャ層で行います（例: SQLiteRepository, InMemoryRepository）。
    """

    @abstractmethod
    def save(self, quest: Quest) -> None:
        """クエストを保存する

        Args:
            quest: 保存するクエスト
        """
        pass

    @abstractmethod
    def find_by_id(self, quest_id: UUID) -> Quest | None:
        """IDでクエストを検索する

        Args:
            quest_id: クエストID

        Returns:
            見つかったクエスト。存在しない場合はNone
        """
        pass

    @abstractmethod
    def find_by_hero_id(self, hero_id: UUID) -> list[Quest]:
        """ヒーローIDで全クエストを検索する

        Args:
            hero_id: ヒーローID

        Returns:
            そのヒーローに割り当てられた全クエストのリスト
        """
        pass

    @abstractmethod
    def find_by_status(self, hero_id: UUID, status: QuestStatus) -> list[Quest]:
        """ステータスでクエストを絞り込む

        Args:
            hero_id: ヒーローID
            status: クエストステータス

        Returns:
            指定されたステータスのクエストリスト
        """
        pass

    @abstractmethod
    def delete(self, quest_id: UUID) -> None:
        """クエストを削除する

        Args:
            quest_id: 削除するクエストのID
        """
        pass

    @abstractmethod
    def list_all(self) -> list[Quest]:
        """全クエストを取得する

        Returns:
            全クエストのリスト
        """
        pass
