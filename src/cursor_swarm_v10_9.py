import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import sys
from pathlib import Path
import random
import math
import time
import ctypes
import atexit
from ctypes import wintypes
from PIL import Image, ImageTk

# -----------------------------
# V10 SETTINGS
# -----------------------------
APP_VERSION = "v10.9"
CURRENT_PRESET_NAME = "Legacy v8.1"
MAX_CUSTOM_PRESETS = 10
def get_app_dir():
    """Return the folder where app-side config files should live.

    Normal Python mode:
        Use the script folder.

    Normal PyInstaller EXE mode:
        Use the folder containing CursorSwarm.exe so the portable EXE
        keeps its files beside the app.

    MSIX / WindowsApps mode:
        The package install folder is read-only, so use a writable
        LocalAppData folder instead. This prevents PermissionError when
        CursorSwarm creates cursor_presets.json, cursor_settings.json,
        restore_cursor_emergency.py, restore_cursor_emergency.exe, and README.txt.
    """
    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.executable).resolve().parent
        exe_dir_text = str(exe_dir).lower()

        if "windowsapps" in exe_dir_text or "\\vfs\\" in exe_dir_text:
            local_app_data = os.environ.get("LOCALAPPDATA")
            if local_app_data:
                return Path(local_app_data) / "CursorSwarm"
            return Path.home() / "AppData" / "Local" / "CursorSwarm"

        return exe_dir

    return Path(__file__).resolve().parent


APP_DIR = get_app_dir()
APP_DIR.mkdir(parents=True, exist_ok=True)
PRESET_FILE = APP_DIR / "cursor_presets.json"
SETTINGS_FILE = APP_DIR / "cursor_settings.json"
RESTORE_SCRIPT_FILE = APP_DIR / "restore_cursor_emergency.py"
RESTORE_EXE_FILE = APP_DIR / "restore_cursor_emergency.exe"
README_FILE = APP_DIR / "README.txt"
PRIVACY_POLICY_FILE = APP_DIR / "CursorSwarm_PrivacyPolicy.txt"
TERMS_SAFETY_FILE = APP_DIR / "CursorSwarm_TermsAndSafety.txt"
RELEASE_NOTES_FILE = APP_DIR / "CursorSwarm_ReleaseNotes.txt"

STATIC_COUNT = 70

SLOW_CLONE_COUNT = 35
SAME_SPEED_CLONE_COUNT = 40
FAST_CLONE_COUNT = 35
RANDOM_MOVER_COUNT = 28
TARGET_MOVER_COUNT = 14

MOVE_DISTANCE_THRESHOLD = 0.6
FAKE_CURSOR_WOBBLE = 1.0

CURSOR_SCALE_PRESETS = [0.60, 0.70, 0.82, 0.92, 1.00, 1.00, 1.00]
REAL_DRAWN_CURSOR_SCALE = 1.00

RANDOMIZE_DRAW_ORDER = True
AUTO_RESTORE_SECONDS = None

TRANSPARENT_COLOR = "#ff00ff"

# Mirror settings
MIRROR_ENABLED = False
MIRROR_X = True
MIRROR_Y = True
MIRROR_STRENGTH = 1.0

# Nightmare cursor behavior modes
NIGHTMARE_MODE_OPTIONS = [
    "Disabled",
    "Blind Mode",
    "Fake-only Mode",
    "Flicker Hint Mode",
]
NIGHTMARE_FLICKER_INTERVAL = 3.0
NIGHTMARE_FLICKER_DURATION = 0.18

# -----------------------------
# Built-in preset defaults
# -----------------------------
BUILT_IN_PRESETS = {
    "Chill": {
        "display_name": "Chill",
        "danger_level": "Safe",
        "static_count": 18,
        "slow_clone_count": 10,
        "same_speed_clone_count": 12,
        "fast_clone_count": 6,
        "random_mover_count": 5,
        "target_mover_count": 3,
        "show_fake_cursors": True,
        "show_drawn_real_cursor": True,
        "transparent_cursor": False,
        "mirror_enabled": False,
        "mirror_x": True,
        "mirror_y": True,
        "mirror_strength": 1.0,
        "swarm_paused": False,
        "randomize_draw_order": True,
        "nightmare_mode": "Disabled",
    },
    "Cursed": {
        "display_name": "Cursed",
        "danger_level": "Cursed",
        "static_count": 40,
        "slow_clone_count": 20,
        "same_speed_clone_count": 24,
        "fast_clone_count": 18,
        "random_mover_count": 12,
        "target_mover_count": 8,
        "show_fake_cursors": True,
        "show_drawn_real_cursor": True,
        "transparent_cursor": True,
        "mirror_enabled": False,
        "mirror_x": True,
        "mirror_y": True,
        "mirror_strength": 1.0,
        "swarm_paused": False,
        "randomize_draw_order": True,
        "nightmare_mode": "Disabled",
    },
    "Legendary": {
        "display_name": "Legendary",
        "danger_level": "Extreme",
        "static_count": 70,
        "slow_clone_count": 35,
        "same_speed_clone_count": 40,
        "fast_clone_count": 35,
        "random_mover_count": 28,
        "target_mover_count": 14,
        "show_fake_cursors": True,
        "show_drawn_real_cursor": True,
        "transparent_cursor": True,
        "mirror_enabled": False,
        "mirror_x": True,
        "mirror_y": True,
        "mirror_strength": 1.0,
        "swarm_paused": False,
        "randomize_draw_order": True,
        "nightmare_mode": "Disabled",
    },
    "Nightmare": {
        "display_name": "Nightmare",
        "danger_level": "Dangerous",
        "static_count": 95,
        "slow_clone_count": 45,
        "same_speed_clone_count": 55,
        "fast_clone_count": 50,
        "random_mover_count": 38,
        "target_mover_count": 22,
        "show_fake_cursors": True,
        "show_drawn_real_cursor": False,
        "transparent_cursor": True,
        "mirror_enabled": False,
        "mirror_x": True,
        "mirror_y": True,
        "mirror_strength": 1.0,
        "swarm_paused": False,
        "randomize_draw_order": True,
        "nightmare_mode": "Fake-only Mode",
    },
}

# -----------------------------
# Screen density presets for the Swarm tab
# -----------------------------
SCREEN_DENSITY_PRESETS = {
    "Low": {
        "static_count": 18,
        "slow_clone_count": 10,
        "same_speed_clone_count": 12,
        "fast_clone_count": 6,
        "random_mover_count": 5,
        "target_mover_count": 3,
    },
    "Medium": {
        "static_count": 40,
        "slow_clone_count": 20,
        "same_speed_clone_count": 24,
        "fast_clone_count": 18,
        "random_mover_count": 12,
        "target_mover_count": 8,
    },
    "High": {
        "static_count": 70,
        "slow_clone_count": 35,
        "same_speed_clone_count": 40,
        "fast_clone_count": 35,
        "random_mover_count": 28,
        "target_mover_count": 14,
    },
    "Nightmare": {
        "static_count": 95,
        "slow_clone_count": 45,
        "same_speed_clone_count": 55,
        "fast_clone_count": 50,
        "random_mover_count": 38,
        "target_mover_count": 22,
    },
}

# -----------------------------
# Startup / app settings
# -----------------------------
STARTUP_MODE_OPTIONS = [
    "Safe Mode",
    "Last Used State",
    "Built-in Preset",
    "Custom Preset",
]

DEFAULT_APP_SETTINGS = {
    "startup_mode": "Safe Mode",
    "startup_builtin_preset": "Legendary",
    "startup_custom_slot": "1",
    "show_startup_help": True,
    "runtime_hud_visible": False,
    "last_state": None,
}


def load_app_settings_file():
    settings = dict(DEFAULT_APP_SETTINGS)

    if not SETTINGS_FILE.exists():
        return settings

    try:
        data = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return settings

    if isinstance(data, dict):
        settings.update(data)

    if settings.get("startup_mode") not in STARTUP_MODE_OPTIONS:
        settings["startup_mode"] = "Safe Mode"

    settings["startup_builtin_preset"] = str(settings.get("startup_builtin_preset", "Legendary"))
    settings["startup_custom_slot"] = str(settings.get("startup_custom_slot", "1"))

    return settings


app_settings = load_app_settings_file()


# Hotkeys
VK_CTRL = 0x11
VK_ALT = 0x12
VK_SHIFT = 0x10

VK_Q = 0x51
VK_R = 0x52
VK_M = 0x4D
VK_X = 0x58
VK_Y = 0x59
VK_P = 0x50
VK_H = 0x48
VK_C = 0x43
VK_SPACE = 0x20
VK_D = 0x44

VK_LEFT = 0x25
VK_UP = 0x26
VK_RIGHT = 0x27
VK_DOWN = 0x28

# -----------------------------
# Windows setup
# -----------------------------
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
kernel32 = ctypes.windll.kernel32

SCREEN_W = user32.GetSystemMetrics(0)
SCREEN_H = user32.GetSystemMetrics(1)

CURSOR_W = user32.GetSystemMetrics(13)
CURSOR_H = user32.GetSystemMetrics(14)

if CURSOR_W <= 0:
    CURSOR_W = 32
if CURSOR_H <= 0:
    CURSOR_H = 32

PTR_SIZE = ctypes.sizeof(ctypes.c_void_p)
LONG_PTR = ctypes.c_longlong if PTR_SIZE == 8 else ctypes.c_long
LRESULT = LONG_PTR

# -----------------------------
# Raw input constants
# -----------------------------
WM_INPUT = 0x00FF
RID_INPUT = 0x10000003
RIM_TYPEMOUSE = 0
RIDEV_INPUTSINK = 0x00000100
MOUSE_MOVE_ABSOLUTE = 0x0001

SM_XVIRTUALSCREEN = 76
SM_YVIRTUALSCREEN = 77
SM_CXVIRTUALSCREEN = 78
SM_CYVIRTUALSCREEN = 79

# -----------------------------
# Cursor constants
# -----------------------------
DIB_RGB_COLORS = 0
BI_RGB = 0
DI_NORMAL = 0x0003
CURSOR_SHOWING = 0x00000001

IMAGE_CURSOR = 2
LR_COPYFROMRESOURCE = 0x4000
OCR_NORMAL = 32512

SYSTEM_CURSOR_IDS = [
    32512, 32513, 32514, 32515, 32516,
    32640, 32641, 32642, 32643, 32644,
    32645, 32646, 32648, 32649, 32650,
    32651, 32671, 32672,
]

# -----------------------------
# Structures
# -----------------------------
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class CURSORINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("hCursor", wintypes.HANDLE),
        ("ptScreenPos", POINT),
    ]


class ICONINFO(ctypes.Structure):
    _fields_ = [
        ("fIcon", wintypes.BOOL),
        ("xHotspot", wintypes.DWORD),
        ("yHotspot", wintypes.DWORD),
        ("hbmMask", wintypes.HANDLE),
        ("hbmColor", wintypes.HANDLE),
    ]


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", wintypes.DWORD),
        ("biWidth", wintypes.LONG),
        ("biHeight", wintypes.LONG),
        ("biPlanes", wintypes.WORD),
        ("biBitCount", wintypes.WORD),
        ("biCompression", wintypes.DWORD),
        ("biSizeImage", wintypes.DWORD),
        ("biXPelsPerMeter", wintypes.LONG),
        ("biYPelsPerMeter", wintypes.LONG),
        ("biClrUsed", wintypes.DWORD),
        ("biClrImportant", wintypes.DWORD),
    ]


class BITMAPINFO(ctypes.Structure):
    _fields_ = [
        ("bmiHeader", BITMAPINFOHEADER),
        ("bmiColors", wintypes.DWORD * 3),
    ]


class RAWINPUTDEVICE(ctypes.Structure):
    _fields_ = [
        ("usUsagePage", wintypes.USHORT),
        ("usUsage", wintypes.USHORT),
        ("dwFlags", wintypes.DWORD),
        ("hwndTarget", wintypes.HWND),
    ]


class RAWINPUTHEADER(ctypes.Structure):
    _fields_ = [
        ("dwType", wintypes.DWORD),
        ("dwSize", wintypes.DWORD),
        ("hDevice", wintypes.HANDLE),
        ("wParam", wintypes.WPARAM),
    ]


class RAWMOUSE_BUTTONS_STRUCT(ctypes.Structure):
    _fields_ = [
        ("usButtonFlags", wintypes.USHORT),
        ("usButtonData", wintypes.USHORT),
    ]


class RAWMOUSE_BUTTONS_UNION(ctypes.Union):
    _fields_ = [
        ("ulButtons", wintypes.ULONG),
        ("buttons", RAWMOUSE_BUTTONS_STRUCT),
    ]


class RAWMOUSE(ctypes.Structure):
    _fields_ = [
        ("usFlags", wintypes.USHORT),
        ("buttonUnion", RAWMOUSE_BUTTONS_UNION),
        ("ulRawButtons", wintypes.ULONG),
        ("lLastX", wintypes.LONG),
        ("lLastY", wintypes.LONG),
        ("ulExtraInformation", wintypes.ULONG),
    ]


class RAWINPUT_DATA(ctypes.Union):
    _fields_ = [("mouse", RAWMOUSE)]


class RAWINPUT(ctypes.Structure):
    _fields_ = [
        ("header", RAWINPUTHEADER),
        ("data", RAWINPUT_DATA),
    ]


# -----------------------------
# API signatures
# -----------------------------
user32.GetCursorInfo.argtypes = [ctypes.POINTER(CURSORINFO)]
user32.GetCursorInfo.restype = wintypes.BOOL

user32.GetIconInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(ICONINFO)]
user32.GetIconInfo.restype = wintypes.BOOL

user32.CopyIcon.argtypes = [wintypes.HANDLE]
user32.CopyIcon.restype = wintypes.HANDLE

user32.DestroyIcon.argtypes = [wintypes.HANDLE]
user32.DestroyIcon.restype = wintypes.BOOL

user32.CreateCursor.argtypes = [
    wintypes.HINSTANCE,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_void_p,
    ctypes.c_void_p,
]
user32.CreateCursor.restype = wintypes.HANDLE

user32.SetSystemCursor.argtypes = [wintypes.HANDLE, wintypes.DWORD]
user32.SetSystemCursor.restype = wintypes.BOOL

user32.DestroyCursor.argtypes = [wintypes.HANDLE]
user32.DestroyCursor.restype = wintypes.BOOL

user32.CopyImage.argtypes = [
    wintypes.HANDLE,
    wintypes.UINT,
    ctypes.c_int,
    ctypes.c_int,
    wintypes.UINT,
]
user32.CopyImage.restype = wintypes.HANDLE

user32.LoadCursorW.restype = wintypes.HANDLE

user32.GetAsyncKeyState.argtypes = [ctypes.c_int]
user32.GetAsyncKeyState.restype = wintypes.SHORT

user32.GetCursorPos.argtypes = [ctypes.POINTER(POINT)]
user32.GetCursorPos.restype = wintypes.BOOL

user32.SetCursorPos.argtypes = [ctypes.c_int, ctypes.c_int]
user32.SetCursorPos.restype = wintypes.BOOL

user32.GetSystemMetrics.argtypes = [ctypes.c_int]
user32.GetSystemMetrics.restype = ctypes.c_int

user32.RegisterRawInputDevices.argtypes = [
    ctypes.POINTER(RAWINPUTDEVICE),
    wintypes.UINT,
    wintypes.UINT,
]
user32.RegisterRawInputDevices.restype = wintypes.BOOL

user32.GetRawInputData.argtypes = [
    wintypes.HANDLE,
    wintypes.UINT,
    wintypes.LPVOID,
    ctypes.POINTER(wintypes.UINT),
    wintypes.UINT,
]
user32.GetRawInputData.restype = wintypes.UINT

user32.CallWindowProcW.argtypes = [
    LONG_PTR,
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM,
]
user32.CallWindowProcW.restype = LRESULT

gdi32.DeleteObject.argtypes = [wintypes.HANDLE]
gdi32.DeleteObject.restype = wintypes.BOOL

gdi32.DeleteDC.argtypes = [wintypes.HANDLE]
gdi32.DeleteDC.restype = wintypes.BOOL

GWLP_WNDPROC = -4

if PTR_SIZE == 8:
    SetWindowLongPtr = user32.SetWindowLongPtrW
    SetWindowLongPtr.argtypes = [wintypes.HWND, ctypes.c_int, LONG_PTR]
    SetWindowLongPtr.restype = LONG_PTR
else:
    SetWindowLongPtr = user32.SetWindowLongW
    SetWindowLongPtr.argtypes = [wintypes.HWND, ctypes.c_int, LONG_PTR]
    SetWindowLongPtr.restype = LONG_PTR

WNDPROC = ctypes.WINFUNCTYPE(
    LRESULT,
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM,
)

# -----------------------------
# Helpers
# -----------------------------
def key_down(vk):
    return bool(user32.GetAsyncKeyState(vk) & 0x8000)


def ctrl_alt_down():
    return key_down(VK_CTRL) and key_down(VK_ALT)


hotkey_latches = {}


def hotkey_pressed(name, condition):
    """Return True only once when a hotkey combo first becomes pressed.

    This avoids timer-based double toggles and makes Safe Mode / Resume reliable
    even when the keys are held for a moment.
    """
    condition = bool(condition)
    was_pressed = hotkey_latches.get(name, False)
    hotkey_latches[name] = condition
    return condition and not was_pressed


def get_mouse_position():
    point = POINT()
    user32.GetCursorPos(ctypes.byref(point))
    return point.x, point.y


screen_left = user32.GetSystemMetrics(SM_XVIRTUALSCREEN)
screen_top = user32.GetSystemMetrics(SM_YVIRTUALSCREEN)
screen_w = user32.GetSystemMetrics(SM_CXVIRTUALSCREEN)
screen_h = user32.GetSystemMetrics(SM_CYVIRTUALSCREEN)

