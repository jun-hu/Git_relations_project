import re
 
# 입,출력 파일명
INPUT_FILE_NAME = 'output1.txt'
OUTPUT_FILE_NAME = 'output_cleand1.txt'
 

INPUT_FILE_NAME1 = 'output2.txt'
OUTPUT_FILE_NAME1 = 'output_cleand2.txt'

# 클리닝 함수
def clean_text(text):
    cleaned_text = re.sub('   ', '', text)
    cleaned_text = re.sub('[n]', '', text)
    cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$&\\\=\(\'\"]',
                          '', cleaned_text)
    return cleaned_text
    
 
# 메인 함수
def main():
    read_file = open(INPUT_FILE_NAME, 'r')
    write_file = open(OUTPUT_FILE_NAME, 'w')
    text = read_file.read()
    text = clean_text(text)

    read_file1 = open(INPUT_FILE_NAME1, 'r')
    write_file1 = open(OUTPUT_FILE_NAME1, 'w')
    text1 = read_file1.read()
    text1 = clean_text(text1)
    write_file1.write(text1)

    write_file.write(text)
    read_file.close()
    write_file.close()
 
 
if __name__ == "__main__":
    main()


