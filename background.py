import pygame
import random
from GameState import *

#정의
game_state = GameState()

# 화면 크기 설정
SCREEN_WIDTH = 375
SCREEN_HEIGHT = 812
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 바닥 설정
GROUND_Y = 350  # 캐릭터 위치에 맞춘 바닥 y 좌표
GROUND_HEIGHT = 20  # 바닥 높이

# 배경 설정
clouds = [{"x": 100, "y": 50, "speed": 0.2}, {"x": 250, "y": 100, "speed": 0.3}]
mountains = [{"x": 0, "y": GROUND_Y - 100, "speed": 0.5}, {"x": 200, "y": GROUND_Y - 100, "speed": 0.5}]

# 색상 정의
SKY_BLUE = (135, 206, 235)
CLOUD_WHITE = (255, 255, 255)
GROUND_GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
SUNSET_ORANGE = (255, 140, 0)
DARK_PURPLE = (75, 0, 130)
MOON_YELLOW = (240, 230, 140)
SNOW_WHITE = (240, 248, 255)
ICY_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)
LIGHT_BLUE = (173, 216, 230)

# 화면 분할 높이
SCREEN_SPLIT = GROUND_Y 

# 레벨별 배경
def level_0():
    draw_split_background(SKY_BLUE, SKY_BLUE)
    draw_clouds_and_mountains(CLOUD_WHITE, GROUND_GREEN, 0.2, 0.5)
    draw_ground(BROWN)

def level_1():
    draw_split_background(SUNSET_ORANGE, SKY_BLUE)
    draw_clouds_and_mountains(CLOUD_WHITE, GROUND_GREEN, 0.3, 0.6)
    draw_ground(BROWN)

def level_2():
    draw_split_background(DARK_PURPLE, SKY_BLUE)
    draw_clouds_and_mountains(MOON_YELLOW, GROUND_GREEN, 0.1, 0.4)
    draw_stars()
    draw_ground(BROWN)

def level_3():
    draw_split_background(DARK_BLUE, LIGHT_BLUE)  # 위쪽: 어두운 하늘, 아래쪽: 밝은 물
    draw_clouds_and_mountains(MOON_YELLOW, (70, 130, 180), 0.2, 0.5)  # 구름과 산
    draw_ground((211, 211, 211))  # 바닥을 어두운 색으로 설정하여 강한 대비

def level_4():
    draw_split_background(DARK_PURPLE, SKY_BLUE)
    draw_clouds_and_mountains((255, 105, 180), (72, 61, 139), 0.4, 0.6)
    draw_ground((147, 112, 219))

# 화면 분할 배경 그리기
def draw_split_background(top_color, bottom_color):
    pygame.draw.rect(screen, top_color, (0, 0, SCREEN_WIDTH, SCREEN_SPLIT))  # 위쪽
    pygame.draw.rect(screen, bottom_color, (0, SCREEN_SPLIT, SCREEN_WIDTH, SCREEN_HEIGHT - SCREEN_SPLIT))  # 아래쪽

# 공통 함수: 구름, 산, 별, 바닥 그리기
def draw_clouds_and_mountains(cloud_color, mountain_color, cloud_speed, mountain_speed):
    for cloud in clouds:
        pygame.draw.ellipse(screen, cloud_color, (cloud["x"], cloud["y"], 100, 50))
        cloud["x"] -= cloud["speed"] * game_state.character_speed
        if cloud["x"] < -100:
            cloud["x"] = SCREEN_WIDTH
    for mountain in mountains:
        # 산이 바닥과 자연스럽게 연결되도록 위치 수정
        pygame.draw.polygon(
            screen,
            mountain_color,
            [(mountain["x"], GROUND_Y), (mountain["x"] + 100, GROUND_Y - 100), (mountain["x"] + 200, GROUND_Y)],
        )
        mountain["x"] -= mountain["speed"] * game_state.character_speed
        if mountain["x"] < -200:
            mountain["x"] = SCREEN_WIDTH

def draw_stars():
    for i in range(50):  # 별 추가
        x, y = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_SPLIT)
        pygame.draw.circle(screen, MOON_YELLOW, (x, y), 2)

def draw_ground(ground_color):
    pygame.draw.rect(screen, ground_color, (0, GROUND_Y, SCREEN_WIDTH, GROUND_HEIGHT))



def background(game_state):
    # 돈 증가가 아직 적용되지 않았다면
    if game_state.money_increased:
        if game_state.map_level_factor == 1:
            level_1()
            game_state.money_increased = False
            game_state.bg_increase_money(6)  # 레벨 1에서만 돈 증가
        elif game_state.map_level_factor == 2:
            level_2()
            game_state.money_increased = False
            game_state.bg_increase_money(12)  # 레벨 2에서만 돈 증가
        elif game_state.map_level_factor == 3:
            level_3()
            game_state.money_increased = False
            game_state.bg_increase_money(18)  # 레벨 3에서만 돈 증가
        elif game_state.map_level_factor == 4:
            level_4()
            game_state.money_increased = False
            game_state.bg_increase_money(24)  # 레벨 4에서만 돈 증가
        else:
            level_0()
            game_state.money_per_run = game_state.money_per_runf
        
    else:
        # 돈 증가가 이미 적용되었으면 단순히 레벨을 그리기만 함
        if game_state.map_level_factor == 0:
            level_0()
            game_state.money_per_run = game_state.money_per_runf
        elif game_state.map_level_factor == 1:
            level_1()
        elif game_state.map_level_factor == 2:
            level_2()
        elif game_state.map_level_factor == 3:
            level_3()
        elif game_state.map_level_factor == 4:
            level_4()
