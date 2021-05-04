from requests_html import HTMLSession
import re
import asyncio
if asyncio.get_event_loop().is_running(): # Only patch if needed (i.e. running in Notebook, Spyder, etc)
    import nest_asyncio
    nest_asyncio.apply()

class Parser:
    
    def __init__(self):
        self.session = HTMLSession()
    
    def getPage(self, url):
        r = self.session.get(url)
        return r.text
         
    def getHeroData(self, hero):
        url = "https://ru.dotabuff.com/heroes/winning"
        text = self.getPage(url)
        pattern = '<tr>(.*?)</tr>'
        match = re.findall(pattern, text)
        for s in match:
            if hero.lower() in s.lower():
                pattern = '<.*<td data-value=".*">(.*?)<div class="bar bar-default"><div class="segment segment-win" style=".*"></div></div></td><td data-value=".*">(.*?)<div class="bar bar-default"><div class="segment segment-pick" style="width:.*"></div></div></td><td data-value=".*">(.*?)<div class="bar bar-default"><div class="segment segment-kda" style="width:.*"></div></div></td>'
                m = re.search(pattern, s)
                winrate = m.group(1)
                pickrate = m.group(2)
                kda = m.group(3)
                return "Stats for {0}\nWinrate: {1}\nPickrate: {2}\nKDA: {3}".format(hero.title(), winrate, pickrate, kda)
        return "Oops, something went wrong"
    
    def getCounterPick_old(self, enemies, allies):
        url = 'http://dotapicker.com/herocounter#!'
        for enemy in enemies:
            url += '/E_' + enemy.title().replace(' ', '_')
        for ally in allies:
            url += '/T_' + ally.title().replace(' ', '_')
        while True:
            r = self.session.get(url)
            r.html.render(timeout=300)
            text = r.html.html
            text = " ".join(text.split())
            pattern = 'class="inlineBlock vAlignMid ng-binding ng-scope"> (.*?)<br>'
            match = re.findall(pattern, text)
            if len(match) != 0:
                break
        return match[0:5]
    
    def getCounterPick(self, enemies):
        heros = {}
        for enemy in enemies:
            url = "https://ru.dotabuff.com/heroes/{0}/counters".format(enemy.lower().replace(' ', '-'))
            text = self.getPage(url).replace('&#39;', "'")
            pattern = '">\s*([^>]*?)\s*<\/a>\s*<\/td>\s*<td data-value="([^>]*?)">'
            match = re.findall(pattern, text)
            for hero in match:
                if hero[0] in heros:
                    heros[hero[0]] += float(hero[1])
                else:
                    heros[hero[0]] = float(hero[1])
        heros = {k: v for k, v in sorted(heros.items(), key=lambda item: item[1])}
        res = list(heros.keys())[-5:]
        res.reverse()
        return res
    
if __name__ == '__main__':
    url = "https://ru.dotabuff.com/heroes/abaddon"
    parser = Parser()
    print(parser.getCounterPick(['Abaddon', 'Ancient Apparition']))