import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f'https://kr.indeed.com/jobs?q=python&l=%EC%84%9C%EC%9A%B8&limit={LIMIT}'

def extract():
  #getting HTML
  get_indeed = requests.get(URL)
  #extracting: how many pages
  soup = BeautifulSoup(get_indeed.text, 'html.parser')
  pagination = soup.find("div", {"class":"pagination"})
  links = pagination.find_all('a')
  #print("links:", links[0], "여기까지")
  pages =[]
  for link in links[:-1]:
    pages.append(int(link.find('span').string))
  max_page = pages[-1]
  return max_page

def extract_job(html):
  title = html.find("h2", {"class":"title"}).find("a")["title"]
  company = html.find("span", {"class":"company"})
  company_anchor = company.find("a")
  if company_anchor is not None:
    company =str(company_anchor.string)
  else: 
    company =str(company.string)
  company = company.strip()
  location = html.find("div", {"class":"recJobLoc"})["data-rc-loc"]
  job_id = str(html["data-jk"]).strip()
  #print(job_id)
  return {
    "title":title, 
    "company":company, 
    "location":location, 
    "link":f'https://kr.indeed.com/viewjob?jk={job_id} '
    }
#extracting: job info
def extract_indeed_jobs(last_page):
  jobs=[]
  for page in range(last_page):
    print("scraping Indeed page:",page)
    result =requests.get(f'{URL}&start={page*LIMIT}')
    #print(f'&start={page*LIMIT}')
    #print(result.status_code)
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all("div",{"class":"jobsearch-SerpJobCard"})
    for result in results:
      job = extract_job(result)
      jobs.append(job) 
  return jobs

def get_jobs():
  last_page = extract()
  jobs = extract_indeed_jobs(last_page)
  return jobs
