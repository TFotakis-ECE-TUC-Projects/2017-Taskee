from django.db.models import Max

from taskmanager.models import Day, Availability, WeeklySchedule


def hasConflict(critical, ws):
	criticalIsTransitive = critical.endingTime < critical.startingTime
	critical_end_day = Day.objects.get(id=(ws.day.id - (not criticalIsTransitive) % 7) + 1)
	wsIsTransitive = ws.endingTime < ws.startingTime
	ws_end_day = Day.objects.get(id=(ws.day.id - (not wsIsTransitive) % 7) + 1)

	sameDay = ws.day == critical.day
	almost_sameDay1 = critical_end_day == ws.day
	almost_sameDay2 = ws_end_day == critical.day

	check_days = sameDay | almost_sameDay1 | almost_sameDay2
	if check_days:
		if criticalIsTransitive & wsIsTransitive:
			return True

		if criticalIsTransitive & (not ((critical.startingTime >= ws.endingTime) & (critical.endingTime <= ws.startingTime))):
			secondHalfTaken = (critical.startingTime < ws.endingTime) | (critical.endingTime > ws.startingTime)  # & (critical.endingTime <= ws.startingTime)
		else:
			secondHalfTaken = (critical.startingTime <= ws.startingTime) & (critical.endingTime > ws.startingTime)  # ([)]

		if wsIsTransitive & (not ((critical.startingTime >= ws.endingTime) & (critical.endingTime <= ws.startingTime))):
			firstHalfTaken = (critical.startingTime < ws.endingTime) | (critical.endingTime > ws.startingTime)  # & (ws.endingTime <= critical.endingTime)
		else:
			firstHalfTaken = (ws.startingTime <= critical.startingTime) & (critical.startingTime < ws.endingTime)  # [(])

		return secondHalfTaken | firstHalfTaken  # wholeTaken |  | partlyTaken


def reposition(self):
	ws_list = WeeklySchedule.objects.all()
	av_list = Availability.objects.all()

	######################## Gia WEEKLYSCEDULE                                                                                                  #D
	for ws1 in ws_list:  # O
		if ws1.canMove:  # N
			for ws2 in ws_list:  # T
				if ws1.id != ws2.id & ws2.canMove & hasConflict(ws1, ws2):
					if find_max_priority(ws1.task, self.request.user, ws1.instanceId) >= find_max_priority(ws2.task, self.request.user, ws2.instanceId):
						ws1.valid = True
						ws2.valid = False
					else:
						ws1.valid = False
						ws2.valid = True

	######################### Gia Availability###
	for ws in ws_list:
		pass


def find_max_priority(task, user, instanceId):
	return Availability.objects.filter(task=task, user=user, instanceId=instanceId).aggregate(Max('priority'))

# av_list = Availability.objects.filter(task=task, user=user, instanceId=instanceId).get()
# maximum=-1000000
# for av1 in av_list:
#     if av1.task==task & av1.priority > maximum:
#         maximum=av1.priority
# return maximum


# Logic
# for ws
#     if canMove & not valid
#         for av
#             if canMove
#                 check conflict (av= critical, ws=ws)
#                 check priority
#                 put valid
#                 an egine antikatastasi tote : rasie flag continue
#



# Logic
# for στο weeklylist (ws1)
# if canMove
# for weeklylist (ws2)
# if not self
# if canMove
# if τα παραπάνω έχουν confilctr (ws1,ws2) & 1 of them is valid
# find max priority->change to valid
# το αλλο παιρνει πούλο






# if ws.endingTime < ws.startingTime:  # exoume transicion hmeras (Monday -> Tuesday)
#     ws_end_day = Day.objects.get(id=ws.day_id + 1)
#     transicion2 = True
# else:
#     transicion2 = False
#     ws_end_day = ws.day
# sameDay = ws.day == critical_day
# almost_sameDay1 = critical_end_day == ws.day
# almost_sameDay2 = ws_end_day == critical_day
#
# check_days = sameDay | almost_sameDay1 | almost_sameDay2
#
# if transicion1 & transicion2:
#     if critical.canMove == True:
#         critical.save()
#         return redirect('taskmanager:weeklyScheduleView')
#     else:
#         return render(request=request, template_name='taskmanager/weeklyschedule_form.html',
#                       context={'errorMessage': 'The schedule you are trying to create conflicts with: ' + str(ws)})
# if transicion1 & (
# not ((critical_startime >= ws.endingTime) & (critical_endingtime <= ws.startingTime))):
#     secondHalfTaken = (critical_startime < ws.endingTime) | (
#         critical_endingtime > ws.startingTime)  # & (critical_endingtime <= ws.startingTime)
# else:
#     secondHalfTaken = (critical_startime <= ws.startingTime) & (critical_endingtime > ws.startingTime) & (critical_endingtime <= ws.startingTime)  # ([)]
#
# if transicion2 & (not ((critical_startime >= ws.endingTime) & (critical_endingtime <= ws.startingTime))):
#     firstHalfTaken = (critical_startime < ws.endingTime) | (critical_endingtime > ws.startingTime)  # & (ws.endingTime <= critical_endingtime)
# else:
#     firstHalfTaken = (ws.startingTime <= critical_startime) & (critical_startime < ws.endingTime) & (ws.endingTime <= critical_endingtime)  # [(])
#
# if check_days & (secondHalfTaken | firstHalfTaken):  # wholeTaken |  | partlyTaken
