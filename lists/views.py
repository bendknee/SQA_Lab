from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):

	html_payload = '''<html>
			<head>
				<title>HomePage</title>
			</head>
			<body>

				<h4>The name's Benny.</h4>
				<h1>Benny William Pardede</h1>
				<p>But they usually call me the <strong>trequartista</strong></p>
				<p>- 1606917550</p>
				
			</body>
		</html>'''
	return HttpResponse(html_payload)
