# Roadmap: DWARF II Steuerung mit Qt (C++)

Basierend auf der Machbarkeitsstudie (`CPP_WXWIDGETS_FEASIBILITY_STUDY.md`) wurde diese Roadmap für die Umsetzung mit dem **Qt Framework** erstellt. Qt bietet gegenüber der wxWidgets/Boost-Kombination den Vorteil einer integrierten Lösung ("Batteries Included") für Netzwerk, UI und Multimedia.

## 1. Technologie-Stack

| Komponente | Technologie | Beschreibung |
|------------|-------------|--------------|
| **Sprache** | C++17 | Moderner C++ Standard |
| **Framework** | **Qt 6.x** | Umfassendes Framework für UI, Netzwerk, Events |
| **Build System** | **CMake** | Industriestandard, hervorragende Qt-Integration |
| **UI-Technologie** | **Qt Widgets** (oder QML) | Widgets für klassische Desktop-Apps, QML für Touch/Modern UI |
| **Daten** | **Protocol Buffers** | Binäres Format für DWARF-Kommunikation |
| **Video** | **Qt Multimedia** / libvlc | RTSP-Streaming und Wiedergabe |

## 2. Architektur-Mapping

Die Architektur wird analog zur wxWidgets-Studie aufgebaut, jedoch mit Qt-nativen Klassen ersetzt. Dies vereinfacht das Threading und Event-Handling massiv (Signals & Slots).

| Konzept | wxWidgets/Boost | Qt Äquivalent |
|---------|-----------------|---------------|
| **WebSocket** | `boost::beast` / `websocketpp` | **`QWebSocket`** (Qt WebSockets) |
| **HTTP Client** | `libcurl` / `cpp-httplib` | **`QNetworkAccessManager`** (Qt Network) |
| **Event Loop** | `boost::asio::io_context` | **`QEventLoop`** (integriert in `QCoreApplication`) |
| **Threading** | `std::thread` / `wxThread` | **`QThread`** / `QtConcurrent` |
| **JSON** | `nlohmann/json` | **`QJsonDocument`** / `QJsonObject` |
| **Video** | `libvlc` | **`QMediaPlayer`** (`QVideoWidget`) |

## 3. Detaillierter Implementierungsplan

### Phase 1: Projekt-Setup & Infrastruktur (1 Woche)
*Ziel: Eine kompilierbare Qt-Anwendung mit integriertem Protobuf.*

1.  **CMake Setup**:
    *   `CMakeLists.txt` erstellen mit `find_package(Qt6 COMPONENTS Widgets Network Multimedia REQUIRED)`.
    *   Integration von `protobuf` via `find_package(Protobuf)`.
2.  **Protobuf Integration**:
    *   Kompilierung der `.proto` Dateien (camera, astro, motor, etc.) in C++ Klassen.
    *   Erstellung einer Helper-Klasse `ProtobufHelper` zur Serialisierung/Deserialisierung (Qt `QByteArray` <-> `std::string`).
3.  **Basis-GUI**:
    *   Erstellung des `MainWindow` mit Platzhaltern für die verschiedenen Module (Tabs).

### Phase 2: Netzwerk-Layer (Core) (1-2 Wochen)
*Ziel: Kommunikation mit dem Teleskop (Senden/Empfangen).*

1.  **DwarfConnectionManager**:
    *   Singleton-Klasse zur Verwaltung der Verbindung.
    *   Implementierung von `QWebSocket` für Port 9900.
    *   Signal-Slot-Verbindungen für eingehende Nachrichten.
2.  **Nachrichten-Handling**:
    *   Dispatcher, der eingehende Binärdaten (Protobuf) an die entsprechenden UI-Komponenten weiterleitet.
    *   Mapping von `cmd` (Befehls-ID) auf Signale (z.B. `sigMotorStatusReceived`).
3.  **HTTP-Client**:
    *   Klasse `DwarfHttpClient` für REST-Anfragen (Medienlisten, Firmware).
    *   Asynchrone Verarbeitung mit `QNetworkReply`.

