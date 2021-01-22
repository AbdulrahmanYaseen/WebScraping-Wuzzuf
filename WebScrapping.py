import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

job_title = []
company_name = []
location = []
skills = []
links = []
salary = []
responsabilites = []
date = []
page_num = 0

while True:
    try:

        result = requests.get(f"https://wuzzuf.net/search/jobs/?a=navbl%7Cspbl&q=data%20analyst&start={page_num}")
        src = result.content
        soup = BeautifulSoup(src, "lxml")
        page_limit = int(soup.find("strong").text)

        if (page_num > page_limit // 15):
            print("Pages ended")
            break

        job_titles = soup.find_all("h2", {"class": "css-m604qf"})
        company_names = soup.find_all("a", {"class": "css-17s97q8"})
        location_names = soup.find_all("span", {"class": "css-5wys0k"})
        job_skills = soup.find_all("div", {"class": "css-y4udm8"})
        posted_new = soup.find_all("div", {"class": "css-4c4ojb"})
        posted_old = soup.find_all("div", {"class": "css-do6t5g"})
        posted = [*posted_new, *posted_old]

        for i in range(len(job_titles)):
            job_title.append(job_titles[i].text)
            links.append(job_titles[i].find("a").attrs['href'])
            company_name.append(company_names[i].text)
            location.append(location_names[i].text)
            skills.append(job_skills[i].text)
            date_text = posted[i].text.replace("_", "").strip()
            date.append(date_text)

        page_num += 1
        print("Page Switched")

    except:
        print("error occurred")
        break



for link in links:
    try:
        result = requests.get(link)
        src = result.content
        soup = BeautifulSoup(src, "lxml")
        salaries = soup.find("div", {"class": "matching-requirement-icon-container", "data-toggle": "tooltip",
                                     "data-placement": "top"})
        salary.append(salaries.text.strip())
    except:
        salary.append("not found")
        print("one job salary not found")
    continue


for link in links:
    try:
        result = requests.get(link)
        src = result.content
        soup = BeautifulSoup(src, "lxml")
        requirements = soup.find("span", {"itemprop": "responsibilities"}).ul
        requirements_text = ""
        for li in requirements.find_all("li"):
            requirements_text += li.text + " | "
            requirements_text = requirements_text[:-2]
        responsabilites.append(requirements_text)
    except:
        print('one requirement not in ul format ')
        responsabilites.append('Not readable')
    continue






file_list = [job_title, company_name, date, location, skills, links, salary, responsabilites]
exported = zip_longest(*file_list)

with open("file location", "w", encoding='utf-8') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(['job_title', 'company_name', 'date', 'location', 'skills', 'links', 'salary', 'responsabilites'])
    wr.writerows(exported)