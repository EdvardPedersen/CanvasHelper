#!/usr/bin/env python

import asyncio
import urllib.request
import datetime
import re

import discord
import html2text

import canvas_integration
import config
import cal

class CanvasClient(discord.Client):
    def __init__(self):
        super().__init__()
        self.files = {}
        self.announcements = {}
        self.courses = {}
        self.calendars = {}
        self.course_names = config.COURSE_NAMES
        self.channels = config.CHANNEL_COURSES
        for channel in self.channels:
            for course in self.channels[channel]:
                if course not in self.courses:
                    self.courses[course] = []
                self.courses[course].append(channel)
        self.converter = html2text.HTML2Text()

        self.loop.create_task(self.check_canvas())
        self.loop.create_task(self.check_calendar())

    async def on_ready(self):
        print("Connected to {}".format(client.guilds))

    async def on_message(self, message):
        if message.channel.id not in self.channels:
            return
        if message.content.startswith(config.LANG["helpcommand"]):
            await message.channel.send(config.LANG["helptext"])
        elif message.content.startswith(config.LANG["calendarcommand"]):
            courses = self.channels[message.channel.id]
            for course in courses:
                await message.channel.send(self.calendars[course].get_weekly_calendar())
        elif message.content.startswith(config.LANG["lecturecommand"]):
            courses = self.channels[message.channel.id]
            for course in courses:
                await message.channel.send(self.calendars[course].get_weekly_calendar(restrict = "lecture"))
        elif message.content.startswith(config.LANG["groupcommand"]):
            courses = self.channels[message.channel.id]
            for course in courses:
                await message.channel.send(self.calendars[course].get_weekly_calendar(restrict = "group"))
        elif message.content.startswith(config.LANG["plancommand"]):
            courses = self.channels[message.channel.id]
            for course in courses:
                await message.channel.send(self.get_semester_plan(course))

    def get_semester_plan(self, course):
        now = datetime.datetime.now()
        week = int(now.strftime("%V"))

        content = urllib.request.urlopen(config.COURSE_SEMESTER_PLAN[course]).read().decode()
        current_week = 0
        selected = ["```"]
        for line in content.split("\n"):
            if line.startswith("|"):
                match = re.search("w(\s*)[0-9]*", line)
                if match is not None:
                    weeknum = match.group(0).split()[-1]
                    try:
                        int(weeknum)
                    except ValueError:
                        continue
                    current_week = int(weeknum)
                if week <= current_week <= week + 1:
                    l = line.split("|")
                    selected.append(f"{l[2]} | {l[3]}")
        selected.append("```")
        return "\n".join(selected)



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

    async def check_calendar(self):
        await self.wait_until_ready()
        for c in self.course_names:
            self.calendars[c] = cal.CourseCalendar(self.course_names[c])
        while not self.is_closed():
            for c in self.calendars:
                self.calendars[c].update_calendar()
            await asyncio.sleep(config.CALENDAR_UPDATE_INTERVAL)


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
                                await channel.send(config.LANG["fileuploadtext"].format(course.course.attributes["name"], name, url))
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
                            await channel.send(config.LANG["announcementtext"].format(course.course.attributes["name"], url, title, content))
            self.announcements[course.course_id] = new_a

if __name__ == "__main__":
    token = canvas_integration.get_token(config.DISCORD_TOKEN_FILE)
    client = CanvasClient()
    client.get_semester_plan("21176")
    client.run(token)
