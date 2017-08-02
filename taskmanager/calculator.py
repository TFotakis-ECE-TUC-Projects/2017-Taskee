from taskmanager.models import Day


def hasConflict(critical, ws):
	criticalIsTransitive = critical.endingTime < critical.startingTime
	critical_end_day = Day.objects.get(id=(ws.day.id - (not criticalIsTransitive) % 7) + 1)
	wsIsTransitive = ws.endingTime < ws.startingTime
	ws_end_day = Day.objects.get(id=(ws.day.id - (not wsIsTransitive) % 7) + 1)

	sameDay = ws.day == critical.day
	almost_sameDay1 = critical_end_day == ws.day
	almost_sameDay2 = ws_end_day == critical.day
	# Todo: den vgazei noima????????
	check_days = sameDay | almost_sameDay1 | almost_sameDay2
	if criticalIsTransitive & wsIsTransitive:
		return True

	if criticalIsTransitive & (not ((critical.startingTime >= ws.endingTime) & (critical.endingTime <= ws.startingTime))):
		secondHalfTaken = (critical.startingTime < ws.endingTime) | (critical.endingTime > ws.startingTime)  # & (critical.endingTime <= ws.startingTime)
	else:
		secondHalfTaken = (critical.startingTime <= ws.startingTime) & (critical.endingTime > ws.startingTime) & (critical.endingTime <= ws.startingTime)  # ([)]

	if wsIsTransitive & (not ((critical.startingTime >= ws.endingTime) & (critical.endingTime <= ws.startingTime))):
		firstHalfTaken = (critical.startingTime < ws.endingTime) | (critical.endingTime > ws.startingTime)  # & (ws.endingTime <= critical.endingTime)
	else:
		firstHalfTaken = (ws.startingTime <= critical.startingTime) & (critical.startingTime < ws.endingTime) & (ws.endingTime <= critical.endingTime)  # [(])

	if check_days & (secondHalfTaken | firstHalfTaken):  # wholeTaken |  | partlyTaken
		return True
	return False
