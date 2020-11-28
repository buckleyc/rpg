def die_roll_str(d) -> str:
	if len(d) == 1:
		return d
	else:
		return f"{d[0]}d{d[1]} [{d[2]}]"


def dmg_icon(type='bludgeoning') -> str:
	import re
	dmgs = {
		'bludgeoning': u'🔨',
		'piercing': u'🗡',
		'slashing': u'⚔️',
		'acid': u'',
		'cold': u'❄️',
		'fire': u'🔥',
		'force': u'💨',
		'lightning': u'⚡️',
		'necrotic': u"\u2623",  # u'💀', ☣
		'poison': u"\u2620",
		'psychic': u'🧠',
		'radiant': u"\u2622",  # u'💥',
		'thunder': u'☁️',
		'sneak': u'😏',
	}
	# 'necrotic': u'💀',
	# 'radiant': u'💥',
	return dmgs[type]


class Weapon:
	"""Weapons"""

	# name, category, distance, cost, damagetype, rollstr, weight, properties

	def __init__(self, name='my weapon', *,
				 regExpSearch='', source=[],
				 list='', ability=1, type='',damage=[[1,4,'fire']], range='',
				 description='', monkweapon=False, abilitytodamage=True,
				 weight=0, ammo='', dc=8, baseWeapon=',',
				 magical=False, bonus_magic=0,
				 ):
		self.name = name
		self.regExpSearch = regExpSearch
		self.source = source
		self.list = list
		self.ability = ability
		self.type = type
		self.damage = damage
		self.range = range
		self.description = description
		self.monkweapon = monkweapon
		self.abilitytodamage = abilitytodamage
		self.weight = weight
		self.ammo = ammo
		self.dc = dc
		self.baseWeapon = baseWeapon
		self.magical = magical
		self.bonus_magic = bonus_magic

		self.cost = 0
		self.prof = False
		self.bonus_attack = 0
		self.bonus_damage = []
		self.rollstrappend = ''
		self.dice_roll_str = ''
		self.properties = description
		self.versatile = False

	def get_my_damage(self):
		return self._damage

	def get_my_bonus_damage(self):
		return self._bonus_damage

	def set_my_damage(self, val):
		self._damage = val
		# generate dice_roll_str when damage is updated
		roll_str = " + ".join([die_roll_str(d) for d in self._damage])

		# roll_str_bonus = " + ".join([f"{d[0]}d{d[1]} [{d[2]}]" for d in self._bonus_damage])
		# print(roll_str)
		self.dice_roll_str = roll_str

	# now my_list can be used as a variable
	damage = property(get_my_damage, set_my_damage, None, 'this damage makes the dice_roll_str')
	# bonus_damage = property(get_my_bonus_damage, set_my_damage, None, 'append bonus_damage to dice_roll_str')

	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

	def weapon_roll(self, type='attack'):
		# todo: unify as 'weapon_roll('attack'|'damage)
		import d20
		if type in 'attack':
			self.rollstr += f"{self.bonus_attack:+}"
		elif type in 'damage':
			self.rollstr += f"{self.bonus_damage:+}"
		if self.rollstrappend:
			self.rollstr += f"{self.rollstrappend:+}"
		# rolls = [random.randint(1, self.sides) for _ in range(self.dice)]
		rolls = d20.roll(self.rollstr).total
		# print(rolls)
		return rolls

	def attack_roll(self, type='damage'):
		import d20
		if type in 'attack':
			#
			self.rollstr += f"{self.bonus_attack:+}"
		elif type in 'damage':
			self.rollstr += f"{self.bonus_damage:+}"
		if self.rollstrappend:
			self.rollstr += f"{self.rollstrappend:+}"
		# rolls = [random.randint(1, self.sides) for _ in range(self.dice)]
		rolls = d20.roll(self.rollstr).total
		# print(rolls)
		return rolls
