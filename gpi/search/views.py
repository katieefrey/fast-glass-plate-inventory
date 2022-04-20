from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

#from astroquery.simbad import Simbad
from astropy import units as u
from astropy.coordinates import SkyCoord

import requests

import pymongo
import json

from main.secrets import connect_string

my_client = pymongo.MongoClient(connect_string)
dbname = my_client['plates']
glass = dbname["glass"]
archives = dbname["archives"]

sort_list = [
    {
        "name" : "Identifier",
        "nickname" :"identifier",
        "field": "identifier"
    },
    {
        "name" : "Archive",
        "nickname" :"archive",
        "field": "archive"
    },
    {
        "name" : "Right Ascension",
        "nickname" : "ra",
        "field": "exposure_info.ra_deg"
    },
]

def index(request):
    archive = list(archives.find({"plate_details" : True}).distinct("identifier"))
   
    context = {
            "archive": archive,
            "sort_list" : sort_list,
            "error" : ""
            }

    return render(request, "search/search.html", context)


def result(request):

    apiurl = request.build_absolute_uri().replace("search/result","api")+"&format=json"
    r = (requests.get(apiurl)).json()

    context = {
        "results" : r["results"] 
    }
    
    try:
        params = (request.build_absolute_uri()).split("?")
        query = params[1].split("&")
        context["query"] = query    
    except:
        pass

    if len(r["results"]) == 0:
        context["no_res"] = "No results!"

    context["results_count"] = r["total_results"]
    try:
        context["num_start"] = r["start"]
        context["num_end"] = r["end"]
        context["num_skip"] = r["num_skip"]
    except:
        pass
    
    context["num_results"] = r["num_results"]
   
    return render(request, "search/results.html", context)