import canvasapi

def get_token(filename):
    with open(filename) as f:
        access_token = f.readline().strip()
    return access_token

class CanvasIntegration:
    def __init__(self, api_url, api_key):
        self.canvas = canvasapi.Canvas(api_url, api_key)

    def set_course(self, course_id):
        self.course = self.canvas.get_course(course_id)

    def get_list_of_users(self):
        return self.course.get_users()



if __name__ == "__main__":
    c = CanvasIntegration("https://uit.instructure.com", get_token("access-token"))
    c.set_course("16497")
    users = c.get_list_of_users()
    for u in users:
        print(u)
