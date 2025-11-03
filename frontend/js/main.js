/**
 * DWARF II Control - Main Application
 */

import api from './api-client.js';
import { STATUS } from './constants.js';

class App {
    constructor() {
        this.currentIP = null;
        this.connectionStatus = STATUS.DISCONNECTED;
        this.currentMediaType = 0;
        this.mediaList = [];
        this.init();
    }

    init() {
        this.setupNavigation();
        this.setupEventListeners();
        this.updateConnectionStatus();
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
        document.getElementById('connectBtn').addEventListener('click', () => this.connect());
        
        // Camera
        document.getElementById('teleOpenBtn').addEventListener('click', () => this.openCamera());
        document.getElementById('teleCloseBtn').addEventListener('click', () => this.closeCamera());
        document.getElementById('telePhotoBtn').addEventListener('click', () => this.takePhoto());
        document.getElementById('teleVideoStartBtn').addEventListener('click', () => this.startVideo());
        document.getElementById('teleVideoStopBtn').addEventListener('click', () => this.stopVideo());
        document.getElementById('streamStartBtn').addEventListener('click', () => this.startStream());
        document.getElementById('streamStopBtn').addEventListener('click', () => this.stopStream());
        
        // Astro
        document.getElementById('calibrationStartBtn').addEventListener('click', () => this.startCalibration());
        document.getElementById('calibrationStopBtn').addEventListener('click', () => this.stopCalibration());
        document.getElementById('gotoDsoBtn').addEventListener('click', () => this.gotoDSO());
        document.getElementById('gotoStopBtn').addEventListener('click', () => this.stopGoto());
        document.getElementById('oneClickGotoBtn').addEventListener('click', () => this.oneClickGoto());
        document.getElementById('oneClickStopBtn').addEventListener('click', () => this.stopOneClickGoto());
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
        document.getElementById('motorStopBtn').addEventListener('click', () => this.stopMotor());
        document.getElementById('motorUpBtn').addEventListener('click', () => this.moveMotor(90));
        document.getElementById('motorDownBtn').addEventListener('click', () => this.moveMotor(270));
        document.getElementById('motorLeftBtn').addEventListener('click', () => this.moveMotor(180));
        document.getElementById('motorRightBtn').addEventListener('click', () => this.moveMotor(0));
        
        // Joystick
        this.setupJoystick();
        
        // Album
        document.getElementById('loadMediaBtn').addEventListener('click', () => this.loadMedia());
        
        // Album filters
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.currentMediaType = parseInt(e.target.dataset.type);
                this.loadMedia();
            });
        });
    }

    async connect() {
        const ip = document.getElementById('deviceIp').value;
        
        if (!ip) {
            this.showError('Bitte IP-Adresse eingeben');
            return;
        }

        try {
            this.setConnectionStatus(STATUS.CONNECTING);
            const result = await api.connectDevice(ip);
            
            if (result.status === 'connected') {
                this.currentIP = ip;
                api.setIP(ip);
                this.setConnectionStatus(STATUS.CONNECTED);
                this.showDeviceInfo(result);
                this.showSuccess('Verbunden!');
            }
        } catch (error) {
            this.setConnectionStatus(STATUS.ERROR);
            this.showError('Verbindung fehlgeschlagen: ' + error.message);
        }
    }

    async openCamera() {
        if (!this.checkConnection()) return;
        
        try {
            const result = await api.openTeleCamera(this.currentIP);
            if (result.status === 'success') {
                this.showSuccess('Kamera geöffnet');
            }
        } catch (error) {
            this.showError('Fehler: ' + error.message);
        }
    }

    async closeCamera() {
        if (!this.checkConnection()) return;
        
        try {
            const result = await api.closeTeleCamera(this.currentIP);
            if (result.status === 'success') {
                this.showSuccess('Kamera geschlossen');
            }
        } catch (error) {
            this.showError('Fehler: ' + error.message);
        }
    }

    async takePhoto() {
        if (!this.checkConnection()) return;
        
        try {
            const result = await api.takePhoto(this.currentIP);
            if (result.status === 'success') {
                this.showSuccess('Foto aufgenommen');
            }
        } catch (error) {
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
        const img = document.getElementById('liveStream');
        const placeholder = document.getElementById('streamPlaceholder');
        img.src = `http://localhost:8000/api/camera/stream/tele?ip=${this.currentIP}`;
        img.classList.add('active');
        placeholder.style.display = 'none';
        this.showSuccess('Stream gestartet');
    }

    stopStream() {
        const img = document.getElementById('liveStream');
        const placeholder = document.getElementById('streamPlaceholder');
        img.src = '';
        img.classList.remove('active');
        placeholder.style.display = 'block';
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

    async oneClickGoto() {
        if (!this.checkConnection()) return;
        const ra = parseFloat(document.getElementById('gotoRa').value);
        const dec = parseFloat(document.getElementById('gotoDec').value);
        const target = document.getElementById('gotoTarget').value;
        
        if (!ra || !dec || !target) {
            this.showError('Bitte alle Felder ausfüllen');
            return;
        }
        
        try {
            const result = await api.request('/astro/goto/one-click/dso?ip=' + this.currentIP, {
                method: 'POST',
                body: { ra, dec, target_name: target }
            });
            if (result.status === 'success') this.showSuccess('Ein-Klick GOTO gestartet');
        } catch (error) {
            this.showError('Fehler: ' + error.message);
        }
    }

    async stopOneClickGoto() {
        if (!this.checkConnection()) return;
        try {
            const result = await api.request('/astro/goto/one-click/stop?ip=' + this.currentIP, {
                method: 'POST'
            });
            if (result.status === 'success') this.showSuccess('Ein-Klick GOTO gestoppt');
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
            if (result.status === 'success') this.showSuccess('Motor gestoppt');
        } catch (error) {
            this.showError('Fehler: ' + error.message);
        }
    }

    setupJoystick() {
        const joystick = document.getElementById('joystick');
        const handle = document.getElementById('joystickHandle');
        let isDragging = false;

        joystick.addEventListener('mousedown', (e) => {
            isDragging = true;
            this.handleJoystickMove(e, joystick, handle);
        });

        document.addEventListener('mousemove', (e) => {
            if (isDragging) {
                this.handleJoystickMove(e, joystick, handle);
            }
        });

        document.addEventListener('mouseup', () => {
            if (isDragging) {
                isDragging = false;
                handle.style.transform = 'translate(-50%, -50%)';
                this.stopMotor();
            }
        });
    }

    handleJoystickMove(e, joystick, handle) {
        const rect = joystick.getBoundingClientRect();
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const x = e.clientX - rect.left - centerX;
        const y = e.clientY - rect.top - centerY;
        
        const distance = Math.sqrt(x * x + y * y);
        const maxDistance = rect.width / 2 - 30;
        
        if (distance > maxDistance) {
            const angle = Math.atan2(y, x);
            const limitedX = Math.cos(angle) * maxDistance;
            const limitedY = Math.sin(angle) * maxDistance;
            handle.style.transform = `translate(calc(-50% + ${limitedX}px), calc(-50% + ${limitedY}px))`;
        } else {
            handle.style.transform = `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`;
        }
        
        // Calculate angle for motor control
        const angle = (Math.atan2(y, x) * 180 / Math.PI + 360) % 360;
        const length = Math.min(distance / maxDistance, 1);
        
        // Send joystick command (throttled)
        if (this.joystickTimeout) clearTimeout(this.joystickTimeout);
        this.joystickTimeout = setTimeout(() => {
            if (this.currentIP && length > 0.1) {
                api.request('/motor/joystick/start?ip=' + this.currentIP, {
                    method: 'POST',
                    body: {
                        vector_angle: angle,
                        vector_length: length,
                        speed: 5.0
                    }
                }).catch(err => console.error(err));
            }
        }, 100);
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

    showSuccess(message) {
        console.log('✅', message);
        // TODO: Toast-Notification
    }

    showError(message) {
        console.error('❌', message);
        alert(message);
    }

    async loadMedia() {
        if (!this.checkConnection()) return;
        
        try {
            // Load counts
            const counts = await api.getMediaCounts(this.currentIP);
            if (counts.code === 0) {
                document.getElementById('photoCount').textContent = counts.data?.photo || 0;
                document.getElementById('videoCount').textContent = counts.data?.video || 0;
                document.getElementById('stackCount').textContent = counts.data?.stacking || 0;
            }
            
            // Load media list
            const result = await api.getMediaList(this.currentIP, this.currentMediaType);
            if (result.code === 0) {
                this.mediaList = result.data?.list || [];
                this.renderMediaGrid();
                this.showSuccess(`${this.mediaList.length} Medien geladen`);
            }
        } catch (error) {
            this.showError('Fehler beim Laden: ' + error.message);
        }
    }

    renderMediaGrid() {
        const grid = document.getElementById('mediaGrid');
        
        if (this.mediaList.length === 0) {
            grid.innerHTML = `
                <div class="media-placeholder">
                    <p>📁</p>
                    <p>Keine Medien gefunden</p>
                    <p class="info-text">Wähle einen anderen Filter</p>
                </div>
            `;
            return;
        }
        
        grid.innerHTML = this.mediaList.map(media => `
            <div class="media-item" data-path="${media.filePath}" data-name="${media.fileName}">
                <div class="media-thumbnail">
                    ${this.getMediaIcon(media.mediaType)}
                </div>
                <div class="media-info">
                    <div class="media-name" title="${media.fileName}">${media.fileName}</div>
                    <div class="media-meta">${this.formatFileSize(media.fileSize)}</div>
                </div>
                <div class="media-actions">
                    <button class="btn btn-download" onclick="app.downloadMedia('${media.filePath}', '${media.fileName}')">
                        ⬇️
                    </button>
                    <button class="btn btn-delete" onclick="app.deleteMediaItem(${media.mediaType}, '${media.filePath}', '${media.fileName}')">
                        🗑️
                    </button>
                </div>
            </div>
        `).join('');
    }

    getMediaIcon(mediaType) {
        const icons = {
            1: '📷', // Photo
            2: '🎥', // Video
            3: '🌌', // Stacking
            4: '📹', // Timelapse
        };
        return icons[mediaType] || '📁';
    }

    formatFileSize(bytes) {
        if (!bytes) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    }

    async downloadMedia(filePath, fileName) {
        if (!this.checkConnection()) return;
        this.showSuccess(`Download: ${fileName} (Funktion in Entwicklung)`);
        // TODO: Implement download via backend proxy
    }

    async deleteMediaItem(mediaType, filePath, fileName) {
        if (!this.checkConnection()) return;
        
        if (!confirm(`${fileName} wirklich löschen?`)) return;
        
        try {
            const result = await api.deleteMedia(this.currentIP, [{
                media_type: mediaType,
                file_path: filePath,
                file_name: fileName
            }]);
            
            if (result.code === 0) {
                this.showSuccess('Gelöscht');
                this.loadMedia();
            }
        } catch (error) {
            this.showError('Fehler: ' + error.message);
        }
    }
}

// Initialize app
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new App();
});
