# Machbarkeitsstudie: C++/wxWidgets Portierung der DWARF II Teleskop-Steuerung

## Executive Summary

Die Portierung der Python-Backend-API auf C++/wxWidgets ist **technisch machbar** und ermöglicht eine leistungsfähige Native Cross-Platform-Anwendung.

**Optimierte Empfehlung**:
Durch den Einsatz von High-Level-Bibliotheken (**libvlc** statt FFmpeg) und modernem Dependency-Management (**vcpkg**) kann die Komplexität deutlich reduziert werden.
Besonders effizient wäre ein **Hybrid-Ansatz**: Das existierende Python-Backend wird als lokaler Server genutzt, während die C++/wxWidgets-App als GUI-Client fungiert. Dies reduziert die Entwicklungszeit drastisch auf **2-3 Wochen**.

---

## 1. Analyse der Python-Backend-Architektur

### 1.1 Kernkomponenten

Die Python-Implementierung basiert auf folgenden Hauptkomponenten:

| Komponente | Python-Technologie | Funktion |
|------------|-------------------|----------|
| **WebSocket-Client** | `websockets` | Bidirektionale Kommunikation mit DWARF II |
| **HTTP-Client** | `httpx` | REST-API für Medien, Firmware, Logs |
| **Protocol Buffers** | `protobuf` | Binäre Serialisierung der Nachrichten |
| **Async I/O** | `asyncio` | Asynchrone Event-Loop |
| **Connection Manager** | Singleton Pattern | Persistente WebSocket-Verbindungen |

### 1.2 Kommunikationsprotokolle

#### WebSocket-Protokoll (Port 9900)
```
WsPacket {
  major_version: 2
  minor_version: 0
  device_id: 1 (DWARF II) / 2 (DWARF3)
  module_id: 1-13 (Camera, Astro, Motor, etc.)
  cmd: 10000-15599 (Befehlscodes)
  type: 0 (Request) / 1 (Response)
  data: bytes (Protobuf-serialisiert)
  client_id: string
}
```

#### HTTP-Protokoll (Port 8082, 8092)
- REST-API für Medien-Verwaltung
- Firmware-Updates
- Log-Downloads
- JPG-Streams (Port 8092)

---

## 2. C++/wxWidgets Äquivalente

### 2.1 Bibliotheken-Mapping

| Python | C++ Äquivalent | Verfügbarkeit | Lizenz |
|--------|---------------|---------------|--------|
| `websockets` | **libwebsockets** oder **Boost.Beast** | ✅ Stabil | MIT / Boost |
| `httpx` | **libcurl** oder **cpp-httplib** | ✅ Stabil | MIT |
| `protobuf` | **protobuf-cpp** | ✅ Stabil | BSD |
| `asyncio` | **Boost.Asio** oder **wxWidgets Events** | ✅ Stabil | Boost / wxWindows |
| `FastAPI` | Nicht benötigt (Desktop-App) | - | - |

### 2.2 Empfohlene Bibliotheken

#### Option A: Boost-basiert (Empfohlen für Profis)
```cpp
// WebSocket
#include <boost/beast/websocket.hpp>
#include <boost/asio.hpp>

// HTTP
#include <boost/beast/http.hpp>

// Protocol Buffers
#include <google/protobuf/message.h>

// Threading
#include <boost/thread.hpp>
```

**Vorteile:**
- Industriestandard
- Hervorragende Performance
- Umfangreiche Dokumentation
- Aktive Community

**Nachteile:**
- Große Abhängigkeit (~100 MB)
- Steile Lernkurve
- Längere Kompilierzeiten

#### Option B: Leichtgewichtig (Empfohlen für schnelle Entwicklung)
```cpp
// WebSocket
#include <websocketpp/websocketpp.hpp>

// HTTP
#include <httplib.h>  // cpp-httplib (Header-only)

// Protocol Buffers
#include <google/protobuf/message.h>

// Threading
#include <thread>
#include <mutex>
#include <condition_variable>
```

