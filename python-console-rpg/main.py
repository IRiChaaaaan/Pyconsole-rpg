import os
import random
import itertools
import pandas as pd
from enum import Enum

scene = -1

filename_csv_player  = "./csv/player.csv"
filename_csv_enemies = "./csv/enemies.csv"

def main():
	# プレイヤー読み込み
	player = introduction()
	
	while True:
		scene = scene_select(player)
	
		if scene == 1:
			up_status(player)
			scene = -1
		elif scene == 2:
			stage_select(player)
			scene = -1
		elif scene == 3:
			save_status(player)
			break

def title():
	os.system('cls')
	print("------------------------")
	print("Console RPG")
	print("------------------------")
	print()

def introduction():
	while True:
		title()
		print("はじめから( 1 )")
		print("つづきから( 2 )")
		print()
		print("対応する値を入力してください -> ", end = "")
		val = input_int()
		if val == -1:
			continue
		print()
		if val == 1:
			# プレイヤーデータの作成
			print("あなたの名前を入力してください -> ", end = "")
			name = input()
			player = Actor(name, [3, 3, 3, 3, 3, 0])
			return player
		elif val == 2:
			# プレイヤーデータの読み込み
			if not os.path.exists(filename_csv_player):
				print("データがありません")
				print("はじめからはじめてください( Enterを押してください )", end = "")
				input()
				continue
			df = pd.read_csv(filename_csv_player)
			param = df.values.tolist()[0]
			player = Actor(param[0], param[1:])
			return player

def scene_select(player):
	while True:
		title()
		print("名前：" + player.name)
		print()
		text = ["ステータス振り分け", "ステージ選択", "セーブして終わる"]
		for i in range(len(text)):
			print(text[i] + "( " + str(i + 1) + " )")
		# 入力
		print()
		print("対応する値を入力してください -> ", end = "")
		val = input_int()
		if val == -1:
			continue
		if val > 0 and val < len(text) + 1:
			return val
	return -1

def stage_select(player):
	stage = []
	stage.append(["平野", "始まりの森", "始まりの洞窟"])
	stage.append(["湿原", "沼地", "湿った洞窟", "迷いの森"])
	stage.append(["砂漠", "砂漠の塔", "砂漠の洞窟"])
	stage.append(["雪原", "雪山", "吹雪の森", "氷の洞窟"])
	stage.append(["荒野", "火山", "炎の洞窟"])
	stage.append(["おわりの大地"])
	
	while True:
		title()
		for i in range(6):
			print("ステージ" + str(i + 1))
		print()
		print("ステージを選択してください( 0を入力すると前に戻る ) -> ", end = "")
		stage_num = input_int()
		if stage_num == -1:
			continue
		if stage_num == 0:
			break
		if stage_num > 0 and stage_num < 7:
			while True:
				title()
				for i in range(len(stage[stage_num - 1])):
					print(str(i + 1) + ":" + stage[stage_num - 1][i])
				print()
				print("ステージを選択してください( 0を入力すると前に戻る ) -> ", end = "")
				field_num = input_int()
				if field_num == -1:
					continue
				if field_num > 0 and field_num < len(stage[stage_num - 1]) + 1:
					battle(stage[stage_num - 1][field_num - 1], player)
				if field_num == 0:
					break

