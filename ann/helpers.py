from datetime import datetime
import requests
from bs4 import BeautifulSoup


class Memoize:
    def __init__ (self, f):
        self.f = f
        self.mem = {}
    def __call__ (self, *args, **kwargs):
        if (args, str(kwargs)) in self.mem:
            return self.mem[args, str(kwargs)]
        else:
            tmp = self.f(*args, **kwargs)
            self.mem[args, str(kwargs)] = tmp
            return tmp


@Memoize
def scrap_episodes(anime_id):
    r = requests.get("http://www.animenewsnetwork.com/encyclopedia/anime.php",
         params={"id": anime_id, "page": 25}
    )
    soup = BeautifulSoup(r.text)
    episodes = {}
    table = soup.find("table", class_="episode-list")
    for row in table.find_all("tr"):
        """
          <tr>
            <td class="d">
                    <div>2014-01-05</div>
                </td>
                <td class="n">1.</td>
                <td class="pn"></td>
                <td valign="top">
                    <div>Live With the Flow, Baby</div>
                    <div class="j">
                     <div> Nagare nagasarete ikiru jan yo</div>
                     <div> japan stuff</div>
                    </div>
                </td>
            </tr>
        """
        num = int(row.find_all(class_="n", limit=1)[0].text[:-1])
        date = datetime(
            *map(int, row.find_all(class_="d", limit=1)[0].div.text.split("-"))
        )
        episodes[num] = {"date": date}
    return episodes
