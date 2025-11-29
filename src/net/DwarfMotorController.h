#pragma once

#include "DwarfWebSocketClient.h"
#include "motor.pb.h"

#include <QObject>

class DwarfMotorController : public QObject {
  Q_OBJECT

public:
  enum class Axis { Azimuth = 0, Altitude = 1 };

  explicit DwarfMotorController(QObject *parent = nullptr);

  void setClient(DwarfWebSocketClient *client);

  void runMotor(Axis axis, bool directionRightOrUp, double speed,
                int speedRamping = 100, int resolutionLevel = 0);
  void stopMotor(Axis axis);

signals:
  void errorOccurred(const QString &message);

private:
  DwarfWebSocketClient *m_client;

  quint32 moduleId() const;
  quint32 cmdRun() const;
  quint32 cmdStop() const;
};
