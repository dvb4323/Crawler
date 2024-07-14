import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class YoutubeSpider(scrapy.Spider):
    name = 'youtube_video'
    start_urls = ['https://www.youtube.com/watch?v=mSLs-gUzDHM']

    def __init__(self, *args, **kwargs):
        super(YoutubeSpider, self).__init__(*args, **kwargs)
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=service, options=options)

    def parse(self, response):
        self.driver.get(response.url)

        # Wait for the title element to be present
        wait = WebDriverWait(self.driver, 10)
        title_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#title .ytd-watch-metadata .ytd-watch-metadata')))

        # Extract the video title
        title = title_element.text
        print(f"Video title: {title}")

        # Get the page source and parse it with Scrapy
        page_source = self.driver.page_source
        response = Selector(text=page_source)

        # Example: extract other information
        #description = response.css('#description::text').extract()
        #print(f"Description: {description}")

        channel_name = response.css('a.yt-simple-endpoint.style-scope.yt-formatted-string::text').get()
        print(f"Channel name: {channel_name}")

        subs = response.css('#owner-sub-count::text').get()
        subs = subs.replace('\xa0', ' ')
        print(f"Video subs: {subs}")

        view_count = response.css('#info > span:nth-child(1)::text').get()
        view_count = view_count.replace('\xa0', ' ')
        print(f"View count: {view_count}")
        # Close the browser
        self.driver.quit()

        # Yield or return the extracted information
        yield {
            'title': title,
            #'description': description,
            'channel_name': channel_name,
            'subs': subs,
            'view_count': view_count
        }
