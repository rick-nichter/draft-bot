import math

# gets the cards in the draft and the current picks from the Cardsphere HTTP request response
def createDraftEnvironment(info, picksInfo):
	# a dict of draftID -> card name
	draftCards = {}
	# a dict of packID -> cardList (all cards in the pack)
	draftPacks = {}
	# a list of cards the primary player has already drafted
	draftPickIds = []

	# first we need to get cardSphere's ids for cards
	idToName = {}
	for cardId in info["info"].keys():
		idToName[cardId] = info["info"][cardId]["n"]

	seats = info["seats"]
	# each draft has a number of seats (usually 8), so we need to get packs from every seat
	for seat in seats:
		packs = seat["packs"]
		# each seat has a number (usually 3) packs, so we need to get cards from each pack
		for pack in packs:
			# save this pack and all its cards
			draftPacks[pack["id"]] = []
			cards = pack["cards"]
			# each pack has a number (usually 15) of cards, and we need to save each card
			for card in cards:
				# save the cards in a dict that connects card ID to cardname
				draftCards[card["id"]] = idToName[str(card["m"])]
				# add this card id to this pack
				draftPacks[pack["id"]].append(card["id"])

	# based on the current picks, filter the cards available in packs
	players = picksInfo["picks"]
	isFirstPlayer = True

	# for each player in picks, need to remove those cards from packs
	for playerPicks in players:

		# remove each card picked from its pack
		for pick in playerPicks:
			# add cards to draftpickids if this is the primary player
			if isFirstPlayer:
				draftPickIds.append(pick["id"])

			# slice the card id to get its pack id
			packId = pick["id"][0:3]
			# remove this card from the pack
			draftPacks[packId].remove(pick["id"])

		if isFirstPlayer:
			isFirstPlayer = False

	# the ids of the card in the current pack the player is picking from
	currentPackIds = draftPacks[calculateCurrentPack(len(draftPickIds))]

	# translate pack ids to card names so draft bot can read them
	currentPack = []
	for i in currentPackIds:
		currentPack.append(draftCards[i])

	# do the same for previously picked cards
	draftPicks = []
	for i in draftPickIds:
		draftPicks.append(draftCards[i])

	return draftPacks, draftCards, draftPicks, currentPack

# calculates the pack the primary player is picking from based on the number of picks
def calculateCurrentPack(numberOfPicks):
	# which round of packs is open (0, 1, or 2)
	packRound = math.floor(numberOfPicks / 15)
	# since theyre are typically 8 packs, this is the pack number
	packNumber = (numberOfPicks - (packRound * 15)) % 8
	# in the second round, switch the direction of the packs
	if packRound == 1:
		packNumber = (8 - packNumber) % 8
	packId = str(packNumber) + ":" + str(packRound)

	return packId

