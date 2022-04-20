import pymongo
from django.shortcuts import render
from main.secrets import connect_string

from django.http import HttpResponse

my_client = pymongo.MongoClient(connect_string)
dbname = my_client['plates']

glass = dbname["glass"]
archives = dbname["archives"]

def index(request):

    archivedetails = archives.find({})

    context = {
            "details" : archivedetails,
            }

    return render(request, "plates/collections.html", context)

def archive(request, archive_id):

    plates = glass.find({"archive" : archive_id}).sort([("identifier",pymongo.ASCENDING)]).collation({"locale": "en_US", "numericOrdering": True}).limit(10)

    archive_info = list(archives.find({"identifier" : archive_id}))

    context = {
        "archive" : archive_info[0],
        "plates": plates
    }

    return render(request, "plates/archive.html", context)


def plate(request, archive_id, plate_id):

    newid = plate_id.replace("%2520", " ")

    plate = list(glass.find({"identifier" : newid}))
    
    context = {
        "archive" : archive_id,
        "plate": plate[0],
    }

    return render(request, "plates/plate.html", context)