**Vorteile:**
- Einfachere Integration
- Header-only Bibliotheken (cpp-httplib)
- Schnellere Kompilierung
- Geringere Komplexität

**Nachteile:**
- Weniger Features
- Teilweise geringere Performance

---

## 3. Architektur-Entwurf

### 3.1 Klassenstruktur

```cpp
// Connection Management
class DwarfConnectionManager {
private:
    static DwarfConnectionManager* instance;
    std::map<std::string, WebSocketHandler*> connections;
    std::mutex connectionMutex;
    
public:
    static DwarfConnectionManager* getInstance();
    WebSocketHandler* getConnection(const std::string& ip);
    void closeConnection(const std::string& ip);
    void closeAll();
};

// WebSocket Handler
class WebSocketHandler {
private:
    websocket::stream<tcp::socket> ws;
    boost::asio::io_context& ioc;
    std::string ipDwarf;
    std::queue<std::vector<uint8_t>> sendingQueue;
    std::mutex queueMutex;
    bool isOpened;
    bool isRunning;
    
    // Callbacks
    std::map<std::string, std::function<void(const MessageData&)>> messageCallbacks;
    std::map<std::string, std::function<void(const std::string&)>> errorCallbacks;
    
public:
    WebSocketHandler(const std::string& ip, boost::asio::io_context& ioc);
    ~WebSocketHandler();
    
    void open();
    void close();
    bool isConnected() const;
    
    void sendPacket(const std::vector<uint8_t>& packet);
    std::vector<uint8_t> createPacket(int moduleId, int cmd, const std::string& data);
    
    void registerMessageCallback(const std::string& name, 
                                 std::function<void(const MessageData&)> callback);
    void registerErrorCallback(const std::string& name,
                              std::function<void(const std::string&)> callback);
    
private:
    void receiveLoop();
    void sendLoop();
    void handleMessage(const std::vector<uint8_t>& data);
};

// HTTP Client
class DwarfHTTPClient {
private:
    std::string ip;
    int port;
    int jpgPort;
    httplib::Client* client;
    
public:
    DwarfHTTPClient(const std::string& ip, int port = 8082, int jpgPort = 8092);
    ~DwarfHTTPClient();
    
    nlohmann::json getDeviceInfo();
    nlohmann::json getMediaCounts();
    nlohmann::json getMediaList(int mediaType, int pageIndex, int pageSize);
    bool deleteMedia(const std::vector<MediaItem>& items);
    
    std::string getRTSPUrl(const std::string& camera = "tele");
};

// Protocol Buffers Wrapper
class ProtobufHelper {
public:
    static std::string serializeMessage(const google::protobuf::Message& msg);
    static bool parseMessage(const std::string& data, google::protobuf::Message& msg);
    
    // Spezifische Nachrichten
    static WsPacket createWsPacket(int moduleId, int cmd, const std::string& data);
    static ComResponse parseComResponse(const std::string& data);
};
```

### 3.2 wxWidgets GUI-Struktur

