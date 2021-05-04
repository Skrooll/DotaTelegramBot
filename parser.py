from requests_html import HTMLSession
import re

class Parser:
    def getPage(self, url):
        session = HTMLSession()
        r = session.get(url)
        return r.text
         
    def getHeroData(self, hero):
        url = "https://ru.dotabuff.com/heroes/" + hero.lower()
        text = self.getPage(url)
        winrate = re.search('<span class="won">(.*?)</span>', text).group(1)
        print(winrate)
    
if __name__ == '__main__':
    url = "https://ru.dotabuff.com/heroes/abaddon"
    parser = Parser()
    parser.getHeroData('Abaddon')