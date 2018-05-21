from urllib.request import urlopen
import sys
from bs4 import BeautifulSoup
import urllib.request
import re 
import time
set_commiters = set()


OUTPUT_FILE_NAME = 'Repository.txt'
OUTPUT_FILE_NAME1 = 'Commiter.txt'

base_url = "https://github.com/tensorflow/tensorflow"
commits_url = "/commits/master"
URL1 = base_url + '/commits/master'
URL2= 'https://github.com'

plain_text = urlopen(base_url).read()
soup = BeautifulSoup(plain_text, 'html.parser')

def get_topics():
    topics = soup.select("#topics-list-container a")
    text1 = ''
    for topic in topics:
        text1 = text1 + str(topic.text)
        print(topic.text)
    return text1

def get_languages():
    langs = soup.select(".overall-summary.overall-summary-bottomless a .lang")
    text1=''
    for lang in langs:
        text1 = text1+str(lang.text)
        print(lang.text)
    return text1

def get_percentage():
    percentages = soup.select(".overall-summary.overall-summary-bottomless a .percent")
    text1=''
    for percent in percentages:
        text1=text1+str(percent.text)
        print(percent.text)
    return text1



def get_commiters(page):
    plain_text_commits = urlopen(page).read()
    soup_commiter = BeautifulSoup(plain_text_commits, 'html.parser')
    commiters = soup_commiter.select(".AvatarStack.flex-self-start a")
    pages = soup_commiter.select(".paginate-container a")
    for commiter in commiters:
        set_commiters.add(commiter.get("href"))
    return pages[pages.__len__() - 1].get('href')

###################################################3
def get_textt(base_url):
    source_code_from_URL = urllib.request.urlopen(base_url)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    text = ''
    for item in soup.find_all('span',{"class":"Counter"}):
        text = text + str(item.find_all(text=True))
    return text

def get_textt1(base_url):
    source_code_from_URL = urllib.request.urlopen(base_url)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    text = ''
    for item in soup.find_all('span',{"class":"p-nickname vcard-username d-block"}):
        text = text + str(item.find_all(text=True))
    return text

def get_textt2(base_url):
    source_code_from_URL = urllib.request.urlopen(base_url)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    text = ''
    for item in soup.find_all('span',{"class":"p-org"}):
        text = text + str(item.find_all(text=True))
    return text



################################################

get_topics()
get_languages()
get_percentage()

next_page = get_commiters(base_url + commits_url)


open_output_file = open(OUTPUT_FILE_NAME, 'w')
open_output_file1 = open(OUTPUT_FILE_NAME1, 'w')


result_text = get_topics()
result_text1 = get_languages()
result_text2 = get_percentage()
open_output_file.write(result_text)
open_output_file.write(result_text1)
open_output_file.write(result_text2)


for i in range(0,10):
    next_page = get_commiters(next_page)
    print(next_page)

#############################33
sum = 0

#
#def get_text3(URL1):
#    source_code_from_URL = urllib.request.urlopen(URL1)
#    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
#    text = ''
#    for item in soup.find_all("a",{"class":"commit-author tooltipped tooltipped-s user-mention"}):
#       # text = text + str(item.find_all(text=True))
#        text1.append(str(item.find_all(text=True)))
	#print(text[a])
#    return text

text22 = list(set_commiters)
for i in text22:
        #i = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]','',i)
        URL3 = URL2+i
##       URL_.append(URL3)
        print(URL3)
        result_textt = get_textt(URL3)
        open_output_file1.write(result_textt)

        result_textt1 = get_textt1(URL3)
        open_output_file1.write(result_textt1)

        result_textt2 = get_textt2(URL3)
        open_output_file1.write(result_textt2)

       
        sum = sum + 1
        if sum==100:
                #time.sleep(30)
                break;
                sum=0


#print('중복제거한 총 커미터들 : ',set_commiters.__len__(),'명')
#print(set_commiters)