```cpp
// Main Frame
class DwarfMainFrame : public wxFrame {
private:
    // Connection
    wxTextCtrl* ipInput;
    wxButton* connectButton;
    wxStaticText* statusLabel;
    
    // Tabs
    wxNotebook* notebook;
    CameraPanel* cameraPanel;
    AstroPanel* astroPanel;
    FocusPanel* focusPanel;
    MotorPanel* motorPanel;
    AlbumPanel* albumPanel;
    
    // Backend
    DwarfConnectionManager* connectionManager;
    std::string currentIP;
    
    // Threading
    boost::asio::io_context ioc;
    std::thread ioThread;
    
public:
    DwarfMainFrame();
    ~DwarfMainFrame();
    
private:
    void OnConnect(wxCommandEvent& event);
    void OnDisconnect(wxCommandEvent& event);
    void OnClose(wxCloseEvent& event);
    
    void InitializeBackend();
    void ShutdownBackend();
    
    wxDECLARE_EVENT_TABLE();
};

// Camera Panel
class CameraPanel : public wxPanel {
private:
    wxButton* openCameraBtn;
    wxButton* closeCameraBtn;
    wxButton* takePhotoBtn;
    wxButton* startVideoBtn;
    wxButton* stopVideoBtn;
    
    // Stream Display
    wxPanel* streamPanel;
    wxImage currentFrame;
    
    // Parameters
    wxSlider* exposureSlider;
    wxSlider* gainSlider;
    wxChoice* binningChoice;
    
public:
    CameraPanel(wxWindow* parent, DwarfConnectionManager* connMgr);
    
private:
    void OnOpenCamera(wxCommandEvent& event);
    void OnTakePhoto(wxCommandEvent& event);
    void OnStartVideo(wxCommandEvent& event);
    
    void UpdateStream(const wxImage& frame);
};

// Astro Panel
class AstroPanel : public wxPanel {
private:
    // Calibration
    wxButton* startCalibrationBtn;
    wxButton* stopCalibrationBtn;
    
    // GOTO
    wxTextCtrl* raInput;
    wxTextCtrl* decInput;
    wxTextCtrl* targetNameInput;
    wxButton* gotoBtn;
    wxButton* stopGotoBtn;
    
    // Stacking
    wxButton* startStackingBtn;
    wxButton* stopStackingBtn;
    wxStaticText* stackCountLabel;
    
public:
    AstroPanel(wxWindow* parent, DwarfConnectionManager* connMgr);
    
private:
    void OnStartCalibration(wxCommandEvent& event);
    void OnGotoDSO(wxCommandEvent& event);
    void OnStartStacking(wxCommandEvent& event);
};
```

---

## 4. Implementierungsplan

### Phase 1: Grundgerüst (1 Woche)
- [ ] CMake-Build-System einrichten
- [ ] wxWidgets-Projekt aufsetzen
- [ ] Abhängigkeiten integrieren (Boost/WebSocketPP, Protobuf)
- [ ] Protobuf-Dateien kompilieren
- [ ] Basis-GUI mit Tabs erstellen

### Phase 2: WebSocket-Kommunikation (1-2 Wochen)
- [ ] WebSocketHandler implementieren
- [ ] Connection Manager implementieren
- [ ] Packet-Serialisierung/Deserialisierung
- [ ] Callback-System
- [ ] Ping/Pong-Mechanismus
- [ ] Reconnect-Logik

### Phase 3: HTTP-Client (3-5 Tage)
- [ ] DwarfHTTPClient implementieren
- [ ] Medien-Verwaltung
- [ ] Firmware-Updates
- [ ] Log-Downloads
- [ ] Stream-Handling

### Phase 4: GUI-Panels (1-2 Wochen)
- [ ] Camera Panel
- [ ] Astro Panel
- [ ] Focus Panel
- [ ] Motor Panel
- [ ] Album Panel
- [ ] Settings Panel

### Phase 5: Integration & Testing (1 Woche)
- [ ] End-to-End-Tests
- [ ] Error-Handling
- [ ] UI-Polishing
- [ ] Performance-Optimierung

### Phase 6: Packaging (3-5 Tage)
- [ ] Linux: AppImage/DEB/RPM
- [ ] macOS: DMG
- [ ] Windows: Installer (NSIS/WiX)

---

## 5. Technische Herausforderungen

### 5.1 Asynchrone Programmierung

**Problem**: Python's `asyncio` ist sehr komfortabel, C++ erfordert mehr Boilerplate.

