#!pip install selenium
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
from tqdm import tqdm


class DataDownloader:
    '''
    This class crawls through dynamic content of https://www.portaldrazeb.cz and collects following things:

            1) soup object for every auctioneer
            2) link to every auction + auction category (since the category is not within the auction page itself)
            3) list of all possible values from drop-down menu (auction categories, regions and districts)
    
    Subsequently it extracts soup objects of all auctions from the links collected in 2).
    '''

    def __init__(self):
        # we initiate the lists for data within particular methods
        self.auctioneers_soups = []
        self.auction_links_and_categories = []
        self.categories = []
        self.regions_and_districts = []
        print('Downloader successfully initialized!')
        print(' ')
        print(DataDownloader.__doc__)
    
    def get_soups_of_auctioneers(self,link):
        '''
        Crawls through all pages of auctioneers and creates a soup object of everyone that is listed there right now.
        '''
        # initiating a webdriver
        driver = webdriver.Chrome('./chromedriver') 
        
        # opening the link in Chrome
        driver.get(link)  
        time.sleep(5) 
        
        # creating a soup object from the page source code
        soup = BeautifulSoup(driver.page_source, "html.parser")  
        
        # getting number of pages
        last_page = int(soup.find('div',{'class':'el-pagination'}).findAll('li',{'class':'number'})[-1].text) 
        
        # locating the element into which we write page number
        page_number = driver.find_element_by_css_selector('input[type="number"]')
        
        # looping through all pages and save the soups
        for page in tqdm(range(1,last_page+1)):
            # getting to a page (delete content, send number of the page, press Enter)
            page_number.send_keys(Keys.BACK_SPACE)
            page_number.send_keys(Keys.BACK_SPACE)
            page_number.send_keys(str(page)) 
            page_number.send_keys(Keys.RETURN)
            time.sleep(5)  

            # save soups of particular auctioneers
            html = driver.page_source   
            soup = BeautifulSoup(html, features="lxml") # soup of current page  
            for i in soup.findAll('article'):
                self.auctioneers_soups.append(i) # extract all auctioneers
                
        # close the window and check soups
        driver.close()
        if len(self.auctioneers_soups)>50:
                print(f'Soup objects of auctioneers successfully downloaded! There are {len(self.auctioneers_soups)} of them right now.')
                
    def get_auction_links_and_categories(self, link):
        '''
        Method that rawls through all pages of auctions and from their source codes then collects link and category of every auction.

        '''

        # initiating the webdriver and opening the link
        driver = webdriver.Chrome('./chromedriver')
        driver.get(link)
        time.sleep(5)

        # getting number of pages from a soup
        html = driver.page_source
        soup = BeautifulSoup(html,features="lxml")
        last_page = int(soup.find('div', {'class': 'el-pagination'}).findAll('li', {'class': 'number'})[
                            -1].text)  # get number of pages

        # getting source codes from all pages and saving as soups
        page_number = driver.find_element_by_css_selector(
            'input[type="number"]')  # locating element into which we write page number
        auctions_pages_soups = []
        for page in tqdm(range(1, last_page + 1)):
            # get to a page
            page_number.send_keys(Keys.BACK_SPACE)
            page_number.send_keys(Keys.BACK_SPACE)
            page_number.send_keys(str(page))
            page_number.send_keys(Keys.RETURN)
            time.sleep(5)
            # save soup object of the page
            html = driver.page_source
            auctions_pages_soups.append(BeautifulSoup(html, features="lxml"))

        for soup in auctions_pages_soups:
            for i in soup.findAll('article'):
                # extracting link
                auction = []
                auction.append(i.find('a')['href'])

                # extracting categories and region
                categ = i.find('tbody').findAll('tr')[1].find('span').text.lstrip('/').split('/')
                auction.append(categ)
                region = i.find("th",string="Okres:").find_next_sibling().text
                auction.append(region)
                
                self.auction_links_and_categories.append(auction)  # saving the data

        # closing the window and checking whether something downloaded
        driver.close()
        if len(self.auction_links_and_categories) > 200:
            print(
                f'Auction links and categories successfully downloaded! There are {len(self.auction_links_and_categories)} auctions right now.')

    def get_items_from_dropdown_menu(self, link):
        '''
        Method that downloads all auctions categories, regions and districts.
        '''

        # initiating the webdriver and opening the link
        driver = webdriver.Chrome('./chromedriver')
        driver.get(link)
        time.sleep(5)

        # saving source code, extracting auction categories
        html = driver.page_source
        soup = BeautifulSoup(html, features="lxml")
        for categ in soup.findAll('ul', {'class': 'el-scrollbar__view el-select-dropdown__list'})[0].findAll('span'):
            self.categories.append(categ.text)

        # extracting regions and districts
        for region in soup.findAll('ul', {'class': 'el-scrollbar__view el-select-dropdown__list'})[1].findAll('ul', {
            'class': 'el-select-group__wrap'}):
            aux = []
            for district in region.findAll('span'):
                aux.append(district.text)
            self.regions_and_districts.append([region.find('li').text, aux])

        # closing the window and checking whether everyhing downloaded
        driver.close()
        if (len(self.categories) > 5) & (len(self.regions_and_districts) == 14):
            print('Auction categories, regions and districts successfully downloaded!')
    def extract_auction_soups(self):
        '''
        Method that extracts soup objects from links provided by get_auction_links_and_categories.
        '''

        if len(self.auction_links_and_categories) > 0:
            for i in tqdm(range(len(self.auction_links_and_categories))):
                req = requests.get(self.auction_links_and_categories[i][0])
                soup = BeautifulSoup(req.text, features="lxml")
                self.auction_links_and_categories[i].append(soup)
            print("Soup objects successfully appended to auction_links_and_categories.")
        else: raise NameError("First, you need to download the links using the method get_auction_links_and_categories!")
