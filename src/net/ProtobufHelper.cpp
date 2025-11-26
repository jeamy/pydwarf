#include "ProtobufHelper.h"

QByteArray ProtobufHelper::serialize(const google::protobuf::Message &message) {
  std::string serialized = message.SerializeAsString();
  return QByteArray(serialized.data(), static_cast<int>(serialized.size()));
}
