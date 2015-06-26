from django.db import models

from accounts.models import SECTION_CHOICES, author

# Create your models here.
class story(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=100)
	date = models.DateField()
	section = models.CharField(choices=SECTION_CHOICES, max_length=2)
	url = models.CharField(max_length=150)
	def authors(self):
		authors = []
		for ar in author_relationship.objects.filter(story=self):
			authors.append(ar.author)
		return authors
	def editors(self):
		editors = []
		for er in editor_relationship.objects.filter(story=self):
			editors.append(er.editor)
		return editors

class author_relationship(models.Model):
	id = models.AutoField(primary_key=True)
	story = models.ForeignKey(story)
	author = models.ForeignKey(author)

class editor_relationship(models.Model):
	id = models.AutoField(primary_key=True)
	story = models.ForeignKey(story)
	editor = models.ForeignKey(author)