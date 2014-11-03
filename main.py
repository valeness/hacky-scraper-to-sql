import urllib
from bs4 import BeautifulSoup

f = urllib.urlopen('http://apm.spm-sites.com/whats-new/blog-articles/')
soup = BeautifulSoup(f)

sql = []

for li in soup.findAll('li', {"class" : "object"}):

	child = li.find('a')

	link = child.get('href')
	link = "http://apm.spm-sites.com%s" % link

	print(link)

	post = urllib.urlopen(link)
	postSoup = BeautifulSoup(post)

	title = postSoup.find('h1').get_text()
	title = title.replace('"', '""')

	if title == 'Not Found':
		continue

  print(title)

	body = ''

	for p in postSoup.findAll('p'):
		body += p.get_text().encode('ascii', 'ignore')
		body += '\n'

	if not (postSoup.find('time')):
		date = 'none'
		year = link.split('/', 6)[6]
		print('Year: ' + year)
	else:
		date = postSoup.find('time').get_text()
		year = date.split(', ', 1)[1]

	body = body.replace(date + ' - ', '')
	body = body.replace("'", "''")
	body = body.replace('"', '""')

	author = "American Pest Management"
	stmt = 'INSERT INTO posts (title, body, date, author, year) VALUES ("%s", "%s", "%s", "%s", "%s");' % (title, body, date, author, year)
	stmt += '\n'

	sql.append(stmt)

for i in sql:
	with open("sql.txt", 'a') as file:
		print(i)
		file.write(i)
