import os

config = {}
config["root"] = 'J:'

count = 0

for dir_path, dir_names, file_names in os.walk(config["root"]):
    for file in file_names:
        count += 1
        if not(file[0].isdigit()) and not(file[1].isdigit()):
            path = os.path.join(dir_path, file)
            print(path)
            # if os.path.exists(path):
            #     os.remove(path)
            # else:
            #     print("Unable to delete: " + path)
        if "DESKTOP" in file:
            path = os.path.join(dir_path, file)
            print(path)
        
print("amount of file scanned: " + str(count))