if screen_w <= 0:
    screen_left = 0
    screen_w = SCREEN_W

if screen_h <= 0:
    screen_top = 0
    screen_h = SCREEN_H

screen_right = screen_left + screen_w - 1
screen_bottom = screen_top + screen_h - 1


def set_mouse_position(x, y):
    x = max(screen_left, min(screen_right, int(round(x))))
    y = max(screen_top, min(screen_bottom, int(round(y))))
    user32.SetCursorPos(x, y)
    return x, y


# -----------------------------
# System cursor backup / transparent / restore
# -----------------------------
def make_cursor_copy(hcursor):
    if not hcursor:
        return None

    copied = user32.CopyImage(
        hcursor,
        IMAGE_CURSOR,
        0,
        0,
        LR_COPYFROMRESOURCE
    )

    if copied:
        return copied

    copied = user32.CopyIcon(hcursor)

    if copied:
        return copied

    return None


def backup_system_cursors():
    backups = {}

    for cursor_id in SYSTEM_CURSOR_IDS:
        hcursor = user32.LoadCursorW(None, cursor_id)

        if not hcursor:
            continue

        copied = make_cursor_copy(hcursor)

        if copied:
            backups[cursor_id] = copied

    return backups


def create_transparent_cursor():
    width = 32
    height = 32
    plane_bytes = width * height // 8

    and_plane = (ctypes.c_ubyte * plane_bytes)(*([0xFF] * plane_bytes))
    xor_plane = (ctypes.c_ubyte * plane_bytes)(*([0x00] * plane_bytes))

    return user32.CreateCursor(
        None,
        0,
        0,
        width,
        height,
        ctypes.cast(and_plane, ctypes.c_void_p),
        ctypes.cast(xor_plane, ctypes.c_void_p),
    )


def apply_transparent_cursors():
    success = 0

    for cursor_id in SYSTEM_CURSOR_IDS:
        htransparent = create_transparent_cursor()

        if not htransparent:
            continue

        result = user32.SetSystemCursor(htransparent, cursor_id)

        if result:
            success += 1
        else:
            user32.DestroyCursor(htransparent)

    return success


def restore_from_backup(backups):
    success = 0

    for cursor_id, backup_handle in backups.items():
        hrestore = make_cursor_copy(backup_handle)

        if not hrestore:
            continue

        result = user32.SetSystemCursor(hrestore, cursor_id)

        if result:
            success += 1
        else:
            user32.DestroyCursor(hrestore)

    return success


print("Backing up system cursors...")
cursor_backups = backup_system_cursors()

if len(cursor_backups) == 0:
    raise RuntimeError("Could not backup system cursors. Aborting for safety.")

transparent_active = False


def restore_cursors_safely():
    global transparent_active

    if cursor_backups:
        restore_from_backup(cursor_backups)

    transparent_active = False


atexit.register(restore_cursors_safely)


def set_transparent_mode():
    global transparent_active, transparent_started_at

    if not transparent_active:
        apply_transparent_cursors()
        transparent_active = True
        transparent_started_at = time.time()


def set_visible_mode():
    global transparent_active, transparent_started_at

    if transparent_active:
        restore_from_backup(cursor_backups)
        transparent_active = False
        transparent_started_at = None


# -----------------------------
# Capture cursor image / hotspot
# -----------------------------
def get_capture_cursor_handle():
    hcursor = user32.LoadCursorW(None, OCR_NORMAL)

    if hcursor:
        return hcursor

    info = CURSORINFO()
    info.cbSize = ctypes.sizeof(CURSORINFO)

    if user32.GetCursorInfo(ctypes.byref(info)) and (info.flags & CURSOR_SHOWING):
        return info.hCursor

    return None


def get_cursor_hotspot(hcursor):
    icon_info = ICONINFO()

    if not user32.GetIconInfo(hcursor, ctypes.byref(icon_info)):
        return 0, 0

    hotspot_x = int(icon_info.xHotspot)
    hotspot_y = int(icon_info.yHotspot)

    if icon_info.hbmMask:
        gdi32.DeleteObject(wintypes.HANDLE(icon_info.hbmMask))

    if icon_info.hbmColor:
        gdi32.DeleteObject(wintypes.HANDLE(icon_info.hbmColor))

    return hotspot_x, hotspot_y


def draw_cursor_to_image(hcursor, bg=(0, 0, 0, 0)):
    width = CURSOR_W
    height = CURSOR_H

    screen_dc = user32.GetDC(None)
    mem_dc = gdi32.CreateCompatibleDC(screen_dc)

    bmi = BITMAPINFO()
    bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.bmiHeader.biWidth = width
    bmi.bmiHeader.biHeight = -height
    bmi.bmiHeader.biPlanes = 1
    bmi.bmiHeader.biBitCount = 32
    bmi.bmiHeader.biCompression = BI_RGB

    bits = ctypes.c_void_p()

    hbitmap = gdi32.CreateDIBSection(
        screen_dc,
        ctypes.byref(bmi),
        DIB_RGB_COLORS,
        ctypes.byref(bits),
        None,
        0
    )

    old_bitmap = gdi32.SelectObject(mem_dc, hbitmap)

    buffer_size = width * height * 4
    buffer = (ctypes.c_ubyte * buffer_size).from_address(bits.value)

    r, g, b, a = bg

    for i in range(0, buffer_size, 4):
        buffer[i] = b
        buffer[i + 1] = g
        buffer[i + 2] = r
        buffer[i + 3] = a

    copied_icon = user32.CopyIcon(hcursor)

    user32.DrawIconEx(
        mem_dc,
        0,
        0,
        copied_icon,
        width,
        height,
        0,
        None,
        DI_NORMAL
    )

    raw = bytes(buffer)

    gdi32.SelectObject(mem_dc, old_bitmap)
    gdi32.DeleteObject(hbitmap)
    gdi32.DeleteDC(mem_dc)
    user32.ReleaseDC(None, screen_dc)

    if copied_icon:
        user32.DestroyIcon(copied_icon)

    return Image.frombuffer(
        "RGBA",
        (width, height),
        raw,
        "raw",
        "BGRA",
        0,
        1
    )


def extract_cursor_image_and_hotspot():
    hcursor = get_capture_cursor_handle()

    if not hcursor:
        return None, 0, 0

    hotspot_x, hotspot_y = get_cursor_hotspot(hcursor)

    img = draw_cursor_to_image(hcursor, bg=(0, 0, 0, 0))
    alpha = img.getchannel("A")

    if alpha.getbbox() is not None:
        bbox = img.getbbox()

        if bbox:
            cropped = img.crop(bbox)
            return cropped, hotspot_x - bbox[0], hotspot_y - bbox[1]

        return img, hotspot_x, hotspot_y

    black = draw_cursor_to_image(hcursor, bg=(0, 0, 0, 255)).convert("RGBA")
    white = draw_cursor_to_image(hcursor, bg=(255, 255, 255, 255)).convert("RGBA")

    black_pixels = black.load()
    white_pixels = white.load()

    result = Image.new("RGBA", black.size)
    result_pixels = result.load()

    for y in range(black.height):
        for x in range(black.width):
            br, bg, bb, _ = black_pixels[x, y]
            wr, wg, wb, _ = white_pixels[x, y]

            diff = max(abs(wr - br), abs(wg - bg), abs(wb - bb))
            alpha_value = max(0, min(255, 255 - diff))

            if alpha_value == 0:
                result_pixels[x, y] = (0, 0, 0, 0)
            else:
                result_pixels[x, y] = (br, bg, bb, alpha_value)

    bbox = result.getbbox()

    if bbox:
        result = result.crop(bbox)
        hotspot_x -= bbox[0]
        hotspot_y -= bbox[1]

    return result, hotspot_x, hotspot_y


def remove_alpha_glow(img, threshold=120):
    img = img.convert("RGBA")
    pixels = img.load()

    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]

            if a < threshold:
                pixels[x, y] = (0, 0, 0, 0)
            else:
                pixels[x, y] = (r, g, b, 255)

    return img


# -----------------------------
# Fake cursor object
# -----------------------------
class FakeCursor:
    def __init__(self, mode):
        self.mode = mode
        self.x = random.randint(0, SCREEN_W)
        self.y = random.randint(0, SCREEN_H)

        self.scale = random.choice(CURSOR_SCALE_PRESETS)

        self.vx = random.uniform(-500, 500)
        self.vy = random.uniform(-500, 500)

        self.target_x = random.randint(0, SCREEN_W)
        self.target_y = random.randint(0, SCREEN_H)

        self.angle_offset = random.uniform(-0.18, 0.18)
        self.noise_amount = random.uniform(0.02, 0.14)

        if mode == "slow":
            self.factor = random.uniform(0.35, 0.75)
        elif mode == "same":
            self.factor = random.uniform(0.85, 1.15)
        elif mode == "fast":
            self.factor = random.uniform(1.35, 2.35)
        else:
            self.factor = random.uniform(0.7, 1.6)

    def choose_target(self):
        self.target_x = random.randint(20, SCREEN_W - 40)
        self.target_y = random.randint(20, SCREEN_H - 40)

    def wrap_screen(self):
        margin = 70

        if self.x < -margin:
            self.x = SCREEN_W + margin
        elif self.x > SCREEN_W + margin:
            self.x = -margin

        if self.y < -margin:
            self.y = SCREEN_H + margin
        elif self.y > SCREEN_H + margin:
            self.y = -margin

    def update(self, moving, real_dx, real_dy, dt):
        if self.mode == "static":
            return

        if not moving:
            return

        if self.mode in ("slow", "same", "fast"):
            real_distance = math.hypot(real_dx, real_dy)

            if real_distance > 0:
                angle = math.atan2(real_dy, real_dx)
                angle += self.angle_offset
                angle += random.uniform(-self.noise_amount, self.noise_amount) * FAKE_CURSOR_WOBBLE

                step = real_distance * self.factor

                self.x += math.cos(angle) * step
                self.y += math.sin(angle) * step

                self.x += random.uniform(-1.0, 1.0) * FAKE_CURSOR_WOBBLE
                self.y += random.uniform(-1.0, 1.0) * FAKE_CURSOR_WOBBLE

                if random.random() < 0.015:
                    self.angle_offset = random.uniform(-0.25, 0.25)

        elif self.mode == "random":
            self.vx += random.uniform(-900, 900) * dt * FAKE_CURSOR_WOBBLE
            self.vy += random.uniform(-900, 900) * dt * FAKE_CURSOR_WOBBLE

            speed = math.hypot(self.vx, self.vy)
            max_speed = 900

            if speed > max_speed:
                self.vx = self.vx / speed * max_speed
                self.vy = self.vy / speed * max_speed

            self.x += self.vx * dt
            self.y += self.vy * dt

        elif self.mode == "target":
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.hypot(dx, dy)

            if distance < 18:
                self.choose_target()
            else:
                speed = 650
                self.x += (dx / distance) * speed * dt
                self.y += (dy / distance) * speed * dt

                self.x += random.uniform(-1.5, 1.5) * FAKE_CURSOR_WOBBLE
                self.y += random.uniform(-1.5, 1.5) * FAKE_CURSOR_WOBBLE

        self.wrap_screen()


# -----------------------------
# Tkinter overlay
# -----------------------------
root = tk.Tk()
root.overrideredirect(True)
root.geometry(f"{SCREEN_W}x{SCREEN_H}+0+0")
root.attributes("-topmost", True)
root.wm_attributes("-transparentcolor", TRANSPARENT_COLOR)
root.configure(bg=TRANSPARENT_COLOR)

canvas = tk.Canvas(
    root,
    width=SCREEN_W,
    height=SCREEN_H,
    bg=TRANSPARENT_COLOR,
    highlightthickness=0,
    bd=0
)
canvas.pack()

root.update()
root.update_idletasks()

# Click-through overlay
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020
WS_EX_TOOLWINDOW = 0x00000080

hwnd = user32.GetParent(root.winfo_id())
if hwnd == 0:
    hwnd = root.winfo_id()

style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)

user32.SetWindowLongW(
    hwnd,
    GWL_EXSTYLE,
    style | WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOOLWINDOW
)

# -----------------------------
# Raw input integration
# -----------------------------
virtual_x, virtual_y = get_mouse_position()
raw_event_count = 0
absolute_event_count = 0

old_wndproc = None
new_wndproc_ref = None


def read_raw_mouse_delta(lparam):
    size = wintypes.UINT(0)

    user32.GetRawInputData(
        lparam,
        RID_INPUT,
        None,
        ctypes.byref(size),
        ctypes.sizeof(RAWINPUTHEADER),
    )

    if size.value == 0:
        return None

    buffer = ctypes.create_string_buffer(size.value)

    result = user32.GetRawInputData(
        lparam,
        RID_INPUT,
        buffer,
        ctypes.byref(size),
        ctypes.sizeof(RAWINPUTHEADER),
    )

    if result == 0xFFFFFFFF:
        return None

    raw = RAWINPUT.from_buffer_copy(buffer)

    if raw.header.dwType != RIM_TYPEMOUSE:
        return None

    mouse = raw.data.mouse

    if mouse.usFlags & MOUSE_MOVE_ABSOLUTE:
        return "absolute"

    return int(mouse.lLastX), int(mouse.lLastY)


def window_proc(hwnd_value, msg, wparam, lparam):
    global virtual_x, virtual_y
    global raw_event_count, absolute_event_count

    if msg == WM_INPUT:
        data = read_raw_mouse_delta(lparam)

        if data == "absolute":
            absolute_event_count += 1
            return 0

        if data is not None:
            dx, dy = data
            raw_event_count += 1

            if MIRROR_ENABLED and not key_down(VK_SHIFT):
                move_x = -dx if MIRROR_X else dx
                move_y = -dy if MIRROR_Y else dy

                virtual_x += move_x * MIRROR_STRENGTH
                virtual_y += move_y * MIRROR_STRENGTH

                virtual_x, virtual_y = set_mouse_position(virtual_x, virtual_y)
            else:
                virtual_x, virtual_y = get_mouse_position()

            return 0

    return user32.CallWindowProcW(old_wndproc, hwnd_value, msg, wparam, lparam)


new_wndproc_ref = WNDPROC(window_proc)
old_wndproc = SetWindowLongPtr(
    hwnd,
    GWLP_WNDPROC,
    ctypes.cast(new_wndproc_ref, ctypes.c_void_p).value,
)

rid = RAWINPUTDEVICE()
rid.usUsagePage = 0x01
rid.usUsage = 0x02
rid.dwFlags = RIDEV_INPUTSINK
rid.hwndTarget = hwnd

ok = user32.RegisterRawInputDevices(
    ctypes.byref(rid),
    1,
    ctypes.sizeof(RAWINPUTDEVICE),
)

if not ok:
    raise RuntimeError("RegisterRawInputDevices failed.")

# -----------------------------
# Cursor image setup
# -----------------------------
base_cursor_image, hotspot_x, hotspot_y = extract_cursor_image_and_hotspot()

if base_cursor_image is None:
    raise RuntimeError("Could not capture cursor image.")

base_cursor_image = remove_alpha_glow(base_cursor_image, threshold=120)

tk_cursor_images = {}


def cursor_scale_key(scale):
    return round(float(scale), 2)


def ensure_cursor_image_for_scale(scale):
    scale = cursor_scale_key(scale)

    if scale not in tk_cursor_images:
        new_w = max(1, round(base_cursor_image.width * scale))
        new_h = max(1, round(base_cursor_image.height * scale))

        resized = base_cursor_image.resize(
            (new_w, new_h),
            Image.Resampling.NEAREST
        )

        resized = remove_alpha_glow(resized, threshold=120)
        tk_cursor_images[scale] = ImageTk.PhotoImage(resized)

    return tk_cursor_images[scale]


for scale in sorted(set(CURSOR_SCALE_PRESETS + [REAL_DRAWN_CURSOR_SCALE])):
    ensure_cursor_image_for_scale(scale)


def draw_cursor_image(x, y, scale):
    image = ensure_cursor_image_for_scale(scale)
    canvas.create_image(round(x), round(y), image=image, anchor="nw")


# -----------------------------
# Create / rebuild fake cursors
# -----------------------------
fake_cursors = []


def rebuild_fake_cursors():
    global fake_cursors

    fake_cursors = []

    for _ in range(STATIC_COUNT):
        fake_cursors.append(FakeCursor("static"))

    for _ in range(SLOW_CLONE_COUNT):
        fake_cursors.append(FakeCursor("slow"))

    for _ in range(SAME_SPEED_CLONE_COUNT):
        fake_cursors.append(FakeCursor("same"))

    for _ in range(FAST_CLONE_COUNT):
        fake_cursors.append(FakeCursor("fast"))

    for _ in range(RANDOM_MOVER_COUNT):
        fake_cursors.append(FakeCursor("random"))

    for _ in range(TARGET_MOVER_COUNT):
        c = FakeCursor("target")
        c.choose_target()
        fake_cursors.append(c)


rebuild_fake_cursors()

# -----------------------------
# State
# -----------------------------
last_time = time.time()
start_time = time.time()
last_adjust_time = 0
last_toggle_time = 0
transparent_started_at = None

# v9.3/v9.6 polish state
runtime_hud_visible = bool(app_settings.get("runtime_hud_visible", False))
show_startup_help = bool(app_settings.get("show_startup_help", True))
last_hud_toggle_time = 0

prev_real_x, prev_real_y = get_mouse_position()

manual_offset_x = 0
manual_offset_y = 0

swarm_paused = False
show_fake_cursors = True
show_drawn_real_cursor = True

