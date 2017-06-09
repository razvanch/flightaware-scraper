from mongoengine import connect, Document, StringField, FloatField, ReferenceField


class Airport(Document):
    """
    Airport document structure
    """
    iata = StringField(required=True)
    icao = StringField()
    name = StringField()
    location = StringField()
    latitude = FloatField()
    longitude = FloatField()

class Route(Document):
    """
    Route document structure
    """
    iata = StringField(required=True)
    origin = ReferenceField(Airport)
    destination = ReferenceField(Airport)
    aircraft = StringField()

# Connects to the flightaware database - make sure you have a mongo service
# running on localhost!
connect('flightaware')
