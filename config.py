# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 00:04:16 2022

@author: Alexa
"""
from dotenv import load_dotenv
import os

load_dotenv(override=True)

TOKEN = os.environ.get("TOKEN")
#database = os.environ.get("DATABASE")
#host = os.environ.get("HOST")
#user = os.environ.get("USER")
#password = os.environ.get("PASSWORD")
#port = os.environ.get("PORT")

###############################################################################
database='postgres'
host='psychobot.postgres.database.azure.com'
user='alexmodestov'
password='PostgreSQL!#'
port=5432
DATABASE_URL = 'postgresql+asyncpg://alexmodestov:PostgreSQL!#@psychobot.postgres.database.azure.com:5432/postgres'