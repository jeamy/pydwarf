#pragma once

#include "DwarfWebSocketClient.h"
#include "camera.pb.h"
#include <QObject>

class DwarfCameraController : public QObject {
  Q_OBJECT

public:
  enum class CameraKind { Tele, Wide };

  explicit DwarfCameraController(QObject *parent = nullptr);

  void setClient(DwarfWebSocketClient *client);

  // High level camera actions
  void openCamera(CameraKind kind, bool binning, int rtspEncodeType);
  void closeCamera(CameraKind kind);
  void takePhoto(CameraKind kind);
  void startRecord(CameraKind kind);
  void stopRecord(CameraKind kind);

  // Parameter setters (will internally send ReqSetAllParams)
  void setExposureMode(CameraKind kind, int mode);
  void setExposureIndex(CameraKind kind, int index);
  void setGainMode(CameraKind kind, int mode);
  void setGainIndex(CameraKind kind, int index);
  void setIrCut(CameraKind kind, int value);
  void setWhiteBalanceMode(CameraKind kind, int mode);
  void setWhiteBalanceByTemperature(CameraKind kind, int ctIndex);
  void setBrightness(CameraKind kind, int value);
  void setContrast(CameraKind kind, int value);
  void setHue(CameraKind kind, int value);
  void setSaturation(CameraKind kind, int value);
  void setSharpness(CameraKind kind, int value);

signals:
  void errorOccurred(const QString &message);

private:
  DwarfWebSocketClient *m_client;

  dwarf::ReqSetAllParams m_teleParams;
  dwarf::ReqSetAllParams m_wideParams;

  void sendSetAllParams(CameraKind kind);
  quint32 moduleIdFor(CameraKind kind) const;
  quint32 cmdSetAllParamsFor(CameraKind kind) const;
  quint32 cmdOpenCameraFor(CameraKind kind) const;
  quint32 cmdCloseCameraFor(CameraKind kind) const;
  quint32 cmdPhotoFor(CameraKind kind) const;
  quint32 cmdStartRecordFor(CameraKind kind) const;
  quint32 cmdStopRecordFor(CameraKind kind) const;
};
