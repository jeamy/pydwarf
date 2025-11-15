/**
 * API-Konstanten
 */

export const API_BASE_URL = 'http://localhost:8000/api';

export const ENDPOINTS = {
    // Device
    DEVICE_CONNECT: '/device/connect',
    DEVICE_INFO: '/device/info',
    DEVICE_LIST: '/device/list',
    DEVICE_FIRMWARE: '/device/firmware',
    
    // Camera
    CAMERA_TELE_OPEN: '/camera/tele/open',
    CAMERA_TELE_CLOSE: '/camera/tele/close',
    CAMERA_TELE_PHOTO: '/camera/tele/photo',
    CAMERA_TELE_VIDEO_START: '/camera/tele/video/start',
    CAMERA_TELE_VIDEO_STOP: '/camera/tele/video/stop',
    CAMERA_STREAM: '/camera/stream',
    
    // Album
    ALBUM_COUNTS: '/album/counts',
    ALBUM_LIST: '/album/list',
    ALBUM_DELETE: '/album/delete',
    
    // Astro
    ASTRO_CALIBRATION_START: '/astro/calibration/start',
    ASTRO_CALIBRATION_STOP: '/astro/calibration/stop',
    ASTRO_GOTO_DSO: '/astro/goto/dso',
    ASTRO_GOTO_SOLAR: '/astro/goto/solar',
    ASTRO_STACKING_START: '/astro/stacking/start',
    ASTRO_STACKING_STOP: '/astro/stacking/stop',
    
    // Focus
    FOCUS_AUTO: '/focus/auto',
    FOCUS_ASTRO_START: '/focus/astro/start',
    FOCUS_ASTRO_STOP: '/focus/astro/stop',
    FOCUS_MANUAL_STEP: '/focus/manual/step',
    
    // Motor
    MOTOR_RUN: '/motor/run',
    MOTOR_STOP: '/motor/stop',
    MOTOR_JOYSTICK_START: '/motor/joystick/start',
    MOTOR_JOYSTICK_STOP: '/motor/joystick/stop',
    
    // System
    SYSTEM_SHUTDOWN: '/system/shutdown',
    SYSTEM_REBOOT: '/system/reboot',
    SYSTEM_RGB_ON: '/system/rgb/on',
    SYSTEM_RGB_OFF: '/system/rgb/off',
};

export const STATUS = {
    DISCONNECTED: 'disconnected',
    CONNECTING: 'connecting',
    CONNECTED: 'connected',
    ERROR: 'error'
};
