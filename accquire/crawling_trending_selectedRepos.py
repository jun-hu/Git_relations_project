# -*- coding: utf-8 -*-
from urllib.request import urlopen
import sys
import time
import json
from bs4 import BeautifulSoup
import pickle

pageNum = 5
start_time = time.time()
base_url = "https://github.com"
followers_url = "?tab=followers"
following_url = "?tab=following"
ownRepo_url = "?tab=repositories"

set_trending = set()
set_selected_repos = set()

# set_trending.add("danistefanovic/build-your-own-x")
# set_trending.add("trekhleb/javascript-algorithms")
# set_trending.add("xingshaocheng/architect-awesome")
# set_trending.add("ry/deno")
# set_trending.add("klauscfhq/signale")
# set_trending.add("wiredjs/wired-elements")
# set_trending.add("senorprogrammer/wtf")
# set_trending.add("RelaxedJS/ReLaXed")
# set_trending.add("CyC2018/Interview-Notebook")
# set_trending.add("olistic/warriorjs")
# set_trending.add("iamkun/dayjs")
# set_trending.add("flutter/flutter")
# set_trending.add("Microsoft/vscode")
# set_trending.add("anordal/shellharden")
# set_trending.add("isomorphic-git/isomorphic-git")
# set_trending.add("tensorflow/models")
# set_trending.add("dotnet/machinelearning")
# set_trending.add("guess-js/guess")
# set_trending.add("GetStream/Winds")
# set_trending.add("sindresorhus/awesome")

set_selected_repos.add("meteor/meteor")
set_selected_repos.add("opencv/opencv")
set_selected_repos.add("tensorflow/tensorflow")
set_selected_repos.add("vuejs/vue")
set_selected_repos.add("d3/d3")
set_selected_repos.add("nodejs/node")
set_selected_repos.add("freeCodeCamp/freeCodeCamp")
set_selected_repos.add("facebook/react")
set_selected_repos.add("twbs/bootstrap")

outputDict = {}
outputDict['trending'] = {}
outputDict['selectedRepo'] = {}

set_commiters = set()

def get_trendingList():
    trendingUrl = "https://github.com/trending?since=monthly"
    plain_text = urlopen(trendingUrl).read()
    soup = BeautifulSoup(plain_text, 'html.parser')
    hrefs = soup.select(".repo-list li > div > h3 > a")
    for href in hrefs:
        print(href.get("href")[1:])
        set_trending.add(href.get("href"))
    with open('trending.txt', 'wb') as outfile:
        pickle.dump(list(set_trending), outfile)


def get_topics(soup):
    topicArr = []
    topics = soup.select("#topics-list-container a")
    for topic in topics:
        # print(topic.text.strip())
        topicArr.append(topic.text.strip())
    return topicArr


def get_languages(soup):
    lang_percentage_dict = {}
    langs = soup.select(".overall-summary.overall-summary-bottomless a .lang")
    percentages = soup.select(".overall-summary.overall-summary-bottomless a .percent")
    count = 0
    for lang in langs:
        # print(lang.text)
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


def get_name(soup):
    name = soup.select_one("span.p-name.vcard-fullname.d-block.overflow-hidden").text
    return name


def get_id(soup):
    id = soup.select_one("span.p-nickname.vcard-username.d-block").text
    return id


def get_location(soup):
    if not soup.select_one(".p-label") == None:
        location = soup.select_one(".p-label").text
        return location
    else:
        return ""

def get_forkedRepos(reposUrl):
    forkedRopoInfoObject = []
    plain_text = urlopen(reposUrl).read()
    soup = BeautifulSoup(plain_text, 'html.parser')
    forkedRepos = soup.select(".fork span .muted-link")

    for forkedRepo in forkedRepos:
        repoName = forkedRepo.get("href")
        # print("current forked repo :", repoName)
        repoinfo = {}
        repo_url = base_url + repoName
        try :
            repo_plain_text = urlopen(repo_url).read()
            repo_soup = BeautifulSoup(repo_plain_text, 'html.parser')
            repoinfo['topic'] = get_topics(repo_soup)
            repoinfo['language'] = get_languages(repo_soup)
            repoinfo['name'] = repoName
            forkedRopoInfoObject.append(repoinfo)
        except :
            pass
    return forkedRopoInfoObject


