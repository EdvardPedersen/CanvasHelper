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
        742657261347799103: ["18522"]
        610855182539948052: ["18522"]
        }

# Names for courses as used in timeplan.uit.no
COURSE_NAMES = {
        "18522": "INF-1049-1"
        }
