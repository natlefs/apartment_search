from dataclasses import dataclass

@dataclass
class Location:
    lat: str
    lon: str

    def gql(this):
        return {
            "coordinates": {
                "latitude": float(this.lat),
                "longitude": float(this.lon)
            }
        }

@dataclass
class StopPlace:
    """https://developer.entur.org/pages-nsr-nsr"""
    nsr_code: str
    name: str

    def gql(this):
        return {
            "place": this.nsr_code
        }

WORK = Location('59.9', '10.8')
LILLESTROM = Location('59.9551798', '11.0419991')
OSLO_SOUTH = Location('59.877947', '10.820198')
