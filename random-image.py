#!/usr/bin/env python3.7

import asyncio
import iterm2
import os
import random
import re

# This script was created with the "basic" environment which does not support adding dependencies
# with pip.

# osascript "/Users/admin/Library/Application Support/iTerm2/Scripts/iterm2-random-background.scpt"
image_dir = "/Users/admin/Pictures/BackgroundImage"
images_temp = os.listdir(image_dir)

blend_re = re.compile("_blend\(([^)]*)\)")


def blend_value(s, default=0.25):
    m = re.findall(blend_re, s)
    if len(m) == 0:
        return default
    else:
        return float(m[0])


images = list(
    map(
        lambda p: (os.path.join(image_dir, p), blend_value(p)),
        filter(lambda s: not s.startswith("."), images_temp),
    )
)

print(images)


async def main(connection):
    app = await iterm2.async_get_app(connection)

    async def change_pic(session_id):
        session = app.get_session_by_id(session_id)
        profile = await session.async_get_profile()
        print("Session ID {} created".format(session_id))
        p, blend = random.choice(images)
        await profile.async_set_blend(0)
        await profile.async_set_background_image_location(p)

        async def change_blend(b: float, steps: int = 10):
            b = max(0.0, min(1.0, b))
            frame = 0.1 / steps
            i = 0
            while i < steps:
                s = asyncio.sleep(frame)
                i += 1
                await profile.async_set_blend((b * i) / steps)
                await s

        await change_blend(blend)

    await iterm2.EachSessionOnceMonitor.async_foreach_session_create_task(
        app, change_pic
    )

    async with iterm2.NewSessionMonitor(connection) as mon:
        while True:
            session_id = await mon.async_get()
            change_pic(session_id)


# This instructs the script to run the "main" coroutine and to keep running even after it returns.
iterm2.run_forever(main)
