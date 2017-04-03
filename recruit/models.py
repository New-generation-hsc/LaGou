from django.db import models

# Create your models here.

class Job(models.Model):

	position = models.CharField(max_length=100)
	url = models.URLField()

	class Meta:
		ordering = ['position']

	def __str__(self):
		return self.position


class Information(models.Model):

	url = models.URLField()
	salary = models.CharField(max_length=30)
	location = models.CharField(max_length=30)
	expreience = models.CharField(max_length=30, null=True, blank=True)
	degree = models.CharField(max_length=30, null=True, blank=True)

	job = models.ForeignKey(Job, related_name='job_info')

	class Meta:
		ordering = ['salary', 'expreience']

	def __str__(self):
		return "{}/{}/{}/{}".format(self.salary, self.location, self.expreience, self.degree)


class Skill(models.Model):

	skill = models.CharField(max_length=30)
	frequency = models.IntegerField()

	job = models.ForeignKey(Job, related_name='job_skill')

	class Meta:
		ordering = ['-frequency']

	def __str__(self):
		return "{}: {}".format(self.skill, self.frequency)
