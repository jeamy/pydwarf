#include "DwarfHttpClient.h"

#include <QJsonDocument>
#include <QJsonObject>
#include <QNetworkRequest>
#include <QUrl>

DwarfHttpClient::DwarfHttpClient(const QString &ip, QObject *parent)
    : QObject(parent), m_manager(new QNetworkAccessManager(this)), m_ip(ip) {}

void DwarfHttpClient::fetchMediaList() {
  QUrl url(
      QString("http://%1:%2/album/list/mediaInfos").arg(m_ip).arg(HTTP_PORT));
  QNetworkRequest request(url);
  request.setHeader(QNetworkRequest::ContentTypeHeader,
                    QStringLiteral("application/json"));

  QJsonObject payload;
  payload.insert(QStringLiteral("mediaType"), 0);
  payload.insert(QStringLiteral("pageIndex"), 0);
  payload.insert(QStringLiteral("pageSize"), 0);
  QJsonDocument doc(payload);

  QNetworkReply *reply = m_manager->post(request, doc.toJson());

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
