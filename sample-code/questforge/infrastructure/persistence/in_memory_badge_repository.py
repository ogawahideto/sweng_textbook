"""インメモリバッジリポジトリ実装

メモリ上にデータを保存する、テスト用の実装です。
"""

from uuid import UUID

from ...domain.entities.badge import Badge
from ...domain.repositories.badge_repository import BadgeRepository


class InMemoryBadgeRepository(BadgeRepository):
    """インメモリバッジリポジトリ

    辞書を使ってメモリ上にバッジを保存します。
    """

    def __init__(self):
        """初期化"""
        self._badges: dict[UUID, Badge] = {}

    def save(self, badge: Badge) -> None:
        """バッジを保存する"""
        self._badges[badge.id] = badge

    def find_by_id(self, badge_id: UUID) -> Badge | None:
        """IDでバッジを検索する"""
        return self._badges.get(badge_id)

    def find_by_name(self, name: str) -> Badge | None:
        """名前でバッジを検索する"""
        for badge in self._badges.values():
            if badge.name == name:
                return badge
        return None

    def list_all(self) -> list[Badge]:
        """全バッジを取得する"""
        return list(self._badges.values())
