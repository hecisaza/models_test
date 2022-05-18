from datetime import datetime, timezone
from doctest import testfile
from enum import Enum
from optparse import Option
from pydantic import BaseModel, Field, constr
from pydantic.dataclasses import dataclass
from ipaddress import IPv4Address
from typing import Optional, Literal


input_data = {
    "data": {
        "host": "1120lab-2821-111-gw",
        "ip": "5.5.5.5",
        "device_type": "fabric_edges",
        "vendor_name": "Cisco",
        "description": "IP 5555 with fabric_edges device",
        "server_data": {
            "radius": {
                "attributes": {"Wired_Default_Action": "Open"},
                "secret": "Compl3x",
            },
            "tacacs": {
                "attributes": {
                                "open": "Default",
                                "network_device_group": "Build",
                                "environment": "Build",
                                "managed_by": "Atos"
                              },
                "secret": "Test123",
                "group": "SDA - Cisco Wired Devices",
            },
        },
    }
}
NOW_ISO = datetime.now().replace(tzinfo=timezone.utc).isoformat()

#############################################################
# Attributes Models 
#############################################################

class AttributesRadius(BaseModel):
    Wired_Default_Action: str

class AttributesTacacsData(BaseModel):
    open: str
    network_device_group: Literal["Build", "Test", "Production", "Lab", "MSP", "Designated", "Network"]
    managed_by: Literal["Atos","Presidio"]
    environment: Literal["Build", "Production"]

#############################################################
# TacacsData Model
#############################################################

class TacacsData(BaseModel):
    attributes: AttributesTacacsData
    secret: constr(max_length=128)
    group: Literal["SDA - Cisco Wired Devices", "Cisco"]

#############################################################
# RadiusData Model
#############################################################

class RadiusData(BaseModel):
    attributes: AttributesRadius
    secret: str

class ServerData(BaseModel):
    radius: RadiusData
    tacacs: TacacsData

class ClearpassRegisterData(BaseModel):
    host: constr(regex=r'\w')
    ip: IPv4Address
    device_type: Literal["fabric_edges", "borders"]
    vendor_name: Literal["Cisco"]
    description: constr(max_length=1024)
    server_data: ServerData


class ClearPassRegister(BaseModel):
    data: ClearpassRegisterData
    print(f"Printed on Clear Pass")



test = ClearPassRegister(data=input_data["data"])
print(test)
