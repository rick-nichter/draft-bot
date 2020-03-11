import json, sys, requests


idealDistribution = [3, 12, 10, 6, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0]

totalCardsNeeded = sum(idealDistribution)

def main(argv):
	with open("jsonFiles/" + argv, encoding="utf8") as cardListFile:
		cards = json.load(cardListFile)
		build(cards)

# build a deck using the given set of cards
def build(cardSet):
	global totalCardsNeeded

	# write the cards selected to a json file called deck
	deckFile = open("jsonFiles/deck.json", "w")
	
	deckList = []
	manaDistribution = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	for cardName in cardSet:
		card = cardSet[cardName]

		# the card data to be saved in the output deck
		newDeckCard = {
			"name": cardName,
			"cmc": card.get("convertedManaCost", 0.0),
			"power": card.get("power", 0.0),
			"toughness": card.get("toughness", 0.0),
			"utility": calculateCreatureUtility(card)
		}

		# just add cards until limit is reached
		if totalCardsNeeded > 0:
			deckList.append(newDeckCard)
			manaDistribution[int(newDeckCard["cmc"]) - 1] += 1
			totalCardsNeeded -= 1
		else:
			for deckCard in deckList:
				# the difference in individual utility
				utilDiff = newDeckCard.get("utility", 0.0) - deckCard.get("utility", 0.0)

				# see if replacing this card with the new one would better distribute cmc's
				distributionCopy = manaDistribution.copy()
				distributionCopy[int(deckCard["cmc"]) - 1] -= 1
				distributionCopy[int(newDeckCard["cmc"]) - 1] += 1
				distributionUtilDiff = calculateCurveUtility(distributionCopy) - \
				  calculateCurveUtility(manaDistribution)
				
				# if the total utility gained would be greater than zero, replace
				if distributionUtilDiff + utilDiff > 0:
					deckList.remove(deckCard)
					deckList.append(newDeckCard)
					manaDistribution = distributionCopy.copy()

					break;

	deckList.sort(key=cmc)
	json.dump(deckList, deckFile)
	

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


# send the first argument, which should be a json file name
main(sys.argv[1])
