import unittest
from uuid import uuid4
from datetime import datetime, timedelta
from questforge.domain.entities.quest import Quest, QuestCategory, DifficultyLevel, QuestStatus
from questforge.domain.exceptions import InvalidQuestStateError

class TestQuest(unittest.TestCase):
    def setUp(self):
        self.hero_id = uuid4()
        self.quest = Quest(
            title="テストクエスト",
            description="テスト用の説明",
            category=QuestCategory.DAILY,
            difficulty=DifficultyLevel.NORMAL,
            hero_id=self.hero_id
        )

    def test_initial_status_is_available(self):
        """作成直後のステータスは AVAILABLE であること"""
        self.assertEqual(self.quest.status, QuestStatus.AVAILABLE)
        # 文字列としての比較も通ることを確認（StrEnumの効果）
        self.assertEqual(self.quest.status, "AVAILABLE")
        self.assertEqual(self.quest.experience_points, 50)

    def test_start_changes_status_to_in_progress(self):
        """start()を呼ぶとステータスが IN_PROGRESS に変わること"""
        self.quest.start()
        self.assertEqual(self.quest.status, QuestStatus.IN_PROGRESS)
        self.assertEqual(self.quest.status, "IN_PROGRESS")

    def test_cannot_start_already_started_quest(self):
        """進行中のクエストを再度開始しようとすると例外が発生すること"""
        self.quest.start()
        with self.assertRaises(InvalidQuestStateError):
            self.quest.start()

    def test_complete_changes_status_to_completed(self):
        """サイクル1相当: complete()を呼ぶとステータスが COMPLETED に変わること"""
        self.quest.start()
        xp = self.quest.complete()
        
        self.assertEqual(self.quest.status, QuestStatus.COMPLETED)
        self.assertEqual(self.quest.status, "COMPLETED")
        self.assertEqual(xp, 50)

    def test_cannot_complete_without_starting(self):
        """サイクル2相当: 開始していないクエストを完了しようとすると例外が発生すること"""
        with self.assertRaises(InvalidQuestStateError):
            self.quest.complete()

    def test_cannot_complete_already_completed_quest(self):
        """サイクル2相当: 完了済みのクエストを再度完了しようとすると例外が発生すること"""
        self.quest.start()
        self.quest.complete()
        with self.assertRaises(InvalidQuestStateError):
            self.quest.complete()

if __name__ == '__main__':
    unittest.main()
