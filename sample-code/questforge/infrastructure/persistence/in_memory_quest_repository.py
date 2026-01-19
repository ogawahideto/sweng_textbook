"""インメモリクエストリポジトリ実装

メモリ上にデータを保存する、テスト用の実装です。
"""

from uuid import UUID

from ...domain.entities.quest import Quest, QuestStatus
from ...domain.repositories.quest_repository import QuestRepository


class InMemoryQuestRepository(QuestRepository):
    """インメモリクエストリポジトリ

    辞書を使ってメモリ上にクエストを保存します。
    本番環境では、SQLiteやPostgreSQLなどのデータベースを使用します。
    """

    def __init__(self):
        """初期化"""
        self._quests: dict[UUID, Quest] = {}

    def save(self, quest: Quest) -> None:
        """クエストを保存する"""
        self._quests[quest.id] = quest

    def find_by_id(self, quest_id: UUID) -> Quest | None:
        """IDでクエストを検索する"""
        return self._quests.get(quest_id)

    def find_by_hero_id(self, hero_id: UUID) -> list[Quest]:
        """ヒーローIDで全クエストを検索する"""
        return [q for q in self._quests.values() if q.hero_id == hero_id]

    def find_by_status(self, hero_id: UUID, status: QuestStatus) -> list[Quest]:
        """ステータスでクエストを絞り込む"""
        return [
            q
            for q in self._quests.values()
            if q.hero_id == hero_id and q.status == status
        ]

    def delete(self, quest_id: UUID) -> None:
        """クエストを削除する"""
        if quest_id in self._quests:
            del self._quests[quest_id]

    def list_all(self) -> list[Quest]:
        """全クエストを取得する"""
        return list(self._quests.values())
