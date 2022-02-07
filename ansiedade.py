import os
from traceback import print_tb
#import sys
from discord.ext import tasks
from dotenv import load_dotenv

import discord

import urllib.request, json

import pickle

class MyClient(discord.Client):
	def __init__(self, *args, **kwargs):
		self.channelsFileName = "channels.pickle"
		try:
			with open('channels.pickle', 'rb') as handle:
				self.channels = pickle.load(handle)
			print('Channels file found. The following channels will be used for notifying:')

		except FileNotFoundError:
			print('Channels file not found. This is either your first time running this or an error has ocurred.')

		self.URL = "https://www.fuvest.br/wp-json/wp/v2/media"
		
		super().__init__(*args, **kwargs)
		self.background_task.start()
		urllib.request.urlretrieve(self.URL, "original.json")

	async def on_ready(self):
			print('Logged on as {0}!'.format(self.user))

	def save_channels(self):
		with open('channels.pickle', 'wb') as handle:
			pickle.dump(self.channels, handle, protocol=pickle.HIGHEST_PROTOCOL)

	async def notify(self, message, file = None):
		for i in self.channels:
			channel = self.get_channel(i)
			await channel.send(message, file=file)

	async def on_message(self, message):
		if message.author.id != self.user.id:
			if message.content.startswith('oi bot'): #era pra isso ser só um teste mas vou deixar aqui
				await message.reply('oi :]')
			
			if message.content.startswith('%'):
				command = message.content[1:]

				if command == "help":
					await message.reply("mensagem de ajuda ainda será feita")
				elif command == "add-channel":
					channel = message.channel.id

					if channel in self.channels:
						await message.reply("Esse canal já foi adicionado. Vou pingar everyone aqui quando sair o resultado da FUVEST.")
						
					else:
						self.channels.append(channel)
						self.save_channels()
						await message.reply("Esse canal será adicionado e vou pingar everyone aqui quando sair o resultado da FUVEST.")

				else:
					await message.reply("Não reconheço esse comando. Digite direito por favor.")

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