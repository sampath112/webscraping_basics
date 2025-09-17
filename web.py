import requests
from bs4 import BeautifulSoup
import csv

# If file is local, you can read directly:
with open('sample_books.html', 'r', encoding='utf-8') as f:
    html_content = f.read()
    

# Or serve via: python -m http.server 8000 → then use:
# url = "http://localhost:8000/sample_books.html"
# response = requests.get(url)
# html_content = response.text

soup = BeautifulSoup(html_content, 'lxml')

# tags=soup.find_all('h3')    
# for i in tags:
#     print(i.text)




books = []

for book in soup.find_all('div', class_='book'):
    title = book.find('h3', class_='title').get_text()
    author = book.find('span', class_=None).get_text()  # first span without class
    price = book.find('span', class_=None).find_next('span').get_text()  # next span
    rating_text = book.find('p', class_='rating').get_text()
    
    books.append({
        'Title': title,
        'Author': author,
        'Price': price,
        'Rating': rating_text
    })

# Save to CSV
with open('books.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Title', 'Author', 'Price', 'Rating']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(books)

print("✅ Scraped and saved to books.csv")