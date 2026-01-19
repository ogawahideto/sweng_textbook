"""バッジリポジトリインターフェース

バッジのデータアクセスインターフェースを定義します。
"""

from abc import ABC, abstractmethod
from uuid import UUID

from ..entities.badge import Badge


class BadgeRepository(ABC):
    """バッジリポジトリインターフェース

    バッジの永続化を抽象化します。
    """

    @abstractmethod
    def save(self, badge: Badge) -> None:
        """バッジを保存する

        Args:
            badge: 保存するバッジ
        """
        pass

    @abstractmethod
    def find_by_id(self, badge_id: UUID) -> Badge | None:
        """IDでバッジを検索する

        Args:
            badge_id: バッジID

        Returns:
            見つかったバッジ。存在しない場合はNone
        """
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> Badge | None:
        """名前でバッジを検索する

        Args:
            name: バッジ名

        Returns:
            見つかったバッジ。存在しない場合はNone
        """
        pass

    @abstractmethod
    def list_all(self) -> list[Badge]:
        """全バッジを取得する

        Returns:
            全バッジのリスト
        """
        pass
