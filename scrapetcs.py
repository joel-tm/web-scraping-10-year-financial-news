import requests
from bs4 import BeautifulSoup
import re
import csv
from datetime import datetime

a_values = []
date_value = []

base_url = "https://www.moneycontrol.com/stocks/company_info/stock_news.php?sc_id=TCS&scat=&pageno={}&next=0&durationType=Y&Year={}&duration=1&news_type="

for year in range(2011, 2024): # Change the range as per your requirement here the number of years are given
    start_url = base_url.format(1, year)  # Use 1 as the page number just for printing
    print(start_url)#this will print when 1 year is done and goes to next year
    
    for page_number in range(1,50):# here it goes on to next pages ie checks for values from 1 to 50
         start_url = base_url.format(page_number, year)  
         page_data=requests.get(start_url) #sending a http request to the site
         soup=BeautifulSoup(page_data.content,"html.parser") #getting that requested data to store in an object called soup

         job_tags = soup.find_all('div',class_="FL PR20")
         if not job_tags:  # If the page has no matching tags, break the loop and move to the next year,without this the code took so long :(
            print(page_number,year)
            break

         for job_tag in soup.find_all('div',class_="FL PR20"):
             #finding all the div tags with class name FL which  has the news heading

            a=job_tag.find('a')['href'] #finding the a tag and getting the text
            a = a.replace('/news/recommendations/', '').replace('.html', '') .replace('/news/results/','').replace('/news/','')

            '''#remove '/news/recommendations' and '.html' from the string 
            #/news/recommendations/buy-reliance-industries-targetrs-3130-sharekhan_17408921.html what it originally looks like'''

            a = a.split('_')[0] # removes the part after the '_' in the output string
            a_values.append(a)
            #print(a)# if you want to see news heading in terminal not recommended as lot of lines are there,if you want then reduce the years and range for just 1year

            c = job_tag.parent
            date_element = c.find('p', class_="PT3 a_10dgry")
            if date_element:
                date_text = re.sub(r'\d+\.\d+ (am|pm) \| ', '', date_element.text).replace('Source: Moneycontrol.com', '').replace('|', '').strip()
                date_text=date_text.split('\xa0')[0]
                date_value.append(date_text)
                #print(date_value) 


pairs = [(datetime.strptime(date, "%d %b %Y"), news) for date, news in zip(date_value, a_values)]
'''
This line is creating a list of tuples, where each tuple contains a date 
and the corresponding news. The datetime.strptime(date, "%d %b %Y") 
part is converting each date from a string to a datetime object. The zip(date_value, a_values)
 part is pairing each date with the corresponding news.
'''

pairs.sort()#This line is sorting the list of tuples by date in ascending order.
#Because the dates are now datetime objects, they can be sorted correctly.

# Convert the dates back to strings and unzip the pairs
date_value, a_values = zip(*[(date.strftime("%d %b %Y"), news) for date, news in pairs])
'''
This line is converting the dates back to strings and unzipping the list of tuples. The date.strftime("%d %b %Y") 
part is converting each date from a datetime object back to a string. 
The zip(*[(date.strftime("%d %b %Y"), news)for date, news in pairs]) 
part is unzipping the list of tuples into two lists: one for the dates and one for the news.
'''


with open('tcsnews.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Date", "News"])
    for g,h in zip(date_value, a_values):
        writer.writerow([g,h])