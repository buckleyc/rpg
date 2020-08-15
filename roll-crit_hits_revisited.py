#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Critical Hits Revisited
"""

# Futures
from __future__ import unicode_literals

# Generic/Built-in
import random
import textwrap

# Other Libs
from typing import Any, Union
# from colorama import Fore, Style

# Owned
# from {path} import {class}

__author__ = "Buckley Collum"
__copyright__ = "Copyright 2020, QuoinWorks"
__credits__ = ["Buckley Collum"]
__license__ = "GNU General Public License v3.0"
__version__ = "0.0.1"
__maintainer__ = "Buckley Collum"
__email__ = "buckleycollum@gmail.com"
__status__ = "Dev"


class Die(object):
	def __init__(self, sides=6):
		self.sides = sides

	def roll(self):
		return random.randint(1, self.sides)


class Weapon:
	def __init__(self, name, dice, sides, damagetype):
		self.name = name
		self.dice = dice
		self.sides = sides
		self.damagetype = damagetype

	def roll(self):
		rolls = [random.randint(1, self.sides) for _ in range(self.dice)]
		# print(rolls)
		return rolls


class Color:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


damages = {
	'bludgeoning':
	(
		("You call that a crit?", 1, "", ''),
		("Smashed off balance!", 1,
			"Your next attack against the creature has advantage.", ''),
		("Good hit!", 2, "", ''),
		("Sent reeling!", 2,
			"You push the creature up to 15 feet in any direction.", ''),
		("Great hit!", 3, "", ''),
		("Take a seat!", 3,
			"The creature is knocked prone.", ''),
		("Rocked and rolled!", 3,
			"You push the creature up to 15 feet away, and the creature is knocked prone.", ''),
		("Grievous injury!", 4, "", 'minor'),
		("Crushed!", 5, "", 'major'),
		("Splat!", 5, "The creature is stunned until the end of your next turn.", 'major')
	),
	'piercing':
	(
		("You call that a crit?", 1, "", ''),
		("Lunge and thrust!", 3, "", ''),
		("Good hit!", 2, "", ''),
		("Stabbed!", 3, "", ''),
		("Great hit!", 3, "", ''),
		("Swiss cheese!", 3, "", 'minor'),
		("Punctured!", 3, "", 'minor'),
		("Cruel prick!", 3, "", 'major'),
		("Run through!", 4, "", 'major'),
		("Pierce!", 5, "", 'major')
	),
	'slashing':
	(
		("You call that a crit?", 1, "", ''),
		("Sliced and diced!", 1,
			"The creature loses 1d6 hit points at the start of its next turn.", ''),
		("Good hit!", 2, "", ''),
		("Open gash!", 1,
			"The creature is bleeding! For the next minute the creature loses 1d4 damage"
			"at the start of each of its turns until it uses an action to staunch this wound.", ''),
		("Great hit!", 3, "", ''),
		("Deep slice!", 3,
			"The creature is bleeding! For the next minute the creature loses 1d8 hit points "
			"at the start of each of its turns until it uses an action to staunch this wound.", ''),
		("Lacerated!", 3,
			"The creature is bleeding! For the next minute the creature loses 1d12 hit points "
			"at the start of each of its turns until it uses an action to staunch this wound.", ''),
		("Severed!", 4, "", 'minor'),
		("Dissected!", 5, "", 'major'),
		("Slash!", 5,
			"The creature is bleeding! For the next minute the creature loses 2d8 hit points "
			"at the start of each of its turns until it uses an action to staunch this wound.", 'major')
	),
	'acid':
	(
		("You call that a crit?", 1, "", ''),
		("Scalding bile!", 1,
			"The creature is scarred. While scarred the creature has "
			"disadvantage on all Charisma ability checks except Charisma (Intimidation). "
			"Being scarred can be healed in the same way as a minor injury.", ''),
		("Good hit!", 2, '', ''),
		("Melted flesh!", 1,
			"The creature is disfigured. While disfigured the creature has "
			"disadvantage on all Charisma ability checks except Charisma (Intimidation). "
			"Being disfigured can be removed with the spell greater restoration.", ''),
		("Great hit!", 3, "", ''),
		("Boiling flesh!", 3,
			"If the creature is wearing armor its AC modifier is reduced by 1 until "
			"it can be repaired (for 1/4th the price of new armor of the same type) "
			"or cleaned (if the armor is magical). If the creature is not wearing armor, "
			"roll on the minor injury chart.", 'minor'),
		("Horrific mutilation!", 3,
			"the creature is disfigured. While disfigured the creature has disadvantage "
			"on all Charisma ability checks except Charisma (Intimidation). "
			"Being disfigured can be removed with the spell greater restoration.", 'minor'),
		("Caustic trauma!", 4,
			"If the creature is wearing armor, roll on the minor injury chart and "
			"its AC modifier is reduced by 2 until it can be repaired (for half the price "
			"of new armor of the same type) or cleaned (if the armor is magical). "
			"If the creature is not wearing armor, roll on the major injury chart.", 'major'),
		("Vitriolic!", 5, "", 'major'),
		("Acid bath!", 5,
			"If the creature is wearing armor, the armor is destroyed (if non-magical)or "
			"rendered useless until cleaned during a long rest (if magical) and roll on "
			"the major injury chart. If the creature is not wearing armor, roll on the "
			"major injury chart and the creature is disfigured. "
			"While disfigured the creature has disadvantage on all Charisma ability checks "
			"except Charisma (Intimidation). Being disfigured can be removed with "
			"the spell greater restoration.", 'major')
	),
	'cold':
	(
		("You call that a crit?", 1, "", ''),
		("Scalding bile!", 1,
			"The creature may only move half its movement speed on its next turn.", ''),
		("Good hit!", 2, "", ''),
		("Frosty!", 1,
			"The creature’s movement speed is 0 until the end of its next turn.", ''),
		("Great hit!", 3, "", ''),
		("Freezing!", 3,
			"The creature is paralyzed until the end of its next turn.", ''),
		("Frozen!", 3,
			"The creature is paralyzed until the end of its next turn. "
			"If the creature takes damage before the end of its next turn, "
			"roll on the minor injury chart.", ''),
		("Ice block!", 4,
			"The creature is paralyzed until the end of its next turn and "
			"rolls on the minor injury chart.", 'minor'),
		("Glacial!", 5, "", 'major'),
		("Subzero!", 5, "The creature is paralyzed for the next minute. "
						"The creature may attempt a saving throw at the end "
						"of each of its turns (DC 16) to end this effect. "
						"If it fails this saving throw three times it is "
						"frozen solid and becomes a petrified but frozen solid "
						"in a block of ice rather than turned to stone.", 'major')
	),
	'fire':
	(
		("You call that a crit?", 1, "", ''),
		("Heat wave!", 1,
		 "Attack rolls for attacks that deal fire damage have advantage "
		 "when made against the creature until the end of its next turn.", ''),
		("Good hit!", 2, "", ''),
		("Hot flash!", 1,
		 "The creature is on fire. While the creature is on fire it takes "
		 "2d4 fire damage at the start of each of its turns. "
		 "The creature can end this condition by dropping prone and "
		 "using 5 feet of movement to roll on the ground.", ''),
		("Great hit!", 3, "", ''),
		("Ablaze!", 3,
		 "The creature is on fire. While the creature is on fire, "
		 "it takes 2d6 fire damage at the start of each of its turns. "
		 "The creature can end this condition by dropping prone and "
		 "using 5 feet of movement to roll on the ground.", ''),
		("Burnt to a crisp!", 3,
		 "The creature is charred. If the creature has resistance to fire, "
		 "it loses that resistance. If the creature does not have resistance "
		 "to fire, it gains vulnerability to fire. Both of these effects can "
		 "be ended the same as a minor injury.", ''),
		("Hellfire!", 4,
		 "The creature is on fire. While the creature is on fire it takes "
		 "2d6 fire damage at the start of each of its turns. The creature can "
		 "end this condition by dropping prone and using 5 feet of movement "
		 "to roll on the ground.", 'minor'),
		("Combustion!", 5, "", 'major'),
		("Inferno!", 5,
		 "The creature is on fire. While the creature is on fire it takes "
		 "2d8 fire damage at the start of each of its turns. "
		 "The creature can end this condition by dropping prone and "
		 "using 5 feet of movement to roll on the ground.", 'major')
	),
	'force':
	(
		("You call that a crit?", 1, "", ''),
		("Spellstruck!", 1,
		 "The creature has disadvantage on saving throws against "
		 "spells until the end of its next turn.", ''),
		("Good hit!", 2, "", ''),
		("Eldritch incandescence!", 1,
		 "Spell attack rolls against the creature have advantage "
		 "until the end of its next turn.", ''),
		("Great hit!", 3, "", ''),
		("Bewitching blow!", 3,
		 "The creature is spellbound until the end of its next turn. "
		 "While spellbound it makes saving throws against spells with "
		 "disadvantage and spell attack rolls against it have advantage.", ''),
		("Mystic magnet!", 3,
		 "The creature is spellbound for the next minute. "
		 "While spellbound it makes saving throws against spells with "
		 "disadvantage and spell attack rolls against it have advantage. "
		 "At the end of each of the creature’s turns it can make an Intelligence "
		 "saving throw (DC 14) to end this effect.", 'minor'),
		("Ensorcelled!", 4,
		 "the creature is spellbound for the next minute. "
		 "While spellbound it makes saving throws against spells with "
		 "disadvantage and spell attack rolls against it have advantage. "
		 "At the end of each of the creature’s turns it can make an "
		 "Intelligence saving throw (DC 16) to end this effect.", ''),
		("Arcane injury!", 5, "", 'major'),
		("Magically mauled!", 5,
		 "The creature is spellbound for the next minute. "
		 "While spellbound it makes saving throws against spells with "
		 "disadvantage and spell attack rolls against it have advantage. "
		 "At the end of each of the creature’s turns it can make an "
		 "Intelligence saving throw (DC 18) to end this effect.", 'major')
	),
	'lightning':
	(
		("You call that a crit?", 1, "", ''),
		("Shocking!", 1,
		 "The creature cannot use reactions until the end of its next turn.", ''),
		("Good hit!", 2, "", ''),
		("Sparks fly!", 1,
		 "You may choose one other creature within 15 ft. of the victim. "
		 "That creature must succeed on a Dexterity saving throw (DC 14) or "
		 "take half as much damage.", ''),
		("Great hit!", 3, "", ''),
		("Electric arc!", 3,
		 "You may choose one other creature within 15 ft. of the victim. "
		 "That creature must succeed on a Dexterity saving throw (DC 18) or "
		 "take half as much damage.", 'minor'),
		("Fulminate!", 3,
		 "If the creature is wearing metal armor, then roll on the major injury chart instead.", 'minor'),
		("Lit up!", 4,
		 "The creature and each creature you choose within 15 ft. of it "
		 "cannot take reactions until the end of their next turn.", 'minor'),
		("Electrocuted!", 5, "", 'major'),
		("Lightning rod!", 5,
		 "You may choose one other creature within 15 ft. of the victim. "
		 "That creature must succeed on a Dexterity saving throw (DC 20) or "
		 "take half as much damage.", 'major')
	),
	'necrotic':
	(
		("You call that a crit?", 1, "", ''),
		("Spoil!", 1,
		 "The creature cannot regain hit points until the end of its next turn.", ''),
		("Good hit!", 2, "", ''),
		("Fester!", 1,
		 "The creature’s maximum hit points are reduced by the same amount.", ''),
		("Great hit!", 3, "", ''),
		("Decay!", 3,
		 "The creature’s maximum hit points are reduced by the same amount.", ''),
		("Rot!", 3,
		 "the creature cannot regain hit points for the next minute. "
		 "It may make a saving throw (DC 16) at the end of each of its turns to end this effect.", ''),
		("Blight!", 4,
		 "The creature’s maximum hit points are reduced by the same amount. ", 'minor'),
		("Atrophy!", 5, "", 'major'),
		("Putrefy!", 5,
		 "The creature’s maximum hit points are reduced by the same amount, and "
		 "the creature cannot regain hit points until the end of its next turn. ", 'major')
	),
	'poison':
	(
		("You call that a crit?", 1, "", ''),
		("Nauseous!", 1,
		 "The creature has disadvantage on its next ability check, "
		 "attack roll, or saving throw.", ''),
		("Good hit!", 2, "", ''),
		("Sickened!", 1,
		 "The creature has disadvantage on all ability checks, "
		 "attack rolls, and saving throws until the end of its next turn.", ''),
		("Great hit!", 3, "", ''),
		("Poisoned!", 3,
		 "The creature may attempt a saving throw (DC 12) at the end of each "
		 "of its turns to end this effect.", 'minor'),
		("Contaminated!", 3,
		 "The creature is poisoned for the next minute. "
		 "The creature may attempt a saving throw (DC 16) at the end of each "
		 "of its turns to end this effect.", ''),
		("Toxic shock!", 4,
		 "The creature is poisoned for the next minute. "
		 "The creature may attempt a saving throw (DC 12) at the end of each "
		 "of its turns to end this effect.", 'minor'),
		("System failure!", 5, "", 'major'),
		("Biological breakdown!", 5,
		 "The creature is poisoned for the next minute. "
		 "The creature may attempt a saving throw (DC 16) at the end of each "
		 "of its turns to end this effect.", 'major')
	),
	'psychic':
	(
		("You call that a crit?", 1, "", ''),
		("Disoriented!", 1,
		 "You control the creature’s movement on its next turn.", ''),
		("Confused!", 1,
		 "The creature cannot differentiate friend from foe until the end of its next turn.", ''),
		("Good hit!", 2, "", ''),
		("Great hit!", 3, "", ''),
		("Dominated!", 3,
		 "You control the creature’s action on its next turn.", ''),
		("Psychological fracture!", 3, "", 'insanity.disadvantage()'),
		("Psychological break!", 4, "", 'insanity'),
		("Madness!", 5, "", 'insanity'),
		("Mind melt!", 5, "", 'insanity.advantage()')
	),
	'radiant':
	(
		("You call that a crit?", 1, "", ''),
		("Scalding bile!", 1, "", ''),
		("Good hit!", 2, "", ''),
		("Melted flesh!", 1, "", ''),
		("Great hit!", 3, "", ''),
		("Boiling flesh!", 3, "", 'minor'),
		("Horrific mutilation!", 3, "", 'minor'),
		("Caustic trauma!", 4, "", 'major'),
		("Vitriolic!", 5, "", 'major'),
		("Acid bath!", 5, "", 'major')
	),
	'thunder':
	(
		("You call that a crit?", 1, "", ''),
		("Scalding bile!", 1, "", ''),
		("Good hit!", 2, "", ''),
		("Melted flesh!", 1, "", ''),
		("Great hit!", 3, "", ''),
		("Boiling flesh!", 3, "", 'minor'),
		("Horrific mutilation!", 3, "", 'minor'),
		("Caustic trauma!", 4, "", 'major'),
		("Vitriolic!", 5, "", 'major'),
		("Acid bath!", 5, "", 'major')
	),
}

injuries = {
	'minor':
		(
			"Injured leg! The creature’s movement speed is reduced by 10 ft.",
			"Injured arm! Randomly determine one of the creature’s arms. "
			"That arm cannot be used to hold a shield and the creature has "
			"disadvantage on any rolls involving the use of that arm.",
			"Multiple injuries! The creature’s maximum hit points are "
			"reduced by an amount equivalent to half of the damage dealt by the attack.",
			"Badly beaten! The creature has disadvantage on Constitution saving throws",
			"Ringing blow! The creature is stunned until the end of its "
			"next turn and deafened until it completes a the recuperate downtime activity.",
			"Blow to the head! The creature is unconscious for 2d12 hours.",
		),
	'major':
		(
			"Crippled leg! The creature’s movement speed is reduced by 10 feet and "
			"it has disadvantage on Dexterity saving throws.",
			"Crippled arm! Randomly determine one of the creature’s arms. "
			"That arm cannot be used to hold an item and any ability check requiring "
			"that arm automatically fails or has disadvantage (DM’s choice).",
			"Severely wounded! The creature’s maximum hit points are reduced by an "
			"amount equivalent to the damage dealt by the attack.",
			"Edge of death! The creature has disadvantage on Constitution and death saving throws.",
			"My eyes! The creature is blinded.",
			"Decapitated! The creature is dead.",
		)
}


insanities = {
	1:	'Synesthesia. You can hear colors, smell sounds, or taste textures. '
		'Regardless of the specific manifestation, you have disadvantage on all Perception and Investigation skill checks.',
	2:	'Kleptomania. Once per day when you are in a personal residence or marketplace, '
		'the DM can call on you to succeed on a Wisdom saving throw (DC 12) or '
		'attempt to steal an item of insignificant practical and monetary value.',
	3:	'Paranoia. Once per day following an interaction with another creature '
		'(including other PCs) the DM can call on you to succeed on a Wisdom saving '
		'throw (DC 12) or you suspect that creature is secretly plotting against you.',
	4:	'Obsession. Choose a person or personal interest you are obsessed with. '
		'Once per day, when you are presented with an opportunity to interact with or '
		'learn more about the subject of your obsession, then the DM can call on you '
		'to succeed on a Wisdom saving throw (DC 14) or ignore everything else to '
		'obsess over the object of your fascination.',
	5:	'Addiction. Choose a behavior or substance you have used.'
		'Once per day, when you are presented with an opportunity to do '
		'the behavior or use the substance, the DM can call on you to succeed on a Wisdom '
		'saving throw (DC 14) or ignore everything else to indulge in your vice.',
	6:	'Odd Thinking. Once per day when you hear a rational explanation for an event or '
		'occurrence, your DM may call on you to succeed on a Wisdom saving throw (DC 12) or '
		'you reject the rational explanation for a conspiratorial or fantastical explanation.',
	7:	'Narcissism. When you take an action or series of action that doesn\’t directly benefit you, '
		'you must pass a Wisdom saving throw (DC 11) or you can’t take that action or series of actions. '
		'If any self-sacrifice on your part would be required, then the DC of the saving throw is '
		'increased to 16.',
	8:	'Delusional. When you gain this insanity, the DM will tell you a belief that you have. '
		'No matter what evidence is presented to the contrary, so long as you have this insanity, '
		'you cannot be persuaded that this belief is not true.',
	9:	'Pica. Once per day the DM can call on you to pass a Wisdom saving throw (DC 14) or '
		'immediately eat one non-food object (such as dirt, napkins, or a small piece of jewelry) '
		'of the DM\’s choice.',
	10: 'Retrograde amnesia. You forget everything about your personal life prior to the moment '
		'you received this insanity.',
	11: 'Overwhelmed. If you do not have immunity or resistance to psychic damage, '
		'then you gain vulnerability to psychic damage. If you have resistance to '
		'psychic damage, then you lose it. If you have immunity to psychic damage, '
		'then you lose it but gain resistance to psychic damage.',
	12: 'Anterograde amnesia. Whenever you try to recall a fact you learned since you '
		'received this insanity, make a Wisdom saving throw (DC 12). If you fail you '
		'cannot recall the fact.',
	13: 'Dependence. You must pass a Wisdom saving throw (DC 14) to take an action '
		'that one or more of your allies disapprove of.',
	14: 'Anxious. You have disadvantage on saving throws against being frightened. '
		'Additionally, once per day the DM can call on you to succeed a Wisdom saving '
		'throw (DC 14) or be frightened by a creature of the DM’s choosing for the next minute.',
	15: 'Mute. Whenever you wish to speak aloud (including casting a spell that has verbal components), '
		'then you must succeed on a Wisdom saving throw (DC 13) to do so.',
	16: 'Narcolepsy. You have disadvantage on saving throws against sleeping or unconsciousness. '
		'Once per day the DM may call on you to succeed on a Constitution saving throw (DC 12) or '
		'fall unconscious for one minute or until you take damage or another creature spends '
		'their action trying to rouse you.',
	17: 'Insomnia. You cannot take long rests and your short rests take 8 hours to complete.',
	18: 'Homicidal. After each long rest you must pass a Wisdom saving throw (DC 14) or be '
		'overcome with the urge to end the life of a humanoid creature and you cannot benefit '
		'from another long rest until you do so.',
	19: 'Suicidal. After each long rest you must pass a Wisdom saving throw (DC 12) or '
		'make an attempt to end your own life.',
	20: 'Catatonia. You are unconscious for 10d10 years.',
}


def roll(d=20):
	"""Roll a 'd'-sided dice"""
	return random.randint(1, d)


def attack(target=None, weapon=None, advantage=False, disadvantage=False, condition=None):
	output = f"Attacking {'' if target == None else target} with {weapon.name}."
	print(f"{' '.join(output.split())}")
	if advantage or disadvantage:
		rolls = [roll(20) for x in range(2)]
		myroll = rolls.max() if advantage else rolls.min()
	else:
		myroll = roll(20)
	# myroll = 20
	if myroll == 1:
		criticalmiss()
	elif myroll == 20:
		criticalhit(weapon)
	else:
		hitanddamage(myroll, weapon)


def criticalmiss():
	print(f"{Color.FAIL}Critical Fail!{Color.ENDC}")
	mymiss = roll(20)
	if mymiss < 3:
		print("Weapon breaks!")
	elif mymiss < 6:
		print("Dropped weapon! Disadvantage on next attack, and lose 10ft of motion next turn to pick up weapon.")
	elif mymiss < 11:
		print("Fumbled weapon! Lose half your motion next turn as you gain your composure.")
	else:
		print("You missed spectacularly, and your opponent snickered at your failure.")


def criticalhit(weapon):
	print(f"{Color.HEADER}Critical Hit!{Color.ENDC}")
	rollmatch = {
		1: 0,
		2: 1, 3: 1,
		4: 2, 5: 2, 6: 2,
		7: 3, 8: 3,
		9: 4, 10: 4, 11: 4,
		12: 5, 13: 5,
		14: 6, 15: 6, 16: 6,
		17: 7, 18: 7,
		19: 8,
		20: 9,
	}

	mycrit = roll(20)
	title, value, effect, injurytype = damages[weapon.damagetype][rollmatch[mycrit]]
	critdamage = pointscritdamage(weapon, value)
	wrapper = textwrap.TextWrapper(width=40, initial_indent="* ", subsequent_indent=" + ")
	output = f" {Color.HEADER}{title}{Color.ENDC} Your {weapon.name.lower()} does " \
			 f"{Color.WARNING}{sum(critdamage)}{Color.ENDC} {critdamage} points of " \
			 f"{Color.WARNING}{weapon.damagetype}{Color.ENDC} damage.\n"
	if effect:
		if 'the creature' in effect.lower():
			index = effect.lower().find('the creature')
			revision1 = effect[:index+13] + ' TARGET' + effect[index:]
		else:
			revision1 = effect
		if 'the same amount' in revision1.lower():
			index = revision1.lower().find('the same amount')
			revision2 = revision1[:index+15] + f" ({sum(critdamage)}" + revision1[index:]
		else:
			revision2 = revision1
		output += f"  {Color.FAIL}{revision2.capitalize()}{Color.ENDC}\n"
	if injurytype:
		if injurytype == 'insanity':
		output += f"  {Color.FAIL}{injurytype.title()} Injury: {injury(injurytype)}{Color.ENDC}\n"
	wrapper.text = output
	print(f"{wrapper.text}")


def pointscritdamage(weapon, value):
	critdamage = []
	if value == 1:
		critdamage.extend(weapon.roll())
	elif value == 2:
		critdamage.append(weapon.sides)
	elif value == 3:
		critdamage.extend(weapon.roll())
		critdamage.extend(weapon.roll())
	elif value == 4:
		critdamage.append(weapon.sides)
		critdamage.extend(weapon.roll())
	elif value == 5:
		critdamage.append(weapon.sides)
		critdamage.append(weapon.sides)
	return critdamage


def hitanddamage(attackroll, weapon):
	damage = weapon.roll()
	output = f" Your Attack roll is {Color.OKGREEN}{attackroll}{Color.ENDC}."\
		f" Your {weapon.name.lower()} caused {Color.OKGREEN}{sum(damage)}{Color.ENDC}"\
		f" {damage if weapon.dice > 1 else ''} points of " \
		f"{Color.OKGREEN}{weapon.damagetype.capitalize()}{Color.ENDC} damage."
	print(" ".join(output.split()))


def injury(injurytype=''):
	if not injurytype:
		return
	rollmatch = {
		1: 0, 2: 0, 3: 0,
		4: 1, 5: 1, 6: 1, 7: 1, 8: 1,
		9: 2, 10: 2, 11: 2,
		12: 3, 13: 3, 14: 3, 15: 3, 16: 3,
		17: 4, 18: 4, 19: 4,
		20: 5
	}
	return injuries[injurytype][rollmatch[roll(20)]]


def main():
	longsword = Weapon("Longsword", 1, 8, 'slashing')
	maul = Weapon("Maul", 2, 6, 'bludgeoning')
	greatsword = Weapon("Greatsword", 2, 6, 'slashing')
	dagger = Weapon("Dagger", 1, 4, 'piercing')
	lance = Weapon("Lance", 1, 12, 'piercing')
	# print(f"{longsword.name} dmg = {longsword.roll()}")
	attack(weapon=random.choice([longsword, maul, greatsword, dagger, lance]))


# print(injury(random.choice([True, False])))


if __name__ == '__main__':
	main()
