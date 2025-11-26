#include "DwarfHttpClient.h"

#include <QNetworkRequest>
#include <QUrl>

DwarfHttpClient::DwarfHttpClient(const QString &ip, QObject *parent)
    : QObject(parent), m_manager(new QNetworkAccessManager(this)), m_ip(ip) {}

void DwarfHttpClient::fetchMediaList() {
  QUrl url(QString("http://%1:%2/api/v1/files").arg(m_ip).arg(HTTP_PORT));
  QNetworkRequest request(url);
  QNetworkReply *reply = m_manager->get(request);

  connect(reply, &QNetworkReply::finished, this, [this, reply]() {
    if (reply->error() == QNetworkReply::NoError) {
      QJsonDocument document = QJsonDocument::fromJson(reply->readAll());
      emit mediaListReceived(document);
    } else {
      emit errorOccurred(reply->errorString());
    }
    reply->deleteLater();
  });
}
