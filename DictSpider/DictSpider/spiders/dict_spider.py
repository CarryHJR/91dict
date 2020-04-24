#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright ¬© 2020 carry <carry@CarrHJRs-MBP.local>
#
# Distributed under terms of the MIT license.

"""
spider for 91dict
scrapy runspider test_91dictSpider.py
"""

import scrapy
from bs4 import BeautifulSoup
from DictSpider.items import DictspiderItem


class DictSpider(scrapy.Spider):
    def start_requests(self):
        file_name = "../allWords.json"
        with open(file_name, 'r', encoding='utf-8') as f:
            step = 0
            for line in f:
                step = step + 1
                #  if (step == 5):
                #      break
                word = line.strip()
                url = 'http://www.91dict.com/words?w=' + word
                yield scrapy.Request(url=url, callback=self.parse)

    name = "91dict"

    def parse(self, response):
        soup = BeautifulSoup(response.body, features="lxml")
        tmp = soup.find_all(id="flexslider_2")[0].find_all("ul")[0].find_all("li")
        word = response.request.url.split("?w=")[-1]
        results = []
        for x in tmp:
            item = DictspiderItem()
            imgMainbox = x.find(class_="imgMainbox")
            img_src = imgMainbox.find("img")["src"]
            audio_src = imgMainbox.find("audio")["src"]
            sentence = imgMainbox.find(class_="mBottom").text.strip()
            item['word'] = word
            item['sentence'] = sentence
            item['file_urls'] = [img_src, audio_src]
            yield item

