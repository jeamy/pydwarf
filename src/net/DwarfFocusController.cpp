#include "DwarfFocusController.h"
#include "ProtobufHelper.h"

#include <QDebug>

using dwarf::ReqNormalAutoFocus;
using dwarf::ReqManualSingleStepFocus;

DwarfFocusController::DwarfFocusController(QObject *parent)
    : QObject(parent), m_client(nullptr) {}

void DwarfFocusController::setClient(DwarfWebSocketClient *client) {
  m_client = client;
  qWarning() << "[DwarfFocusController] setClient called with"
             << (client ? "valid" : "null") << "client";
}

void DwarfFocusController::autoFocusNormal() {
  if (!m_client || !m_client->isConnected()) {
    qWarning() << "[DwarfFocusController] Cannot start auto focus, client not connected";
    emit errorOccurred("Focus client not connected");
    return;
  }

  ReqNormalAutoFocus req;
  req.set_mode(0);
  req.set_center_x(0);
  req.set_center_y(0);

  const QByteArray data = ProtobufHelper::serialize(req);
  m_client->sendCommand(moduleId(), cmdAutoFocus(), data);
}

void DwarfFocusController::manualStepNear() {
  if (!m_client || !m_client->isConnected()) {
    qWarning() << "[DwarfFocusController] Cannot do manual focus near, client not connected";
    emit errorOccurred("Focus client not connected");
    return;
  }

  ReqManualSingleStepFocus req;
  req.set_direction(1);

  const QByteArray data = ProtobufHelper::serialize(req);
  m_client->sendCommand(moduleId(), cmdManualSingleStep(), data);
}

void DwarfFocusController::manualStepFar() {
  if (!m_client || !m_client->isConnected()) {
    qWarning() << "[DwarfFocusController] Cannot do manual focus far, client not connected";
    emit errorOccurred("Focus client not connected");
    return;
  }

  ReqManualSingleStepFocus req;
  req.set_direction(0);

  const QByteArray data = ProtobufHelper::serialize(req);
  m_client->sendCommand(moduleId(), cmdManualSingleStep(), data);
}

quint32 DwarfFocusController::moduleId() const { return 8u; }

quint32 DwarfFocusController::cmdAutoFocus() const { return 15000u; }

quint32 DwarfFocusController::cmdManualSingleStep() const { return 15001u; }
