import csv
import urllib.request
import json
import requests
from flask import redirect, render_template, request, session
from functools import wraps
from cs50 import SQL
from helpers import *
from passlib.apps import custom_app_context as pwd_context


temp = lookup("Siege")
print(temp)

temp2 = list()
for game in temp:
    try:
        temp2.append(game["name"])
    except:
        break

for game in temp2:
    print(game)
