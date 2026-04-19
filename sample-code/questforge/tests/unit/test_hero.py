import unittest
from datetime import date, timedelta
from questforge.domain.entities.hero import Hero
from questforge.domain.exceptions import DomainError

class TestHero(unittest.TestCase):
    def setUp(self):
        self.hero = Hero(name="Alice", email="alice@example.com")

    def test_initial_hero_stats(self):
        self.assertEqual(self.hero.level, 1)
        self.assertEqual(self.hero.total_experience, 0)

    def test_gain_experience_and_level_up(self):
        # 100 * (2^1.5) = 282.8...
        result = self.hero.gain_experience(300)
        self.assertTrue(result.leveled_up)
        self.assertEqual(self.hero.level, 2)

    def test_gain_negative_experience_raises_error(self):
        """負の経験値を獲得しようとするとDomainErrorが発生すること"""
        with self.assertRaises(DomainError):
            self.hero.gain_experience(-10)

    def test_streak_updates(self):
        self.hero.complete_quest_today()
        self.assertEqual(self.hero.current_streak, 1)
        
        yesterday = date.today() - timedelta(days=1)
        self.hero.last_quest_date = yesterday
        self.hero.complete_quest_today()
        self.assertEqual(self.hero.current_streak, 2)

if __name__ == '__main__':
    unittest.main()
