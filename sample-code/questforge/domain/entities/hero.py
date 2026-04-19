"""ヒーロー（ユーザー）エンティティ

このモジュールは、QuestForgeを使用するユーザーを「ヒーロー」として表現します。
クエストを完了すると経験値を獲得し、レベルアップしていきます。
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from uuid import UUID, uuid4
from ..exceptions import DomainError


@dataclass
class LevelUpResult:
    """レベルアップ結果

    レベルアップしたかどうかと、新しいレベルを返します。
    """
    leveled_up: bool
    new_level: int
    previous_level: int


@dataclass
class Hero:
    """ヒーロー（ユーザー）エンティティ

    クエストを遂行し、経験値を獲得してレベルアップするユーザーを表現します。

    Attributes:
        id: ヒーローの一意識別子
        name: 名前（例: "Alice the Alchemist"）
        email: メールアドレス
        level: 現在のレベル
        total_experience: 累計経験値
        current_streak: 現在の連続達成日数
        best_streak: 最高連続達成記録
        last_quest_date: 最後にクエストを完了した日
        created_at: 作成日時

    Example:
        >>> hero = Hero(name="Alice", email="alice@example.com")
        >>> result = hero.gain_experience(100)
        >>> if result.leveled_up:
        ...     print(f"Level up! Now level {result.new_level}")
    """

    # 必須フィールド
    name: str
    email: str

    # 自動生成フィールド
    id: UUID = field(default_factory=uuid4)
    level: int = field(default=1)
    total_experience: int = field(default=0)
    current_streak: int = field(default=0)
    best_streak: int = field(default=0)
    created_at: datetime = field(default_factory=datetime.now)

    # 内部管理フィールド
    last_quest_date: date | None = field(default=None)

    def gain_experience(self, points: int) -> LevelUpResult:
        """経験値を獲得する

        経験値を加算し、必要に応じてレベルアップします。

        Args:
            points: 獲得する経験値

        Returns:
            レベルアップ結果

        Raises:
            DomainError: 経験値がマイナスの場合

        Example:
            >>> hero = Hero(name="Bob", email="bob@example.com")
            >>> result = hero.gain_experience(500)
            >>> print(result.leveled_up)  # レベルアップしたか
            True
        """
        if points < 0:
            raise DomainError("Experience points must be non-negative")

        previous_level = self.level
        self.total_experience += points

        # 新しいレベルを計算
        new_level = self._calculate_level(self.total_experience)

        leveled_up = new_level > previous_level
        if leveled_up:
            self.level = new_level

        return LevelUpResult(
            leveled_up=leveled_up,
            new_level=new_level,
            previous_level=previous_level,
        )

    def complete_quest_today(self) -> None:
        """今日クエストを完了したことを記録

        ストリーク（連続達成日数）を更新します。
        """
        today = date.today()

        if self.last_quest_date is None:
            # 初回クエスト
            self.current_streak = 1
            self.best_streak = 1
        elif self.last_quest_date == today:
            # 今日すでに完了済み（ストリークは変更なし）
            pass
        elif self._is_consecutive_day(self.last_quest_date, today):
            # 連続している
            self.current_streak += 1
            if self.current_streak > self.best_streak:
                self.best_streak = self.current_streak
        else:
            # 連続が途切れた
            self.current_streak = 1

        self.last_quest_date = today

    def get_next_level_exp(self) -> int:
        """次のレベルまでに必要な経験値を取得

        Returns:
            次のレベルに到達するために必要な総経験値
        """
        return self._exp_for_level(self.level + 1)

    def get_exp_to_next_level(self) -> int:
        """次のレベルまでに必要な残り経験値を取得

        Returns:
            次のレベルまであと何経験値必要か
        """
        return self.get_next_level_exp() - self.total_experience

    def get_level_progress(self) -> float:
        """現在のレベル内での進捗率を取得

        Returns:
            進捗率（0.0〜1.0）

        Example:
            >>> hero = Hero(name="Alice", email="alice@example.com")
            >>> hero.total_experience = 250  # Level 2の途中
            >>> progress = hero.get_level_progress()
            >>> print(f"{progress:.1%}")  # 例: 50.0%
        """
        current_level_exp = self._exp_for_level(self.level)
        next_level_exp = self._exp_for_level(self.level + 1)

        if next_level_exp == current_level_exp:
            return 1.0

        exp_in_current_level = self.total_experience - current_level_exp
        exp_needed_for_level = next_level_exp - current_level_exp

        return exp_in_current_level / exp_needed_for_level

    @staticmethod
    def _calculate_level(total_exp: int) -> int:
        """累計経験値からレベルを計算

        Args:
            total_exp: 累計経験値

        Returns:
            現在のレベル

        Note:
            レベル計算式は様々なバリエーションがあります。
            ここでは簡易的に「二次関数」を使用しています。
            レベルN到達に必要な経験値 = 100 * N^1.5
        """
        level = 1
        while total_exp >= Hero._exp_for_level(level + 1):
            level += 1
        return level

    @staticmethod
    def _exp_for_level(level: int) -> int:
        """指定レベルに到達するために必要な累計経験値

        Args:
            level: レベル

        Returns:
            そのレベルに到達するために必要な累計経験値

        Example:
            Level 1: 0 XP
            Level 2: 100 XP
            Level 3: 283 XP
            Level 4: 519 XP
            Level 5: 806 XP
        """
        if level <= 1:
            return 0
        return int(100 * (level ** 1.5))

    @staticmethod
    def _is_consecutive_day(last_date: date, current_date: date) -> bool:
        """2つの日付が連続しているか判定

        Args:
            last_date: 前回の日付
            current_date: 今回の日付

        Returns:
            連続している場合True
        """
        delta = current_date - last_date
        return delta.days == 1

    def __str__(self) -> str:
        """文字列表現

        Returns:
            ヒーローの情報
        """
        return (
            f"⚔️ {self.name} | "
            f"Lv.{self.level} | "
            f"{self.total_experience}XP | "
            f"🔥{self.current_streak}days"
        )
