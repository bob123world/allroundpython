import os
from shutil import copy2
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH

config = {}
config["root"] = 'C:/Users/admin/Music'

count = 0



for dir_path, dir_names, file_names in os.walk(config["root"]):
    for file in file_names:
        try:
            mp3 = MP3File(os.path.join(dir_path, file))
            mp3.set_version(VERSION_2)
            
            if not os.path.exists(os.path.join(config["root"], mp3.album)):
                os.makedirs(os.path.join(config["root"], mp3.album))
            
            orgfile = os.path.join(dir_path, file)
            track = mp3.track
            track = track.split("/")
            if int(track[0]) < 10:
                number = "0" + track[0]
            else:
                number = track[0]
            new_file_name = number + " " + mp3.song + ".mp3"
            destfile = os.path.join(config["root"], mp3.album, new_file_name)
            copy2(orgfile, destfile)
            os.remove(orgfile)

        except Exception as e:
            print(e)