control_panel_visible = False
last_panel_toggle_time = 0
panel_hint_text = ""
panel_hint_until = 0
floating_control_bubble = None
floating_control_hidden_by_user = False
floating_control_drag = {
    "pressed": False,
    "moved": False,
    "mouse_x": 0,
    "mouse_y": 0,
    "window_x": 0,
    "window_y": 0,
}
pre_panic_state = None
nightmare_mode = "Disabled"


def restore_and_quit():
    if "save_app_settings" in globals():
        save_app_settings(update_last_state=True)
    set_visible_mode()
    restore_cursors_safely()
    root.destroy()



root.protocol("WM_DELETE_WINDOW", restore_and_quit)

# -----------------------------
# V9 Control Panel
# -----------------------------
def show_control_panel_hint(message=None, duration=5.0):
    global panel_hint_text, panel_hint_until

    panel_hint_text = message or "Control Panel hidden. Press Ctrl + Alt + C to open it again."
    panel_hint_until = time.time() + float(duration)


def clear_control_panel_hint():
    global panel_hint_text, panel_hint_until

    panel_hint_text = ""
    panel_hint_until = 0


def hide_control_panel():
    global control_panel_visible
    control_panel.withdraw()
    control_panel_visible = False
    show_control_panel_hint()
    update_floating_control_bubble_visibility()


def show_control_panel():
    global control_panel_visible
    clear_control_panel_hint()
    sync_ui_vars()
    control_panel.deiconify()
    control_panel.lift()
    control_panel.focus_force()
    control_panel_visible = True
    update_floating_control_bubble_visibility()


def toggle_control_panel():
    if control_panel_visible:
        hide_control_panel()
    else:
        show_control_panel()


def should_show_floating_control_bubble():
    """Show the floating CS bubble only when the Control Panel is hidden."""
    if floating_control_hidden_by_user:
        return False

    return not bool(control_panel_visible)


def update_floating_control_bubble_visibility():
    bubble = globals().get("floating_control_bubble")

    if bubble is None:
        return

    try:
        if should_show_floating_control_bubble():
            bubble.deiconify()
            bubble.attributes("-topmost", True)
            bubble.lift()
        else:
            bubble.withdraw()
    except Exception:
        pass


def lift_floating_control_bubble():
    """Backward-compatible helper used by older call sites."""
    update_floating_control_bubble_visibility()


def hide_floating_control_bubble_for_session():
    """Hide the floating CS bubble until the app is restarted.

    The keyboard shortcut still works, so users can reopen the Control Panel with
    Ctrl+Alt+C even after hiding this optional button.
    """
    global floating_control_hidden_by_user

    floating_control_hidden_by_user = True
    update_floating_control_bubble_visibility()
    show_control_panel_hint(
        "Floating CS button hidden for this session. Press Ctrl + Alt + C to open the Control Panel.",
        duration=6.0,
    )


def create_floating_control_bubble():
    """Create a small draggable CS button that reopens the Control Panel.

    The bubble is visible only while the Control Panel is hidden. It can be
    right-clicked and hidden for the current session if the user does not want
    it on screen.
    """
    global floating_control_bubble

    if floating_control_bubble is not None:
        update_floating_control_bubble_visibility()
        return floating_control_bubble

    bubble_size = 58
    default_x = max(screen_left + 18, min(screen_right - bubble_size - 18, screen_left + screen_w - bubble_size - 28))
    default_y = max(screen_top + 18, min(screen_bottom - bubble_size - 18, screen_top + screen_h - bubble_size - 92))

    bubble = tk.Toplevel(root)
    floating_control_bubble = bubble
    bubble.overrideredirect(True)
    bubble.geometry(f"{bubble_size}x{bubble_size}+{default_x}+{default_y}")
    bubble.configure(bg="#101820")
    bubble.attributes("-topmost", True)

    try:
        bubble.attributes("-toolwindow", True)
    except Exception:
        pass

    button = tk.Label(
        bubble,
        text="CS",
        bg="#101820",
        fg="#ffffff",
        activebackground="#101820",
        activeforeground="#ffffff",
        font=("Segoe UI", 14, "bold"),
        bd=2,
        relief="ridge",
        cursor="hand2",
    )
    button.pack(fill="both", expand=True)

    bubble_menu = tk.Menu(bubble, tearoff=0)
    bubble_menu.add_command(label="Open Control Panel", command=show_control_panel)
    bubble_menu.add_separator()
    bubble_menu.add_command(label="Hide Floating Button", command=hide_floating_control_bubble_for_session)

    def show_bubble_menu(event):
        floating_control_drag["pressed"] = False
        floating_control_drag["moved"] = False

        try:
            bubble_menu.tk_popup(event.x_root, event.y_root)
        finally:
            bubble_menu.grab_release()

    def on_press(event):
        if getattr(event, "num", None) == 3:
            return

        floating_control_drag["pressed"] = True
        floating_control_drag["moved"] = False
        floating_control_drag["mouse_x"] = event.x_root
        floating_control_drag["mouse_y"] = event.y_root
        floating_control_drag["window_x"] = bubble.winfo_x()
        floating_control_drag["window_y"] = bubble.winfo_y()

    def on_drag(event):
        if not floating_control_drag.get("pressed"):
            return

        dx = event.x_root - floating_control_drag["mouse_x"]
        dy = event.y_root - floating_control_drag["mouse_y"]

        if abs(dx) > 3 or abs(dy) > 3:
            floating_control_drag["moved"] = True

        new_x = floating_control_drag["window_x"] + dx
        new_y = floating_control_drag["window_y"] + dy

        new_x = max(screen_left + 4, min(screen_right - bubble_size - 4, int(new_x)))
        new_y = max(screen_top + 4, min(screen_bottom - bubble_size - 4, int(new_y)))

        bubble.geometry(f"{bubble_size}x{bubble_size}+{new_x}+{new_y}")

    def on_release(event):
        if getattr(event, "num", None) == 3:
            return

        floating_control_drag["pressed"] = False

        if not floating_control_drag.get("moved"):
            show_control_panel()

        update_floating_control_bubble_visibility()

    button.bind("<ButtonPress-1>", on_press)
    button.bind("<B1-Motion>", on_drag)
    button.bind("<ButtonRelease-1>", on_release)
    button.bind("<Button-3>", show_bubble_menu)
    bubble.bind("<ButtonPress-1>", on_press)
    bubble.bind("<B1-Motion>", on_drag)
    bubble.bind("<ButtonRelease-1>", on_release)
    bubble.bind("<Button-3>", show_bubble_menu)

    update_floating_control_bubble_visibility()
    return bubble


def toggle_runtime_hud():
    global runtime_hud_visible
    runtime_hud_visible = not runtime_hud_visible
    if "runtime_hud_var" in globals():
        runtime_hud_var.set(runtime_hud_visible)


def panic_resume_toggle():
    if pre_panic_state is None:
        panic_mode()
    else:
        resume_previous_mode()


def panic_button_text():
    return "RESUME PREVIOUS MODE" if pre_panic_state is not None else "SAFE MODE / PANIC"


def update_panic_button_labels():
    text = panic_button_text()
    for name in (
        "dashboard_panic_toggle_button",
        "safety_panic_toggle_button",
        "bottom_panic_toggle_button",
    ):
        button = globals().get(name)
        if button is not None:
            button.configure(text=text)


def panic_mode():
    global MIRROR_ENABLED, MIRROR_X, MIRROR_Y
    global swarm_paused, show_drawn_real_cursor, show_fake_cursors
    global pre_panic_state, nightmare_mode

    # Save the state only the first time panic is entered.
    # This lets Resume Previous Mode return to the exact setup you had before panic.
    if pre_panic_state is None:
        pre_panic_state = {
            "transparent_active": bool(transparent_active),
            "mirror_enabled": bool(MIRROR_ENABLED),
            "mirror_x": bool(MIRROR_X),
            "mirror_y": bool(MIRROR_Y),
            "mirror_strength": float(MIRROR_STRENGTH),
            "swarm_paused": bool(swarm_paused),
            "show_fake_cursors": bool(show_fake_cursors),
            "show_drawn_real_cursor": bool(show_drawn_real_cursor),
            "nightmare_mode": nightmare_mode,
            "manual_offset_x": int(manual_offset_x),
            "manual_offset_y": int(manual_offset_y),
            "real_drawn_cursor_scale": float(REAL_DRAWN_CURSOR_SCALE),
            "fake_cursor_wobble": float(FAKE_CURSOR_WOBBLE),
        }

    set_visible_mode()
    MIRROR_ENABLED = False
    show_drawn_real_cursor = True
    show_fake_cursors = True
    swarm_paused = True
    nightmare_mode = "Disabled"
    globals()["virtual_x"], globals()["virtual_y"] = get_mouse_position()
    sync_ui_vars()
    show_control_panel()


def resume_previous_mode():
    global MIRROR_ENABLED, MIRROR_X, MIRROR_Y, MIRROR_STRENGTH
    global swarm_paused, show_drawn_real_cursor, show_fake_cursors
    global pre_panic_state, nightmare_mode
    global manual_offset_x, manual_offset_y, REAL_DRAWN_CURSOR_SCALE, FAKE_CURSOR_WOBBLE

    if pre_panic_state is None:
        # Nothing to resume; just sync the UI so the user sees current state.
        sync_ui_vars()
        return

    state = pre_panic_state
    pre_panic_state = None

    MIRROR_ENABLED = bool(state["mirror_enabled"])
    MIRROR_X = bool(state["mirror_x"])
    MIRROR_Y = bool(state["mirror_y"])
    MIRROR_STRENGTH = float(state["mirror_strength"])
    swarm_paused = bool(state["swarm_paused"])
    show_fake_cursors = bool(state["show_fake_cursors"])
    show_drawn_real_cursor = bool(state["show_drawn_real_cursor"])
    nightmare_mode = normalize_nightmare_mode(state.get("nightmare_mode", "Disabled"))
    manual_offset_x = int(state.get("manual_offset_x", manual_offset_x))
    manual_offset_y = int(state.get("manual_offset_y", manual_offset_y))
    REAL_DRAWN_CURSOR_SCALE = max(0.25, min(3.0, float(state.get("real_drawn_cursor_scale", REAL_DRAWN_CURSOR_SCALE))))
    FAKE_CURSOR_WOBBLE = max(0.0, min(5.0, float(state.get("fake_cursor_wobble", FAKE_CURSOR_WOBBLE))))
    ensure_cursor_image_for_scale(REAL_DRAWN_CURSOR_SCALE)

    globals()["virtual_x"], globals()["virtual_y"] = get_mouse_position()

    if state["transparent_active"]:
        set_transparent_mode()
    else:
        set_visible_mode()

    sync_ui_vars()


def normalize_nightmare_mode(mode):
    mode = str(mode or "Disabled")
    if mode in NIGHTMARE_MODE_OPTIONS:
        return mode
    return "Disabled"


def apply_nightmare_mode(mode=None, sync=True):
    global nightmare_mode, show_fake_cursors, show_drawn_real_cursor, swarm_paused

    nightmare_mode = normalize_nightmare_mode(mode if mode is not None else nightmare_mode)

    if nightmare_mode == "Disabled":
        # Leaving Nightmare Mode returns to a safe, visible cursor state.
        set_visible_mode()
        show_fake_cursors = True
        show_drawn_real_cursor = True

    elif nightmare_mode == "Blind Mode":
        # No real drawn cursor and no fake cursors. Hold Shift for a temporary hint.
        set_transparent_mode()
        show_fake_cursors = False
        show_drawn_real_cursor = False

    elif nightmare_mode == "Fake-only Mode":
        # Fake cursors remain, but the real/drawn cursor is hidden.
        set_transparent_mode()
        show_fake_cursors = True
        show_drawn_real_cursor = False
        swarm_paused = False

    elif nightmare_mode == "Flicker Hint Mode":
        # Fake-only base, with a brief drawn-real cursor flash every few seconds.
        set_transparent_mode()
        show_fake_cursors = True
        show_drawn_real_cursor = False
        swarm_paused = False

    globals()["virtual_x"], globals()["virtual_y"] = get_mouse_position()

    if sync and "sync_ui_vars" in globals():
        sync_ui_vars()


def ui_apply_nightmare_mode():
    apply_nightmare_mode(nightmare_mode_var.get())


def ui_disable_nightmare_mode():
    apply_nightmare_mode("Disabled")


def ui_toggle_transparent():
    if transparent_var.get():
        set_transparent_mode()
    else:
        set_visible_mode()
    sync_ui_vars()


def ui_toggle_fake_cursors():
    global show_fake_cursors
    show_fake_cursors = bool(show_fake_var.get())


def ui_toggle_drawn_real():
    global show_drawn_real_cursor
    show_drawn_real_cursor = bool(drawn_real_var.get())


def ui_toggle_mirror():
    global MIRROR_ENABLED
    MIRROR_ENABLED = bool(mirror_enabled_var.get())
    globals()["virtual_x"], globals()["virtual_y"] = get_mouse_position()


def ui_toggle_mirror_x():
    global MIRROR_X
    MIRROR_X = bool(mirror_x_var.get())
    globals()["virtual_x"], globals()["virtual_y"] = get_mouse_position()


def ui_toggle_mirror_y():
    global MIRROR_Y
    MIRROR_Y = bool(mirror_y_var.get())
    globals()["virtual_x"], globals()["virtual_y"] = get_mouse_position()


def ui_toggle_pause():
    global swarm_paused
    swarm_paused = bool(pause_var.get())


def ui_toggle_runtime_hud():
    global runtime_hud_visible
    runtime_hud_visible = bool(runtime_hud_var.get())


def ui_toggle_startup_help():
    global show_startup_help
    show_startup_help = bool(startup_help_var.get())


def ui_set_mirror_strength(value):
    global MIRROR_STRENGTH
    MIRROR_STRENGTH = round(float(value), 2)
    mirror_strength_label_var.set(f"{MIRROR_STRENGTH:.2f}x")


def ui_restore_cursor():
    set_visible_mode()
    sync_ui_vars()


def ui_make_transparent():
    set_transparent_mode()
    sync_ui_vars()


def ui_disable_mirror():
    global MIRROR_ENABLED
    MIRROR_ENABLED = False
    globals()["virtual_x"], globals()["virtual_y"] = get_mouse_position()
    sync_ui_vars()


def ui_show_drawn_real():
    global show_drawn_real_cursor
    show_drawn_real_cursor = True
    sync_ui_vars()


def ui_pause_swarm():
    global swarm_paused
    swarm_paused = True
    sync_ui_vars()


def ui_resume_swarm():
    global swarm_paused
    swarm_paused = False
    sync_ui_vars()


def set_cursor_polish_vars_from_globals():
    if "manual_offset_x_var" not in globals():
        return

    manual_offset_x_var.set(int(manual_offset_x))
    manual_offset_y_var.set(int(manual_offset_y))
    real_cursor_scale_var.set(float(REAL_DRAWN_CURSOR_SCALE))
    real_cursor_scale_label_var.set(f"{REAL_DRAWN_CURSOR_SCALE:.2f}x")


def apply_cursor_polish_from_ui():
    global manual_offset_x, manual_offset_y, REAL_DRAWN_CURSOR_SCALE, CURRENT_PRESET_NAME

    manual_offset_x = safe_int_from_var(manual_offset_x_var, manual_offset_x, minimum=-200, maximum=200)
    manual_offset_y = safe_int_from_var(manual_offset_y_var, manual_offset_y, minimum=-200, maximum=200)
    REAL_DRAWN_CURSOR_SCALE = safe_float_from_var(real_cursor_scale_var, REAL_DRAWN_CURSOR_SCALE, minimum=0.25, maximum=3.0)
    REAL_DRAWN_CURSOR_SCALE = round(REAL_DRAWN_CURSOR_SCALE, 2)
    ensure_cursor_image_for_scale(REAL_DRAWN_CURSOR_SCALE)

    CURRENT_PRESET_NAME = "Custom Cursor"
    set_cursor_polish_vars_from_globals()
    update_panel_status()


def reset_cursor_polish_fields_to_current():
    set_cursor_polish_vars_from_globals()



def total_fake_cursor_count():
    return (
        STATIC_COUNT
        + SLOW_CLONE_COUNT
        + SAME_SPEED_CLONE_COUNT
        + FAST_CLONE_COUNT
        + RANDOM_MOVER_COUNT
        + TARGET_MOVER_COUNT
    )


def safe_int_from_var(var, default, minimum=0, maximum=500):
    try:
        value = int(var.get())
    except Exception:
        value = default

    return max(minimum, min(maximum, value))


def safe_float_from_var(var, default, minimum=0.0, maximum=100.0):
    try:
        value = float(var.get())
    except Exception:
        value = default

    return max(minimum, min(maximum, value))


def set_swarm_count_vars_from_globals():
    if "static_count_var" not in globals():
        return

    static_count_var.set(int(STATIC_COUNT))
    slow_count_var.set(int(SLOW_CLONE_COUNT))
    same_count_var.set(int(SAME_SPEED_CLONE_COUNT))
    fast_count_var.set(int(FAST_CLONE_COUNT))
    random_count_var.set(int(RANDOM_MOVER_COUNT))
    target_count_var.set(int(TARGET_MOVER_COUNT))
    movement_threshold_var.set(float(MOVE_DISTANCE_THRESHOLD))
    fake_cursor_wobble_var.set(float(FAKE_CURSOR_WOBBLE))
    fake_cursor_wobble_label_var.set(f"{FAKE_CURSOR_WOBBLE:.2f}x")
    randomize_draw_order_var.set(bool(RANDOMIZE_DRAW_ORDER))


