import common, Cecilia
import json

j= Cecilia.Cecilia()
#j.execute_command('hi')

d= j._SPOT.devices()
print(json.dumps(d, indent= 4, sort_keys= True))
maind= j.get_active_device_info()

text= 'cc play Nah nah nah by kanye'
j.search_song(text)

j.reauth_spotify()