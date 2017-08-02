from taskmanager.models import Day


def Conflict_check(critical_startime,critical_endingtime,critical_day,critical_end_day,ws_endingTime,ws_startingTime,ws_day):
    transicion1=False
    if critical_endingtime < critical_startime:  # exoume transicion hmeras (Monday -> Tuesday)
        critical_end_day = Day.objects.get(id=critical_day + 1)
        transicion1 = True
    else:
        critical_end_day = critical_day
    if ws_endingTime < ws_startingTime:  # exoume transicion hmeras (Monday -> Tuesday)
        ws_end_day = Day.objects.get(id=ws_day.id + 1)
        transicion2 = True
    else:
        transicion2 = False
        ws_end_day = ws_day
    sameDay = ws_day == critical_day
    almost_sameDay1 = critical_end_day == ws_day
    almost_sameDay2 = ws_end_day == critical_day

    check_days = sameDay  | almost_sameDay1 | almost_sameDay2
    #
    if transicion1 & transicion2:
        return True

    if transicion1 & (
            not ((critical_startime >= ws_endingTime) & (critical_endingtime <= ws_startingTime))):
        secondHalfTaken = (critical_startime < ws_endingTime) | (
            critical_endingtime > ws_startingTime)  # & (critical_endingtime <= ws_startingTime)
    else:
        secondHalfTaken = (critical_startime <= ws_startingTime) & (critical_endingtime > ws_startingTime) & (critical_endingtime <= ws_startingTime)  # ([)]

    if transicion2 & (not ((critical_startime >= ws_endingTime) & (critical_endingtime <= ws_startingTime))):
        firstHalfTaken = (critical_startime < ws_endingTime) | (critical_endingtime > ws_startingTime)  # & (ws_endingTime <= critical_endingtime)
    else:
        firstHalfTaken = (ws_startingTime <= critical_startime) & (critical_startime < ws_endingTime) & (ws_endingTime <= critical_endingtime)  # [(])

    if check_days & (secondHalfTaken | firstHalfTaken):  # wholeTaken |  | partlyTaken
        return True

    return False