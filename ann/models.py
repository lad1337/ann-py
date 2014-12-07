from helpers import scrap_episodes

class BaseModel(object):

    _repr_fields = []
    _converters = {}

    def __init__(self, raw_data):
        self.raw_data = raw_data

    def __getattr__(self, item):
        try:
            value = self.raw_data[item]
        except KeyError:
            try:
                value = self.raw_data["@{}".format(item)]
            except KeyError:
                raise AttributeError(
                    "{} has no attribute or data under key '{}'".format(
                        self.__class__, item)
                )
        if item in self._converters:
            return self._converters[item](value)
        return value

    def __eq__(self, other):
        return self.raw_data == other.raw_data

    def __repr__(self):
        if not self._repr_fields:
            return super(BaseModel, self).__repr__()
        return u"{}: {}".format(
            self.__class__.__name__, (u"{} " * len(self._repr_fields)).format(
                *[getattr(self, key) for key in self._repr_fields]
        )[:-1])

    def __str__(self):
        return unicode(repr(self))

class Anime(BaseModel):

    _repr_fields = ["name"]
    _converters = {
        "id": int
    }

    @property
    def episodes(self):
        episodes = [Episode(self, ep)
                    for ep in self.raw_data["episode"]]
        return sorted(episodes)

    def __getattr__(self, item):
        try:
            return super(Anime, self).__getattr__(item)
        except AttributeError:
            info = self.info(item)
            if info:
                return info[0]["value"] if info else None
            raise

    @property
    def image(self, size=1):
        info = self.info("picture", tag="@src")
        if info and info[0]["img"]:
            try:
               return info[0]["img"][size]["@src"]
            except KeyError:
                try:
                    return info[0]["img"][0]["@src"]
                except KeyError:
                    return info[0]["img"]["@src"]
        return None

    def info(self, type, tag=None):
        data = []
        for i in self.raw_data["info"]:
            if type.lower() not in i["@type"].lower().replace(" ", "_"):
                continue
            _data = dict(**i)
            if tag:
                _data["value"] = i.get(tag)
            else:
                _data["value"] = _data.get("#text")
            data.append(_data)

        return data

    def info_types(self):
        return set([
            i["@type"].lower().replace(" ", "_")
            for i in self.raw_data["info"]
        ])

    def fill(self):
        scrap_episodes(self.id)

class Episode(BaseModel):

    _repr_fields = ["title", "num"]
    _converters = {
        "num": int
    }

    def __init__(self, anime, raw_data):
        self.anime = anime
        super(Episode, self).__init__(raw_data)

    def __eq__(self, other):
        return super(Episode, self).__eq__(other) and self.anime == other.anime

    def __cmp__(self, other):
        if self.num < other.num:
            return -1
        return 1

    @property
    def date(self):
        data = scrap_episodes(self.anime.id)
        if data and self.num in data:
            return data[self.num]["date"]

    @property
    def title(self):
        return self.raw_data["title"]["#text"]

