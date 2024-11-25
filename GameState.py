import pygame
from pet import *

class GameState:
    def __init__(self):
        self.character_speed = 5
        self.character_size = 30
        self.character_x = 50
        self.character_y = 350 - 30  # ground_y = 350
        self.character_image = pygame.Surface((self.character_size, self.character_size))
        self.character_image.fill((0, 120, 255))  # BLUE
        self.money = 100000
        self.money_per_run = 100
        self.money_per_runf = self.money_per_run
        self.money_increased = True
        self.total_money_earned = 0
        self.start_time = pygame.time.get_ticks()
        self.speed_upgrade_price = 200
        self.size_upgrade_price = 300
        self.game_messages = []
        self.message_time = 0
        self.pat_level = 0
        self.pat_price = 2500
        self.pet_money = 0
        self.equipped_pat = []  # 장착된 팻
        self.map_level = 0
        self.map_price = 10000
        self.equipped_map = None  # 장착된 맵
        self.map_level_factor = 0
        self.pet_size_max = 100
        self.pet_size_min = 20
        self.last_size_change_time = pygame.time.get_ticks()
        self.size_change_interval = 1000  # 크기 변경 간격 (1초)

        # 팻 설정 (캐릭터 뒤에 따라오는 팻)
        self.pets = [
            Pet(level=1, size=20, color=(255, 0, 0), max_size=30, min_size=20, y=330, money_increase_factor=50),
            Pet(level=2, size=25, color=(0, 255, 0), max_size=40, min_size=25, y=325, money_increase_factor=100),
            Pet(level=3, size=30, color=(0, 0, 255), max_size=50, min_size=35, y=320, money_increase_factor=250),
            Pet(level=4, size=35, color=(255, 255, 0), max_size=60, min_size=45, y=315, money_increase_factor=500)
        ]
        
        self.last_money_increase_time = pygame.time.get_ticks()  # 돈 증가 마지막 시간

    def update_money(self):
        """1초마다 돈 증가"""
        money_current_time = pygame.time.get_ticks()

        if money_current_time - self.last_money_increase_time >= 1000:  # 1초마다 돈 증가
            total_money_increase = sum(pet.increase_money() for pet in self.equipped_pat)  # 장착된 팻들이 증가시키는 돈
            self.total_money_earned += total_money_increase  # 증가된 돈을 총 증가액에 더함
            self.money += total_money_increase  # 실제 게임 머니에 더함
            self.last_money_increase_time = money_current_time  # 마지막 증가 시간 갱신

    def bg_increase_money(self, multiplier):
        self.money_per_run = int(self.money_per_runf * multiplier)  # multiplier만큼 돈을 증가시킴

    def increase_money_from_pets(self):
        """장착된 팻들이 돈을 증가시킴"""
        total_money_increase = sum(pet.increase_money() for pet in self.equipped_pat)
        self.money += total_money_increase

    def update_pet_size(self):
        """장착된 팻 크기 업데이트"""
        for pet in self.equipped_pat:
            pet.update_size()

    def update_pet_money(self):
        """
        장착된 모든 팻의 increase_money 메서드를 호출하여 돈 증가
        """
        for pet in self.equipped_pat:
            pet.increase_money()  # GameState의 pet_money를 증가시킴


    def add_message(self, message):
        """게임 메시지 추가"""
        current_time = pygame.time.get_ticks()
        self.game_messages.append({"text": message, "time": current_time})

    def remove_expired_messages(self):
        """메시지 만료 제거"""
        current_time = pygame.time.get_ticks()
        self.game_messages = [
            msg for msg in self.game_messages if current_time - msg["time"] <= 1000
        ]

    def draw_messages(self, screen, font):
        """화면에 메시지 출력"""
        for i, msg in enumerate(self.game_messages):
            text_surface = font.render(msg["text"], True, (0, 0, 0))  # 검은색 텍스트
            screen.blit(text_surface, (180, 45 + i * 30))  # 메시지 위치 조정

    def update_character_position(self):
        # 장착된 맵 레벨에 따른 이동 속도 계산
        if self.equipped_map is not None:  # 맵이 장착되어 있다면
            self.map_level_factor = self.equipped_map  # 장착된 맵의 레벨
        else:
            self.map_level_factor = 0  # 기본값 (장착되지 않으면 1로 설정)

        # 캐릭터의 이동 속도 조절: 맵 레벨에 따라 이동 속도가 감소
        self.character_x += self.character_speed / (self.map_level_factor * 8 + 1)  # 맵 레벨에 따라 이동 속도 감소
        if self.character_x > 375:  # SCREEN_WIDTH
            self.character_x = -self.character_size
            self.money += self.money_per_run  # 이동할 때마다 돈 획득

            # 팻들이 돈을 증가시키는 함수 호출
            self.increase_money_from_pets()

        # 2초마다 돈 증가 처리
        self.update_money()

    # 맵 장착 또는 해제
    def equip_map(self, map_level):
        if self.equipped_map == map_level:  # 이미 장착된 맵이면 해제
            self.add_message(f"맵 장착 {map_level} 해제")
            self.equipped_map = None  # 장착 해제
        else:
            if self.equipped_map is not None:  # 다른 맵이 이미 장착되어 있으면
                self.add_message(f"맵 장착 {self.equipped_map} 해제")  # 이전 맵 해제 메시지
            self.equipped_map = map_level  # 새로운 맵을 장착
            self.add_message(f"맵 장착 {map_level}")

        # 현재 장착된 맵 출력
        self.add_message(f"현재 장착된 맵: {self.equipped_map if self.equipped_map is not None else '없음'}")

            
