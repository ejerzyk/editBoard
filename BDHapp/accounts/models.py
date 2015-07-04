from django.db import models
from django.contrib.auth.models import User

import urllib2
from dateutil import parser
from bs4 import BeautifulSoup

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

PERMISSION_CHOICES = (
		('CE', 'COPY ED'),
		('SW', 'SENIOR STAFF WRITER'),
		('SE', 'SECTION ED'),
		('EB', 'EDIT BOARD'),
	)

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
	def scrape_page(self, story_soup_list):
		for story_soup in story_soup_list:
			section = story_soup.find('p', class_='category_list').get_text(strip=True)
			title_html = story_soup.h2.a 
			story_url = title_html.get('href')
			title = title_html.get_text(strip=True)
			date_of_article = parser.parse(story_soup.find('div', class_='recent-meta').find('span').get_text())
			try: 
				story_in_db = story.objects.get(title=title)
				try:
					author_related = author_relationship.objects.get(story=story_in_db, author=self)
					return False
				except author_relationship.DoesNotExist:
					new_ar = author_relationship(story=story_in_db, author=self)
					new_ar.save()
			except story.DoesNotExist:
				new_story = story(title=title, section=section, date=date_of_article, url=story_url)
				new_story.save()
				new_ar = author_relationship(story=new_story, author=self)
				new_ar.save()
		return True 
	def scrape(self):
		url = self.author_url
		req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
		con = urllib2.urlopen( req )
		resp_str = unicode(con.read().replace('&raquo;', '&#187;'), 'utf-8')
		con.close()
		soup = BeautifulSoup(resp_str, 'html.parser')
		next_page = True
		while next_page:
			print 'SCRAPING ' + url
			next_page = self.scrape_page(soup.find_all('div', class_='post-content'))
			next_page_html = soup.find('a', class_='next page-numbers')
			if next_page_html is not None and next_page:
				url = next_page_html.get('href')
				next_req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
				next_con = urllib2.urlopen( next_req )
				resp_str = unicode(next_con.read().replace('&raquo;', '&#187;'), 'utf-8')
				con.close()
				soup = BeautifulSoup(resp_str, 'html.parser')
			else: 
				print 'NO NEXT PAGE'
				next_page = False

class perm_request(models.Model):
	id = models.AutoField(primary_key=True)
	by = models.ForeignKey(BDHuser)
	new_permission = models.CharField(max_length=2, choices=PERMISSION_CHOICES, default='CE')
	req = models.CharField(max_length=2, choices=REQUEST_CHOICES, default='CU')

class story(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=100)
	date = models.DateField()
	section = models.CharField(choices=SECTION_CHOICES, max_length=2)
	url = models.CharField(max_length=150)
	def __str__(self):
		return self.title
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