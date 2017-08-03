from django.db.models import Max

from taskmanager.models import Day, Availability, WeeklySchedule, TaskTypeWeight


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


######################## Gia WEEKLYSCEDULE

def priority_reschedule(self, user, null=None):
        ws_list = WeeklySchedule.objects.all()
        for ws1 in ws_list:
            if ws1.canMove:
                for ws2 in ws_list:
                    if ws1.id != ws2.id & ws2.canMove & hasConflict(ws1, ws2):
                        if find_max_Weight(ws1.task, self.request.user) >= find_max_Weight(ws2.task, self.request.user):
                            ws1.valid = True
                            ws2.valid = False
                            return null             #Todo  Attentioin please....passengers without tickets  must cum to the counter, thank you ...
                        else:
                            ws1.valid = False
                            ws2.valid = True
                            return null
                        return null
        return null



def reposition(self, user):
        ws_list=WeeklySchedule.objects.filter(canMove=True, user=user).get()
        for ws in ws_list:
            if not ws.valid:
                av_list = Availability.objects.filter(task=ws.task, user= ws.user)
                broken=False
                for av in av_list:
                    for ws2 in ws_list:
                        if ws2.task != av.task:
                            if hasConflict(av,ws):
                                if find_max_priority(av.task, av.user) > find_max_priority(ws2.task, ws2.user):
                                        #create weeklyschedule
                                        broken = True
                                        break

                            else:
                                #create weeklyschedule
                                broken = True
                                break
                    if broken:
                        break
                    # return error










def find_max_Weight(task, user): ### DEn theloume to instanceId
	return TaskTypeWeight.objects.filter(taskType=task, user=user).aggregate(Max('weight'))

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
