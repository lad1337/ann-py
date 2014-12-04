#from __future__ import absolute_import
import requests
import convert

URL = "http://cdn.animenewsnetwork.com/encyclopedia/api.xml"


def search(term):
    r = requests.get(URL, params={"title": "~{}".format(term)})
    return convert.search(r.text)


def anime(id):
    r = requests.get(URL, params={"anime": "{}".format(id)})
    return convert.anime(r.text)



