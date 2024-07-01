import unittest
import base64
from simulation_orchestrator.parse_esdl import get_model_list
from rest.schemas.simulation_schemas import CalculationService

class TestParse(unittest.TestCase):

    def test_get_model_list(self):

        # Arrange
        with open("test/test.esdl", mode="r") as esdl_file:
            encoded_base64_esdl = base64.b64encode(esdl_file.read().encode('utf-8')).decode("utf-8")
        
        calculation_service_energy_system = CalculationService()
        calculation_service_energy_system.esdl_type = "EnergySystem"
        calculation_service_energy_system.calc_service_name = "test2_energy_system_service"
        calculation_service_energy_system.service_image_url = "dotsenergyframework/test2_energy_system_service:0.0.1"
        calculation_service_energy_system.nr_of_models = 1

        calculation_service_pv_installation = CalculationService()
        calculation_service_pv_installation.esdl_type = "PVInstallation"
        calculation_service_pv_installation.calc_service_name = "test2_pv_installation_service"
        calculation_service_pv_installation.service_image_url = "dotsenergyframework/test2_pv_installation_service:0.0.1"
        calculation_service_pv_installation.nr_of_models = 2

        calculation_service_e_connection = CalculationService()
        calculation_service_e_connection.esdl_type = "EConnection"
        calculation_service_e_connection.calc_service_name = "test2_econnection_service"
        calculation_service_e_connection.service_image_url = "dotsenergyframework/test2_econnection_service:0.0.1"
        calculation_service_e_connection.nr_of_models = 1

        expected_pv_installation_ids = [
            '1830a516-fae5-4cc7-99bd-6e9a5d175a80',
            '176af591-6d9d-4751-bb0f-fac7e99b1c3d',
            'b8766109-5328-416f-9991-e81a5cada8a6',
            '529aca74-b8da-4489-9d76-1b2320aa3f40',
            '2113dfc3-08d4-40df-8e76-9e53a55d3342',
            'fdfd4af3-570b-4b81-ac5f-46ca1e687764',
            '2d81c891-40e7-46c4-bedc-44421085a7a6',
            'd6ccc94f-876c-4c6a-9917-8a3fa6975dc2',
            '0f2fc1a6-db36-40a4-932f-31d4fddeac42',
            '4ba625a0-78bd-495a-83cd-726f52befcd7',
            'd4af44ac-aab8-40b3-868c-0668bdb1d9f2',
            '6b22f9d6-c184-4ebf-bfd7-804dd2d56f60',
            'afc87f44-b232-462c-9103-01867dee800b',
            '10f2b7e1-0da7-4d46-93a5-696cc01ef07e',
            '2ff29e6c-4136-4a12-9dec-85e60d64f990'
        ]

        expected_e_connection_ids = [
            'e1b3dc89-cee8-4f8e-81ce-a0cb6726c17e',
            'f006d594-0743-4de5-a589-a6c2350898da',
            'f3857348-cbd8-4a89-9e37-cbcf67e649d7',
            'e8711505-2744-48e9-b863-b7bd58722d3b',
            '51dd7fc3-323f-4262-b7ef-64c38ba59f8f'
        ]

        expected_energysystem_ids = [
            '37e0284d-29f8-453e-91ec-2e7e02b5c16d'
        ]

        calculation_services = [
            calculation_service_energy_system,
            calculation_service_pv_installation,
            calculation_service_e_connection
        ]

        # Execute
        model_list = get_model_list(calculation_services, encoded_base64_esdl.decode('utf-8'))

        # Assert
        self.assertEqual(sum([calculation_service_e_connection.nr_of_models, calculation_service_pv_installation.nr_of_models, calculation_service_energy_system.nr_of_models]), len(model_list))
        energy_system_models = [model for model in model_list if model.calc_service_name == calculation_service_energy_system.calc_service_name]
        pv_installation_models = [model for model in model_list if model.calc_service_name == calculation_service_pv_installation.calc_service_name]
        e_connection_models = [model for model in model_list if model.calc_service_name == calculation_service_e_connection.calc_service_name]

        first_pv_installation_model = pv_installation_models[0]
        second_pv_installation_model = pv_installation_models[1]

        # Assert correct assets are extracted from esdl file
        self.assertListEqual(expected_e_connection_ids, e_connection_models[0].esdl_ids)
        self.assertListEqual(expected_energysystem_ids, energy_system_models[0].esdl_ids)
        self.assertListEqual(expected_pv_installation_ids, first_pv_installation_model.esdl_ids + second_pv_installation_model.esdl_ids)

        # Assert correct amount of models
        self.assertEqual(calculation_service_energy_system.nr_of_models, len(energy_system_models))
        self.assertEqual(calculation_service_pv_installation.nr_of_models, len(pv_installation_models))
        self.assertEqual(calculation_service_e_connection.nr_of_models, len(e_connection_models))

        # Assert esdl ids are seperated in different moddels
        for esdl_id in first_pv_installation_model.esdl_ids:
            self.assertNotIn(esdl_id, second_pv_installation_model.esdl_ids)

if __name__ == '__main__':
    unittest.main()