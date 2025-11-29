#pragma once

#include <QObject>
#include <QImage>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QUrl>

class DwarfMjpegStream : public QObject {
  Q_OBJECT

public:
  explicit DwarfMjpegStream(QObject *parent = nullptr);
  ~DwarfMjpegStream();

  void start(const QUrl &url);
  void stop();

  const QImage &currentFrame() const { return m_currentFrame; }

signals:
  void frameUpdated();
  void errorOccurred(const QString &message);

private slots:
  void onReadyRead();
  void onFinished();
  void onError(QNetworkReply::NetworkError code);

private:
  QNetworkAccessManager m_manager;
  QNetworkReply *m_reply;
  QByteArray m_buffer;
  QImage m_currentFrame;
};