# 팻 그리기
def draw_pets(game_state, screen):
    for index, pet in enumerate(game_state.equipped_pat):
        pet.update_size()  # 팻 크기 업데이트 (y 좌표도 함께 갱신됨)
        pet.update_position(game_state.character_x, index)  # 장착된 순서에 맞게 팻 위치 업데이트
        screen.blit(pet.image, (pet.x, pet.y))  # 팻 그리기

# 버튼 눌림 효과 함수
def draw_button(button, screen, font):
    color = button["color"]
    if button["pressed"]:
        # 눌린 상태일 때 버튼 크기 줄이기 (살짝 눌린 느낌)
        button_rect = button["rect"].inflate(-10, -10)
    else:
        button_rect = button["rect"]
    
    pygame.draw.rect(screen, color, button_rect)
    text = font.render(button["text"], True, (0, 0, 0))  # BLACK
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

# 스텟 업그레이드
def handle_upgrade(upgrade_text, game_state):
    size_max = 100
    pat_max = 4
    map_max = 4
    if upgrade_text == "속도 업그레이드":
        if game_state.money >= game_state.speed_upgrade_price:
            game_state.money -= game_state.speed_upgrade_price
            game_state.speed_upgrade_price = int(game_state.speed_upgrade_price * 1.3)
            game_state.character_speed += 0.5
            game_state.add_message("속도 업그레이드 완료!")
            game_state.add_message(f"현재 속도: {game_state.character_speed}")
        else:
            game_state.add_message("돈이 부족합니다.")
    elif upgrade_text == "크기 업그레이드":
        if game_state.character_size >= size_max:
            game_state.add_message("최대 크기 도달.")
            return
        if game_state.money >= game_state.size_upgrade_price:
            game_state.money -= game_state.size_upgrade_price
            game_state.size_upgrade_price = int(game_state.size_upgrade_price * 1.5)
            game_state.character_size += 5
            game_state.character_y -= 5
            game_state.money_per_runf += 75
            game_state.character_image = pygame.Surface(
                (game_state.character_size, game_state.character_size)
            )
            game_state.character_image.fill((0, 120, 255))  # BLUE
            game_state.add_message(f"크기 업그레이드 완료!")
            game_state.add_message(f"현재 크기: {game_state.character_size}")
        else:
            game_state.add_message("돈이 부족합니다.")

    elif upgrade_text == "팻 구매":
        if game_state.pat_level >= pat_max:
            game_state.add_message("모든 팻 구매 완료.")
            return
        if game_state.money >= game_state.pat_price:
            game_state.money -= game_state.pat_price
            game_state.pat_price = int(game_state.pat_price * 3)
            game_state.pat_level += 1
            game_state.add_message("팻 구매 완료!")
            game_state.add_message(f"팻 구매 현황: {game_state.pat_level}/4")

    elif upgrade_text == "맵 구매":
        if game_state.map_level >= map_max:
            game_state.add_message("모든 맵 구매 완료.")
            return
        if game_state.money >= game_state.map_price:
            game_state.money -= game_state.map_price
            game_state.map_price = int(game_state.map_price * 5)
            game_state.map_level += 1
            game_state.add_message("맵 구매 완료!")
            game_state.add_message(f"맵 구매 현황: {game_state.map_level}/4")

# 장착/해제 처리 함수
def equip_upgrade(equip_text, game_state):
    try:
        # "팻 1" 같은 형식에서 숫자만 추출
        parts = equip_text.split(" ")
        level = int(parts[-1])  # 마지막 부분이 숫자

        if "팻 " in equip_text:
            pet_to_equip = next((pet for pet in game_state.pets if pet.level == level), None)
            if pet_to_equip:
                if level <= game_state.pat_level:
                    # 팻이 장착되어 있지 않으면 장착, 이미 장착되어 있으면 해제
                    if pet_to_equip in game_state.equipped_pat:
                        pet_to_equip.unequip(game_state)  # 이미 장착된 팻은 해제
                    else:
                        pet_to_equip.equip(game_state, level)  # 장착되지 않은 팻은 장착
                else:
                    game_state.add_message(f"팻 {level}를 구입하지 않음.")
            else:
                game_state.add_message(f"존재하지 않는 팻: {level}")
        
        elif "맵 " in equip_text:
            if level <= game_state.map_level:
                game_state.equip_map(level)
                game_state.money_increased = True
                game_state.character_x = 0
            else:
                game_state.add_message(f"맵 {level}를 가지고 있지 않음.")
    
    except ValueError as e:
        print(f"오류 발생: {e}. 입력된 값: {equip_text}")
