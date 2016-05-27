"""This version used Jinja templates for cleaner look and loops through days"""

from flask import Flask
from flask import render_template
import os
import json
import time
import urllib2


app = Flask(__name__)

def get_weather():
	url = "http://api.openweathermap.org/data/2.5/forecast/daily?id=5778244&appid=64aaf003f19380ac5c268ae0724efea2&cnt=10&mode=json&units=imperial"
	# api_key ='64aaf003f19380ac5c268ae0724efea2'
	response = urllib2.urlopen(url).read()
	return response

@app.route("/")
def index():
	forcast_list = []
	data = json.loads(get_weather())
	city = data.get('city').get('name')
	country = data.get('city').get("country")
	for d in data.get('list'):
		day = time.strftime('%d %B', time.localtime(d.get('dt')))
		mini = d.get('temp').get('min')
		maxi = d.get('temp').get('max')
		description = d.get('weather')[0].get('description')
		forcast_list.append((day, mini, maxi, description))
	return render_template("indexV3.html", city=city, country=country, forcast_list=forcast_list)

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True)