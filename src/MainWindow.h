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
#include <QMediaPlayer>
#include <QMouseEvent>
#include <QPushButton>
#include <QSlider>
#include <QTabWidget>
#include <QVideoWidget>
#include <QWidget>

class DwarfCameraController;

class ClickableLabel : public QLabel {
  Q_OBJECT

public:
  explicit ClickableLabel(QWidget *parent = nullptr)
      : QLabel(parent) {}
  explicit ClickableLabel(const QString &text, QWidget *parent = nullptr)
      : QLabel(text, parent) {}

signals:
  void clicked();

protected:
  void mousePressEvent(QMouseEvent *event) override {
    QLabel::mousePressEvent(event);
    emit clicked();
  }
};

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
  void onPipStreamClicked();
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
  void onBrightnessSliderChanged(int value);
  void onWbModeChanged(int index);
  void onWbTemperatureChanged(int value);

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
  DwarfCameraController *m_cameraController;

  enum class CameraStream { Tele, Wide };

  QLabel *m_mainStreamView;
  ClickableLabel *m_pipStreamView;
  QVideoWidget *m_mainVideoWidget;
  QVideoWidget *m_pipVideoWidget;
  CameraStream m_mainStream;
  CameraStream m_pipStream;
  void updateCameraStreamViews();
  void updateStreamRouting();
  void startStreaming(const QString &ip);
  void stopStreaming();

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
  QSlider *m_brightnessSlider;
  QComboBox *m_wbModeCombo;
  QSlider *m_wbTemperatureSlider;
  bool m_isRecording;

  QMediaPlayer *m_telePlayer;
  QMediaPlayer *m_widePlayer;
};
