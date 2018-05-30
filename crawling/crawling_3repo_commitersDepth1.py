from urllib.request import urlopen
import sys
import time
import json
from bs4 import BeautifulSoup
start_time = time.time()
base_url = "https://github.com"

set_repos = set()
set_repos.add("meteor/meteor")
set_repos.add("opencv/opencv")
set_repos.add("tensorflow/tensorflow")

outputDict = {}
outputDict['trending'] = ""
outputDict['reposWhatiSelect'] = {}

def get_topics():
    topicArr = []
    topics = soup.select("#topics-list-container a")
    for topic in topics:
        print(topic.text.strip())
        topicArr.append(topic.text.strip())
    return topicArr

def get_languages():
    lang_percentage_dict = {}
    langs = soup.select(".overall-summary.overall-summary-bottomless a .lang")
    percentages = soup.select(".overall-summary.overall-summary-bottomless a .percent")
    count = 0
    for lang in langs:
        print(lang.text)
        lang_percentage_dict[lang.text] = percentages[count].text
        count += 1
    return lang_percentage_dict

def get_commiters(page):
    plain_text_commits = urlopen(page).read()
    soup_commiter = BeautifulSoup(plain_text_commits, 'html.parser')
    commiters = soup_commiter.select(".AvatarStack.flex-self-start a")
    pages = soup_commiter.select(".paginate-container a")
    for commiter in commiters:
        set_commiters.add(commiter.get("href")[1:])
    if pages.__len__() == 0:    return "null"
    if pages[pages.__len__() - 1].text == "Newer":
        return "null"
    return pages[pages.__len__() - 1].get('href')


def get_name():
    name = soup.select_one("span.p-name.vcard-fullname.d-block.overflow-hidden").text
    return name


def get_id():
    id = soup.select_one("span.p-nickname.vcard-username.d-block").text
    return id


def get_location():
    if not soup.select_one(".p-label") == None:
        location = soup.select_one(".p-label").text
        return location
    else:
        return ""

def get_followers(page):
    followers_plain_text = urlopen(page).read()
    followers_soup = BeautifulSoup(followers_plain_text, 'html.parser')
    followers = followers_soup.select(".d-inline-block.no-underline.mb-1")
    pages = followers_soup.select(".pagination a")
    for follower in followers:
        set_followers.add(follower.get("href")[1:])
    if pages.__len__() == 0:    return "null"
    if pages[pages.__len__() - 1].text == "Previous":
        return "null"
    return pages[pages.__len__() - 1].get('href')

def get_following(page):
    following_plain_text = urlopen(page).read()
    following_soup = BeautifulSoup(following_plain_text, 'html.parser')
    followings = following_soup.select(".d-inline-block.no-underline.mb-1")
    pages = following_soup.select(".pagination a")
    for following in followings:
        set_following.add(following.get('href')[1:])
    if pages.__len__() == 0:    return "null"
    if pages[pages.__len__() - 1].text == "Previous" or len(pages) == 0:
        return "null"
    return pages[pages.__len__() - 1].get('href')

for repo in set_repos:
    set_commiters = set()
    set_followers = set()
    set_following = set()
    repoinfo = {}
    repo_url = base_url + "/" + repo
    commits_url = "/commits/master"
    plain_text = urlopen(repo_url).read()
    soup = BeautifulSoup(plain_text, 'html.parser')

    repoinfo['topic'] = get_topics()
    repoinfo['language'] = get_languages()

    next_page = get_commiters(repo_url + commits_url)
    for i in range(0, 10):
        if (next_page == "null"): break
        next_page = get_commiters(next_page)

    print('중복제거한 총 커미터들 : ', set_commiters.__len__(), '명')
    print(set_commiters)

    commiters_array = []
    for commiter in set_commiters:
        print(commiter)
        commiter_dict = {}
        plain_text = urlopen(base_url + "/" + commiter).read()
        soup = BeautifulSoup(plain_text, 'html.parser')

        commiter_dict['id'] = get_id()
        commiter_dict['name'] = get_name()
        commiter_dict['location'] = get_location()

        # store followers
        followers_url = "?tab=followers"
        next_page = get_followers(base_url + "/" + commiter + followers_url)
        for i in range(0, 10):
            if (next_page == "null"): break
            next_page = get_followers(next_page)
        commiter_dict['followers'] = list(set_followers)
        set_followers.clear()

        # store followings
        following_url = "?tab=following"
        next_page = get_following(base_url + "/" + commiter + following_url)
        for j in range(0, 10):
            if (next_page == "null"): break
            next_page = get_following(next_page)
        commiter_dict['following'] = list(set_following)
        set_following.clear()

        commiters_array.append(commiter_dict)

    repoinfo['commiters'] = commiters_array
    print(repoinfo)
    outputDict['reposWhatiSelect'][repo] = repoinfo

    print("start_time", start_time) #출력해보면, 시간형식이 사람이 읽기 힘든 일련번호형식입니다.
    print("--- %s seconds ---" %(time.time() - start_time))

# outputJson = json.dumps(outputDict, indent=2)

with open('outputjson.json', 'w') as outfile:
    json.dump(outputDict, outfile)