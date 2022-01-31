# Web Scraping Java Tutorial Data from Javatpoint

import requests
from bs4 import BeautifulSoup
import pandas as pd

mainURL = "https://www.javatpoint.com/java-tutorial"
urls = []

while mainURL != 'https://www.javatpoint.com/java-runtime-class':
    page = requests.get(mainURL)
    htmlContent = page.content
    soup = BeautifulSoup(htmlContent, 'html.parser')

    mainURL = 'https://www.javatpoint.com/' + str(
        soup.find('div', {'class': 'nexttopicdiv'}).find(href=True).get('href'))
    if mainURL == 'https://www.javatpoint.com/java-string-faqs':
        mainURL = 'https://www.javatpoint.com/java-string-charat'
    urls.append(mainURL)

mainHeadings = []
mainContents = []
links = []
imageURLs = []
videoURLs = []
subHeadingsH2 = []
subHeadingsH3 = []
subHeadingsH4 = []
facts = []
definitions = []
explanations = []
codes = []
outputs = []
tableData = []
listItems = []
data = {}

for url in urls:
    page = requests.get(url)
    htmlContent = page.content
    soup = BeautifulSoup(htmlContent, 'html.parser')

    subContent = soup.find('div', {"id": "city"})  # Sub Content
    if subContent is None:
        continue

    mainHeading = subContent.findAll('h1')  # Main Heading
    pageMainHeadings = []
    if mainHeading is not None:
        for head in mainHeading:
            pageMainHeadings.append(head.text)

    mainContent = subContent.find('p')  # Main Content
    pageMainContents = []
    if mainContent is not None:
        pageMainContents.append(mainContent.text)

    link = subContent.findAll('a')  # Page Links
    pageLinks = []
    if link is not None:
        for lin in link:
            pageLinks.append('https://www.javatpoint.com/' + str(lin.get('href')))

    images = subContent.findAll('img')  # Images
    pageImageURLs = []
    if images is not None:
        for img in images:
            pageImageURLs.append(img.get('src'))

    videos = subContent.findAll('div', {"class": "video-responsive"})  # Video URL
    pageVideoURLs = []
    if videos is not None:
        for vid in videos:
            pageVideoURLs.append(vid.find('iframe').get('src'))

    subHeadingH2 = subContent.findAll('h2', {"class": "h2"})  # Sub Headings h2
    pageSubHeadingsH2 = []
    if subHeadingH2 is not None:
        for head in subHeadingH2:
            pageSubHeadingsH2.append(head.text)

    subHeadingH3 = subContent.findAll('h3')  # Sub Headings h3
    pageSubHeadingsH3 = []
    if subHeadingH3 is not None:
        for head in subHeadingH3:
            pageSubHeadingsH3.append(head.text)

    subHeadingH4 = subContent.findAll('h4')  # Sub Headings h3
    pageSubHeadingsH4 = []
    if subHeadingH4 is not None:
        for head in subHeadingH4:
            pageSubHeadingsH4.append(head.text)

    paragraphs = subContent.findAll('p')  # Paragraphs
    pageFacts = []
    pageDefinitions = []
    pageExplanations = []
    if paragraphs is not None:
        for para in paragraphs[1:]:
            slug = para.text
            if 10 <= len(slug) <= 149:
                pageFacts.append(slug)
            elif 150 <= len(slug) <= 249:
                pageDefinitions.append(slug)
            elif 250 <= len(slug):
                pageExplanations.append(slug)

    codeContent = subContent.findAll('div', {"class": "codeblock"})  # Codes
    pageSnippets = []
    pageCodes = []
    if codeContent is not None:
        for slug in codeContent:
            for cod in slug.text.split('\n'):
                if cod != '' and not cod.lstrip().rstrip().startswith('//') and len(cod) > 7:
                    cod = cod.lstrip().rstrip()
                    pageCodes.append(cod)

    outputContent = subContent.findAll('pre')  # Outputs
    pageOutputs = []
    if outputContent is not None:
        for slug in outputContent:
            for out in slug.text.split('\r\n'):
                if out != '':
                    out = out.lstrip().rstrip()
                    pageOutputs.append(out)

    tables = subContent.findAll('table', {'class': 'alt'})  # Tables
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

    allListUL = subContent.findAll('ul', {"class": "points"})  # List Items
    allListOL = subContent.findAll('ol', {"class": "points"})
    listUL = ""
    listOL = ""
    listItem = ""
    pageListItems = []
    if len(allListUL) != 0 or len(allListOL) != 0:
        if len(allListUL) != 0:
            for lis in allListUL:
                listUL = listUL + str(lis.text).replace('\n', '|||').replace('\t\t', '')
        if len(allListOL) != 0:
            for lis in allListOL:
                listOL = listOL + str(lis.text).replace('\n', '|||').replace('\t\t', '')

        if len(allListUL) != 0 and len(allListOL) == 0:
            listItem = listItem + listUL
        elif len(allListUL) == 0 and len(allListOL) != 0:
            listItem = listItem + listOL
        else:
            listItem = listItem + listUL + '&&&' + listOL
        pageListItems.append(listItem)

    # print(pageMainHeadings)
    # print(pageMainContents)
    # print(pageLinks)
    # print(pageImageURLs)
    # print(pageVideoURLs)
    # print(pageSubHeadingsH2)
    # print(pageSubHeadingsH3)
    # print(pageSubHeadingsH4)
    # print(pageFacts)
    # print(pageDefinitions)
    # print(pageExplanations)
    # print(pageCodes)
    # print(pageOutputs)
    # print(pageTableData)
    # print(pageListItems)

    mainHeadings.append(pageMainHeadings)
    mainContents.append(pageMainContents)
    links.append(pageLinks)
    imageURLs.append(pageImageURLs)
    videoURLs.append(pageVideoURLs)
    subHeadingsH2.append(pageSubHeadingsH2)
    subHeadingsH3.append(pageSubHeadingsH3)
    subHeadingsH4.append(pageSubHeadingsH4)
    facts.append(pageFacts)
    definitions.append(pageDefinitions)
    explanations.append(pageExplanations)
    codes.append(pageCodes)
    outputs.append(pageOutputs)
    listItems.append(pageListItems)
    tableData.append(pageTableData)

data = {'main_headings': mainHeadings, 'main_contents': mainContents, 'links': links, 'image_urls': imageURLs,
        'video_urls': videoURLs, 'sub_headings_h2': subHeadingsH2, 'sub_headings_h3': subHeadingsH3,
        'sub_headings_h4': subHeadingsH4, 'facts': facts, 'definitions': definitions, 'explanations': explanations,
        'codes': codes, 'outputs': outputs, 'table_data': tableData, 'list_items': listItems}

df = pd.DataFrame(data)
df.to_csv('Javatpoint-Java-Data.csv')
