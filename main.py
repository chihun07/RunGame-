import pygame
import sys
from GameState import *
from background import *


# 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 375
SCREEN_HEIGHT = 812
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("캐릭터 달리기 & 메뉴창")

# 프레임 설정
clock = pygame.time.Clock()
FPS = 60


# 색상
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
BROWN = (139, 69, 19)
SKY_BLUE = (135, 206, 250)
CLOUD_WHITE = (245, 245, 245)
GROUND_GREEN = (34, 139, 34)
LOCK_BROWN = (143, 120, 75)

# 바닥 설정
ground_y = 350
ground_height = 20

# GameState를 import해서 사용
game_state = GameState()

# 메뉴 버튼 설정
buttons = [
    {"rect": pygame.Rect(20, 380, 80, 60), "color": GRAY, "text": "업그레이드", "pressed": False},
    {"rect": pygame.Rect(110, 380, 80, 60), "color": GRAY, "text": "장착", "pressed": False},
    {"rect": pygame.Rect(200, 380, 80, 60), "color": GRAY, "text": "도움말", "pressed": False},
    {"rect": pygame.Rect(290, 380, 80, 60), "color": GRAY, "text": "종료", "pressed": False},
]

# 업그레이드 버튼 설정
upgrade_buttons = [
    {"rect": pygame.Rect(25, 500, 150, 50), "color": GRAY, "text": "속도 업그레이드", "pressed": False},
    {"rect": pygame.Rect(25, 625, 150, 50), "color": GRAY, "text": "팻 구매", "pressed": False},
    {"rect": pygame.Rect(200, 500, 150, 50), "color": GRAY, "text": "크기 업그레이드", "pressed": False},
    {"rect": pygame.Rect(200, 625, 150, 50), "color": GRAY, "text": "맵 구매", "pressed": False},
]

# 장착 버튼 설정
equip_buttons = [
    #팻
    {"rect": pygame.Rect(25, 500, 150, 50), "color": LOCK_BROWN, "text": "팻 1", "pressed": False},
    {"rect": pygame.Rect(25, 570, 150, 50), "color": LOCK_BROWN, "text": "팻 2", "pressed": False},
    {"rect": pygame.Rect(25, 640, 150, 50), "color": LOCK_BROWN, "text": "팻 3", "pressed": False},
    {"rect": pygame.Rect(25, 710, 150, 50), "color": LOCK_BROWN, "text": "팻 4", "pressed": False},
    #맵
    {"rect": pygame.Rect(200, 500, 150, 50), "color": LOCK_BROWN, "text": "맵 1", "pressed": False},
    {"rect": pygame.Rect(200, 570, 150, 50), "color": LOCK_BROWN, "text": "맵 2", "pressed": False},
    {"rect": pygame.Rect(200, 640, 150, 50), "color": LOCK_BROWN, "text": "맵 3", "pressed": False},
    {"rect": pygame.Rect(200, 710, 150, 50), "color": LOCK_BROWN, "text": "맵 4", "pressed": False},
]

# 폰트 설정
font = pygame.font.SysFont("malgungothic", 20)

# 화면 상태 플래그
show_upgrades = False
show_help = False
show_equip = False

# 도움말 텍스트
help_text = """이 게임은 캐릭터가 바닥 위를 달리는
간단한 게임입니다. 업그레이드를 통해
속도와 크기를 개선할 수 있습니다."""


