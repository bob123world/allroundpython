import os,sys

config = {}
config["folder"] = '//beanr1edi001/pelican/TO_TOL/PUSX15/dat'
config["extension"] = ".txt"

for filename in os.listdir(config["folder"]):
       infilename = os.path.join(config["folder"],filename)
       if not os.path.isfile(infilename): continue
       oldbase = os.path.splitext(filename)
       newname = infilename + config["extension"]
       output = os.rename(infilename, newname)