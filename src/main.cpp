#include "MainWindow.h"
#include <QApplication>
#include <QLoggingCategory>
#include <iostream>

int main(int argc, char *argv[]) {
  // Disable Qt's verbose debug output, only show warnings and critical
  QLoggingCategory::setFilterRules("qt.*=false\n*.debug=false");
  qSetMessagePattern("[%{if-category}%{category}: %{endif}%{message}]");

  fprintf(stderr, "=== DWARF II Controller starting ===\n");
  fflush(stderr);

  QApplication app(argc, argv);

  // Apply Dark Theme
  QPalette darkPalette;
  darkPalette.setColor(QPalette::Window, QColor(53, 53, 53));
  darkPalette.setColor(QPalette::WindowText, Qt::white);
  darkPalette.setColor(QPalette::Base, QColor(25, 25, 25));
  darkPalette.setColor(QPalette::AlternateBase, QColor(53, 53, 53));
  darkPalette.setColor(QPalette::ToolTipBase, Qt::white);
  darkPalette.setColor(QPalette::ToolTipText, Qt::white);
  darkPalette.setColor(QPalette::Text, Qt::white);
  darkPalette.setColor(QPalette::Button, QColor(53, 53, 53));
  darkPalette.setColor(QPalette::ButtonText, Qt::white);
  darkPalette.setColor(QPalette::BrightText, Qt::red);
  darkPalette.setColor(QPalette::Link, QColor(42, 130, 218));
  darkPalette.setColor(QPalette::Highlight, QColor(42, 130, 218));
  darkPalette.setColor(QPalette::HighlightedText, Qt::black);

  app.setPalette(darkPalette);
  app.setStyle("Fusion");

  MainWindow w;
  w.show();

  return app.exec();
}
