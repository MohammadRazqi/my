from rubpy import Rubika
from re import findall
from time import sleep
import asyncio
# rubpy

bot = Rubika("YOUR-AUTH")
channel_guid : str = "GUID-LINKDONI"
# داخل channel_guid شناسه‌ی کانال لینکدونی که ربات توش عضوه رو باید بزنید تا پیام هاش رو دریافت کنه و لینکارو برداره برای تبلیغ ها
post_link: str = "POST"
# داخل post_link لینک پستتونو میزارین

get_infos: list = [] # get post info
links = []

async def main():
	t: bool = False
	while(t != True):
		try:
			message_info: str = await bot.getLinkFromAppUrl(post_link)
			global get_infos
			get_infos.append(message_info['message_id'])
			get_infos.append(message_info['object_guid'])
			t: bool = True
		except:
			t: bool = False

	t: bool = False
	while(t!=True):
		try:
			messages : list = await bot.getMessagesInterval(channel_guid, await bot.getChannelLastMessageId(channel_guid))
			t:bool=True
		except:
			t:bool=False
	for msg in messages:
		try:
			msg = msg['text']
			group_link = findall(r"https://rubika.ir/joing/\w{32}", msg)
			for link in group_link:
				links.append(link)
		except: pass
	
	while(1):
		for link in links:
			sleep(2)
			t:bool=False
			count:int=0
			limit:int=5
			while(count<5 and t!=True):
				try:
					group_guid:str= await bot.joinGroup(link)
					group_guid: str = group_guid.get('data').get('group').get('group_guid')
					t:bool=True
					count += 5
				except:
					t:bool=False
					count += 1
			t:bool=False
			count:int=0
			limit:int=5
			while(count<5 and t!=True):
				try:
				#	await bot.sendMessage(group_guid, "تبلیغ")
					await bot.forwardMessages(get_infos[1], [get_infos[0]], group_guid)
					print('Sended!')
					t:bool=True
					count+=5
				except:
					t:bool=False
					count+=1
			t:bool=False
			count:int=0
			limit:int=5
			while(count<5 and t!=True):
				try:
					await bot.leaveGroup(group_guid)
					t:bool=True
					count+=5
				except:
					t:bool=False
					count+=1

asyncio.run(main())