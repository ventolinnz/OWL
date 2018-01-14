# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 11:49:39 2018

@author: Nguyen
"""

#Discord and Networking Libraries
import discord
import asyncio

#Supprorting Libraries
import os
import time
import datetime
import logging
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver


logging.basicConfig(level=logging.INFO)
token = os.environ['discord_token']
client = discord.Client()
options = webdriver.ChromeOptions()
options.add_argument('headless')

if __name__ == '__main__':
    weekly_info = {'last_usage':datetime.datetime(1984,1,1), 'week_info': ''}
    @client.event
    async def on_ready():
        '''On start notification'''
        print('Logged in as %s' % client.user.name)

    @client.event
    async def on_message(message):
        if 'bot help' in message.content.lower() and message.author != client.user:
            await client.send_message(message.channel, 'To use OW-League-Bot, please @ the bot and send a command. List of commands are found through the use of \'commands\' when mentioning the bot')
        if client.user.mentioned_in(message):
            if 'developer' in message.content.lower():
                await client.send_message(message.channel, 'This application was developed by Jacob, more work found at https://github.com/Jbiloki')
            if 'commands' in message.content.lower():
                await client.send_message(message.channel, 'Current available commands are \'developer\', \'bot help\' and \'show week\'')
            if 'show week' in message.content.lower():
                current_date = datetime.datetime.now()
                print(current_date, (current_date - weekly_info['last_usage']).days) 
                if weekly_info['last_usage'] == datetime.time(0, 0) or (current_date - weekly_info['last_usage']).days >= 3:
                    browser = webdriver.Chrome('C:/Users/Nguyen/Downloads/chromedriver_win32/chromedriver.exe', chrome_options=options)
                    browser.get('https://overwatchleague.com/en-us/schedule')
                    time.sleep(5)
                    html_raw = browser.execute_script('return document.body.innerHTML')
                    full_html = BeautifulSoup(html_raw, 'html.parser')
                    ret_info = []
                    for schedule in full_html.find_all(class_='MatchRow MatchRow-match'):
                        ret_info.append(schedule.getText(separator=u' ')[:-13])
                    browser.close()
                    weekly_info['last_usage'] = current_date
                    weekly_info['week_info'] = ret_info
                    await client.send_message(message.channel, '\n'.join(ret_info))
                else:
                    await client.send_message(message.channel, '\n'.join(weekly_info['week_info']))
    client.run(token)
