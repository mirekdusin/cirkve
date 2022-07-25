#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import pandas as pd
import requests
from concurrent.futures.thread import ThreadPoolExecutor
from bs4 import BeautifulSoup


def parse_html(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    soup_string = str(soup)

    if (soup_string.find("V systému se vyskytla chyba.") != -1):
        while 1:
            print("chyba")
            time.sleep(20)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            soup_string = str(soup)
            if (soup_string.find("V systému se vyskytla chyba.") == -1):
                break

    if page.status_code != 200:
        while 1:
            print("chyba")
            time.sleep(20)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            soup_string = str(soup)
            if page.status_code == 200:
                if (soup_string.find("V systému se vyskytla chyba.") == -1):
                    break

    content = soup.find("table", {"id": "Table3"})
    trs = content.find_all("tr")

    res = [""] * 11

    for tr in trs:
        tds = tr.find_all("td")
        if (tds[0].text.find("IČO:") != -1):
            try:
                res[0] = tds[1].text
            except IndexError:
                return ["error", url]
        if (tds[0].text.find("Název:") != -1):
            try:
                res[1] = tds[1].text
            except IndexError:
                return ["error", url]
        if (tds[0].text.find("Datum evidence:") != -1):
            try:
                res[2] = tds[1].text
            except IndexError:
                return ["error", url]
        if (tds[0].text.find("Datum registrace:") != -1):
            try:
                res[3] = tds[1].text
            except IndexError:
                return ["error", url]
        if (tds[0].text.find("Sídlo:") != -1):
            try:
                res[4] = tds[2].text
            except IndexError:
                return ["error", url]
        if (tds[0].text.find("Obec:") != -1):
            try:
                res[5] = tds[1].text
            except IndexError:
                return ["error", url]
        if (tds[0].text.find("PSČ:") != -1):
            try:
                res[6] = tds[1].text
            except IndexError:
                return ["error", url]
        if (tds[0].text.find("Zřizovatel:") != -1):
            try:
                res[7] = tds[1].text
            except IndexError:
                return ["error", url]
        if (tds[0].text.find("Předmět obecně") != -1):
            try:
                res[8] = tds[1].text
            except IndexError:
                return ["error", url]
        if (tds[0].text.find("Zánik:") != -1):
            try:
                res[9] = tds[1].text
            except IndexError:
                return ["error", url]
        if (tds[0].text.find("Právní nástupce:") != -1):
            try:
                res[10] = tds[1].text
            except IndexError:
                return ["error", url]

    return res


executor = ThreadPoolExecutor(8)
futures = []

header = ["ICO", "Název", "Datum evidence", "Datum registrace", "Ulice a číslo", "Obec", "PSČ", "zrizovatel",
          "ucel_popis", "Zánik", "Právní nástupce"]

output = [header]
index = 0
with open("urls") as f:
    for line in f:
        if line:
            if ((index != 0) & (index % 100 == 0)):
                print(index)
            result = parse_html(line)
            if (result[0] == "error"):
                print(line)
            else:
                output.append(result)
            index = index + 1

    df = pd.DataFrame(output)
    df.to_excel('output.xlsx', header=False, index=False)
