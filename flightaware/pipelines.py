# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from mongoengine import connect
from db.models import Airport, Route


class FlightawarePipeline(object):
    collection_name = 'routes'

    def process_item(self, item, spider):
        flight = list(item['data']['flights'].values())[0]

        airports = {}
        
        for airport_key in ('origin', 'destination'):
            origin = flight[airport_key]

            # Check if airport already exists, so it can be updated
            airport = Airport.objects(iata=origin['iata']).first()

            if airport is None:
                airport = Airport(iata=origin['iata'])

            airport.icao = origin['icao']
            airport.name = origin['friendlyName']
            airport.location = origin['friendlyLocation']
            airport.longitude = origin['coord'][0]
            airport.latitude = origin['coord'][1]

            airport.save()

            airports[airport_key] = airport

        route_data = flight['codeShare']

        route = Route.objects(iata=route_data['iataIdent']).first()

        if route is None:
            route = Route(iata=route_data['iataIdent'])

        route.origin = airports['origin']
        route.destination = airports['destination']
        route.aircraft = flight['aircraft']['type']

        route.save()

        # Return route here to pass it to the next pipeline item which prints it
        return item['route']
