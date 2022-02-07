import os
#import sys
from discord.ext import tasks
from dotenv import load_dotenv

import discord

import urllib.request, json

class MyClient(discord.Client):
	def __init__(self, *args, **kwargs):
		self.channels = [460965505222574102, 691056194852487229]
		self.URL = "https://www.fuvest.br/wp-json/wp/v2/media"
		
		super().__init__(*args, **kwargs)
		self.background_task.start()
		urllib.request.urlretrieve(self.URL, "original.json")

	async def on_ready(self):
			print('Logged on as {0}!'.format(self.user))

	async def notify(self, message, file = None):
		for i in self.channels:
			channel = self.get_channel(i)
			await channel.send(message, file=file)
	
	@tasks.loop(seconds = 10)
	async def background_task(self): #função de fundo pra testar se saiu e resultado
		print("Test initiated")
		
		urllib.request.urlretrieve("https://www.fuvest.br/wp-json/wp/v2/media", "new.json")

		originalFile = open("original.json")
		newFile = open("new.json")

		original = json.load(originalFile)
		new = json.load(newFile)

		originalFile.close()
		newFile.close()

		if new == original:
			print("Test succeded. No new files found.")
		else:
			print("Test succeded. Fetching download link.")
			
			link = new[0].get('source_url')
			name = new[0].get('slug') + '.pdf'
			urllib.request.urlretrieve(link, name)
			
			file = discord.File(open(name,'rb'), name)

			await self.notify("@everyone A FUVEST fez o upload de um novo arquivo. O link para baixá-lo é {} . Isso é tudo que sei.".format(link), file=file)

			os.remove('original.json')
			os.rename('new.json', 'original.json')

	@background_task.before_loop
	async def before_my_task(self):
		await self.wait_until_ready() # wait until the bot logs in
		

client = MyClient()

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
client.run(token)