def refresh_swarm_summary():
    if "swarm_summary_var" not in globals():
        return

    swarm_summary_var.set(
        f"Static: {STATIC_COUNT} | Slow: {SLOW_CLONE_COUNT} | Same: {SAME_SPEED_CLONE_COUNT} | Fast: {FAST_CLONE_COUNT}\n"
        f"Random: {RANDOM_MOVER_COUNT} | Target: {TARGET_MOVER_COUNT} | Total: {total_fake_cursor_count()}\n"
        f"Movement Threshold: {MOVE_DISTANCE_THRESHOLD:.2f} | Wobble: {FAKE_CURSOR_WOBBLE:.2f}x | Randomize Draw Order: {RANDOMIZE_DRAW_ORDER}"
    )


def apply_swarm_settings_from_ui():
    global STATIC_COUNT, SLOW_CLONE_COUNT, SAME_SPEED_CLONE_COUNT
    global FAST_CLONE_COUNT, RANDOM_MOVER_COUNT, TARGET_MOVER_COUNT
    global MOVE_DISTANCE_THRESHOLD, FAKE_CURSOR_WOBBLE, RANDOMIZE_DRAW_ORDER, CURRENT_PRESET_NAME

    STATIC_COUNT = safe_int_from_var(static_count_var, STATIC_COUNT)
    SLOW_CLONE_COUNT = safe_int_from_var(slow_count_var, SLOW_CLONE_COUNT)
    SAME_SPEED_CLONE_COUNT = safe_int_from_var(same_count_var, SAME_SPEED_CLONE_COUNT)
    FAST_CLONE_COUNT = safe_int_from_var(fast_count_var, FAST_CLONE_COUNT)
    RANDOM_MOVER_COUNT = safe_int_from_var(random_count_var, RANDOM_MOVER_COUNT)
    TARGET_MOVER_COUNT = safe_int_from_var(target_count_var, TARGET_MOVER_COUNT)
    MOVE_DISTANCE_THRESHOLD = safe_float_from_var(movement_threshold_var, MOVE_DISTANCE_THRESHOLD, minimum=0.0, maximum=50.0)
    FAKE_CURSOR_WOBBLE = safe_float_from_var(fake_cursor_wobble_var, FAKE_CURSOR_WOBBLE, minimum=0.0, maximum=5.0)
    FAKE_CURSOR_WOBBLE = round(FAKE_CURSOR_WOBBLE, 2)
    fake_cursor_wobble_label_var.set(f"{FAKE_CURSOR_WOBBLE:.2f}x")
    RANDOMIZE_DRAW_ORDER = bool(randomize_draw_order_var.get())

    CURRENT_PRESET_NAME = "Custom Swarm"
    density_preset_var.set("Custom")
    rebuild_fake_cursors()
    refresh_swarm_summary()
    update_panel_status()


def apply_density_preset_from_ui():
    name = density_preset_var.get()
    config = SCREEN_DENSITY_PRESETS.get(name)

    if not config:
        return

    static_count_var.set(config["static_count"])
    slow_count_var.set(config["slow_clone_count"])
    same_count_var.set(config["same_speed_clone_count"])
    fast_count_var.set(config["fast_clone_count"])
    random_count_var.set(config["random_mover_count"])
    target_count_var.set(config["target_mover_count"])
    apply_swarm_settings_from_ui()
    density_preset_var.set(name)


def reset_swarm_entries_to_current():
    set_swarm_count_vars_from_globals()
    density_preset_var.set("Custom")
    refresh_swarm_summary()


def apply_all_changes():
    apply_swarm_settings_from_ui()
    apply_cursor_polish_from_ui()
    sync_ui_vars()



# -----------------------------
# Preset system
# -----------------------------
def sanitize_count(value, default):
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return default


def capture_current_config(display_name=None, danger_level="Custom"):
    return {
        "display_name": display_name or CURRENT_PRESET_NAME,
        "danger_level": danger_level,
        "static_count": int(STATIC_COUNT),
        "slow_clone_count": int(SLOW_CLONE_COUNT),
        "same_speed_clone_count": int(SAME_SPEED_CLONE_COUNT),
        "fast_clone_count": int(FAST_CLONE_COUNT),
        "random_mover_count": int(RANDOM_MOVER_COUNT),
        "target_mover_count": int(TARGET_MOVER_COUNT),
        "movement_threshold": float(MOVE_DISTANCE_THRESHOLD),
        "fake_cursor_wobble": float(FAKE_CURSOR_WOBBLE),
        "manual_offset_x": int(manual_offset_x),
        "manual_offset_y": int(manual_offset_y),
        "real_drawn_cursor_scale": float(REAL_DRAWN_CURSOR_SCALE),
        "show_fake_cursors": bool(show_fake_cursors),
        "show_drawn_real_cursor": bool(show_drawn_real_cursor),
        "transparent_cursor": bool(transparent_active),
        "mirror_enabled": bool(MIRROR_ENABLED),
        "mirror_x": bool(MIRROR_X),
        "mirror_y": bool(MIRROR_Y),
        "mirror_strength": float(MIRROR_STRENGTH),
        "swarm_paused": bool(swarm_paused),
        "randomize_draw_order": bool(RANDOMIZE_DRAW_ORDER),
        "nightmare_mode": nightmare_mode,
    }



def preset_slot_key(value):
    """Convert UI slot display like '1' into internal key 'Preset 1'.
    Older JSON files that already use 'Preset 1' are still supported.
    """
    text_value = str(value).strip()

    if text_value.lower().startswith("preset "):
        suffix = text_value.split(" ", 1)[1].strip()
        if suffix.isdigit():
            return f"Preset {int(suffix)}"
        return text_value

    if text_value.isdigit():
        return f"Preset {int(text_value)}"

    return text_value


def preset_slot_display_values():
    return [str(i) for i in range(1, MAX_CUSTOM_PRESETS + 1)]


def preset_slot_display_from_key(key):
    text_value = str(key).strip()
    if text_value.lower().startswith("preset "):
        suffix = text_value.split(" ", 1)[1].strip()
        if suffix.isdigit():
            return str(int(suffix))
    return text_value

def default_custom_presets():
    base = dict(BUILT_IN_PRESETS["Chill"])
    presets = {}

    for i in range(1, MAX_CUSTOM_PRESETS + 1):
        key = f"Preset {i}"
        presets[key] = dict(base)
        presets[key]["display_name"] = key
        presets[key]["danger_level"] = "Custom"

    return presets


def load_custom_presets():
    if not PRESET_FILE.exists():
        presets = default_custom_presets()
        save_custom_presets(presets)
        return presets

    try:
        data = json.loads(PRESET_FILE.read_text(encoding="utf-8"))
    except Exception:
        data = {}

    presets = default_custom_presets()

    if isinstance(data, dict):
        raw_presets = data.get("custom_presets", data)

        if isinstance(raw_presets, dict):
            for key, cfg in raw_presets.items():
                if key in presets and isinstance(cfg, dict):
                    merged = dict(presets[key])
                    merged.update(cfg)
                    merged["display_name"] = str(merged.get("display_name", key))
                    presets[key] = merged

    return presets


def save_custom_presets(presets=None):
    presets = presets if presets is not None else custom_presets
    payload = {
        "version": APP_VERSION,
        "max_custom_presets": MAX_CUSTOM_PRESETS,
        "custom_presets": presets,
    }
    PRESET_FILE.write_text(json.dumps(payload, indent=4), encoding="utf-8")


def preset_preview_text(config):
    danger = config.get("danger_level", "Custom")
    transparent = "Transparent" if config.get("transparent_cursor", False) else "Visible"
    fake = "Visible" if config.get("show_fake_cursors", True) else "Hidden"
    drawn = "Visible" if config.get("show_drawn_real_cursor", True) else "Hidden"
    mirror = "On" if config.get("mirror_enabled", False) else "Off"
    paused = "Paused" if config.get("swarm_paused", False) else "Running"

    total = sum(
        sanitize_count(config.get(name), 0)
        for name in (
            "static_count",
            "slow_clone_count",
            "same_speed_clone_count",
            "fast_clone_count",
            "random_mover_count",
            "target_mover_count",
        )
    )

    return (
        f"Name: {config.get('display_name', 'Unnamed')}\n"
        f"Danger Level: {danger}\n"
        f"System Cursor: {transparent}\n"
        f"Fake Cursors: {fake}\n"
        f"Drawn-Real Cursor: {drawn}\n"
        f"Mirror: {mirror} | X: {config.get('mirror_x', True)} | Y: {config.get('mirror_y', True)} | Strength: {float(config.get('mirror_strength', 1.0)):.2f}x\n"
        f"Swarm: {paused} | Total fake cursors: {total}\n"
        f"Counts: static {config.get('static_count', 0)}, slow {config.get('slow_clone_count', 0)}, same {config.get('same_speed_clone_count', 0)}, fast {config.get('fast_clone_count', 0)}, random {config.get('random_mover_count', 0)}, target {config.get('target_mover_count', 0)}\n"
        f"Nightmare Mode: {config.get('nightmare_mode', 'Disabled')}\n"
        f"Movement Threshold: {float(config.get('movement_threshold', MOVE_DISTANCE_THRESHOLD)):.2f} | Wobble: {float(config.get('fake_cursor_wobble', FAKE_CURSOR_WOBBLE)):.2f}x\n"
        f"Real Cursor Scale: {float(config.get('real_drawn_cursor_scale', REAL_DRAWN_CURSOR_SCALE)):.2f}x | Manual Offset: ({int(config.get('manual_offset_x', manual_offset_x))}, {int(config.get('manual_offset_y', manual_offset_y))})"
    )


def apply_preset_config(config, source_name=None):
    global CURRENT_PRESET_NAME
    global STATIC_COUNT, SLOW_CLONE_COUNT, SAME_SPEED_CLONE_COUNT
    global FAST_CLONE_COUNT, RANDOM_MOVER_COUNT, TARGET_MOVER_COUNT
    global MOVE_DISTANCE_THRESHOLD, FAKE_CURSOR_WOBBLE
    global manual_offset_x, manual_offset_y, REAL_DRAWN_CURSOR_SCALE
    global MIRROR_ENABLED, MIRROR_X, MIRROR_Y, MIRROR_STRENGTH
    global swarm_paused, show_fake_cursors, show_drawn_real_cursor
    global RANDOMIZE_DRAW_ORDER, nightmare_mode

    STATIC_COUNT = sanitize_count(config.get("static_count"), STATIC_COUNT)
    SLOW_CLONE_COUNT = sanitize_count(config.get("slow_clone_count"), SLOW_CLONE_COUNT)
    SAME_SPEED_CLONE_COUNT = sanitize_count(config.get("same_speed_clone_count"), SAME_SPEED_CLONE_COUNT)
    FAST_CLONE_COUNT = sanitize_count(config.get("fast_clone_count"), FAST_CLONE_COUNT)
    RANDOM_MOVER_COUNT = sanitize_count(config.get("random_mover_count"), RANDOM_MOVER_COUNT)
    TARGET_MOVER_COUNT = sanitize_count(config.get("target_mover_count"), TARGET_MOVER_COUNT)
    try:
        MOVE_DISTANCE_THRESHOLD = max(0.0, float(config.get("movement_threshold", MOVE_DISTANCE_THRESHOLD)))
    except (TypeError, ValueError):
        pass

    try:
        FAKE_CURSOR_WOBBLE = max(0.0, min(5.0, float(config.get("fake_cursor_wobble", FAKE_CURSOR_WOBBLE))))
    except (TypeError, ValueError):
        pass

    try:
        manual_offset_x = max(-200, min(200, int(config.get("manual_offset_x", manual_offset_x))))
        manual_offset_y = max(-200, min(200, int(config.get("manual_offset_y", manual_offset_y))))
    except (TypeError, ValueError):
        pass

    try:
        REAL_DRAWN_CURSOR_SCALE = max(0.25, min(3.0, float(config.get("real_drawn_cursor_scale", REAL_DRAWN_CURSOR_SCALE))))
        REAL_DRAWN_CURSOR_SCALE = round(REAL_DRAWN_CURSOR_SCALE, 2)
        ensure_cursor_image_for_scale(REAL_DRAWN_CURSOR_SCALE)
    except (TypeError, ValueError):
        pass

    show_fake_cursors = bool(config.get("show_fake_cursors", show_fake_cursors))
    show_drawn_real_cursor = bool(config.get("show_drawn_real_cursor", show_drawn_real_cursor))
    MIRROR_ENABLED = bool(config.get("mirror_enabled", MIRROR_ENABLED))
    MIRROR_X = bool(config.get("mirror_x", MIRROR_X))
    MIRROR_Y = bool(config.get("mirror_y", MIRROR_Y))
    MIRROR_STRENGTH = float(config.get("mirror_strength", MIRROR_STRENGTH))
    swarm_paused = bool(config.get("swarm_paused", swarm_paused))
    RANDOMIZE_DRAW_ORDER = bool(config.get("randomize_draw_order", RANDOMIZE_DRAW_ORDER))
    nightmare_mode = normalize_nightmare_mode(config.get("nightmare_mode", "Disabled"))

    CURRENT_PRESET_NAME = source_name or str(config.get("display_name", "Custom Preset"))
    globals()["virtual_x"], globals()["virtual_y"] = get_mouse_position()
    rebuild_fake_cursors()

    if bool(config.get("transparent_cursor", transparent_active)):
        set_transparent_mode()
    else:
        set_visible_mode()

    if nightmare_mode != "Disabled":
        apply_nightmare_mode(nightmare_mode, sync=False)

    if "set_swarm_count_vars_from_globals" in globals():
        set_swarm_count_vars_from_globals()
    if "set_cursor_polish_vars_from_globals" in globals():
        set_cursor_polish_vars_from_globals()
    if "sync_ui_vars" in globals():
        sync_ui_vars()
    if "refresh_swarm_summary" in globals():
        refresh_swarm_summary()


def load_builtin_preset():
    name = built_in_preset_var.get()
    config = BUILT_IN_PRESETS.get(name)

    if not config:
        return

    apply_preset_config(dict(config), source_name=name)
    selected_builtin_preview_var.set(preset_preview_text(config))


def reset_builtin_preview():
    name = built_in_preset_var.get()
    config = BUILT_IN_PRESETS.get(name, {})
    selected_builtin_preview_var.set(preset_preview_text(config))


def load_custom_preset():
    key = preset_slot_key(custom_preset_slot_var.get())
    config = custom_presets.get(key)

    if not config:
        return

    apply_preset_config(dict(config), source_name=config.get("display_name", key))
    custom_preset_name_var.set(config.get("display_name", key))
    custom_preset_preview_var.set(preset_preview_text(config))


def save_current_to_custom_slot():
    key = preset_slot_key(custom_preset_slot_var.get())
    if key not in custom_presets:
        return

    name = custom_preset_name_var.get().strip() or key
    config = capture_current_config(display_name=name, danger_level="Custom")
    custom_presets[key] = config
    save_custom_presets()
    custom_preset_preview_var.set(preset_preview_text(config))


def rename_custom_preset():
    key = preset_slot_key(custom_preset_slot_var.get())
    if key not in custom_presets:
        return

    name = custom_preset_name_var.get().strip() or key
    custom_presets[key]["display_name"] = name
    save_custom_presets()
    custom_preset_preview_var.set(preset_preview_text(custom_presets[key]))


def delete_custom_preset():
    key = preset_slot_key(custom_preset_slot_var.get())
    if key not in custom_presets:
        return

    replacement = dict(BUILT_IN_PRESETS["Chill"])
    replacement["display_name"] = key
    replacement["danger_level"] = "Custom"
    custom_presets[key] = replacement
    custom_preset_name_var.set(key)
    save_custom_presets()
    custom_preset_preview_var.set(preset_preview_text(replacement))


def on_custom_slot_changed(_event=None):
    key = preset_slot_key(custom_preset_slot_var.get())
    config = custom_presets.get(key, {})
    custom_preset_name_var.set(config.get("display_name", key))
    custom_preset_preview_var.set(preset_preview_text(config))


def on_builtin_changed(_event=None):
    reset_builtin_preview()


custom_presets = load_custom_presets()

def save_app_settings(update_last_state=True):
    global app_settings

    app_settings["startup_mode"] = startup_mode_var.get() if "startup_mode_var" in globals() else app_settings.get("startup_mode", "Safe Mode")
    app_settings["startup_builtin_preset"] = startup_builtin_var.get() if "startup_builtin_var" in globals() else app_settings.get("startup_builtin_preset", "Legendary")
    app_settings["startup_custom_slot"] = startup_custom_slot_var.get() if "startup_custom_slot_var" in globals() else app_settings.get("startup_custom_slot", "1")
    app_settings["show_startup_help"] = bool(show_startup_help)
    app_settings["runtime_hud_visible"] = bool(runtime_hud_visible)

    if update_last_state:
        app_settings["last_state"] = capture_current_config(
            display_name=CURRENT_PRESET_NAME,
            danger_level="Last Used",
        )

    SETTINGS_FILE.write_text(json.dumps(app_settings, indent=4), encoding="utf-8")


def startup_safe_mode():
    global MIRROR_ENABLED, swarm_paused, show_fake_cursors, show_drawn_real_cursor
    global CURRENT_PRESET_NAME, pre_panic_state, nightmare_mode

    set_visible_mode()
    MIRROR_ENABLED = False
    swarm_paused = True
    show_fake_cursors = True
    show_drawn_real_cursor = True
    nightmare_mode = "Disabled"
    pre_panic_state = None
    CURRENT_PRESET_NAME = "Startup Safe Mode"
    globals()["virtual_x"], globals()["virtual_y"] = get_mouse_position()


