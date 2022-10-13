# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: lifecycle.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0flifecycle.proto\"2\n\x13\x45nvironmentVariable\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"o\n\x12ModelConfiguration\x12\x0f\n\x07modelID\x18\x01 \x01(\t\x12\x14\n\x0c\x63ontainerURL\x18\x02 \x01(\t\x12\x32\n\x14\x65nvironmentVariables\x18\x03 \x03(\x0b\x32\x14.EnvironmentVariable\"l\n\x0c\x44\x65ployModels\x12\x13\n\x0bsimulatorId\x18\x01 \x01(\t\x12\x30\n\x13modelConfigurations\x18\x02 \x03(\x0b\x32\x13.ModelConfiguration\x12\x15\n\rkeepLogsHours\x18\x03 \x01(\x01\"\x14\n\x12ReadyForProcessing\"\r\n\x0bModelsReady\"*\n\x0fModelParameters\x12\x17\n\x0fparameters_dict\x18\x01 \x01(\t\"\x0e\n\x0cParametrized\"\"\n\x07NewStep\x12\x17\n\x0fparameters_dict\x18\x01 \x01(\t\"\x12\n\x10\x43\x61lculationsDone\"&\n\rErrorOccurred\x12\x15\n\rerror_message\x18\x01 \x01(\t\"\x10\n\x0eSimulationDone\"7\n\x0eUnhealthyModel\x12%\n\x06status\x18\x01 \x01(\x0e\x32\x15.UnhealthyModelStatus\"J\n\x12ModelHasTerminated\x12\"\n\x06status\x18\x01 \x01(\x0e\x32\x12.TerminationStatus\x12\x10\n\x08\x65xitCode\x18\x02 \x01(\x05\"\x19\n\x17\x41llModelsHaveTerminated*&\n\x14UnhealthyModelStatus\x12\x0e\n\nNOPROGRESS\x10\x00*0\n\x11TerminationStatus\x12\x0f\n\x0bSUCCESSFULL\x10\x00\x12\n\n\x06\x46\x41ILED\x10\x01\x62\x06proto3')

_UNHEALTHYMODELSTATUS = DESCRIPTOR.enum_types_by_name['UnhealthyModelStatus']
UnhealthyModelStatus = enum_type_wrapper.EnumTypeWrapper(_UNHEALTHYMODELSTATUS)
_TERMINATIONSTATUS = DESCRIPTOR.enum_types_by_name['TerminationStatus']
TerminationStatus = enum_type_wrapper.EnumTypeWrapper(_TERMINATIONSTATUS)
NOPROGRESS = 0
SUCCESSFULL = 0
FAILED = 1


_ENVIRONMENTVARIABLE = DESCRIPTOR.message_types_by_name['EnvironmentVariable']
_MODELCONFIGURATION = DESCRIPTOR.message_types_by_name['ModelConfiguration']
_DEPLOYMODELS = DESCRIPTOR.message_types_by_name['DeployModels']
_READYFORPROCESSING = DESCRIPTOR.message_types_by_name['ReadyForProcessing']
_MODELSREADY = DESCRIPTOR.message_types_by_name['ModelsReady']
_MODELPARAMETERS = DESCRIPTOR.message_types_by_name['ModelParameters']
_PARAMETRIZED = DESCRIPTOR.message_types_by_name['Parametrized']
_NEWSTEP = DESCRIPTOR.message_types_by_name['NewStep']
_CALCULATIONSDONE = DESCRIPTOR.message_types_by_name['CalculationsDone']
_ERROROCCURRED = DESCRIPTOR.message_types_by_name['ErrorOccurred']
_SIMULATIONDONE = DESCRIPTOR.message_types_by_name['SimulationDone']
_UNHEALTHYMODEL = DESCRIPTOR.message_types_by_name['UnhealthyModel']
_MODELHASTERMINATED = DESCRIPTOR.message_types_by_name['ModelHasTerminated']
_ALLMODELSHAVETERMINATED = DESCRIPTOR.message_types_by_name['AllModelsHaveTerminated']
EnvironmentVariable = _reflection.GeneratedProtocolMessageType('EnvironmentVariable', (_message.Message,), {
  'DESCRIPTOR' : _ENVIRONMENTVARIABLE,
  '__module__' : 'lifecycle_pb2'
  # @@protoc_insertion_point(class_scope:EnvironmentVariable)
  })
_sym_db.RegisterMessage(EnvironmentVariable)

ModelConfiguration = _reflection.GeneratedProtocolMessageType('ModelConfiguration', (_message.Message,), {
  'DESCRIPTOR' : _MODELCONFIGURATION,
  '__module__' : 'lifecycle_pb2'
  # @@protoc_insertion_point(class_scope:ModelConfiguration)
  })
_sym_db.RegisterMessage(ModelConfiguration)

DeployModels = _reflection.GeneratedProtocolMessageType('DeployModels', (_message.Message,), {
  'DESCRIPTOR' : _DEPLOYMODELS,
  '__module__' : 'lifecycle_pb2'
  # @@protoc_insertion_point(class_scope:DeployModels)
  })
_sym_db.RegisterMessage(DeployModels)

ReadyForProcessing = _reflection.GeneratedProtocolMessageType('ReadyForProcessing', (_message.Message,), {
  'DESCRIPTOR' : _READYFORPROCESSING,
  '__module__' : 'lifecycle_pb2'
  # @@protoc_insertion_point(class_scope:ReadyForProcessing)
  })
_sym_db.RegisterMessage(ReadyForProcessing)