# 게임 루프
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button["rect"].collidepoint(event.pos):
                    button["pressed"] = True
                    if button["text"] == "업그레이드":
                        show_upgrades = True
                        show_help = False
                        show_equip = False
                    elif button["text"] == "장착":
                        show_equip = True
                        show_help = False
                        show_upgrades = False
                    elif button["text"] == "도움말":
                        show_help = True
                        show_upgrades = False
                        show_equip = False
                    elif button["text"] == "종료":
                        running = False
            #업그레이드
            if show_upgrades:
                for upgrade in upgrade_buttons:
                    if upgrade["rect"].collidepoint(event.pos):
                        upgrade["pressed"] = True 
                        handle_upgrade(upgrade["text"], game_state)
            #장착
            if show_equip:
                for equip in equip_buttons:
                    if equip["rect"].collidepoint(event.pos):
                        equip["pressed"] = True  
                        equip_upgrade(equip["text"], game_state)

        elif event.type == pygame.MOUSEBUTTONUP:
            # 마우스 버튼을 떼면 눌림 효과를 제거
            for button in buttons:
                button["pressed"] = False
            if show_upgrades:
                for upgrade in upgrade_buttons:
                    upgrade["pressed"] = False
            if show_equip:
                for equip in equip_buttons:
                    equip["pressed"] = False

    # 캐릭터 위치 업데이트
    game_state.update_character_position()  # 캐릭터 위치 업데이트
    game_state.update_pet_size()  # 팻 크기 업데이트
    game_state.increase_money_from_pets()  # 팻들로 인한 돈 증가

    #배경화면
    background(game_state)

    # 캐릭터 그리기
    screen.blit(game_state.character_image, (game_state.character_x, game_state.character_y))

    # 팻 그리기
    draw_pets(game_state, screen)

    # 기본 버튼 그리기
    for button in buttons:
        draw_button(button, screen, font)

    # 업그레이드 버튼 그리기
    if show_upgrades:
        for upgrade_button in upgrade_buttons:
            draw_button(upgrade_button, screen, font)

        # 업그레이드 가격과 현재 속도/크기 표시
        # 속도 업그레이드
        speed_text_line1 = font.render("속도 업그레이드:", True, BLACK)
        speed_text_line2 = font.render(f"{game_state.speed_upgrade_price}원", True, BLACK)
        speed_text_line3 = font.render(f"현재 속도: {game_state.character_speed}", True, BLACK)
        screen.blit(speed_text_line1, (25, 560))  # 첫 번째 줄
        screen.blit(speed_text_line2, (25, 590))  # 두 번째 줄
        screen.blit(speed_text_line3, (25, 460))  # 세 번째 줄

        # 크기 업그레이드
        size_text_line1 = font.render("크기 업그레이드:", True, BLACK)
        size_text_line2 = font.render(f"{game_state.size_upgrade_price}원", True, BLACK)
        size_text_line3 = font.render(f"현재 크기: {game_state.character_size}", True, BLACK)
        screen.blit(size_text_line1, (200, 560))  # 첫 번째 줄
        screen.blit(size_text_line2, (200, 590))  # 두 번째 줄
        screen.blit(size_text_line3, (200, 460))  # 세 번째 줄

        # 팻 구매
        pat_text_line1 = font.render("팻 구매: ", True, BLACK)
        pat_text_line2 = font.render(f"{game_state.pat_price}원", True, BLACK)
        screen.blit(pat_text_line1, (25, 680))  # 첫 번째 줄
        screen.blit(pat_text_line2, (25, 710))  # 두 번째 줄

        # 맵 구매
        map_text_line1 = font.render("맵 구매: ", True, BLACK)
        map_text_line2 = font.render(f"{game_state.map_price}원", True, BLACK)
        screen.blit(map_text_line1, (200, 680))  # 첫 번째 줄
        screen.blit(map_text_line2, (200, 710))  # 두 번째 줄
        
    # 장착 버튼 그리기
    if show_equip:
        for equip_button in equip_buttons:
            draw_button(equip_button, screen, font)

    # 도움말 표시
    if show_help:
        help_lines = help_text.split("\n")
        for i, line in enumerate(help_lines):
            help_surface = font.render(line, True, BLACK)
            screen.blit(help_surface, (20, 500 + i * 30))

    # 돈 표시
    money_text = font.render(f"돈: {game_state.money}원", True, BLACK)
    screen.blit(money_text, (20, 10))
    # 버는 돈 표시
    money_text = font.render(f"돈: {game_state.money_per_run}원", True, BLACK)
    screen.blit(money_text, (200, 10))
    # 팻이 버는 돈 표시
    pet_money_text = font.render(f"팻 초당 돈: {game_state.pet_money}원", True, BLACK)
    screen.blit(pet_money_text, (20, 40))

    # 메시지 그리기
    game_state.draw_messages(screen, font)
    # 메시지 관리: 오래된 메시지 제거
    game_state.remove_expired_messages()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
