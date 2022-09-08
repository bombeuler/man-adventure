import os

# 游戏全局配置
SCALE_RATE = 3
TILESIZE = 16 * SCALE_RATE

SCREEN_SIZE = (1200, 800)  # 25,25
GAME_TITLE = "荒漠求生"
FPS = 60
TOTAL_TIME = 60000
ITEM_PROBABLY = 0.3

# 精灵顺序
spriteOrder = {
    "bullet": 3,
    "enemy": 2,
    "staticbody": 2,
    "player": 2,
    "item": 1,
}

# 项目路径设置
ASSETS_PATH = os.path.abspath("./assets")

# f'{ASSETS_PATH}/'
# 玩家设置

PLAYER_MINSPEED = 5
MAX_HEALTH = 5
MAX_COLDDOWN = 400
BULLET_MINSPEED = 4
BULLET_MAXDISTANCE = SCALE_RATE * 200

# 怪物设置

monosterData = {
    "creeper": {
        "health": 3,
        "speed": 4.8,
        "damage": 1,
        "fly": False,
        "color": "green",
        "score": 1,
    },
    "turtle": {
        "health": 5,
        "speed": 4.2,
        "damage": 1,
        "fly": False,
        "color": "green",
        "score": 3,
    },
    "bat": {
        "health": 1,
        "speed": 7.2,
        "damage": 1,
        "fly": True,
        "color": "red",
        "score": 2,
    },
    "dragon": {
        "health": 8,
        "speed": 4,
        "damage": 2,
        "fly": True,
        "color": "red",
        "score": 4,
    },
}

# monosterData = {
#     "creeper": {
#         "health": 3,
#         "speed": 2,
#         "damage": 1,
#         "fly": False,
#         "color": "green",
#         "score": 1,
#     },
#     "turtle": {
#         "health": 5,
#         "speed": 2,
#         "damage": 1,
#         "fly": False,
#         "color": "green",
#         "score": 3,
#     },
#     "bat": {
#         "health": 1.2,
#         "speed": 2,
#         "damage": 1,
#         "fly": True,
#         "color": "red",
#         "score": 2,
#     },
#     "dragon": {
#         "health": 8,
#         "speed": 2,
#         "damage": 2,
#         "fly": True,
#         "color": "red",
#         "score": 4,
#     },
# }

# 游戏道具效果

effectData = {
    "speedup": {
        "influence": ("speed", 0.3, PLAYER_MINSPEED, 7.1),
        "imageIndex": 4,
        "weight": 5,
        "type": "simple",
    },
    "shootspeedup": {
        "influence": ("shootingCooldown", -40, 160, MAX_COLDDOWN),
        "imageIndex": 1,
        "weight": 5,
        "type": "simple",
    },
    "healthrecover": {
        "influence": ("health", 1, 0, MAX_HEALTH),
        "imageIndex": 7,
        "weight": 5,
        "type": "simple",
    },
    "fiveBullets": {
        "infuence": "bulletNumber",
        "imageIndex": 5,
        "weight": 3,
        "type": "complex",
        "lastTime": 30,
    },
    "bigBullets": {
        "infuence": "bulletSize",
        "imageIndex": 2,
        "weight": 2,
        "type": "complex",
        "lastTime": 5,
    }
}


WEIGHT_ALL = 0

for k, item in effectData.items():
    WEIGHT_ALL += item["weight"]



# 用户界面设置
BAR_HEIGHT = 16
TIME_BAR_WIDTH = SCREEN_SIZE[0] // 3
ITEM_BOX_SIZE = 80
UI_FONT = f"{ASSETS_PATH}/minecraftAE.ttf"
UI_FONT_SIZE = 22

# 颜色设置
UI_BG_COLOR = "red"
TEXT_COLOR = "#EEEEEE"
UI_BORDER_COLOR = "#111111"
TIME_COLOR = "yellow"
UI_BORDER_COLOR_ACTIVE = "gold"
