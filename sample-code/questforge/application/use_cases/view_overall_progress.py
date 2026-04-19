"""全体進捗確認ユースケース

全ヒーロー・全クエストを横断した集計情報を提供します。
"""

from dataclasses import dataclass

from ...domain.repositories.hero_repository import HeroRepository
from ...domain.repositories.quest_repository import QuestRepository
from ...domain.entities.quest import QuestStatus


@dataclass
class ViewOverallProgressOutput:
    """全体進捗の出力データ"""

    total_heroes: int
    total_quests: int
    quests_completed: int
    quests_in_progress: int
    average_level: float
    top_hero_name: str | None
    top_hero_level: int | None


class ViewOverallProgressUseCase:
    """全体進捗確認ユースケース"""

    def __init__(
        self,
        hero_repository: HeroRepository,
        quest_repository: QuestRepository,
    ) -> None:
        self.hero_repository = hero_repository
        self.quest_repository = quest_repository

    def execute(self) -> ViewOverallProgressOutput:
        heroes = self.hero_repository.list_all()
        quests = self.quest_repository.list_all()

        total_heroes = len(heroes)
        total_quests = len(quests)
        quests_completed = len([q for q in quests if q.status == QuestStatus.COMPLETED])
        quests_in_progress = len([q for q in quests if q.status == QuestStatus.IN_PROGRESS])

        average_level = (
            sum(h.level for h in heroes) / total_heroes if total_heroes > 0 else 0.0
        )
        top_hero = max(heroes, key=lambda h: h.level, default=None)

        return ViewOverallProgressOutput(
            total_heroes=total_heroes,
            total_quests=total_quests,
            quests_completed=quests_completed,
            quests_in_progress=quests_in_progress,
            average_level=average_level,
            top_hero_name=top_hero.name if top_hero else None,
            top_hero_level=top_hero.level if top_hero else None,
        )

