from fastapi import APIRouter
from geopy.geocoders import Nominatim
from geopy import distance
from Model import schemas





router = APIRouter()



@router.post('/distance_finder',tags=['ZIPCODE_VALIDATION'])
def d_finder(code:schemas.AZA_geocode):
  geocoder =Nominatim(user_agent='python')
  location1=code.pin1
  location2=code.pin2
  cor1 =geocoder.geocode(location1)
  cor2 =geocoder.geocode(location2)
  lat1,log1 =(cor1.latitude),(cor1.longitude)
  lat2,log2 =(cor2.latitude),(cor2.longitude)
  place1=(lat1,log1)
  place2=(lat2,log2)
  
  
    
  return {"distance":distance.distance(place1,place2)._Distance__kilometers}
