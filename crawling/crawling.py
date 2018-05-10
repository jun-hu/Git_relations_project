from bs4 import BeautifulSoup
import urllib.request
import re 
import time


# 출력 파일 명i
OUTPUT_FILE_NAME = 'output.txt'
OUTPUT_FILE_NAME1 = 'output1.txt'
OUTPUT_FILE_NAME2 = 'output.txt'

# 긁어 올 URL
URL = 'https://github.com/RelaxedJS/ReLaXed'\ # 깃터브 유저의  URL

URL1 = URL+'/commits/master' # 깃터브 유저의 레저피토리 URL

URL2= 'https://github.com/' # 깃터브의 URL

a=0
text1 = []


# 크롤링 함수
def get_text(URL): # 레퍼지토리의 토픽 키워트를 뽑아내는 함수
    source_code_from_URL = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    text = ''
    for item in soup.find_all("div",{"class":"list-topics-container f6 mt-1"}):
        text = text + str(item.find_all(text=True))
    return text


def get_text1(URL): # # 레퍼지토리의 프로그래밍 언어 사용 비율 함수
    source_code_from_URL = urllib.request.urlopen(URL) 
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    text = ''
    for item in soup.find_all("div",{"class":"repository-lang-stats"}):
        text = text + str(item.find_all(text=True))
    return text
 

def get_text2(URL1): # 레퍼지토리의 커밋으로 들어가서 커밋터들의 정보를 뽑아오는 함수
    source_code_from_URL = urllib.request.urlopen(URL1) 
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    text = ''
    for item in soup.find_all("a",{"class":"commit-author tooltipped tooltipped-s user-mention"}):
        text = text + str(item.find_all(text=True))
    return text


def get_text3(URL1): # 레퍼지토리의 커밋으로 들어가서 커밋터들의 정보를 뽑아오는 함수를 list에 적재
    source_code_from_URL = urllib.request.urlopen(URL1)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    text = ''
    for item in soup.find_all("a",{"class":"commit-author tooltipped tooltipped-s user-mention"}):
       # text = text + str(item.find_all(text=True))
        text1.append(str(item.find_all(text=True)))
	#print(text[a])
    return text

get_text3(URL1)
#####################################33
#print(text1)

##########################


def get_textt(URL): # 레포지토리 갯수를 뽑아내는 함수
    source_code_from_URL = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    text = ''
    for item in soup.find_all('span',{"class":"Counter"}):
        text = text + str(item.find_all(text=True))
    return text

def get_textt1(URL): # 커밋터의 아이디를 뽑아내는 함수
    source_code_from_URL = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    text = ''
    for item in soup.find_all('span',{"class":"p-nickname vcard-username d-block"}):
        text = text + str(item.find_all(text=True))
    return text

def get_textt2(URL):
    source_code_from_URL = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    text = ''
    for item in soup.find_all('span',{"class":"p-org"}):
        text = text + str(item.find_all(text=True))
    return text


def get_textt3(URL): # 커밋터의 사는 지역을 뽑아내는 함수
    source_code_from_URL = urllib.request.urlopen(URL) 
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    text = ''
    for item in soup.find_all('span',{"class":"p-label"}):
        text = text + str(item.find_all(text=True))
    return text


####################################

URL_ = []
open_output_file = open(OUTPUT_FILE_NAME, 'w')

#for i in text1:
#	i = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]','',i)
#	URL3 = URL2+i
#	URL_.append(URL3)
#	print(URL3)
#	result_textt = get_textt(URL3)
#	open_output_file.write(result_textt)
#
#	result_textt1 = get_textt1(URL3)
#        open_output_file.write(result_textt1)
#
#	result_textt2 = get_textt2(URL3)
#        open_output_file.write(result_textt2)
#
#	result_textt3 = get_textt3(URL3)
#       open_output_file.write(result_textt3)



	

#print(URL_)
#open_output_file.close()

#############################3

# 메인 함수
def main():
#    open_output_file = open(OUTPUT_FILE_NAME, 'w')
    result_text = get_text(URL)
    result_text1 = get_text1(URL)
    #result_text2 = get_text2(URL1)


    open_output_file.write(result_text)
    open_output_file.write(result_text1)
    #open_output_file.write(result_text2)
sum = 0


		
#open_output_file.close()


for i in text1:  # 커밋터들의 정보를 하나씩 파고들어가서 커밋터의 정보를 뽑아내는 for
        i = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]','',i)
        URL3 = URL2+i
##       URL_.append(URL3)
        print(URL3)
        result_textt = get_textt(URL3)
        open_output_file.write(result_textt)

        result_textt1 = get_textt1(URL3)
        open_output_file.write(result_textt1)

        result_textt2 = get_textt2(URL3)
        open_output_file.write(result_textt2)

        result_textt3 = get_textt3(URL3)
        open_output_file.write(result_textt3)
	
        sum = sum + 1
        if sum==10:
                time.sleep(20)
                sum=0

if __name__ == '__main__':
    main()
