
import requests
import convert

URL = "http://cdn.animenewsnetwork.com/encyclopedia/api.xml"

__version__ = "0.1.0"

def search(term):
    r = requests.get(URL, params={"title": "~{}".format(term)})
    return convert.search(r.text)


def anime(id):
    r = requests.get(URL, params={"anime": "{}".format(id)})
    return convert.anime(r.text)



