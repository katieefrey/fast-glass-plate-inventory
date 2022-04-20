from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

#from astroquery.simbad import Simbad
from astropy import units as u
from astropy.coordinates import SkyCoord

import pymongo
import requests
import json

from main.secrets import connect_string

my_client = pymongo.MongoClient(connect_string)
dbname = my_client['plates']
glass = dbname["glass"]
repos = dbname["plates_repository"]


sort_list = [
    {
        "name" : "Identifier",
        "nickname" :"identifier",
        "field": "identifier"
    },
    {
        "name" : "Archive",
        "nickname" :"archive",
        "field": "repository"
    },
    {
        "name" : "Right Ascension",
        "nickname" : "ra",
        "field": "exposure_info.ra_deg"
    },
]

def index(request):

    archives = repos.distinct("abbr")
   
    context = {
            "repositories": archives,
            "sort_list" : sort_list,
            "error" : ""
            }

    return render(request, "search/search.html", context)




def holding(request):
    
    archives = repos.distinct("abbr")

    getstring = ''

    try:
        archive = request.POST["archive"].strip()
    except:
        archive = "all"

    try:
        identifier = (request.POST["identifier"]).strip()
    except:
        identifier = ""

    try:
        obj = (request.POST["object"]).strip()
    except:
        obj = ""

    try:
        radius = int((request.POST["radius"]).strip())
    except:
        radius = 10

    try:
        ra = request.POST["ra"].strip()
    except:
        ra = ""

    try:
        dec = request.POST["dec"].strip()
    except:
        dec = ""

    try:
        text = (request.POST["text"]).strip()
    except:
        text = ""

    try:
        observer = (request.POST["observer"]).strip()
    except:
        observer = ""

    try:
        sort_order = request.POST["sort_order"].strip()
        for x in sort_list:
            if x["nickname"] == sort_order:
                sortfield = x["field"]
    except:
        sortfield = "identifier"

    context = {
        "repositories": archives,
        "sort_list" : sort_list,
        "archive"  : archive,
        "identifier"  : identifier,
        "obj"  : obj,
        "radius"  : radius,
        "ra"  : ra,
        "dec"  : dec,
        "text"  : text,
        "observer"  : observer,
    }


    if archive != "all":
        getstring += "&archive="+request.POST["archive"].strip()

    if identifier != "":
        getstring += "&identifier="+(request.POST["identifier"]).strip()

    
    # if plate identifer and ardchive provided, attempt to go straight there
    if identifier != "" and archive != "all":
        try:
            plate = list(glass.find({"identifier" : identifier}))
            return redirect('/collections/'+plate[0]["repository"]+'/'+plate[0]["identifier"])
        except:
            pass

    # if object was queried, this overwrites any ra and dec that might have been queried
    if obj != "":
        try:
            coords = SkyCoord.from_name(obj)
            getstring += "&obj="+(request.POST["object"]).strip()
        except:
            context["objerror"] = "Object not found."
            return render(request, "search/search.html", context)

    if ra != "":
        try:
            if ":" in str(ra):
                coords = SkyCoord(ra+" 0", unit=(u.hourangle, u.deg))
            minra = round(float(ra) - radius*15, 4)
            getstring += "&ra="+request.POST["ra"].strip()
        except:
            context["raerror"] = "RA not valid."
            return render(request, "search/search.html", context)

    if dec != "":
        try:
            if ":" in str(dec):
                coords = SkyCoord("0 "+dec, unit=(u.hourangle, u.deg))
            mindec = round(float(dec) - radius, 4)
            getstring +=  "&dec="+request.POST["dec"].strip()
        except:
            context["decerror"] = "DEC not valid."
            return render(request, "search/search.html", context)

    if radius != 10:
        getstring += "&radius="+str((request.POST["radius"]).strip())

    if text != "":
        getstring += "&text="+(request.POST["text"]).strip()
    
    if observer != "":
        getstring += "&observer="+(request.POST["observer"]).strip()

    if sortfield != "identifier":
        getstring += "&sort_order="+request.POST["sort_order"].strip()

    outget = (request.build_absolute_uri('?')+"?"+getstring[1:]).replace("error","result")

    return redirect(outget)



def result(request):

    apiurl = request.build_absolute_uri().replace("search/result","api")+"&format=json"

    r = (requests.get(apiurl)).json()

    context = {
        "results" : r["results"] 
    }


    if len(r["results"]) == 0:
        context["no_res"] = "No results!"

    context["results_count"] = r["total_results"]
    context["num_start"] = r["start"]
    context["num_end"] = r["end"]
    context["num_results"] = r["num_results"]

    # also need to write a no results returned page
    return render(request, "search/results.html", context)















    # def result(request):

#     archives = repos.distinct("abbr")

#     try:
#         identifier = (request.GET["identifier"]).strip()
#     except:
#         identifier = ""

#     try:
#         obj = (request.GET["object"]).strip()
#     except:
#         obj = ""

#     try:
#         radius = float((request.GET["radius"]).strip())/60
#     except:
#         radius = 10/60

#     try:
#         ra = request.GET["ra"].strip()
#     except:
#         ra = ""

#     try:
#         dec = request.GET["dec"].strip()
#     except:
#         dec = ""

#     try:
#         text = (request.GET["text"]).strip()
#     except:
#         text = ""