def battle(name, player):
	# 敵読み込み
	df = pd.read_csv(filename_csv_enemies)
	param = df.values.tolist()
	enemies = []
	for i, p in enumerate(param):
		if p[-1] == name:
			enemies.append(Actor(param[i][0], param[i][1:7]))
	
	while True:
		title()
		print("---" + name + "---")
		print()
		print("探索  ( 1 )")
		print("おわる( 2 )")
		print()
		print("値を入力してください -> ", end = "")
		select = input_int()
		if select == -1:
			continue
		rand = random.randrange(len(enemies))
		enemy = enemies[rand]
		if select == 2:
			break
		elif select == 1:
			while True:
				title()
				print(player.name + " -> HP：" + str(player.parameters.HP) + " / " + str(player.parameters.HP_MAX))
				print()
				print(enemy.name + "が現れた")
				print(enemy.name + " -> HP：" + str(enemy.parameters.HP) + " / " + str(enemy.parameters.HP_MAX))
				print()
				print("攻撃  ( 1 )")
				print("逃げる( 2 )")
				print()
				print("値を入力してください -> ", end = "")
				command = input_int()
				if command == -1:
					continue
				if command == 1:
					if player.parameters.AGI > enemy.parameters.AGI:
						print()
						print(enemy.name + "に" + str(enemy.damage(player.parameters.ATK)) + "ダメージを与えた")
						print()
						enemy.parameters.HP -= enemy.damage(player.parameters.ATK)
						if enemy.parameters.HP <= 0:
							print(enemy.name + "を倒しました")
							print(str(enemy.parameters.EXP) + "の経験値を得ました")
							player.parameters.EXP += enemy.parameters.EXP
							enemy.parameters.HP = enemy.parameters.HP_MAX
							player.parameters.HP = player.parameters.HP_MAX
							print()
							print("Enterを押してください", end = "")
							input()
							break
						print("プレイヤーは" + str(player.damage(enemy.parameters.ATK)) + "ダメージ受けた")
						print()
						player.parameters.HP -= player.damage(enemy.parameters.ATK)
						if player.parameters.HP <= 0:
							print(enemy.name + "に倒されました")
							player.parameters.HP = player.parameters.HP_MAX
							enemy.parameters.HP = enemy.parameters.HP_MAX
							print("経験値が半分になりました")
							player.parameters.EXP -= int(player.parameters.EXP / 2)
							print()
							print("Enterを押してください", end = "")
							input()
							break
						print()
						print("Enterを押してください", end = "")
						input()
					else:
						print()
						print("プレイヤーは" + str(player.damage(enemy.parameters.ATK)) + "ダメージ受けた")
						print()
						player.parameters.HP -= player.damage(enemy.parameters.ATK)
						if player.parameters.HP <= 0:
							print(enemy.name + "に倒されました")
							player.parameters.HP = player.parameters.HP_MAX
							print("経験値が半分になりました")
							player.parameters.EXP -= int(player.parameters.EXP / 2)
							print()
							print("Enterを押してください", end = "")
							input()
							break
						print(enemy.name + "に" + str(enemy.damage(player.parameters.ATK)) + "ダメージを与えた")
						print()
						enemy.parameters.HP -= enemy.damage(player.parameters.ATK)
						if enemy.parameters.HP <= 0:
							print(enemy.name + "を倒しました")
							print(str(enemy.parameters.EXP) + "の経験値を得ました")
							player.parameters.EXP += enemy.parameters.EXP
							enemy.parameters.HP = enemy.parameters.HP_MAX
							player.parameters.HP = player.parameters.HP_MAX
							print()
							print("Enterを押してください", end = "")
							input()
							break
						print()
						print("Enterを押してください", end = "")
						input()
				elif command == 2:
					enemy.parameters.HP = enemy.parameters.HP_MAX
					player.parameters.HP = player.parameters.HP_MAX
					break

def up_status(player):
	while True:
		title()
		print("ステータス")
		print(" HP ：" + str(player.parameters.HP))
		print(" ATK：" + str(player.parameters.ATK))
		print(" DEF：" + str(player.parameters.DEF))
		print(" AGI：" + str(player.parameters.AGI))
		print()
		print("振り分けポイント -> " + str(player.parameters.EXP))
		print()
		print("HP( 1 ), ATK( 2 ), DEF( 3 ), AGI( 4 )")
		print()
		print("上昇させるパラメータに対応する値を入力してください( 0を入力すると終わる ) -> ", end = "")
		val = input_int()
		if val == -1:
			continue
		if val < 0 or val > 4:
			print()
			print("正しい値を入力してください( Enterを押してください )", end = "")
			input()
			continue
		if val == 0:
			break
		print("上昇させる数値を入力してください -> ", end = "")
		num = input_int()
		if num == -1:
			continue
		if player.parameters.EXP >= num:
			player.up_status(val, num)
		else:
			print("振り分けポイント以上を入力しています( Enterを押してください )", end = "")
			input()

def save_status(player):
	data = [player.name]
	for p in player.parameters.get_parameters():
		data.append(p)
	data = [data]
	df = pd.DataFrame(data, columns = ["名前", "HP", "HP_MAX", "ATK", "DEF", "AGI", "EXP"])
	df.to_csv(filename_csv_player, index=False)

def input_int():
	val = input()
	if not val.isdigit():
		return -1
	val = int(val)
	return val

class Parameters:
	def __init__(self):
		self.HP     = 0
		self.HP_MAX = 0
		self.ATK    = 0
		self.DEF    = 0
		self.AGI    = 0
		self.EXP    = 0
	
	def set_parameters(self, param):
		self.HP     = int(param[0])
		self.HP_MAX = int(param[1])
		self.ATK    = int(param[2])
		self.DEF    = int(param[3])
		self.AGI    = int(param[4])
		self.EXP    = int(param[5])
	
	def get_parameters(self):
		data = [self.HP, self.HP_MAX, self.ATK, self.DEF, self.AGI, self.EXP]
		return data

###  役職クラス  ###
class Actor:
	
	def __init__(self, name, param):
		self.name = name
		self.parameters = Parameters()
		self.parameters.set_parameters(param)
	
	def damage(self, atk):
		damage = atk * 2 / self.parameters.DEF
		return int(damage)
	
	def up_status(self, kind, num):
		if kind == 1:
			self.parameters.HP += num
			self.parameters.HP_MAX += num
		elif kind == 2:
			self.parameters.ATK += num
		elif kind == 3:
			self.parameters.DEF += num
		elif kind == 4:
			self.parameters.AGI += num
		self.parameters.EXP -= num

if __name__ == "__main__":
	main()
