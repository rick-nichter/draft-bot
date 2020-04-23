import json, sys, requests
import environmentBuilder as env

idealDistribution = [2, 7, 6, 4, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0]
totalCardsNeeded = sum(idealDistribution)
# a dict of all cards in standard with details about each card
# CardName -> CardObject
with open("jsonFiles/thbCardList.json", encoding="utf8") as cardListFile:
		thbCards = json.load(cardListFile)

def main(picksId, draftFile, pickNum, pickThreshold):
	picksLocation = "https://draft.cardsphere.com/rest/v1/draft/*/instance/" + picksId
	picksResponse = requests.get(picksLocation).json()

	infoId = picksResponse["draftId"]
	infoLocation = "https://draft.cardsphere.com/rest/v1/draft/" + infoId
	infoResponse = requests.get(infoLocation).json()

	draftPacks, draftCards, draftPicks, currentPack = \
		env.createDraftEnvironment(infoResponse, picksResponse)

	draftFile.write("PICK " + str(pickNum) + "\n\n")
	return draftCard(currentPack, draftFile, pickThreshold, draftPicks)

# select a card to draft from the given set, based on the cards already picked
def draftCard(pack, draftFile, pickThreshold, previousPicks = []):
	global thbCards
	
	draftFile.write("Options: \n")
	draftFile.write(str(pack)[1:-1] + "\n")
	draftFile.write("\nPreviously picked: \n")
	draftFile.write(str(previousPicks)[1:-1] + "\n")

	# create a detailed dict of previous picks (not just their names)
	detailedPreviousPicks = {}
	for pick in previousPicks:
		detailedPreviousPicks[pick] = thbCards[pick]

	# select best card out of pack based on a number of factors

	highestUtility = -1000000.0
	highestArchetypeUtility = -1000000.0
	# this is the highest card rating in general
	pick = ""
	# this is the highest card rating for current archetype
	archetypePick = ""

	mostPresentArchetype, rating = calculateMostPresentArchetype(detailedPreviousPicks)
	topRating = calculateAverageDeckRating(detailedPreviousPicks, mostPresentArchetype)

	for cardName in pack:
		cardDetails = thbCards[cardName]
		cardUtility = calculateArchetypeUtility(cardDetails)
		cardArchetypeUtility = calculateArchetypeUtility(cardDetails, mostPresentArchetype)
		if cardUtility > highestUtility:
			highestUtility = cardUtility
			pick = cardName
		if cardArchetypeUtility > highestArchetypeUtility:
			highestArchetypeUtility = cardArchetypeUtility
			archetypePick = cardName

	# if a card is very good, but outside of the archetype, see if we should pick it	
	if cardUtility > cardArchetypeUtility + pickThreshold:
		archetypePick = pick

	draftFile.write("\nBest rating before pick: " + mostPresentArchetype \
		 + " " + str(rating))
	draftFile.write("\nTop cards rating before pick: " + str(topRating))

	draftFile.write("\nDraftBot picked: ")
	draftFile.write(pick + "\n\n")

	return archetypePick, topRating


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
def calculateArchetypeUtility(card, archetype=""):
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

	return bestArchetype, maxRating

# Calculate the average rating of the top 23 cards given
def calculateAverageDeckRating(cards, bestArchetype):
	bestCardRatings = []
	for card in cards.values():
		if len(bestCardRatings) < 23:
			bestCardRatings.append(card["archetypes"][bestArchetype])
		elif bestCardRatings[22] < card["archetypes"][bestArchetype]:
			bestCardRatings.pop()
			bestCardRatings.append(card["archetypes"][bestArchetype])

		bestCardRatings.sort(reverse=True)

	total = sum(bestCardRatings)
	averageRating = 0.0
	if len(bestCardRatings) != 0:
		averageRating = total / len(bestCardRatings)

	return averageRating


# send the first argument, which should be url to a draft simulation
# main(sys.argv[1])