### Phase 3: GUI-Module (Funktionalität) (2-3 Wochen)
*Ziel: Steuerung der Teleskop-Funktionen.*

1.  **Camera Panel**:
    *   Controls für Belichtung, Gain, IR-Cut (Slider, Buttons).
    *   Anzeige von Tele- und Weitwinkel-Bildern.
2.  **Motor & Astro Panel**:
    *   Joystick-Steuerung (Senden von `StepMotor`-Befehlen).
    *   Goto-Interface (Eingabe RA/DEC oder Objektsuche).
    *   Kalibrierungs-Workflow.
3.  **Media Panel**:
    *   Anzeige der aufgenommenen Fotos/Videos (Thumbnails via HTTP laden).
    *   Download-Funktion.

### Phase 4: Video-Streaming (1 Woche)
*Ziel: Live-Bild vom Teleskop.*

1.  **RTSP-Stream**:
    *   Implementierung eines Video-Players mit `QMediaPlayer`.
    *   Setzen der Quelle: `rtsp://10.1.1.102:554/live/channel0` (Tele) bzw. `channel1` (Wide).
    *   *Fallback*: Sollte `QMediaPlayer` Probleme mit dem spezifischen RTSP-Format haben, Integration von `libvlc` via Wrapper.

### Phase 5: Testing & Deployment (1 Woche)
*Ziel: Stabiles Release für Endanwender.*

1.  **Cross-Platform Tests**:
    *   Testen auf Linux und Windows (ggf. macOS).
2.  **Packaging**:
    *   **Windows**: `windeployqt` nutzen, um alle DLLs zu bündeln. Erstellung eines Installers (Inno Setup).
    *   **Linux**: Erstellung eines AppImage (läuft auf fast allen Distros).

## 4. Code-Beispiele (Qt)

### WebSocket Verbindung
```cpp
// DwarfClient.h
class DwarfClient : public QObject {
    Q_OBJECT
public:
    void connectToDevice(const QString &ip);
    void sendCommand(int moduleId, int cmd, const QByteArray &data);

signals:
    void connected();
    void messageReceived(int cmd, const QByteArray &data);

private slots:
    void onSocketConnected();
    void onBinaryMessage(const QByteArray &message);

private:
    QWebSocket m_socket;
};
```

### HTTP Request (Medienliste)
```cpp
void DwarfHttpClient::fetchMediaList() {
    QNetworkRequest request(QUrl("http://10.1.1.102:8082/api/v1/files"));
    QNetworkReply *reply = m_manager->get(request);
    
    connect(reply, &QNetworkReply::finished, this, [reply](){
        if (reply->error() == QNetworkReply::NoError) {
            QJsonDocument doc = QJsonDocument::fromJson(reply->readAll());
            // Verarbeite JSON...
        }
        reply->deleteLater();
    });
}
```

## 5. Zeitplan & Aufwandsschätzung

| Phase | Dauer | Fokus |
|-------|-------|-------|
| **1. Setup** | 3 Tage | Build-System, Protobuf |
| **2. Netzwerk** | 7 Tage | WebSocket, HTTP, Protokoll |
| **3. GUI** | 10 Tage | Panels, Interaktion, Logik |
| **4. Video** | 4 Tage | Streaming Integration |
| **5. Polish** | 4 Tage | Tests, Bugfixes, Deployment |
| **Gesamt** | **~4-5 Wochen** | (Vollzeit) |

## 6. Empfehlung: Qt Widgets vs. Qt Quick

*   **Qt Widgets**: Empfohlen, wenn der Fokus auf einem klassischen Desktop-Tool liegt. Einfacher zu debuggen, striktere Trennung, näher an C++.
*   **Qt Quick (QML)**: Empfohlen, wenn eine "moderne", animierte Oberfläche (wie auf Smartphones) gewünscht ist. Erfordert JavaScript-Kenntnisse für die UI-Logik.

**Entscheidung**: Für eine direkte Portierung und maximale Kontrolle über die Hardware-Steuerung ist **Qt Widgets** der sicherere und schnellere Weg.
