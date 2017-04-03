from pyquery import PyQuery
from requests.exceptions import ConnectionError
from collections import Counter
from queue import Queue
from threading import Thread
# from wordcloud import WordCloud
# from matplotlib import pyplot
from .log import logger
from .models import Job, Information, Skill
import requests
import time
import re


class LG(object):
    """A base class generate the position link"""
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/55.0.2883.87 Safari/537.36'
        }
        self.start_url = 'https://www.lagou.com/'
        self._positions = None

    def get_page_code(self, url):
        """get the given url page code"""
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.content.decode('utf-8')
            else:
                logger.error("Get page source code error")
                return None
        except ConnectionError as e:
            logger.error("requests connection error")
            return None

    @property
    def positions(self):
        """get all the position link"""
        if not self._positions:
            queryset = Job.objects.all()
            if queryset.exists():
                position_dict = {}
                for query in queryset:
                    position_dict[query.position] = query.url
            else:
                position_dict = self._parse_postion_link()
            self._positions = position_dict
            # print(self._positions)
        return self._positions

    def _parse_postion_link(self):

        html = self.get_page_code(self.start_url)
        query = PyQuery(html)
        position_dict = {}
        position_data = query(".menu_sub dd a").items()
        for _position in position_data:
            name = _position.text()
            link = _position.attr("href")
            position_dict[name] = link
            if name and link:
                instance = Job(position=name, url=link)
                instance.save()
                print(name, link)
        return position_dict



class Recruit(LG):
    """A class obtain specific job information"""
    def __init__(self, keyword):
        super(Recruit, self).__init__()
        self.keyword = keyword
        self.skills = []
        self.link_queue = Queue()

    def parse_job_link(self, page=1):
        """get all job link of one page"""
        try:
            url = self.positions[self.keyword] + '{}/'.format(page)
            response = self.get_page_code(url)
            logger.info("Ready to crawl the {}th page link".format(page))
            query = PyQuery(response)
            item_lists = query(".item_con_list li").items()
            for item in item_lists:
                link = item(".position_link").attr("href")
                # title = item("h2").text()
                self.link_queue.put(link)
                print(link)
        except KeyError:
            logger.error("NO such job")

    def parse_job_info(self, link):
        """get the job information"""
        response = self.get_page_code(link)
        query = PyQuery(response)

        infor = query("dd.job_request")
        salary = infor("span.salary").text().strip()
        location = infor("span:nth-child(2)").text().strip('/')
        expreience = infor("span:nth-child(3)").text().strip('/')
        degree = infor("span:nth-child(4)").text().strip('/')
        information = Information(url=link, salary=salary, location=location, expreience=expreience, degree=degree)
        job = Job.objects.filter(position__iexact=self.keyword).first()
        information.job = job
        information.save()
        print(salary, location, expreience, degree)

        description = query("#job_detail > dd.job_bt > div")
        logger.info("正在爬取第...个职位描述")
        text = description.text()
        self._search_skill(text)

    def _search_skill(self, text):
        rule = re.compile('([a-zA-Z]+)')
        results = rule.findall(text)
        self.skills.extend(results)

    def count_skill(self):
        for i in range(len(self.skills)):
            self.skills[i] = self.skills[i].lower()
        _skill_frequency = Counter(self.skills).most_common(160)
        return _skill_frequency

    def working_thread(self):
        while True:
            link = self.link_queue.get()
            self.parse_job_info(link)
            time.sleep(1)
            self.link_queue.task_done()

    def run(self):
        for i in range(1, 11):
            self.parse_job_link(i)

        for i in range(10):
            t = Thread(target=self.working_thread)
            t.setDaemon(True)
            t.start()
        self.link_queue.join()

        skill_count = self.count_skill()
        for _skill in skill_count:
            skill_instance = Skill(skill=_skill[0], frequency=_skill[1])
            job = Job.objects.filter(position__iexact=self.keyword).first()
            skill_instance.job = job
            skill_instance.save()
        print(skill_count)


def generate_word_cloud(frequencies):
    word_cloud = WordCloud().fit_words(frequencies)
    pyplot.imshow(word_cloud, interpolation="bilinear")
    pyplot.axis("off")
    pyplot.show()

if __name__ == '__main__':
    recruit = Recruit("Java")
    recruit.run()
    #skill_frequency = recruit.count_skill()
    #generate_word_cloud(skill_frequency)


