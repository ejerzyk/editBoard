from django.db import models
from django.contrib.auth.models import User

SECTION_CHOICES = (
		('M', 'METRO'),
		('N', 'UNIVERSITY NEWS'),
		('AC', 'ARTS & CULTURE'),
		('SR', 'SCIENCE & RESEARCH'),
		('S', 'SPORTS'),
	)

REQUEST_CHOICES = (
		('CU', 'CREATE USER'),
		('CP', 'CHANGE PERMISSION'),
	)

# Create your models here.
class BDHuser(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, unique=True)
	class_year = models.IntegerField()
	phone_number = models.CharField(max_length=10)
	def __str__(self):
		return self.user.get_full_name()

class author(models.Model):
	id = models.AutoField(primary_key=True)
	gen_user = models.ForeignKey(BDHuser, unique=True)
	author_url = models.CharField(max_length=20)
	section = models.CharField(max_length=2, choices=SECTION_CHOICES, default='N')
	def __str__(self):
		return self.gen_user.__str__()

class requests(models.Model):
	id = models.AutoField(primary_key=True)
	by = models.ForeignKey(BDHuser)
	approved_rejected_by = models.ForeignKey(author)
	req = models.CharField(max_length=2, choices=REQUEST_CHOICES, default='CU')