**Lösung**:
```cpp
// Boost.Asio Event-Loop
boost::asio::io_context ioc;

// Worker-Thread
std::thread ioThread([&ioc]() {
    ioc.run();
});

// Async WebSocket Read
ws.async_read(buffer, [this](boost::system::error_code ec, std::size_t bytes) {
    if (!ec) {
        handleMessage(buffer);
        // Continue reading
        ws.async_read(buffer, ...);
    }
});

// Thread-safe GUI-Updates
wxQueueEvent(mainFrame, new wxThreadEvent(wxEVT_THREAD, UPDATE_STREAM));
```

### 5.2 Protocol Buffers

**Problem**: Protobuf-Dateien müssen für C++ kompiliert werden.

**Lösung**:
```bash
# CMakeLists.txt
find_package(Protobuf REQUIRED)
protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS
    proto/base.proto
    proto/astro.proto
    proto/camera.proto
    proto/focus.proto
    proto/motor.proto
    proto/system.proto
)
```

```cpp
// Usage
astro::ReqGotoDSO req;
req.set_ra(10.684);
req.set_dec(41.269);
req.set_target_name("M31");

std::string serialized;
req.SerializeToString(&serialized);
```

### 5.3 Thread-Safety

**Problem**: GUI-Thread vs. I/O-Thread.

**Lösung**:
```cpp
// Thread-safe Queue
template<typename T>
class ThreadSafeQueue {
private:
    std::queue<T> queue;
    mutable std::mutex mutex;
    std::condition_variable cv;
    
public:
    void push(T item) {
        std::lock_guard<std::mutex> lock(mutex);
        queue.push(std::move(item));
        cv.notify_one();
    }
    
    bool pop(T& item) {
        std::unique_lock<std::mutex> lock(mutex);
        cv.wait(lock, [this]{ return !queue.empty(); });
        item = std::move(queue.front());
        queue.pop();
        return true;
    }
};

// wxWidgets Event-System
wxDEFINE_EVENT(EVT_DWARF_MESSAGE, wxThreadEvent);

Bind(EVT_DWARF_MESSAGE, &DwarfMainFrame::OnDwarfMessage, this);

// Von Worker-Thread
    wxQueueEvent(mainFrame, event);
```

### 5.4 Video-Streaming (Optimiert)
 
 **Problem**: RTSP-Stream in wxWidgets anzeigen.
 
 **Lösung**: Anstatt FFmpeg manuell zu implementieren (komplex, fehleranfällig), sollte **libvlc** verwendet werden.
 
 ```cpp
 // libvlc Integration (Viel einfacher & stabiler)
 #include <vlc/vlc.h>
 
 class VLCPanel : public wxPanel {
 private:
     libvlc_instance_t* vlcInstance;
     libvlc_media_player_t* mediaPlayer;
     
 public:
     VLCPanel(wxWindow* parent) : wxPanel(parent) {
         vlcInstance = libvlc_new(0, nullptr);
         mediaPlayer = libvlc_media_player_new(vlcInstance);
     }
 
     void playRTSP(const std::string& url) {
         libvlc_media_t* media = libvlc_media_new_location(vlcInstance, url.c_str());
         libvlc_media_player_set_media(mediaPlayer, media);
         
         // Window Handle binden (OS-spezifisch)
         #ifdef _WIN32
             libvlc_media_player_set_hwnd(mediaPlayer, this->GetHandle());
         #elif __linux__
             libvlc_media_player_set_xwindow(mediaPlayer, this->GetHandle()->GetXWindow());
         #elif __APPLE__
             libvlc_media_player_set_nsobject(mediaPlayer, this->GetHandle());
         #endif
         
         libvlc_media_player_play(mediaPlayer);
         libvlc_media_release(media);
     }
 };
 ```

---

## 6. Abhängigkeiten & Build-System

