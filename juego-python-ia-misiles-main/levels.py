import os
import json

LEVELS = [
    {"level": 1, "missile_speed": 5, "enemy_count": 3, "points_to_win": 150},
    {"level": 2, "missile_speed": 7, "enemy_count": 5, "points_to_win": 300},
    {"level": 3, "missile_speed": 9, "enemy_count": 7, "points_to_win": 450},
    {"level": 4, "missile_speed": 11, "enemy_count": 9, "points_to_win": 600},
    {"level": 5, "missile_speed": 13, "enemy_count": 12, "points_to_win": 750},
]

PROGRESS_FILE = "progress.json"

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f).get("unlocked_level", 1)
    return 1

def save_progress(unlocked_level):
    with open(PROGRESS_FILE, "w") as f:
        json.dump({"unlocked_level": unlocked_level}, f)

def get_level_config(level):
    if 1 <= level <= 5:
        return LEVELS[level - 1]
    return LEVELS[-1]