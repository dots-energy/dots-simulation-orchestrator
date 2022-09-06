# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: healthcheck.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11healthcheck.proto\"b\n\x14PingHealthESSIMToMSO\x12\x1e\n\x07healthy\x18\x01 \x01(\x0e\x32\r.HealthStatus\x12\x0f\n\x07reasons\x18\x02 \x03(\t\x12\x19\n\x11\x61\x63tiveSimulations\x18\x03 \x03(\t\"G\n\x14PongHealthMSOToEssim\x12\x1e\n\x07healthy\x18\x01 \x01(\x0e\x32\r.HealthStatus\x12\x0f\n\x07reasons\x18\x02 \x03(\t\"G\n\x14PingHealthMSOToModel\x12\x1e\n\x07healthy\x18\x01 \x01(\x0e\x32\r.HealthStatus\x12\x0f\n\x07reasons\x18\x02 \x03(\t\"z\n\x14PongHealthModelToMSO\x12\x1e\n\x07healthy\x18\x01 \x01(\x0e\x32\r.HealthStatus\x12\x0f\n\x07reasons\x18\x02 \x03(\t\x12\x14\n\x0cnumberOfBids\x18\x03 \x01(\x05\x12\x1b\n\x13numberOfAllocations\x18\x04 \x01(\x05**\n\x0cHealthStatus\x12\x0b\n\x07HEALTHY\x10\x00\x12\r\n\tUNHEALTHY\x10\x01\x62\x06proto3')

_HEALTHSTATUS = DESCRIPTOR.enum_types_by_name['HealthStatus']
HealthStatus = enum_type_wrapper.EnumTypeWrapper(_HEALTHSTATUS)
HEALTHY = 0
UNHEALTHY = 1


_PINGHEALTHESSIMTOMSO = DESCRIPTOR.message_types_by_name['PingHealthESSIMToMSO']
_PONGHEALTHMSOTOESSIM = DESCRIPTOR.message_types_by_name['PongHealthMSOToEssim']
_PINGHEALTHMSOTOMODEL = DESCRIPTOR.message_types_by_name['PingHealthMSOToModel']
_PONGHEALTHMODELTOMSO = DESCRIPTOR.message_types_by_name['PongHealthModelToMSO']
PingHealthESSIMToMSO = _reflection.GeneratedProtocolMessageType('PingHealthESSIMToMSO', (_message.Message,), {
  'DESCRIPTOR' : _PINGHEALTHESSIMTOMSO,
  '__module__' : 'healthcheck_pb2'
  # @@protoc_insertion_point(class_scope:PingHealthESSIMToMSO)
  })
_sym_db.RegisterMessage(PingHealthESSIMToMSO)

PongHealthMSOToEssim = _reflection.GeneratedProtocolMessageType('PongHealthMSOToEssim', (_message.Message,), {
  'DESCRIPTOR' : _PONGHEALTHMSOTOESSIM,
  '__module__' : 'healthcheck_pb2'
  # @@protoc_insertion_point(class_scope:PongHealthMSOToEssim)
  })
_sym_db.RegisterMessage(PongHealthMSOToEssim)

PingHealthMSOToModel = _reflection.GeneratedProtocolMessageType('PingHealthMSOToModel', (_message.Message,), {
  'DESCRIPTOR' : _PINGHEALTHMSOTOMODEL,
  '__module__' : 'healthcheck_pb2'
  # @@protoc_insertion_point(class_scope:PingHealthMSOToModel)
  })
_sym_db.RegisterMessage(PingHealthMSOToModel)

PongHealthModelToMSO = _reflection.GeneratedProtocolMessageType('PongHealthModelToMSO', (_message.Message,), {
  'DESCRIPTOR' : _PONGHEALTHMODELTOMSO,
  '__module__' : 'healthcheck_pb2'
  # @@protoc_insertion_point(class_scope:PongHealthModelToMSO)
  })
_sym_db.RegisterMessage(PongHealthModelToMSO)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _HEALTHSTATUS._serialized_start=391
  _HEALTHSTATUS._serialized_end=433
  _PINGHEALTHESSIMTOMSO._serialized_start=21
  _PINGHEALTHESSIMTOMSO._serialized_end=119
  _PONGHEALTHMSOTOESSIM._serialized_start=121
  _PONGHEALTHMSOTOESSIM._serialized_end=192
  _PINGHEALTHMSOTOMODEL._serialized_start=194
  _PINGHEALTHMSOTOMODEL._serialized_end=265
  _PONGHEALTHMODELTOMSO._serialized_start=267
  _PONGHEALTHMODELTOMSO._serialized_end=389
# @@protoc_insertion_point(module_scope)
