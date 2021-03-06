#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Critical Hits Revisited
"""

# Futures
from __future__ import unicode_literals

import sys
import logging
import inspect
import csv
import random
import re
import textwrap

# Other Libs
# from typing import Any, Union
# from colorama import Fore, Style
import d20
from Weapon import Weapon
from PlayerCharacter import PC

# Owned
# from {path} import {class}

__author__ = "Buckley Collum"
__copyright__ = "Copyright 2020, QuoinWorks"
__credits__ = ["Buckley Collum"]
__license__ = "GNU General Public License v3.0"
__version__ = "0.1.6"
__maintainer__ = "Buckley Collum"
__email__ = "buckleycollum@gmail.com"
__status__ = "Dev"


default_loglevel = 'warning'


class Color:
	HEADER = "\033[95m"
	BLUE = "\033[94m"
	GREEN = "\033[92m"
	YELLOW = "\033[93m"
	RED = "\033[91m"
	ENDC = "\033[0m"
	BOLD = "\033[1m"
	UNDERLINE = "\033[4m"


characterClass = {
	"artificer": {"proficiency": {"weapon": ["simple"]}},
	"barbarian": {"proficiency": {"weapon": ["simple", "martial"]}},
	"bard": {"proficiency": {"weapon": ["simple", "martial"]}},
	"cleric": {"proficiency": {"weapon": ["simple"]}},
	"druid": {"proficiency": {"weapon": ["simple", "martial"]}},
	"fighter": {"proficiency": {"weapon": ["simple", "martial"]}},
	"monk": {"proficiency": {"weapon": ["simple"]}},
	"paladin": {"proficiency": {"weapon": ["simple", "martial"]}},
	"ranger": {"proficiency": {"weapon": ["simple", "martial"]}},
	"rogue": {"proficiency": {"weapon": ["simple", "martial"]}},
	"sorcerer": {"proficiency": {"weapon": ["simple", "martial"]}},
	"warlock": {"proficiency": {"weapon": ["simple", "martial"]}},
	"wizard": {"proficiency": {"weapon": ["simple", "martial"]}},
}

damages = {
	"bludgeoning": (
		("You call that a crit?", 1, "", ""),
		(
			"Smashed off balance!",
			1,
			"Your next attack against the creature has advantage.",
			"",
		),
		("Good hit!", 2, "", ""),
		(
			"Sent reeling!",
			2,
			"You push the creature up to 15 feet in any direction.",
			"",
		),
		("Great hit!", 3, "", ""),
		("Take a seat!", 3, "The creature is knocked prone.", ""),
		(
			"Rocked and rolled!",
			3,
			"You push the creature up to 15 feet away, and the creature is knocked prone.",
			"",
		),
		("Grievous injury!", 4, "", "minor"),
		("Crushed!", 5, "", "major"),
		(
			"Splat!",
			5,
			"The creature is stunned until the end of your next turn.",
			"major",
		),
	),
	"piercing": (
		("You call that a crit?", 1, "", ""),
		("Lunge and thrust!", 3, "", ""),
		("Good hit!", 2, "", ""),
		("Stabbed!", 3, "", ""),
		("Great hit!", 3, "", ""),
		("Swiss cheese!", 3, "", "minor"),
		("Punctured!", 3, "", "minor"),
		("Cruel prick!", 3, "", "major"),
		("Run through!", 4, "", "major"),
		("Pierce!", 5, "", "major"),
	),
	"slashing": (
		("You call that a crit?", 1, "", ""),
		(
			"Sliced and diced!",
			1,
			"The creature loses 1d6 hit points at the start of its next turn.",
			"",
		),
		("Good hit!", 2, "", ""),
		(
			"Open gash!",
			1,
			"The creature is bleeding! For the next minute the creature loses 1d4 damage"
			"at the start of each of its turns until it uses an action to staunch this wound.",
			"",
		),
		("Great hit!", 3, "", ""),
		(
			"Deep slice!",
			3,
			"The creature is bleeding! For the next minute the creature loses 1d8 hit points "
			"at the start of each of its turns until it uses an action to staunch this wound.",
			"",
		),
		(
			"Lacerated!",
			3,
			"The creature is bleeding! For the next minute the creature loses 1d12 hit points "
			"at the start of each of its turns until it uses an action to staunch this wound.",
			"",
		),
		("Severed!", 4, "", "minor"),
		("Dissected!", 5, "", "major"),
		(
			"Slash!",
			5,
			"The creature is bleeding! For the next minute the creature loses 2d8 hit points "
			"at the start of each of its turns until it uses an action to staunch this wound.",
			"major",
		),
	),
	"acid": (
		("You call that a crit?", 1, "", ""),
		(
			"Scalding bile!",
			1,
			"The creature is scarred. While scarred the creature has "
			"disadvantage on all Charisma ability checks except Charisma (Intimidation). "
			"Being scarred can be healed in the same way as a minor injury.",
			"",
		),
		("Good hit!", 2, "", ""),
		(
			"Melted flesh!",
			1,
			"The creature is disfigured. While disfigured the creature has "
			"disadvantage on all Charisma ability checks except Charisma (Intimidation). "
			"Being disfigured can be removed with the spell greater restoration.",
			"",
		),
		("Great hit!", 3, "", ""),
		(
			"Boiling flesh!",
			3,
			"If the creature is wearing armor its AC modifier is reduced by 1 until "
			"it can be repaired (for 1/4th the price of new armor of the same type) "
			"or cleaned (if the armor is magical). If the creature is not wearing armor, "
			"roll on the minor injury chart.",
			"minor",
		),
		(
			"Horrific mutilation!",
			3,
			"the creature is disfigured. While disfigured the creature has disadvantage "
			"on all Charisma ability checks except Charisma (Intimidation). "
			"Being disfigured can be removed with the spell greater restoration.",
			"minor",
		),
		(
			"Caustic trauma!",
			4,
			"If the creature is wearing armor, roll on the minor injury chart and "
			"its AC modifier is reduced by 2 until it can be repaired (for half the price "
			"of new armor of the same type) or cleaned (if the armor is magical). "
			"If the creature is not wearing armor, roll on the major injury chart.",
			"major",
		),
		("Vitriolic!", 5, "", "major"),
		(
			"Acid bath!",
			5,
			"If the creature is wearing armor, the armor is destroyed (if non-magical)or "
			"rendered useless until cleaned during a long rest (if magical) and roll on "
			"the major injury chart. If the creature is not wearing armor, roll on the "
			"major injury chart and the creature is disfigured. "
			"While disfigured the creature has disadvantage on all Charisma ability checks "
			"except Charisma (Intimidation). Being disfigured can be removed with "
			"the spell greater restoration.",
			"major",
		),
	),
	"cold": (
		("You call that a crit?", 1, "", ""),
		(
			"Scalding bile!",
			1,
			"The creature may only move half its movement speed on its next turn.",
			"",
		),
		("Good hit!", 2, "", ""),
		(
			"Frosty!",
			1,
			"The creature’s movement speed is 0 until the end of its next turn.",
			"",
		),
		("Great hit!", 3, "", ""),
		(
			"Freezing!",
			3,
			"The creature is paralyzed until the end of its next turn.",
			"",
		),
		(
			"Frozen!",
			3,
			"The creature is paralyzed until the end of its next turn. "
			"If the creature takes damage before the end of its next turn, "
			"roll on the minor injury chart.",
			"",
		),
		(
			"Ice block!",
			4,
			"The creature is paralyzed until the end of its next turn and "
			"rolls on the minor injury chart.",
			"minor",
		),
		("Glacial!", 5, "", "major"),
		(
			"Subzero!",
			5,
			"The creature is paralyzed for the next minute. "
			"The creature may attempt a saving throw at the end "
			"of each of its turns (DC 16) to end this effect. "
			"If it fails this saving throw three times it is "
			"frozen solid and becomes a petrified but frozen solid "
			"in a block of ice rather than turned to stone.",
			"major",
		),
	),
	"fire": (
		("You call that a crit?", 1, "", ""),
		(
			"Heat wave!",
			1,
			"Attack rolls for attacks that deal fire damage have advantage "
			"when made against the creature until the end of its next turn.",
			"",
		),
		("Good hit!", 2, "", ""),
		(
			"Hot flash!",
			1,
			"The creature is on fire. While the creature is on fire it takes "
			"2d4 fire damage at the start of each of its turns. "
			"The creature can end this condition by dropping prone and "
			"using 5 feet of movement to roll on the ground.",
			"",
		),
		("Great hit!", 3, "", ""),
		(
			"Ablaze!",
			3,
			"The creature is on fire. While the creature is on fire, "
			"it takes 2d6 fire damage at the start of each of its turns. "
			"The creature can end this condition by dropping prone and "
			"using 5 feet of movement to roll on the ground.",
			"",
		),
		(
			"Burnt to a crisp!",
			3,
			"The creature is charred. If the creature has resistance to fire, "
			"it loses that resistance. If the creature does not have resistance "
			"to fire, it gains vulnerability to fire. Both of these effects can "
			"be ended the same as a minor injury.",
			"",
		),
		(
			"Hellfire!",
			4,
			"The creature is on fire. While the creature is on fire it takes "
			"2d6 fire damage at the start of each of its turns. The creature can "
			"end this condition by dropping prone and using 5 feet of movement "
			"to roll on the ground.",
			"minor",
		),
		("Combustion!", 5, "", "major"),
		(
			"Inferno!",
			5,
			"The creature is on fire. While the creature is on fire it takes "
			"2d8 fire damage at the start of each of its turns. "
			"The creature can end this condition by dropping prone and "
			"using 5 feet of movement to roll on the ground.",
			"major",
		),
	),
	"force": (
		("You call that a crit?", 1, "", ""),
		(
			"Spellstruck!",
			1,
			"The creature has disadvantage on saving throws against "
			"spells until the end of its next turn.",
			"",
		),
		("Good hit!", 2, "", ""),
		(
			"Eldritch incandescence!",
			1,
			"Spell attack rolls against the creature have advantage "
			"until the end of its next turn.",
			"",
		),
		("Great hit!", 3, "", ""),
		(
			"Bewitching blow!",
			3,
			"The creature is spellbound until the end of its next turn. "
			"While spellbound it makes saving throws against spells with "
			"disadvantage and spell attack rolls against it have advantage.",
			"",
		),
		(
			"Mystic magnet!",
			3,
			"The creature is spellbound for the next minute. "
			"While spellbound it makes saving throws against spells with "
			"disadvantage and spell attack rolls against it have advantage. "
			"At the end of each of the creature’s turns it can make an Intelligence "
			"saving throw (DC 14) to end this effect.",
			"minor",
		),
		(
			"Ensorcelled!",
			4,
			"the creature is spellbound for the next minute. "
			"While spellbound it makes saving throws against spells with "
			"disadvantage and spell attack rolls against it have advantage. "
			"At the end of each of the creature’s turns it can make an "
			"Intelligence saving throw (DC 16) to end this effect.",
			"",
		),
		("Arcane injury!", 5, "", "major"),
		(
			"Magically mauled!",
			5,
			"The creature is spellbound for the next minute. "
			"While spellbound it makes saving throws against spells with "
			"disadvantage and spell attack rolls against it have advantage. "
			"At the end of each of the creature’s turns it can make an "
			"Intelligence saving throw (DC 18) to end this effect.",
			"major",
		),
	),
	"lightning": (
		("You call that a crit?", 1, "", ""),
		(
			"Shocking!",
			1,
			"The creature cannot use reactions until the end of its next turn.",
			"",
		),
		("Good hit!", 2, "", ""),
		(
			"Sparks fly!",
			1,
			"You may choose one other creature within 15 ft. of the victim. "
			"That creature must succeed on a Dexterity saving throw (DC 14) or "
			"take half as much damage.",
			"",
		),
		("Great hit!", 3, "", ""),
		(
			"Electric arc!",
			3,
			"You may choose one other creature within 15 ft. of the victim. "
			"That creature must succeed on a Dexterity saving throw (DC 18) or "
			"take half as much damage.",
			"minor",
		),
		(
			"Fulminate!",
			3,
			"If the creature is wearing metal armor, then roll on the major injury chart instead.",
			"minor",
		),
		(
			"Lit up!",
			4,
			"The creature and each creature you choose within 15 ft. of it "
			"cannot take reactions until the end of their next turn.",
			"minor",
		),
		("Electrocuted!", 5, "", "major"),
		(
			"Lightning rod!",
			5,
			"You may choose one other creature within 15 ft. of the victim. "
			"That creature must succeed on a Dexterity saving throw (DC 20) or "
			"take half as much damage.",
			"major",
		),
	),
	"necrotic": (
		("You call that a crit?", 1, "", ""),
		(
			"Spoil!",
			1,
			"The creature cannot regain hit points until the end of its next turn.",
			"",
		),
		("Good hit!", 2, "", ""),
		(
			"Fester!",
			1,
			"The creature’s maximum hit points are reduced by the same amount.",
			"",
		),
		("Great hit!", 3, "", ""),
		(
			"Decay!",
			3,
			"The creature’s maximum hit points are reduced by the same amount.",
			"",
		),
		(
			"Rot!",
			3,
			"the creature cannot regain hit points for the next minute. "
			"It may make a saving throw (DC 16) at the end of each of its turns to end this effect.",
			"",
		),
		(
			"Blight!",
			4,
			"The creature’s maximum hit points are reduced by the same amount. ",
			"minor",
		),
		("Atrophy!", 5, "", "major"),
		(
			"Putrefy!",
			5,
			"The creature’s maximum hit points are reduced by the same amount, and "
			"the creature cannot regain hit points until the end of its next turn. ",
			"major",
		),
	),
	"poison": (
		("You call that a crit?", 1, "", ""),
		(
			"Nauseous!",
			1,
			"The creature has disadvantage on its next ability check, "
			"attack roll, or saving throw.",
			"",
		),
		("Good hit!", 2, "", ""),
		(
			"Sickened!",
			1,
			"The creature has disadvantage on all ability checks, "
			"attack rolls, and saving throws until the end of its next turn.",
			"",
		),
		("Great hit!", 3, "", ""),
		(
			"Poisoned!",
			3,
			"The creature may attempt a saving throw (DC 12) at the end of each "
			"of its turns to end this effect.",
			"minor",
		),
		(
			"Contaminated!",
			3,
			"The creature is poisoned for the next minute. "
			"The creature may attempt a saving throw (DC 16) at the end of each "
			"of its turns to end this effect.",
			"",
		),
		(
			"Toxic shock!",
			4,
			"The creature is poisoned for the next minute. "
			"The creature may attempt a saving throw (DC 12) at the end of each "
			"of its turns to end this effect.",
			"minor",
		),
		("System failure!", 5, "", "major"),
		(
			"Biological breakdown!",
			5,
			"The creature is poisoned for the next minute. "
			"The creature may attempt a saving throw (DC 16) at the end of each "
			"of its turns to end this effect.",
			"major",
		),
	),
	"psychic": (
		("You call that a crit?", 1, "", ""),
		(
			"Disoriented!",
			1,
			"You control the creature’s movement on its next turn.",
			"",
		),
		(
			"Confused!",
			1,
			"The creature cannot differentiate friend from foe until the end of its next turn.",
			"",
		),
		("Good hit!", 2, "", ""),
		("Great hit!", 3, "", ""),
		("Dominated!", 3, "You control the creature’s action on its next turn.", ""),
		("Psychological fracture!", 3, "", "insanity.disadvantage()"),
		("Psychological break!", 4, "", "insanity"),
		("Madness!", 5, "", "insanity"),
		("Mind melt!", 5, "", "insanity.advantage()"),
	),
	"radiant": (
		("You call that a crit?", 1, "", ""),
		("Scalding bile!", 1, "", ""),
		("Good hit!", 2, "", ""),
		("Melted flesh!", 1, "", ""),
		("Great hit!", 3, "", ""),
		("Boiling flesh!", 3, "", "minor"),
		("Horrific mutilation!", 3, "", "minor"),
		("Caustic trauma!", 4, "", "major"),
		("Vitriolic!", 5, "", "major"),
		("Acid bath!", 5, "", "major"),
	),
	"thunder": (
		("You call that a crit?", 1, "", ""),
		("Scalding bile!", 1, "", ""),
		("Good hit!", 2, "", ""),
		("Melted flesh!", 1, "", ""),
		("Great hit!", 3, "", ""),
		("Boiling flesh!", 3, "", "minor"),
		("Horrific mutilation!", 3, "", "minor"),
		("Caustic trauma!", 4, "", "major"),
		("Vitriolic!", 5, "", "major"),
		("Acid bath!", 5, "", "major"),
	),
}


def dmg_icon(damage_type="bludgeoning") -> str:
	dmgs = {
		"bludgeoning": "🔨",
		"piercing": "🗡",
		"slashing": "⚔️",
		"acid": "",
		"cold": "❄️",
		"fire": "🔥",
		"force": "💨",
		"lightning": "⚡️",
		"necrotic": "\u2623",  # u'💀', ☣
		"poison": "\u2620",
		"psychic": "🧠",
		"radiant": "\u2622",  # u'💥',
		"thunder": "☁️",
		"sneak": "😏",
	}
	# 'necrotic': u'💀',
	# 'radiant': u'💥',

	return dmgs[damage_type]


addon = {
	"none": [None, None],
	"minor": ["injury", "minor"],
	"major": ["injury", "major"],
	"insanity": ["insanity", ""],
	"insanity_adv": ["insanity", "advantage"],
	"insanity_dis": ["insanity", "disadvantage"],
}

injuryDescription = {
	"minor": (
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
	"major": (
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
	),
}


def csv_dict_list(variables_file):
	# Open csv, iterate over the rows and map values to a list of dictionaries containing key/value pairs

	reader = csv.DictReader(open(variables_file, "r"))
	dict_list = []
	for line in reader:
		dict_list.append(line)
	return dict_list


def insanity(i):
	switcher = {
		1: "Synesthesia. You can hear colors, smell sounds, or taste textures. "
			"Regardless of the specific manifestation, you have disadvantage on all "
			"Perception and Investigation skill checks.",
		2: "Kleptomania. Once per day when you are in a personal residence or marketplace, "
			"the DM can call on you to succeed on a Wisdom saving throw (DC 12) or "
			"attempt to steal an item of insignificant practical and monetary value.",
		3: "Paranoia. Once per day following an interaction with another creature "
			"(including other PCs) the DM can call on you to succeed on a Wisdom saving "
			"throw (DC 12) or you suspect that creature is secretly plotting against you.",
		4: "Obsession. Choose a person or personal interest you are obsessed with. "
			"Once per day, when you are presented with an opportunity to interact with or "
			"learn more about the subject of your obsession, then the DM can call on you "
			"to succeed on a Wisdom saving throw (DC 14) or ignore everything else to "
			"obsess over the object of your fascination.",
		5: "Addiction. Choose a behavior or substance you have used."
			"Once per day, when you are presented with an opportunity to do "
			"the behavior or use the substance, the DM can call on you to succeed on a Wisdom "
			"saving throw (DC 14) or ignore everything else to indulge in your vice.",
		6: "Odd Thinking. Once per day when you hear a rational explanation for an event or "
			"occurrence, your DM may call on you to succeed on a Wisdom saving throw (DC 12) or "
			"you reject the rational explanation for a conspiratorial or fantastical explanation.",
		7: "Narcissism. When you take an action or series of action that doesn’t directly benefit you, "
			"you must pass a Wisdom saving throw (DC 11) or you can’t take that action or series of actions. "
			"If any self-sacrifice on your part would be required, then the DC of the saving throw is "
			"increased to 16.",
		8: "Delusional. When you gain this insanity, the DM will tell you a belief that you have. "
			"No matter what evidence is presented to the contrary, so long as you have this insanity, "
			"you cannot be persuaded that this belief is not true.",
		9: "Pica. Once per day the DM can call on you to pass a Wisdom saving throw (DC 14) or "
			"immediately eat one non-food object (such as dirt, napkins, or a small piece of jewelry) "
			"of the DM’s choice.",
		10: "Retrograde amnesia. You forget everything about your personal life prior to the moment "
			"you received this insanity.",
		11: "Overwhelmed. If you do not have immunity or resistance to psychic damage, "
			"then you gain vulnerability to psychic damage. If you have resistance to "
			"psychic damage, then you lose it. If you have immunity to psychic damage, "
			"then you lose it but gain resistance to psychic damage.",
		12: "Anterograde amnesia. Whenever you try to recall a fact you learned since you "
			"received this insanity, make a Wisdom saving throw (DC 12). If you fail you "
			"cannot recall the fact.",
		13: "Dependence. You must pass a Wisdom saving throw (DC 14) to take an action "
			"that one or more of your allies disapprove of.",
		14: "Anxious. You have disadvantage on saving throws against being frightened. "
			"Additionally, once per day the DM can call on you to succeed a Wisdom saving "
			"throw (DC 14) or be frightened by a creature of the DM’s choosing for the next minute.",
		15: "Mute. Whenever you wish to speak aloud (including casting a spell that has verbal components), "
			"then you must succeed on a Wisdom saving throw (DC 13) to do so.",
		16: "Narcolepsy. You have disadvantage on saving throws against sleeping or unconsciousness. "
			"Once per day the DM may call on you to succeed on a Constitution saving throw (DC 12) or "
			"fall unconscious for one minute or until you take damage or another creature spends "
			"their action trying to rouse you.",
		17: "Insomnia. You cannot take long rests and your short rests take 8 hours to complete.",
		18: "Homicidal. After each long rest you must pass a Wisdom saving throw (DC 14) or be "
			"overcome with the urge to end the life of a humanoid creature and you cannot benefit "
			"from another long rest until you do so.",
		19: "Suicidal. After each long rest you must pass a Wisdom saving throw (DC 12) or "
			"make an attempt to end your own life.",
		20: "Catatonia. You are unconscious for 10d10 years.",
	}
	return switcher.get(i, f"Invalid roll: {i}")


def roll(d=20):
	"""Roll a 'd'-sided dice"""
	return random.randint(1, d)


def advantage():
	return max([roll(20) for _ in range(2)])


def disadvantage():
	return min([roll(20) for _ in range(2)])


def append(incoming, hunt, new):
	if hunt.lower() in incoming.lower():
		index = incoming.lower().find(hunt.lower())
		return incoming[: index + len(hunt)] + new + incoming[index + len(hunt):]
	else:
		return incoming


def weapon_attack(
		attacker=None, target=None, weapon=None, adv=False, dis=False, condition=None
):
	# Attack Roll = Ability Modifier + Proficiency + Enchantment/Item Bonus + Class Features

	output = (
		f"{'' if attacker is None else attacker.name + ' is '} attacking "
		f"{'' if target is None else target} with the "
		f"{'magical +' + str(weapon.bonus_magic) if weapon.magical else ''} "
		f"{weapon.name}"
	)
	output += f", and has {Color.BLUE}Advantage{Color.ENDC}." if adv else ""
	print(f"{' '.join(output.split())}")  # clean any repeated spaces

	if condition:
		# ToDo: placeholder to handle influence of condition, e.g., blinded
		pass

	# If Rogue and has Advantage, then add sneak attack damage to weapon
	if "Rogue" in attacker.cclass and adv:
		regexp = re.compile("(\\d+).*Rogue")
		rogue_level = int(regexp.search(attacker.cclass).group(1))  # get Rogue level
		weapon.damage += [[(rogue_level + 1) // 2, 6, "sneak"]]  # append sneak damage to Weapon

	attack_roll_str = attacker.attack_roll(adv, dis)

	d20roll = d20.roll(attack_roll_str)

	# d20roll = d20.roll('20')
	# Critical 20, for testing
	logging.debug(d20roll.crit)
	print(f'\tYour Attack roll is ', end='')
	if d20roll.crit == d20.CritType.CRIT or d20roll.total >= attacker.crit:
		print(f"a Critical HIT: {d20roll.result}")
		criticalhit(attacker, weapon, target)
	elif d20roll.crit == d20.CritType.FAIL:  # total == 1:
		print(f"a Critical Fail: {d20roll.result}")
		critical_miss(weapon)
	else:
		attackbonus = attacker.attack_bonus(weapon)
		attack_result_str = " + ".join([str(d20roll.total), attackbonus])
		attack_result = d20.roll(f"{attack_result_str}")
		print(
			f"{attack_roll_str} + {attackbonus} = {attack_result_str.replace(' ', '')} = {Color.YELLOW}{attack_result.total}{Color.ENDC}."
		)
		hitanddamage(attacker, weapon, target)


def die_roll_str(d) -> str:
	return f"{d[0]}d{d[1]} [{d[2]}]"


def critical_miss(weapon=None):
	print(f"{Color.RED}Critical Fail!{Color.ENDC}")

	def indent(my_paragraph) -> str:
		return f"\t{my_paragraph}"

	print(f"Critical fail roll for d100 is {roll(100)}")  # for David Gavrin's table

	mymiss = roll(20)
	if mymiss == 1:
		if weapon:
			if weapon.magical:
				print(f"\tMagic backfires!")
				magic_damage = d20.roll('+'.join([die_roll_str(weapon.damage[0]), str(weapon.bonus_magic)]))
				print(
					f"\tYou take {magic_damage.result} points of {weapon.damage[0][2]} damage."
				)
			elif weapon.list == "ranged":
				print(
					f"\tThe bowstring on {weapon.name} broke!\n"
					f"\tOn your next turn you lose your Action and half your movement.\n"
					f"\tEither use your next turn to replace the string, or switch weapons."
				)
			else:
				print(
					f"\tDangerous Design-Flaw! {weapon.name} broke, and injured you.\n"
					f"\tTake {d20.roll(die_roll_str(weapon.damage[0])).result} points of {weapon.damage[0][2]} damage."
				)
			print(f"")
		# print("Weapon breaks!")
	elif mymiss < 4:
		print(
			"\tPoor attack: Has 50% chance to hit any character in the line of attack or within 5' of the target."
		)
		if random.randint(0, 1):
			print(f"\tWhuh? Looks like you missed everyone.")
		else:
			print(
				f"\tYour victim takes {d20.roll(weapon.dice_roll_str).result} points of damage."
			)
		print(
			f"\tAlso, due to dismay, lose your next Bonus Action (either this turn or the next turn)."
		)
	elif mymiss < 6:
		print(
			"\tDropped weapon! Disadvantage on next attack, and lose 10ft of motion next turn to pick up weapon."
		)
	elif mymiss < 11:
		print(
			"\tFumbled weapon! Lose half your motion until the end of your next turn as you regain your composure."
		)
	else:
		print(
			"\tYou missed spectacularly, and your opponent snickered at your failure."
		)


def criticalhit(attacker, weapon, target=None, *, outside_roll=0):
	"""Critical Hit"""
	print(f"{Color.HEADER}Critical Hit!{Color.ENDC}")
	rollmatch = {
		1: 0,
		2: 1,
		3: 1,
		4: 2,
		5: 2,
		6: 2,
		7: 3,
		8: 3,
		9: 4,
		10: 4,
		11: 4,
		12: 5,
		13: 5,
		14: 6,
		15: 6,
		16: 6,
		17: 7,
		18: 7,
		19: 8,
		20: 9,
	}

	title = effect = also = ''
	if not attacker.crits_revisited:
		# Double the number of dice rolls for criticals; e.g., change '2d6' to '4d6'
		dice_roll_str = re.sub(
			"(\\d+)d", lambda m: str(int(m.groups()[0]) * 2) + "d", weapon.dice_roll_str
		)
	else:
		# Roll for Criticals Revisited lookup, if value not specified
		my_crit_roll = d20.roll("1d20").total if not outside_roll else outside_roll
		primary_damage_type = weapon.damage[0][2]
		title, value, effect, also = damages[primary_damage_type][rollmatch[my_crit_roll]]
		print(f"\tThe d20 roll for Crits Revisited is {my_crit_roll}")
		logging.debug(damages[weapon.damage[0][2]][rollmatch[my_crit_roll]])

		# add icons to damage type
		new_dmg = []
		for d in weapon.damage:
			n, s, t = d
			t += dmg_icon(t)
			new_dmg.append([n, s, t.title()])
		weapon.damage = new_dmg
		logging.debug(weapon.damage)

		dice_roll_str = crits_revisited_hp(weapon, value)

	dice_roll_str += f" + {attacker.damage_bonus(weapon)}"
	logging.debug(dice_roll_str)
	critdamage = d20.roll(dice_roll_str)

	print(
		f"\t{Color.HEADER}{title}{Color.ENDC} Your {weapon.name} does {critdamage.result} points "
		f"of {'magical ' if weapon.magical else ''}damage."
	)

	if attacker.crits_revisited:
		output = ""
		if effect:
			output += f"\t{Color.YELLOW}{effect}{Color.ENDC}\n"

		# ToDo: Add Insanity handling
		#  if also == 'insanity':
		if also == "":
			""" HACK to handle damage field that has '' instead of 'none' """
			also = "none"
		what, howmuch = addon[also]
		logging.debug("%s, %s", what, howmuch)
		# print(f" * {howmuch} {what}")
		if what == "injury":
			output += (
				f"\t{Color.RED}{howmuch.title()} Injury: {injury(howmuch)}{Color.ENDC}\n"
			)
		elif what == "insanity":
			output += f"\t{Color.YELLOW}Insanity: "
			if howmuch == "advantage":
				output += f"{insanity(advantage())}"
			elif howmuch == "disadvantage":
				output += f"{insanity(disadvantage())}"
			else:
				output += f"{insanity(roll())}"
			output += f"{Color.ENDC}\n"
		# ToDo: Clean-up TARGET name added into output
		if target is not None:
			pattern = re.compile(re.escape("creature"), re.IGNORECASE)
			output = pattern.sub(target, output)

		revision1 = (
			append(output, "The creature", f" {target}") if target is not None else effect
		)
		revision2 = append(revision1, "the same amount", f" ({critdamage.total})")

		wrapper = textwrap.TextWrapper(width=80, initial_indent="", subsequent_indent="  ")
		word_list = wrapper.wrap(text=revision2)
		for element in word_list:
			print(element)


def crits_revisited_hp(weapon, value) -> str:
	"""return string for crit revisited damage"""
	func = inspect.currentframe().f_code
	# FORMAT = "[ • %(funcName)20s() ] %(message)s"
	# logging.basicConfig(format=FORMAT)
	# logging.debug("%s", func.co_name)
	critdamage = []
	for die in weapon.damage:
		# logging.debug("Die = %s", str(die))
		quantity, sides, damage_type = die
		if value == 1:
			logging.debug('%s(): regular roll', func.co_name)
			critdamage.append(die_roll_str(die))
		elif value == 2:
			logging.debug('%s(): maximum regular roll', func.co_name)
			critdamage.append(str(sides))
		elif value == 3:
			logging.debug('%s(): double the rolls', func.co_name)
			# Double the number of dice rolled; e.g. change '2d6' to '4d6'
			critdamage.append(
				re.sub(
					"(\\d+)d",
					lambda m: str(int(m.groups()[0]) * 2) + "d",
					die_roll_str(die),
				)
			)
		elif value == 4:
			logging.debug('%s(): maximum + roll', func.co_name)
			critdamage.append(str(sides))
			critdamage.append(die_roll_str(die))
		elif value == 5:
			logging.debug('%s(): double maximum', func.co_name)
			# print([str(sides)] * (2 * quantity))
			# critdamage.extend([str(sides)] * (2 * quantity))
			critdamage.extend([f"{2 * quantity}*{str(sides)}"])

	# print(f"{value} and {critdamage}")
	logging.debug("crit damage revisited = %s", str(critdamage))
	return "+".join(critdamage)


def hitanddamage(attacker, weapon, target=None):
	rollplus = ""
	# print(attacker.feature)
	if attacker.feature == "Great Weapon Fighting":
		rollplus = "ro<3"
	damagebonus = attacker.damage_bonus(weapon)
	# print(damagebonus)
	rollplus += f"{damagebonus}"

	if weapon.magical > 0:
		rollplus += f"{weapon.bonus_magic:+}"

	new_dmg = []
	for d in weapon.damage:
		n, s, t = d
		t += dmg_icon(t)
		new_dmg.append([n, s, t.title()])
	# print(new_dmg)
	weapon.damage = new_dmg
	damage_roll_str = " + ".join([weapon.dice_roll_str, rollplus])
	# print(damage_roll_str)
	# dice_roll_str = damage_roll_str

	damage_result = d20.roll(damage_roll_str)
	damage_result_str = f"{damage_result.total}{rollplus}"
	damage_total = damage_result.total
	output = f"Your {weapon.name} "
	output += "caused " if target is None else f"targets {target} for "
	output += f" {damage_result.result} points of {'magical ' if weapon.magical else ''}damage."
	print(f"\t{' '.join(output.split())}")


def injury(injurytype=""):
	if not injurytype:
		return
	rollmatch = {
		1: 0,
		2: 0,
		3: 0,
		4: 1,
		5: 1,
		6: 1,
		7: 1,
		8: 1,
		9: 2,
		10: 2,
		11: 2,
		12: 3,
		13: 3,
		14: 3,
		15: 3,
		16: 3,
		17: 4,
		18: 4,
		19: 4,
		20: 5,
	}
	return injuryDescription[injurytype][rollmatch[roll(20)]]


def ordinal(n) -> str:
	return f"{n}{'tsnrhtdd'[(n / 10 % 10 != 1) * (n % 10 < 4) * n % 10:: 4]}"


def mypc(shortname="Malorin"):
	import logging
	import sqlite3

	sqlfile = "/Users/buckley/Desktop/5e/oldone/oldone.sqlite3"
	conn = sqlite3.connect(sqlfile)
	c = conn.cursor()

	pcid = 0
	hero = PC(shortname)

	try:
		# Select PC history
		sqlite_select_query = f"SELECT PCID, Level, Race, Background, Specialty FROM pc WHERE ShortName='{shortname}';"
		# logging.debug(sqlite_select_query)
		c.execute(sqlite_select_query)
		try:
			result = c.execute(sqlite_select_query).fetchone()
			logging.debug(result)
			if result is None:
				return hero
			pcid, hero.level, hero.race, hero.background, hero.specialty = result

		except sqlite3.Error as error:
			logging.error("Failed to read data from table: %s", error)
			c.close()
			return hero

	except sqlite3.Error as error:
		logging.error("Error while connecting to sqlite: %s", error)

	# Select PC Class
	sqlcmd = (
		f"SELECT c.Class,c.SubClass, c.Level FROM class AS c "
		f"INNER JOIN pc USING (PCID) WHERE ShortName='{shortname}';"
	)
	row = c.execute(sqlcmd).fetchall()
	classes = []
	for r in row:
		(cl, sub, lvl) = r
		classes.append(f"{ordinal(lvl)} level {sub} {cl}")
		# Champion Fighter - Improved Critical (19 or 20)
		if cl == "Fighter" and sub == "Champion":
			hero.crit = 19
	hero.cclass = f"{' and '.join(classes)}"

	# Select Ability Scores
	sqlcmd = (
		f"SELECT Ability, total(AbilityScore) FROM abilities "
		f"INNER JOIN pc USING (PCID) WHERE ShortName='{shortname}' "
		f"GROUP BY Ability;"
	)
	rows = c.execute(sqlcmd).fetchall()
	for (abi, n) in rows:
		abshort = f"c{abi.lower()[0:3]}"
		setattr(hero, abshort, int(n))

	# Select Proficiencies
	sqlcmd = f"SELECT Category, Item FROM proficiency WHERE PCID='{pcid}';"
	rows = c.execute(sqlcmd).fetchall()
	prof = {}
	for (key, item) in rows:
		prof.setdefault(key, []).append(item)
	hero.proficiency = prof

	# Select Feats
	conn.row_factory = lambda cursor, row: row[0]
	c = conn.cursor()
	feats = c.execute(f"SELECT Name FROM feat WHERE PCID='{pcid}';").fetchall()
	hero.feat = feats

	hero.skill()
	hero.tool()

	if conn:
		conn.close()

	return hero


def load_weapons(handle=None):
	import os
	import json
	import re
	from pathlib import Path
	data_folder = os.path.dirname(__file__)
	data_folder = Path(data_folder or Path.cwd())
	weapons_json_file = data_folder / r"Base_WeaponsList.json"
	with open(weapons_json_file, "r") as dataFile:
		data = dataFile.read()
	obj = json.loads(data)

	for k, v in obj.items():
		# newname = v["name"].replace(" ", "_").lower()
		pattern = re.compile(r"\b" + v["regExpSearch"], re.IGNORECASE)
		# print(f"{handle} -- {v['name']} -- {v['regExpSearch']}")
		if re.search(pattern, handle):
			# print(handle)
			my_weapon = Weapon(name=handle)
			for i in v.keys():
				if i == "damage":
					setattr(my_weapon, i, [v[i]])
				# print(f"{i} = {getattr(my_weapon, i)}")
				else:
					setattr(my_weapon, i, v[i])
			return my_weapon
	return Weapon("body odor")


def makepc():
	mybow = load_weapons("longbow")
	mybow.name = "Dark Blood Longbow"
	mybow.magical = True
	mybow.bonus_magic = 0

	myrapier = load_weapons("rapier")
	myrapier.name = f"Ebony Needle {myrapier.name}"

	malorin = mypc("Malorin")
	malorin.crits_revisited = True
	malorin.feature.append("Archery")

	# malorin.skill('stealth')
	# malorin.tool('thieves')

	# print(weapon.keys())
	weapon_attack(
		attacker=malorin,
		weapon=random.choice([mybow, myrapier]),
		adv=True,
		target=random.choice(["Orc", "Harpy"]),
	)

	# print(injury(random.choice([True, False])))

	malorin.check("Stealth")
	malorin.saving_throw("Death", bless=True)


def import_ClassData():
	import json

	with open(r"your_js_file.js") as dataFile:
		data = dataFile.read()
		obj = data[data.find("{"): data.rfind("}") + 1]
		jsonObj = json.loads(obj)


def get_mpmb_js(request: object = False) -> None:
	"""Pull/use JSON from NYT to report election results
	:type request: object
	"""
	import os
	import requests
	import json

	mpmb_github_path = r"https://github.com/morepurplemorebetter/MPMBs-Character-Record-Sheet/blob/master/_variables/"
	listsClasses_file = r"ListsClasses.js"
	mpmb_class_js_uri = mpmb_github_path + listsClasses_file

	if not os.path.exists(listsClasses_file):
		# if no JSON file, then get the file and save it to disk
		with requests.get(mpmb_class_js_uri) as r:
			with open(listsClasses_file, "w") as f:
				f.write(r.content)
			f.close()
		print(f"Pulled data and Wrote file {listsClasses_file}")

	with open(listsClasses_file) as dataFile:
		data = dataFile.read()
		obj = data[data.find("{"): data.rfind("}") + 1]
		print(obj)
		jsonObj = json.loads(obj)

	import pprint

	pprint.pprint(jsonObj)


# print(*[key for key in data['data']['races'][0]])
# for i, key in enumerate(data['data']['races'][0]):
# 	print(f"{key}") if i%5 == 4 else print(f"{key}  ", end="")


def setup_logging(verbosity=0):
	import os
	import logging

	base_loglevel = getattr(logging, (os.getenv("LOGLEVEL", default_loglevel)).upper())
	# print(base_loglevel)
	verbosity = min(verbosity, 2)
	loglevel = base_loglevel - (verbosity * 10)
	# print(loglevel)
	logging.basicConfig(level=loglevel, format=" • %(message)s")
	# logging.info(os.getenv('LOGLEVEL', default_loglevel).upper())


def parse_args():
	import argparse

	parser = argparse.ArgumentParser(
		description="RPG PC and Weapon roller."
	)
	parser.add_argument(
		"-v",
		"--verbose",
		dest="verbosity",
		action="count",
		default=0,
		help="verbose output (repeat for increased verbosity)",
	)
	parser.add_argument(
		"--adv",
		action='store_true',
		help="has Advantage"
	)
	parser.add_argument(
		"--dis",
		action='store_true',
		help="has Disadvantage"
	)
	args = parser.parse_args()

	setup_logging(args.verbosity)

	return args


def main(args):
	# My PC
	malorin = mypc("Malorin")
	malorin.feature.append("Archery")
	malorin.crits_revisited = True

	# My Weapons
	my_bow = load_weapons("longbow")
	my_bow.name = "Dark Blood Longbow"
	# my_bow.magical = True
	# my_bow.bonus_magic = 1
	# my_bow.damage += [[1, 8, "psychic"]]

	my_rapier = load_weapons("rapier")
	my_rapier.name = f"Ebony Needle {my_rapier.name}"

	my_weapon = load_weapons("maul")
	my_weapon.magical = True
	my_weapon.bonus_magic = 2
	my_weapon.damage += [[1, 8, "poison"]]
	if my_weapon.bonus_damage:
		my_weapon.damage += my_weapon.bonus_damage

	# malorin.skill('stealth')
	# malorin.tool('thieves')

	logging.info(malorin)

	# print(weapon.keys())
	weapon_attack(
		attacker=malorin,
		weapon=random.choice([my_bow]),
		adv=args.adv,
		dis=args.dis,
		target=random.choice(["Boney Lizard"]),
	)
	# criticalhit(malorin, my_bow)

	# All went well, so clean exit using None to return a 0 exit code
	return None


if __name__ == "__main__":
	ret = main(parse_args())  # main(sys.argv[1:])
	sys.exit(0 if ret is None else ret)
