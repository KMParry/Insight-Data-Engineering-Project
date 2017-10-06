from app import app
from flask import render_template
from flask import redirect
from flask import request
from flask import jsonify
from flask_googlemaps import GoogleMaps
from flask_googlemaps import  Map, icons
import redis, os, json

GoogleMaps(app,key="AIzaSyDwfcLtwYD5C7onl9TVetTpYHq3okLw59Y")
r=redis.StrictRedis(host="localhost",port=6379,db=0)


def convert_loc_to_markers(listmet):

	list_of_dict=[]
	dict_of_met={}	
	for ii in range(0,len(listmet)):
		dict_of_met['lng']=listmet[ii][1]
		dict_of_met['lat']=listmet[ii][0]
		dict_of_met['icon']='http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
     		dict_of_met['infobox'] ="<b>Hello World from other place</b>"
		list_of_dict.append(dict(dict_of_met))

	return list_of_dict

def get_meters(loc):

        key="sanfran"

        # long/lat are swapped in redis
        r.geoadd(key,loc[1].decode('utf-8'),loc[0].decode('utf-8'),"tmp")

        meters=r.georadiusbymember(key,"tmp",.5,"mi")
        print meters

        return meters

def get_avail(meters):

        key="sanfran"

        avail=[]
        for ii in meters:
                state=r.get(ii)
                if(state=='1') and (ii!='tmp'):
                        avail.append(ii)

        met_list=[]
        meters_avail={}

        for ii in avail:
                locs=r.geopos(key,ii)
                lng,lat=locs[0]
		meters_avail['id']=ii
                meters_avail['lng']=lng
                meters_avail['lat']=lat
                meters_avail['icon']='http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
                met_list.append(dict(meters_avail))

	#check this is working
	#r.zrem(key,"tmp")

        return met_list

def make_reservation(meter):

        duration=300

        index=r.get(meter)

        # error handling; check current state (latency issue)
        # set state to zero to indicate that it is reserved
        current=r.get(index)
        if current=='-1':
                print 'error!! THIS IS METER ALREADY IN USE!!'
        elif current=='1':
                r.set(index,0)
                r.expire(index,duration)

        # convert to time to live to m:s format to return to user
        time_to_live=r.ttl(index)
        m,s = divmod(seconds,60)

        timeleft="%02d:%02d" % (m,s)

        return timeleft


@app.route('/redis')
def get_gps():

	latitude=request.args.get('lat')
	longitude=request.args.get('long')

	#pId=request.args.get('id')
	#print pID

	locs=[latitude,longitude]	

	meters=get_meters(locs)
	met_list=get_avail(meters)

	return jsonify(met_list)


@app.route('/redis/reserve')
def secure_reservation():

	latitude=request.args.get('lat')
	longitude=request.args.get('long')

	print latitude
	print longitude

	#get the index of the double clicked meter
#        meter=r.georadius(key,longitude,latitude,.1,"mi")
	
	print meter

	ttl=make_reservation(meter)
	
	output={}
	output['id']=meter
	output['lat']=latitude
	output['lng']=longitude
	output['ttl']=ttl

	return jsonify(output)

	
@app.route('/')
@app.route('/index')
def index():
	return render_template('example.html',title="Meter May I?")
	

@app.route('/github')
def github():
		
	address='https://github.com/KMParry/MeterMayI'
	return redirect(address)

@app.route('/slides')
def slides():
		
	address="https://docs.google.com/presentation/d/11bW_Z4gY6lj99j9FVwwiltHv1qDv9Vtopt7Bkn7WMZU/edit#slide=id.g20178e9d63_0_319"
	return redirect(address)
