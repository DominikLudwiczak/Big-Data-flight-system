from cassandra.cluster import Cluster
from cassandra.query import BatchStatement


class Connect:
    def __init__(self):
        self.cluster = Cluster(
            contact_points=[
            ('127.0.0.1', 9042),
            ('127.0.0.1', 9043),
            ('127.0.0.1', 9044)
            ]
        )
        self.connect('flights_system')

    def connect(self, keyspace_name):
        metadata = self.cluster.metadata
        if keyspace_name not in metadata.keyspaces:
            keyspace_name = None
        self.session = self.cluster.connect(keyspace_name)

    def execute(self, query):
        return self.session.execute(query)
    
    def get_cluster(self):
        return self.cluster

    def get_session(self):
        return self.session
    
    def close(self):
        self.cluster.shutdown()
    