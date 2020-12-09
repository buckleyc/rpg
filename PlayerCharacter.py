def ability_score_mod(score):
	return score // 2 - 5


def level_proficiency(level):
	return (level - 1) // 4 + 2


class PC:
	def __init__(self, name='',
				 cclass=None, race=None, background=None, level=1,
				 cstr=8, cdex=8, ccon=8, cint=8, cwis=8, ccha=8,
				 ac=8, hp=1, proficiency=None):
		if proficiency is None:
			self.proficiency = {
				'skill': {},
				'armour': {},
				'weapon': {},
				'save': {},
				'resistance': {},
				'language': {},
				'tool': {},
				'savetxt': {},
				'vision': {},
				'speed': {},
				'specialarmour': {},
				'carryingcapacity': {},
				'advantage': {}
			}
		self.name = name
		self.cclass = cclass
		self.race = race
		self.background = background
		self.level = level
		self.cstr = cstr
		self.cdex = cdex
		self.ccon = ccon
		self.cint = cint
		self.cwis = cwis
		self.ccha = ccha
		self.ac = ac
		self.hp = hp
		self.feature = None
		self.feat = []
		# ToDo: Add Skills
		self.skills = {}
		self.tools = {}
		self.expertise = {'skill': []}
		self.crit = 20
		self.feature = []
		self.crits_revisited = False


	def __str__(self):
		# return str(self.__class__) + ": " + str(self.__dict__)
		return f"{self.name} is a {self.cclass} {self.race} that has a background as a {self.background} {self.specialty if self.specialty else ''}."


	def __repr__(self):
		return str(self.__class__) + ": " + str(self.__dict__)


	def attack_bonus(self, weapon) -> str:
		# What is the attacker's ATTACK Bonus for this weapon?
		bonus = []

		# Ability Modifier
		if 'finesse' in weapon.description.lower():
			# print('Finesse')
			bonus.append(max(ability_score_mod(self.cstr), ability_score_mod(self.cdex)))
		elif weapon.list == 'ranged':
			bonus.append(ability_score_mod(self.cdex))
			# print(bonus[-1])
		elif weapon.list == 'melee':
			bonus.append(ability_score_mod(self.cstr))

		# Proficiency: Is attacker proficient with this weapon?
		# print(f"Checking attack Proficiency : weapon type = {weapon.type}, attacker weapon prof. = {self.proficiency['weapon']}")
		if weapon.type.lower() in self.proficiency['weapon']:
			bonus.append(level_proficiency(self.level))

		# Magic Weapon Bonus: Is weapon magical?
		if weapon.magical:
			bonus.append(weapon.bonus_magic)

		# Does attacker have any Class Features? E.g., Archery Fighting Style
		# ToDo: Need to support Class Features
		if weapon.list == 'ranged' and 'Archery' in self.feature:
				bonus.append(2)

		atk_bonus = ' + '.join([str(i) for i in bonus])
		# print(f" -> Attack bonus = {atk_bonus}")
		return atk_bonus

	def damage_bonus(self, weapon) -> str:
		# What is the attacker's DAMAGE Bonus for this weapon?
		bonus = []

		# Ability Modifier
		if 'finesse' in weapon.description.lower():
			# print('Finesse')
			bonus.append(max(ability_score_mod(self.cstr), ability_score_mod(self.cdex)))
		elif weapon.list == 'ranged':
			bonus.append(ability_score_mod(self.cdex))
		elif weapon.list == 'melee':
			bonus.append(ability_score_mod(self.cstr))

		# Magic Weapon Bonus: Is weapon magical?
		if weapon.magical:
			bonus.append(weapon.bonus_magic)

		# Does attacker have any Class Features? E.g., XXX
		# ToDo: Need to support Class Features

		dmg_bonus = ' + '.join([str(i) for i in bonus])
		# print(f" -> Damage bonus = {dmg_bonus}")
		return dmg_bonus

	def save(self, score):
		return ability_score_mod(score) + level_proficiency(self.level)

	def tool(self, /, req=''):
		tool_bonus = {}
		for s in ['tool']:
			if s in self.proficiency:
				for p in self.proficiency[s]:
					# print(fr"{p}")
					tool_bonus[p] = tool_bonus.setdefault(p, 0) + level_proficiency(self.level)

		sorted_tuples = sorted(tool_bonus.items(), key=lambda item: item[0])
		# print(sorted_tuples)
		sorted_tool_bonus = {k: v for k, v in sorted_tuples}
		self.tools = sorted_tool_bonus

		# for k, v in sorted_tool_bonus.items():
		# 	# print(f"{req.lower()} in {k.lower()}")
		# 	if req.lower() in k.lower():
		# 		print(f"{k}: {v:+}")
		return

	def skill(self, /, req='as'):
		skills = {
			'Strength': ['Athletics'],
			'Dexterity': ['Acrobatics', 'Sleight of Hand', 'Stealth'],
			'Intelligence': ['Arcana', 'History', 'Investigation', 'Nature', 'Religion'],
			'Wisdom': ['Animal' 'Handling', 'Insight', 'Medicine', 'Perception', 'Survival'],
			'Charisma': ['Deception', 'Intimidation', 'Persuasion', 'Performance'],
		}
		skill_bonus = {}
		# [[i for i in test_dict[x]] for x in test_dict.keys()]
		for k in skills.keys():
			for s in skills[k]:
				skill_bonus[s] = ability_score_mod(getattr(self, f"c{k.lower()[0:3]}"))
		# print(f"{s} = {skill_bonus[s]}")
		for s in ['skill', 'expertise']:
			if s in self.proficiency:
				for p in self.proficiency[s]:
					# print(fr"{p}")
					skill_bonus[p] = skill_bonus[p] + level_proficiency(self.level)
		sorted_tuples = sorted(skill_bonus.items(), key=lambda item: item[0])
		# print(sorted_tuples)
		sorted_skill_bonus = {k: v for k, v in sorted_tuples}
		self.skills = sorted_skill_bonus

		# for k, v in sorted_skill_bonus.items():
		# 	# print(f"{req.lower()} in {k.lower()}")
		# 	if req.lower() in k.lower():
		# 		print(f"{k}: {v:+}")
		return

	def check(self, what='', adv=False, dis=False):
		import d20
		skills = {
			'Strength': ['Athletics'],
			'Dexterity': ['Acrobatics', 'Sleight of Hand', 'Stealth'],
			'Intelligence': ['Arcana', 'History', 'Investigation', 'Nature', 'Religion'],
			'Wisdom': ['Animal' 'Handling', 'Insight', 'Medicine', 'Perception', 'Survival'],
			'Charisma': ['Deception', 'Intimidation', 'Persuasion', 'Performance'],
		}
		for k in skills.keys():
			if what in skills[k]:
				ability = k

		nouns = list(self.skills.keys()) + list(self.tools.keys())
		# print(list(self.skills.keys()))
		if adv:
			roll_str = "2d20kh1"
		elif dis:
			roll_str = "2d20kl1"
		else:
			roll_str = f"1d20"

		mymod = ability_score_mod(getattr(self, f"c{ability.lower()[0:3]}"))
		roll_str += f"{mymod:+}"
		roll_str += f"{level_proficiency(self.level):+}" if what in self.proficiency else ""
		if what in nouns:
			# print(f"Found {what}")
			print(f"{self.name} performs a {what} check : {d20.roll(roll_str)}")

	def attack_roll(self, adv=False, dis=False) -> str:
		if adv:
			if 'Elven Accuracy' in self.feat:
				roll_str = "3d20kh1"
			else:
				roll_str = "2d20kh1"
		elif dis:
			roll_str = "2d20kl1"
		else:
			roll_str = f"1d20"
		return roll_str

	def saving_throw(self, ability='Constitution', *, adv=False, dis=False, bless=False):
		import d20
		if adv:
			roll_str = "2d20kh1"
		elif dis:
			roll_str = "2d20kl1"
		else:
			roll_str = f"1d20"
		my_d20 = d20.roll(roll_str).total
		my_d4 = d20.roll('1d4').total
		my_total = my_d20 + my_d4 if bless else my_d20
		if 'death' in ability.lower():
			print(f"{self.name} rolls a Death Saving Throw, and ", end='')
			if my_d20 == 1:
				print(f"Failed TWICE with a roll of 1.")
				return
			elif my_d20 == 20:
				print(f"Succeeded TWICE with a roll of 20.")
				return
			if my_total < 10:
				print(f"Failed with a roll of {my_total}.")
				return
			else:
				print(f"Succeeded with a roll of {my_total}.")
				return
		else:
			mymod = ability_score_mod(getattr(self, f"c{ability.lower()[0:3]}"))
			roll_str += f"{mymod:+}"
			# print(self.proficiency['save'])
			roll_str += f"{level_proficiency(self.level):+}" if ability in self.proficiency['save'] else ""
			roll_str += f"+1d4" if bless else ""
			print(f"{self.name} performs a {ability} check : {d20.roll(roll_str)}")

