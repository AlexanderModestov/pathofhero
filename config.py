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
#database='postgres'
#host='psychobot.postgres.database.azure.com'
#user='alexmodestov'
#password='PostgreSQL!#'
#port=5432
#DATABASE_URL = 'postgresql+asyncpg://alexmodestov:PostgreSQL!#@psychobot.postgres.database.azure.com:5432/postgres'

host='ec2-52-210-44-5.eu-west-1.compute.amazonaws.com'
database='dfe7n9tqm5cq2'
user='ceangsfkkcakpj'
port=5432
password='7e4295dbbd5a2bda1868d58d2307b9eaa1dfc4812c42408ac68727645350b1ec'