def get_followers(page, depth):
    list_followers = []
    followers_plain_text = urlopen(page).read()
    followers_soup = BeautifulSoup(followers_plain_text, 'html.parser')
    followers = followers_soup.select(".d-inline-block.no-underline.mb-1")
    pages = followers_soup.select(".pagination a")
    for follower in followers:
        dict = get_userInfo(follower.get("href")[1:], depth + 1)
        list_followers.append(dict)

    # print("list_followers : ", list_followers)
    returndict = {}
    returndict["page"] = "null"
    returndict["list"] = []
    if pages.__len__() == 0:    return returndict
    if pages[pages.__len__() - 1].text == "Previous":
        return returndict
    returndict["page"] = pages[pages.__len__() - 1].get('href')
    returndict["list"] = list_followers
    return returndict


def get_following(page, depth):
    list_following = []
    following_plain_text = urlopen(page).read()
    following_soup = BeautifulSoup(following_plain_text, 'html.parser')
    followings = following_soup.select(".d-inline-block.no-underline.mb-1")
    pages = following_soup.select(".pagination a")
    for following in followings:
        dict = get_userInfo(following.get("href")[1:], depth + 1)
        list_following.append(dict)

    # print("list_following : ", list_following)
    returndict = {}
    returndict["page"] = "null"
    returndict["list"] = []
    if pages.__len__() == 0:    return returndict
    if pages[pages.__len__() - 1].text == "Previous" or len(pages) == 0:
        return returndict
    returndict["page"] = pages[pages.__len__() - 1].get('href')
    returndict["list"] = list_following
    return returndict


def get_userInfo(user, depth):
    if (depth == 2): return user
    # print("user : ", user, "depth : ", depth)
    list_followers = []
    list_following = []

    commiter_dict = {}
    try :
        plain_text = urlopen(base_url + "/" + user).read()
    except :
        return commiter_dict

    soup = BeautifulSoup(plain_text, 'html.parser')

    commiter_dict['id'] = get_id(soup)
    commiter_dict['name'] = get_name(soup)
    commiter_dict['location'] = get_location(soup)
    commiter_dict['forkedRepos'] = get_forkedRepos(base_url + "/" + user + ownRepo_url)

    # store followers
    returnedDict = get_followers(base_url + "/" + user + followers_url, depth)
    list_temp = returnedDict["list"]
    next_page = returnedDict["page"]
    list_followers.extend(list_temp)
    for i in range(0, pageNum):
        if (next_page == "null"): break
        returnedDict = get_followers(next_page, depth)
        list_temp = returnedDict["list"]
        next_page = returnedDict["page"]
        list_followers.extend(list_temp)
    commiter_dict['followers'] = list_followers

    # store followings
    returnedDict = get_following(base_url + "/" + user + following_url, depth)
    list_temp = returnedDict["list"]
    next_page = returnedDict["page"]
    list_following.extend(list_temp)
    for j in range(0, pageNum):
        if (next_page == "null"): break
        returnedDict = get_following(next_page, depth)
        list_temp = returnedDict["list"]
        next_page = returnedDict["page"]
        list_following.extend(list_temp)
    commiter_dict['following'] = list_following

    return commiter_dict


def setDict(set_repos):
    outputDictWithKey = []
    repoCount = 0
    for repo in set_repos:
        repoCount += 1
        print(repoCount, " in ", len(set_repos), " repos")
        print("current repo :", repo)
        repoinfo = {}
        repo_url = base_url + "/" + repo
        commits_url = "/commits/master"
        plain_text = urlopen(repo_url).read()
        soup = BeautifulSoup(plain_text, 'html.parser')

        repoinfo['name'] = repo
        repoinfo['topic'] = get_topics(soup)
        repoinfo['language'] = get_languages(soup)

        next_page = get_commiters(repo_url + commits_url)
        for i in range(0, pageNum):
            if (next_page == "null"): break
            next_page = get_commiters(next_page)
        print('중복제거한 총 커미터들 : ', set_commiters.__len__(), '명')

        print(set_commiters)
        commiters_array = []

        commiterCount = 0
        for commiter in set_commiters:
            commiterCount += 1
            print(repoCount, " in ", len(set_repos), " repos")
            print(commiterCount, " in ", len(set_commiters), " commiters")
            commiters_array.append(get_userInfo(commiter, 0))

        repoinfo['commiters'] = commiters_array

        outputDictWithKey.append(repoinfo)
        set_commiters.clear()
        # outputDict["trending"] = outputDictWithKey
        # with open('outputjson.json', 'w') as outfile:
        #     json.dump(outputDict, outfile)
    return outputDictWithKey

get_trendingList()
outputDict["trending"] = setDict(set_trending)
outputDict["selectedRepo"] = setDict(set_selected_repos)

with open('outputjson.json', 'w') as outfile:
    json.dump(outputDict, outfile)

print("start_time", start_time)  # 출력해보면, 시간형식이 사람이 읽기 힘든 일련번호형식입니다.
print("--- %s seconds ---" % (time.time() - start_time))
