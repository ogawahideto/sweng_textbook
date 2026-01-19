"""インメモリヒーローリポジトリ実装

メモリ上にデータを保存する、テスト用の実装です。
"""

from uuid import UUID

from ...domain.entities.hero import Hero
from ...domain.repositories.hero_repository import HeroRepository


class InMemoryHeroRepository(HeroRepository):
    """インメモリヒーローリポジトリ

    辞書を使ってメモリ上にヒーローを保存します。
    """

    def __init__(self):
        """初期化"""
        self._heroes: dict[UUID, Hero] = {}

    def save(self, hero: Hero) -> None:
        """ヒーローを保存する"""
        self._heroes[hero.id] = hero

    def find_by_id(self, hero_id: UUID) -> Hero | None:
        """IDでヒーローを検索する"""
        return self._heroes.get(hero_id)

    def find_by_email(self, email: str) -> Hero | None:
        """メールアドレスでヒーローを検索する"""
        for hero in self._heroes.values():
            if hero.email == email:
                return hero
        return None

    def delete(self, hero_id: UUID) -> None:
        """ヒーローを削除する"""
        if hero_id in self._heroes:
            del self._heroes[hero_id]

    def list_all(self) -> list[Hero]:
        """全ヒーローを取得する"""
        return list(self._heroes.values())
