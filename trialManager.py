import draftAutomator, sys, multiprocessing

# how many trials per automator
trials = int(sys.argv[1])
instances = int(sys.argv[2])
minThreshold = int(sys.argv[3])
interval = int(sys.argv[4])

started = 0
currentThreshold = minThreshold

if __name__ == "__main__":
	while started < instances:		
		p = multiprocessing.Process(target=draftAutomator.automate, \
			args=(trials, currentThreshold, started,))
		p.start()
		currentThreshold += interval
		started += 1