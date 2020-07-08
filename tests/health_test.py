import unittest
import sys
import os

sys.path.append(os.getcwd() + '/pygate_grpc')

import health
import proto.health_rpc_pb2 as health_rpc_pb2

class TestHealth(unittest.TestCase):

    # Consider create a mock server here, currently we need to spin up local net
    def test_check(self):
        client = health.HealthClient("127.0.0.1:5002")
        status = client.check()
        self.assertEqual(status, health_rpc_pb2.STATUS_OK)


if __name__ == '__main__':
    unittest.main()
