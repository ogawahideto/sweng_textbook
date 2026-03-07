import unittest
from uuid import uuid4
from questforge.domain.entities.quest import Quest, QuestCategory, DifficultyLevel, QuestStatus
from questforge.domain.entities.hero import Hero
from questforge.application.use_cases.complete_quest import CompleteQuestUseCase, CompleteQuestInput
from questforge.infrastructure.persistence.in_memory_quest_repository import InMemoryQuestRepository
from questforge.infrastructure.persistence.in_memory_hero_repository import InMemoryHeroRepository
from questforge.domain.exceptions import InvalidQuestStateError

class TestCompleteQuestUseCase(unittest.TestCase):
    def setUp(self):
        self.quest_repo = InMemoryQuestRepository()
        self.hero_repo = InMemoryHeroRepository()
        
        self.hero = Hero(name="Test Hero", email="test@example.com")
        self.hero_repo.save(self.hero)
        
        self.quest = Quest(
            title="完了テストクエスト",
            description="ユースケーステスト用",
            category=QuestCategory.DAILY,
            difficulty=DifficultyLevel.NORMAL,
            hero_id=self.hero.id
        )
        self.quest.start()
        self.quest_repo.save(self.quest)
        
        self.use_case = CompleteQuestUseCase(self.quest_repo, self.hero_repo)

    def test_execute_completes_quest_and_rewards_hero(self):
        input_data = CompleteQuestInput(quest_id=self.quest.id)
        output = self.use_case.execute(input_data)
        
        self.assertEqual(output.reward.experience_points, 50)
        
        saved_quest = self.quest_repo.find_by_id(self.quest.id)
        self.assertEqual(saved_quest.status, "COMPLETED")

    def test_execute_fails_for_invalid_state(self):
        """完了済みのクエストを再度完了しようとすると例外が発生すること"""
        input_data = CompleteQuestInput(quest_id=self.quest.id)
        self.use_case.execute(input_data)  # 1回目
        
        with self.assertRaises(InvalidQuestStateError):
            self.use_case.execute(input_data)  # 2回目

if __name__ == '__main__':
    unittest.main()
