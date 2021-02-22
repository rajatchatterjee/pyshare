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
decompose_classes = [ 'article-tools twitter-icon icons pos1' , 'article-tools facebook-icon icons pos2',
    'article-tools linkedin-icon icons pos3', 'article-sticky-tools save-icon icons pos5' ,'article-tools email-icon icons pos6',
    'article-tools print-icon icons' ,'sponsor-box2'
    ]

file_saving_location = "C:\\Users\\shikha agrawal\\Documents\\PythonNewsMon\\"
file_extension= ".txt"
splitFileArticle="splitArtilceNews"
seperator= "_"

def decompose_unwanted(div_container):
    
    for decompose_tag in decompose_classes:
        for tag in div_container.find_all(class_ = decompose_tag):
            tag.decompose()
    
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
    
def parsehtml(html_page , i):
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
    decompose_unwanted(div_container)
    
    #for s in div_container.find_all('div'):
     #       s.decompose()
    #for s in div_container.find_all('p', class_ = 'sponsor-box2'):
     #       s.decompose()
    #print(div_container)
    try:
        content=div_container.find('span', class_='paywall_content')
        #content = content.find_all('hr')
        tagtoString = str(content)
        splitList  =tagtoString.split("<hr/>")
        if len(splitList) > 1:
   
            
            j = 0
            for art in splitList:
                j = j+1
                soup1 = BeautifulSoup(art , 'html.parser')
                
                
                #print(soup1)
                #print(type(soup1))
                parah_tags = soup1.find_all('p')
                article_text = ''
                for p in parah_tags:
                    article_text = article_text + p.text
                writefile(file_saving_location + splitFileArticle + str(i) + seperator +  str(j) + file_extension,  article_text)
                print('Saved Splitted File As  :' +splitFileArticle + str(i) + str(j) + ".txt"  )
                text = content.find_all(text=True)
        else:
             text = content.find_all(text=True)
            
    except:
        print ('paywall_content not found')
        content=div_container
       
        print(content)
        text = content.find_all(text=True)

    #print (text)
    #set([t.parent.name for t in text])
    
   # rawtext = ''
    #for t in text: rawtext += '{} '.format(t)
    
            
    
    #print(rawtext)
    output = ''
    for t in text:
      #  print(t.parent.name)
       # print(t)
        if t.parent.name in whitelist_tags:
            output += '{} '.format(t)
            #print ('add...' + t.parent.name + '    text-->', t)
        #else:
            #print ('skip...' + t.parent.name + '    text-->', t)
    return output


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
        
        writefile(file_saving_location+"news-html" + str(++i) + file_extension, html_page)
         
        output = parsehtml(html_page , i) 
        
        writefile(file_saving_location+ "news" + str(++i) + file_extension, output)
        print ('---------------------Done-------------------------')

if __name__ == "__main__":
    main()            



 

    
    
    

       
    
    


