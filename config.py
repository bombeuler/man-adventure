import os

# 游戏全局配置
SCALE_RATE = 3
TILESIZE = 16 * SCALE_RATE

SCREEN_SIZE = (1200, 800)  # 25,25
GAME_TITLE = "男人的冒险"
FPS = 60
TOTAL_TIME = 60000

# 项目路径设置
ASSETS_PATH = os.path.abspath("./assets")

# 玩家设置

PLAYER_MAXSPEED = 5
BULLET_MINSPEED = 2
BULLET_MAXDISTANCE = SCALE_RATE * 400

# 怪物设置

monosterData = {
    "creeper": {"health": 2, "speed": 5, "damage": 1, "fly": False, "color": "green"},
    "turtle": {"health": 4, "speed": 4, "damage": 1, "fly": False, "color": "green"},
    "bat": {"health": 1, "speed": 7, "damage": 1, "fly": True, "color": "red"},
    "dragon": {"health": 8, "speed": 4, "damage": 2, "fly": True, "color": "red"},
}
