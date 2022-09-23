import requests

api_link = "https://api.fusionsid.xyz/api/runcode/"

data = {
    "code" : 'take me to ur heart\n    i just wanna tell u how im feeling "I am cool"\nsay goodbye',
    "language" : "rickroll_lang"
}

response = requests.post(api_link, json=data).json()
print(response)