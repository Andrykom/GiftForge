import secrets
from typing import Dict

RARITY_CONFIG = {
    "common": {"chance": 0.85, "stars": 10, "name": "☕ Классика", "emoji": "☕"},
    "rare": {"chance": 0.10, "stars": 25, "name": "🌟 Редкость", "emoji": "🌟"},
    "epic": {"chance": 0.04, "stars": 50, "name": "🔥 Эпик", "emoji": "🔥"},
    "mythic": {"chance": 0.01, "stars": 100, "name": "💎 Мифик", "emoji": "💎"}
}

class GiftEngine:
    @staticmethod
    def calculate_drop() -> Dict:
        roll = secrets.randbelow(10000) / 10000.0

        cumulative = 0.0
        for rarity, config in RARITY_CONFIG.items():
            cumulative += config["chance"]
            if roll <= cumulative:
                return {
                    "rarity": rarity,
                    "stars": config["stars"],
                    "name": config["name"],
                    "emoji": config["emoji"]
                }

        return {
            "rarity": "common",
            "stars": 10,
            "name": "☕ Классика",
            "emoji": "☕"
        }

gift_engine = GiftEngine()
