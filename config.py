import localization

LANG = localization.LOCALE_NO

# File that contains the Discord token
DISCORD_TOKEN_FILE="discord-token"


# File that contains the Canvas token
CANVAS_TOKEN_FILE="canvas-token"

# Update interval in seconds (int)
CANVAS_UPDATE_INTERVAL=60
CALENDAR_UPDATE_INTERVAL=60

CANVAS_URL="https://uit.instructure.com"

# Relation between discord channels and courses
# Each channel can have multiple courses
CHANNEL_COURSES={
        781144324263116824: ["21176"],
        804666124121538591: ["21176"]
        }

# Names for courses as used in timeplan.uit.no
COURSE_NAMES = {
        "21176": "INF-1400-1"
        }

COURSE_SEMESTER_PLAN = {
        "21176": "https://raw.githubusercontent.com/uit-inf-1400-2021/uit-inf-1400-2021.github.io/main/semesterplan.md"
        }