ModelsReady = _reflection.GeneratedProtocolMessageType('ModelsReady', (_message.Message,), {
  'DESCRIPTOR' : _MODELSREADY,
  '__module__' : 'lifecycle_pb2'
  # @@protoc_insertion_point(class_scope:ModelsReady)
  })
_sym_db.RegisterMessage(ModelsReady)

ModelParameters = _reflection.GeneratedProtocolMessageType('ModelParameters', (_message.Message,), {
  'DESCRIPTOR' : _MODELPARAMETERS,
  '__module__' : 'lifecycle_pb2'
  # @@protoc_insertion_point(class_scope:ModelParameters)
  })
_sym_db.RegisterMessage(ModelParameters)

Parametrized = _reflection.GeneratedProtocolMessageType('Parametrized', (_message.Message,), {
  'DESCRIPTOR' : _PARAMETRIZED,
  '__module__' : 'lifecycle_pb2'
  # @@protoc_insertion_point(class_scope:Parametrized)
  })
_sym_db.RegisterMessage(Parametrized)

NewStep = _reflection.GeneratedProtocolMessageType('NewStep', (_message.Message,), {
  'DESCRIPTOR' : _NEWSTEP,
  '__module__' : 'lifecycle_pb2'
  # @@protoc_insertion_point(class_scope:NewStep)
  })
_sym_db.RegisterMessage(NewStep)

CalculationsDone = _reflection.GeneratedProtocolMessageType('CalculationsDone', (_message.Message,), {
  'DESCRIPTOR' : _CALCULATIONSDONE,
  '__module__' : 'lifecycle_pb2'
  # @@protoc_insertion_point(class_scope:CalculationsDone)
  })
_sym_db.RegisterMessage(CalculationsDone)

ErrorOccurred = _reflection.GeneratedProtocolMessageType('ErrorOccurred', (_message.Message,), {
  'DESCRIPTOR' : _ERROROCCURRED,
  '__module__' : 'lifecycle_pb2'
  # @@protoc_insertion_point(class_scope:ErrorOccurred)
  })
_sym_db.RegisterMessage(ErrorOccurred)

SimulationDone = _reflection.GeneratedProtocolMessageType('SimulationDone', (_message.Message,), {
  'DESCRIPTOR' : _SIMULATIONDONE,
  '__module__' : 'lifecycle_pb2'
  # @@protoc_insertion_point(class_scope:SimulationDone)
  })
_sym_db.RegisterMessage(SimulationDone)

UnhealthyModel = _reflection.GeneratedProtocolMessageType('UnhealthyModel', (_message.Message,), {
  'DESCRIPTOR' : _UNHEALTHYMODEL,
  '__module__' : 'lifecycle_pb2'
  # @@protoc_insertion_point(class_scope:UnhealthyModel)
  })
_sym_db.RegisterMessage(UnhealthyModel)

ModelHasTerminated = _reflection.GeneratedProtocolMessageType('ModelHasTerminated', (_message.Message,), {
  'DESCRIPTOR' : _MODELHASTERMINATED,
  '__module__' : 'lifecycle_pb2'
  # @@protoc_insertion_point(class_scope:ModelHasTerminated)
  })
_sym_db.RegisterMessage(ModelHasTerminated)

AllModelsHaveTerminated = _reflection.GeneratedProtocolMessageType('AllModelsHaveTerminated', (_message.Message,), {
  'DESCRIPTOR' : _ALLMODELSHAVETERMINATED,
  '__module__' : 'lifecycle_pb2'
  # @@protoc_insertion_point(class_scope:AllModelsHaveTerminated)
  })
_sym_db.RegisterMessage(AllModelsHaveTerminated)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _UNHEALTHYMODELSTATUS._serialized_start=665
  _UNHEALTHYMODELSTATUS._serialized_end=703
  _TERMINATIONSTATUS._serialized_start=705
  _TERMINATIONSTATUS._serialized_end=753
  _ENVIRONMENTVARIABLE._serialized_start=19
  _ENVIRONMENTVARIABLE._serialized_end=69
  _MODELCONFIGURATION._serialized_start=71
  _MODELCONFIGURATION._serialized_end=182
  _DEPLOYMODELS._serialized_start=184
  _DEPLOYMODELS._serialized_end=292
  _READYFORPROCESSING._serialized_start=294
  _READYFORPROCESSING._serialized_end=314
  _MODELSREADY._serialized_start=316
  _MODELSREADY._serialized_end=329
  _MODELPARAMETERS._serialized_start=331
  _MODELPARAMETERS._serialized_end=373
  _PARAMETRIZED._serialized_start=375
  _PARAMETRIZED._serialized_end=389
  _NEWSTEP._serialized_start=391
  _NEWSTEP._serialized_end=425
  _CALCULATIONSDONE._serialized_start=427
  _CALCULATIONSDONE._serialized_end=445
  _ERROROCCURRED._serialized_start=447
  _ERROROCCURRED._serialized_end=485
  _SIMULATIONDONE._serialized_start=487
  _SIMULATIONDONE._serialized_end=503
  _UNHEALTHYMODEL._serialized_start=505
  _UNHEALTHYMODEL._serialized_end=560
  _MODELHASTERMINATED._serialized_start=562
  _MODELHASTERMINATED._serialized_end=636
  _ALLMODELSHAVETERMINATED._serialized_start=638
  _ALLMODELSHAVETERMINATED._serialized_end=663
# @@protoc_insertion_point(module_scope)
