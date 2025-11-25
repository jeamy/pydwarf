# Entwicklungsumgebung einrichten

Um die DWARF II Qt-Anwendung zu kompilieren und zu entwickeln, müssen folgende Abhängigkeiten auf dem System installiert sein.

## 1. System-Anforderungen
*   **Betriebssystem:** Linux (empfohlen: Ubuntu 22.04+ / Debian 12+), Windows 10/11, oder macOS.
*   **Compiler:** C++17 kompatibler Compiler (GCC 9+, Clang 10+, MSVC 2019+).
*   **Build System:** CMake 3.16 oder neuer.

## 2. Benötigte Bibliotheken

### Qt 6
Wir verwenden **Qt 6** (mindestens 6.2 LTS, empfohlen 6.5+).
Benötigte Module:
*   `qt6-base` (Core, Gui, Widgets, Network)
*   `qt6-multimedia` (Video-Streaming)

### Protocol Buffers
Für die Kommunikation mit dem Teleskop.
*   `protobuf-compiler` (protoc)
*   `libprotobuf-dev` (C++ Bindings)

## 3. Installation (Fedora Linux)

Da Sie Fedora nutzen (insb. KDE Plasma), sind viele Qt-Bibliotheken oft schon vorhanden. Für die Entwicklung benötigen wir jedoch die Header-Dateien (`-devel`).

Führen Sie folgenden Befehl im Terminal aus:

```bash
sudo dnf install -y \
    cmake \
    gcc-c++ \
    qt6-qtbase-devel \
    qt6-qtmultimedia-devel \
    protobuf-devel \
    protobuf-compiler
```

## 4. Installation (Andere)

### Debian / Ubuntu
```bash
sudo apt-get install -y build-essential cmake qt6-base-dev qt6-multimedia-dev protobuf-compiler libprotobuf-dev
```

### Windows
1.  Installieren Sie den [Qt Online Installer](https://www.qt.io/download-qt-installer).
2.  Wählen Sie bei der Installation **Qt 6.x** und **MinGW** oder **MSVC** aus.
3.  Installieren Sie CMake.
4.  Installieren Sie Protobuf (z.B. via `vcpkg`): `vcpkg install protobuf:x64-windows`.

### macOS
```bash
brew install qt6 cmake protobuf
brew link qt6 --force
```

## 5. Build-Anleitung

```bash
mkdir build
cd build
cmake ..
make -j$(nproc)
./DwarfController
```
