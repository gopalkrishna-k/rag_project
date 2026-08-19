from vector_store import collection


records = collection.get(
    include=["metadatas"]
)


bikes = set()


for metadata in records["metadatas"]:

    bike = metadata.get("bike")

    if bike:
        bikes.add(bike)


print("Bikes in document:")

for bike in sorted(bikes):
    print("-", bike)
