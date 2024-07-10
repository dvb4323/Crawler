import scrapy

class WebsiteScraper(scrapy.Spider):
  name = "youtube_scraper"

  def start_requests(self):
    # Replace 'https://www.example.com' with the actual website URL
    url = 'https://www.youtube.com'
    yield scrapy.Request(url, callback=self.parse_website)

  def parse_website(self, response):
    filename = 'youtube.html'
    with open(filename, 'wb') as f:
      # Directly write the response body to the file
      f.write(response.body)
    self.log(f"Website HTML saved to {filename}")