def apply_startup_mode():
    mode = app_settings.get("startup_mode", "Safe Mode")

    # Startup is intentionally safe-first: the script finishes setup before this runs.
    if mode == "Safe Mode":
        startup_safe_mode()

    elif mode == "Last Used State":
        last_state = app_settings.get("last_state")
        if isinstance(last_state, dict):
            apply_preset_config(dict(last_state), source_name=last_state.get("display_name", "Last Used State"))
        else:
            startup_safe_mode()

    elif mode == "Built-in Preset":
        preset_name = app_settings.get("startup_builtin_preset", "Legendary")
        config = BUILT_IN_PRESETS.get(preset_name)
        if config:
            apply_preset_config(dict(config), source_name=preset_name)
        else:
            startup_safe_mode()

    elif mode == "Custom Preset":
        key = preset_slot_key(app_settings.get("startup_custom_slot", "1"))
        config = custom_presets.get(key)
        if config:
            apply_preset_config(dict(config), source_name=config.get("display_name", key))
        else:
            startup_safe_mode()

    else:
        startup_safe_mode()

    sync_ui_vars()



def apply_startup_mode_safely():
    """Apply startup mode only after setup is complete, with a safe fallback."""
    try:
        apply_startup_mode()
    except Exception as exc:
        try:
            set_visible_mode()
            startup_safe_mode()
            sync_ui_vars()
        except Exception:
            # Last-resort cursor restore attempt.
            restore_cursors_safely()

        messagebox.showwarning(
            "Startup Safety Fallback",
            "Startup mode failed, so Cursor Swarm opened in Safe Mode.\n\n"
            f"{exc}"
        )

def ui_save_startup_settings():
    app_settings["startup_mode"] = startup_mode_var.get()
    app_settings["startup_builtin_preset"] = startup_builtin_var.get()
    app_settings["startup_custom_slot"] = startup_custom_slot_var.get()
    app_settings["show_startup_help"] = bool(show_startup_help)
    app_settings["runtime_hud_visible"] = bool(runtime_hud_visible)
    save_app_settings(update_last_state=True)
    messagebox.showinfo("Startup Settings", f"Startup settings saved to:\n{SETTINGS_FILE}")


def ui_apply_startup_now():
    app_settings["startup_mode"] = startup_mode_var.get()
    app_settings["startup_builtin_preset"] = startup_builtin_var.get()
    app_settings["startup_custom_slot"] = startup_custom_slot_var.get()
    apply_startup_mode()


def generate_emergency_restore_script(show_message=True):
    """Create/update the emergency restore helper in the same folder.

    This is intentionally small and standalone so it can still be run if the
    main app is closed while the Windows cursor is hidden.
    """
    restore_path = RESTORE_SCRIPT_FILE

    script = """import ctypes

# Emergency cursor restore script for Cursor Swarm.
# Run this if the app closes while your system cursor is hidden.
SPI_SETCURSORS = 0x0057
user32 = ctypes.windll.user32

user32.SystemParametersInfoW(SPI_SETCURSORS, 0, None, 0)
print("Requested Windows to reload the system cursor scheme.")
input("Press Enter to close...")
"""

    try:
        restore_path.write_text(script, encoding="utf-8")
    except Exception as exc:
        if show_message:
            messagebox.showerror(
                "Emergency Restore Script",
                f"Could not create emergency restore script:\n{restore_path}\n\n{exc}"
            )
        return None

    if show_message:
        messagebox.showinfo("Emergency Restore Script", f"Created/updated:\n{restore_path}")

    return restore_path


def ensure_emergency_restore_script():
    """Quietly create the restore helper during startup."""
    return generate_emergency_restore_script(show_message=False)


README_TEXT = 'CursorSwarm v10.9\n==================\n\nCursorSwarm is a Windows cursor effects app for fake cursors, mirror movement, transparent cursor modes, presets, and visual cursor camouflage.\n\nIt is made for fun, experimentation, and user-controlled visual cursor effects.\n\n--------------------------------------------------\nIMPORTANT SAFETY NOTE\n--------------------------------------------------\n\nCursorSwarm can hide your real system cursor and make your mouse movement intentionally confusing.\n\nUse stronger modes carefully. Do not use CursorSwarm while doing important work, payments, exams, accessibility-dependent tasks, or anything where losing track of your cursor could cause problems.\n\nBefore using stronger modes, remember these recovery controls:\n\nCtrl + Alt + C      = Open / close Control Panel\nCtrl + Alt + Space  = Safe Mode / Resume Previous Mode\nCtrl + Alt + Q      = Quit Safely and restore cursor\nHold Shift          = Temporary cursor hint / normal movement in some modes\n\nCursorSwarm v10.9 opens the Control Panel automatically when launched so the main app controls are visible.\n\nA small floating CS control button also stays on screen. Click it to reopen or focus the Control Panel. You can drag it to a different screen position.\n\nIf the Control Panel is hidden, a temporary on-screen hint shows the shortcut to reopen it.\n\nIf your cursor ever gets stuck hidden after the app is closed, run:\n\nrestore_cursor_emergency.exe\n\nNo Python installation is required for the emergency restore EXE.\n\nA fallback developer script may also be created as restore_cursor_emergency.py.\n\n--------------------------------------------------\nPRIVACY SUMMARY\n--------------------------------------------------\n\nCursorSwarm does not collect, upload, sell, or share personal data.\n\nCursorSwarm stores settings and presets locally on your device only.\n\nThe app does not require an account, server connection, analytics, telemetry, ads, or cloud syncing.\n\nFor the full privacy policy, see:\n\nCursorSwarm_PrivacyPolicy.txt\n\n--------------------------------------------------\nTERMS AND SAFETY NOTICE\n--------------------------------------------------\n\nCursorSwarm is provided as an experimental cursor effects app.\n\nBy using CursorSwarm, you understand that it can make the cursor difficult to see or control, especially in Nightmare and Mirror modes.\n\nUse Safe Mode, Quit Safely, and the standalone emergency restore EXE if needed.\n\nFor the full terms and safety notice, see:\n\nCursorSwarm_TermsAndSafety.txt\n\n--------------------------------------------------\nFILES\n--------------------------------------------------\n\nCursorSwarm may create these support files if they are missing:\n\ncursor_presets.json\n    Stores your custom preset slots.\n\ncursor_settings.json\n    Stores startup mode, HUD visibility, and last-used state.\n\nrestore_cursor_emergency.exe\n    Standalone emergency cursor restore helper included with installer/MSIX builds.\n\nrestore_cursor_emergency.py\n    Fallback emergency cursor restore script created by the app for development/manual recovery.\n\nREADME.txt\n    Basic usage, safety, recovery, and troubleshooting information.\n\nCursorSwarm_PrivacyPolicy.txt\n    Privacy policy for release/distribution.\n\nCursorSwarm_TermsAndSafety.txt\n    Terms, safety notice, and user responsibility information.\n\nCursorSwarm_ReleaseNotes.txt\n    Current release notes.\n\nIn normal portable EXE mode, these files are created beside CursorSwarm.exe.\n\nIn MSIX mode, Windows may install the app in a read-only package folder, so CursorSwarm stores support files in:\n\n%LOCALAPPDATA%\\CursorSwarm\n\n--------------------------------------------------\nBASIC HOTKEYS\n--------------------------------------------------\n\nCtrl + Alt + C\n    Show / hide the Control Panel.\n\nCtrl + Alt + Space\n    Toggle Safe Mode / Resume Previous Mode.\n\nCtrl + Alt + Q\n    Quit safely and restore your system cursor.\n\nCtrl + Alt + R\n    Toggle real system cursor visible / transparent.\n\nCtrl + Alt + M\n    Toggle Mirror Mode.\n\nCtrl + Alt + X\n    Toggle Mirror X direction.\n\nCtrl + Alt + Y\n    Toggle Mirror Y direction.\n\nCtrl + Alt + P\n    Pause / resume fake cursor swarm.\n\nCtrl + Alt + H\n    Hide / show drawn-real cursor.\n\nCtrl + Alt + D\n    Toggle Runtime HUD.\n\nHold Shift\n    Temporary safety hint / normal movement behavior depending on mode.\n\n--------------------------------------------------\nCONTROL PANEL AND FLOATING BUTTON\n--------------------------------------------------\n\nCursorSwarm opens the Control Panel automatically when launched.\n\nYou can also open or hide it anytime with:\n\nCtrl + Alt + C\n\nIf the panel is hidden, CursorSwarm briefly displays a reminder showing this shortcut.\n\nThe floating CS button is a small draggable on-screen control. Click it to reopen or focus the Control Panel.\n\nMain tabs:\n\nDashboard\n    Quick controls and important safety buttons.\n\nCursor\n    System cursor visibility, drawn-real cursor, cursor scale, manual offset, and Nightmare modes.\n\nMirror\n    Raw input mirror movement controls.\n\nSwarm\n    Fake cursor counts, density presets, movement threshold, wobble/randomness, and draw order.\n\nPresets\n    Built-in presets and 10 custom preset slots.\n\nSafety\n    Startup mode, emergency restore, and recovery options.\n\nAdvanced\n    Debug/status information, import/export backup tools, app info, and release document helpers.\n\n--------------------------------------------------\nRECOMMENDED FIRST TEST\n--------------------------------------------------\n\nBefore using strong modes, test these:\n\n1. Open app.\n2. Confirm the Control Panel appears automatically.\n3. Confirm the floating CS button is visible.\n4. Press Ctrl + Alt + C to hide the Control Panel.\n5. Confirm the shortcut hint appears briefly.\n6. Click the floating CS button to reopen the Control Panel.\n7. Press Ctrl + Alt + Space for Safe Mode.\n8. Press Ctrl + Alt + Q to quit safely.\n\nMake sure the cursor restores normally.\n\n--------------------------------------------------\nTROUBLESHOOTING\n--------------------------------------------------\n\nIf the cursor is hidden:\n    Press Ctrl + Alt + R or Ctrl + Alt + Q.\n\nIf movement is confusing:\n    Press Ctrl + Alt + Space for Safe Mode.\n\nIf the Control Panel is hidden:\n    Press Ctrl + Alt + C or click the floating CS button.\n\nIf the app is closed but the cursor is still hidden:\n    Run restore_cursor_emergency.exe.\n\nIf config files are broken:\n    Delete cursor_settings.json and restart the app.\n    The app will recreate it.\n\nIf presets are broken:\n    Use Reset All Custom Presets from the app,\n    or delete cursor_presets.json and restart.\n\n--------------------------------------------------\nVERSION\n--------------------------------------------------\n\nCursorSwarm v10.9\n\nv10.7\n    Release-readiness polish, privacy policy, terms/safety notice, and final pre-publishing documents.\n\nv10.8\n    Certification fix and recovery polish: visible Control Panel on launch, temporary shortcut hint, Store-friendly Start Menu packaging, and standalone emergency restore EXE support.\n\nv10.9\n    Added a draggable floating CS control button so users can reopen or focus the Control Panel without relying only on a keyboard shortcut.\n\nCopyright (C) 2026 Palugula Tharun Kumar.\n'


PRIVACY_POLICY_TEXT = "CursorSwarm Privacy Policy\n==========================\n\nEffective Version: CursorSwarm v10.9\nCopyright (C) 2026 Palugula Tharun Kumar.\n\nCursorSwarm does not collect, transmit, sell, rent, or share personal data.\n\nCursorSwarm is designed as a local Windows desktop app. It runs on your device and stores its settings locally.\n\nCursorSwarm does not use user accounts, cloud syncing, analytics, telemetry, advertising trackers, remote servers, or automatic data uploads.\n\nCursorSwarm may create local settings, presets, README, terms, release notes, and emergency restore files on your device. These files are stored locally. In normal portable EXE mode, they may be created beside CursorSwarm.exe. In MSIX mode, they are stored under the user's Local AppData folder.\n\nCursorSwarm reads local mouse movement and keyboard shortcut input only while the app is running, in order to provide cursor effects, mirror movement, Safe Mode, and safe quit controls.\n\nCursorSwarm does not need internet access for its core features and does not intentionally contact external servers.\n\nYou can delete CursorSwarm's local settings files to reset the app. You can uninstall CursorSwarm using Windows Settings, the installer uninstaller, or the MSIX uninstall flow depending on how it was installed.\n\nFuture versions may update this policy if the app changes.\n\nNo public support email or website is configured for this release.\n"


TERMS_SAFETY_TEXT = "CursorSwarm Terms and Safety Notice\n===================================\n\nEffective Version: CursorSwarm v10.9\nCopyright (C) 2026 Palugula Tharun Kumar.\n\nCursorSwarm is a Windows cursor effects app made for fun, experimentation, and visual cursor confusion.\n\nCursorSwarm can make your cursor difficult to see or control. Do not use stronger modes while performing important, sensitive, or high-risk tasks, including payments, exams, accessibility-dependent tasks, system configuration tasks, or work where cursor accuracy is important.\n\nImportant recovery controls:\n\nCtrl + Alt + C      = Open / close Control Panel\nFloating CS button  = Reopen or focus Control Panel\nCtrl + Alt + Space  = Safe Mode / Resume Previous Mode\nCtrl + Alt + Q      = Quit Safely and restore cursor\nCtrl + Alt + R      = Toggle real system cursor visible / transparent\nHold Shift          = Temporary cursor hint / normal movement behavior in some modes\n\nIf your cursor is still hidden after closing the app, run:\n\nrestore_cursor_emergency.exe\n\nThe standalone emergency restore EXE does not require Python to be installed.\n\nBy using CursorSwarm, you understand that the app intentionally changes cursor visibility and movement behavior. You are responsible for using Safe Mode, Quit Safely, the floating control button, keyboard shortcuts, and the emergency restore tool when needed.\n\nDo not use CursorSwarm to mislead, disrupt, or interfere with another person's computer use.\n\nCursorSwarm is provided as-is, without warranty of any kind. The developer is not responsible for data loss, interrupted work, user error, or device-specific issues caused by misuse or unexpected behavior.\n\nCursorSwarm is designed to run locally and does not collect, upload, sell, or share personal data. See CursorSwarm_PrivacyPolicy.txt for details.\n"


RELEASE_NOTES_TEXT = 'CursorSwarm v10.9 Release Notes\n===============================\n\nRelease type: Microsoft Store certification follow-up and visible-control polish\n\nHighlights:\n\n- Updated app version to v10.9.\n- Added a small draggable floating CS control button.\n- The floating CS button can reopen or focus the Control Panel when clicked.\n- Control Panel still opens automatically when the app launches.\n- Ctrl + Alt + C still works as the keyboard shortcut to show or hide the Control Panel.\n- Temporary shortcut hint remains visible when the Control Panel is hidden.\n- Standalone emergency restore EXE support remains included.\n- Installer script still creates only one Start Menu shortcut: CursorSwarm.\n\nCertification-focused changes:\n\n- The main product UI is visible immediately after launch.\n- A visible floating on-screen control remains available for reopening/focusing the Control Panel.\n- The shortcut to reopen the Control Panel is shown to users when the panel is hidden.\n- Extra installed documents/tools are not exposed as separate Start Menu tiles in the installer script.\n\nRecommended testing:\n\n1. Build CursorSwarm.exe v10.9.\n2. Build or reuse restore_cursor_emergency.exe.\n3. Install with the v10.9 installer.\n4. Confirm only CursorSwarm appears in the Start Menu.\n5. Launch CursorSwarm and confirm the Control Panel opens automatically.\n6. Confirm the floating CS button is visible.\n7. Hide the Control Panel and confirm the temporary shortcut hint appears.\n8. Click the floating CS button and confirm the Control Panel opens/focuses.\n9. Test Ctrl + Alt + C, Ctrl + Alt + Space, and Ctrl + Alt + Q.\n10. Build the Store-identity MSIX and resubmit with certification notes.\n'


def generate_readme_file(show_message=True, overwrite=False):
    """Create README.txt beside the app.

    By default this does not overwrite an existing README, so manual edits are kept.
    """
    readme_path = README_FILE

    if readme_path.exists() and not overwrite:
        if show_message:
            messagebox.showinfo(
                "README",
                f"README already exists and was left unchanged:\n{readme_path}"
            )
        return readme_path

    try:
        readme_path.write_text(README_TEXT, encoding="utf-8")
    except Exception as exc:
        if show_message:
            messagebox.showerror(
                "README",
                f"Could not create README file:\n{readme_path}\n\n{exc}"
            )
        return None

    if show_message:
        messagebox.showinfo("README", f"Created README file:\n{readme_path}")

    return readme_path


def ensure_readme_file():
    """Quietly create README.txt during startup if it is missing."""
    return generate_readme_file(show_message=False, overwrite=False)


def generate_text_document(path, content, title, show_message=True, overwrite=False):
    """Create a text document beside the app without overwriting manual edits by default."""
    path = Path(path)

    if path.exists() and not overwrite:
        if show_message:
            messagebox.showinfo(
                title,
                f"{title} already exists and was left unchanged:\n{path}"
            )
        return path

    try:
        path.write_text(content, encoding="utf-8")
    except Exception as exc:
        if show_message:
            messagebox.showerror(
                title,
                f"Could not create {title}:\n{path}\n\n{exc}"
            )
        return None

    if show_message:
        messagebox.showinfo(title, f"Created/updated:\n{path}")

    return path


def generate_privacy_policy_file(show_message=True, overwrite=False):
    return generate_text_document(
        PRIVACY_POLICY_FILE,
        PRIVACY_POLICY_TEXT,
        "Privacy Policy",
        show_message=show_message,
        overwrite=overwrite,
    )


def generate_terms_safety_file(show_message=True, overwrite=False):
    return generate_text_document(
        TERMS_SAFETY_FILE,
        TERMS_SAFETY_TEXT,
        "Terms and Safety Notice",
        show_message=show_message,
        overwrite=overwrite,
    )


