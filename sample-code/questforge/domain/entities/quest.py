"""クエスト（タスク）エンティティ

このモジュールは、QuestForgeシステムの中核となるクエスト（タスク）を表現します。
第1章で設計し、第2章で実装、第3章でテスト、第4章でリファクタリングします。
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from uuid import UUID, uuid4


class QuestCategory(Enum):
    """クエストカテゴリ

    タスクの種類を分類します。
    RPGゲームの「クエストタイプ」に相当します。
    """
    DAILY = "daily"  # デイリークエスト（毎日の小タスク）
    WEEKLY = "weekly"  # ウィークリークエスト
    EPIC = "epic"  # エピッククエスト（大規模タスク）
    SIDE = "side"  # サイドクエスト（オプショナル）


class DifficultyLevel(Enum):
    """難易度レベル

    クエストの難しさと、それに応じた報酬（経験値）を定義します。
    """
    TRIVIAL = (1, 10)  # 簡単（5分以内、経験値10）
    EASY = (2, 25)  # 易しい（30分程度、経験値25）
    NORMAL = (3, 50)  # 普通（1-2時間、経験値50）
    HARD = (4, 100)  # 難しい（半日、経験値100）
    EPIC = (5, 250)  # 超難関（数日、経験値250）

    def __init__(self, rank: int, base_exp: int):
        self.rank = rank
        self.base_exp = base_exp


from ..exceptions import InvalidQuestStateError


class QuestStatus(str, Enum):
    """クエストステータス

    クエストの現在の状態を表します。
    """
    AVAILABLE = "AVAILABLE"  # 利用可能（まだ着手していない）
    IN_PROGRESS = "IN_PROGRESS"  # 進行中
    COMPLETED = "COMPLETED"  # 完了
    FAILED = "FAILED"  # 失敗（期限切れなど）
    CANCELLED = "CANCELLED"  # キャンセル


@dataclass
class Quest:
    """クエスト（タスク）エンティティ
    # ... (省略)
    """

    # 必須フィールド
    title: str
    description: str
    category: QuestCategory
    difficulty: DifficultyLevel
    hero_id: UUID

    # 自動生成フィールド
    id: UUID = field(default_factory=uuid4)
    experience_points: int = field(init=False)
    status: QuestStatus = field(default=QuestStatus.AVAILABLE)
    created_at: datetime = field(default_factory=datetime.now)

    # オプショナルフィールド
    due_date: datetime | None = None
    completed_at: datetime | None = None

    def __post_init__(self):
        """初期化後の処理

        経験値を難易度から自動計算します。
        """
        self.experience_points = self.difficulty.base_exp

    def start(self) -> None:
        """クエストを開始する

        ステータスをIN_PROGRESSに変更します。

        Raises:
            InvalidQuestStateError: すでに開始済みまたは完了済みの場合
        """
        if self.status != QuestStatus.AVAILABLE:
            raise InvalidQuestStateError(
                f"Cannot start quest in status {self.status}. "
                "Quest must be AVAILABLE."
            )
        self.status = QuestStatus.IN_PROGRESS

    def complete(self) -> int:
        """クエストを完了する

        ステータスをCOMPLETEDに変更し、完了時刻を記録します。

        Returns:
            獲得した経験値

        Raises:
            InvalidQuestStateError: 進行中でない場合
        """
        if self.status != QuestStatus.IN_PROGRESS:
            raise InvalidQuestStateError(
                f"Cannot complete quest in status {self.status}. "
                "Quest must be IN_PROGRESS."
            )

        self.status = QuestStatus.COMPLETED
        self.completed_at = datetime.now()

        # ボーナス経験値の計算（期限前完了など）
        bonus = self._calculate_bonus()
        total_exp = self.experience_points + bonus

        return total_exp

    def cancel(self) -> None:
        """クエストをキャンセルする

        ステータスをCANCELLEDに変更します。
        """
        if self.status == QuestStatus.COMPLETED:
            raise InvalidQuestStateError("Cannot cancel completed quest.")

        self.status = QuestStatus.CANCELLED

    def fail(self) -> None:
        """クエストを失敗にする

        期限切れなどの場合に呼び出されます。
        """
        if self.status == QuestStatus.COMPLETED:
            raise InvalidQuestStateError("Cannot fail completed quest.")

        self.status = QuestStatus.FAILED

    def is_overdue(self) -> bool:
        """期限切れかどうかを判定

        Returns:
            期限が設定されており、かつ現在時刻が期限を過ぎている場合True
        """
        if self.due_date is None:
            return False

        return datetime.now() > self.due_date and self.status != QuestStatus.COMPLETED

    def estimate_effort(self) -> timedelta:
        """必要な作業時間を推定

        難易度から、おおよその作業時間を推定します。

        Returns:
            推定作業時間
        """
        # 難易度に応じた推定時間（簡易版）
        effort_map = {
            DifficultyLevel.TRIVIAL: timedelta(minutes=5),
            DifficultyLevel.EASY: timedelta(minutes=30),
            DifficultyLevel.NORMAL: timedelta(hours=2),
            DifficultyLevel.HARD: timedelta(hours=4),
            DifficultyLevel.EPIC: timedelta(days=1),
        }
        return effort_map[self.difficulty]

    def _calculate_bonus(self) -> int:
        """ボーナス経験値を計算

        期限前に完了した場合などにボーナスを付与します。

        Returns:
            ボーナス経験値
        """
        bonus = 0

        # 期限前完了ボーナス
        if self.due_date and self.completed_at:
            if self.completed_at < self.due_date:
                # 期限までの残り時間に応じてボーナス
                time_saved = self.due_date - self.completed_at
                if time_saved > timedelta(days=1):
                    bonus += 50  # 1日以上前に完了
                elif time_saved > timedelta(hours=6):
                    bonus += 25  # 6時間以上前に完了

        return bonus

    def __str__(self) -> str:
        """文字列表現

        Returns:
            クエストの簡潔な説明
        """
        status_emoji = {
            QuestStatus.AVAILABLE: "📋",
            QuestStatus.IN_PROGRESS: "⚔️",
            QuestStatus.COMPLETED: "✅",
            QuestStatus.FAILED: "❌",
            QuestStatus.CANCELLED: "🚫",
        }

        emoji = status_emoji[self.status]
        return f"{emoji} {self.title} ({self.difficulty.name}, {self.experience_points}XP)"
