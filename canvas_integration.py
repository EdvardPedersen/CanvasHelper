import canvasapi

def get_token(filename):
    with open(filename) as f:
        access_token = f.readline().strip()
    return access_token

class CanvasIntegration:
    def __init__(self, api_url, api_key, course):
        self.canvas = canvasapi.Canvas(api_url, api_key)
        self._set_course(course)
        self.users = {}
        self.sections = {}

    def _set_course(self, course_id):
        self.course_id = course_id
        self.course = self.canvas.get_course(course_id)

    def get_list_of_users(self):
        users = self.course.get_users()
        for u in users:
            self.users[u.id] = u
        return users

    def get_files(self):
        return [f for f in self.course.get_files(sort="created_at", order="desc")]

    def get_announcements(self):
        course_text = "course_{}".format(self.course_id)
        start = "2000-01-01"
        end = "2100-01-01"
        ann = self.canvas.get_announcements(context_codes=[course_text],
                                            start_date=start,
                                            end_date=end)
        return [f for f in ann]

    def get_section_overview(self):
        if len(self.users) == 0:
            self.get_list_of_users()
        sections = self.course.get_sections()
        for section in sections:
            if section.sis_section_id not in self.sections:
                self.sections[section.sis_section_id] = []
            enrollments = section.get_enrollments()
            for enrollment in enrollments:
                if enrollment.user_id not in self.users:
                    print(f"Student enrolled, but not in course: {enrollment.user_id}")
                else:
                    self.sections[section.sis_section_id].append(enrollment.user_id)
        return self.sections



if __name__ == "__main__":
    c = CanvasIntegration("https://uit.instructure.com", get_token("canvas-token"), "18522")
    users = c.get_list_of_users()
    sections = c.get_section_overview()

    for section in sections:
        print(section)
