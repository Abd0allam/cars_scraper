import json
import re
from django.core.management.base import BaseCommand
from cards.models import UsedCars, NewdCars
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

class Command(BaseCommand):
    help = 'Scrapes car data from syarah.com and saves it to the database'

    def handle(self, *args, **options):
        # Scrape used cars data
        used_car_data = self.scrape_used_cars()
        # Save used car data to the database
        for data in used_car_data:
            used_car = UsedCars.objects.create(
                name=data['name'],
                price=data['price'],
                image_url=data['image_url'],
                odo=data['odo']
            )
            used_car.save()

        # Scrape new cars data
        new_car_data = self.scrape_new_cars()
        # Save new car data to the database
        for data in new_car_data:
            new_car = NewdCars.objects.create(
                name=data['name'],
                price=data['price'],
                image_url=data['image_url']
            )
            new_car.save()

    def scrape_used_cars(self):
        driver = webdriver.Firefox()
        wait = WebDriverWait(driver, 20)

        # Navigate to the website
        driver.get('https://syarah.com')

        # Find the menu icon and click on it
        menu = driver.find_element(By.CSS_SELECTOR, '.Header-module__MenuIcnSizeRev.hasEvents')
        menu.click()

        # Click on the 'English' link
        lang = driver.find_element(By.CLASS_NAME, 'langSwitch')
        lang.click()


        # Click on the find all cars
        target_element_xpath = '/html/body/div[1]/div[1]/main/div[1]/div[2]/div/div/a'
        target_element = wait.until(EC.element_to_be_clickable((By.XPATH, target_element_xpath)))
        target_element.click()

        # Wait for the page to load
        time.sleep(5)

        # Scroll the page step by step for 5 seconds
        start_time = time.time()
        while time.time() - start_time < 5:
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)

        # Find all elements with class name 'SearchCard-module__card'
        cars = driver.find_elements(By.CLASS_NAME, 'SearchCard-module__card')

        car_data = []
        for card in cars:
            # Find the element with class name 'SearchCard-module__title' and extract the car name
            car_name_element = card.find_element(By.CLASS_NAME, "SearchCard-module__title")
            car_name = car_name_element.get_attribute("innerHTML").strip()

            # Find the element with class name 'SearchCard-module__beforeDiscount' and extract the car price

            car_price_element = card.find_element(By.CLASS_NAME, "SearchCard-module__beforeDiscount")
            car_price_html = car_price_element.get_attribute("innerHTML").strip()

            # Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(car_price_html, 'html.parser')

            # Find the <strong> tag and extract its contents
            strong_tag = soup.find('strong')
            car_price = strong_tag.text.strip()
            car_price = car_price.replace(',', '')

            # Find the img tag with alt="car" and extract the image URL
            img_element = card.find_element(By.CSS_SELECTOR, 'img[alt="car"]')
            img_url = img_element.get_attribute("src")

            # Find the span element inside div with class 'SearchCard-module__tag' and extract the ODO value
            # Find the element with class name 'SearchCard-module__bottomSection'
            bottom_section_element = card.find_element(By.CLASS_NAME, 'SearchCard-module__bottomSection')

            # Find the second 'div' element inside 'SearchCard-module__bottomSection'
            second_div_element = bottom_section_element.find_elements(By.TAG_NAME, 'div')[1]

            # Find the 'span' element inside the second 'div' element
            span_element = second_div_element.find_element(By.TAG_NAME, 'span')

            # Get the inner text of the 'span' element
            odo = span_element.get_attribute('innerHTML')
            odo = re.sub('[^0-9]', '', odo)

            data = {
                'name': car_name,
                'price': car_price,
                'image_url': img_url,
                'odo': odo
            }
            
            car_data.append(data)

        driver.quit()
        

        return car_data

    def scrape_new_cars(self):
        # Create a new Firefox browser instance and set a wait time for 10 seconds
        driver = webdriver.Firefox()
        wait = WebDriverWait(driver, 10)

        # Navigate to the website
        driver.get('https://syarah.com/en/new-cars')

        # Find the 'New' tab and click on it
        new_cars = driver.find_element(By.ID, 'QA_Auto_NewTab')
        new_cars.click()

        # Click on the 'Browse All New Cars' link
        driver.find_element(By.LINK_TEXT, "Browse All New Cars").click()

        # Wait for the page to load
        time.sleep(10)

        # Set the start time
        start_time = time.time()

        # Scroll the page step by step for 5 seconds
        while time.time() - start_time < 5:
            # Scroll the page down by a certain amount
            driver.execute_script("window.scrollBy(0, 500);")
            # Wait for a short period before scrolling again
            time.sleep(1)

        # Find the elements with class name 'SearchCard-module__card'
        cards = driver.find_elements(By.CLASS_NAME, 'SearchCard-module__card')

        # Create an empty list to store the data for each car
        car_data = []

        # Loop through the cards and extract the data for each car
        for card in cards:

            # Extract the car name
            car_name_element = card.find_element(By.CLASS_NAME, 'SearchCard-module__title')
            car_name = car_name_element.get_attribute("innerHTML").strip()

            # Extract the car price
            car_price_element = card.find_element(By.CLASS_NAME, "SearchCard-module__beforeDiscount")
            car_price_html = car_price_element.get_attribute("innerHTML").strip()
            # Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(car_price_html, 'html.parser')
            # Find the <strong> tag and extract its contents
            strong_tag = soup.find('strong')
            car_price = strong_tag.text.strip()
            car_price = car_price.replace(',', '')


            # Find the img tag with alt="car" and extract the image URL
            img_element = card.find_element(By.CSS_SELECTOR, 'img[alt="car"]')
            img_url = img_element.get_attribute("src")


            data = {
                'name': car_name,
                'price': car_price,
                'image_url': img_url,
            }
            
            car_data.append(data)

        # Close the browser window
        driver.quit()

        # Return the car data list
        return car_data
    
