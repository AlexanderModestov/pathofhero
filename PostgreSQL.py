# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 00:02:56 2022

@author: Alexa
"""

import psycopg2

class PostgreSQL:

    def __init__(self, database, user, password, host, port):
        self.connection = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
        self.cursor = self.connection.cursor()
        with self.connection:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS answers(
                                            chat_id bigint,
                                            user_id bigint,
                                            poll_number int,
                                            question_id int,
                                            response int, 
                                            timestamp TIMESTAMP WITH TIME ZONE)
                                """)
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS profile(
                                            user_id bigint,
                                            name TEXT,
                                            age TEXT,
                                            location TEXT,
                                            position TEXT,
                                            links TEXT,
                                            satisfaction TEXT,
                                            interests TEXT,
                                            hobbies TEXT,
                                            achievments TEXT)
                                """)

    def get_poll(self, chat_id):
        """ Получаем все строки """
        with self.connection:
            self.cursor.execute('SELECT max(poll_number) FROM answers where chat_id={}'.format(chat_id))
            serial_poll = self.cursor.fetchall()
            if serial_poll[0][0] is None:
                return 0
            else:
                return serial_poll[0][0]
        
    def get_question(self, poll_id):
        """ Получаем все строки """
        with self.connection:
            question_id = self.cursor.execute('SELECT max(question_id) from answers where poll_number = {}'.format(poll_id)).fetchall()   
            if question_id[0][0] is None:
                return 1
            else:
                return question_id[0][0]

    def select_all(self):
        """ Получаем все строки """
        with self.connection:
            self.cursor.execute('SELECT * FROM answers')
            return self.cursor.fetchall()
    
    def insert_row(self, values):
        """ Получаем все строки """
        with self.connection:
            self.cursor.execute('insert into answers (chat_id, user_id, poll_number, question_id, response, timestamp) values ({}, {}, {}, {}, {}, {})'.format(values[0], values[1], values[2], values[3], values[4], 'CURRENT_TIMESTAMP'))

    def create_profile(self, user_id):
        with self.connection:
            #user = self.cursor.execute("SELECT 1 FROM profile WHERE user_id = {}".format(user_id)).fetchone()
            if self.cursor.execute('SELECT 1 FROM profile WHERE user_id = {}'.format(user_id)) is None:
                self.cursor.execute('INSERT INTO profile (user_id) VALUES({})'.format(user_id))

    def edit_profile(self, state, user_id):
        pass
        #with state.proxy() as data:
        #    cur.execute("UPDATE profile SET photo = '{}', age = '{}', description = '{}', name = '{}' WHERE user_id == '{}'".format(
        #    data['photo'], data['age'], data['description'], data['name'], user_id))

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()