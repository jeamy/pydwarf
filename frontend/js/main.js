/**
 * DWARF II Control - Main Application
 */

import api from './api-client.js';
import { STATUS } from './constants.js';

class App {
    constructor() {
        this.currentIP = null;
        this.connectionStatus = STATUS.DISCONNECTED;
        this.cameraOpen = false;
        this.albumState = {
            mediaType: 1,
            pageIndex: 0,
            pageSize: 12,
            hasMore: false
        };
        this.mediaTypeLabels = {
            0: 'Alle',
            1: 'Fotos',
            2: 'Videos',
            3: 'Serien',
            4: 'Astro',
            5: 'Panorama'
        };
        this.init();
    }

    init() {
        console.log('🚀 [INIT] Initialisiere App...');
        this.setupNavigation();
        this.setupEventListeners();
        this.updateConnectionStatus();
        // Verstecke Controls initial (nicht verbunden)
        this.hideControls();
        console.log('✅ [INIT] App bereit');
    }

    setupNavigation() {
        const navButtons = document.querySelectorAll('.nav-btn');
        const views = document.querySelectorAll('.view');

        navButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const viewName = btn.dataset.view;
                
                // Update active nav button
                navButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                // Show corresponding view
                views.forEach(v => v.classList.remove('active'));
                document.getElementById(`${viewName}View`).classList.add('active');
            });
        });
    }

    setupEventListeners() {
        // Connection
        document.getElementById('scanBtn').addEventListener('click', () => this.scanNetwork());
        document.getElementById('connectBtn').addEventListener('click', () => this.connect());
        document.getElementById('disconnectBtn').addEventListener('click', () => this.disconnect());
        
        // Camera
        document.getElementById('teleOpenBtn').addEventListener('click', () => this.openCamera());
        document.getElementById('teleCloseBtn').addEventListener('click', () => this.closeCamera());
        document.getElementById('telePhotoBtn').addEventListener('click', () => this.takePhoto());
        document.getElementById('teleVideoStartBtn').addEventListener('click', () => this.startVideo());
        document.getElementById('teleVideoStopBtn').addEventListener('click', () => this.stopVideo());
        document.getElementById('streamStartBtn').addEventListener('click', () => this.startStream());
        document.getElementById('streamStopBtn').addEventListener('click', () => this.stopStream());

        // Album
        document.getElementById('albumRefreshBtn').addEventListener('click', () => this.loadAlbum(true));
        document.getElementById('albumMediaType').addEventListener('change', (event) => {
            this.albumState.mediaType = parseInt(event.target.value, 10);
            this.albumState.pageIndex = 0;
            this.loadAlbum(true);
        });
        document.getElementById('albumPrevBtn').addEventListener('click', () => {
            if (this.albumState.pageIndex > 0) {
                this.albumState.pageIndex -= 1;
                this.loadAlbum();
            }
        });
        document.getElementById('albumNextBtn').addEventListener('click', () => {
            if (this.albumState.hasMore) {
                this.albumState.pageIndex += 1;
                this.loadAlbum();
            }
        });
        
        // Astro
        document.getElementById('calibrationStartBtn').addEventListener('click', () => this.startCalibration());
        document.getElementById('calibrationStopBtn').addEventListener('click', () => this.stopCalibration());
        document.getElementById('gotoDsoBtn').addEventListener('click', () => this.gotoDSO());
        document.getElementById('gotoStopBtn').addEventListener('click', () => this.stopGoto());
        document.getElementById('stackingStartBtn').addEventListener('click', () => this.startStacking());
        document.getElementById('stackingStopBtn').addEventListener('click', () => this.stopStacking());
        
        // Focus
        document.getElementById('autoFocusBtn').addEventListener('click', () => this.autoFocus());
        document.getElementById('astroFocusSlowBtn').addEventListener('click', () => this.astroFocus(0));
        document.getElementById('astroFocusFastBtn').addEventListener('click', () => this.astroFocus(1));
        document.getElementById('astroFocusStopBtn').addEventListener('click', () => this.stopAstroFocus());
        document.getElementById('focusFarBtn').addEventListener('click', () => this.manualFocus(0));
        document.getElementById('focusNearBtn').addEventListener('click', () => this.manualFocus(1));
        
        // Motor
        document.getElementById('motorUpBtn').addEventListener('click', () => this.moveMotor(90));
        document.getElementById('motorDownBtn').addEventListener('click', () => this.moveMotor(270));
        document.getElementById('motorLeftBtn').addEventListener('click', () => this.moveMotor(180));
        document.getElementById('motorRightBtn').addEventListener('click', () => this.moveMotor(0));
        document.getElementById('motorStopBtn').addEventListener('click', () => this.stopMotor());
    }

    async connect() {
        const ip = document.getElementById('deviceIp').value;
        
        if (!ip) {
            console.error('❌ [CONNECT] Keine IP-Adresse eingegeben');
            this.showError('Bitte IP-Adresse eingeben');
            return;
        }

        console.log(`🔄 [CONNECT] Verbinde mit ${ip}...`);
        
        try {
            this.setConnectionStatus(STATUS.CONNECTING);
            const result = await api.connectDevice(ip);
            
            console.log('📥 [CONNECT] Antwort:', result);
            
            if (result.status === 'connected') {
                this.currentIP = ip;
                api.setIP(ip);
                this.setConnectionStatus(STATUS.CONNECTED);
                this.showDeviceInfo(result);
                this.showSuccess('Verbunden!');
                
                console.log('✅ [CONNECT] Erfolgreich verbunden mit', ip);
                
                // UI-Update
                document.getElementById('connectBtn').style.display = 'none';
                document.getElementById('disconnectBtn').style.display = 'inline-block';
                document.getElementById('deviceIp').disabled = true;
                document.getElementById('devicePort').disabled = true;
                
                // Zeige Controls in allen Views
                this.showControls();
            }
        } catch (error) {
            console.error('❌ [CONNECT] Fehler:', error);
            this.setConnectionStatus(STATUS.ERROR);
            this.showError('Verbindung fehlgeschlagen: ' + error.message);
        }
    }

    disconnect() {
        console.log('🔄 [DISCONNECT] Trenne Verbindung...');
        
        this.currentIP = null;
        api.setIP(null);
        this.setConnectionStatus(STATUS.DISCONNECTED);
        
        // UI-Update
        document.getElementById('connectBtn').style.display = 'inline-block';
        document.getElementById('disconnectBtn').style.display = 'none';
        document.getElementById('deviceIp').disabled = false;
        document.getElementById('devicePort').disabled = false;
        document.getElementById('deviceInfo').style.display = 'none';
        
        // Verstecke Controls
        this.hideControls();
        
        console.log('✅ [DISCONNECT] Getrennt');
        this.showSuccess('Getrennt');
    }

    showControls() {
        console.log('👁️ [UI] Zeige Controls (Verbindung aktiv)');
        // Verstecke "Bitte verbinden" Hinweise
        document.querySelectorAll('.connection-required').forEach(el => {
            el.style.display = 'none';
        });
        // Zeige alle Controls (außer kamera-spezifische)
        document.querySelectorAll('.controls-container').forEach(el => {
            el.style.display = 'block';
        });
        // Zeige "Kamera öffnen" Hinweis
        document.querySelectorAll('.camera-required').forEach(el => {
            el.style.display = 'block';
        });

        // Aktualisiere Album bei Verbindung
        if (this.currentIP) {
            this.loadAlbum(true);
        }
    }

    hideControls() {
        console.log('🙈 [UI] Verstecke Controls (nicht verbunden)');
        // Zeige "Bitte verbinden" Hinweise
        document.querySelectorAll('.connection-required').forEach(el => {
            el.style.display = 'block';
        });
        // Verstecke alle Controls
        document.querySelectorAll('.controls-container').forEach(el => {
            el.style.display = 'none';
        });
        // Verstecke Kamera-Controls
        this.hideCameraControls();
    }

    showCameraControls() {
        console.log('📷 [UI] Zeige Kamera-Controls (Kamera geöffnet)');
        // Verstecke "Kamera öffnen" Hinweis
        document.querySelectorAll('.camera-required').forEach(el => {
            el.style.display = 'none';
        });
        // Zeige Kamera-spezifische Controls
        document.querySelectorAll('.camera-controls').forEach(el => {
            el.style.display = 'block';
        });
    }

    hideCameraControls() {
        console.log('📷 [UI] Verstecke Kamera-Controls (Kamera geschlossen)');
        // Zeige "Kamera öffnen" Hinweis (wenn verbunden)
        if (this.currentIP) {
            document.querySelectorAll('.camera-required').forEach(el => {
                el.style.display = 'block';
            });
        }
        // Verstecke Kamera-spezifische Controls
        document.querySelectorAll('.camera-controls').forEach(el => {
            el.style.display = 'none';
        });
    }

    showSuccess(message) {
        this.showToast(message, 'success');
    }

    showError(message) {
        this.showToast(message, 'error');
    }

    showInfo(message) {
        this.showToast(message, 'info');
    }

    showToast(message, type = 'info') {
        if (!message) return;

        let container = document.getElementById('toastContainer');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toastContainer';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        container.appendChild(toast);

        requestAnimationFrame(() => {
            toast.classList.add('visible');
        });

        setTimeout(() => {
            toast.classList.remove('visible');
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }

    async scanNetwork() {
        const resultsDiv = document.getElementById('scanResults');
        const scanBtn = document.getElementById('scanBtn');
        const subnetInput = document.getElementById('scanSubnet');
        
        // UI-Update
        scanBtn.disabled = true;
        scanBtn.textContent = '🔄 Scanne...';
        
        const subnet = subnetInput.value.trim();
        
        if (subnet) {
            // Spezifisches Subnetz scannen
            resultsDiv.innerHTML = `<div class="scan-loading">Scanne ${subnet}.1-254 nach DWARF II...<br><small>Dies kann 10-20 Sekunden dauern</small></div>`;
        } else {
            // Auto-Scan
            resultsDiv.innerHTML = '<div class="scan-loading">Scanne gängige Netzwerke (192.168.88, 192.168.8, etc.)...<br><small>Dies kann 10-20 Sekunden dauern</small></div>';
        }
        
        try {
            let result;
            
            if (subnet) {
                // Spezifisches Subnetz - scannt alle 254 IPs
                result = await api.request(`/scanner/scan/network?subnet=${subnet}`);
            } else {
                // Quick-Scan über gängige Subnetze - scannt alle 254 IPs pro Netz
                result = await api.request('/scanner/scan/quick');
            }
            
            if (result.found_devices === 0) {
                resultsDiv.innerHTML = `
                    <div class="scan-empty">
                        ❌ Kein DWARF II gefunden<br>
                        <small>Gescannte IPs: ${result.scanned_ips}</small><br>
                        <small>Prüfe ob das Gerät eingeschaltet ist</small>
                    </div>
                `;
            } else {
                let html = `<div style="margin-bottom: 0.5rem; color: var(--success); font-weight: 600;">
                    ✅ ${result.found_devices} DWARF II gefunden! (${result.scanned_ips} IPs gescannt)
                </div>`;
                
                result.devices.forEach(device => {
                    html += `
                        <div class="scan-item">
                            <div class="scan-item-info">
                                <div class="scan-item-ip">${device.ip}</div>
                                <div class="scan-item-ports">
                                    ${device.ports.http ? '✅' : '❌'} HTTP | 
                                    ${device.ports.stream ? '✅' : '❌'} Stream | 
                                    ${device.ports.websocket ? '✅' : '❌'} WebSocket
                                </div>
                            </div>
                            <button class="scan-item-btn" data-ip="${device.ip}">
                                Verwenden
                            </button>
                        </div>
                    `;
                });
                resultsDiv.innerHTML = html;
                
                // Event-Delegation für "Verwenden"-Buttons
                resultsDiv.querySelectorAll('.scan-item-btn').forEach(btn => {
                    btn.addEventListener('click', () => {
                        this.useScannedIP(btn.dataset.ip);
                    });
                });
                
                this.showSuccess(`${result.found_devices} DWARF II gefunden!`);
            }
            
        } catch (error) {
            resultsDiv.innerHTML = `
                <div class="scan-empty">
                    ❌ Scan fehlgeschlagen<br>
                    <small>${error.message}</small>
                </div>
            `;
            this.showError('Scan fehlgeschlagen: ' + error.message);
        } finally {
            scanBtn.disabled = false;
            scanBtn.textContent = '🔍 Netzwerk scannen';
        }
    }

    useScannedIP(ip) {
        document.getElementById('deviceIp').value = ip;
        this.showSuccess(`IP ${ip} übernommen`);
    }

    async openCamera() {
        if (!this.checkConnection()) return;
        
        console.log('🔄 [CAMERA] Öffne Kamera...');
        console.log('📍 [CAMERA] IP:', this.currentIP);
        
        try {
            const result = await api.openTeleCamera(this.currentIP);
            console.log('📥 [CAMERA] Antwort:', result);
            
            if (result.status === 'success') {
                console.log('✅ [CAMERA] Kamera erfolgreich geöffnet');
                this.cameraOpen = true;
                this.showCameraControls();
                this.showSuccess('Kamera geöffnet - Warte 2-3 Sekunden!');
            } else if (result.status === 'no_response') {
                console.error('❌ [CAMERA] Keine Antwort vom Gerät (Timeout)');
                console.error('💡 [CAMERA] Mögliche Ursachen:');
                console.error('   1. Gerät ist beschäftigt (warte 5 Sekunden)');
                console.error('   2. WebSocket-Verbindung unterbrochen');
                console.error('   3. Gerät muss neu gestartet werden');
                this.showError('Timeout: Gerät antwortet nicht. Warte 5 Sekunden und versuche es erneut.');
            } else if (result.code === 374) {
                console.warn('⚠️ [CAMERA] Code 374: Kamera bereits geöffnet oder beschäftigt');
                this.cameraOpen = true;
                this.showCameraControls();
                this.showSuccess('Kamera ist bereits geöffnet');
            } else if (result.code === 0) {
                console.log('✅ [CAMERA] Code 0: Erfolgreich');
                this.cameraOpen = true;
                this.showCameraControls();
                this.showSuccess('Kamera geöffnet - Warte 2-3 Sekunden!');
            } else {
                console.warn('⚠️ [CAMERA] Unerwarteter Status:', result);
                const errorMsg = this.getCameraErrorMessage(result.code);
                this.showError(`Kamera-Fehler (Code ${result.code}): ${errorMsg}`);
            }
        } catch (error) {
            console.error('❌ [CAMERA] Fehler beim Öffnen:', error);
            this.showError('Fehler: ' + error.message);
        }
    }

    getCameraErrorMessage(code) {
        const errorCodes = {
            0: 'Erfolg',
            374: 'Kamera bereits geöffnet oder beschäftigt',
            375: 'Kamera-Hardware-Fehler',
            376: 'Timeout',
            377: 'Ungültige Parameter',
            378: 'Nicht unterstützt',
            379: 'Gerät beschäftigt'
        };
        return errorCodes[code] || 'Unbekannter Fehler';
    }

    async closeCamera() {
        if (!this.checkConnection()) return;
        
        console.log('🔄 [CAMERA] Schließe Kamera...');
        
        try {
            const result = await api.closeTeleCamera(this.currentIP);
            console.log('📥 [CAMERA] Antwort:', result);
            
            if (result.status === 'success' || result.code === 0) {
                console.log('✅ [CAMERA] Kamera geschlossen');
                this.cameraOpen = false;
                this.hideCameraControls();
                this.showSuccess('Kamera geschlossen');
            }
        } catch (error) {
            console.error('❌ [CAMERA] Fehler:', error);
            this.showError('Fehler: ' + error.message);
        }
    }

    async takePhoto() {
        if (!this.checkConnection()) return;
        
        console.log('🔄 [CAMERA] Nehme Foto auf...');
        
        try {
            const result = await api.takePhoto(this.currentIP);
            console.log('📥 [CAMERA] Antwort:', result);
            
            if (result.status === 'success') {
                console.log('✅ [CAMERA] Foto aufgenommen');
                this.showSuccess('Foto aufgenommen');
                await this.loadAlbum(true);
            }
        } catch (error) {
            console.error('❌ [CAMERA] Fehler:', error);
            this.showError('Fehler: ' + error.message);
        }
    }

    async startCalibration() {
        if (!this.checkConnection()) return;
        
        try {
            const result = await api.startCalibration(this.currentIP);
            if (result.status === 'success') {
                this.showSuccess('Kalibrierung gestartet');
            }
        } catch (error) {
            this.showError('Fehler: ' + error.message);
        }
    }

    async startStacking() {
        if (!this.checkConnection()) return;
        
        try {
            const result = await api.startStacking(this.currentIP);
            if (result.status === 'success') {
                this.showSuccess('Stacking gestartet');
            }
        } catch (error) {
            this.showError('Fehler: ' + error.message);
        }
    }

    async autoFocus() {
        if (!this.checkConnection()) return;
        
        try {
            const result = await api.autoFocus(this.currentIP);
            if (result.status === 'success') {
                this.showSuccess('Auto-Fokus gestartet');
            }
        } catch (error) {
            this.showError('Fehler: ' + error.message);
        }
    }

    async startVideo() {
        if (!this.checkConnection()) return;
        try {
            const result = await api.startVideo(this.currentIP);
            if (result.status === 'success') this.showSuccess('Video gestartet');
        } catch (error) {
            this.showError('Fehler: ' + error.message);
        }
    }

    async stopVideo() {
        if (!this.checkConnection()) return;
        try {
            const result = await api.stopVideo(this.currentIP);
            if (result.status === 'success') this.showSuccess('Video gestoppt');
        } catch (error) {
            this.showError('Fehler: ' + error.message);
        }
    }

    startStream() {
        if (!this.checkConnection()) return;
        
        console.log('🔄 [STREAM] Starte Stream...');
        console.log('📍 [STREAM] IP:', this.currentIP);
        
        const img = document.getElementById('liveStream');
        const placeholder = document.getElementById('streamPlaceholder');
        const streamUrl = `http://localhost:8000/api/camera/stream/tele?ip=${this.currentIP}`;
        
        console.log('🌐 [STREAM] URL:', streamUrl);
        
        img.src = streamUrl;
        img.classList.add('active');
        placeholder.style.display = 'none';
        
        // Logging für Bild-Events
        img.onload = () => {
            console.log('✅ [STREAM] Stream lädt erfolgreich');
        };
        img.onerror = (e) => {
            console.error('❌ [STREAM] Stream-Fehler:', e);
            console.error('❌ [STREAM] Mögliche Ursachen:');
            console.error('   - Kamera nicht geöffnet');
            console.error('   - Port 8092 nicht erreichbar');
            console.error('   - Backend-Proxy-Problem');
        };
        
        console.log('✅ [STREAM] Stream gestartet');
        this.showSuccess('Stream gestartet');
    }

    stopStream() {
        console.log('🔄 [STREAM] Stoppe Stream...');
        
        const img = document.getElementById('liveStream');
        const placeholder = document.getElementById('streamPlaceholder');
        img.src = '';
        img.classList.remove('active');
        placeholder.style.display = 'block';
        
        console.log('✅ [STREAM] Stream gestoppt');
        this.showSuccess('Stream gestoppt');
    }

    async stopCalibration() {
        if (!this.checkConnection()) return;
        try {
            const result = await api.stopCalibration(this.currentIP);
            if (result.status === 'success') this.showSuccess('Kalibrierung gestoppt');
        } catch (error) {
            this.showError('Fehler: ' + error.message);
        }
    }

    async gotoDSO() {
        if (!this.checkConnection()) return;
        const ra = parseFloat(document.getElementById('gotoRa').value);
        const dec = parseFloat(document.getElementById('gotoDec').value);
        const target = document.getElementById('gotoTarget').value;
        
        if (!ra || !dec || !target) {
            this.showError('Bitte alle Felder ausfüllen');
            return;
        }
        
        try {
            const result = await api.request('/astro/goto/dso?ip=' + this.currentIP, {
                method: 'POST',
                body: { ra, dec, target_name: target }
            });
            if (result.status === 'success') this.showSuccess(`GOTO ${target} gestartet`);
        } catch (error) {
            this.showError('Fehler: ' + error.message);
        }
    }

    async stopGoto() {
        if (!this.checkConnection()) return;
        try {
            const result = await api.request('/astro/goto/stop?ip=' + this.currentIP, {
                method: 'POST'
            });
            if (result.status === 'success') this.showSuccess('GOTO gestoppt');
        } catch (error) {
            this.showError('Fehler: ' + error.message);
        }
    }

    async stopStacking() {
        if (!this.checkConnection()) return;
        try {
            const result = await api.stopStacking(this.currentIP);
            if (result.status === 'success') this.showSuccess('Stacking gestoppt');
        } catch (error) {
            this.showError('Fehler: ' + error.message);
        }
    }

    async astroFocus(mode) {
        if (!this.checkConnection()) return;
        try {
            const result = await api.startAstroFocus(this.currentIP, mode);
            const modeName = mode === 0 ? 'Langsam' : 'Schnell';
            if (result.status === 'success') this.showSuccess(`Astro-Fokus ${modeName} gestartet`);
        } catch (error) {
            this.showError('Fehler: ' + error.message);
        }
    }

    async stopAstroFocus() {
        if (!this.checkConnection()) return;
        try {
            const result = await api.request('/focus/astro/stop?ip=' + this.currentIP, {
                method: 'POST'
            });
            if (result.status === 'success') this.showSuccess('Astro-Fokus gestoppt');
        } catch (error) {
            this.showError('Fehler: ' + error.message);
        }
    }

    async manualFocus(direction) {
        if (!this.checkConnection()) return;
        try {
            const result = await api.request('/focus/manual/step?ip=' + this.currentIP, {
                method: 'POST',
                body: { direction }
            });
            const dirName = direction === 0 ? 'Fern' : 'Nah';
            if (result.status === 'success') this.showSuccess(`Fokus ${dirName}`);
        } catch (error) {
            this.showError('Fehler: ' + error.message);
        }
    }

    async moveMotor(angle) {
        if (!this.checkConnection()) return;
        try {
            const result = await api.request('/motor/joystick/start?ip=' + this.currentIP, {
                method: 'POST',
                body: {
                    vector_angle: angle,
                    vector_length: 1.0,
                    speed: 5.0
                }
            });
            if (result.status === 'success') this.showSuccess('Motor bewegt');
        } catch (error) {
            this.showError('Fehler: ' + error.message);
        }
    }

    async stopMotor() {
        if (!this.checkConnection()) return;
        
        try {
            const result = await api.stopMotor(this.currentIP);
            if (result.status === 'success') {
                this.showSuccess('Motor gestoppt');
            }
        } catch (error) {
            this.showError('Fehler: ' + error.message);
        }
    }

    checkConnection() {
        if (!this.currentIP) {
            this.showError('Nicht verbunden');
            return false;
        }
        return true;
    }

    setConnectionStatus(status) {
        this.connectionStatus = status;
        this.updateConnectionStatus();
    }

    updateConnectionStatus() {
        const indicator = document.getElementById('statusIndicator');
        const text = document.getElementById('statusText');
        
        switch (this.connectionStatus) {
            case STATUS.CONNECTED:
                indicator.classList.add('connected');
                text.textContent = `Verbunden (${this.currentIP})`;
                break;
            case STATUS.CONNECTING:
                indicator.classList.remove('connected');
                text.textContent = 'Verbinde...';
                break;
            case STATUS.ERROR:
                indicator.classList.remove('connected');
                text.textContent = 'Fehler';
                break;
            default:
                indicator.classList.remove('connected');
                text.textContent = 'Nicht verbunden';
        }
    }

    showDeviceInfo(data) {
        const infoCard = document.getElementById('deviceInfo');
        infoCard.style.display = 'block';
        infoCard.innerHTML = `
            <h3>Gerät verbunden</h3>
            <p><strong>Name:</strong> ${data.device?.device_name || 'N/A'}</p>
            <p><strong>IP:</strong> ${data.device?.ip_address || 'N/A'}</p>
        `;
    }

    async loadAlbum(resetPage = false) {
        if (!this.checkConnection()) return;

        const listEl = document.getElementById('albumList');
        const countsEl = document.getElementById('albumCounts');
        const pageInfoEl = document.getElementById('albumPageInfo');
        const prevBtn = document.getElementById('albumPrevBtn');
        const nextBtn = document.getElementById('albumNextBtn');

        if (resetPage) {
            this.albumState.pageIndex = 0;
        }

        pageInfoEl.textContent = `Seite ${this.albumState.pageIndex + 1}`;
        listEl.innerHTML = '<div class="album-empty">Lade Medien...</div>';

        try {
            const [countsResponse, listResponse] = await Promise.all([
                api.getAlbumCounts(this.currentIP),
                api.getAlbumList(this.currentIP, {
                    media_type: this.albumState.mediaType,
                    page_index: this.albumState.pageIndex,
                    page_size: this.albumState.pageSize
                })
            ]);

            this.renderAlbumCounts(countsResponse, countsEl);
            const items = this.extractAlbumItems(listResponse);
            this.albumState.hasMore = items.length === this.albumState.pageSize;
            prevBtn.disabled = this.albumState.pageIndex === 0;
            nextBtn.disabled = !this.albumState.hasMore;
            this.renderAlbumList(items, listEl);
        } catch (error) {
            console.error('❌ [ALBUM] Fehler:', error);
            listEl.innerHTML = '<div class="album-empty">Fehler beim Laden der Medien</div>';
            this.showError('Album konnte nicht geladen werden: ' + error.message);
            prevBtn.disabled = true;
            nextBtn.disabled = true;
        }
    }

    renderAlbumCounts(response, container) {
        const data = response?.data || response;

        if (!Array.isArray(data) || data.length === 0) {
            container.innerHTML = '<div class="album-empty">Keine Medien gefunden</div>';
            return;
        }

        container.innerHTML = data
            .map(item => {
                const label = this.mediaTypeLabels[item.mediaType] || `Typ ${item.mediaType}`;
                return `<div class="album-count"><strong>${label}:</strong> ${item.count}</div>`;
            })
            .join('');
    }

    extractAlbumItems(response) {
        if (!response) return [];
        if (Array.isArray(response.data)) return response.data;
        if (Array.isArray(response.list)) return response.list;
        if (response.data?.list) return response.data.list;
        if (response.mediaInfos) return response.mediaInfos;
        return [];
    }

    renderAlbumList(items, container) {
        if (!items || items.length === 0) {
            container.innerHTML = '<div class="album-empty">Keine Medien auf dieser Seite</div>';
            return;
        }

        container.innerHTML = items.map(item => {
            const name = item.fileName || item.file_name || 'Unbekannt';
            const path = item.filePath || item.file_path || '';
            const size = this.formatBytes(item.fileSize || item.file_size || 0);
            const timestamp = item.modificationTime || item.modification_time || item.createTime || null;
            const date = timestamp ? new Date(timestamp * 1000).toLocaleString() : '—';
            return `
                <div class="album-card">
                    <div class="album-card-thumb">${this.getAlbumIcon()}</div>
                    <div class="album-card-meta">
                        <div class="album-card-title">${name}</div>
                        <div class="album-card-path">${path}</div>
                        <div class="album-card-info">${date} • ${size}</div>
                    </div>
                </div>
            `;
        }).join('');
    }

    getAlbumIcon() {
        const type = this.albumState.mediaType;
        switch (type) {
            case 2:
                return '🎥';
            case 3:
                return '📸';
            case 4:
                return '🌌';
            case 5:
                return '📷';
            default:
                return '🖼️';
        }
    }

    formatBytes(bytes) {
        if (!bytes) return '0 B';
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(1024));
        return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`;
    }
}

// Initialize app - global variable für onclick-Handler
window.app = null;

document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
});
