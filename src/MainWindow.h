#pragma once

#include "net/DwarfFinder.h"
#include "net/DwarfWebSocketClient.h"
#include "net/DwarfMessageDispatcher.h"
#include <QComboBox>
#include <QCheckBox>
#include <QGroupBox>
#include <QLabel>
#include <QLineEdit>
#include <QListWidget>
#include <QMainWindow>
#include <QPushButton>
#include <QSlider>
#include <QTabWidget>

class MainWindow : public QMainWindow {
  Q_OBJECT

public:
  MainWindow(QWidget *parent = nullptr);
  ~MainWindow();

private slots:
  void onConnectClicked();
  void onCancelConnectClicked();
  void onScanClicked();
  void onCancelScanClicked();
  void onSubnetTextChanged(const QString &text);
  void onWebSocketConnected();
  void onWebSocketDisconnected();
  void onWebSocketError(const QString &error);
  void onDeviceFound(const DwarfDeviceInfo &info);
  void onScanFinished();
  void onScanProgress(int percent);
  void onDeviceSelected(QListWidgetItem *item);
  void onCameraSourceTele();
  void onCameraSourceWide();
  void onCameraPhotoClicked();
  void onCameraRecClicked();
  void onExposureModeChanged(int index);
  void onShutterSliderChanged(int value);
  void onGainSliderChanged(int value);
  void onIrCutToggled(bool checked);
  void onBinningChanged(int index);
  void onContrastSliderChanged(int value);
  void onSaturationSliderChanged(int value);
  void onSharpnessSliderChanged(int value);
  void onHueSliderChanged(int value);

private:
  void setupUi();

  QLineEdit *m_ipInput;
  QLineEdit *m_subnetInput;
  QPushButton *m_connectButton;
  QPushButton *m_cancelConnectButton;
  QPushButton *m_scanButton;
  QPushButton *m_cancelScanButton;
  QListWidget *m_deviceList;
  QLabel *m_statusLabel;
  QTabWidget *m_tabWidget;
  DwarfWebSocketClient *m_wsClient;
  DwarfMessageDispatcher *m_dispatcher;
  DwarfFinder *m_finder;
  bool m_scanCancelled;
  void updateStatusStyle(const char *statusKey);

  QPushButton *m_teleButton;
  QPushButton *m_wideButton;
  QPushButton *m_photoButton;
  QPushButton *m_recButton;
  QComboBox *m_exposureModeCombo;
  QSlider *m_shutterSlider;
  QSlider *m_gainSlider;
  QCheckBox *m_irCutCheckBox;
  QComboBox *m_binningCombo;
  QSlider *m_contrastSlider;
  QSlider *m_saturationSlider;
  QSlider *m_sharpnessSlider;
  QSlider *m_hueSlider;
};
