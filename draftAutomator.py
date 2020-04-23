import time, draftBot, sys, datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def findCardElement(pageId, draftFile, pickNum, pickThreshold, driver):
	try:
		pick, topRating = draftBot.main(pageId, draftFile, pickNum, pickThreshold)
		pickClick = WebDriverWait(driver, 2).until(EC.presence_of_element_located(("xpath", \
			"//div[text() = \"" + pick + "\"]")))

		return pickClick, topRating
	except Exception as e:
		print(e)
		return findCardElement(pageId, draftFile, pickNum, pickThreshold, driver)


def automate(trials, pickThreshold, fileNum):
	#trials = int(sys.argv[1])
	#pickThreshold = int(sys.argv[2])

	completed = 0
	driver = webdriver.Chrome()
	draftFile = open("logs/draftLog" + str(fileNum) + ".txt", "w")
	startTime = datetime.datetime.now()
	topRatings = []

	while completed < trials:
		# First select the right draft type from the select element
		driver.get("https://draft.cardsphere.com/")
		select = Select(driver.find_element_by_id("__BVID__19"))
		select.select_by_value("THB-THB-THB")

		# Now load the draft
		driver.find_element_by_tag_name("button").click()
		WebDriverWait(driver, 10).until(EC.presence_of_element_located(("class name", "pick-view")))
		pageId = driver.current_url[31:67]
		draftFile.write("\n\nNEW DRAFT\n\n")
		pickNum = 1
		topRating = 0.0

		# Loop through until draft is finished
		while len(driver.find_elements_by_xpath("//h3[text() = 'Draft finished']")) < 1:
			pickClick, topRating = findCardElement(pageId, draftFile, pickNum, pickThreshold, \
				driver)
			# pickClick = driver.find_element_by_xpath("//div[text() = \"" + pick + "\"]")
			driver.execute_script("arguments[0].click();", pickClick)
			driver.execute_script("arguments[0].click();", pickClick)
			pickNum += 1

		topRatings.append(topRating)
		completed += 1

	endTime = datetime.datetime.now()
	draftFile.write("\n" + str(trials) + " drafts completed")
	draftFile.write("\nMax rating: " + str(max(topRatings)))
	draftFile.write("\nMin rating: " + str(min(topRatings)))
	draftFile.write("\nAverage rating: " + str(sum(topRatings) / len(topRatings)))
	draftFile.write("\nSim start: " + str(startTime) + "\nSim end: " + str(endTime))

	draftFile.close()
	driver.close()