"""JSON永続化リポジトリ

データをJSONファイルに保存する実装です。
"""

import json
from pathlib import Path
from datetime import datetime, date
from uuid import UUID
from typing import Any

from ...domain.entities.quest import Quest, QuestCategory, QuestStatus, DifficultyLevel
from ...domain.entities.hero import Hero
from ...domain.entities.badge import Badge
from ...domain.repositories.quest_repository import QuestRepository
from ...domain.repositories.hero_repository import HeroRepository
from ...domain.repositories.badge_repository import BadgeRepository


class JSONEncoder(json.JSONEncoder):
    """カスタムJSONエンコーダー"""

    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, (QuestCategory, QuestStatus, DifficultyLevel)):
            return obj.value if hasattr(obj, 'value') else obj.name
        return super().default(obj)


def decode_quest(data: dict) -> Quest:
    """辞書からQuestオブジェクトを復元"""
    return Quest(
        id=UUID(data['id']),
        title=data['title'],
        description=data['description'],
        category=QuestCategory(data['category']),
        difficulty=DifficultyLevel[data['difficulty']],
        hero_id=UUID(data['hero_id']),
        status=QuestStatus(data['status']),
        experience_points=data['experience_points'],
        due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None,
        completed_at=datetime.fromisoformat(data['completed_at']) if data.get('completed_at') else None,
        created_at=datetime.fromisoformat(data['created_at']),
    )


def decode_hero(data: dict) -> Hero:
    """辞書からHeroオブジェクトを復元"""
    hero = Hero(
        id=UUID(data['id']),
        name=data['name'],
        email=data['email'],
        level=data['level'],
        total_experience=data['total_experience'],
        current_streak=data['current_streak'],
        best_streak=data['best_streak'],
        created_at=datetime.fromisoformat(data['created_at']),
        last_quest_date=date.fromisoformat(data['last_quest_date']) if data.get('last_quest_date') else None,
    )
    return hero


def decode_badge(data: dict) -> Badge:
    """辞書からBadgeオブジェクトを復元"""
    return Badge(
        id=UUID(data['id']),
        name=data['name'],
        description=data['description'],
        icon=data.get('icon', '🏆'),
        rarity=data.get('rarity', 'common'),
    )


class JSONQuestRepository(QuestRepository):
    """JSON永続化クエストリポジトリ"""

    def __init__(self, file_path: str = "data/quests.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self._quests: dict[UUID, Quest] = {}
        self._load()

    def _load(self):
        """JSONファイルから読み込み"""
        if self.file_path.exists():
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._quests = {UUID(k): decode_quest(v) for k, v in data.items()}
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Warning: Failed to load quests: {e}")
                self._quests = {}

    def _save(self):
        """JSONファイルに保存"""
        data = {str(k): v.__dict__ for k, v in self._quests.items()}
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, cls=JSONEncoder, ensure_ascii=False, indent=2)

    def save(self, quest: Quest) -> None:
        self._quests[quest.id] = quest
        self._save()

    def find_by_id(self, quest_id: UUID) -> Quest | None:
        return self._quests.get(quest_id)

    def find_by_hero_id(self, hero_id: UUID) -> list[Quest]:
        return [q for q in self._quests.values() if q.hero_id == hero_id]

    def find_by_status(self, hero_id: UUID, status: QuestStatus) -> list[Quest]:
        return [q for q in self._quests.values() if q.hero_id == hero_id and q.status == status]

    def delete(self, quest_id: UUID) -> None:
        if quest_id in self._quests:
            del self._quests[quest_id]
            self._save()

    def list_all(self) -> list[Quest]:
        return list(self._quests.values())


class JSONHeroRepository(HeroRepository):
    """JSON永続化ヒーローリポジトリ"""

    def __init__(self, file_path: str = "data/heroes.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self._heroes: dict[UUID, Hero] = {}
        self._load()

    def _load(self):
        """JSONファイルから読み込み"""
        if self.file_path.exists():
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._heroes = {UUID(k): decode_hero(v) for k, v in data.items()}
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Warning: Failed to load heroes: {e}")
                self._heroes = {}

    def _save(self):
        """JSONファイルに保存"""
        data = {str(k): v.__dict__ for k, v in self._heroes.items()}
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, cls=JSONEncoder, ensure_ascii=False, indent=2)

    def save(self, hero: Hero) -> None:
        self._heroes[hero.id] = hero
        self._save()

    def find_by_id(self, hero_id: UUID) -> Hero | None:
        return self._heroes.get(hero_id)

    def find_by_email(self, email: str) -> Hero | None:
        for hero in self._heroes.values():
            if hero.email == email:
                return hero
        return None

    def delete(self, hero_id: UUID) -> None:
        if hero_id in self._heroes:
            del self._heroes[hero_id]
            self._save()

    def list_all(self) -> list[Hero]:
        return list(self._heroes.values())


class JSONBadgeRepository(BadgeRepository):
    """JSON永続化バッジリポジトリ"""

    def __init__(self, file_path: str = "data/badges.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self._badges: dict[UUID, Badge] = {}
        self._load()

    def _load(self):
        """JSONファイルから読み込み"""
        if self.file_path.exists():
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._badges = {UUID(k): decode_badge(v) for k, v in data.items()}
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Warning: Failed to load badges: {e}")
                self._badges = {}

    def _save(self):
        """JSONファイルに保存"""
        data = {str(k): v.__dict__ for k, v in self._badges.items()}
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, cls=JSONEncoder, ensure_ascii=False, indent=2)

    def save(self, badge: Badge) -> None:
        self._badges[badge.id] = badge
        self._save()

    def find_by_id(self, badge_id: UUID) -> Badge | None:
        return self._badges.get(badge_id)

    def find_by_name(self, name: str) -> Badge | None:
        for badge in self._badges.values():
            if badge.name == name:
                return badge
        return None

    def list_all(self) -> list[Badge]:
        return list(self._badges.values())
