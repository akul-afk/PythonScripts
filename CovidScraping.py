
import requests 
from bs4 import BeautifulSoup 
import texttable as tt


url = 'https://www.worldometers.info/coronavirus/countries-where-coronavirus-has-spread/'


page = requests.get(url) 
soup = BeautifulSoup(page.text, 'html.parser') 

data = [] 


data_iterator = iter(soup.find_all('td')) 



while True: 
	try: 
		country = next(data_iterator).text 
		confirmed = next(data_iterator).text 
		deaths = next(data_iterator).text 
		continent = next(data_iterator).text 
		deaths=deaths.replace(',','')			#Removing "," from deaths string
		confirmed=confirmed.replace(',','')		#Removing "," from confirmed string

		data.append(( 
			country, 
			int(confirmed), 		#Converting string to int
			int(deaths), 			#Converting string to int
			continent 
		)) 

	except StopIteration: 
		break
data.sort(key = lambda row: row[1], reverse = True) 


table = tt.Texttable() 
table.add_rows([(None, None, None, None)] + data)  # Add an empty row at the beginning for the headers 
table.set_cols_align(('c', 'c', 'c', 'c'))  # 'l' denotes left, 'c' denotes center, and 'r' denotes right 
table.header((' Country ', ' Number of cases ', ' Deaths ', ' Continent ')) 

print(table.draw()) 
