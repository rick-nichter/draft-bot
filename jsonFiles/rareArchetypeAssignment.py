import json

with open("jsonFiles/thbCardList.json", encoding="utf8") as cardListFile:
		thbCards = json.load(cardListFile)

rareList = ["Heliod, Sun-Crowned", "Erebos, Bleak-Hearted", "Elspeth, Sun's Nemesis", \
	"Nightmare Shepherd", "Kiora Bests the Sea God", "Polukranos, Unchained", "Shadowspear", \
	"Purphoros, Bronze-Blooded", "Archon of Sun's Grace", "Nadir Kraken", \
	"Uro, Titan of Nature's Wrath", "Ashiok, Nightmare Muse", "Thassa, Deep-Dwelling", \
	"Thryx, the Sudden Storm", "Nylea, Keen-Eyed", "Setessan Champion", "Dream Trawler", \
	"Kroxa, Titan of Death's Hunger", "Taranika, Akroan Veteran", "Mantle of the Wolf", \
	"Woe Strider", "Klothys, God of Destiny", \
	"Erebos's Intervention", "Eat to Extinction", "Ox of Agonas", "The First Iroan Games", \
	"Arasta of the Endless Web", "Phoenix of Ash", "Dryad of the Ilysian Grove", \
	"Elspeth Conquers Death", "Gravebreaker Lamia", "Aphemia, the Cacophony", \
	"Tectonic Giant", "Storm's Wrath", "Shatter the Sky", "Calix, Destiny's Hand", \
	"Kunoros, Hound of Athreos", "The Akroan War", "Nessian Boar", "Purphoros's Intervention"]