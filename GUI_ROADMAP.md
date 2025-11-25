# GUI Design Roadmap & UX Spezifikation

Diese Roadmap definiert das visuelle Design und die Benutzeroberfläche (GUI) für die DWARF II Qt-Anwendung. Das Ziel ist eine professionelle, "Cockpit"-artige Oberfläche, die alle Funktionen logisch gruppiert und für die Nachtnutzung optimiert ist.

## 1. Design-Philosophie

*   **Dark Mode First:** Die gesamte Anwendung nutzt ein dunkles Farbschema (#2D2D30), um die Dunkeladaption der Augen bei der Astrofotografie nicht zu stören.
*   **Modulares Layout:** Verwendung von "Docking Widgets". Der Nutzer kann Bereiche anpassen, aber der Standard ist fest definiert.
*   **Fokus auf das Bild:** Der Live-Stream nimmt immer den maximal verfügbaren Platz ein.
*   **Visuelles Feedback:** Aktive Zustände (z.B. "Aufnahme läuft", "Verbunden") werden durch klare Signalfarben (Orange/Rot) hervorgehoben.

## 2. Layout-Struktur (Main Window)

Das Hauptfenster (`QMainWindow`) ist in drei Bereiche unterteilt:

### A. Zentraler Bereich (Viewport)
*   **Komponente:** `QVideoWidget` (oder VLC-Wrapper).
*   **Inhalt:** Zeigt den Live-Stream (Tele oder Weitwinkel).
*   **HUD (Heads-Up Display):** Transparente Overlays über dem Video:
    *   *Oben Links:* Akku-Stand (%), Speicherplatz (SD).
    *   *Oben Rechts:* Ziel-Objekt (z.B. "M42"), Verbindungsstatus.
    *   *Mitte:* Optionales Fadenkreuz (ein-/ausschaltbar).
    *   *Unten:* Status der aktuellen Aktion (z.B. "Stacking: 15 Frames").

### B. Rechte Seitenleiste (Control Deck)
*   **Komponente:** `QDockWidget` mit einem `QTabWidget`.
*   **Breite:** Fixiert (ca. 300-350px), aber einklappbar.
*   **Inhalt:** Beherbergt alle Steuerungsfunktionen in Tabs (siehe Punkt 3).

### C. Fußleiste (Status Bar)
*   **Komponente:** `QStatusBar`.
*   **Inhalt:** Technische Telemetrie.
    *   IP-Adresse.
    *   Aktuelle FPS des Streams.
    *   Ping/Latenz.
    *   Temperatur des Sensors (falls verfügbar).

---

## 3. Funktions-Module (Tabs)

Hier werden "alle Funktionen" logisch sortiert.

### Tab 1: 📷 Kamera & Aufnahme (Standard)
Der wichtigste Tab für die allgemeine Nutzung.

*   **Stream-Quelle:**
    *   Umschalter: `[ TELE ]` / `[ WIDE ]`.
*   **Aufnahme-Steuerung (Video & Foto):**
    *   Großer Button: `[ FOTO ]`.
    *   Großer Button: `[ REC ]` (Video).
        *   *Funktion:* Startet die Aufnahme auf der **SD-Karte** des DWARF II.
        *   *Status:* Button blinkt rot während der Aufnahme. Timer läuft (00:00:05).
*   **Belichtung (Exposure):**
    *   Modus: `Auto` / `Manuell`.
    *   Slider: Belichtungszeit (Shutter).
    *   Slider: Gain (ISO).
*   **Bild-Parameter:**
    *   Toggle: `IR-Cut` (Tag/Nacht Filter).
    *   Dropdown: `Binning` (4k / 2k).
    *   Slider: Kontrast, Sättigung, Schärfe, Farbton.

### Tab 2: 🔭 Astro & Navigation (Erweitert)
Integration eines vollwertigen Planetariums ("Point & Drive").

*   **Sternkarte (Mini-Planetarium):**
    *   **Komponente:** `StarMapWidget` (Custom `QGraphicsView`).
    *   **Datenbasis:** Integrierte SQLite-Datenbank (HYG Star Catalog + OpenNGC).
    *   **Funktion:** Zeigt den aktuellen Himmel basierend auf GPS-Position und Zeit.
    *   **Interaktion:**
        *   Klick auf Stern/Nebel -> Zeigt Info (Name, Helligkeit, Auf/Untergang).
        *   Doppelklick oder Button `[ GOTO ]` -> Teleskop fährt Objekt an.
    *   **Visualisierung:** Zeigt das aktuelle Sichtfeld (FOV) des Teleskops als Rechteck auf der Karte an.
*   **Objekt-Suche:**
    *   Suchfeld mit Autocomplete (z.B. "Andr..." -> "Andromeda Galaxie (M31)").
    *   Listenansicht: "Heute sichtbar" (Vorschläge für die aktuelle Nacht).
*   **Astro-Aufnahme:**
    *   Einstellung: Anzahl der Bilder (z.B. 100).
    *   Einstellung: Belichtung pro Bild (z.B. 15s).
    *   Button: `[ Start Stacking ]`.
    *   *Live-Feedback:* Kleines Histogramm und Kurve der "Rejected Frames".

### Tab 3: 🕹️ Motor & Fokus
Manuelle Feinsteuerung.

*   **Joystick:**
    *   Virtuelles Steuerkreuz für Pan/Tilt.
    *   Slider: Geschwindigkeit (Speed).
*   **Fokus:**
    *   Button: `[ Auto-Fokus ]`.
    *   Manuell: `<<<` `<<` `<` `>` `>>` `>>>`.
    *   Anzeige: Numerischer Fokus-Wert (0-Max).

### Tab 4: ⚙️ System & Medien
Verwaltung und Einstellungen.

*   **Verbindung:**
    *   Eingabefeld: IP-Adresse.
    *   Button: `Verbinden` / `Trennen`.
*   **Medien-Galerie:**
    *   Button: `[ Galerie öffnen ]`. Lädt Thumbnails von der SD-Karte.
    *   Funktion: Download von Bildern/Videos auf den PC.
*   **Erweitert:**
    *   Firmware-Update.
    *   Log-Download.
    *   *Optional:* Lokale Video-Aufnahme (Stream-Dump auf PC-Festplatte).
    *   **LX200 Server:** Option zum Aktivieren eines lokalen Servers, um externe Apps (SkySafari, Stellarium) zu verbinden.

---

## 4. Visuelles Design (Theme Spezifikation)

Das Design orientiert sich an professioneller Kreativ-Software (Blender, DaVinci Resolve).

*   **Farbschema:**
    *   Hintergrund (App): `#1E1E1E` (Sehr dunkles Grau).
    *   Hintergrund (Panels): `#2D2D30` (Dunkelgrau).
    *   Text (Primary): `#E0E0E0` (Helles Grau, nicht Reinweiß).
    *   Text (Secondary): `#AAAAAA`.
    *   **Akzentfarbe:** `#FF9800` (Orange) oder `#D32F2F` (Dunkelrot) für Nachtmodus.
*   **Typografie:**
    *   Schriftart: `Segoe UI` (Windows) / `Roboto` (Linux) / `San Francisco` (macOS).
    *   Größe: 10pt (Standard), 12pt (Buttons).
*   **Icons:**
    *   Verwendung von Vektor-Icons (SVG) in Weiß/Grau.

## 5. Implementierung in Qt

### Qt Widgets Struktur
```cpp
// MainWindow
QMainWindow
├── QWidget (CentralWidget)
│   └── QVBoxLayout
│       └── QVideoWidget (Der Viewport)
│           └── OverlayWidget (Transparentes HUD darübergelegt)
├── QDockWidget (RightArea)
│   └── QTabWidget
│       ├── QWidget (Tab: Camera)
│       │   └── QFormLayout (Controls)
│       ├── QWidget (Tab: Astro)
│       │   └── QVBoxLayout
│       │       ├── StarMapWidget (Custom QGraphicsView)
│       │       └── QListView (Objekt-Suche/Ergebnisse)
│       ├── QWidget (Tab: Motor)
│       └── QWidget (Tab: Settings)
└── QStatusBar
```

### Video-Aufnahme Logik
Die Frage "Videoaufnahmen sind auch vorgesehen?" wird wie folgt beantwortet:

1.  **Native Aufnahme (SD-Karte):**
    *   Dies ist die primäre Funktion.
    *   Der Button `REC` sendet den Befehl `StartRecording` an das DWARF II.
    *   Das Teleskop speichert die Datei intern (bessere Qualität, kein Netzwerk-Lag).
2.  **Lokale Aufnahme (PC):**
    *   *Optionales Feature.*
    *   Der RTSP-Stream wird direkt auf die Festplatte des PCs geschrieben.
    *   Vorteil: Sofortiger Zugriff ohne Download.
    *   Nachteil: Abhängig von WLAN-Qualität.

## 6. Mockup Referenz
*(Siehe generiertes Bild-Artefakt für visuelle Referenz)*
