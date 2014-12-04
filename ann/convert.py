from __future__ import absolute_import
import xmltodict
from .models import *


def search(xml):
    data = xmltodict.parse(xml)
    return [Anime(anime) for anime in data["ann"]["anime"]]


def anime(xml):
    data = xmltodict.parse(xml)

    if len(data["ann"]["anime"]):
        return Anime(data["ann"]["anime"])
