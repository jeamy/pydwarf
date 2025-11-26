#pragma once

#include <QByteArray>
#include <google/protobuf/message.h>

class ProtobufHelper {
public:
  static QByteArray serialize(const google::protobuf::Message &message);

  template <typename T>
  static bool parse(const QByteArray &data, T &message) {
    if (!message.ParseFromArray(data.constData(), data.size())) {
      return false;
    }
    return true;
  }
};
