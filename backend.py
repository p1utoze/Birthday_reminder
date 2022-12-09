import json
import time
import os

def checkdate():
    path = os.path.join("/home/p1utoze/Documents/pyprojects/bdayrem/", "data.json")
    with open(path, "r") as f:
        d = json.load(f)
    today = time.strftime("%m/%d")
    print("Running")
    try:
        names = d[today]
        for name in names:
            os.system('notify-send -u critical "\nBirthdays Today: "'+name)

    except KeyError:
        os.system('notify-send "\nNo Birthdays Today!\n"')

if __name__ == "__main__":
    checkdate()
