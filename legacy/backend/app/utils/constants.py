"""
DWARF II API Konstanten
Alle Module-IDs, Befehle und Fehlercodes
"""

# ============================================================================
# Error Codes
# ============================================================================
ERROR_CODES = {
    0: "Erfolg",
    27: "Kamera-Fehler (Gerät nicht bereit oder Befehl abgelehnt)",
    56: "Kamera-Fehler (möglicherweise bereits geöffnet oder Gerät beschäftigt)",
    57: "Kamera-Fehler (Gerät beschäftigt oder Befehl nicht möglich)",
    374: "Kamera bereits geöffnet oder beschäftigt",
    # Weitere Codes werden bei Bedarf hinzugefügt
}

# ============================================================================
# Module IDs
# ============================================================================
MODULE_NONE = 0
MODULE_CAMERA_TELE = 1
MODULE_CAMERA_WIDE = 2
MODULE_ASTRO = 3
MODULE_SYSTEM = 4
MODULE_RGB_POWER = 5
MODULE_MOTOR = 6
MODULE_TRACK = 7
MODULE_FOCUS = 8
MODULE_NOTIFY = 9
MODULE_PANORAMA = 10
MODULE_SHOOTING_SCHEDULE = 13

# ============================================================================
# Camera Commands (Teleobjektiv) - 10000-10499
# ============================================================================
CMD_CAMERA_TELE_OPEN_CAMERA = 10000
CMD_CAMERA_TELE_CLOSE_CAMERA = 10001
CMD_CAMERA_TELE_PHOTOGRAPH = 10002
CMD_CAMERA_TELE_BURST = 10003
CMD_CAMERA_TELE_STOP_BURST = 10004
CMD_CAMERA_TELE_START_RECORD = 10005
CMD_CAMERA_TELE_STOP_RECORD = 10006
CMD_CAMERA_TELE_SET_EXP_MODE = 10007
CMD_CAMERA_TELE_GET_EXP_MODE = 10008
CMD_CAMERA_TELE_SET_EXP = 10009
CMD_CAMERA_TELE_GET_EXP = 10010
CMD_CAMERA_TELE_SET_GAIN_MODE = 10011
CMD_CAMERA_TELE_GET_GAIN_MODE = 10012
CMD_CAMERA_TELE_SET_GAIN = 10013
CMD_CAMERA_TELE_GET_GAIN = 10014
CMD_CAMERA_TELE_SET_BRIGHTNESS = 10015
CMD_CAMERA_TELE_GET_BRIGHTNESS = 10016
CMD_CAMERA_TELE_SET_CONTRAST = 10017
CMD_CAMERA_TELE_GET_CONTRAST = 10018
CMD_CAMERA_TELE_SET_SATURATION = 10019
CMD_CAMERA_TELE_GET_SATURATION = 10020
CMD_CAMERA_TELE_SET_HUE = 10021
CMD_CAMERA_TELE_GET_HUE = 10022
CMD_CAMERA_TELE_SET_SHARPNESS = 10023
CMD_CAMERA_TELE_GET_SHARPNESS = 10024
CMD_CAMERA_TELE_SET_WB_MODE = 10025
CMD_CAMERA_TELE_GET_WB_MODE = 10026
CMD_CAMERA_TELE_SET_IRCUT = 10031
CMD_CAMERA_TELE_GET_IRCUT = 10032
CMD_CAMERA_TELE_START_TIMELAPSE_PHOTO = 10033
CMD_CAMERA_TELE_STOP_TIMELAPSE_PHOTO = 10034
CMD_CAMERA_TELE_SET_ALL_PARAMS = 10035
CMD_CAMERA_TELE_GET_ALL_PARAMS = 10036
CMD_CAMERA_TELE_GET_SYSTEM_WORKING_STATE = 10039

# ============================================================================
# Camera Commands (Weitwinkel) - 12000-12499
# ============================================================================
CMD_CAMERA_WIDE_OPEN_CAMERA = 12000
CMD_CAMERA_WIDE_CLOSE_CAMERA = 12001
CMD_CAMERA_WIDE_PHOTOGRAPH = 12022
CMD_CAMERA_WIDE_BURST = 12023
CMD_CAMERA_WIDE_STOP_BURST = 12024
CMD_CAMERA_WIDE_START_TIMELAPSE_PHOTO = 12025
CMD_CAMERA_WIDE_STOP_TIMELAPSE_PHOTO = 12026
CMD_CAMERA_WIDE_GET_ALL_PARAMS = 12027
CMD_CAMERA_WIDE_SET_ALL_PARAMS = 12028

