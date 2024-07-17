import scrapy
import re
from ..items import BatdongsanItem


class BatdongsanSpiderSpider(scrapy.Spider):
    name = 'batdongsan_spider'
    allowed_domains = ['alonhadat.com.vn']
    start_urls = [
        'https://alonhadat.com.vn/nha-dat/can-ban/nha-dat/ha-noi/704/quan-bac-tu-liem/trang--9.html',
        # 'https://alonhadat.com.vn/nha-dat/can-ban/nha-dat/ha-noi/407/quan-ba-dinh/trang--2.html'
        # 'https://alonhadat.com.vn/nha-dat/can-ban/nha-dat/ha-noi/408/quan-cau-giay.html',
        # 'https://alonhadat.com.vn/nha-dat/can-ban/nha-dat/ha-noi/435/huyen-ung-hoa.html',
        # 'https://alonhadat.com.vn/nha-dat/can-ban/nha-dat/ha-noi/409/quan-dong-da.html',
    ]
    page_number = 10

    def start_requests(self):
        # Read URLs from file
        # with open('urls.txt', 'r') as file:
        #     start_urls = [url.strip() for url in file.readlines()]

        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)
    def parse(self, response):
        items = BatdongsanItem()
        all_items = response.css('.content-item')
        self.crawled_url = response.url
        # Function to extract number
        def extract_number(text):
            if text:
                match = re.search(r'\d+', text)
                if match:
                    return match.group()
            return None
        # Function to reformat price
        def reformat_price(price_str, area_str):
            # Extract numerical value from the 'triệu' price string
            price_match = re.search(r'(\d+)\s*triệu', price_str)
            if price_match:
                price_value = int(price_match.group(1)) * 1e6  # Convert triệu to VND
            else:
                return None

            # Extract numerical value from the area string
            area_match = re.search(r'(\d+(\.\d+)?)\s*m²?', area_str)
            if area_match:
                area_value = float(area_match.group(1))
            else:
                return None

            # Calculate total price
            total_price = price_value * area_value

            # Convert total price to 'tỷ'
            total_price = total_price / 1e9
            total_price = round(total_price, 0)
            total_price_in_ty = str(total_price) + ' tỷ'

            return total_price_in_ty

        for each in all_items:
            title = each.css('.ct_title a::text').extract_first()

            # url extraction
            relative_url = each.css('.ct_title a::attr(href)').get()
            url = response.urljoin(relative_url) if relative_url else None

            # road before width extraction
            road_before_width = each.css('.road-width::text').extract_first()
            road_before_width = str(road_before_width).replace(',', '.')

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
            area_raw = area_raw.replace(',', '.').strip()
            area_raw = area_raw[:-1]
            area = area_raw + "m²"

            # size check
            size = each.css('.ct_kt::text').extract_first()
            size = size.replace(',', '.').strip()

            # direction check
            direction = each.css('.ct_direct::text').extract_first()
            direction = direction.strip()

            # price reformat
            price_raw = each.css('.ct_price::text').extract_first()
            price = re.sub(r'<[^>]+>', '', price_raw).replace(',', '.').strip() if price_raw else None
            if 'triệu' in price and '/' in price:
                price = reformat_price(price_raw, area)
            if 'ngàn' in price:
                price = price.replace('ngàn', 'tỷ')


            # location format
            # Extract the text content of all <a> tags within the div with class ct_dis
            location_parts = each.css('div.ct_dis a::text').getall()
            # Extract the remaining text in the div
            additional_text_chunks = each.css('div.ct_dis::text').getall()
            # Strip and filter out empty strings and redundant commas
            location_parts = [part.strip() for part in location_parts if part.strip()]
            # Split additional text by commas and clean up each chunk
            additional_text = []
            for text in additional_text_chunks:
                for chunk in text.split(','):
                    cleaned_chunk = chunk.strip()
                    if cleaned_chunk:
                        additional_text.append(cleaned_chunk)
            # Combine all parts and filter out any empty or redundant parts
            full_location_list = location_parts + additional_text
            full_location_list = [part for part in full_location_list if part and part != ',']
            # Join the filtered parts into a single string
            location = full_location_list

            items['title'] = title
            items['url'] = url
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

            # Scrap using pagination
            next_page = 'https://alonhadat.com.vn/nha-dat/can-ban/nha-dat/ha-noi/704/quan-bac-tu-liem/trang--' + str(BatdongsanSpiderSpider.page_number) +'.html'
            if BatdongsanSpiderSpider.page_number <= 17:
                BatdongsanSpiderSpider.page_number += 1
                yield response.follow(next_page, callback=self.parse)

            # page_number = response.meta['page_number']
            # base_url = response.meta['base_url']
            # if page_number < 10:
            #     next_page_number = page_number + 1
            #     next_page = f'{base_url.rsplit(".html", 1)[0]}/trang--{next_page_number}.html'
            #     if next_page:
            #         yield response.follow(next_page, callback=self.parse,
            #                               meta={'page_number': next_page_number, 'base_url': base_url})