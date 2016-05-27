"""This version used Jinja templates for cleaner look, but didn't loop through days"""

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
	data = json.loads(get_weather())
	city = data.get('city').get('name')
	country = data.get('city').get("country")
	day = time.strftime('%d %B', time.localtime(data.get('list')[0].get("dt")))
	mini = data.get("list")[0].get("temp").get("min")
	maxi = data.get("list")[0].get("temp").get("max")
	description = data.get("list")[0].get("weather")[0].get("description")
	return render_template("indexV2.html", city=city, country=country, day=day, mini=mini, maxi=maxi, description=description)

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True)