import urllib.request
from datetime import date, datetime, timezone
import ics

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
        #time_now = datetime.now(tz=timezone.utc)
        time_now = datetime.fromisoformat('2020-01-15 12:00:00.000+00:00')
        for event in self.calendar.events:
            delta_time = event.begin - time_now
            if delta_time.total_seconds() < seconds:
                print(delta_time)
                print(event)

    def delta_to_seconds(self,delta):
        return delta.total_seconds()



if __name__ == "__main__":
    c = CourseCalendar("INF-1400-1")
    c.get_upcoming_events(20)
