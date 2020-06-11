import canvasapi

def get_token(filename):
    with open(filename) as f:
        access_token = f.readline().strip()
    return access_token

class CanvasIntegration:
    def __init__(self, api_url, api_key, course):
        self.canvas = canvasapi.Canvas(api_url, api_key)
        self._set_course(course)

    def _set_course(self, course_id):
        self.course_id = course_id
        self.course = self.canvas.get_course(course_id)

    def get_list_of_users(self):
        return self.course.get_users()

    def get_files(self):
        return [f for f in self.course.get_files(sort="created_at", order="desc")]

    def get_announcements(self):
        course_text = "course_{}".format(self.course_id)
        start = "2000-01-01"
        end = "2100-01-01"
        ann = self.canvas.get_announcements(context_codes=course_text,
                                            start_date=start,
                                            end_date=end)
        return [f for f in ann]



if __name__ == "__main__":
    c = CanvasIntegration("https://uit.instructure.com", get_token("canvas-token"), "16497")
    users = c.get_list_of_users()
    ann = c.get_announcements()
    print(ann)
    for u in ann:
        print(u.attributes)