### 6.1 CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.15)
project(DwarfController VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# wxWidgets
find_package(wxWidgets REQUIRED COMPONENTS core base net)
include(${wxWidgets_USE_FILE})

# Boost (optional, wenn Boost.Beast verwendet wird)
find_package(Boost 1.75 REQUIRED COMPONENTS system thread)

# Protobuf
find_package(Protobuf REQUIRED)

# WebSocket (Option A: WebSocketPP)
find_package(websocketpp REQUIRED)

# HTTP (Option B: cpp-httplib - Header-only)
include_directories(${CMAKE_SOURCE_DIR}/third_party/cpp-httplib)

# Protobuf Generation
protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS
    proto/base.proto
    proto/astro.proto
    proto/camera.proto
    proto/focus.proto
    proto/motor.proto
    proto/system.proto
)

# Sources
set(SOURCES
    src/main.cpp
    src/DwarfMainFrame.cpp
    src/DwarfConnectionManager.cpp
    src/WebSocketHandler.cpp
    src/DwarfHTTPClient.cpp
    src/panels/CameraPanel.cpp
    src/panels/AstroPanel.cpp
    src/panels/FocusPanel.cpp
    src/panels/MotorPanel.cpp
    src/panels/AlbumPanel.cpp
    ${PROTO_SRCS}
)

# Executable
add_executable(DwarfController ${SOURCES})

target_link_libraries(DwarfController
    ${wxWidgets_LIBRARIES}
    ${Boost_LIBRARIES}
    ${Protobuf_LIBRARIES}
    pthread
)

# Platform-specific
if(WIN32)
    target_link_libraries(DwarfController ws2_32)
endif()

# Install
install(TARGETS DwarfController DESTINATION bin)
```

### 6.2 Abhängigkeiten-Installation (Optimiert: vcpkg)
 
 Anstatt Abhängigkeiten manuell zu installieren, wird **vcpkg im Manifest-Modus** empfohlen. Dies garantiert identische Versionen auf allen Plattformen.
 
 #### `vcpkg.json` (im Projekt-Root)
 ```json
 {
   "name": "dwarf-controller",
   "version": "1.0.0",
   "dependencies": [
     "wxwidgets",
     "boost-asio",
     "boost-beast",
     "protobuf",
     "nlohmann-json",
     "libvlc"
   ]
 }
 ```
 
 #### Build
 ```bash
 cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE=[path/to/vcpkg]/scripts/buildsystems/vcpkg.cmake
 cmake --build build
 ```

---

## 7. Vor- und Nachteile

### 7.1 Vorteile der C++/wxWidgets-Lösung

✅ **Native Performance**
- Schnellere Startup-Zeit
- Geringerer RAM-Verbrauch (~50 MB vs. ~200 MB Python)
- Bessere Responsiveness

✅ **Echte Cross-Platform**
- Ein Codebase für Linux/macOS/Windows
- Native Look & Feel auf jedem OS
- Keine Python-Installation erforderlich

✅ **Deployment**
- Einzelne Executable (statisch gelinkt)
- Keine Abhängigkeiten für Endnutzer
- Kleinere Installer (~20-30 MB)

✅ **Professionelles Erscheinungsbild**
- Native Menüs, Dialoge, Widgets
- Bessere Desktop-Integration
- System-Tray-Support

### 7.2 Nachteile

❌ **Entwicklungsaufwand**
- Höhere Komplexität als Python
- Mehr Boilerplate-Code
- Längere Entwicklungszeit

❌ **Build-System**
- Komplexere Abhängigkeiten
- Plattform-spezifische Builds
- Längere Kompilierzeiten

❌ **Debugging**
- Schwieriger als Python
- Memory-Management (Smart Pointers erforderlich)
- Potenzielle Segfaults

---

## 8. Alternative: Qt statt wxWidgets

### 8.1 Qt-Vorteile

✅ **Modernere API**
- Qt 6 mit C++17/20-Features
- Bessere Dokumentation
- Größere Community

✅ **Integrierte Features**
- Qt Network (HTTP, WebSocket)
- Qt Multimedia (Video-Streaming)
- Qt Charts (für Astro-Daten)

✅ **Qt Designer**
- Visueller GUI-Editor
- Schnellere UI-Entwicklung

### 8.2 Qt-Nachteile
 
 ❌ **Lizenz (Missverständnis)**
 - Oft wird angenommen, Qt sei nur kommerziell nutzbar.
 - **Fakt**: Qt ist **LGPL**. Dynamisches Linken erlaubt auch proprietäre/kommerzielle Nutzung ohne Quellcode-Offenlegung.
 
 ❌ **Größe**
 - Größere Runtime (~100 MB)
 - Mehr Abhängigkeiten

### 8.3 Qt-Beispiel

```cpp
// WebSocket mit Qt
#include <QWebSocket>
#include <QCoreApplication>

