# Web Scraping Python Tutorial Data from GeeksforGeeks

import requests
from bs4 import BeautifulSoup
import pandas as pd

mainURL = "https://www.geeksforgeeks.org/python-programming-language/?ref=shm"

page = requests.get(mainURL)
htmlContent = page.content
soup = BeautifulSoup(htmlContent, 'html.parser')

urls = []
pages = soup.find('ul', {'class': 'leftBarList'}).findAll(href=True)
for slug in pages[1:]:
    urls.append(slug.get('href'))

mainHeadings = []
subHeadingsH2 = []
subHeadingsH3 = []
imageURLs = []
videoURLs = []
links = []
facts = []
definitions = []
explanations = []
codes = []
outputs = []
listItems = []
tableData = []
data = {}

for url in urls:
    page = requests.get(url)
    htmlContent = page.content
    soup = BeautifulSoup(htmlContent, 'html5lib')

    subContent = soup.find('article', {"class": "content"})  # Page Sub Content
    if subContent is None:
        continue

    mainHeading = subContent.findAll('h1')  # Main Heading
    pageMainHeadings = []
    if mainHeading is not None:
        for head in mainHeading:
            pageMainHeadings.append(head.text)

    subHeadingH2 = subContent.findAll('h2')  # Sub Headings h2
    pageSubHeadingsH2 = []
    if subHeadingH2 is not None:
        for head in subHeadingH2:
            pageSubHeadingsH2.append(head.text)

    subHeadingH3 = subContent.findAll('h3')  # Sub Headings h3
    pageSubHeadingsH3 = []
    if subHeadingH3 is not None:
        for head in subHeadingH3:
            pageSubHeadingsH3.append(head.text)

    images = subContent.findAll('img')  # Images
    pageImageURLs = []
    if images is not None:
        for img in images[:-1]:
            pageImageURLs.append(img.get('src'))

    videos = subContent.findAll('iframe')  # Videos
    pageVideoURLs = []
    if videos is not None:
        for vid in videos:
            pageVideoURLs.append(vid.get('src'))

    link = subContent.findAll('a')  # Page Links
    pageLinks = []
    if link is not None:
        for lin in link:
            if lin.get('href') is not None and not lin.get('href').startswith('http'):
                pageLinks.append('https://www.geeksforgeeks.org/' + lin.get('href'))
            else:
                pageLinks.append(lin.get('href'))

    paragraphs = subContent.findAll('p')  # Paragraphs
    pageFacts = []
    pageDefinitions = []
    pageExplanations = []
    if paragraphs is not None:
        for para in paragraphs:
            slug = para.text.replace('\n', '')
            if 10 <= len(slug) <= 99:
                pageFacts.append(slug)
            elif 100 <= len(slug) <= 399:
                pageDefinitions.append(slug)
            elif 400 <= len(slug):
                pageExplanations.append(slug)

    codeContent = subContent.findAll('div', {"class": "container"})  # Codes
    pageCodes = []
    if codeContent is not None:
        for slug in codeContent:
            pageCodes.append(slug.text.replace('\xa0', ' ').lstrip().rstrip())

    outputContent = subContent.findAll('pre')  # Outputs
    pageOutputs = []
    if outputContent is not None:
        for slug in outputContent:
            if slug.text != '':
                pageOutputs.append(slug.text.lstrip().rstrip())

    tab = subContent.findAll('figure', {"class": "table"})  # Tables
    tables = []
    for t in tab:
        tables.append(t.table)
    pageTableData = []
    if tables is not None:
        for tb in tables:
            final = ''
            for td in tb.findAll('tr'):
                table = ''
                row = ''
                data = td.findAll('td')
                if len(data) != 0:
                    for d in data:
                        row = row + str(d.text) + '|||'
                    table = table + row[:-3:1] + '&&&'
                    final = final + table
            if final != '':
                pageTableData.append(final[:-3:1])

    allListUL = subContent.findAll('ul')[1:]  # List Items
    allListOL = subContent.findAll('ol')
    listItem = ""
    ulListItem = ""
    olListItem = ""
    pageListItems = []
    if len(allListUL) != 0 or len(allListOL) != 0:
        if len(allListUL) != 0:
            ulListItem = ''
            for ulLis in allListUL:
                listUL = ""
                for lis in ulLis.findAll('li'):
                    listUL = listUL + str(lis.text).replace('\xa0', '') + '|||'
                ulListItem = ulListItem + listUL[:-3:1] + '&&&'
        if len(allListOL) != 0:
            olListItem = ''
            for olLis in allListOL:
                listOL = ""
                for lis in olLis.findAll('li'):
                    listOL = listOL + str(lis.text).replace('\xa0', '') + '|||'
                olListItem = olListItem + listOL[:-3:1] + '&&&'
        if len(allListUL) != 0 and len(allListOL) == 0:
            listItem = listItem + ulListItem[:-3:1]
        elif len(allListUL) == 0 and len(allListOL) != 0:
            listItem = listItem + olListItem[:-3:1]
        else:
            listItem = listItem + ulListItem + '&&&' + olListItem
        pageListItems.append(listItem)

    # print(pageMainHeadings)
    # print(pageSubHeadingsH2)
    # print(pageSubHeadingsH3)
    # print(pageImageURLs)
    # print(pageVideoURLs)
    # print(pageLinks)
    # print(pageFacts)
    # print(pageDefinitions)
    # print(pageExplanations)
    # print(pageCodes)
    # print(pageOutputs)
    # print(pageTableData)
    # print(pageListItems)

    mainHeadings.append(pageMainHeadings)
    subHeadingsH2.append(pageSubHeadingsH2)
    subHeadingsH3.append(pageSubHeadingsH3)
    imageURLs.append(pageImageURLs)
    videoURLs.append(pageVideoURLs)
    links.append(pageLinks)
    facts.append(pageFacts)
    definitions.append(pageDefinitions)
    explanations.append(pageExplanations)
    codes.append(pageCodes)
    outputs.append(pageOutputs)
    tableData.append(pageTableData)
    listItems.append(pageListItems)

data = {'main_headings': mainHeadings, 'sub_headings_h2': subHeadingsH2, 'sub_headings_h3': subHeadingsH3,
        'image_urls': imageURLs, 'video_urls': videoURLs, 'links': links, 'facts': facts, 'definitions': definitions,
        'explanations': explanations, 'codes': codes, 'outputs': outputs, 'table_data': tableData,
        'list_items': listItems}

df = pd.DataFrame(data)
df.to_csv('GeeksforGeeks-Python-Data.csv')