def generate_release_notes_file(show_message=True, overwrite=False):
    return generate_text_document(
        RELEASE_NOTES_FILE,
        RELEASE_NOTES_TEXT,
        "Release Notes",
        show_message=show_message,
        overwrite=overwrite,
    )


def ensure_release_documents():
    """Quietly create release documents during startup if they are missing."""
    generate_privacy_policy_file(show_message=False, overwrite=False)
    generate_terms_safety_file(show_message=False, overwrite=False)
    generate_release_notes_file(show_message=False, overwrite=False)

# -----------------------------
# Import / Export and config reset
# -----------------------------
def backup_timestamp():
    return time.strftime("%Y%m%d_%H%M%S")


def read_json_file(json_path):
    try:
        return json.loads(Path(json_path).read_text(encoding="utf-8"))
    except Exception as exc:
        messagebox.showerror("JSON Error", f"Could not read JSON file:\n{json_path}\n\n{exc}")
        return None


def write_json_file(json_path, payload):
    try:
        Path(json_path).write_text(json.dumps(payload, indent=4), encoding="utf-8")
        return True
    except Exception as exc:
        messagebox.showerror("Save Error", f"Could not write JSON file:\n{json_path}\n\n{exc}")
        return False


def normalize_imported_presets(raw_presets):
    presets = default_custom_presets()

    if not isinstance(raw_presets, dict):
        return presets

    for raw_key, cfg in raw_presets.items():
        key = preset_slot_key(raw_key)

        if key not in presets or not isinstance(cfg, dict):
            continue

        merged = dict(presets[key])
        merged.update(cfg)
        merged["display_name"] = str(merged.get("display_name", key))
        merged["nightmare_mode"] = normalize_nightmare_mode(merged.get("nightmare_mode", "Disabled"))
        presets[key] = merged

    return presets


def normalize_imported_app_settings(raw_settings):
    settings = dict(DEFAULT_APP_SETTINGS)

    if isinstance(raw_settings, dict):
        settings.update(raw_settings)

    if settings.get("startup_mode") not in STARTUP_MODE_OPTIONS:
        settings["startup_mode"] = "Safe Mode"

    settings["startup_builtin_preset"] = str(settings.get("startup_builtin_preset", "Legendary"))
    settings["startup_custom_slot"] = str(settings.get("startup_custom_slot", "1"))
    settings["show_startup_help"] = bool(settings.get("show_startup_help", True))
    settings["runtime_hud_visible"] = bool(settings.get("runtime_hud_visible", False))

    return settings


def export_full_backup():
    # Capture the current state before exporting.
    if "save_app_settings" in globals():
        save_app_settings(update_last_state=True)

    default_name = f"cursor_swarm_full_backup_{backup_timestamp()}.json"
    filename = filedialog.asksaveasfilename(
        title="Export Cursor Swarm Backup",
        defaultextension=".json",
        initialfile=default_name,
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
    )

    if not filename:
        return

    payload = {
        "type": "cursor_swarm_full_backup",
        "version": APP_VERSION,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "app_settings": app_settings,
        "custom_presets": custom_presets,
    }

    if write_json_file(filename, payload):
        messagebox.showinfo("Export Complete", f"Full backup exported to:\n{filename}")


