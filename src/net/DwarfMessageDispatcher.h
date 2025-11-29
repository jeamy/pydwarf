#pragma once

#include <QByteArray>
#include <QObject>
#include <cstdint>

class DwarfMessageDispatcher : public QObject {
  Q_OBJECT

public:
  explicit DwarfMessageDispatcher(QObject *parent = nullptr);

public slots:
  void dispatch(std::uint32_t moduleId, std::uint32_t cmd,
                const QByteArray &data);

signals:
  void astroMessage(std::uint32_t cmd, const QByteArray &data);
  void systemMessage(std::uint32_t cmd, const QByteArray &data);
  void rgbPowerMessage(std::uint32_t cmd, const QByteArray &data);
  void motorMessage(std::uint32_t cmd, const QByteArray &data);
  void trackMessage(std::uint32_t cmd, const QByteArray &data);
  void focusMessage(std::uint32_t cmd, const QByteArray &data);
  void notifyMessage(std::uint32_t cmd, const QByteArray &data);
  void panoramaMessage(std::uint32_t cmd, const QByteArray &data);
  void cameraTeleMessage(std::uint32_t cmd, const QByteArray &data);
  void cameraWideMessage(std::uint32_t cmd, const QByteArray &data);
  void unknownMessage(std::uint32_t moduleId, std::uint32_t cmd,
                      const QByteArray &data);

private:
  static constexpr std::uint32_t MODULE_CAMERA_TELE = 1;
  static constexpr std::uint32_t MODULE_CAMERA_WIDE = 2;
  static constexpr std::uint32_t MODULE_ASTRO = 3;
  static constexpr std::uint32_t MODULE_SYSTEM = 4;
  static constexpr std::uint32_t MODULE_RGB_POWER = 5;
  static constexpr std::uint32_t MODULE_MOTOR = 6;
  static constexpr std::uint32_t MODULE_TRACK = 7;
  static constexpr std::uint32_t MODULE_FOCUS = 8;
  static constexpr std::uint32_t MODULE_NOTIFY = 9;
  static constexpr std::uint32_t MODULE_PANORAMA = 10;
};
