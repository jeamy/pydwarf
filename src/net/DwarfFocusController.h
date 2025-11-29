#pragma once

#include "DwarfWebSocketClient.h"
#include "focus.pb.h"

#include <QObject>

class DwarfFocusController : public QObject {
  Q_OBJECT

public:
  explicit DwarfFocusController(QObject *parent = nullptr);

  void setClient(DwarfWebSocketClient *client);

  void autoFocusNormal();
  void manualStepNear();
  void manualStepFar();

signals:
  void errorOccurred(const QString &message);

private:
  DwarfWebSocketClient *m_client;

  quint32 moduleId() const;
  quint32 cmdAutoFocus() const;
  quint32 cmdManualSingleStep() const;
};
