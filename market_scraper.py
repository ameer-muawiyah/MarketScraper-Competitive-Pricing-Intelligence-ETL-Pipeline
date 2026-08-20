import requests
from bs4 import BeautifulSoup
import pandas as pd

class MarketScraper:
    
    def __init__(self):
        # 1. The universal dictionary map for the entire class
        self.mapping_dict = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        
        # 2. The master vault that will hold all scraped data
        self.master_list = []

    def extract_book_data(self, book_pod):
        """
        Takes ONE single book's HTML pod, extracts the metrics, 
        and returns a clean Python dictionary.
        """
        book_title = book_pod.h3.a['title']
        book_price = book_pod.find('p', {'class': 'price_color'}).text
        book_instock_status = book_pod.find('p', {'class': 'instock availability'}).text.strip()
        
        # Rating extraction
        book_rating_element = book_pod.find('p', {'class': 'star-rating'})
        mystery_book_ratings = None
        
        if book_rating_element:
            book_class_list = book_rating_element['class']
            mystery_book_ratings = book_class_list[1]
            # Convert string to integer using the class attribute
            mystery_book_ratings = self.mapping_dict[mystery_book_ratings] 
            
        return {
            'Title': book_title, 
            'Price': book_price, 
            'Ratings': mystery_book_ratings, 
            'Availability Status': book_instock_status
        }

    def scrape_category(self, start_url):
        """
        Dynamically paginates through a given category URL, scraping all available books.
        """
        num = 1
        print(f"Initiating scraping protocol for: {start_url}...")
        
        while True:
            # Construct the dynamic URL for the current page
            target_url = f"{start_url}/page-{num}.html"
            r = requests.get(target_url)
            
            # The Failsafe: Break if the page does not exist
            if r.status_code != 200:
                print(f"Target exhausted. Scraping completed at page {num - 1}.")
                break
                
            print(f"Successfully breached page {num}...")
            
            # Parse the HTML and extract the pods
            mystery_soup = BeautifulSoup(r.text, 'html.parser')
            mystery_books = mystery_soup.find_all('article', {'class': 'product_pod'})
            
            # Loop through the pods, call the extraction method, and store the dictionary
            for book in mystery_books:
                clean_book_dict = self.extract_book_data(book)
                self.master_list.append(clean_book_dict)
                
            # Increment to target the next page
            num += 1

    def export_to_csv(self, filename):
        """
        Converts the master_list to a Pandas DataFrame, saves it to a CSV, 
        and returns the DataFrame for notebook preview.
        """
        df = pd.DataFrame(self.master_list)
        df.to_csv(filename, index=False)
        print(f"SUCCESS: Exported {len(self.master_list)} rows to {filename}.")
        
        return df
    

