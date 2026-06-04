#Convert the video to mp3
import os
import subprocess

files = os.listdir('videos')
for file in files:
  # print(file)
  tutorial_number = file.split(".")[0].split("Part-")[1]
  file_name = file.split(" - ")[0]
  print(tutorial_number, file_name)
  subprocess.run(['ffmpeg','-i',f"videos/{file}",f"Audios/{tutorial_number}_{file_name}.mp3"])