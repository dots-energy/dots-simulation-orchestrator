from io import BytesIO
import unittest
from unittest.mock import MagicMock
import zipfile
from dots_infrastructure.test_infra.InfluxDBMock import InfluxDBMock
from influxdb.resultset import ResultSet

from simulation_orchestrator.data_handler.data_handler import DataHandler

class TestActions(unittest.TestCase):

    def setUp(self):
        self.data_handler = DataHandler(InfluxDBMock())
        self.measurements_series = {
                    'series' : [
                        { 
                            "columns" : ["name"],
                            "values" : [["EConnection"], ["PVInstallation"]]
                        }
                    ]
                }

    def test_when_query_returns_no_data_none_is_returned(self):
        # Arrange
        def test_query_function(query):
            measurement_series = {}
            if query == 'SHOW MEASUREMENTS ON "test"':
                measurement_series = self.measurements_series
            return ResultSet(measurement_series)

        self.data_handler.influxdb_connector.query = test_query_function

        # Execute
        zip_file = self.data_handler.get_all_data_for_simulation_id("test-id")

        # assert
        self.assertIsNone(zip_file)

    def test_when_query_returns_data_zip_is_generated(self):
        # Arrange        
        test_simulation_id = "test-id"
        def test_query_function(query):
            measurement_series ={}
            if query == 'SHOW MEASUREMENTS ON "test"':
                measurement_series = measurement_series = self.measurements_series
            elif query == f"SELECT * FROM \"PVInstallation\" WHERE simulation_id = \'{test_simulation_id}\'":
                measurement_series = {
                    'series' : [
                        { 
                            "measurement" : "PVInstallation",
                            "columns" : ["model_id", "simulation_id", "Dispatch"],
                            "values" : [["test-d", "test-id", 1.0], ["test-d", "test-id", 1.0]]
                        }
                    ]
                }
            elif query == f"SELECT * FROM \"EConnection\" WHERE simulation_id = \'{test_simulation_id}\'":
                measurement_series = {
                    'series' : [
                        { 
                            "measurement" : "EConnection",
                            "columns" : ["model_id", "simulation_id", "Dispatch"],
                            "values" : [["test-d", "test-id", 1.0], ["test-d", "test-id", 1.0]]
                        }
                    ]
                }

            return ResultSet(measurement_series)

        self.data_handler.influxdb_connector.query = test_query_function
        expected_filenames = [
            f'{test_simulation_id}_EConnection.csv',
            f'{test_simulation_id}_PVInstallation.csv',
        ]

        # Execute
        zip_file = self.data_handler.get_all_data_for_simulation_id(test_simulation_id)

        # assert
        self.assertTrue(zipfile.is_zipfile(zip_file))

        with zipfile.ZipFile(zip_file) as zip_archive:
            self.assertIsNone(zip_archive.testzip())
            self.assertListEqual(sorted(zip_archive.namelist()), expected_filenames)

if __name__ == '__main__':
    unittest.main()