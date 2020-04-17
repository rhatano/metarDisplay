import Tkinter as tk
import pycurl
from io import BytesIO
import time
from metar import Metar
import re
import pandas as pd


#takes in metar object and returns pressure altitude
def pressureAlt(metarObs):
	elevation =  airports.loc[airports["ICAO_ID"]==metarObs.station_id].iloc[0]["ELEVATION"]
	pressure = metarObs.press.value("in")
	return str(elevation + (29.92 - pressure)*1000)

#takes in metar object and returns density altitude
def densityAlt(metarObs):
	temperature = metarObs.temp.value("F")
	pressure = metarObs.press.value("in")

display = tk.Tk()

# Airport Database
airports = pd.read_csv('airports.csv')

airportList = []
with open('airports.txt','r') as f:
	airportList = f.read().splitlines()
airportMetars = []

print airportList

for airport in airportList:
	b_obj = BytesIO() 
	crl = pycurl.Curl() 

	# Set URL value
	crl.setopt(crl.URL, 'https://tgftp.nws.noaa.gov/data/observations/metar/stations/'+airport+'.TXT')

	# Write bytes that are utf-8 encoded
	crl.setopt(crl.WRITEDATA, b_obj)

	# Perform a file transfer 
	crl.perform() 

	# End curl session
	crl.close()

	# Get the content stored in the BytesIO object (in byte characters) 
	get_body = b_obj.getvalue()

	# Decode the bytes stored in get_body to HTML and print the result 
	metarString = get_body.decode('utf8')
	try:
		airportMetars.append(Metar.Metar(re.split('\n',metarString)[1]))
	except:
		airportMetars.append('No METAR found')


for airportMetar in airportMetars:
	# try:
		print airportMetar.string()
		print "Pressure Altitude: " + pressureAlt(airportMetar)
	# except:
	# 	print airportMetar




# def densityAlt():
# 	pass

#print Metar.Metar(re.split('\n',metarString)[1]).wind_dir


# greeting = tk.Label(text=displayString)
# greeting.pack()
# display.mainloop()