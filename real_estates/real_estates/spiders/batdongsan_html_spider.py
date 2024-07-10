from pathlib import Path

import scrapy


class BatDongSanHTML(scrapy.Spider):
    name = "batdongsan_html"

    def start_requests(self):
        urls = [
            "https://alonhadat.com.vn/nha-dat/can-ban/nha-dat/1/ha-noi.html",

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = f"alonhadat_hanoi-structure.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
