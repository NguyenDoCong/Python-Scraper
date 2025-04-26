# download mp3 file from url https://sf19-music.tiktokcdn-eu.com/obj/ies-music-eu2-no/7491329851941538582.mp3
#     """Log the download status in history and log file."""
import os
import requests

file = requests.get("https://www.tikwm.com/video/music/7496340302253362439.mp3")
print(file.text)
with open("test.m4a", "wb") as f:
    f.write(file.content)