class DwarfWebSocket : public QObject {
    Q_OBJECT
    
private:
    QWebSocket webSocket;
    
public:
    DwarfWebSocket(const QString& url) {
        connect(&webSocket, &QWebSocket::connected, this, &DwarfWebSocket::onConnected);
        connect(&webSocket, &QWebSocket::binaryMessageReceived, 
                this, &DwarfWebSocket::onMessageReceived);
        
        webSocket.open(QUrl(url));
    }
    
private slots:
    void onConnected() {
        qDebug() << "WebSocket connected";
    }
    
    void onMessageReceived(const QByteArray& message) {
        // Parse Protobuf
        WsPacket packet;
        packet.ParseFromArray(message.data(), message.size());
        
        emit messageReceived(packet);
    }
    
signals:
    void messageReceived(const WsPacket& packet);
};
```

---

## 9. Empfehlung

### 9.1 Technologie-Stack (Empfohlen)

| Komponente | Technologie | Begründung |
|------------|-------------|------------|
| **GUI** | **wxWidgets 3.2** | Native Widgets, keine Lizenz-Sorgen |
| **Video** | **libvlc** | Stabil, einfach, robust |
| **Build** | **CMake + vcpkg** | Standardisiertes Build-System |

### 9.2 Entwicklungs-Optionen

#### Option A: Pure C++ (Native Portierung)
- **Dauer**: 4-6 Wochen
- **Vorteil**: Single Binary, maximale Performance.
- **Nachteil**: Hoher Aufwand für Backend-Logik.

#### Option B: Hybrid-Ansatz (Empfohlen!)
- **Konzept**: Nutze das fertige Python-Backend (als EXE/Binary gepackt) als lokalen Server. Die C++ App ist nur ein GUI-Client, der via WebSocket/HTTP mit `localhost` spricht.
- **Dauer**: 2-3 Wochen
- **Vorteil**: Backend-Logik muss nicht neu geschrieben werden.
- **Nachteil**: Zwei Prozesse (GUI + Backend).

### 9.3 Entwicklungsreihenfolge

1. **Proof of Concept** (1 Woche)
   - Minimale GUI
   - WebSocket-Verbindung
   - Ein Befehl (z.B. Kalibrierung starten)

2. **Core Features** (2 Wochen)
   - Alle WebSocket-Befehle
   - HTTP-Client
   - Connection Manager

3. **GUI Completion** (1-2 Wochen)
   - Alle Panels
   - Video-Streaming
   - Settings

4. **Polish & Package** (1 Woche)
   - Testing
   - Bug-Fixes
   - Installer

**Gesamt: 5-6 Wochen**

---

## 10. Risiken & Mitigation

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| **WebSocket-Kompatibilität** | Mittel | Hoch | Frühzeitig mit echtem DWARF II testen |
| **Protobuf-Versionen** | Niedrig | Mittel | Exakte Version wie Python verwenden |
| **Video-Streaming** | Hoch | Mittel | FFmpeg-Fallback, VLC-Plugin als Alternative |
| **Cross-Platform-Bugs** | Mittel | Mittel | CI/CD mit allen Plattformen |
| **Memory-Leaks** | Mittel | Niedrig | Valgrind, AddressSanitizer, Smart Pointers |

---

## 11. Fazit

### ✅ Machbar
Die Portierung ist **definitiv machbar** mit den vorgeschlagenen Technologien.

### 📊 Aufwand
- **Erfahrener C++-Entwickler**: 4-6 Wochen
- **Junior-Entwickler**: 8-12 Wochen
- **Python-Entwickler (neu in C++)**: 12-16 Wochen

### 💡 Empfehlung
1. **Starte mit Proof of Concept** (1 Woche)
2. **Evaluiere wxWidgets vs. Qt** anhand der Lizenzanforderungen
3. **Nutze Header-only Libraries** wo möglich (cpp-httplib, WebSocketPP)
4. **Vermeide Boost** wenn möglich (reduziert Komplexität)
5. **Plane 20% Puffer** für unvorhergesehene Probleme

### 🚀 Next Steps
1. CMake-Projekt aufsetzen
2. Protobuf-Dateien kompilieren
3. Minimale wxWidgets-App erstellen
4. WebSocket-Verbindung testen
5. Ersten Befehl implementieren (z.B. Device Info)

---

## Anhang A: Minimal Viable Product (MVP)

Für einen schnellen Start:

```cpp
// main.cpp - Minimal wxWidgets + WebSocket
#include <wx/wx.h>
#include <websocketpp/client.hpp>
#include <websocketpp/config/asio_no_tls_client.hpp>

