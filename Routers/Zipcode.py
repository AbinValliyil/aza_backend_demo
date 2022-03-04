from fastapi import APIRouter
from geopy.geocoders import Nominatim
from geopy import distance
from Model import schemas





router = APIRouter()



# @router.post('/distance_finder',tags=['ZIPCODE_VALIDATION'])
# async def d_finder(code:schemas.AZA_geocode):
#   geocoder =Nominatim(user_agent='python')
#   cor1 =geocoder.geocode(code.pin1)
#   cor2 =geocoder.geocode(code.pin2)
#   lat1,log1 =(cor1.latitude),(cor1.longitude)
#   lat2,log2 =(cor2.latitude),(cor2.longitude)
#   place1=(lat1,log1)
#   place2=(lat2,log2)
  
  
    
#   return {"distance":distance.distance(place1,place2)._Distance__kilometers}



@router.post('/distance_finder',tags=['ZIPCODE_VALIDATION'])
async def d_finder(pin1:str,pin2:str):
  geocoder =Nominatim(user_agent = "0")
  cor1 =geocoder.geocode(pin1)
  cor2 =geocoder.geocode(pin2)
  lat1,log1 =(cor1.latitude),(cor1.longitude)
  lat2,log2 =(cor2.latitude),(cor2.longitude)
  place1=(lat1,log1)
  place2=(lat2,log2)
  dis =int(distance.distance(place1,place2)._Distance__kilometers)
  
  return {"distance":dis}
