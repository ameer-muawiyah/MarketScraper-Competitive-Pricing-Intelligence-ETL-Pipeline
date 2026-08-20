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

    

