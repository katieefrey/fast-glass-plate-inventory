from typing import List, Optional, Any, Callable
# from typing import Optional
# from typing import Any, Callable

# from fastapi import APIRouter
# from api import models, schemas

         
from fastapi import APIRouter as FastAPIRouter
from fastapi.types import DecoratedCallable

from astropy import units as u
from astropy.coordinates import SkyCoord

from bson.json_util import dumps
import pymongo
import json

from main.secrets import connect_string
      
class APIRouter(FastAPIRouter):
    def add_api_route(
            self, path: str, endpoint: Callable[..., Any], *,
            include_in_schema: bool = True, **kwargs: Any
            ) -> None:
        if path.endswith("/"):
            alternate_path = path[:-1]
        else:           
            alternate_path = path + "/"
        super().add_api_route(                                                 
            alternate_path, endpoint, include_in_schema=False, **kwargs)
        return super().add_api_route(
            path, endpoint, include_in_schema=include_in_schema, **kwargs)

api_router = APIRouter()

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

# search plates
@api_router.get("/plates")
def search_plates(
    skip: int = 0,
    limit: int = 50,
    identifier: Optional[str] = None,
    archive: Optional[str] = "all",
    obj: Optional[str] = None,
    ra: Optional[str] = None,
    dec: Optional[str] = None,
    radius: Optional[str] = 10,
    text: Optional[str] = None,
    observer: Optional[str] = None,
    sort_order: Optional[str] = "identifier"
    ):
    
    radius = int(radius)/60

    query = {}
    
    if identifier != None:
        query["identifier"] = { "$regex" : identifier, "$options" : "i"}

    if archive != "all":
        query["archive"] = { "$regex" : archive, "$options" : "i"}

    if obj != None:
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
            return {"error" : "no results"}

    if ra != None:
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
            return {"error" : "no results"}

    if dec != None:
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
            return {"error" : "no results"}

    if ra != None and dec != None:
        del query["exposure_info"]
        query["$and"] = [
            {"exposure_info": {"$elemMatch": {"dec_deg": {"$gt": mindec, "$lt": maxdec}}}},
            {"exposure_info": {"$elemMatch": {"ra_deg": {"$gt": minra, "$lt": maxra}}}}
        ]

    if text != None:
        
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
    
    if observer != None:
        query["$or"] = [
            {"plate_info.observer" : { "$regex" : observer, "$options" : "i"}},
        ]

    try:
        plates = (
                (
                    glassplates.find(query)
                        .sort([('identifier',pymongo.ASCENDING)])
                        .collation({"locale": "en_US", "numericOrdering": True})
                    )
                    .skip(skip)
                    .limit(limit)
                )
        
        plates_out = json.loads(dumps(plates))

        results_count = plates.count()

        results = {
            "total" : results_count,
            "limit" : limit,
            "skip" : skip,
            "results" : plates_out,
        }
        return results

    except:
        return {"error" : "no results"}


# show all archives
@api_router.get("/archives")
def list_archives(skip: int=0, limit: int = 50):

    try:
        archive = (
                (
                    archives.find({})
                        .sort([('identifier',pymongo.ASCENDING)])
                        .collation({"locale": "en_US", "numericOrdering": True})
                    )
                    .skip(skip)
                    .limit(limit)
                )

        archive_out = json.loads(dumps(archive))

        results_count = archive.count()

        results = {
            "total" : results_count,
            "limit" : limit,
            "skip" : skip,
            "results" : archive_out,
        }
        return results

    except:
        return {"error" : "no results"}

# show details about one archives
@api_router.get("/archives/{archive_id}")
def archive_details(archive_id):

    try:
        query = {}
        query["identifier"] = { "$regex" : archive_id, "$options" : "i"}
        
        archive = (archives.find(query))
        archive_out = json.loads(dumps(archive))

        results_count = archive.count()

        results = {
             "results" : archive_out,
        }
        return results

    except:
        return {"error" : "no results"}


# show plates in specific archive
@api_router.get("/{archive_id}")
def List_plates_in_archive(archive_id, skip: int=0, limit: int = 50):
    print("is this pinging?")
    try:
        query = {}
        query["archive"] = { "$regex" : archive_id, "$options" : "i"}
        plates = (
                (
                    glassplates.find(query)
                        .sort([('identifier',pymongo.ASCENDING)])
                        .collation({"locale": "en_US", "numericOrdering": True})
                    )
                    .skip(skip)
                    .limit(limit)
                )
        
        plates_out = json.loads(dumps(plates))

        results_count = plates.count()

        results = {
            "total" : results_count,
            "limit" : limit,
            "skip" : skip,
            "results" : plates_out,
        }
        return results

    except:
        return {"error" : "no results"}


# show one specific plate
@api_router.get("/{archive_id}/{plate_id}")
def plate_details(archive_id, plate_id):

    try:
        query = {}
        query["archive"] = { "$regex" : archive_id, "$options" : "i"}
        query["identifier"] = { "$regex" : '^'+plate_id+'$', "$options" : "i"}
        plates = json.loads(dumps(glassplates.find_one(query)))
        return plates

    except:
        return {"error" : "no results"}








# @api_router.get("/items/")
# def read_item(skip: int = 0, limit: int = 10, ra: Optional[str] = None):
#     if ra:
#         return fake_items_db[skip : skip + limit]
#     return fake_items_db[skip : skip + limit]



# @api_router.get("/plates")
# def read_plates():


#     plates = list(models.Plate.objects.all())

#     return plates



# @api_router.get("/plates/{plate_id}")#, response_model=List[schemas.Plate])
# def read_plates(plate_id):
#     #plates = models.Plate.objects.all()

#     #return plates
#     return {"item_id": plate_id}