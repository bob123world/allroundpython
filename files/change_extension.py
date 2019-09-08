import os,sys

config = {}
config["folder"] = 'C:/Users/admin/Music'
config["extension"] = ".mp3"

for filename in os.listdir(config["folder"]):
       infilename = os.path.join(config["folder"],filename)
       if not os.path.isfile(infilename): continue
       oldbase = os.path.splitext(filename)
       newname = infilename + config["extension"]
       output = os.rename(infilename, newname)