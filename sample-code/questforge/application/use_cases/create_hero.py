"""ヒーロー作成ユースケース

新しいヒーローを作成する業務処理を定義します。
"""

from dataclasses import dataclass
from uuid import UUID

from ...domain.entities.hero import Hero
from ...domain.repositories.hero_repository import HeroRepository


@dataclass
class CreateHeroInput:
    """ヒーロー作成の入力データ

    Attributes:
        name: ヒーローの名前
        email: メールアドレス
    """

    name: str
    email: str


@dataclass
class CreateHeroOutput:
    """ヒーロー作成の出力データ

    Attributes:
        hero_id: 作成されたヒーローのID
        name: ヒーローの名前
    """

    hero_id: UUID
    name: str


class CreateHeroUseCase:
    """ヒーロー作成ユースケース

    新しいヒーローを作成し、データベースに保存します。

    Example:
        >>> hero_repo = InMemoryHeroRepository()
        >>> use_case = CreateHeroUseCase(hero_repo)
        >>> input_data = CreateHeroInput(
        ...     name="Alice the Alchemist",
        ...     email="alice@example.com"
        ... )
        >>> output = use_case.execute(input_data)
        >>> print(f"Hero created: {output.name}")
    """

    def __init__(self, hero_repository: HeroRepository):
        """初期化

        Args:
            hero_repository: ヒーローリポジトリ
        """
        self.hero_repository = hero_repository

    def execute(self, input_data: CreateHeroInput) -> CreateHeroOutput:
        """ヒーローを作成する

        Args:
            input_data: 作成するヒーローの情報

        Returns:
            作成されたヒーローの情報

        Raises:
            ValueError: 同じメールアドレスのヒーローが既に存在する場合
        """
        # メールアドレスの重複チェック
        existing_hero = self.hero_repository.find_by_email(input_data.email)
        if existing_hero is not None:
            raise ValueError(f"Hero with email {input_data.email} already exists")

        # ヒーローを作成
        hero = Hero(
            name=input_data.name,
            email=input_data.email,
        )

        # 保存
        self.hero_repository.save(hero)

        return CreateHeroOutput(
            hero_id=hero.id,
            name=hero.name,
        )
