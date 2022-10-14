from datetime import datetime

from esdl import esdl
from esdl.esdl_handler import EnergySystemHandler
from base64 import b64decode, b64encode
from typing import Dict, Type
import json
import uuid


# with open("test_file.esdl", "rb") as esdl_file:
#     esdl_base64string = b64encode(esdl_file.read()).decode("utf-8")
#
# esdl_string = b64decode(esdl_base64string + b"==".decode("utf-8")).decode("utf-8")
# # print(esdl_string)
#
esh = EnergySystemHandler()
esh.load_file("minimal_es_GOe.esdl")
# esh.load_from_string(esdl_string)
energy_system = esh.get_energy_system()

calc_service_image_urls: Dict[Type[esdl.EnergyAsset], str] = {
    esdl.PVPanel: "pvpanel_service_url",
    esdl.PVPark: "evchargingstation_service_url",
    esdl.ElectricityNetwork: "electricitynetwork_service_url",
}

models_input = []
# Iterate over all contents of an EnergySystem
print(f"{energy_system.id}, {type(energy_system).__name__}")
for obj in energy_system.eAllContents():
    if hasattr(obj, 'id'):
        obj_id = obj.id
    else:
        obj_id = ''
    print(f"{type(obj).__name__}, {obj_id}")
    # # Filter out EnergyAssets (which have ports)
    # if isinstance(obj, tuple(calc_service_image_urls)):
    #     receiving_services = {}
    #     # Iterate over all ports of this asset
    #     for port in obj.port:
    #         # only InPorts to find connected receiving services
    #         if isinstance(port, esdl.InPort):
    #             # Iterate over all connected ports of this port
    #             for ct_port in port.connectedTo:
    #                 # Get the asset to which the connected port belongs to
    #                 ct_asset = ct_port.eContainer()
    #                 # print(
    #                 #     f"{type(obj).__name__}, {obj.name}, {obj.id} connected to: {ct_asset.name}, {ct_asset.id}"
    #                 # )
    #                 if type(ct_asset).__name__ not in tuple(receiving_services):
    #                     receiving_services[type(ct_asset).__name__] = {
    #                         "number_of": 1,
    #                         "model_ids": [ct_asset.id],
    #                     }
    #                 else:
    #                     receiving_services[type(ct_asset).__name__]["number_of"] += 1
    #                     receiving_services[type(ct_asset).__name__]["model_ids"].append(
    #                         ct_asset.id
    #                     )
    #
    #     print(json.dumps(receiving_services))
    #     models_input.append(
    #         {
    #             "service_name": type(obj).__name__,
    #             "image_url": calc_service_image_urls[type(obj)],
    #             "model_id": obj.id,
    #             "model_parameters": {},
    #             "receiving_services": receiving_services,
    #         }
    #     )
    # elif isinstance(obj, esdl.EnergyAsset):
    #     print(
    #         f"No Calculation Service found for ESDL Asset Type: {type(obj).__name__}"
    #     )

print(json.dumps(models_input, indent=2))
