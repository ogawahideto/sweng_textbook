"""ヒーローリポジトリインターフェース

ヒーローのデータアクセスインターフェースを定義します。
"""

from abc import ABC, abstractmethod
from uuid import UUID

from ..entities.hero import Hero


class HeroRepository(ABC):
    """ヒーローリポジトリインターフェース

    ヒーローの永続化を抽象化します。
    """

    @abstractmethod
    def save(self, hero: Hero) -> None:
        """ヒーローを保存する

        Args:
            hero: 保存するヒーロー
        """
        pass

    @abstractmethod
    def find_by_id(self, hero_id: UUID) -> Hero | None:
        """IDでヒーローを検索する

        Args:
            hero_id: ヒーローID

        Returns:
            見つかったヒーロー。存在しない場合はNone
        """
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Hero | None:
        """メールアドレスでヒーローを検索する

        Args:
            email: メールアドレス

        Returns:
            見つかったヒーロー。存在しない場合はNone
        """
        pass

    @abstractmethod
    def delete(self, hero_id: UUID) -> None:
        """ヒーローを削除する

        Args:
            hero_id: 削除するヒーローのID
        """
        pass

    @abstractmethod
    def list_all(self) -> list[Hero]:
        """全ヒーローを取得する

        Returns:
            全ヒーローのリスト
        """
        pass
