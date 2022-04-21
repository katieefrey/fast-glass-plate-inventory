from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from bson.json_util import dumps

from astropy import units as u
from astropy.coordinates import SkyCoord

import pymongo
import json
import re

from main.secrets import connect_string

my_client = pymongo.MongoClient(connect_string)
dbname = my_client['plates']
glassplates = dbname["glass"]
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

# my custom API build
# this needs documentation
@api_view(['GET'])
def root(request):

    try:
        identifier = (request.GET["identifier"]).strip()
    except:
        identifier = ""

    try:
        obj = (request.GET["object"]).strip()
    except:
        obj = ""

    try:
        radius = float((request.GET["radius"]).strip())/60
    except:
        radius = 10/60

    try:
        ra = request.GET["ra"].strip()
    except:
        ra = ""

    try:
        dec = request.GET["dec"].strip()
    except:
        dec = ""

    try:
        text = (request.GET["text"]).strip()
    except:
        text = ""

    try:
        observer = (request.GET["observer"]).strip()
    except:
        observer = ""

    try:
        sort_order = request.GET["sort_order"].strip()
        for x in sort_list:
            if x["nickname"] == sort_order:
                sortfield = x["field"]
    except:
        sortfield = "identifier"

    try:
        archive = request.GET["archive"].strip()
    except:
        archive = "all"

    try:
        num_skip = int(request.GET["num_skip"].strip())
    except:
        num_skip = 0

    try:
        num_results = int(request.GET["num_results"].strip())
    except:
        num_results = 50

    query = {}
    
    if identifier != "":
        query["identifier"] = { "$regex" : identifier, "$options" : "i"}

    if archive != "all":
        query["archive"] = { "$regex" : archive, "$options" : "i"}

    # if plate identifer and ardchive provided, attempt to go straight there
    if identifier != "" and archive != "all":
        try:
            plate = list(glassplates.find({"identifier" : identifier}))
            return redirect('/collections/'+plate[0]["archive"]+'/'+plate[0]["identifier"])
        except:
            pass

    # if object was queried, this overwrites any ra and dec that might have been queried
    if obj != "":
        try:
            coords = SkyCoord.from_name(obj)
            ra = coords.ra.deg
            dec = coords.dec.deg
        except:
            results = {
                "total_results" : 0,
                "num_results" : 0,
                "results": {}
            }
            return Response(results, status=status.HTTP_404_NOT_FOUND)

    if ra != "":
        try:
            if ":" in str(ra):
                coords = SkyCoord(ra+" 0", unit=(u.hourangle, u.deg))
                ra = coords.ra.deg
            minra = round(float(ra) - radius*15, 4)
            maxra = round(float(ra) + radius*15, 4)
            query["exposure_info"] = {"$elemMatch": {"ra_deg": {"$gt": minra, "$lt": maxra}}}
        except:
            results = {
                "total_results" : 0,
                "num_results" : 0,
                "results": {}
            }
            return Response(results, status=status.HTTP_404_NOT_FOUND)

    if dec != "":
        try:
            if ":" in str(dec):
                coords = SkyCoord("0 "+dec, unit=(u.hourangle, u.deg))
                dec = coords.dec.deg
            mindec = round(float(dec) - radius, 4)
            maxdec = round(float(dec) + radius, 4)
            query["exposure_info"] = {"$elemMatch": {"dec_deg": {"$gt": mindec, "$lt": maxdec}}}
        except:
            results = {
                "total_results" : 0,
                "num_results" : 0,
                "results": {}
            }
            return Response(results, status=status.HTTP_404_NOT_FOUND)

    if ra != "" and dec != "":
        del query["exposure_info"]
        query["$and"] = [
            {"exposure_info": {"$elemMatch": {"dec_deg": {"$gt": mindec, "$lt": maxdec}}}},
            {"exposure_info": {"$elemMatch": {"ra_deg": {"$gt": minra, "$lt": maxra}}}}
        ]

    if text != "":
        
        query["$or"] = [
            {"plate_info.availability_note" : { "$regex" : text, "$options" : "i"}},
            {"plate_info.digitization_note" : { "$regex" : text, "$options" : "i"}},
            {"plate_info.quality" : { "$regex" : text, "$options" : "i"}},
            {"plate_info.notes" : { "$regex" : text, "$options" : "i"}},
            {"plate_info.condition" : { "$regex" : text, "$options" : "i"}},
            {"plate_info.observer" : { "$regex" : text, "$options" : "i"}},
            {"obs_info.instrument" : { "$regex" : text, "$options" : "i"}},
            {"obs_info.observatory" : { "$regex" : text, "$options" : "i"}},
            {"exposure_info.target" : { "$regex" : text, "$options" : "i"}},
            {"plate_info.emulsion" : { "$regex" : text, "$options" : "i"}}
        ]
    
    if observer != "":
        query["$or"] = [
            {"plate_info.observer" : { "$regex" : observer, "$options" : "i"}},
        ]

    # execute the full query
    plates = (
        (
        glassplates.find(query)
             .sort([(sortfield,pymongo.ASCENDING)])
             .collation({"locale": "en_US", "numericOrdering": True})
        )
        .skip(num_skip)
        .limit(num_results)
    )

    plates_out = json.loads(dumps(plates))

    results_count = plates.count()

    results = {
        "total_results" : results_count,
        "num_results" : num_results,
        "num_skip" : num_skip,
        "start" : num_skip+1,
    }

    if num_skip + num_results >= results_count:
        results["end"] = results_count
    else:
        results["end"] = num_skip + num_results

    # find next page
    if num_skip + num_results <= results_count:
        if "num_skip" in request.build_absolute_uri():
            results["next_page"] = re.sub(r"num_skip=\d+", "num_skip="+str(num_skip+num_results), request.build_absolute_uri())
        elif "?" in request.build_absolute_uri():
            results["next_page"] = request.build_absolute_uri()+"&num_skip="+str(num_skip + num_results)
        else:
            results["next_page"] = request.build_absolute_uri()+"?num_skip="+str(num_skip + num_results)

    # find previous page
    if num_skip+1 > 1 :
        newnum = num_skip - num_results
        if newnum < 0:
            newnum = 0

        if "num_skip" in request.build_absolute_uri():
            results["previous_page"] = re.sub(r"num_skip=\d+", "num_skip="+str(newnum), request.build_absolute_uri())
        elif "?" in request.build_absolute_uri():
            results["previous_page"] = request.build_absolute_uri()+"&num_skip="+str(newnum)
        else:
            results["previous_page"] = request.build_absolute_uri()+"?num_skip="+str(newnum)

    results["results"] = plates_out
    
    if plates == None:
        return Response(results, status=status.HTTP_404_NOT_FOUND)
            
    return Response(results, status=status.HTTP_200_OK)