typedef websocketpp::client<websocketpp::config::asio_client> client;

class DwarfApp : public wxApp {
public:
    virtual bool OnInit() {
        DwarfFrame* frame = new DwarfFrame();
        frame->Show(true);
        return true;
    }
};

class DwarfFrame : public wxFrame {
public:
    DwarfFrame() : wxFrame(NULL, wxID_ANY, "DWARF II Controller") {
        wxPanel* panel = new wxPanel(this);
        wxBoxSizer* sizer = new wxBoxSizer(wxVERTICAL);
        
        ipInput = new wxTextCtrl(panel, wxID_ANY, "192.168.88.1");
        connectBtn = new wxButton(panel, wxID_ANY, "Connect");
        statusText = new wxStaticText(panel, wxID_ANY, "Disconnected");
        
        sizer->Add(ipInput, 0, wxEXPAND | wxALL, 5);
        sizer->Add(connectBtn, 0, wxEXPAND | wxALL, 5);
        sizer->Add(statusText, 0, wxEXPAND | wxALL, 5);
        
        panel->SetSizer(sizer);
        
        connectBtn->Bind(wxEVT_BUTTON, &DwarfFrame::OnConnect, this);
    }
    
private:
    wxTextCtrl* ipInput;
    wxButton* connectBtn;
    wxStaticText* statusText;
    client wsClient;
    
    void OnConnect(wxCommandEvent& event) {
        std::string ip = ipInput->GetValue().ToStdString();
        std::string uri = "ws://" + ip + ":9900";
        
        try {
            wsClient.init_asio();
            
            websocketpp::lib::error_code ec;
            client::connection_ptr con = wsClient.get_connection(uri, ec);
            
            if (ec) {
                statusText->SetLabel("Connection failed: " + ec.message());
                return;
            }
            
            wsClient.connect(con);
            wsClient.run();
            
            statusText->SetLabel("Connected to " + ip);
        } catch (const std::exception& e) {
            statusText->SetLabel("Error: " + std::string(e.what()));
        }
    }
};

wxIMPLEMENT_APP(DwarfApp);
```

**Kompilieren:**
```bash
g++ main.cpp -o dwarf_controller \
    `wx-config --cxxflags --libs` \
    -lwebsocketpp \
    -lboost_system \
    -lpthread
```

Dies ist ein funktionierender Startpunkt für die Entwicklung!
