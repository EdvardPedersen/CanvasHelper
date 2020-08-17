import urllib.request
from datetime import date, datetime, timezone
import ics
import config

class CourseCalendar():
    def __init__(self, course_name):
        self.course_name = course_name
        self.update_calendar()

    def update_calendar(self):
        today = date.today()
        year = str(today.year)[2:]
        semester = "v"
        if today.month > 6:
            semester = "h"
        url = "http://timeplan.uit.no/calendar.ics?sem={}{}&module[]={}".format(year, semester, self.course_name)
        calendar_text = urllib.request.urlopen(url).read()
        self.calendar = ics.Calendar(calendar_text.decode("utf-8"))

    def get_upcoming_events(self, hours_ahead):
        seconds = hours_ahead * 3600
        time_now = datetime.now(tz=timezone.utc)
        for event in self.calendar.events:
            delta_time = event.begin - time_now
            if delta_time.total_seconds() < seconds:
                print(delta_time)
                print(event)

    def delta_to_seconds(self,delta):
        return delta.total_seconds()

    def get_weekly_calendar(self, restrict=None):
        now = datetime.now()
        week = now.strftime("%W")
        if now.weekday() > 4:
            week = str(int(week) + 1)

        events_for_cal = []
        for event in self.calendar.events:
            eventweek = event.begin.strftime("%W")
            if eventweek == week:
                events_for_cal.append(event)

        events_for_cal.sort(key = lambda x: x.begin)
        output = config.LANG["calendartext"].format(week, self.course_name)
        output += config.LANG["calendarheader"]
        weekdays = config.LANG["weekdays"]
        for event in events_for_cal:
            temp_output = "{} | {} | {} - {} \n".format(weekdays[event.begin.weekday()], event.begin.strftime("%H:%M"), event.description, event.location)
            if not restrict:
                output += temp_output
            elif restrict == "lecture":
                if "Forelesning" in event.description:
                    output += temp_output
            elif restrict == "group":
                if not "Forelesning" in event.description:
                    output += temp_output
        output += "```"
        return output.replace("&nbsp;Opptak", "(Opptak)")


if __name__ == "__main__":
    c = CourseCalendar("INF-1049-1")
    c.get_upcoming_events(20)
    print(c.get_weekly_calendar())