# ============================================================================
# Astro Commands - 11000-11499
# ============================================================================
CMD_ASTRO_START_CALIBRATION = 11000
CMD_ASTRO_STOP_CALIBRATION = 11001
CMD_ASTRO_START_GOTO_DSO = 11002
CMD_ASTRO_START_GOTO_SOLAR_SYSTEM = 11003
CMD_ASTRO_STOP_GOTO = 11004
CMD_ASTRO_START_CAPTURE_RAW_LIVE_STACKING = 11005
CMD_ASTRO_STOP_CAPTURE_RAW_LIVE_STACKING = 11006
CMD_ASTRO_START_CAPTURE_RAW_DARK = 11007
CMD_ASTRO_STOP_CAPTURE_RAW_DARK = 11008
CMD_ASTRO_CHECK_GOT_DARK = 11009
CMD_ASTRO_GO_LIVE = 11010
CMD_ASTRO_START_TRACK_SPECIAL_TARGET = 11011
CMD_ASTRO_STOP_TRACK_SPECIAL_TARGET = 11012
CMD_ASTRO_START_ONE_CLICK_GOTO_DSO = 11013
CMD_ASTRO_START_ONE_CLICK_GOTO_SOLAR_SYSTEM = 11014
CMD_ASTRO_STOP_ONE_CLICK_GOTO = 11015
CMD_ASTRO_START_WIDE_CAPTURE_LIVE_STACKING = 11016
CMD_ASTRO_STOP_WIDE_CAPTURE_LIVE_STACKING = 11017
CMD_ASTRO_START_EQ_SOLVING = 11018
CMD_ASTRO_STOP_EQ_SOLVING = 11019
CMD_ASTRO_START_CAPTURE_RAW_DARK_WITH_PARAM = 11021
CMD_ASTRO_STOP_CAPTURE_RAW_DARK_WITH_PARAM = 11022
CMD_ASTRO_GET_DARK_FRAME_LIST = 11023
CMD_ASTRO_DEL_DARK_FRAME_LIST = 11024

# ============================================================================
# System Commands - 13000-13299
# ============================================================================
CMD_SYSTEM_SET_TIME = 13000
CMD_SYSTEM_SET_TIME_ZONE = 13001
CMD_SYSTEM_SET_MTP_MODE = 13002
CMD_SYSTEM_SET_CPU_MODE = 13003

# ============================================================================
# RGB & Power Commands - 13500-13799
# ============================================================================
CMD_RGB_POWER_OPEN_RGB = 13500
CMD_RGB_POWER_CLOSE_RGB = 13501
CMD_RGB_POWER_POWER_DOWN = 13502
CMD_RGB_POWER_POWERIND_ON = 13503
CMD_RGB_POWER_POWERIND_OFF = 13504
CMD_RGB_POWER_REBOOT = 13505

# ============================================================================
# Motor Commands - 14000-14499
# ============================================================================
CMD_STEP_MOTOR_RUN = 14000
CMD_STEP_MOTOR_STOP = 14002
CMD_STEP_MOTOR_SERVICE_JOYSTICK = 14006
CMD_STEP_MOTOR_SERVICE_JOYSTICK_FIXED_ANGLE = 14007
CMD_STEP_MOTOR_SERVICE_JOYSTICK_STOP = 14008
CMD_STEP_MOTOR_SERVICE_DUAL_CAMERA_LINKAGE = 14009

# ============================================================================
# Tracking Commands - 14800-14899
# ============================================================================
CMD_TRACK_START_TRACK = 14800
CMD_TRACK_STOP_TRACK = 14801
CMD_SENTRY_MODE_START = 14802
CMD_SENTRY_MODE_STOP = 14803
CMD_MOT_START = 14804
CMD_MOT_TRACK_ONE = 14805

