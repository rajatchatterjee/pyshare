# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#!pip install feedparser



import feedparser
import requests
from bs4 import BeautifulSoup

blacklist_tags = [
    '[document]','noscript','header',
    'html','meta','head', 'input','script',
    # there may be more elements you don't want, such as "style", etc.
    ]
    
whitelist_tags = [
    'p', 'strong', 'div', 'span'
    # there may be more elements you such as "style", etc.
    ]


def parserssentry(entry):
    '''
    Returns and title and link from rss entry

    Parameters
    ----------
    entry : TYPE
        DESCRIPTION.

    Returns
    -------
    title : TYPE
        DESCRIPTION.
    link : TYPE
        DESCRIPTION.

    '''
    
    
    title = entry.title
    link = entry.link
    return title, link

def gethtml(link):
    '''
    Retutns the htmnl content from a link

    Parameters
    ----------
    link : TYPE
        DESCRIPTION.

    Returns
    -------
    html_page : TYPE
        DESCRIPTION.

    '''
    res = requests.get(link)
    html_page = res.content
    return html_page

def writefile(filename, content):
    '''
    Write a file with given contents

    Parameters
    ----------
    filename : TYPE
        DESCRIPTION.
    content : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    f = open(filename, "w",  encoding="utf-8")
    f.write(str(content))
    print('written -->'+  filename)
    f.close()
    
def parsehtml(html_page):
    '''
    Custom fn to extarct data from html page: WIP

    Parameters
    ----------
    html_page : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    soup = BeautifulSoup(html_page, 'html.parser')
    
    div_container = soup.find('div', class_ = 'article-page-body-content')
    
    #print(div_container)
    try:
        content=div_container.find('span', class_='paywall_content')
        #print(content)
        text = content.find_all(text=True)
    except:
        print ('paywall_content not found')
        content=div_container
        #print(content)
        text = content.find_all(text=True)

    #print (text)
    #set([t.parent.name for t in text])
    
    rawtext = ''
    for t in text: rawtext += '{} '.format(t)
            
    
    #print(text)
    output = ''
    for t in text:
        #print(t.parent.name)
        #print(t)
        if t.parent.name in whitelist_tags:
            output += '{} '.format(t)
            #print ('add...' + t.parent.name + '    text-->', t)
        #else:
            #print ('skip...' + t.parent.name + '    text-->', t)


def main():
    '''
    Main function

    Returns
    -------
    None.

    '''
    NewsFeed = feedparser.parse("https://www.risk.net/feeds/rss/category/people")
    i=0
    for entry in NewsFeed.entries:
        i+=1
        print ("Processing " + str(i) + "  :----------------------------------")
        title,link = parserssentry(entry)
        print (title)
        print (link)
        html_page = gethtml(link)
        #print(html_page)
    
        output = parsehtml(html_page) 
        
        writefile("news" + str(++i) + ".txt", output)
        print ('---------------------Done-------------------------')

if __name__ == "__main__":
    main()            



 

    
    
    

       
    
    



