from pydantic import BaseModel
from typing import List, Optional

class ItineraryDay(BaseModel):
    day_number: int
    location: str
    date: str
    departure_time: Optional[str] = None

class Cabin(BaseModel):
    cabinType: Optional[str] = None
    grade: Optional[str] = None
    gradeName: Optional[str] = None
    description: Optional[str] = None
    deck: Optional[str] = None
    price: Optional[str] = None

class CruiseData(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    shipName: Optional[str] = None
    destinationName: Optional[str] = None
    departureCountry: Optional[str] = None
    arrivalCountry: Optional[str] = None
    departureDate: Optional[str] = None
    arrivalDate: Optional[str] = None
    duration: Optional[str] = None
    itinerary: List[ItineraryDay] = []
    cabins: List[Cabin] = []
