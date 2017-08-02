from taskmanager.models import Day


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
            firstHalfTaken = (ws.startingTime <= critical.startingTime) & (critical.startingTime < ws.endingTime)   # [(])

        return secondHalfTaken | firstHalfTaken  # wholeTaken |  | partlyTaken




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