#     try:
#         observer = (request.GET["observer"]).strip()
#     except:
#         observer = ""

#     try:
#         sort_order = request.GET["sort_order"].strip()
#         for x in sort_list:
#             if x["nickname"] == sort_order:
#                 sortfield = x["field"]
#     except:
#         sortfield = "identifier"

#     try:
#         archive = request.GET["archive"].strip()
#     except:
#         archive = "all"

#     context = {
#         "repositories": archives,
#         "sort_list" : sort_list,
#         "archive"  : archive,
#         "identifier"  : identifier,
#         "obj"  : obj,
#         "radius"  : int(radius*60),
#         "ra"  : ra,
#         "dec"  : dec,
#         "text"  : text,
#         "observer"  : observer,
#     }

#     try:
#         num_skip = int(request.GET["num_skip"].strip())
#     except:
#         num_skip = 0

#     try:
#         num_results = int(request.GET["num_results"].strip())
#     except:
#         num_results = 50

#     query = {}
    
#     if identifier != "":
#         query["identifier"] = { "$regex" : identifier, "$options" : "i"}

#     if archive != "all":
#         query["repository"] = { "$regex" : archive, "$options" : "i"}

#     # if plate identifer and ardchive provided, attempt to go straight there
#     if identifier != "" and archive != "all":
#         try:
#             plate = list(glass.find({"identifier" : identifier}))
#             return redirect('/collections/'+plate[0]["repository"]+'/'+plate[0]["identifier"])
#         except:
#             pass

#     # if object was queried, this overwrites any ra and dec that might have been queried
#     if obj != "":
#         try:
#             coords = SkyCoord.from_name(obj)
#             ra = coords.ra.deg
#             dec = coords.dec.deg
#         except:
#             context["objerror"] = "Object not found."
#             return render(request, "search/search.html", context)

#     if ra != "":
#         try:
#             if ":" in str(ra):
#                 coords = SkyCoord(ra+" 0", unit=(u.hourangle, u.deg))
#                 ra = coords.ra.deg
#             minra = round(float(ra) - radius*15, 4)
#             maxra = round(float(ra) + radius*15, 4)
#             query["exposure_info"] = {"$elemMatch": {"ra_deg": {"$gt": minra, "$lt": maxra}}}

#         except:
#             context["raerror"] = "RA not valid."
#             return render(request, "search/search.html", context)

#     if dec != "":
#         try:
#             if ":" in str(dec):
#                 coords = SkyCoord("0 "+dec, unit=(u.hourangle, u.deg))
#                 dec = coords.dec.deg
#             mindec = round(float(dec) - radius, 4)
#             maxdec = round(float(dec) + radius, 4)
#             query["exposure_info"] = {"$elemMatch": {"dec_deg": {"$gt": mindec, "$lt": maxdec}}}
#         except:
#             context["decerror"] = "DEC not valid."
#             return render(request, "search/search.html", context)

#     if ra != "" and dec != "":
#         del query["exposure_info"]
#         query["$and"] = [
#             {"exposure_info": {"$elemMatch": {"dec_deg": {"$gt": mindec, "$lt": maxdec}}}},
#             {"exposure_info": {"$elemMatch": {"ra_deg": {"$gt": minra, "$lt": maxra}}}}
#         ]

#     if text != "":
        
#         query["$or"] = [
#             {"plate_info.availability_note" : { "$regex" : text, "$options" : "i"}},
#             {"plate_info.digitization_note" : { "$regex" : text, "$options" : "i"}},
#             {"plate_info.quality" : { "$regex" : text, "$options" : "i"}},
#             {"plate_info.notes" : { "$regex" : text, "$options" : "i"}},
#             {"plate_info.observer" : { "$regex" : text, "$options" : "i"}},
#             {"obs_info.instrument" : { "$regex" : text, "$options" : "i"}},
#             {"obs_info.observatory" : { "$regex" : text, "$options" : "i"}},
#             {"exposure_info.target" : { "$regex" : text, "$options" : "i"}},
#             {"plate_info.emulsion" : { "$regex" : text, "$options" : "i"}}
#         ]
    
#     if observer != "":
#         query["$or"] = [
#             {"plate_info.observer" : { "$regex" : observer, "$options" : "i"}},
#         ]

#     # execute the full query
#     plates = (
#         (
#         glass.find(query)
#              .sort([(sortfield,pymongo.ASCENDING)])
#              .collation({"locale": "en_US", "numericOrdering": True})
#         )
#         .skip(num_skip)
#         .limit(num_results)
#     )

#     results_count = plates.count()

#     if results_count == 0:
#         context["no_res"] = "No results!"

#     context["query"] = query
#     context["results"] = plates
#     context["results_count"] = results_count
#     context["num_start"] = num_skip + 1
#     context["num_end"] = num_skip + num_results
#     context["num_results"] = num_results


#     # also need to write a no results returned page
#     return render(request, "search/results.html", context)




# def holding(request):

#     test = request.build_absolute_uri().split("&")
    
#     getstring = ''
#     for y in test:
#         z = y.split("=")
#         if z[1] != '':
#             a = ("&"+z[0]+"="+z[1])
#             getstring+=a

#     print (getstring)

#     outget = request.build_absolute_uri('?')+"?"+getstring[1:]

#     print ("LOOK AT THIS")
#     print (outget)

#     return redirect(outget)