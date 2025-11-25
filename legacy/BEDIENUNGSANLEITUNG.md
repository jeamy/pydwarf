# DWARF II Control - Bedienungsanleitung

## 🚀 Schnellstart

### Schritt 1: Verbinden ✅
1. Öffne http://localhost:8000/static/
2. Gehe zu "🔌 Verbindung"
3. Klicke "🔍 Netzwerk scannen" (findet dein DWARF II)
4. Klicke "Verwenden" bei gefundenem Gerät
5. Klicke "Verbinden"
6. Status zeigt: "🟢 Verbunden (192.168.8.223)"

### Schritt 2: Kamera öffnen ⚠️ WICHTIG!
1. Gehe zu "📷 Kamera"
2. Klicke "Öffnen"
3. **WARTE 2-3 Sekunden!**
4. Du hörst ein Klicken am Gerät
5. Erfolg-Meldung: "Kamera geöffnet"

**OHNE diesen Schritt funktioniert NICHTS!**

### Schritt 3: Funktionen nutzen
Jetzt kannst du alle Funktionen nutzen:
- 📷 Foto aufnehmen
- 🎥 Video aufnehmen
- 📹 Live-Stream starten
- 🌌 Astro-Funktionen
- 🎯 Fokus-Steuerung
- 🕹️ Motor-Steuerung

---

## 📷 Kamera-Funktionen

### Kamera-Steuerung
- **Öffnen**: Öffnet die Kamera (IMMER ZUERST!)
- **Schließen**: Schließt die Kamera (am Ende)

### Aufnahme
- **📷 Foto**: Macht ein Foto (gespeichert auf DWARF II)
- **🎥 Video Start**: Startet Videoaufnahme
- **⏹️ Video Stop**: Stoppt Videoaufnahme

### Live-Stream
1. Scrolle runter zum "Live-Stream" Bereich
2. Klicke "Stream starten"
3. Stream erscheint im 16:9 Container
4. Klicke "Stream stoppen" zum Beenden

**Stream-URL**: `http://192.168.8.223:8092/stream?video=0`

---

## 🌌 Astro-Funktionen

### Kalibrierung
1. **Start**: Startet Polar-Alignment
2. **Stop**: Stoppt Kalibrierung

### GOTO (Objekt anfahren)
1. Trage ein:
   - **Target Name**: z.B. "M31" (Andromeda)
   - **RA**: Rektaszension in Stunden (z.B. 0.712)
   - **Dec**: Deklination in Grad (z.B. 41.269)
2. Klicke "GOTO Start"
3. DWARF II fährt zum Objekt
4. "GOTO Stop" zum Abbrechen

**Beispiel-Objekte**:
- M31 (Andromeda): RA 0.712, Dec 41.269
- M42 (Orion): RA 5.583, Dec -5.391
- M45 (Plejaden): RA 3.783, Dec 24.117

### Stacking
1. **Start**: Startet Astro-Stacking
2. **Stop**: Stoppt Stacking

---

## 🎯 Fokus-Funktionen

### Auto-Fokus
- Klicke "Auto-Fokus starten"
- DWARF II fokussiert automatisch
- Dauert 10-30 Sekunden

### Astro-Fokus (für Sterne)
- **Langsam**: Langsame Fokus-Bewegung
- **Schnell**: Schnelle Fokus-Bewegung
- **Stop**: Stoppt Bewegung

### Manueller Fokus
- **← Fern**: Fokus nach Fern (Unendlich)
- **Nah →**: Fokus nach Nah
- Jeder Klick = 1 Schritt

---

## 🕹️ Motor-Funktionen

### Richtungs-Steuerung
```
       ↑
       
  ←  ⏹️  →
  
       ↓
```

- **↑**: Nach oben (90°)
- **↓**: Nach unten (270°)
- **←**: Nach links (180°)
- **→**: Nach rechts (0°)
- **⏹️ Stop**: Stoppt Bewegung

**Geschwindigkeit**: 5.0 (fest)
**Länge**: 1.0 (fest)

---

## ⚠️ Wichtige Hinweise

### Reihenfolge IMMER:
1. ✅ Verbinden
2. ✅ Kamera öffnen
3. ✅ 2-3 Sekunden warten
4. ✅ Funktionen nutzen

### Häufige Fehler:

**❌ "Kamera öffnen" reagiert nicht**
- Lösung: Bist du verbunden? (Status oben rechts prüfen)

**❌ Stream zeigt nichts**
- Lösung: Kamera geöffnet? Warte 2-3 Sekunden nach Öffnen

**❌ Befehle funktionieren nicht**
- Lösung: Kamera muss geöffnet sein!

**❌ "Verbindung fehlgeschlagen"**
- Lösung: DWARF II eingeschaltet? Im richtigen WLAN?

### Wartezeiten:
- Nach "Kamera öffnen": **2-3 Sekunden**
- Nach "Verbinden": **1 Sekunde**
- Zwischen Befehlen: **1-2 Sekunden**

### Ports:
- **8082**: HTTP API (Befehle)
- **8092**: JPG Stream (Live-Bild)
- **9900**: WebSocket (Kommunikation)

---

## 🔧 Troubleshooting

### Stream funktioniert nicht:

**Checkliste**:
1. ✅ Verbunden?
2. ✅ Kamera geöffnet?
3. ✅ 2-3 Sekunden gewartet?
4. ✅ "Stream starten" geklickt?
5. ✅ Runter gescrollt zu den Buttons?

**Direkt-Test**:
```bash
# Öffne im Browser:
http://192.168.8.223:8092/stream?video=0
```

Wenn das funktioniert, ist das Problem im Frontend.

### Kamera öffnet nicht:

**Test**:
```bash
curl -X POST "http://localhost:8000/api/camera/tele/open?ip=192.168.8.223" \
  -H "Content-Type: application/json" \
  -d '{"binning": false, "rtsp_encode_type": 0}'
```

**Erwartete Antwort**:
```json
{"status": "success"}
```

### Verbindung prüfen:

```bash
# Gerät erreichbar?
ping 192.168.8.223

# Ports offen?
nmap -p 8082,8092,9900 192.168.8.223
```

---

## 📊 Status-Anzeige

**Oben rechts im Header**:
- 🔴 Nicht verbunden
- 🟡 Verbinde...
- 🟢 Verbunden (IP-Adresse)
- ❌ Fehler

---

## 💡 Tipps & Tricks

### Workflow für Astro-Fotografie:
1. Verbinden
2. Kamera öffnen
3. Kalibrierung starten (Polar-Alignment)
4. GOTO zu Objekt
5. Auto-Fokus
6. Stacking starten
7. Warten...

### Workflow für Mond/Planeten:
1. Verbinden
2. Kamera öffnen
3. Stream starten (Objekt suchen)
4. Manuell fokussieren
5. Video aufnehmen

### Workflow für Tageslicht:
1. Verbinden
2. Kamera öffnen
3. Stream starten
4. Fotos machen

---

## 🆘 Support

Bei Problemen siehe:
- `TROUBLESHOOTING.md` - Detaillierte Problemlösungen
- `PROGRESS.md` - Projekt-Status
- Browser-Console (F12) - Fehler-Logs
- Backend-Logs: `docker compose logs -f`

---

## 🎯 Zusammenfassung

**Die 3 goldenen Regeln**:
1. **IMMER zuerst verbinden**
2. **IMMER Kamera öffnen**
3. **IMMER 2-3 Sekunden warten**

**Dann funktioniert alles!** ✨
