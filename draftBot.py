import json, sys, requests
import environmentBuilder as env

idealDistribution = [3, 12, 10, 6, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0]
totalCardsNeeded = sum(idealDistribution)
# a dict of all cards in standard with details about each card
# CardName -> CardObject
with open("jsonFiles/thbCardList.json", encoding="utf8") as cardListFile:
		thbCards = json.load(cardListFile)

def main(infoId, picksId):
	infoLocation = "https://draft.cardsphere.com/rest/v1/draft/" + infoId
	picksLocation = "https://draft.cardsphere.com/rest/v1/draft/*/instance/" + picksId
	infoResponse = requests.get(infoLocation)
	picksResponse = requests.get(picksLocation)
	draftPacks, draftCards, draftPicks, currentPack = \
		env.createDraftEnvironment(infoResponse.json(), picksResponse.json())
	draftCard(currentPack, draftPicks)

# select a card to draft from the given set, based on the cards already picked
def draftCard(pack, previousPicks = []):
	global thbCards

	# TODO: write draft data to a file
	#draftFile = open("jsonFiles/draft.json")
	print("Options: ")
	print(pack)
	print("Previously picked: ")
	print(previousPicks)

	# create a detailed dict of previous picks (not just their names)
	detailedPreviousPicks = {}
	for pick in previousPicks:
		detailedPreviousPicks[pick] = thbCards[pick]

	# select best card out of pack based on a number of factors
	highestUtility = -1000000.0
	pick = ""
	mostPresentArchetype = calculateMostPresentArchetype(detailedPreviousPicks)
	for cardName in pack:
		cardDetails = thbCards[cardName]
		cardUtility = calculateArchetypeUtility(cardDetails, mostPresentArchetype)
		if cardUtility > highestUtility:
			highestUtility = cardUtility
			pick = cardName

	print("DraftBot recommends picking: ")
	print(pick)


# calculates the individual utility of a creature card 
def calculateCreatureUtility(card):
	toughness = card.get("toughness", 0.0)
	power = card.get("power", 0.0)
	if toughness == "*":
		toughness = 0.0
	if power == "*":
		power = 0.0
	toughness = float(toughness)
	power = float(power)
	cmc = card.get("convertedManaCost", 0.0)

	return ((toughness + power) / 2) - cmc

# calculates the individual utility of an instant/sorcery card
def calculateSpellUtility(card):
	# util function for spells
	print("hi")

# calculate the utility of the current curve
def calculateCurveUtility(distribution):
	global idealDistribution
	util = 0.0
	# util function for curve
	for i in range(len(distribution)):
		diff = abs(distribution[i] - idealDistribution[i])
		util -= diff

	return util

# calculate the total utility of the given deck
def calculateDeckUtility(deck):
	print("nothing yet")

# used to sort by mana curve
def cmc(card):
	return card["cmc"]

# Calcualte the archetype utility of the given card
def calculateArchetypeUtility(card, archetype):
	# if there is no strongest archetype, just return this cards highest utility
	if archetype == "":
		maxRating = 0.0
		for a in card["archetypes"].keys():
			if card["archetypes"][a] > maxRating:
				maxRating = card["archetypes"][a]

		return maxRating
	else:
		return card["archetypes"][archetype]

# Calculate the most present archetype based on previous picks
def calculateMostPresentArchetype(previousPicks):
	averageArchetypeRatings = {}
	firstPick = True
	for card in previousPicks.values():
		if firstPick:
			averageArchetypeRatings = card["archetypes"]
			firstPick = False
		else:
			for a in card["archetypes"].keys():
				averageArchetypeRatings[a] += card["archetypes"][a]

	bestArchetype = ""
	maxRating = 0.0
	for a in averageArchetypeRatings.keys():
		totalRating = averageArchetypeRatings[a]
		averageArchetypeRatings[a] = totalRating / len(previousPicks)
		
		if averageArchetypeRatings[a] > maxRating:
			bestArchetype = a
			maxRating = averageArchetypeRatings[a]

	print(averageArchetypeRatings)
	print(bestArchetype)

	return bestArchetype


# send the first and second argument, which should be urls to a draft simulation
main(sys.argv[1], sys.argv[2])
