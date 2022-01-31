# Web Scraping Kotlin Tutorial Data from Tutorialspoint

import requests
from bs4 import BeautifulSoup
import pandas as pd

mainURL = "https://www.tutorialspoint.com/kotlin/index.htm"

page = requests.get(mainURL)
htmlContent = page.content
soup = BeautifulSoup(htmlContent, 'html.parser')

urls = []
pages = soup.find('ul', {'class': 'toc chapters'}).findAll(href=True)
for slug in pages:
    urls.append('https://www.tutorialspoint.com' + slug.get('href'))

mainHeadings = []
subHeadingsH2 = []
subHeadingsH3 = []
links = []
imageURLs = []
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
    soup = BeautifulSoup(htmlContent, 'html.parser')

    subContent = soup.find('div', {"class": "tutorial-content"})  # Page Sub Content
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

    link = subContent.findAll('a')  # Page Links
    pageLinks = []
    if link is not None:
        for lin in link:
            if lin.get('href') is not None and not lin.get('href').startswith('http'):
                pageLinks.append('https://www.tutorialspoint.com' + lin.get('href'))
            else:
                pageLinks.append(lin.get('href'))

    images = subContent.findAll('img')  # Images
    pageImageURLs = []
    if images is not None:
        for img in images:
            if img.get('src') is not None and not img.get('src').startswith('http'):
                pageImageURLs.append('https://www.tutorialspoint.com' + img.get('src'))
            else:
                pageImageURLs.append(img.get('src'))

    paragraphs = subContent.findAll('p')  # Paragraphs
    pageFacts = []
    pageDefinitions = []
    pageExplanations = []
    if paragraphs is not None:
        for para in paragraphs:
            slug = para.text.replace('\n', '')
            if 36 <= len(slug) <= 79:
                pageFacts.append(slug)
            elif 80 <= len(slug) <= 119:
                pageDefinitions.append(slug)
            elif 120 <= len(slug):
                pageExplanations.append(slug)

    codeContent = subContent.findAll('pre', not {"class": "result"})  # Codes
    pageCodes = []
    if codeContent is not None:
        for slug in codeContent:
            pageCodes.append(slug.text)

    outputContent = subContent.findAll('pre', {"class": "result"})  # Outputs
    pageOutputs = []
    if outputContent is not None:
        for slug in outputContent:
            pageOutputs.append(slug.text)

    tables = subContent.findAll('table')  # Tables
    pageTableData = []
    if tables is not None:
        for tb in tables:
            table = ""
            rowData = []
            tableRows = tb.findAll('tr')
            for row in tableRows:
                rowData.append(row.text[1:-1].replace('\n', '|||'))
            for row in rowData:
                table = table + str(row) + '&&&'
            pageTableData.append(table[:-3])

    allListUL = subContent.findAll('ul')  # List Items
    allListOL = subContent.findAll('ol')
    listUL = ""
    listOL = ""
    listItem = ""
    pageListItems = []
    if len(allListUL) != 0 or len(allListOL) != 0:
        if len(allListUL) != 0:
            for lis in allListUL:
                listUL = listUL + str(lis.text[1:]).replace('\n', '|||').replace('\t\t', '')
        if len(allListOL) != 0:
            for lis in allListOL:
                listOL = listOL + str(lis.text[1:]).replace('\n', '|||').replace('\t\t', '')
        if len(allListUL) != 0 and len(allListOL) == 0:
            listItem = listItem + listUL
        elif len(allListUL) == 0 and len(allListOL) != 0:
            listItem = listItem + listOL
        else:
            listItem = listItem + listUL + '&&&' + listOL
        pageListItems.append(listItem)

    # print(pageMainHeadings)
    # print(pageSubHeadingsH2)
    # print(pageSubHeadingsH3)
    # print(pageLinks)
    # print(pageImageURLs)
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
    links.append(pageLinks)
    imageURLs.append(pageImageURLs)
    facts.append(pageFacts)
    definitions.append(pageDefinitions)
    explanations.append(pageExplanations)
    codes.append(pageCodes)
    outputs.append(pageOutputs)
    tableData.append(pageTableData)
    listItems.append(pageListItems)


data = {'main_headings': mainHeadings, 'sub_headings_h2': subHeadingsH2, 'sub_headings_h3': subHeadingsH3,
        'links': links, 'image_urls': imageURLs, 'facts': facts, 'definitions': definitions,
        'explanations': explanations, 'codes': codes, 'outputs': outputs, 'table_data': tableData,
        'list_items': listItems}

df = pd.DataFrame(data)
df.to_csv('Tutorialspoint-Kotlin-Data.csv')
