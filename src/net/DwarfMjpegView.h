#pragma once

#include <QImage>
#include <QWidget>

class QPaintEvent;
class QMouseEvent;
class QPointF;

class DwarfMjpegView : public QWidget {
  Q_OBJECT

public:
  explicit DwarfMjpegView(QWidget *parent = nullptr);

  void setSourceImage(const QImage *image);

signals:
  void pointClicked(const QPointF &normalizedPos);

protected:
  void paintEvent(QPaintEvent *event) override;
  void mouseDoubleClickEvent(QMouseEvent *event) override;

private:
  const QImage *m_image;
};