def import_full_backup():
    global app_settings, custom_presets, runtime_hud_visible, show_startup_help

    filename = filedialog.askopenfilename(
        title="Import Cursor Swarm Backup",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
    )

    if not filename:
        return

    data = read_json_file(filename)
    if not isinstance(data, dict):
        return

    raw_presets = data.get("custom_presets")
    raw_settings = data.get("app_settings")

    if not isinstance(raw_presets, dict) and not isinstance(raw_settings, dict):
        messagebox.showerror(
            "Invalid Backup",
            "This file does not look like a Cursor Swarm full backup."
        )
        return

    if not messagebox.askyesno(
        "Import Full Backup",
        "This will replace your current custom presets and app settings.\n\nContinue?"
    ):
        return

    # Keep local safety copies before overwriting.
    if PRESET_FILE.exists():
        PRESET_FILE.with_name(f"cursor_presets_before_import_{backup_timestamp()}.json").write_text(
            PRESET_FILE.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    if SETTINGS_FILE.exists():
        SETTINGS_FILE.with_name(f"cursor_settings_before_import_{backup_timestamp()}.json").write_text(
            SETTINGS_FILE.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    if isinstance(raw_presets, dict):
        custom_presets = normalize_imported_presets(raw_presets)
        save_custom_presets(custom_presets)

    if isinstance(raw_settings, dict):
        app_settings = normalize_imported_app_settings(raw_settings)
        runtime_hud_visible = bool(app_settings.get("runtime_hud_visible", False))
        show_startup_help = bool(app_settings.get("show_startup_help", True))
        SETTINGS_FILE.write_text(json.dumps(app_settings, indent=4), encoding="utf-8")

    if "custom_preset_slot_var" in globals():
        custom_preset_slot_var.set("1")

    sync_ui_vars()
    messagebox.showinfo("Import Complete", "Backup imported successfully.")


def export_selected_custom_preset():
    key = preset_slot_key(custom_preset_slot_var.get())

    if key not in custom_presets:
        messagebox.showerror("Preset Error", "Selected custom preset slot was not found.")
        return

    preset_name = str(custom_presets[key].get("display_name", key)).replace(" ", "_")
    default_name = f"cursor_swarm_preset_{preset_slot_display_from_key(key)}_{preset_name}.json"

    filename = filedialog.asksaveasfilename(
        title="Export Selected Preset",
        defaultextension=".json",
        initialfile=default_name,
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
    )

    if not filename:
        return

    payload = {
        "type": "cursor_swarm_single_preset",
        "version": APP_VERSION,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "slot": preset_slot_display_from_key(key),
        "preset": custom_presets[key],
    }

    if write_json_file(filename, payload):
        messagebox.showinfo("Export Complete", f"Preset exported to:\n{filename}")


def import_selected_custom_preset():
    key = preset_slot_key(custom_preset_slot_var.get())

    if key not in custom_presets:
        messagebox.showerror("Preset Error", "Selected custom preset slot was not found.")
        return

    filename = filedialog.askopenfilename(
        title="Import Preset Into Selected Slot",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
    )

    if not filename:
        return

    data = read_json_file(filename)
    if not isinstance(data, dict):
        return

    preset_config = data.get("preset", data)

    if not isinstance(preset_config, dict):
        messagebox.showerror("Invalid Preset", "This file does not contain a valid preset.")
        return

    if not messagebox.askyesno(
        "Import Preset",
        f"Import this preset into slot {preset_slot_display_from_key(key)}?\n\n"
        "This will overwrite the selected custom preset slot."
    ):
        return

    base = dict(BUILT_IN_PRESETS["Chill"])
    base.update(preset_config)
    base["display_name"] = str(base.get("display_name", key))
    base["danger_level"] = str(base.get("danger_level", "Custom"))
    base["nightmare_mode"] = normalize_nightmare_mode(base.get("nightmare_mode", "Disabled"))

    custom_presets[key] = base
    save_custom_presets()
    on_custom_slot_changed()
    sync_ui_vars()
    messagebox.showinfo("Import Complete", f"Preset imported into slot {preset_slot_display_from_key(key)}.")


def reset_app_settings_to_default():
    global app_settings, runtime_hud_visible, show_startup_help

    if not messagebox.askyesno(
        "Reset App Settings",
        "Reset startup settings, HUD visibility, and app-level settings to defaults?\n\n"
        "Custom presets will not be deleted."
    ):
        return

    app_settings = dict(DEFAULT_APP_SETTINGS)
    runtime_hud_visible = bool(app_settings.get("runtime_hud_visible", False))
    show_startup_help = bool(app_settings.get("show_startup_help", True))
    SETTINGS_FILE.write_text(json.dumps(app_settings, indent=4), encoding="utf-8")
    sync_ui_vars()
    messagebox.showinfo("Settings Reset", "App settings were reset to defaults.")


def reset_all_custom_presets():
    global custom_presets

    if not messagebox.askyesno(
        "Reset All Custom Presets",
        "This will reset all 10 custom preset slots to default Chill-style presets.\n\n"
        "Continue?"
    ):
        return

    custom_presets = default_custom_presets()
    save_custom_presets()

    if "custom_preset_slot_var" in globals():
        custom_preset_slot_var.set("1")

    on_custom_slot_changed()
    sync_ui_vars()
    messagebox.showinfo("Presets Reset", "All custom preset slots were reset.")


def sync_ui_vars():
    transparent_var.set(bool(transparent_active))
    show_fake_var.set(bool(show_fake_cursors))
    drawn_real_var.set(bool(show_drawn_real_cursor))
    if "nightmare_mode_var" in globals():
        nightmare_mode_var.set(nightmare_mode)
    mirror_enabled_var.set(bool(MIRROR_ENABLED))
    mirror_x_var.set(bool(MIRROR_X))
    mirror_y_var.set(bool(MIRROR_Y))
    pause_var.set(bool(swarm_paused))
    mirror_strength_var.set(float(MIRROR_STRENGTH))
    mirror_strength_label_var.set(f"{MIRROR_STRENGTH:.2f}x")
    if "runtime_hud_var" in globals():
        runtime_hud_var.set(bool(runtime_hud_visible))
    if "startup_help_var" in globals():
        startup_help_var.set(bool(show_startup_help))
    if "startup_mode_var" in globals():
        startup_mode_var.set(app_settings.get("startup_mode", "Safe Mode"))
    if "startup_builtin_var" in globals():
        startup_builtin_var.set(app_settings.get("startup_builtin_preset", "Legendary"))
    if "startup_custom_slot_var" in globals():
        startup_custom_slot_var.set(str(app_settings.get("startup_custom_slot", "1")))
    if "set_swarm_count_vars_from_globals" in globals():
        set_swarm_count_vars_from_globals()
    if "set_cursor_polish_vars_from_globals" in globals():
        set_cursor_polish_vars_from_globals()
    update_panel_status()
    if "update_panic_button_labels" in globals():
        update_panic_button_labels()
    if "selected_builtin_preview_var" in globals():
        reset_builtin_preview()
    if "custom_preset_preview_var" in globals():
        on_custom_slot_changed()
    if "refresh_swarm_summary" in globals():
        refresh_swarm_summary()


def update_panel_status():
    transparent_text = "TRANSPARENT" if transparent_active else "VISIBLE"
    mirror_text = "ON" if MIRROR_ENABLED else "OFF"
    swarm_text = "PAUSED" if swarm_paused else "RUNNING"
    real_text = "VISIBLE" if show_drawn_real_cursor else "HIDDEN"
    fake_text = "VISIBLE" if show_fake_cursors else "HIDDEN"
    nightmare_text = nightmare_mode if nightmare_mode != "Disabled" else "OFF"

    panel_status_var.set(
        f"Preset: {CURRENT_PRESET_NAME} | Cursor: {transparent_text} | "
        f"Mirror: {mirror_text} | Swarm: {swarm_text} | "
        f"RealDrawn: {real_text} | Fake: {fake_text} | Nightmare: {nightmare_text}"
    )


def make_section(parent, title):
    frame = ttk.LabelFrame(parent, text=title, padding=10)
    frame.pack(fill="x", padx=10, pady=8)
    return frame


control_panel = tk.Toplevel(root)
control_panel.title("Cursor Swarm v10.9 Control Panel")
control_panel.geometry("760x560+120+80")
control_panel.minsize(520, 360)
control_panel.attributes("-topmost", True)
control_panel.protocol("WM_DELETE_WINDOW", hide_control_panel)

panel_status_var = tk.StringVar(value="Loading status...")
mirror_strength_label_var = tk.StringVar(value=f"{MIRROR_STRENGTH:.2f}x")

transparent_var = tk.BooleanVar(value=transparent_active)
show_fake_var = tk.BooleanVar(value=show_fake_cursors)
drawn_real_var = tk.BooleanVar(value=show_drawn_real_cursor)
nightmare_mode_var = tk.StringVar(value=nightmare_mode)
mirror_enabled_var = tk.BooleanVar(value=MIRROR_ENABLED)
mirror_x_var = tk.BooleanVar(value=MIRROR_X)
mirror_y_var = tk.BooleanVar(value=MIRROR_Y)
pause_var = tk.BooleanVar(value=swarm_paused)
runtime_hud_var = tk.BooleanVar(value=runtime_hud_visible)
startup_help_var = tk.BooleanVar(value=show_startup_help)
startup_mode_var = tk.StringVar(value=app_settings.get("startup_mode", "Safe Mode"))
startup_builtin_var = tk.StringVar(value=app_settings.get("startup_builtin_preset", "Legendary"))
startup_custom_slot_var = tk.StringVar(value=str(app_settings.get("startup_custom_slot", "1")))
mirror_strength_var = tk.DoubleVar(value=MIRROR_STRENGTH)
density_preset_var = tk.StringVar(value="Custom")
static_count_var = tk.IntVar(value=STATIC_COUNT)
slow_count_var = tk.IntVar(value=SLOW_CLONE_COUNT)
same_count_var = tk.IntVar(value=SAME_SPEED_CLONE_COUNT)
fast_count_var = tk.IntVar(value=FAST_CLONE_COUNT)
random_count_var = tk.IntVar(value=RANDOM_MOVER_COUNT)
target_count_var = tk.IntVar(value=TARGET_MOVER_COUNT)
movement_threshold_var = tk.DoubleVar(value=MOVE_DISTANCE_THRESHOLD)
fake_cursor_wobble_var = tk.DoubleVar(value=FAKE_CURSOR_WOBBLE)
fake_cursor_wobble_label_var = tk.StringVar(value=f"{FAKE_CURSOR_WOBBLE:.2f}x")
manual_offset_x_var = tk.IntVar(value=manual_offset_x)
manual_offset_y_var = tk.IntVar(value=manual_offset_y)
real_cursor_scale_var = tk.DoubleVar(value=REAL_DRAWN_CURSOR_SCALE)
real_cursor_scale_label_var = tk.StringVar(value=f"{REAL_DRAWN_CURSOR_SCALE:.2f}x")
randomize_draw_order_var = tk.BooleanVar(value=RANDOMIZE_DRAW_ORDER)
swarm_summary_var = tk.StringVar(value="")
built_in_preset_var = tk.StringVar(value="Legendary")
selected_builtin_preview_var = tk.StringVar(value=preset_preview_text(BUILT_IN_PRESETS["Legendary"]))
custom_preset_slot_var = tk.StringVar(value="1")
custom_preset_name_var = tk.StringVar(value=custom_presets["Preset 1"].get("display_name", "Preset 1"))
custom_preset_preview_var = tk.StringVar(value=preset_preview_text(custom_presets["Preset 1"]))

# Top bar
top_frame = ttk.Frame(control_panel, padding=(10, 8))
top_frame.pack(fill="x")

ttk.Label(top_frame, text="Cursor Swarm v10.9", font=("Segoe UI", 15, "bold")).pack(side="left")
ttk.Button(top_frame, text="Hide Panel", command=hide_control_panel).pack(side="right", padx=(6, 0))
ttk.Button(top_frame, text="Quit Safely", command=restore_and_quit).pack(side="right", padx=(6, 0))

status_label = ttk.Label(control_panel, textvariable=panel_status_var, padding=(10, 0))
status_label.pack(fill="x")

notebook = ttk.Notebook(control_panel)
notebook.pack(fill="both", expand=True, padx=10, pady=10)


def create_scrollable_tab(book, title):
    outer = ttk.Frame(book)
    book.add(outer, text=title)

    tab_canvas = tk.Canvas(outer, borderwidth=0, highlightthickness=0)
    y_scrollbar = ttk.Scrollbar(outer, orient="vertical", command=tab_canvas.yview)
    x_scrollbar = ttk.Scrollbar(outer, orient="horizontal", command=tab_canvas.xview)
    tab_canvas.configure(
        yscrollcommand=y_scrollbar.set,
        xscrollcommand=x_scrollbar.set,
    )

    content = ttk.Frame(tab_canvas, padding=8)
    tab_canvas.create_window((0, 0), window=content, anchor="nw")

    def on_content_configure(_event):
        tab_canvas.configure(scrollregion=tab_canvas.bbox("all"))

    def on_mousewheel(event):
        # Hold Shift while scrolling to move horizontally.
        if event.state & 0x0001:
            tab_canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
        else:
            tab_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def bind_mousewheel(_event):
        tab_canvas.bind_all("<MouseWheel>", on_mousewheel)

    def unbind_mousewheel(_event):
        tab_canvas.unbind_all("<MouseWheel>")

    content.bind("<Configure>", on_content_configure)
    outer.bind("<Enter>", bind_mousewheel)
    outer.bind("<Leave>", unbind_mousewheel)

    y_scrollbar.pack(side="right", fill="y")
    x_scrollbar.pack(side="bottom", fill="x")
    tab_canvas.pack(side="left", fill="both", expand=True)

    return content

# Dashboard tab
dashboard_tab = create_scrollable_tab(notebook, "Dashboard")

quick = make_section(dashboard_tab, "Quick Controls")
ttk.Checkbutton(quick, text="Transparent System Cursor", variable=transparent_var, command=ui_toggle_transparent).grid(row=0, column=0, sticky="w", padx=8, pady=4)
ttk.Checkbutton(quick, text="Show Fake Cursors", variable=show_fake_var, command=ui_toggle_fake_cursors).grid(row=0, column=1, sticky="w", padx=8, pady=4)
ttk.Checkbutton(quick, text="Show Drawn-Real Cursor", variable=drawn_real_var, command=ui_toggle_drawn_real).grid(row=1, column=0, sticky="w", padx=8, pady=4)
ttk.Checkbutton(quick, text="Mirror Mode", variable=mirror_enabled_var, command=ui_toggle_mirror).grid(row=1, column=1, sticky="w", padx=8, pady=4)
ttk.Checkbutton(quick, text="Pause Swarm", variable=pause_var, command=ui_toggle_pause).grid(row=2, column=0, sticky="w", padx=8, pady=4)
ttk.Checkbutton(quick, text="Runtime HUD", variable=runtime_hud_var, command=ui_toggle_runtime_hud).grid(row=2, column=1, sticky="w", padx=8, pady=4)
ttk.Checkbutton(quick, text="Startup Help Text", variable=startup_help_var, command=ui_toggle_startup_help).grid(row=3, column=0, sticky="w", padx=8, pady=4)

quick_buttons = make_section(dashboard_tab, "Important Actions")
dashboard_panic_toggle_button = ttk.Button(quick_buttons, text="SAFE MODE / PANIC", command=panic_resume_toggle)
dashboard_panic_toggle_button.grid(row=0, column=0, padx=6, pady=6)
ttk.Button(quick_buttons, text="Resume Previous Mode", command=resume_previous_mode).grid(row=1, column=0, padx=6, pady=6)
ttk.Button(quick_buttons, text="Restore Cursor", command=ui_restore_cursor).grid(row=0, column=1, padx=6, pady=6)
ttk.Button(quick_buttons, text="Disable Mirror", command=ui_disable_mirror).grid(row=0, column=2, padx=6, pady=6)
ttk.Button(quick_buttons, text="Hide Panel", command=hide_control_panel).grid(row=0, column=3, padx=6, pady=6)

# Cursor tab
cursor_tab = create_scrollable_tab(notebook, "Cursor")

system_cursor_box = make_section(cursor_tab, "System Cursor")
ttk.Checkbutton(system_cursor_box, text="Transparent System Cursor", variable=transparent_var, command=ui_toggle_transparent).grid(row=0, column=0, sticky="w", padx=8, pady=4)
ttk.Button(system_cursor_box, text="Restore System Cursor", command=ui_restore_cursor).grid(row=0, column=1, padx=8, pady=4)
ttk.Button(system_cursor_box, text="Make Cursor Transparent", command=ui_make_transparent).grid(row=0, column=2, padx=8, pady=4)

drawn_box = make_section(cursor_tab, "Drawn-Real Cursor")
ttk.Checkbutton(drawn_box, text="Show Drawn-Real Cursor", variable=drawn_real_var, command=ui_toggle_drawn_real).grid(row=0, column=0, sticky="w", padx=8, pady=4)

ttk.Label(drawn_box, text="Manual Offset X:").grid(row=1, column=0, sticky="w", padx=8, pady=4)
tk.Spinbox(drawn_box, from_=-200, to=200, textvariable=manual_offset_x_var, width=8).grid(row=1, column=1, sticky="w", padx=8, pady=4)
ttk.Label(drawn_box, text="Manual Offset Y:").grid(row=2, column=0, sticky="w", padx=8, pady=4)
tk.Spinbox(drawn_box, from_=-200, to=200, textvariable=manual_offset_y_var, width=8).grid(row=2, column=1, sticky="w", padx=8, pady=4)

ttk.Label(drawn_box, text="Drawn Cursor Scale:").grid(row=3, column=0, sticky="w", padx=8, pady=4)
ttk.Scale(drawn_box, from_=0.50, to=1.50, variable=real_cursor_scale_var, command=lambda value: real_cursor_scale_label_var.set(f"{float(value):.2f}x"), orient="horizontal", length=240).grid(row=3, column=1, sticky="w", padx=8, pady=4)
ttk.Label(drawn_box, textvariable=real_cursor_scale_label_var).grid(row=3, column=2, sticky="w", padx=8, pady=4)

ttk.Button(drawn_box, text="Apply Cursor Settings", command=apply_cursor_polish_from_ui).grid(row=4, column=0, padx=8, pady=6)
ttk.Button(drawn_box, text="Reset Fields", command=reset_cursor_polish_fields_to_current).grid(row=4, column=1, padx=8, pady=6)

ttk.Label(drawn_box, text=f"Detected Hotspot: ({hotspot_x}, {hotspot_y})  |  Hold Shift = temporary hint").grid(row=5, column=0, columnspan=3, sticky="w", padx=8, pady=4)

nightmare_box = make_section(cursor_tab, "Nightmare Behavior")
ttk.Label(nightmare_box, text="Nightmare Mode:").grid(row=0, column=0, sticky="w", padx=8, pady=4)
nightmare_combo = ttk.Combobox(
    nightmare_box,
    textvariable=nightmare_mode_var,
    values=NIGHTMARE_MODE_OPTIONS,
    state="readonly",
    width=22,
)
nightmare_combo.grid(row=0, column=1, sticky="w", padx=8, pady=4)
ttk.Button(nightmare_box, text="Apply Mode", command=ui_apply_nightmare_mode).grid(row=0, column=2, padx=8, pady=4)
ttk.Button(nightmare_box, text="Disable Nightmare", command=ui_disable_nightmare_mode).grid(row=0, column=3, padx=8, pady=4)
ttk.Label(
    nightmare_box,
    text=(
        "Blind Mode: transparent cursor + no fake cursors + no drawn-real cursor.\n"
        "Fake-only Mode: fake cursors visible, but your drawn-real cursor is hidden.\n"
        "Flicker Hint Mode: fake-only base, with a brief real-cursor hint every few seconds.\n"
        "Hold Shift always temporarily shows the drawn-real cursor. Panic/Safe Mode disables Nightmare."
    ),
    justify="left",
).grid(row=1, column=0, columnspan=4, sticky="w", padx=8, pady=4)

# Mirror tab
mirror_tab = create_scrollable_tab(notebook, "Mirror")

mirror_box = make_section(mirror_tab, "Raw Input Mirror Mode")
ttk.Checkbutton(mirror_box, text="Mirror Enabled", variable=mirror_enabled_var, command=ui_toggle_mirror).grid(row=0, column=0, sticky="w", padx=8, pady=4)
ttk.Checkbutton(mirror_box, text="Mirror X", variable=mirror_x_var, command=ui_toggle_mirror_x).grid(row=1, column=0, sticky="w", padx=8, pady=4)
ttk.Checkbutton(mirror_box, text="Mirror Y", variable=mirror_y_var, command=ui_toggle_mirror_y).grid(row=1, column=1, sticky="w", padx=8, pady=4)
ttk.Label(mirror_box, text="Mirror Strength:").grid(row=2, column=0, sticky="w", padx=8, pady=8)
ttk.Scale(mirror_box, from_=0.25, to=2.0, variable=mirror_strength_var, command=ui_set_mirror_strength, orient="horizontal", length=260).grid(row=2, column=1, sticky="w", padx=8, pady=8)
ttk.Label(mirror_box, textvariable=mirror_strength_label_var).grid(row=2, column=2, sticky="w", padx=8, pady=8)
ttk.Button(mirror_box, text="Disable Mirror", command=ui_disable_mirror).grid(row=3, column=0, padx=8, pady=6)
ttk.Label(mirror_box, text="Hold Shift = temporary normal movement").grid(row=4, column=0, columnspan=3, sticky="w", padx=8, pady=4)

# Swarm tab
swarm_tab = create_scrollable_tab(notebook, "Swarm")

swarm_box = make_section(swarm_tab, "Swarm Controls")
ttk.Checkbutton(swarm_box, text="Show Fake Cursors", variable=show_fake_var, command=ui_toggle_fake_cursors).grid(row=0, column=0, sticky="w", padx=8, pady=4)
ttk.Checkbutton(swarm_box, text="Pause Swarm", variable=pause_var, command=ui_toggle_pause).grid(row=0, column=1, sticky="w", padx=8, pady=4)
ttk.Checkbutton(swarm_box, text="Randomize Draw Order", variable=randomize_draw_order_var, command=apply_swarm_settings_from_ui).grid(row=0, column=2, sticky="w", padx=8, pady=4)
ttk.Button(swarm_box, text="Resume Swarm", command=ui_resume_swarm).grid(row=1, column=0, padx=8, pady=6)
ttk.Button(swarm_box, text="Pause Swarm", command=ui_pause_swarm).grid(row=1, column=1, padx=8, pady=6)

density_box = make_section(swarm_tab, "Screen Density Preset")
ttk.Label(density_box, text="Screen Density:").grid(row=0, column=0, sticky="w", padx=8, pady=4)
density_combo = ttk.Combobox(
    density_box,
    textvariable=density_preset_var,
    values=["Custom"] + list(SCREEN_DENSITY_PRESETS.keys()),
    state="readonly",
    width=18,
)
density_combo.grid(row=0, column=1, sticky="w", padx=8, pady=4)
ttk.Button(density_box, text="Apply Density", command=apply_density_preset_from_ui).grid(row=0, column=2, padx=8, pady=4)
ttk.Label(density_box, text="Density spreads cursors globally across the whole screen, not around the real cursor.").grid(row=1, column=0, columnspan=3, sticky="w", padx=8, pady=4)

count_box = make_section(swarm_tab, "Editable Cursor Counts")
count_rows = [
    ("Static Cursors", static_count_var),
    ("Slow Clones", slow_count_var),
    ("Same-Speed Clones", same_count_var),
    ("Fast Clones", fast_count_var),
    ("Random Movers", random_count_var),
    ("Target Movers", target_count_var),
]

for index, (label_text, variable) in enumerate(count_rows):
    row = index // 2
    col = (index % 2) * 2
    ttk.Label(count_box, text=f"{label_text}:").grid(row=row, column=col, sticky="w", padx=8, pady=5)
    tk.Spinbox(count_box, from_=0, to=500, textvariable=variable, width=8).grid(row=row, column=col + 1, sticky="w", padx=8, pady=5)

ttk.Label(count_box, text="Movement Threshold:").grid(row=3, column=0, sticky="w", padx=8, pady=5)
tk.Spinbox(count_box, from_=0.0, to=10.0, increment=0.1, textvariable=movement_threshold_var, width=8).grid(row=3, column=1, sticky="w", padx=8, pady=5)
ttk.Label(count_box, text="Movement Randomness / Wobble:").grid(row=3, column=2, sticky="w", padx=8, pady=5)
ttk.Scale(count_box, from_=0.0, to=2.5, variable=fake_cursor_wobble_var, command=lambda value: fake_cursor_wobble_label_var.set(f"{float(value):.2f}x"), orient="horizontal", length=190).grid(row=3, column=3, sticky="w", padx=8, pady=5)
ttk.Label(count_box, textvariable=fake_cursor_wobble_label_var).grid(row=3, column=4, sticky="w", padx=8, pady=5)
ttk.Label(count_box, text="Higher threshold ignores tiny movement; higher wobble makes fake cursors less robotic.").grid(row=4, column=0, columnspan=5, sticky="w", padx=8, pady=4)

count_buttons = make_section(swarm_tab, "Apply / Reset")
ttk.Button(count_buttons, text="Apply Swarm Changes", command=apply_swarm_settings_from_ui).grid(row=0, column=0, padx=8, pady=6)
ttk.Button(count_buttons, text="Reset Fields to Current", command=reset_swarm_entries_to_current).grid(row=0, column=1, padx=8, pady=6)
ttk.Label(count_buttons, text="Applying count changes rebuilds the fake cursor swarm immediately.").grid(row=1, column=0, columnspan=2, sticky="w", padx=8, pady=4)

summary_box = make_section(swarm_tab, "Current Swarm Summary")
ttk.Label(summary_box, textvariable=swarm_summary_var, justify="left").pack(anchor="w", padx=8, pady=4)

# Presets tab
presets_tab = create_scrollable_tab(notebook, "Presets")

builtin_box = make_section(presets_tab, "Built-in Presets")
ttk.Label(builtin_box, text="Built-in preset:").grid(row=0, column=0, sticky="w", padx=8, pady=4)
builtin_combo = ttk.Combobox(
    builtin_box,
    textvariable=built_in_preset_var,
    values=list(BUILT_IN_PRESETS.keys()),
    state="readonly",
    width=24,
)
builtin_combo.grid(row=0, column=1, sticky="w", padx=8, pady=4)
builtin_combo.bind("<<ComboboxSelected>>", on_builtin_changed)
ttk.Button(builtin_box, text="Load Built-in", command=load_builtin_preset).grid(row=0, column=2, padx=8, pady=4)
ttk.Button(builtin_box, text="Preview", command=reset_builtin_preview).grid(row=0, column=3, padx=8, pady=4)
ttk.Label(builtin_box, textvariable=selected_builtin_preview_var, justify="left").grid(row=1, column=0, columnspan=4, sticky="w", padx=8, pady=8)

custom_box = make_section(presets_tab, "Custom Preset Slots")
ttk.Label(custom_box, text=f"Max custom presets: {MAX_CUSTOM_PRESETS}").grid(row=0, column=0, columnspan=4, sticky="w", padx=8, pady=4)
ttk.Label(custom_box, text="Preset slot:").grid(row=1, column=0, sticky="w", padx=8, pady=4)
custom_combo = ttk.Combobox(
    custom_box,
    textvariable=custom_preset_slot_var,
    values=preset_slot_display_values(),
    state="readonly",
    width=24,
)
custom_combo.grid(row=1, column=1, sticky="w", padx=8, pady=4)
custom_combo.bind("<<ComboboxSelected>>", on_custom_slot_changed)

ttk.Label(custom_box, text="Preset name:").grid(row=2, column=0, sticky="w", padx=8, pady=4)
ttk.Entry(custom_box, textvariable=custom_preset_name_var, width=32).grid(row=2, column=1, columnspan=2, sticky="w", padx=8, pady=4)

ttk.Button(custom_box, text="Load", command=load_custom_preset).grid(row=3, column=0, padx=6, pady=6)
ttk.Button(custom_box, text="Save Current", command=save_current_to_custom_slot).grid(row=3, column=1, padx=6, pady=6)
ttk.Button(custom_box, text="Rename", command=rename_custom_preset).grid(row=3, column=2, padx=6, pady=6)
ttk.Button(custom_box, text="Delete / Reset Slot", command=delete_custom_preset).grid(row=3, column=3, padx=6, pady=6)
ttk.Button(custom_box, text="Restore Saved Version", command=load_custom_preset).grid(row=4, column=0, columnspan=2, sticky="w", padx=6, pady=6)

ttk.Label(custom_box, text="Preset Preview:").grid(row=5, column=0, sticky="nw", padx=8, pady=(8, 4))
ttk.Label(custom_box, textvariable=custom_preset_preview_var, justify="left").grid(row=5, column=1, columnspan=3, sticky="w", padx=8, pady=(8, 4))

preset_io_box = make_section(presets_tab, "Import / Export Presets")
ttk.Button(preset_io_box, text="Export Selected Preset", command=export_selected_custom_preset).grid(row=0, column=0, padx=8, pady=6)
ttk.Button(preset_io_box, text="Import Into Selected Slot", command=import_selected_custom_preset).grid(row=0, column=1, padx=8, pady=6)
ttk.Button(preset_io_box, text="Export Full Backup", command=export_full_backup).grid(row=1, column=0, padx=8, pady=6)
ttk.Button(preset_io_box, text="Import Full Backup", command=import_full_backup).grid(row=1, column=1, padx=8, pady=6)
ttk.Button(preset_io_box, text="Reset All Custom Presets", command=reset_all_custom_presets).grid(row=2, column=0, padx=8, pady=6)
ttk.Label(
    preset_io_box,
    text="Full backup includes custom presets and app settings. Single preset import overwrites only the selected slot.",
    justify="left",
).grid(row=3, column=0, columnspan=3, sticky="w", padx=8, pady=4)

# Safety tab
safety_tab = create_scrollable_tab(notebook, "Safety")

panic_box = make_section(safety_tab, "Emergency Actions")
safety_panic_toggle_button = ttk.Button(panic_box, text="BIG SAFE MODE / PANIC", command=panic_resume_toggle)
safety_panic_toggle_button.grid(row=0, column=0, padx=8, pady=6)
ttk.Button(panic_box, text="Resume Previous Mode", command=resume_previous_mode).grid(row=2, column=0, padx=8, pady=6)
ttk.Button(panic_box, text="Restore Cursor", command=ui_restore_cursor).grid(row=0, column=1, padx=8, pady=6)
ttk.Button(panic_box, text="Disable Mirror", command=ui_disable_mirror).grid(row=0, column=2, padx=8, pady=6)
ttk.Button(panic_box, text="Show Drawn-Real", command=ui_show_drawn_real).grid(row=1, column=0, padx=8, pady=6)
ttk.Button(panic_box, text="Pause Swarm", command=ui_pause_swarm).grid(row=1, column=1, padx=8, pady=6)
ttk.Button(panic_box, text="Quit Safely", command=restore_and_quit).grid(row=1, column=2, padx=8, pady=6)

hotkey_box = make_section(safety_tab, "Hotkeys")
hotkey_text = (
    "Ctrl+Alt+Q = Quit safely\n"
    "Ctrl+Alt+R = Toggle system cursor visible/transparent\n"
    "Ctrl+Alt+M = Toggle Mirror Mode\n"
    "Ctrl+Alt+X/Y = Toggle Mirror axes\n"
    "Ctrl+Alt+P = Pause/unpause swarm\n"
    "Ctrl+Alt+H = Hide/show drawn-real cursor\n"
    "Ctrl+Alt+C = Show/hide control panel\n"
    "Ctrl+Alt+D = Show/hide runtime HUD\n"
    "Ctrl+Alt+Space = Panic / Resume Previous Mode\n"
    "Hold Shift = Temporary normal movement + cursor hint"
)
ttk.Label(hotkey_box, text=hotkey_text, justify="left").pack(anchor="w", padx=8, pady=4)

safety_options_box = make_section(safety_tab, "Display Options")
ttk.Checkbutton(safety_options_box, text="Show runtime HUD", variable=runtime_hud_var, command=ui_toggle_runtime_hud).grid(row=0, column=0, sticky="w", padx=8, pady=4)
ttk.Checkbutton(safety_options_box, text="Show startup help text", variable=startup_help_var, command=ui_toggle_startup_help).grid(row=1, column=0, sticky="w", padx=8, pady=4)

startup_box = make_section(safety_tab, "Startup / Recovery")
ttk.Label(startup_box, text="Startup Mode:").grid(row=0, column=0, sticky="w", padx=8, pady=4)
startup_mode_combo = ttk.Combobox(
    startup_box,
    textvariable=startup_mode_var,
    values=STARTUP_MODE_OPTIONS,
    state="readonly",
    width=22,
)
startup_mode_combo.grid(row=0, column=1, sticky="w", padx=8, pady=4)

ttk.Label(startup_box, text="Built-in Startup Preset:").grid(row=1, column=0, sticky="w", padx=8, pady=4)
startup_builtin_combo = ttk.Combobox(
    startup_box,
    textvariable=startup_builtin_var,
    values=list(BUILT_IN_PRESETS.keys()),
    state="readonly",
    width=22,
)
startup_builtin_combo.grid(row=1, column=1, sticky="w", padx=8, pady=4)

ttk.Label(startup_box, text="Custom Startup Slot:").grid(row=2, column=0, sticky="w", padx=8, pady=4)
startup_custom_combo = ttk.Combobox(
    startup_box,
    textvariable=startup_custom_slot_var,
    values=preset_slot_display_values(),
    state="readonly",
    width=22,
)
startup_custom_combo.grid(row=2, column=1, sticky="w", padx=8, pady=4)

ttk.Button(startup_box, text="Save Startup Settings", command=ui_save_startup_settings).grid(row=3, column=0, padx=8, pady=6)
ttk.Button(startup_box, text="Apply Startup Mode Now", command=ui_apply_startup_now).grid(row=3, column=1, padx=8, pady=6)
ttk.Button(startup_box, text="Generate Fallback Restore Script", command=generate_emergency_restore_script).grid(row=4, column=0, columnspan=2, sticky="w", padx=8, pady=6)
ttk.Label(
    startup_box,
    text="Safe Mode starts with the Windows cursor visible, mirror disabled, and swarm paused.\nLast Used State is saved when you quit safely.",
    justify="left",
).grid(row=5, column=0, columnspan=3, sticky="w", padx=8, pady=4)

# Advanced tab
advanced_tab = create_scrollable_tab(notebook, "Advanced")

advanced_box = make_section(advanced_tab, "Debug Info")
advanced_info_var = tk.StringVar(value="Debug info will update while the app is running.")
ttk.Label(advanced_box, textvariable=advanced_info_var, justify="left").pack(anchor="w", padx=8, pady=4)

about_box = make_section(advanced_tab, "App Info / About")
about_text = (
    f"Cursor Swarm {APP_VERSION}\n"
    "Certification-fix build with visible startup Control Panel, floating CS control button, shortcut hints, standalone recovery EXE support, privacy/terms documents, and Store packaging polish.\n\n"
    "Main hotkeys:\n"
    "Ctrl+Alt+C = Control Panel\n"
    "Ctrl+Alt+Space = Safe Mode / Resume\n"
    "Ctrl+Alt+Q = Quit Safely\n\n"
    "Privacy summary: CursorSwarm stores settings locally and does not collect, upload, sell, or share personal data.\n\n"
    f"Preset file: {PRESET_FILE}\n"
    f"Settings file: {SETTINGS_FILE}\n"
    f"Emergency restore EXE: {RESTORE_EXE_FILE}\n"
    f"Fallback restore script: {RESTORE_SCRIPT_FILE}\n"
    f"README file: {README_FILE}\n"
    f"Privacy policy: {PRIVACY_POLICY_FILE}\n"
    f"Terms / Safety: {TERMS_SAFETY_FILE}\n"
    f"Release notes: {RELEASE_NOTES_FILE}"
)
ttk.Label(about_box, text=about_text, justify="left").pack(anchor="w", padx=8, pady=4)

config_box = make_section(advanced_tab, "Config / Backup")
ttk.Label(
    config_box,
    text=f"Preset file: {PRESET_FILE}\nSettings file: {SETTINGS_FILE}\nEmergency restore EXE: {RESTORE_EXE_FILE}\nFallback restore script: {RESTORE_SCRIPT_FILE}\nREADME file: {README_FILE}\nPrivacy policy: {PRIVACY_POLICY_FILE}\nTerms / Safety: {TERMS_SAFETY_FILE}\nRelease notes: {RELEASE_NOTES_FILE}",
    justify="left",
).grid(row=0, column=0, columnspan=3, sticky="w", padx=8, pady=4)
ttk.Button(config_box, text="Export Full Backup", command=export_full_backup).grid(row=1, column=0, padx=8, pady=6)
ttk.Button(config_box, text="Import Full Backup", command=import_full_backup).grid(row=1, column=1, padx=8, pady=6)
ttk.Button(config_box, text="Reset App Settings", command=reset_app_settings_to_default).grid(row=2, column=0, padx=8, pady=6)
ttk.Button(config_box, text="Reset Custom Presets", command=reset_all_custom_presets).grid(row=2, column=1, padx=8, pady=6)
ttk.Button(config_box, text="Generate Fallback Restore Script", command=generate_emergency_restore_script).grid(row=3, column=0, sticky="w", padx=8, pady=6)
ttk.Button(config_box, text="Create README", command=generate_readme_file).grid(row=3, column=1, sticky="w", padx=8, pady=6)
ttk.Button(config_box, text="Create Privacy Policy", command=generate_privacy_policy_file).grid(row=4, column=0, sticky="w", padx=8, pady=6)
ttk.Button(config_box, text="Create Terms/Safety", command=generate_terms_safety_file).grid(row=4, column=1, sticky="w", padx=8, pady=6)
ttk.Button(config_box, text="Create Release Notes", command=generate_release_notes_file).grid(row=4, column=2, sticky="w", padx=8, pady=6)

# Bottom action bar
bottom_frame = ttk.Frame(control_panel, padding=(10, 0, 10, 10))
bottom_frame.pack(fill="x")
ttk.Button(bottom_frame, text="Apply Changes", command=apply_all_changes).pack(side="left", padx=(0, 6))
ttk.Button(bottom_frame, text="Restore Preset", command=load_custom_preset).pack(side="left", padx=6)
bottom_panic_toggle_button = ttk.Button(bottom_frame, text="Safe Mode", command=panic_resume_toggle)
bottom_panic_toggle_button.pack(side="left", padx=6)
ttk.Button(bottom_frame, text="Resume Previous", command=resume_previous_mode).pack(side="left", padx=6)
ttk.Button(bottom_frame, text="Hide Panel", command=hide_control_panel).pack(side="right", padx=6)
ttk.Button(bottom_frame, text="Quit Safely", command=restore_and_quit).pack(side="right", padx=6)

refresh_swarm_summary()
update_panic_button_labels()
control_panel.withdraw()

# Auto-create/update helper files before any cursed startup mode runs.
ensure_emergency_restore_script()
ensure_readme_file()
ensure_release_documents()

# Apply startup mode after all setup succeeds. Fall back to Safe Mode on failure.
apply_startup_mode_safely()

# Certification/user-friendly startup: show the main Control Panel immediately
# so the app never appears invisible or impossible to control.
# The floating CS button appears only when the Control Panel is hidden.
create_floating_control_bubble()
show_control_panel()


# -----------------------------
# Main loop
# -----------------------------
def update():
    global last_time, prev_real_x, prev_real_y
    global manual_offset_x, manual_offset_y
    global last_adjust_time, last_toggle_time
    global MIRROR_ENABLED, MIRROR_X, MIRROR_Y
    global swarm_paused, show_fake_cursors, show_drawn_real_cursor
    global control_panel_visible, last_panel_toggle_time
    global panel_hint_text, panel_hint_until
    global runtime_hud_visible, last_hud_toggle_time

    now = time.time()
    dt = now - last_time
    last_time = now

    dt = min(dt, 0.035)

    real_x, real_y = get_mouse_position()

    real_dx = real_x - prev_real_x
    real_dy = real_y - prev_real_y

    real_distance = math.hypot(real_dx, real_dy)
    moving = real_distance > MOVE_DISTANCE_THRESHOLD

    prev_real_x = real_x
    prev_real_y = real_y

    ctrl_alt = ctrl_alt_down()

    # Edge-triggered hotkeys:
    # These fire only once per key press instead of repeatedly while held.
    # This makes Ctrl + Alt + Space behave like a proper Panic/Resume toggle
    # and keeps UI checkboxes synced after shortcut changes.
    if hotkey_pressed("ctrl_alt_q", ctrl_alt and key_down(VK_Q)):
        restore_and_quit()
        return

    if hotkey_pressed("ctrl_alt_r", ctrl_alt and key_down(VK_R)):
        if transparent_active:
            set_visible_mode()
        else:
            set_transparent_mode()
        sync_ui_vars()

    if hotkey_pressed("ctrl_alt_m", ctrl_alt and key_down(VK_M)):
        MIRROR_ENABLED = not MIRROR_ENABLED
        globals()["virtual_x"], globals()["virtual_y"] = get_mouse_position()
        sync_ui_vars()

    if hotkey_pressed("ctrl_alt_x", ctrl_alt and key_down(VK_X)):
        MIRROR_X = not MIRROR_X
        globals()["virtual_x"], globals()["virtual_y"] = get_mouse_position()
        sync_ui_vars()

    if hotkey_pressed("ctrl_alt_y", ctrl_alt and key_down(VK_Y)):
        MIRROR_Y = not MIRROR_Y
        globals()["virtual_x"], globals()["virtual_y"] = get_mouse_position()
        sync_ui_vars()

    if hotkey_pressed("ctrl_alt_p", ctrl_alt and key_down(VK_P)):
        swarm_paused = not swarm_paused
        sync_ui_vars()

    if hotkey_pressed("ctrl_alt_h", ctrl_alt and key_down(VK_H)):
        show_drawn_real_cursor = not show_drawn_real_cursor
        sync_ui_vars()

    if hotkey_pressed("ctrl_alt_c", ctrl_alt and key_down(VK_C)):
        toggle_control_panel()

    if hotkey_pressed("ctrl_alt_d", ctrl_alt and key_down(VK_D)):
        toggle_runtime_hud()
        sync_ui_vars()

    if hotkey_pressed("ctrl_alt_space", ctrl_alt and key_down(VK_SPACE)):
        panic_resume_toggle()

    if ctrl_alt and now - last_adjust_time > 0.08:
        if key_down(VK_LEFT):
            manual_offset_x -= 1
            last_adjust_time = now
            set_cursor_polish_vars_from_globals()
        elif key_down(VK_RIGHT):
            manual_offset_x += 1
            last_adjust_time = now
            set_cursor_polish_vars_from_globals()
        elif key_down(VK_UP):
            manual_offset_y -= 1
            last_adjust_time = now
            set_cursor_polish_vars_from_globals()
        elif key_down(VK_DOWN):
            manual_offset_y += 1
            last_adjust_time = now
            set_cursor_polish_vars_from_globals()

    if AUTO_RESTORE_SECONDS is not None and transparent_active and transparent_started_at is not None:
        elapsed = now - transparent_started_at

        if elapsed >= AUTO_RESTORE_SECONDS:
            set_visible_mode()
            sync_ui_vars()

    canvas.delete("all")

    draw_items = []

    effective_show_fake_cursors = show_fake_cursors and nightmare_mode != "Blind Mode"

    if effective_show_fake_cursors and not swarm_paused:
        for cursor in fake_cursors:
            cursor.update(moving, real_dx, real_dy, dt)
            draw_items.append((cursor.x, cursor.y, cursor.scale))

    # Drawn-real cursor
    # Ctrl + Alt + H toggles this.
    # Hold Shift temporarily shows it for safety/hint mode.
    flicker_hint_active = (
        nightmare_mode == "Flicker Hint Mode"
        and ((now - start_time) % NIGHTMARE_FLICKER_INTERVAL) < NIGHTMARE_FLICKER_DURATION
    )
    should_draw_real_cursor = (
        key_down(VK_SHIFT)
        or flicker_hint_active
        or (nightmare_mode == "Disabled" and show_drawn_real_cursor)
    )

    if should_draw_real_cursor:
        real_draw_x = real_x - (hotspot_x * REAL_DRAWN_CURSOR_SCALE) + manual_offset_x
        real_draw_y = real_y - (hotspot_y * REAL_DRAWN_CURSOR_SCALE) + manual_offset_y

        draw_items.append((real_draw_x, real_draw_y, REAL_DRAWN_CURSOR_SCALE))

    if RANDOMIZE_DRAW_ORDER:
        random.shuffle(draw_items)

    for x, y, scale in draw_items:
        draw_cursor_image(x, y, scale)

    mirror_text = "ON" if MIRROR_ENABLED else "OFF"
    transparent_text = "TRANSPARENT" if transparent_active else "VISIBLE"
    pause_text = "PAUSED" if swarm_paused else "RUNNING"
    drawn_real_text = "VISIBLE" if show_drawn_real_cursor else "HIDDEN"
    fake_text = "VISIBLE" if show_fake_cursors else "HIDDEN"
    nightmare_text = nightmare_mode if nightmare_mode != "Disabled" else "OFF"

    if show_startup_help and now - start_time < 10:
        canvas.create_text(
            SCREEN_W // 2,
            35,
            text="CursorSwarm v10.9 — Ctrl+Alt+C panel | Ctrl+Alt+Space Safe Mode | Ctrl+Alt+Q Quit Safely",
            fill="white",
            font=("Arial", 16, "bold")
        )

    if show_startup_help and now - start_time < 25:
        canvas.create_text(
            SCREEN_W // 2,
            65,
            text=f"Mirror:{mirror_text} | X:{MIRROR_X} Y:{MIRROR_Y} | Cursor:{transparent_text} | RealDrawn:{drawn_real_text} | Swarm:{pause_text} | Nightmare:{nightmare_text}",
            fill="white",
            font=("Arial", 13)
        )

    if panel_hint_text and now < panel_hint_until:
        # Full-width banner prevents the hint text from spilling onto the
        # transparent magenta overlay background on smaller screens.
        # This keeps the hint readable and avoids pink/black color artifacts.
        hint_margin = 24
        hint_x1 = hint_margin
        hint_y1 = SCREEN_H - 102
        hint_x2 = SCREEN_W - hint_margin
        hint_y2 = hint_y1 + 48
        hint_center_x = SCREEN_W // 2
        hint_center_y = hint_y1 + 24

        canvas.create_rectangle(
            hint_x1,
            hint_y1,
            hint_x2,
            hint_y2,
            fill="#101010",
            outline="#101010",
        )
        canvas.create_text(
            hint_center_x + 1,
            hint_center_y + 1,
            text=panel_hint_text,
            fill="#000000",
            font=("Arial", 13, "bold"),
        )
        canvas.create_text(
            hint_center_x,
            hint_center_y,
            text=panel_hint_text,
            fill="#ffffff",
            font=("Arial", 13, "bold"),
        )
    elif panel_hint_until and now >= panel_hint_until:
        clear_control_panel_hint()

    if runtime_hud_visible:
        hud_text = (
            f"Preset: {CURRENT_PRESET_NAME} | Cursor: {transparent_text} | "
            f"Mirror: {mirror_text} | Swarm: {pause_text} | "
            f"Fake: {fake_text} | RealDrawn: {drawn_real_text} | Nightmare: {nightmare_text}"
        )
        canvas.create_rectangle(12, 12, 12 + min(1180, max(520, len(hud_text) * 7)), 44, fill="#111111", outline="white")
        canvas.create_text(22, 28, text=hud_text, fill="white", font=("Consolas", 11), anchor="w")

    if floating_control_bubble is not None:
        try:
            floating_control_bubble.attributes("-topmost", True)
        except Exception:
            pass

    update_panel_status()
    advanced_info_var.set(
        f"Raw events: {raw_event_count}\\n"
        f"Absolute/Ignored: {absolute_event_count}\\n"
        f"Detected hotspot: ({hotspot_x}, {hotspot_y})\\n"
        f"Manual offset: ({manual_offset_x}, {manual_offset_y})\\n"
        f"Real drawn cursor scale: {REAL_DRAWN_CURSOR_SCALE:.2f}x\\n"
        f"Fake cursor wobble: {FAKE_CURSOR_WOBBLE:.2f}x\\n"
        f"Transparent active: {transparent_active}\\n"
        f"Cursor backups: {len(cursor_backups)}\\n"
        f"Mirror virtual position: ({int(virtual_x)}, {int(virtual_y)})\\n"
        f"Runtime HUD visible: {runtime_hud_visible}\\n"
        f"Startup help text: {show_startup_help}\\n"
        f"Startup mode: {app_settings.get('startup_mode', 'Safe Mode')}\\n"
        f"Settings file: {SETTINGS_FILE}\\n"
        f"Panic state saved: {pre_panic_state is not None}\\n"
        f"Fake cursor total: {total_fake_cursor_count()}\\n"
        f"Counts: static {STATIC_COUNT}, slow {SLOW_CLONE_COUNT}, same {SAME_SPEED_CLONE_COUNT}, fast {FAST_CLONE_COUNT}, random {RANDOM_MOVER_COUNT}, target {TARGET_MOVER_COUNT}\\n"
        f"Movement threshold: {MOVE_DISTANCE_THRESHOLD:.2f}\\n"
        f"Nightmare mode: {nightmare_mode}"
    )

    root.after(16, update)

try:
    update()
    root.mainloop()
finally:
    restore_cursors_safely()