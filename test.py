from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
import unittest

cluster = Cluster(
    contact_points=[
      ('127.0.0.1', 9042),
      ('127.0.0.1', 9043),
      ('127.0.0.1', 9044)
    ]
)
session = cluster.connect('flights')

class CassandraTests(unittest.TestCase):
    def test_connect(self):
        self.assertEqual(session.keyspace, 'flights')
        
        

if __name__ == '__main__':
    unittest.main()
