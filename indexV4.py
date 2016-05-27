"""V4 now has the ability to add a city after port 5000 using "/?searchcity=<city>"
so that the page can search using the URL, but still defaults to Midvale"""

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
import datetime
import os
import json
import time
import urllib2


app = Flask(__name__)

def get_weather(city):
	url = "http://api.openweathermap.org/data/2.5/forecast/daily?q={}&appid=64aaf003f19380ac5c268ae0724efea2&cnt=10&mode=json&units=imperial".format(city)
	# api_key ='64aaf003f19380ac5c268ae0724efea2'
	response = urllib2.urlopen(url).read()
	return response

@app.route("/")
def index():
	searchcity = request.args.get("searchcity")
	if not searchcity:
		searchcity = request.cookies.get("last_city")
	if not searchcity:
		searchcity = "Midvale"
	forcast_list = []
	data = json.loads(get_weather(searchcity))
	try:
		city = data['city']['name']
	except KeyError:
		return render_template("invalid_city.html", user_input=searchcity)
	city = data.get('city').get('name')
	country = data.get('city').get("country")
	for d in data.get('list'):
		day = time.strftime('%d %B', time.localtime(d.get('dt')))
		mini = d.get('temp').get('min')
		maxi = d.get('temp').get('max')
		description = d.get('weather')[0].get('description')
		forcast_list.append((day, mini, maxi, description))
	response = make_response(render_template("indexV4.html", city=city, country=country, forcast_list=forcast_list))
	if request.args.get("remember"):
		response.set_cookie("last_city", "{},{}".format(city, country), expires=datetime.datetime.today() + datetime.timedelta(days=365))
	return response

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True)