/**
 * API-Client für DWARF II Backend
 */

import { API_BASE_URL, ENDPOINTS } from './constants.js';

class APIClient {
    constructor() {
        this.baseURL = API_BASE_URL;
        this.currentIP = null;
    }

    setIP(ip) {
        this.currentIP = ip;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        const config = {
            method: options.method || 'GET',
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        };

        if (options.body) {
            config.body = JSON.stringify(options.body);
        }

        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.detail || 'API-Fehler');
            }
            
            return data;
        } catch (error) {
            console.error('API-Request fehlgeschlagen:', error);
            throw error;
        }
    }

    // Device
    async connectDevice(ip, port = 8082) {
        return this.request(ENDPOINTS.DEVICE_CONNECT, {
            method: 'POST',
            body: { ip, port }
        });
    }

    async getDeviceInfo(ip) {
        return this.request(`${ENDPOINTS.DEVICE_INFO}?ip=${ip}`);
    }

    async getDeviceList() {
        return this.request(ENDPOINTS.DEVICE_LIST);
    }

    // Camera
    async openTeleCamera(ip, binning = false) {
        return this.request(`${ENDPOINTS.CAMERA_TELE_OPEN}?ip=${ip}`, {
            method: 'POST',
            body: { binning, rtsp_encode_type: 0 }
        });
    }

    async closeTeleCamera(ip) {
        return this.request(`${ENDPOINTS.CAMERA_TELE_CLOSE}?ip=${ip}`, {
            method: 'POST'
        });
    }

    async takePhoto(ip) {
        return this.request(`${ENDPOINTS.CAMERA_TELE_PHOTO}?ip=${ip}`, {
            method: 'POST'
        });
    }

    async startVideo(ip) {
        return this.request(`${ENDPOINTS.CAMERA_TELE_VIDEO_START}?ip=${ip}`, {
            method: 'POST'
        });
    }

    async stopVideo(ip) {
        return this.request(`${ENDPOINTS.CAMERA_TELE_VIDEO_STOP}?ip=${ip}`, {
            method: 'POST'
        });
    }

    // Astro
    async startCalibration(ip) {
        return this.request(`${ENDPOINTS.ASTRO_CALIBRATION_START}?ip=${ip}`, {
            method: 'POST'
        });
    }

    async stopCalibration(ip) {
        return this.request(`${ENDPOINTS.ASTRO_CALIBRATION_STOP}?ip=${ip}`, {
            method: 'POST'
        });
    }

    async startStacking(ip) {
        return this.request(`${ENDPOINTS.ASTRO_STACKING_START}?ip=${ip}`, {
            method: 'POST'
        });
    }

    async stopStacking(ip) {
        return this.request(`${ENDPOINTS.ASTRO_STACKING_STOP}?ip=${ip}`, {
            method: 'POST'
        });
    }

    // Focus
    async autoFocus(ip, mode = 0) {
        return this.request(`${ENDPOINTS.FOCUS_AUTO}?ip=${ip}`, {
            method: 'POST',
            body: { mode, center_x: 0, center_y: 0 }
        });
    }

    async startAstroFocus(ip, mode = 0) {
        return this.request(`${ENDPOINTS.FOCUS_ASTRO_START}?ip=${ip}`, {
            method: 'POST',
            body: { mode }
        });
    }

    // Motor
    async stopMotor(ip, motorId = 0) {
        return this.request(`${ENDPOINTS.MOTOR_STOP}?ip=${ip}`, {
            method: 'POST',
            body: { motor_id: motorId }
        });
    }

    // System
    async shutdown(ip) {
        return this.request(`${ENDPOINTS.SYSTEM_SHUTDOWN}?ip=${ip}`, {
            method: 'POST'
        });
    }

    async reboot(ip) {
        return this.request(`${ENDPOINTS.SYSTEM_REBOOT}?ip=${ip}`, {
            method: 'POST'
        });
    }
}

export default new APIClient();
