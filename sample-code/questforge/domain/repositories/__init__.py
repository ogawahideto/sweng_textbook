"""リポジトリインターフェースモジュール"""

from .quest_repository import QuestRepository
from .hero_repository import HeroRepository
from .badge_repository import BadgeRepository

__all__ = [
    "QuestRepository",
    "HeroRepository",
    "BadgeRepository",
]
