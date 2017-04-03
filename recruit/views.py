from django.shortcuts import render
import pygal
from .models import Information, Skill, Job
from collections import Counter
from .clawer import Recruit
# Create your views here.

def index(request):

    keyword = request.GET.get('search', None)
    if keyword == None:
        keyword = 'Python'
    position = Job.objects.filter(position__iexact=keyword).first()
    queryset = position.job_skill.all()[:10]

    bar_chart = pygal.Bar()
    bar_chart.title = 'ability frequency in {} recruit'.format(keyword)
    for query in queryset:
        bar_chart.add(query.skill, query.frequency)

    pie_chart = pygal.Pie()
    pie_chart.title = "expreience in {} recruit".format(keyword)
    pie_chart.add("经验不限", position.job_info.filter(expreience="经验不限").count())
    pie_chart.add("经验1-3年", position.job_info.filter(expreience="经验1-3年").count())
    pie_chart.add("经验3-5年", position.job_info.filter(expreience="经验3-5年").count())
    pie_chart.add("经验5-10年", position.job_info.filter(expreience="经验5-10年").count())

    line_chart = pygal.Line()
    line_chart.title = "salary in {} recruit".format(keyword)
    salaries = ["10k-15k", "10k-18k", "10k-20k", "15k-30k", "25k-30k", "20k-40k"]
    line_chart.x_labels = salaries
    line_chart.add('salary', [position.job_info.filter(salary=salary).count() for salary in salaries])

    location_chart = pygal.Pie()
    location_query = position.job_info.all()
    locations = [obj.location for obj in location_query]
    location_count = Counter(locations).most_common(8)
    for query in location_count:
        location_chart.add(query[0], query[1])

    context = {
    'data': bar_chart.render(),
    'pie_chart': pie_chart.render(),
    'line_chart': line_chart.render(),
    'location_chart': location_chart.render()
    }
    return render(request, 'index.html', context)

