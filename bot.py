#!/usr/bin/env python3
import sys
import yaml
import json
import asyncio
import discord
import commands
import requests
import datetime
import importlib
from os import listdir
from os.path import isfile, join
from colorama import Fore, Back


loop = asyncio.get_event_loop()


def loadyaml(file):
    with open(file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data


config = loadyaml("config.yml")


class log:
    def err(push, data):
        if push:
            print(" " * len(str(datetime.datetime.now()) + ": ") + Fore.RED + str(data) + Fore.RESET)
        else:
            print(str(datetime.datetime.now()) + ": " + Fore.RED + str(data) + Fore.RESET)

    def warn(push, data):
        if push:
            print(" " * len(str(datetime.datetime.now()) + ": ") + "\u001b[31;1m" + str(data) + Fore.RESET)
        else:
            print(str(datetime.datetime.now()) + ": " + "\u001b[31;1m" + str(data) + Fore.RESET)

    def log(push, data):
        if push:
            print(" " * len(str(datetime.datetime.now()) + ": ") + Fore.BLUE + str(data) + Fore.RESET)
        else:
            print(str(datetime.datetime.now()) + ": " + Fore.BLUE + str(data) + Fore.RESET)

    def success(push, data):
        if push:
            print(" " * len(str(datetime.datetime.now()) + ": ") + Fore.GREEN + str(data) + Fore.RESET)
        else:
            print(str(datetime.datetime.now()) + ": " + Fore.GREEN + str(data) + Fore.RESET)


l_url = 'https://discordapp.com/api/v6/auth/login'  # Login URL. Used for the login req.
headers = {'User-Agent': config['user-agent']}  # User-Agent.


def perform(method, url, data=None, headers={}, params=None):
    resp = requests.Session().request(method, url, data=data, headers={**headers, **headers}, params=params)
    return resp


#  Login function, returns Token.
def login(email, password):
    credentials = json.dumps({'email': email, 'password': password}).encode('utf-8')
    post = perform('POST', l_url, data=credentials, headers={'Content-Type': 'application/json'})
    if post.status_code == 200:
        token = post.json()['token']
        return token
    return False


allcommands = [f for f in listdir("./commands/") if isfile(join("./commands/", f))]
for fn in range(len(allcommands)):
    allcommands[fn] = allcommands[fn].replace('.py', "")

for lib in allcommands:
    globals()[lib] = importlib.import_module("commands." + lib)

token = False
if config['use-token']:
    token = config['token']
else:
    temp = config['credentials'].split(":", 1)
    log.log(False, f'Logging into [{Fore.YELLOW + temp[0].upper() + Fore.BLUE}]')
    tok = False
    try:
        try:
            tok = login(temp[0], temp[1])
        except:
            tok = login(temp[0], temp[1])
    except:
        pass
    if tok:
        token = tok
    else:
        log.err(False, f"Could not log into [{temp[0]}]")
        sys.exit()

class bot(discord.Client):
    async def on_message(self, msg):
        for p in config['prefixes']:
            for y in allcommands:
                await eval(f"commands.{y}.{y}(self, msg, p, config)")


if token:
    loop.create_task(bot().start(token, bot=False, reconnect=True))
else:
    sys.exit()

log.warn(False, "WARNING: This script is in beta. Don't get angry at me if it's retarded.")
log.log(False, "LOADING MODULES:")
for x in allcommands:
    log.log(True, f"- {x}")


loop.run_forever()
print(config)
