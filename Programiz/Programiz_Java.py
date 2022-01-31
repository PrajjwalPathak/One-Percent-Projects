import requests
from bs4 import BeautifulSoup
import pandas as pd

mainURL = "https://www.programiz.com/java-programming"

page = requests.get(mainURL)
htmlContent = page.content
soup = BeautifulSoup(htmlContent, 'html.parser')

urls = []
pages = soup.find('div', {'class': 'right-bar'}).findAll(href=True)
for slug in pages[:-7]:
    urls.append('https://www.programiz.com' + slug.get('href'))

mainHeadings = []
mainContents = []
videoHeadings = []
videoURLs = []
subHeadingsH2 = []
subHeadingsH3 = []
imageURLs = []
facts = []
definitions = []
explanations = []
codes = []
snippets = []
outputs = []
tableData = []
listItems = []
data = {}

for url in urls:
    page = requests.get(url)
    htmlContent = page.content
    soup = BeautifulSoup(htmlContent, 'html.parser')

    mainHeading = soup.findAll('h1')  # Main Heading
    pageMainHeadings = []
    if mainHeading is not None:
        for head in mainHeading:
            pageMainHeadings.append(head.text)

    mainContent = soup.findAll('p', {"class": "editor-contents__short-description"})  # Main Content
    pageMainContents = []
    if mainContent is not None:
        for mainCon in mainContent:
            pageMainContents.append(mainCon.text)

    videoHeading = soup.findAll('div', {"class": "programiz-youtube-wrapper lite-youtube"})  # Video Heading
    pageVideoHeadings = []
    if videoHeading is not None:
        for vidHead in videoHeading:
            pageVideoHeadings.append(vidHead.find('h2').text)

    videoURL = soup.findAll('div', {"class": "programiz-youtube__container"})  # Video URL
    pageVideoURLs = []
    if videoURL is not None:
        for vid in videoURL:
            pageVideoURLs.append(vid.find('iframe').get('src'))

    subContent = soup.find('div', {"class": "content"})  # Sub Content
    if subContent is None:
        continue

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
        for img in images:
            pageImageURLs.append(img.get('src'))

    paragraphs = subContent.findAll('p')  # Paragraphs
    pageFacts = []
    pageDefinitions = []
    pageExplanations = []
    if paragraphs is not None:
        for para in paragraphs:
            slug = para.text
            if 5 <= len(slug) <= 65:
                pageFacts.append(slug)
            elif 66 <= len(slug) <= 126:
                pageDefinitions.append(slug)
            elif 127 < len(slug):
                pageExplanations.append(slug)

    codeContent = subContent.findAll('pre')  # Codes, Snippets and Outputs
    pageCodes = []
    pageSnippets = []
    pageOutputs = []
    for slug in codeContent:
        if slug.code is not None:
            for cod in slug.code.text.split('\n'):
                if cod != '' and not cod.lstrip().rstrip().startswith('//'):
                    if 7 < len(cod) <= 30:
                        pageSnippets.append(cod)
                    elif 31 < len(cod):
                        pageCodes.append(cod)

        else:
            for out in slug.text.split('\n'):
                if out != '' and not out.lstrip().rstrip().startswith('//'):
                    pageOutputs.append(out)
                else:
                    continue

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


    mainHeadings.append(pageMainHeadings)
    mainContents.append(pageMainContents)
    videoHeadings.append(pageVideoHeadings)
    videoURLs.append(pageVideoURLs)
    subHeadingsH2.append(pageSubHeadingsH2)
    subHeadingsH3.append(pageSubHeadingsH3)
    imageURLs.append(pageImageURLs)
    facts.append(pageFacts)
    definitions.append(pageDefinitions)
    explanations.append(pageExplanations)
    snippets.append(pageSnippets)
    codes.append(pageCodes)
    outputs.append(pageOutputs)
    tableData.append(pageTableData)
    listItems.append(pageListItems)

data = {'main_headings': mainHeadings, 'main_contents': mainContents, 'video_headings': videoHeadings,
        'video_urls': videoURLs, 'sub_headings_h2': subHeadingsH2, 'sub_headings_h3': subHeadingsH3,
        'image_urls': imageURLs, 'facts': facts, 'definitions': definitions, 'explanations': explanations,
        'snippets': snippets, 'codes': codes, 'outputs': outputs, 'table_data': tableData, 'list_items': listItems}

df = pd.DataFrame(data)
df.to_csv('Programiz_Java.csv')