# ============================================================================
# Focus Commands - 15000-15099
# ============================================================================
CMD_FOCUS_AUTO_FOCUS = 15000
CMD_FOCUS_MANUAL_SINGLE_STEP_FOCUS = 15001
CMD_FOCUS_START_MANUAL_CONTINU_FOCUS = 15002
CMD_FOCUS_STOP_MANUAL_CONTINU_FOCUS = 15003
CMD_FOCUS_START_ASTRO_AUTO_FOCUS = 15004
CMD_FOCUS_STOP_ASTRO_AUTO_FOCUS = 15005

# ============================================================================
# Panorama Commands - 15500-15599
# ============================================================================
CMD_PANORAMA_START_GRID = 15500
CMD_PANORAMA_STOP = 15501

# ============================================================================
# Fehlercodes - HTTP
# ============================================================================
HTTP_OK = 0
HTTP_FILE_NOT_EXIST = -1
HTTP_INVAID_PARAM = -2
HTTP_CHECK_MD5_ERROR = -3

# ============================================================================
# Fehlercodes - WebSocket
# ============================================================================
WS_OK = 0
WS_PARSE_PROTOBUF_ERROR = -1
WS_SDCARD_NOT_EXIST = -2
WS_INVAID_PARAM = -3
WS_SDCARD_WRITE_ERROR = -4
WS_DEVICE_NOT_ACTIVATED = -5
WS_SDCARD_FULL_ERROR = -6

# ============================================================================
# Fehlercodes - Kamera
# ============================================================================
CODE_CAMERA_TELE_CLOSED = 10501
CODE_CAMERA_TELE_ISP_ERROR = 10502
CODE_CAMERA_TELE_OPEN_FAILED = 10504
CODE_CAMERA_TELE_WORKING_BUSY = 10507

# ============================================================================
# Fehlercodes - Astronomie
# ============================================================================
CODE_ASTRO_PLATE_SOLVING_FAILED = 11500
CODE_ASTRO_FUNCTION_BUSY = 11501
CODE_ASTRO_DARK_GAIN_OUT_OF_RANGE = 11502
CODE_ASTRO_DARK_NOT_FOUND = 11503
CODE_ASTRO_CALIBRATION_FAILED = 11504
CODE_ASTRO_GOTO_FAILED = 11505
CODE_ASTRO_NEED_GOTO = 11513
CODE_ASTRO_NEED_ADJUST_SHOOT_PARAM = 11514
CODE_ASTRO_EQ_SOLVING_FAILED = 11516
CODE_ASTRO_SKY_SEARCH_FAILED = 11517

# ============================================================================
# Fehlercodes - Fokus
# ============================================================================
CODE_FOCUS_ASTRO_AUTO_FOCUS_SLOW_ERROR = 15100
CODE_FOCUS_ASTRO_AUTO_FOCUS_FAST_ERROR = 15101

# ============================================================================
# Fehlercodes - Motor
# ============================================================================
CODE_STEP_MOTOR_LIMIT_POSITION_WARNING = 14518
CODE_STEP_MOTOR_LIMIT_POSITION_HITTED = 14519

# ============================================================================
# Sonnensystem-Ziele
# ============================================================================
SOLAR_MERCURY = 1
SOLAR_VENUS = 2
SOLAR_MARS = 3
SOLAR_JUPITER = 4
SOLAR_SATURN = 5
SOLAR_URANUS = 6
SOLAR_NEPTUNE = 7
SOLAR_MOON = 8
SOLAR_SUN = 9

# ============================================================================
# Spezial-Tracking-Ziele
# ============================================================================
SPECIAL_TARGET_SUN = 0
SPECIAL_TARGET_MOON = 1

# ============================================================================
# Medien-Typen
# ============================================================================
MEDIA_TYPE_ALL = 0
MEDIA_TYPE_PHOTO = 1
MEDIA_TYPE_VIDEO = 2
MEDIA_TYPE_BURST = 3
MEDIA_TYPE_ASTRO = 4
MEDIA_TYPE_PANORAMA = 5

# ============================================================================
# Ein-Klick GOTO Schritte
# ============================================================================
ONE_CLICK_GOTO_STEP_SKY_DETECTION = 10
ONE_CLICK_GOTO_STEP_FOCUS = 20
ONE_CLICK_GOTO_STEP_CALIBRATION = 30
ONE_CLICK_GOTO_STEP_GOTO = 40
