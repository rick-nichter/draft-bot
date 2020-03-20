import requests, json, rareArchetypeAssignment
from bs4 import BeautifulSoup

# This file adds archetype rankings to common/uncommon cards in the list

with open("standardCardList.json", encoding="utf8") as cardListFile:
		standardCards = json.load(cardListFile)

thbCards = {}

# Get only cards in THB from standard list and add a section for archetypes
for cardName in standardCards.keys():
	card = standardCards[cardName]
	if "THB" in card["printings"]:
		card["archetypes"] = {
			"BG": 0.0,
			"BU": 0.0,
			"RW": 0.0,
			"RB": 0.0,
			"RU": 0.0,
			"UW": 0.0,
			"RG": 0.0,
			"BW": 0.0,
			"UG": 0.0,
			"GW": 0.0
		}
		thbCards[cardName] = card

# Gets a table of archetype rankings from draftsim.com/theros-beyond-death-early-analysis/

wTableLocation = "https://draftsim.com/wp-admin/admin-ajax.php?" + \
	"action=wp_ajax_ninja_tables_public_action&table_id=2128&" + \
	"target_action=get-all-data&default_sorting=old_first"
uTableLocation = "https://draftsim.com/wp-admin/admin-ajax.php?" + \
	"action=wp_ajax_ninja_tables_public_action&table_id=2130&" + \
	"target_action=get-all-data&default_sorting=old_first"
bTableLocation = "https://draftsim.com/wp-admin/admin-ajax.php?" + \
	"action=wp_ajax_ninja_tables_public_action&table_id=2124&" + \
	"target_action=get-all-data&default_sorting=old_first"
rTableLocation = "https://draftsim.com/wp-admin/admin-ajax.php?" + \
	"action=wp_ajax_ninja_tables_public_action&table_id=2131&" + \
	"target_action=get-all-data&default_sorting=old_first"

wTable = requests.get(wTableLocation).json()
uTable = requests.get(uTableLocation).json()
bTable = requests.get(bTableLocation).json()
rTable = requests.get(rTableLocation).json()

# Make sure all archetype ratings get saved
for row in wTable:
	# Get each rank for all 4 white archetypes
	contents = row["value"]
	rank = contents["rank"]
	# Rating is going to be low to high; the higher the better (opposite of rank)
	rating = 187.0 - float(rank)

	wr = BeautifulSoup(contents["wr"], "html.parser").get_text()
	wu = BeautifulSoup(contents["wu"], "html.parser").get_text()
	wb = BeautifulSoup(contents["wb"], "html.parser").get_text()
	wg = BeautifulSoup(contents["wg"], "html.parser").get_text()

	# Add the rating to the file
	thbCards[wr]["archetypes"]["RW"] = rating
	thbCards[wu]["archetypes"]["UW"] = rating
	thbCards[wb]["archetypes"]["BW"] = rating
	thbCards[wg]["archetypes"]["GW"] = rating

for row in uTable:
	# Get each rank for 3 unsaved blue archetypes
	contents = row["value"]
	rank = contents["rank"]
	# Rating is going to be low to high; the higher the better (opposite of rank)
	rating = 187.0 - float(rank)

	ub = BeautifulSoup(contents["ub"], "html.parser").get_text()
	ur = BeautifulSoup(contents["ur"], "html.parser").get_text()
	ug = BeautifulSoup(contents["ug"], "html.parser").get_text()

	# Add the rating to the file
	thbCards[ub]["archetypes"]["BU"] = rating
	thbCards[ur]["archetypes"]["RU"] = rating
	thbCards[ug]["archetypes"]["UG"] = rating

for row in bTable:
	# Get each rank for 2 unsaved black archetypes
	contents = row["value"]
	rank = contents["rank"]
	# Rating is going to be low to high; the higher the better (opposite of rank)
	rating = 187.0 - float(rank)

	bg = BeautifulSoup(contents["bg"], "html.parser").get_text()
	br = BeautifulSoup(contents["br"], "html.parser").get_text()

	# Add the rating to the file
	thbCards[bg]["archetypes"]["BG"] = rating
	thbCards[br]["archetypes"]["RB"] = rating

for row in rTable:
	# Get each rank for last archetype: red-green
	contents = row["value"]
	rank = contents["rank"]
	# Rating is going to be low to high; the higher the better (opposite of rank)
	rating = 187.0 - float(rank)

	rg = BeautifulSoup(contents["rg"], "html.parser").get_text()

	# Add the rating to the file
	thbCards[rg]["archetypes"]["RG"] = rating
	
# Update file
thbFile = open("thbCardList.json", "w")
json.dump(thbCards, thbFile)
thbFile.close()

# Get ratings for rare cards
rareArchetypeAssignment.assignRareRatings(thbCards)