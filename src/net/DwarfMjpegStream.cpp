#include "net/DwarfMjpegStream.h"

#include <QDebug>
#include <QNetworkRequest>

DwarfMjpegStream::DwarfMjpegStream(QObject *parent)
    : QObject(parent), m_reply(nullptr) {}

DwarfMjpegStream::~DwarfMjpegStream() { stop(); }

void DwarfMjpegStream::start(const QUrl &url) {
  stop();

  QNetworkRequest req(url);
  req.setHeader(QNetworkRequest::UserAgentHeader,
                QStringLiteral("DwarfController/0.1"));

  m_buffer.clear();

  qWarning() << "[DwarfMjpegStream] Starting stream from" << url;
  m_reply = m_manager.get(req);
  connect(m_reply, &QNetworkReply::readyRead, this,
          &DwarfMjpegStream::onReadyRead);
  connect(m_reply, &QNetworkReply::finished, this,
          &DwarfMjpegStream::onFinished);
  connect(m_reply,
          qOverload<QNetworkReply::NetworkError>(&QNetworkReply::errorOccurred),
          this, &DwarfMjpegStream::onError);
}

void DwarfMjpegStream::stop() {
  if (m_reply) {
    disconnect(m_reply, nullptr, this, nullptr);
    m_reply->abort();
    m_reply->deleteLater();
    m_reply = nullptr;
  }
  m_buffer.clear();
  m_currentFrame = QImage();
}

void DwarfMjpegStream::onReadyRead() {
  if (!m_reply)
    return;

  m_buffer.append(m_reply->readAll());

  // Extract JPEG frames by SOI/EOI markers
  while (true) {
    int start = m_buffer.indexOf("\xFF\xD8"); // JPEG SOI
    if (start < 0) {
      // Prevent unbounded growth if stream is malformed
      if (m_buffer.size() > 1024 * 1024)
        m_buffer.remove(0, m_buffer.size() - 1024 * 1024);
      break;
    }
    int end = m_buffer.indexOf("\xFF\xD9", start + 2); // JPEG EOI
    if (end < 0)
      break; // Wait for complete frame

    int len = end - start + 2;
    QByteArray frameData = m_buffer.mid(start, len);
    m_buffer.remove(0, end + 2);

    QImage img;
    if (img.loadFromData(frameData, "JPG")) {
      m_currentFrame = img;
      emit frameUpdated();
    }
  }
}

void DwarfMjpegStream::onFinished() {
  if (!m_reply)
    return;

  if (m_reply->error() != QNetworkReply::OperationCanceledError) {
    emit errorOccurred(
        QObject::tr("MJPEG stream finished: %1").arg(m_reply->errorString()));
  }

  m_reply->deleteLater();
  m_reply = nullptr;
}

void DwarfMjpegStream::onError(QNetworkReply::NetworkError code) {
  Q_UNUSED(code);
  if (!m_reply)
    return;

  qWarning() << "[DwarfMjpegStream] Network error:" << m_reply->errorString();
  emit errorOccurred(
      QObject::tr("MJPEG stream error: %1").arg(m_reply->errorString()));
}
