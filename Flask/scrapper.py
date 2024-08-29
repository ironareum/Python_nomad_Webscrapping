import requests
from bs4 import BeautifulSoup


def stock_get_pages(url):
  request = requests.get(url)
  soup = BeautifulSoup(request.text,'html.parser')
  pagination = soup.find("div", {"class":"s-pagination"})
  #print(pagination)
  pages = pagination.find_all("a",{"class":"s-pagination--item"})
  last_page = (pages[-2].text).strip()
  return int(last_page)

def extract_job(html):
  title = html.find("h2",{"class":"mb4"}).find("a")["title"]
  company, location = html.find("h3",{"class":"fc-black-700"}).find_all("span",recursive=False)
  '''
  company = str(company.string).strip()
  location = str(location.string).strip()
  '''
  company = str(company.string).strip()
  location = location.get_text(strip=True)
  job_id = html["data-jobid"]
  return {
    "title" : title,
    "company" : company,
    "location" : location,
    "link" : f"https://stackoverflow.com/jobs/{job_id}/"
  }

def extract_so_jobs(last_page, url):  
  jobs =[]
  for page in range(3): #last_page
    print("scraping S/O page:",page)
    request = requests.get(f'{url}&pg={page+1}')
    soup = BeautifulSoup(request.text,'html.parser')
    infos = soup.find("div",{"class":"listResults"})
    results = infos.find_all("div", {"class":"-job"})
    for info in results:
      job = extract_job(info)
      jobs.append(job)
  return jobs

def get_jobs(word):
  url = f"https://stackoverflow.com/jobs?q={word}"
  last_page = stock_get_pages(url)
  jobs = extract_so_jobs(last_page, url)
  return jobs
