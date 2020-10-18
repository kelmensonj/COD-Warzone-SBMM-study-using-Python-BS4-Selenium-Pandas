import asyncio
from dotenv import load_dotenv
import time
import inspect


import callofduty
from callofduty import Mode, Platform, Reaction, Title

async def main():
	client = await callofduty.Login("********", ********")
	id_list = [14499323038196648427]
	for match_id in id_list:
		time.sleep(1)
		match = await client.GetMatch(Title.ModernWarfare, Platform.Activision, match_id)
		print(match)
asyncio.get_event_loop().run_until_complete(main())



