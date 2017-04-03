from pyquery import PyQuery
import requests
import re

# def get_page_info():
# 	url = 'https://www.lagou.com/jobs/2958376.html'
# 	response = requests.get(url)
# 	if response.status_code == 200:
# 		content = response.content.decode('utf-8')
# 		query = PyQuery(content)
# 		infor = query("dd.job_request")
# 		salary = infor("span.salary").text().strip()
# 		location = infor("span:nth-child(2)").text().strip('/')
# 		expreience = infor("span:nth-child(3)").text().strip('/')
# 		degree = infor("span:nth-child(4)").text().strip('/')
# 		print(salary, location, expreience, degree
# 		url(r'^(?P<slug>[\w-]+)/poll/$',
def test_url_match():
	

if __name__ == '__main__':
	test_url_match()