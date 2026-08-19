from vector_store import collection


def get_bike_names():

    records = collection.get(
        include=["metadatas"]
    )

    bikes = set()

    for metadata in records["metadatas"]:

        bike = metadata.get("bike")

        if bike:
            bikes.add(bike)

    return sorted(bikes)


def detect_bikes(query: str):

    bikes = get_bike_names()

    query_lower = query.lower()

    detected_bikes = []

    for bike in bikes:

        if bike.lower() in query_lower:
            detected_bikes.append(bike)

    return detected_bikes
