"""報酬エンティティ

クエスト完了時に付与される報酬を表現します。
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class Reward:
    """報酬

    クエスト完了時に獲得できる報酬を表現します。

    Attributes:
        experience_points: 獲得経験値
        quest_id: 完了したクエストのID
        hero_id: 報酬を受け取るヒーローのID
        badge_id: 獲得したバッジのID（ある場合）
    """

    experience_points: int
    quest_id: UUID
    hero_id: UUID
    badge_id: UUID | None = None

    def __str__(self) -> str:
        """文字列表現"""
        msg = f"💎 +{self.experience_points} XP"
        if self.badge_id:
            msg += " 🏆 Badge unlocked!"
        return msg
