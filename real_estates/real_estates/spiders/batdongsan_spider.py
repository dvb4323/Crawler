import scrapy
import re
import json


class RealEstateSpider(scrapy.Spider):
    name = "realestate"
    allowed_domains = ["alonhadat.com.vn"]
    start_urls = [
        'https://alonhadat.com.vn/nha-dat/can-ban/nha-dat/1/ha-noi.html'
    ]

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'scraped_data.json'  # Specify the file path where you want to store the JSON data
    }

    def parse(self, response):
        for property in response.css('div.content-item'):
            title = property.css('div.ct_title a::text').get()
            url = response.urljoin(property.css('div.ct_title a::attr(href)').get())
            area_raw = property.css('div.ct_dt').get()  # Change the selector here
            area_match = re.search(r'<label>Diện tích:</label>\s*([\d.,]+)\s*m<sup>2</sup>', area_raw, re.IGNORECASE)
            area = area_match.group(1).strip() + " m²" if area_match else None
            price_raw = property.css('div.ct_price').get()
            price = re.sub(r'<[^>]+>', '', price_raw).strip() if price_raw else None
            location = ', '.join(property.css('div.ct_dis a::text').getall())

            yield {
                'title': title,
                'url': url,
                'area': area,
                'price': price,
                'location': location
            }

        # Follow pagination links if available
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def closed(spider, reason):
        # Post-processing to clean up the JSON file
        print("Closing spider and formatting JSON data...")
        with open('scraped_data.json', 'r') as f:
            data = json.load(f)

        # Write back the data with proper indentation and sorting
        with open('scraped_data.json', 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=True)
