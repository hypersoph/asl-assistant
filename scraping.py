import requests
from bs4 import BeautifulSoup
import psycopg2
import settings
import processing
import re
from interactions import Embed

class HandSpeak:
    def search(self, input, current_page=1):
        url = settings.HS_API_URL
        payload = f'page={current_page}&query={input}'
        headers = {
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

        response = requests.request("POST", url, headers=headers, data = payload)
        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            results = soup.find('ul',class_='col-abc').find_all('a') 
        except:
            return {
                'queryResults':"No results found.",
                'numPages':0
            }
        
        num_pages = int(soup.find('ul',class_='pagination').find_all('li')[-2].get_text())

        return {
            'queryResults':results,
            'numPages':num_pages
        }
    
    def wordOfTheDay(self, id):
        session = requests.session()

        url = "https://www.handspeak.com"
        response = session.get(url)

        headers = {'Referer': url,
                   'Accept': '*/*',
                   'Accept-Encoding': 'identity;q=1, *;q=0', 
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67'}

        soup = BeautifulSoup(response.text, 'html.parser')
        
        wotd_vid_element = soup.select('#signofday + section video')[0]
        relative_video_url = wotd_vid_element.get('src')
        english_equivalent = soup.find('span', class_='tip-line').get_attribute_list('data-tip')[0]
        english_equivalent = re.sub('Meaning: ', '', english_equivalent)
        video_url = url + relative_video_url
        video_request = session.get(video_url, stream=True, headers=headers)

        with open(f"wotd.mp4", "wb") as file:
            for chunk in video_request.iter_content(chunk_size=1024):
                file.write(chunk)
        return f"**The Word of the Day is:** ||{english_equivalent}||"

    def makeSearchEmbed(self,results, search_input):
        query_formatted = '+'.join(search_input.split())
        description = processing.search_result_list(results, source="hs")
        embed = Embed(
            title = f"Search results: {search_input}",
            description=description
        )
        embed.set_footer(text="HandSpeak.com",icon_url="https://i.imgur.com/TBq0Afu.png")
        embed.add_field(name='Additional info',value=f'[See Google search results ⯈](https://www.google.com/search?hl=en&q=site%3Ahandspeak.com+{query_formatted})')
        return embed

class LifePrint:
    hostname = settings.DB_SETTINGS['host']
    username = settings.DB_SETTINGS['user']
    password = settings.DB_SETTINGS['password']
    database = settings.DB_SETTINGS['db']

    def sqlQuery(self, query):
        conn = psycopg2.connect( host=self.hostname, user=self.username, password=self.password, dbname=self.database )
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        return rows

    def randomVid(self):
        query = """
        SELECT video_url FROM lifeprint_vids
        ORDER BY RANDOM()
        LIMIT 1
        """
        rows = self.sqlQuery(query)
        
        selected_vid = rows[0][0]
        return selected_vid

    def search(self, search_input):
        query = f'''
        SELECT * from lifeprint_vids
        WHERE phrase
        ~* '\y{search_input}\y'
        '''
        search_results = self.sqlQuery(query)
        return search_results

            