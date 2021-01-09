#!/usr/bin/python

"""Notifies the user when roblox IDs in a file become online.
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from win10toast import ToastNotifier

endpoint = "https://api.roblox.com/users/ID_HERE/onlinestatus/"
user_endpoint = "https://users.roblox.com/v1/users/ID_HERE"
notifier = ToastNotifier()
ids_to_user = {}
online_users = []
root_dir = Path(__file__).absolute().parents[0]
ids_file = root_dir / Path("ids.txt")
first_execution = True

PING_DURATION = 5
NOTIF_LIFETIME = 5
ALLOW_NOTIFICATIONS = True

# Make the ids file if it doesn't exist.
if not ids_file.exists():
    open(ids_file, "x").close()
    print("IDs file created. Please put the ids you wish to monitor in it, and execute the program again.")
    print(f"ID file location: {root_dir.absolute()}")
    sys.exit()

# Generate the usernames of each user based off their ID.
ids = [int(id_number) for id_number in open("./ids.txt", "r").read().splitlines()]

for ident in ids:
    new_endpoint = user_endpoint.replace("ID_HERE", str(ident))
    response = requests.get(new_endpoint).content.decode("UTF-8")
    accessible_data = json.loads(response)

    ids_to_user[ident] = accessible_data["name"]

print(f"Monitoring IDs {ids}")

while True:    
    for identification in ids:
        new_endpoint = endpoint.replace("ID_HERE", str(identification))
        response = requests.get(new_endpoint).content.decode("UTF-8")
        
        # Make sure there was a valid response
        if not response:
            continue

        accesible_data = json.loads(response)
        
        # Send a notification that this user just came online.
        # Caches their id until they go offline so we don't spam the user with toasts.
        if accesible_data["IsOnline"] is True:
            if identification not in online_users:
                # Handle notifications.
                if ALLOW_NOTIFICATIONS:
                    if sys.platform == "win32":
                        notifier.show_toast(f"{ids_to_user[identification]} is online.", "This user is online.",
                                            duration=NOTIF_LIFETIME, threaded=not first_execution)
                                            
                    elif sys.platform == "linux":
                        os.system(f"notify-send {ids_to_user[identification]} is online.")
                else:
                    print("f{ids_to_user[identification]} is online.")

                online_users.append(identification)
  
        elif accesible_data["IsOnline"] is False:
            if identification in online_users:
                if ALLOW_NOTIFICATIONS:
                    if sys.platform == "win32":
                        notifier.show_toast(f"{ids_to_user[identification]} is offline", "This user is offline.",
                                            duration=NOTIF_LIFETIME, threaded=not first_execution)
                    elif sys.platform == "linux":
                        os.system(f"notify-send {ids_to_user[identification]} is offline.")
                else:
                    print("f{ids_to_user[identification]} is offline.")

                online_users.remove(identification)

    time.sleep(PING_DURATION)
