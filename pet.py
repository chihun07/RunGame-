import pygame
from GameState import *

class Pet:
    def __init__(self, level, size, color, max_size, min_size, y, money_increase_factor=0):
        self.level = level
        self.size = size
        self.max_size = max_size
        self.min_size = min_size
        self.color = color
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)
        self.x = 0
        self.y = y  # 초기 위치 설정
        self.size_change_direction = 1  # 크기 증가 방향
        self.last_size_change_time = pygame.time.get_ticks()  # 크기 변경을 위한 시간 추적 변수
        self.x_offset = 5  # x 좌표의 이동 범위
        self.money_increase_factor = money_increase_factor  # 돈 증가율
        self.last_money_increase_time = pygame.time.get_ticks()  # 돈 증가 시간 추적 변수

    def update_size(self):
        """팻의 크기를 시간이 지나면서 변화시키기 위한 함수"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_size_change_time > 1000:
            self.last_size_change_time = current_time
            if self.size_change_direction == 1:
                self.size += 2
                self.y -= 2
                self.x_offset -= 1
                if self.size >= self.max_size:
                    self.size_change_direction = -1
            else:
                self.size -= 2
                self.y += 2
                self.x_offset += 1
                if self.size <= self.min_size:
                    self.size_change_direction = 1
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill(self.color)

    def increase_money(self):
        """1초마다 돈을 증가시키기 위한 함수"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_money_increase_time >= 1000:  # 1초마다 돈 증가
            self.last_money_increase_time = current_time  # 마지막 증가 시간 갱신
            return self.money_increase_factor  # 팻의 money_increase_factor에 따라 돈 증가
        
        return 0  # 1초가 지나지 않으면 돈 증가 없음

    def update_position(self, character_x, index):
        """팻 위치 업데이트 (장착된 순서에 맞게 y 위치 조정)"""
        self.x = character_x - self.size - 20 + self.x_offset - index * 60  # x_offset을 기준으로 이동
        self.y = self.y  # y 좌표는 변경되지 않음

    def equip(self, game_state, pet_level):
        """팻을 장착하는 함수"""
        if self.level <= pet_level:
            game_state.equipped_pat.append(self)
            game_state.add_message(f"팻 {self.level} 장착 완료!")
            game_state.pet_money += self.money_increase_factor  # GameState의 pet_money 증가
        else:
            game_state.add_message(f"팻 {self.level}를 구입하지 않았습니다.")

    def unequip(self, game_state):
        """장착된 팻을 해제하는 함수"""
        if self in game_state.equipped_pat:
            game_state.equipped_pat.remove(self)
            game_state.add_message(f"팻 {self.level} 해제 완료!")
            game_state.pet_money -= self.money_increase_factor
        else:
            game_state.add_message(f"팻 {self.level}는 이미 해제된 상태입니다.")

