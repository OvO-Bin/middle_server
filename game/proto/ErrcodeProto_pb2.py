# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ErrcodeProto.proto

from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='ErrcodeProto.proto',
  package='com.woke.proto',
  serialized_pb='\n\x12\x45rrcodeProto.proto\x12\x0e\x63om.woke.proto*\xb7\x01\n\x07\x45rrcode\x12\x10\n\x0bUNKNOWN_ERR\x10\xe7\x07\x12\x0b\n\x07SUCCESS\x10\x00\x12\x0f\n\x0bSERVER_BUSY\x10\x01\x12\x11\n\rVERSION_LOWER\x10\x02\x12\x12\n\x0eUSER_NOT_EXSIT\x10\x03\x12\x14\n\x10USER_PWD_INVALID\x10\x04\x12\x12\n\x0eUSER_HAD_EXSIT\x10\x05\x12\x12\n\x0eROLE_NOT_EXSIT\x10\x06\x12\x17\n\x13ROLE_NICKNAME_EXIST\x10\x07')

_ERRCODE = _descriptor.EnumDescriptor(
  name='Errcode',
  full_name='com.woke.proto.Errcode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_ERR', index=0, number=999,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=1, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SERVER_BUSY', index=2, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VERSION_LOWER', index=3, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='USER_NOT_EXSIT', index=4, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='USER_PWD_INVALID', index=5, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='USER_HAD_EXSIT', index=6, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ROLE_NOT_EXSIT', index=7, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ROLE_NICKNAME_EXIST', index=8, number=7,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=39,
  serialized_end=222,
)

Errcode = enum_type_wrapper.EnumTypeWrapper(_ERRCODE)
UNKNOWN_ERR = 999
SUCCESS = 0
SERVER_BUSY = 1
VERSION_LOWER = 2
USER_NOT_EXSIT = 3
USER_PWD_INVALID = 4
USER_HAD_EXSIT = 5
ROLE_NOT_EXSIT = 6
ROLE_NICKNAME_EXIST = 7




# @@protoc_insertion_point(module_scope)