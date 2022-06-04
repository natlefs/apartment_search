from dataclasses import dataclass
from typing import Union

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

from finn_apartment_search.utils import Location, StopPlace

HOST = "https://api.entur.io/journey-planner/v3/graphql"


@dataclass
class ItinerarySearchParameters:
    start: Union[Location, StopPlace]
    stop: Union[Location, StopPlace]
    transfer_limit: int

    def gql(self):
        return {
            "source": self.start.gql(),
            "destination": self.stop.gql(),
            "transferLimit": self.transfer_limit
        }


def filter_itinerary(self, props: ItinerarySearchParameters, max_length: int):
    trip_time = get_itinerary(props)
    return trip_time <= max_length


def get_itinerary(props: ItinerarySearchParameters) -> int:

    transport = AIOHTTPTransport(url=HOST, headers={"ET-Client-Name": "jkbn-finntur"})
    client = Client(transport=transport, fetch_schema_from_transport=True)
    query = gql("""
        query getItinerary(
            $source: Location!,
            $destination: Location!,
            $transferLimit: Int!,

        ){
        trip(
            from: $source
            to: $destination
            numTripPatterns: 5
            dateTime: "2022-04-27T08:30:34.284+01:00"
            walkSpeed: 1.67
            arriveBy: false
            transferPenalty: 480
            maximumTransfers: $transferLimit
        )

        {
            tripPatterns {
            expectedStartTime
            expectedEndTime
            duration
            walkDistance
            legs {
                mode
                distance
                line {
                id
                publicCode
                }
            }
            }
        }
        }
    """)
    
    response = client.execute(query, variable_values=props.gql())
    routes = response['trip']['tripPatterns']
    if len(routes) > 0:
        return routes[0]['duration']
