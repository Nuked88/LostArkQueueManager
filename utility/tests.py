import requests
res = requests.post('https://laq.animecast.net/send_message', json={"queue":300,"serverName":"Neria", "bot_chatID":"89199228","count":0,"send_message_under":400})
if res.ok:
    print(res.text)
res = requests.post('https://laq.animecast.net/send_message', json={"queue":300,"serverName":"", "bot_chatID":"89199228","count":0,"send_message_under":400})
if res.ok:
    print(res.text)
res = requests.post('https://laq.animecast.net/send_message', json={"queue":330,"serverName":"None", "bot_chatID":"89199228","count":0,"send_message_under":400})
if res.ok:
    print(res.text)
res = requests.post('https://laq.animecast.net/send_message', json={"queue":400,"serverName":"Valtan", "bot_chatID":"89199228","count":0,"send_message_under":400})
if res.ok:
    print(res.text)
res = requests.post('https://laq.animecast.net/send_message', json={"queue":450,"serverName":"Valtan", "bot_chatID":"89199228","count":1,"send_message_under":400})
if res.ok:
    print(res.text)
res = requests.post('https://laq.animecast.net/send_message', json={"queue":3210,"serverName":"Valtan", "bot_chatID":"89199228","count":0,"send_message_under":400})
if res.ok:
    print(res.text)
res = requests.post('https://laq.animecast.net/send_message', json={"queue":3110,"serverName":"Neria", "bot_chatID":"89199228","count":0,"send_message_under":400})
if res.ok:
    print(res.text)