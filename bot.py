import asyncio

import discord
import html2text

import canvas_integration
import config

class CanvasClient(discord.Client):
    def __init__(self):
        super().__init__()
        print("Init")
        self.loop.create_task(self.check_canvas())
        self.converter = html2text.HTML2Text()
        self.files = {}
        self.announcements = {}
        self.channels = config.CHANNEL_COURSES
        self.courses = {}
        for channel in self.channels:
            for course in self.channels[channel]:
                if course not in self.courses:
                    self.courses[course] = []
                self.courses[course].append(channel)


    async def on_ready(self):
        print("Connected to {}".format(client.guilds))

    async def check_canvas(self):
        await self.wait_until_ready()
        channels = [self.get_channel(c) for c in self.channels]

        token = canvas_integration.get_token(config.CANVAS_TOKEN_FILE)
        courses = []
        for c in self.courses:
            course = canvas_integration.CanvasIntegration(config.CANVAS_URL,
                                                          token,
                                                          c)
            courses.append(course)
        while not self.is_closed():
            await self.check_files(courses, channels)
            await self.check_announcements(courses, channels)
            await asyncio.sleep(config.CANVAS_UPDATE_INTERVAL)

    async def check_files(self, courses, channels):
        for course in courses:
            new_files = course.get_files()
            if course.course_id not in self.files:
                self.files[course.course_id] = new_files
                return
            last_files = self.files[course.course_id]
            if len(new_files) != len(last_files):
                for i in range(len(new_files) - len(last_files)):
                    f = new_files[i]
                    name = f.attributes["display_name"]
                    url = f.attributes["url"]
                    access_restrictions = [f.attributes["locked"],
                                           f.attributes["hidden"],
                                           f.attributes["locked_for_user"],
                                           f.attributes["hidden_for_user"]]
                    if not any(access_restrictions):
                        for channel in channels:
                            if course.course_id in self.channels[channel.id]:
                                await channel.send("***Ny fil lastet opp:\n{}***\n{}".format(name, url))
            self.files[course.course_id] = new_files

    async def check_announcements(self, courses, channels):
        for course in courses:
            new_a = course.get_announcements()
            if course.course_id not in self.announcements:
                self.announcements[course.course_id] = new_a
            last_a = self.announcements[course.course_id]
            if len(new_a) != len(last_a):
                for i in range(len(new_a) - len(last_a)):
                    a = new_a[i]
                    title = a.attributes["title"]
                    content = self.converter.handle(a.attributes["message"])
                    url = a.attributes["url"]
                    for channel in channels:
                        if course.course_id in self.channels[channel.id]:
                            await channel.send("***Ny kunngjøring i Canvas:\n{}***\n{}\n{}".format(url, title, content))
            self.announcements[course.course_id] = new_a

if __name__ == "__main__":
    token = canvas_integration.get_token(config.DISCORD_TOKEN_FILE)
    client = CanvasClient()
    client.run(token)
