"""バッジ（実績）エンティティ

ヒーローが獲得できるバッジを表現します。
"""

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Badge:
    """バッジ（実績）

    特定の条件を満たすことで獲得できるバッジを表現します。

    Attributes:
        id: バッジの一意識別子
        name: バッジ名（例: "First Quest"）
        description: バッジの説明
        icon: アイコン（絵文字）
        rarity: レア度（common, rare, epic, legendary）

    Example:
        >>> badge = Badge(
        ...     name="First Quest",
        ...     description="Complete your first quest",
        ...     icon="🎯"
        ... )
    """

    name: str
    description: str
    icon: str = "🏆"
    rarity: str = "common"
    id: UUID = field(default_factory=uuid4)

    def __str__(self) -> str:
        """文字列表現"""
        return f"{self.icon} {self.name}"
