import os

# 游戏全局配置
SCALE_RATE = 3
TILESIZE = 16 * SCALE_RATE

SCREEN_SIZE = (1200, 800)  # 25,25
GAME_TITLE = "荒漠求生"
FPS = 60
TOTAL_TIME = 60000

# 项目路径设置
ASSETS_PATH = os.path.abspath("./assets")

#f'{ASSETS_PATH}/'
# 玩家设置

PLAYER_MAXSPEED = 5
MAX_HEALTH = 4
BULLET_MINSPEED = 4
BULLET_MAXDISTANCE = SCALE_RATE * 200

# 怪物设置

monosterData = {
    "creeper": {"health": 2, "speed": 5, "damage": 1, "fly": False, "color": "green","score":1},
    "turtle": {"health": 4, "speed": 4.2, "damage": 1, "fly": False, "color": "green","score":3},
    "bat": {"health": 1, "speed": 7, "damage": 1, "fly": True, "color": "red","score":2},
    "dragon": {"health": 8, "speed": 4.2, "damage": 2, "fly": True, "color": "red","score":4},
}

# 游戏道具效果

effectData = {
    "speedup": {"influence": ["speed"], "imageIndex": 4},
    "bulletspeedup": {"influence": ["shootingCooldown"], "imageIndex": 1},
    "healthrecover": {"influence": ["health"], "imageIndex": 7},
}
#用户界面设置
BAR_HEIGHT=16
TIME_BAR_WIDTH=SCREEN_SIZE[0]//3
ITEM_BOX_SIZE=80
UI_FONT=f'{ASSETS_PATH}/minecraftAE.ttf'
UI_FONT_SIZE=18

#颜色设置
UI_BG_COLOR='red'
TEXT_COLOR='#EEEEEE'
UI_BORDER_COLOR='#111111'
TIME_COLOR='yellow'
UI_BORDER_COLOR_ACTIVE='gold'
