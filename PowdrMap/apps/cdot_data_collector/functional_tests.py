from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000/cdot_hw_data')

assert 'Mountain Crowd Estimates' in browser.title
