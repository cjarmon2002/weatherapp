"""This version is the first on created, it used very pooryly written html
code and is a mess. Future iterations use Jinja templates to make things
cleaner and utilize the render_templates imported from flask"""

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
	page = "<html><head><title>My Weather</title></head><body>"
	page += "<h1>Weather for {}, {}</h1>".format(data.get('city').get('name'),
		data.get('city').get('country'))
	for day in data.get("list"):
		page += "<b>date:</b> {} <b>min:</b> {} <b>max:</b> {} <b>discription</b> {} <br> ".format(
			time.strftime('%d %B', time.localtime(day.get('dt'))),
			(day.get("temp").get("min")),
			day.get("temp").get("max"),
			day.get("weather")[0].get("description"))
	page += "</body></html>"
	return page

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True)