import requests, json
from bs4 import BeautifulSoup

# This file adds archetype rankings to rare cards in the list 
# (since they are not ranked in archetype like commons and uncommons)

def assignRareRatings(thbCards):
	pickTableLocation = "https://draftsim.com/wp-admin/admin-ajax.php?" + \
		"action=wp_ajax_ninja_tables_public_action&table_id=2101&target_action" + \
		"=get-all-data&default_sorting=old_first"

	pickTable = requests.get(pickTableLocation).json()

	# Loop through pick order, saving rare values based on rank
	for row in pickTable:
		# Get the rank of this item
		contents = row["value"]
		rank = contents["rank"]
		# Rating is going to be low to high; the higher the better (opposite of rank)
		rating = 253.5 - float(rank)

		# Get the cardname
		cardName = BeautifulSoup(contents["cardname"], "html.parser").get_text()

		# For each archetype that this card fits, save its rating in our THB cards file
		cardData = thbCards[cardName]
		multipleColors = ""
		# For each color this card is, add its rating to that archetype
		if len(cardData["colors"]) == 1:
			for a in cardData["archetypes"].keys():
				if cardData["colors"][0] in a:
					# Only update for cards that do not have a rating yet
					if cardData["archetypes"][a] == 0.0:
						thbCards[cardName]["archetypes"][a] = rating
		elif len(cardData["colors"]) == 2:
			# If the card is multiple colors, it only fits in one archetype		
			for a in cardData["archetypes"].keys():
				if cardData["colors"][0] in a and cardData["colors"][1] in a:
					# Only update for cards that do not have a rating yet
					if cardData["archetypes"][a] == 0.0:
						thbCards[cardName]["archetypes"][a] = rating


	# Update file
	thbFile = open("thbCardList.json", "w")
	json.dump(thbCards, thbFile)