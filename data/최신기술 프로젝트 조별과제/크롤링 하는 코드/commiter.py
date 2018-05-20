from bs4 import BeautifulSoup
import urllib.request
import re 
import time


# 출력 파일 명i
OUTPUT_FILE_NAME = 'output.txt'
OUTPUT_FILE_NAME1 = 'output1.txt'
OUTPUT_FILE_NAME2 = 'output.txt'

# 긁어 올 URL
URL = 'https://github.com/RelaxedJS/ReLaXed'\

URL1 = URL+'/commits/master'

URL2= 'https://github.com/cdzombak'

a=0
text1 = []


# 크롤링 함수
def get_text(URL):
    source_code_from_URL = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    text = ''
    for item in soup.find_all("a",{"class":"repo js-repo"}):
        text = text + str(item.find_all(text=True))
    return text


def main():
    open_output_file = open(OUTPUT_FILE_NAME, 'w')
    result_text = get_text(URL)
   


    open_output_file.write(result_text)
    #open_output_file.write(result_text2)



		
#open_output_file.close()


if __name__ == '__main__':
    main()
