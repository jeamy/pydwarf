#pragma once

#include <QJsonDocument>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QObject>
#include <QString>

class DwarfHttpClient : public QObject {
  Q_OBJECT

public:
  explicit DwarfHttpClient(const QString &ip, QObject *parent = nullptr);
  void fetchMediaList();

signals:
  void mediaListReceived(const QJsonDocument &document);
  void errorOccurred(const QString &error);

private:
  QNetworkAccessManager *m_manager;
  QString m_ip;
  static constexpr int HTTP_PORT = 8082;
};
