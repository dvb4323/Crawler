import scrapy
import re
from ..items import BatdongsanItem


class BatdongsanSpiderSpider(scrapy.Spider):
    name = "batdongsan_spider"
    allowed_domains = ["alonhadat.com.vn"]
    start_urls = ["https://alonhadat.com.vn/nha-dat/can-ban/nha-dat/ha-noi/407/quan-ba-dinh.html#"]

    def parse(self, response):
        items = BatdongsanItem()
        all_items = response.css('.content-item')

        # Function to extract number
        def extract_number(text):
            if text:
                match = re.search(r'\d+', text)
                if match:
                    return match.group()
            return None

        for each in all_items:
            title = each.css('.vip::text').extract_first()
            road_before_width = each.css('.road-width::text').extract_first()

            # floors and bedrooms reformat
            floors = each.css('.floors::text').extract_first()
            floors = extract_number(floors)

            bedrooms = each.css('.bedroom::text').extract_first()
            bedrooms = extract_number(bedrooms)

            # parking check
            parking_avail = each.css('.parking::text').extract_first()
            parking = bool(parking_avail)

            # area reformat
            area_raw = each.css('.ct_dt::text').extract_first()
            area_raw = area_raw.strip()
            area_raw = area_raw[:-1]
            area = area_raw + "m²"

            # size check
            size = each.css('.ct_kt::text').extract_first()
            size = size.strip()

            # direction check
            direction = each.css('.ct_direct::text').extract_first()
            direction = direction.strip()

            # price reformat
            price_raw = each.css('.ct_price::text').extract_first()
            price = re.sub(r'<[^>]+>', '', price_raw).strip() if price_raw else None

            # location format
            location = ', '.join(each.css('div.ct_dis a::text').getall())

            items['title'] = title
            items['road_before_width'] = road_before_width
            items['floors'] = floors
            items['bedrooms'] = bedrooms
            items['parking'] = parking
            items['area'] = area
            items['size'] = size
            items['direction'] = direction
            items['price'] = price
            items['location'] = location
            yield items
