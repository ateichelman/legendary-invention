from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# from selenium.webdriver.chrome.options import Options

# Testing selenium browser automation
def main():
    # chrome_options = Options()
    # chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome("./chromedriver")
    driver.get("https://www.python.org")
    print(driver.title)
    search_bar = driver.find_element_by_name("q")
    search_bar.clear()
    search_bar.send_keys("getting started with python")
    search_bar.send_keys(Keys.RETURN)
    print(driver.current_url)
    while True:
        pass
        # driver.close()

if __name__ == "__main__":
    main()