@api_view(['GET'])
def archive(request):
    archive = json.loads(dumps(archives.find({})))
    return Response(archive)

# plates in archive
@api_view(['GET'])
def PlateArchive(request, archive):

    try:
        num_skip = int(request.GET["num_skip"].strip())
    except:
        num_skip = 0

    try:
        num_results = int(request.GET["num_results"].strip())
    except:
        num_results = 50

    query = {}
    query["archive"] = { "$regex" : archive, "$options" : "i"}

    plates = (
            (
                glassplates.find(query)
                    .sort([('identifier',pymongo.ASCENDING)])
                    .collation({"locale": "en_US", "numericOrdering": True})
                )
                .skip(num_skip)
                .limit(num_results)
            )
    
    plates_out = json.loads(dumps(plates))
    
    results_count = plates.count()

    results = {
        "total_results" : results_count,
        "num_results" : num_results,
        "num_skip" : num_skip,
        "results" : plates_out,
    }

    if plates == None:
        return Response(results, status=status.HTTP_204_NO_CONTENT)
            
    return Response(results, status=status.HTTP_200_OK)

# specific plate
@api_view(['GET'])
def GlassPlate(request, archive, identifier):

    query = {}
    query["archive"] = { "$regex" : archive, "$options" : "i"}
    query["identifier"] = { "$regex" : '^'+identifier+'$', "$options" : "i"}

    plates = json.loads(dumps(glassplates.find_one(query)))
    
    if plates == None:
        return Response({"results" : plates}, status=status.HTTP_204_NO_CONTENT)
            
    return Response({"results" : plates}, status=status.HTTP_200_OK)



