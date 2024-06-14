from cassandra.cluster import Cluster
cluster = Cluster(
    contact_points=[
    ('127.0.0.1', 9042),
    ('127.0.0.1', 9043)
    ]
)
session = cluster.connect('flights_system')