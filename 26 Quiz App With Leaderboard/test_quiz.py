import unittest
import os
import json
from quiz_manager import calculate_score
from storage import load_users, load_quizzes

class TestQuizApp(unittest.TestCase):
    
    def test_calculate_score_easy(self):
        # Easy: base points = 10
        # Time <= 5s: 2.0x bonus -> 20 pts
        pts, bonus, mult = calculate_score("Easy", 4.5)
        self.assertEqual(pts, 20)
        self.assertEqual(bonus, 1)
        self.assertEqual(mult, 2.0)

        # Time <= 10s: 1.5x bonus -> 15 pts
        pts, bonus, mult = calculate_score("Easy", 7.2)
        self.assertEqual(pts, 15)
        self.assertEqual(bonus, 1)
        self.assertEqual(mult, 1.5)

        # Time > 10s: 1.0x -> 10 pts
        pts, bonus, mult = calculate_score("Easy", 12.0)
        self.assertEqual(pts, 10)
        self.assertEqual(bonus, 0)
        self.assertEqual(mult, 1.0)

    def test_calculate_score_medium(self):
        # Medium: base points = 20
        # Time <= 5s: 2.0x bonus -> 40 pts
        pts, bonus, mult = calculate_score("Medium", 3.0)
        self.assertEqual(pts, 40)
        self.assertEqual(bonus, 1)
        self.assertEqual(mult, 2.0)

        # Time > 10s: 1.0x -> 20 pts
        pts, bonus, mult = calculate_score("Medium", 15.0)
        self.assertEqual(pts, 20)
        self.assertEqual(bonus, 0)
        self.assertEqual(mult, 1.0)

    def test_calculate_score_hard(self):
        # Hard: base points = 30
        # Time <= 5s: 2.0x bonus -> 60 pts
        pts, bonus, mult = calculate_score("Hard", 1.0)
        self.assertEqual(pts, 60)
        self.assertEqual(bonus, 1)
        self.assertEqual(mult, 2.0)

        # Time <= 10s: 1.5x bonus -> 45 pts
        pts, bonus, mult = calculate_score("Hard", 8.0)
        self.assertEqual(pts, 45)
        self.assertEqual(bonus, 1)
        self.assertEqual(mult, 1.5)

    def test_leaderboard_sorting(self):
        # Mock users list
        users = [
            {"username": "userA", "high_score": 100, "total_score": 200, "quizzes_played": 5, "is_admin": False},
            {"username": "userB", "high_score": 120, "total_score": 150, "quizzes_played": 2, "is_admin": False},
            {"username": "userC", "high_score": 100, "total_score": 250, "quizzes_played": 6, "is_admin": False},
            {"username": "userD", "high_score": 100, "total_score": 250, "quizzes_played": 4, "is_admin": False},
            {"username": "admin", "high_score": 300, "total_score": 600, "quizzes_played": 10, "is_admin": True}
        ]

        # Filter out admins and users with 0 quizzes (all our mock users have > 0 except we check filters)
        players = [u for u in users if not u.get("is_admin", False) and u.get("quizzes_played", 0) > 0]
        
        # Sort using the leaderboard logic
        players.sort(key=lambda u: (-u.get("high_score", 0), -u.get("total_score", 0), u.get("quizzes_played", 0)))

        # Expected order: userB (120), userD (100, 250, 4), userC (100, 250, 6), userA (100, 200, 5)
        self.assertEqual(players[0]["username"], "userB")
        self.assertEqual(players[1]["username"], "userD")
        self.assertEqual(players[2]["username"], "userC")
        self.assertEqual(players[3]["username"], "userA")

    def test_storage_seeding(self):
        # Temporarily rename current json files if they exist to test clean seeding
        user_backup = "users.json.bak"
        quiz_backup = "quizzes.json.bak"
        
        if os.path.exists("users.json"):
            os.rename("users.json", user_backup)
        if os.path.exists("quizzes.json"):
            os.rename("quizzes.json", quiz_backup)

        try:
            # Load quizzes which should create a new seeded quizzes.json file
            seeded_quizzes = load_quizzes()
            self.assertTrue(len(seeded_quizzes) >= 20)
            self.assertTrue(os.path.exists("quizzes.json"))

            # Load users which should create a new seeded users.json file with admin
            seeded_users = load_users()
            self.assertEqual(len(seeded_users), 1)
            self.assertEqual(seeded_users[0]["username"], "admin")
            self.assertTrue(seeded_users[0]["is_admin"])
            self.assertTrue(os.path.exists("users.json"))
        finally:
            # Cleanup test files
            if os.path.exists("users.json"):
                os.remove("users.json")
            if os.path.exists("quizzes.json"):
                os.remove("quizzes.json")

            # Restore original backups if they existed
            if os.path.exists(user_backup):
                os.rename(user_backup, "users.json")
            if os.path.exists(quiz_backup):
                os.rename(quiz_backup, "quizzes.json")

if __name__ == "__main__":
    unittest.main()
