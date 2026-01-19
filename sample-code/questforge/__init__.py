"""QuestForge - タスク管理をRPG風に楽しむアプリケーション

このパッケージは、クリーンアーキテクチャとドメイン駆動設計の
実践例として設計されています。

使い方:
    >>> from infrastructure.persistence import InMemoryQuestRepository, InMemoryHeroRepository
    >>> from cli import QuestForgeCLI
    >>>
    >>> quest_repo = InMemoryQuestRepository()
    >>> hero_repo = InMemoryHeroRepository()
    >>> cli = QuestForgeCLI(quest_repo, hero_repo)
    >>>
    >>> cli.create_hero("Alice", "alice@example.com")
"""

__version__ = "0.1.0"
