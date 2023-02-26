import datetime
import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()
AUTH_TOKEN=os.getenv('AUTH_TOKEN')
REQUEST_URL=os.getenv('REQUEST_URL')
def save_last_update(created_at):
    with open("./last_update.json","w") as f:
        json.dump({"last_update":created_at},f)

def get_last_update():
    with open("./last_update.json","r")as f:
        json_data =json.load(f)
    return json_data["last_update"]

def get_message():
    last_update = datetime.datetime.strptime(get_last_update(),"%Y-%m-%dT%H:%M:%SZ")
    response = requests.get(REQUEST_URL,headers={"Authorization":f"Bearer {AUTH_TOKEN}"})
    github_log = reversed(response.json())
    message=""
    for log in github_log:
        created_at = datetime.datetime.strptime(log["created_at"],"%Y-%m-%dT%H:%M:%SZ")
        if created_at > last_update:
            if log["type"] == "PushEvent":
                message+=(message_format(log))

    save_last_update(log["created_at"])
    return message

def message_format(log):
    return f'```{log["actor"]["login"]}さんがpushしました。\nmessage:{log["payload"]["commits"][0]["message"]}```\n'

if __name__=="__main__":
    get_message()