from pathlib import Path

import scrapy


class BatDongSanHTML(scrapy.Spider):
    name = "amazon_html"

    def start_requests(self):
        urls = [
            "https://amazon.com",

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = f"amazon-structure.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")