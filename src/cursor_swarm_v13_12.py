import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import customtkinter as ctk
import json
import os
import sys
from pathlib import Path
import random
import math
import time
import ctypes
import atexit
import traceback
import io
import struct
from ctypes import wintypes
from PIL import Image, ImageTk, ImageFilter, ImageDraw

try:
    import winreg
except Exception:
    winreg = None

# -----------------------------
# V11 SETTINGS
# -----------------------------
APP_VERSION = "v13.12"
CURRENT_PRESET_NAME = "Legacy v8.1"
MAX_CUSTOM_PRESETS = 10
MAX_CUSTOM_THEMES = 10
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
THEME_FILE = APP_DIR / "cursor_themes.json"
COLOR_PRESET_FILE = APP_DIR / "cursor_color_presets.json"
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

# Cursor Lab settings (v12.9.9)
FAKE_CURSOR_SCALE_MULTIPLIER = 1.00
CURSOR_TINT_ENABLED = False
CURSOR_TINT_STYLE = "Single Colour"
CURSOR_TINT_MULTI_PRESET = "Cyberpunk Neon"
CURSOR_TINT_STYLE_OPTIONS = ["Single Colour", "Multi-Colour Neon Preset"]
CURSOR_TINT_COLOR = "#8b5cf6"
CURSOR_TINT_STRENGTH = 0.65
CURSOR_TINT_BRIGHT_NEON = False
CURSOR_TINT_NEON_BRIGHTNESS = 1.20
CURSOR_TINT_BLACK_OUTLINE = False
CURSOR_TINT_OUTLINE_THICKNESS = 2
CURSOR_TINT_APPLY_DRAWN = True
CURSOR_TINT_APPLY_FAKE = True
CUSTOM_CURSOR_ENABLED = False
CUSTOM_CURSOR_IMAGE_PATH = ""
CUSTOM_CURSOR_HOTSPOT_MODE = "Top-left"
CUSTOM_CURSOR_SOURCE_LABEL = "System cursor"
CUSTOM_CURSOR_MAX_SIDE = 128

CURSOR_SHAPE_MODE = "Captured System Cursor"
CURSOR_SHAPE_OPTIONS = [
    "Captured System Cursor",
    "Arrow",
    "Hand",
    "I-Beam",
    "Crosshair",
    "Size Left-Right",
    "Size Up-Down",
    "Size Diagonal NW-SE",
    "Size Diagonal NE-SW",
    "Size All",
    "Working in Background",
    "Busy / Loading",
    "Custom Image File",
]
CURSOR_SHAPE_CURSOR_IDS = {
    "Arrow": 32512,
    "I-Beam": 32513,
    "Busy / Loading": 32514,
    "Crosshair": 32515,
    "Size Diagonal NW-SE": 32642,
    "Size Diagonal NE-SW": 32643,
    "Size Left-Right": 32644,
    "Size Up-Down": 32645,
    "Size All": 32646,
    "Hand": 32649,
    "Working in Background": 32650,
}
CURSOR_SHAPE_ANIMATED = {"Working in Background", "Busy / Loading"}
CURSOR_ANIMATION_SPEED = 0.09
CURSOR_USE_REAL_WINDOWS_ANI = True
CURSOR_ANIMATION_SPEED_MODE = "Normal"
CURSOR_ANIMATION_SPEED_OPTIONS = ["Slow", "Normal", "Fast"]
CURSOR_ANIMATION_SPEED_FACTORS = {
    "Slow": 1.55,
    "Normal": 1.00,
    "Fast": 0.65,
}
current_cursor_animation_frame_index = 0
ANI_CURSOR_CACHE = {}
SYSTEM_ANI_PATH_CACHE = {}
ANI_CURSOR_MAX_SIDE = 48

IDLE_EFFECT_ENABLED = False
IDLE_EFFECT_STYLE = "Disabled"
IDLE_EFFECT_DELAY = 1.20
IDLE_EFFECT_STRENGTH = 0.55
IDLE_EFFECT_NEON_ENABLED = True
IDLE_EFFECT_NEON_PRESET = "Cyberpunk Neon"
IDLE_EFFECT_NEON_COLOR = "#ff4fd8"
IDLE_EFFECT_OPTIONS = ["Disabled", "Pulse", "Glow Ring", "Fade", "Wobble"]
NEON_COLOR_PRESETS = {
    # v12.9: presets are intentionally more distinct. Toxic Plasma was kept
    # close to the version that tested well; Lava/Electric/Cyberpunk were made
    # more intense and less similar to Vaporwave/Royal Glitch.
    "Cyberpunk Neon": ["#00f5ff", "#ff00ff", "#fff200"],
    "Aurora Neon": ["#00ffb3", "#22d3ee", "#7c3cff"],
    "Vaporwave Neon": ["#ff71ce", "#b967ff", "#01cdfe"],
    "Toxic Plasma": ["#39ff14", "#faff00", "#22d3ee"],
    "Lava Circuit": ["#ff003c", "#ff6a00", "#ffe600"],
    "Electric Ice": ["#00f5ff", "#0077ff", "#b8ffff"],
    "Royal Glitch": ["#7c3cff", "#2d00ff", "#ff00aa"],
}

BUILTIN_NEON_COLOR_PRESETS = {name: list(colors) for name, colors in NEON_COLOR_PRESETS.items()}
MAX_CUSTOM_MULTI_COLOUR_PRESETS = 10


def sanitize_multi_colour_list(colors):
    clean = []
    if isinstance(colors, (list, tuple)):
        for color in colors[:3]:
            try:
                clean.append(sanitize_neon_color(color))
            except Exception:
                pass
    while len(clean) < 3:
        clean.append(["#22d3ee", "#8b5cf6", "#ff4fd8"][len(clean)])
    return clean[:3]


def default_custom_multi_colour_presets():
    presets = {}
    starters = [
        ("Custom Aurora", ["#00ffb3", "#22d3ee", "#8b5cf6"]),
        ("Custom Fire Ice", ["#ff3b30", "#ffd166", "#22d3ee"]),
        ("Custom Galaxy", ["#7c3cff", "#ff4fd8", "#22d3ee"]),
    ]
    for i in range(1, MAX_CUSTOM_MULTI_COLOUR_PRESETS + 1):
        key = f"Custom Multi {i}"
        if i <= len(starters):
            display_name, colors = starters[i - 1]
            enabled = True
        else:
            display_name, colors, enabled = f"Custom Multi {i}", ["#22d3ee", "#8b5cf6", "#ff4fd8"], False
        presets[key] = {
            "display_name": display_name,
            "colors": sanitize_multi_colour_list(colors),
            "enabled": bool(enabled),
        }
    return presets


def load_custom_multi_colour_presets():
    defaults = default_custom_multi_colour_presets()
    if not COLOR_PRESET_FILE.exists():
        try:
            write_json_file_safely(COLOR_PRESET_FILE, {"version": APP_VERSION, "custom_multi_colour_presets": defaults})
        except Exception:
            pass
        return defaults
    data = read_json_file_safely(COLOR_PRESET_FILE, default_value=None, backup_broken=True)
    raw = data.get("custom_multi_colour_presets", data) if isinstance(data, dict) else {}
    presets = defaults
    if isinstance(raw, dict):
        for key, cfg in raw.items():
            if key not in presets or not isinstance(cfg, dict):
                continue
            merged = dict(presets[key])
            merged.update(cfg)
            merged["display_name"] = str(merged.get("display_name", key)).strip() or key
            merged["colors"] = sanitize_multi_colour_list(merged.get("colors"))
            merged["enabled"] = bool(merged.get("enabled", True))
            presets[key] = merged
    return presets


def save_custom_multi_colour_presets(presets=None):
    presets = presets if presets is not None else custom_multi_colour_presets
    payload = {
        "version": APP_VERSION,
        "max_custom_multi_colour_presets": MAX_CUSTOM_MULTI_COLOUR_PRESETS,
        "custom_multi_colour_presets": presets,
    }
    write_json_file_safely(COLOR_PRESET_FILE, payload)


def rebuild_neon_color_presets():
    NEON_COLOR_PRESETS.clear()
    for name, colors in BUILTIN_NEON_COLOR_PRESETS.items():
        NEON_COLOR_PRESETS[name] = list(colors)
    for key, cfg in custom_multi_colour_presets.items():
        if not isinstance(cfg, dict) or not cfg.get("enabled", False):
            continue
        display_name = str(cfg.get("display_name", key)).strip() or key
        preset_name = display_name if display_name not in NEON_COLOR_PRESETS else f"Custom: {display_name}"
        NEON_COLOR_PRESETS[preset_name] = sanitize_multi_colour_list(cfg.get("colors"))


def stable_neon_preset_name(value, fallback="Cyberpunk Neon"):
    value = str(value or "").strip()
    if value in NEON_COLOR_PRESETS:
        return value
    if fallback in NEON_COLOR_PRESETS:
        return fallback
    return next(iter(NEON_COLOR_PRESETS.keys()), "Cyberpunk Neon")


# Cursor Lab pending/staged state.
# v12.1 safety rule: editing Cursor Lab controls must not affect the active
# cursor until the user clicks Apply Cursor Lab.
PENDING_CUSTOM_CURSOR_IMAGE = None
PENDING_CUSTOM_CURSOR_IMAGE_PATH = ""
PENDING_CUSTOM_CURSOR_SOURCE_LABEL = ""
PENDING_RESET_TO_SYSTEM_CURSOR = False
CURSOR_LAB_DIRTY = False

RANDOMIZE_DRAW_ORDER = True
AUTO_RESTORE_SECONDS = None

# Performance / Battery settings (v12.9.9)
PERFORMANCE_MODE_OPTIONS = [
    "Smooth (60 FPS)",
    "Balanced (45 FPS)",
    "Battery Saver (30 FPS)",
    "Custom",
]
PERFORMANCE_MODE = "Smooth (60 FPS)"
PERFORMANCE_TARGET_FPS = 60
PERFORMANCE_REDUCE_GLOW_QUALITY = False
PERFORMANCE_PAUSE_SWARM_ON_LONG_IDLE = False
PERFORMANCE_PAUSE_IDLE_EFFECTS_ON_LONG_IDLE = False
PERFORMANCE_LONG_IDLE_SECONDS = 60.0
# Separate timer for Performance long-idle detection. This uses a stronger
# movement threshold than the normal cursor movement code so tiny mouse/sensor
# jitter does not keep resetting the long-idle timer forever.
performance_last_real_motion_time = time.time()
performance_long_idle_is_active = False

# Movement Effects settings (v13.9)
MOVEMENT_EFFECTS_ENABLED = False
# Kept for backward compatibility with older configs, but v13.9 uses individual checkboxes.
MOVEMENT_EFFECT_STYLE = "Motion Trail"
MOVEMENT_EFFECT_STYLE_OPTIONS = ["Disabled", "Motion Trail", "Speed Glow", "Motion Trail + Speed Glow"]
MOVEMENT_MOTION_TRAIL_ENABLED = True
MOVEMENT_SPEED_GLOW_ENABLED = False
MOVEMENT_MOTION_STREAK_ENABLED = False
MOVEMENT_SPARK_PARTICLES_ENABLED = False
MOVEMENT_RIPPLE_BURST_ENABLED = False
MOVEMENT_COMET_TAIL_ENABLED = False
MOVEMENT_SPEED_LINES_ENABLED = False
MOVEMENT_MAGNETIC_ORBIT_ENABLED = False
CLICK_EFFECTS_ENABLED = False
CLICK_EFFECT_LEFT_ENABLED = True
CLICK_EFFECT_RIGHT_ENABLED = True
CLICK_EFFECT_STYLE = "Ripple + Sparks"
CLICK_EFFECT_STYLE_OPTIONS = ["Ripple", "Burst Ring", "Sparks", "Ripple + Sparks"]
MOVEMENT_COLOR_MODE_OPTIONS = ["Cursor Lab Colors", "Custom Color", "Single Colour Preset", "Multi-Colour Neon Preset"]
MOVEMENT_SINGLE_COLOR_PRESETS = {
    "Purple Neon": "#8b5cf6",
    "Cyan Neon": "#22d3ee",
    "Electric Blue": "#3b82f6",
    "Toxic Green": "#39ff14",
    "Hot Pink": "#ff4fd8",
    "Lava Red": "#ff3b30",
    "Gold Neon": "#ffd166",
    "White Ice": "#dff7ff",
}
MOVEMENT_DEFAULT_COLOR_MODE = "Cursor Lab Colors"
MOVEMENT_DEFAULT_CUSTOM_COLOR = "#22d3ee"
MOVEMENT_DEFAULT_SINGLE_PRESET = "Cyan Neon"
MOVEMENT_DEFAULT_NEON_PRESET = "Cyberpunk Neon"
MOTION_TRAIL_COLOR_MODE = MOVEMENT_DEFAULT_COLOR_MODE
MOTION_TRAIL_CUSTOM_COLOR = MOVEMENT_DEFAULT_CUSTOM_COLOR
MOTION_TRAIL_SINGLE_PRESET = MOVEMENT_DEFAULT_SINGLE_PRESET
MOTION_TRAIL_NEON_PRESET = MOVEMENT_DEFAULT_NEON_PRESET
SPEED_GLOW_COLOR_MODE = MOVEMENT_DEFAULT_COLOR_MODE
SPEED_GLOW_CUSTOM_COLOR = MOVEMENT_DEFAULT_CUSTOM_COLOR
SPEED_GLOW_SINGLE_PRESET = MOVEMENT_DEFAULT_SINGLE_PRESET
SPEED_GLOW_NEON_PRESET = MOVEMENT_DEFAULT_NEON_PRESET
MOTION_STREAK_COLOR_MODE = MOVEMENT_DEFAULT_COLOR_MODE
MOTION_STREAK_CUSTOM_COLOR = MOVEMENT_DEFAULT_CUSTOM_COLOR
MOTION_STREAK_SINGLE_PRESET = MOVEMENT_DEFAULT_SINGLE_PRESET
MOTION_STREAK_NEON_PRESET = MOVEMENT_DEFAULT_NEON_PRESET
SPARK_PARTICLE_COLOR_MODE = MOVEMENT_DEFAULT_COLOR_MODE
SPARK_PARTICLE_CUSTOM_COLOR = MOVEMENT_DEFAULT_CUSTOM_COLOR
SPARK_PARTICLE_SINGLE_PRESET = MOVEMENT_DEFAULT_SINGLE_PRESET
SPARK_PARTICLE_NEON_PRESET = MOVEMENT_DEFAULT_NEON_PRESET
RIPPLE_BURST_COLOR_MODE = MOVEMENT_DEFAULT_COLOR_MODE
RIPPLE_BURST_CUSTOM_COLOR = MOVEMENT_DEFAULT_CUSTOM_COLOR
RIPPLE_BURST_SINGLE_PRESET = MOVEMENT_DEFAULT_SINGLE_PRESET
RIPPLE_BURST_NEON_PRESET = MOVEMENT_DEFAULT_NEON_PRESET
COMET_TAIL_COLOR_MODE = MOVEMENT_DEFAULT_COLOR_MODE
COMET_TAIL_CUSTOM_COLOR = MOVEMENT_DEFAULT_CUSTOM_COLOR
COMET_TAIL_SINGLE_PRESET = MOVEMENT_DEFAULT_SINGLE_PRESET
COMET_TAIL_NEON_PRESET = MOVEMENT_DEFAULT_NEON_PRESET
SPEED_LINES_COLOR_MODE = MOVEMENT_DEFAULT_COLOR_MODE
SPEED_LINES_CUSTOM_COLOR = MOVEMENT_DEFAULT_CUSTOM_COLOR
SPEED_LINES_SINGLE_PRESET = MOVEMENT_DEFAULT_SINGLE_PRESET
SPEED_LINES_NEON_PRESET = MOVEMENT_DEFAULT_NEON_PRESET
MAGNETIC_ORBIT_COLOR_MODE = MOVEMENT_DEFAULT_COLOR_MODE
MAGNETIC_ORBIT_CUSTOM_COLOR = MOVEMENT_DEFAULT_CUSTOM_COLOR
MAGNETIC_ORBIT_SINGLE_PRESET = MOVEMENT_DEFAULT_SINGLE_PRESET
MAGNETIC_ORBIT_NEON_PRESET = MOVEMENT_DEFAULT_NEON_PRESET
CLICK_EFFECT_COLOR_MODE = MOVEMENT_DEFAULT_COLOR_MODE
CLICK_EFFECT_CUSTOM_COLOR = MOVEMENT_DEFAULT_CUSTOM_COLOR
CLICK_EFFECT_SINGLE_PRESET = MOVEMENT_DEFAULT_SINGLE_PRESET
CLICK_EFFECT_NEON_PRESET = MOVEMENT_DEFAULT_NEON_PRESET
MOTION_TRAIL_LENGTH = 12
MOTION_TRAIL_FADE_STRENGTH = 0.65
MOTION_TRAIL_MIN_DISTANCE = 2.0
SPEED_GLOW_STRENGTH = 0.65
SPEED_GLOW_THRESHOLD = 900.0
MOTION_STREAK_STRENGTH = 0.65
MOTION_STREAK_THRESHOLD = 750.0
MOTION_STREAK_LENGTH = 72
SPARK_PARTICLE_STRENGTH = 0.70
SPARK_PARTICLE_THRESHOLD = 450.0
SPARK_PARTICLE_AMOUNT = 4
SPARK_PARTICLE_SIZE = 4
SPARK_PARTICLE_LIFETIME = 0.60
RIPPLE_BURST_STRENGTH = 0.70
RIPPLE_BURST_THRESHOLD = 650.0
RIPPLE_BURST_LIFETIME = 0.75
RIPPLE_BURST_RADIUS = 70
COMET_TAIL_STRENGTH = 0.65
COMET_TAIL_LENGTH = 90
COMET_TAIL_THICKNESS = 7
SPEED_LINES_STRENGTH = 0.65
SPEED_LINES_THRESHOLD = 800.0
SPEED_LINES_AMOUNT = 5
SPEED_LINES_LENGTH = 90
MAGNETIC_ORBIT_STRENGTH = 0.60
MAGNETIC_ORBIT_THRESHOLD = 250.0
MAGNETIC_ORBIT_RADIUS = 26
MAGNETIC_ORBIT_DOTS = 5
CLICK_EFFECT_STRENGTH = 0.75
CLICK_EFFECT_RADIUS = 72
CLICK_EFFECT_LIFETIME = 0.65
CLICK_EFFECT_SPARK_AMOUNT = 8
motion_trail_points = []
motion_trail_runtime_images = []
spark_particles = []
ripple_bursts = []
click_effect_ripples = []
click_effect_sparks = []
last_left_click_down = False
last_right_click_down = False
last_ripple_burst_time = 0.0
last_motion_trail_x = None
last_motion_trail_y = None

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
    "Fresh Safe Defaults",
    "Last Used Settings",
    "Built-in Preset",
    "Custom Preset",
    "Selected Theme",
]

STARTUP_MODE_ALIASES = {
    "Safe Mode": "Fresh Safe Defaults",
    "Last Used State": "Last Used Settings",
}

DEFAULT_APP_SETTINGS = {
    "startup_mode": "Fresh Safe Defaults",
    "startup_builtin_preset": "Legendary",
    "startup_custom_slot": "1",
    "startup_theme_slot": "1",
    "show_startup_help": True,
    "runtime_hud_visible": False,
    "last_state": None,
}


# v13.11.2 cleanup: safer JSON writes/loads for settings, presets, themes,
# and custom multi-colour presets. This avoids half-written JSON files if the
# app is closed during saving and preserves broken files as .broken backups.
def backup_broken_json_file(path_obj, reason="invalid JSON"):
    try:
        path_obj = Path(path_obj)
        if not path_obj.exists():
            return ""
        backup_path = path_obj.with_suffix(path_obj.suffix + f".broken_{time.strftime('%Y%m%d_%H%M%S')}")
        path_obj.replace(backup_path)
        return str(backup_path)
    except Exception:
        return ""


def read_json_file_safely(path_obj, default_value=None, *, backup_broken=False):
    path_obj = Path(path_obj)
    if not path_obj.exists():
        return default_value
    try:
        return json.loads(path_obj.read_text(encoding="utf-8"))
    except Exception:
        if backup_broken:
            backup_broken_json_file(path_obj)
        return default_value


def write_json_file_safely(path_obj, payload):
    path_obj = Path(path_obj)
    path_obj.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path_obj.with_suffix(path_obj.suffix + ".tmp")
    temp_path.write_text(json.dumps(payload, indent=4), encoding="utf-8")
    temp_path.replace(path_obj)
    return True


def load_app_settings_file():
    settings = dict(DEFAULT_APP_SETTINGS)

    data = read_json_file_safely(SETTINGS_FILE, default_value=None, backup_broken=True)
    if isinstance(data, dict):
        settings.update(data)

    settings["startup_mode"] = STARTUP_MODE_ALIASES.get(settings.get("startup_mode"), settings.get("startup_mode"))
    if settings.get("startup_mode") not in STARTUP_MODE_OPTIONS:
        settings["startup_mode"] = "Fresh Safe Defaults"

    settings["startup_builtin_preset"] = str(settings.get("startup_builtin_preset", "Legendary"))
    settings["startup_custom_slot"] = str(settings.get("startup_custom_slot", "1"))
    settings["startup_theme_slot"] = str(settings.get("startup_theme_slot", "1"))

    return settings


app_settings = load_app_settings_file()


# Hotkeys
VK_CTRL = 0x11
VK_ALT = 0x12
VK_SHIFT = 0x10
VK_LBUTTON = 0x01
VK_RBUTTON = 0x02

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

# Keep an untouched copy of the captured system cursor so Cursor Lab can safely
# return to the original Windows cursor image after testing custom images.
system_cursor_image = base_cursor_image.copy()
system_hotspot_x = int(hotspot_x)
system_hotspot_y = int(hotspot_y)

# PhotoImage cache. It is cleared whenever Cursor Lab changes source image,
# color/tint, scale settings, or hotspot behavior.
tk_cursor_images = {}


def invalidate_cursor_image_cache():
    tk_cursor_images.clear()


def cursor_scale_key(scale):
    return round(float(scale), 2)


def cursor_alpha_key(alpha):
    return round(float(alpha), 2)


def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def color_to_rgb(value, fallback="#8b5cf6"):
    _hex, rgb = parse_hex_color(value, fallback=fallback)
    return rgb


def rgb_to_hex(rgb):
    r, g, b = [int(clamp(v, 0, 255)) for v in rgb]
    return f"#{r:02x}{g:02x}{b:02x}"


def mix_colors(color_a, color_b, amount):
    amount = clamp(float(amount), 0.0, 1.0)
    ra, ga, ba = color_to_rgb(color_a)
    rb, gb, bb = color_to_rgb(color_b)
    return rgb_to_hex((
        round(ra + (rb - ra) * amount),
        round(ga + (gb - ga) * amount),
        round(ba + (bb - ba) * amount),
    ))


def sanitize_neon_color(hex_color):
    fixed, _ = parse_hex_color(hex_color)
    if fixed.lower() == TRANSPARENT_COLOR.lower():
        return "#ff33dd"
    return fixed


def get_neon_gradient_colors(preset_name=None):
    """Return 2-3 neon colors for the selected fancy neon preset.

    Tkinter cannot do true blurred gradients on this transparent overlay, so we
    fake the neon look by layering multiple colored rings/arcs with slight phase
    offsets. This makes presets look like combined neon palettes instead of one
    flat color.
    """
    if not IDLE_EFFECT_NEON_ENABLED:
        return [sanitize_neon_color(CURSOR_TINT_COLOR)]

    name = preset_name or IDLE_EFFECT_NEON_PRESET
    colors = NEON_COLOR_PRESETS.get(name)

    if isinstance(colors, (list, tuple)) and colors:
        return [sanitize_neon_color(color) for color in colors[:3]]

    return [sanitize_neon_color(IDLE_EFFECT_NEON_COLOR or "#8b5cf6")]


def get_neon_color_for_effects():
    return get_neon_gradient_colors()[0]


def get_neon_preset_primary_color(preset_name=None):
    colors = get_neon_gradient_colors(preset_name)
    return colors[0] if colors else "#8b5cf6"


def get_cursor_tint_gradient_colors():
    if CURSOR_TINT_STYLE == "Multi-Colour Neon Preset":
        colors = NEON_COLOR_PRESETS.get(CURSOR_TINT_MULTI_PRESET, NEON_COLOR_PRESETS.get("Cyberpunk Neon", [CURSOR_TINT_COLOR]))
        if isinstance(colors, (list, tuple)) and colors:
            return [sanitize_neon_color(color) for color in colors[:3]]
    return [sanitize_neon_color(CURSOR_TINT_COLOR)]


def interpolate_rgb(color_a, color_b, amount):
    amount = clamp(float(amount), 0.0, 1.0)
    ra, ga, ba = color_to_rgb(color_a)
    rb, gb, bb = color_to_rgb(color_b)
    return (
        int(round(ra + (rb - ra) * amount)),
        int(round(ga + (gb - ga) * amount)),
        int(round(ba + (bb - ba) * amount)),
    )


def get_gradient_color_for_pixel(x, y, width, height):
    colors = get_cursor_tint_gradient_colors()
    if not colors:
        return color_to_rgb(CURSOR_TINT_COLOR)
    if len(colors) == 1:
        return color_to_rgb(colors[0])
    t = 0.0 if height <= 1 else clamp(y / max(1, height - 1), 0.0, 1.0)
    if len(colors) == 2:
        return interpolate_rgb(colors[0], colors[1], t)
    if t <= 0.5:
        return interpolate_rgb(colors[0], colors[1], t / 0.5)
    return interpolate_rgb(colors[1], colors[2], (t - 0.5) / 0.5)


def draw_idle_glow_ring(center_x, center_y, cursor_width, cursor_height, now, strength):
    strength = clamp(float(strength), 0.0, 1.0)
    colors = get_neon_gradient_colors()
    pulse = 0.5 + 0.5 * math.sin(now * 4.5)

    preset_boosts = {
        "Toxic Plasma": 1.18,
        "Lava Circuit": 1.32,
        "Electric Ice": 1.30,
        "Cyberpunk Neon": 1.28,
        "Aurora Neon": 1.12,
        "Vaporwave Neon": 1.00,
        "Royal Glitch": 1.08,
    }
    boost = preset_boosts.get(IDLE_EFFECT_NEON_PRESET, 1.0)

    # Reduced glow quality should be visibly different and lighter: one simple
    # low-width ring, no halo stack, and no rotating arc highlights.
    if PERFORMANCE_REDUCE_GLOW_QUALITY:
        color = colors[0] if colors else sanitize_neon_color(IDLE_EFFECT_NEON_COLOR or "#8b5cf6")
        expand = (5 + (7 * strength) + (3 * pulse * strength)) * boost
        canvas.create_oval(
            center_x - expand,
            center_y - expand,
            center_x + cursor_width + expand,
            center_y + cursor_height + expand,
            outline=color,
            width=max(1, int(1 + strength * 2)),
        )
        return

    expand = (7 + (13 * strength) + (8 * pulse * strength)) * boost
    x1 = center_x - expand
    y1 = center_y - expand
    x2 = center_x + cursor_width + expand
    y2 = center_y + cursor_height + expand

    # Full-quality softer outer halo layers. Intense presets get wider rings.
    for idx, color in enumerate(reversed(colors)):
        offset = (7 + idx * (5 + int(strength * 4))) * boost
        darker = mix_colors(color, "#000000", 0.24 + idx * 0.08)
        canvas.create_oval(
            x1 - offset,
            y1 - offset,
            x2 + offset,
            y2 + offset,
            outline=darker,
            width=max(1, int((2 + strength * 2) * boost)),
        )

    # Main multi-color ring. Layering offset rings makes the palettes easier to
    # distinguish, especially Cyberpunk/Vaporwave/Royal Glitch.
    for idx, color in enumerate(colors):
        offset = idx * (4 + strength * 3)
        canvas.create_oval(
            x1 + offset,
            y1 + offset,
            x2 - offset,
            y2 - offset,
            outline=color,
            width=max(1, int((2 + strength * 4) * boost)),
        )

    # Rotating arc highlights with staggered directions and extents.
    if len(colors) > 1:
        start = int((now * 115) % 360)
        extents = [80, 52, 34]
        for idx, color in enumerate(colors):
            arc_offset = idx * (5 + strength * 2)
            canvas.create_arc(
                x1 - arc_offset,
                y1 - arc_offset,
                x2 + arc_offset,
                y2 + arc_offset,
                start=start + idx * 118,
                extent=extents[idx % len(extents)],
                style="arc",
                outline=mix_colors(color, "#ffffff", 0.16),
                width=max(1, int((2 + strength * 4) * boost)),
            )


def get_idle_effect_state(now, moving):
    idle_active = False
    pulse_scale = 1.0
    wobble_x = 0.0
    wobble_y = 0.0
    alpha_factor = 1.0
    effect_style = "Disabled"

    try:
        enabled = bool(IDLE_EFFECT_ENABLED)
        style = str(IDLE_EFFECT_STYLE or "Disabled")
        delay = clamp(float(IDLE_EFFECT_DELAY), 0.1, 10.0)
        strength = clamp(float(IDLE_EFFECT_STRENGTH), 0.0, 1.0)
    except Exception:
        enabled = False
        style = "Disabled"
        delay = 1.2
        strength = 0.55

    if not enabled or style == "Disabled":
        return {
            "idle_active": False,
            "style": "Disabled",
            "pulse_scale": 1.0,
            "wobble_x": 0.0,
            "wobble_y": 0.0,
            "alpha_factor": 1.0,
            "strength": strength,
            "delay": delay,
        }

    idle_active = (now - last_motion_time) >= delay and not moving
    if not idle_active:
        return {
            "idle_active": False,
            "style": style,
            "pulse_scale": 1.0,
            "wobble_x": 0.0,
            "wobble_y": 0.0,
            "alpha_factor": 1.0,
            "strength": strength,
            "delay": delay,
        }

    phase = now * 4.0
    if style == "Pulse":
        pulse_scale = 1.0 + (0.06 + 0.10 * strength) * math.sin(phase)
    elif style == "Fade":
        alpha_factor = clamp(0.95 - (0.45 * strength * (0.5 + 0.5 * math.sin(phase))), 0.20, 1.0)
    elif style == "Wobble":
        wobble_x = math.sin(phase * 1.05) * (2.0 + 4.0 * strength)
        wobble_y = math.cos(phase * 1.20) * (2.0 + 4.0 * strength)

    return {
        "idle_active": idle_active,
        "style": style,
        "pulse_scale": pulse_scale,
        "wobble_x": wobble_x,
        "wobble_y": wobble_y,
        "alpha_factor": alpha_factor,
        "strength": strength,
        "delay": delay,
    }


def parse_hex_color(value, fallback="#8b5cf6"):
    text_value = str(value or fallback).strip()
    if not text_value.startswith("#"):
        text_value = "#" + text_value

    if len(text_value) != 7:
        text_value = fallback

    try:
        r = int(text_value[1:3], 16)
        g = int(text_value[3:5], 16)
        b = int(text_value[5:7], 16)

        # The overlay uses pure #ff00ff as its transparent color. If the user
        # picks that exact magenta, Tk may punch holes through the drawn cursor.
        # Nudge it by one value so pink/purple cursor colors remain visible.
        if (r, g, b) == (255, 0, 255):
            r, g, b = 255, 1, 254
            text_value = "#ff01fe"

        return text_value.lower(), (r, g, b)
    except Exception:
        return fallback, (139, 92, 246)


def boost_neon_channel(value):
    value = int(clamp(value, 0, 255))
    # Gentle gamma boost used by non-recolor helpers.
    return int(clamp(255 * ((value / 255) ** 0.58), 0, 255))


def neon_base_color(r, g, b, intensity):
    """Return a saturated neon version of the selected color without washing it white.

    v12.8 made higher brightness values drift too close to white. v12.9 treats
    the slider as neon intensity: max channels stay bright, but weaker channels
    are pushed down to keep the hue rich and saturated.
    """
    intensity = clamp(float(intensity), 1.0, 4.0)
    t = clamp((intensity - 1.0) / 3.0, 0.0, 1.0)

    r = int(clamp(r, 0, 255))
    g = int(clamp(g, 0, 255))
    b = int(clamp(b, 0, 255))
    max_channel = max(r, g, b, 1)

    # Normalize so the dominant channel is bright neon.
    scale = 255.0 / max_channel
    nr = clamp(r * scale, 0, 255)
    ng = clamp(g * scale, 0, 255)
    nb = clamp(b * scale, 0, 255)

    # Increase saturation as intensity rises instead of adding white.
    avg = (nr + ng + nb) / 3.0
    saturation = 1.25 + 0.95 * t
    nr = clamp(avg + (nr - avg) * saturation, 0, 255)
    ng = clamp(avg + (ng - avg) * saturation, 0, 255)
    nb = clamp(avg + (nb - avg) * saturation, 0, 255)

    # Slight electric lift for visibility, still capped per channel so the hue
    # remains colorful and does not collapse into white.
    lift = 10 + 22 * t
    nr = clamp(nr + lift if nr > 24 else nr, 0, 255)
    ng = clamp(ng + lift if ng > 24 else ng, 0, 255)
    nb = clamp(nb + lift if nb > 24 else nb, 0, 255)

    return nr, ng, nb


def apply_bright_neon_tint_pixel(pr, pg, pb, r, g, b, strength, brightness_boost=1.2):
    """Recolor the full visible cursor body into saturated neon.

    The slider now behaves as intensity, not whiteness. Low values give rich
    neon color; higher values make dark cursor regions more vivid while keeping
    the chosen hue saturated.
    """
    pixel_luma = clamp((pr * 0.299 + pg * 0.587 + pb * 0.114) / 255.0, 0.0, 1.0)
    intensity = clamp(float(brightness_boost), 1.0, 4.0)
    t = clamp((intensity - 1.0) / 3.0, 0.0, 1.0)

    nr, ng, nb = neon_base_color(r, g, b, intensity)

    # Preserve cursor readability: white areas become bright neon; dark edges
    # become deeper neon instead of staying black/white.
    floor = 0.52 + 0.20 * t
    shade = clamp(floor + pixel_luma * (1.03 - floor), 0.0, 1.08)

    tr = clamp(nr * shade, 0, 255)
    tg = clamp(ng * shade, 0, 255)
    tb = clamp(nb * shade, 0, 255)

    # Very small highlight only. This avoids the v12.8 washed-out white look.
    highlight = clamp((pixel_luma - 0.72) * (0.03 + 0.04 * t), 0.0, 0.07)
    tr = tr + (255 - tr) * highlight
    tg = tg + (255 - tg) * highlight
    tb = tb + (255 - tb) * highlight

    strong = clamp(0.88 + strength * 0.12, 0.0, 1.0)
    out_r = int(pr * (1.0 - strong) + tr * strong)
    out_g = int(pg * (1.0 - strong) + tg * strong)
    out_b = int(pb * (1.0 - strong) + tb * strong)

    return int(clamp(out_r, 0, 255)), int(clamp(out_g, 0, 255)), int(clamp(out_b, 0, 255))


def cursor_outline_applies_for_role(role):
    """Return True when the current role should receive the black outline."""
    role = "drawn" if role == "drawn" else "fake"
    return bool(CURSOR_TINT_BLACK_OUTLINE) and (
        (role == "drawn" and CURSOR_TINT_APPLY_DRAWN)
        or (role == "fake" and CURSOR_TINT_APPLY_FAKE)
    )


def cursor_outline_padding_for_role(role):
    """Pixel padding added around outlined cursor images after resizing."""
    if not cursor_outline_applies_for_role(role):
        return 0

    try:
        return int(max(1, min(8, round(float(CURSOR_TINT_OUTLINE_THICKNESS))))) + 1
    except Exception:
        return 3


def apply_black_outline_to_image(img, thickness=2):
    """Add a smoother alpha-mask outline around the cursor.

    Older v12.9.1 outlining darkened edge pixels inside the cursor shape, which
    could look chunky or slightly out of shape. This version expands the alpha
    mask behind the original cursor, draws black behind that expanded shape, and
    then pastes the original cursor on top. The result follows the real cursor
    silhouette more evenly.
    """
    try:
        thickness = int(max(1, min(8, round(float(thickness)))))
    except Exception:
        thickness = 2

    src = img.convert("RGBA")
    pad = thickness + 1
    width, height = src.size

    padded = Image.new("RGBA", (width + pad * 2, height + pad * 2), (0, 0, 0, 0))
    padded.alpha_composite(src, (pad, pad))

    alpha = padded.getchannel("A")
    kernel_size = max(3, thickness * 2 + 1)
    if kernel_size % 2 == 0:
        kernel_size += 1

    expanded_alpha = alpha.filter(ImageFilter.MaxFilter(kernel_size))

    outline = Image.new("RGBA", padded.size, (0, 0, 0, 255))
    outline.putalpha(expanded_alpha)
    outline.alpha_composite(padded)
    return outline

def apply_cursor_tint_to_image(img, role):
    role = "drawn" if role == "drawn" else "fake"

    tint_applies = bool(CURSOR_TINT_ENABLED) and (
        (role == "drawn" and CURSOR_TINT_APPLY_DRAWN)
        or (role == "fake" and CURSOR_TINT_APPLY_FAKE)
    )

    outline_applies = cursor_outline_applies_for_role(role)

    if not tint_applies and not outline_applies:
        return img

    _color_hex, (r, g, b) = parse_hex_color(CURSOR_TINT_COLOR)
    strength = max(0.0, min(1.0, float(CURSOR_TINT_STRENGTH)))

    base = img.convert("RGBA")

    if tint_applies:
        pixels = base.load()

        # Strong tint/recolor pass. This keeps cursor shading readable while making
        # the selected color actually visible on black/white system cursors.
        for y in range(base.height):
            for x in range(base.width):
                pr, pg, pb, pa = pixels[x, y]
                if pa == 0:
                    continue

                target_r, target_g, target_b = (r, g, b)
                if CURSOR_TINT_STYLE == "Multi-Colour Neon Preset":
                    target_r, target_g, target_b = get_gradient_color_for_pixel(x, y, base.width, base.height)

                if CURSOR_TINT_BRIGHT_NEON:
                    nr, ng, nb = apply_bright_neon_tint_pixel(pr, pg, pb, target_r, target_g, target_b, strength, CURSOR_TINT_NEON_BRIGHTNESS)
                else:
                    brightness = max(0.25, min(1.0, (pr * 0.299 + pg * 0.587 + pb * 0.114) / 255.0))
                    tr = int(target_r * brightness)
                    tg = int(target_g * brightness)
                    tb = int(target_b * brightness)

                    nr = int(pr * (1.0 - strength) + tr * strength)
                    ng = int(pg * (1.0 - strength) + tg * strength)
                    nb = int(pb * (1.0 - strength) + tb * strength)

                # Avoid the overlay transparent-key color after blending too.
                if (nr, ng, nb) == (255, 0, 255):
                    nr, ng, nb = 255, 1, 254

                pixels[x, y] = (nr, ng, nb, pa)

    if outline_applies:
        base = apply_black_outline_to_image(base, CURSOR_TINT_OUTLINE_THICKNESS)

    return base


def prepare_custom_cursor_image(img):
    prepared = img.convert("RGBA")
    max_side = max(32, int(CUSTOM_CURSOR_MAX_SIDE))
    if prepared.width > max_side or prepared.height > max_side:
        prepared.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    return prepared


def set_custom_cursor_hotspot_from_mode():
    global hotspot_x, hotspot_y

    mode = str(CUSTOM_CURSOR_HOTSPOT_MODE or "Top-left")

    if mode == "Center":
        hotspot_x = base_cursor_image.width // 2
        hotspot_y = base_cursor_image.height // 2
    elif mode == "Bottom-center":
        hotspot_x = base_cursor_image.width // 2
        hotspot_y = max(0, base_cursor_image.height - 1)
    else:
        hotspot_x = 0
        hotspot_y = 0


def set_active_cursor_image(img, *, hotspot_mode=None, source_label="Custom image"):
    global base_cursor_image, CUSTOM_CURSOR_SOURCE_LABEL, CUSTOM_CURSOR_HOTSPOT_MODE, CURSOR_SHAPE_MODE

    base_cursor_image = prepare_custom_cursor_image(img)

    if hotspot_mode is not None:
        CUSTOM_CURSOR_HOTSPOT_MODE = str(hotspot_mode)

    CUSTOM_CURSOR_SOURCE_LABEL = str(source_label or "Custom image")
    CURSOR_SHAPE_MODE = "Custom Image File"
    set_custom_cursor_hotspot_from_mode()
    invalidate_cursor_image_cache()


def mark_cursor_lab_pending(message=None):
    global CURSOR_LAB_DIRTY

    CURSOR_LAB_DIRTY = True

    if "custom_cursor_status_var" in globals():
        status = message or "Cursor Lab changes pending. Click Apply Cursor Lab to activate them."
        try:
            custom_cursor_status_var.set(status + "\n\nCurrent active settings:\n" + cursor_lab_status_text())
        except Exception:
            custom_cursor_status_var.set(status)


def cursor_lab_drawn_replacement_active():
    """True when the drawn cursor is acting as the user's visible replacement cursor."""
    try:
        scale_changed = abs(float(REAL_DRAWN_CURSOR_SCALE) - 1.0) > 0.01
    except Exception:
        scale_changed = False

    offset_changed = int(manual_offset_x) != 0 or int(manual_offset_y) != 0
    tinting_drawn = bool(CURSOR_TINT_ENABLED and CURSOR_TINT_APPLY_DRAWN)
    outlining_drawn = bool(CURSOR_TINT_BLACK_OUTLINE and CURSOR_TINT_APPLY_DRAWN)
    idle_drawn_effect = bool(IDLE_EFFECT_ENABLED and IDLE_EFFECT_STYLE != "Disabled")
    manual_shape_selected = bool(CURSOR_SHAPE_MODE not in ("Captured System Cursor", "Custom Image File"))

    # Idle effects and manual cursor shapes need the drawn system cursor even when no
    # tint/custom image is active. Otherwise the real Windows cursor stays on top.
    return bool(CUSTOM_CURSOR_ENABLED or manual_shape_selected or tinting_drawn or outlining_drawn or idle_drawn_effect or scale_changed or offset_changed)


def enforce_cursor_lab_replacement_visibility():
    """Keep replacement cursor modes usable and visible.

    If the user customizes the drawn-real cursor through Cursor Lab, the normal
    Windows cursor must stay transparent and the drawn cursor must stay enabled.
    """
    global show_drawn_real_cursor

    if not cursor_lab_drawn_replacement_active():
        return

    show_drawn_real_cursor = True

    if not transparent_active:
        set_transparent_mode()

    try:
        root.attributes("-topmost", True)
        root.lift()
    except Exception:
        pass


def begin_native_dialog_cursor_mode():
    """Temporarily restore the normal cursor while native Windows dialogs are open.

    Native dialogs such as the color picker and file picker are outside the
    CustomTkinter panel. If CursorSwarm keeps the Windows cursor transparent and
    keeps drawing the overlay above them, the user can lose the cursor inside the
    dialog. This helper pauses the overlay and restores the real cursor until the
    dialog closes.
    """
    global native_dialog_open

    was_transparent = bool(transparent_active)
    native_dialog_open = True

    try:
        canvas.delete("all")
    except Exception:
        pass

    set_visible_mode()

    try:
        root.attributes("-topmost", False)
        root.lower()
    except Exception:
        pass

    try:
        bubble = globals().get("floating_control_bubble")
        if bubble is not None:
            bubble.withdraw()
    except Exception:
        pass

    return was_transparent


def end_native_dialog_cursor_mode(was_transparent=False):
    """Restore CursorSwarm overlay/cursor state after a native dialog closes."""
    global native_dialog_open

    native_dialog_open = False

    try:
        root.attributes("-topmost", True)
        root.lift()
    except Exception:
        pass

    try:
        update_floating_control_bubble_visibility()
    except Exception:
        pass

    if was_transparent or cursor_lab_drawn_replacement_active():
        set_transparent_mode()

    enforce_cursor_lab_replacement_visibility()


def get_safe_dialog_parent():
    """Return the best parent window for native dialogs/message boxes."""
    panel = globals().get("control_panel")

    try:
        if panel is not None and panel.winfo_exists():
            return panel
    except Exception:
        pass

    return root


def prepare_dialog_parent(parent=None):
    """Bring the parent window forward before a blocking native dialog opens."""
    parent = parent or get_safe_dialog_parent()

    try:
        parent.deiconify()
    except Exception:
        pass

    try:
        parent.attributes("-topmost", True)
    except Exception:
        pass

    try:
        parent.lift()
        parent.focus_force()
        parent.update_idletasks()
    except Exception:
        pass

    return parent


def add_default_dialog_parent(kwargs):
    """Attach dialogs to the Control Panel so they cannot hide behind it."""
    new_kwargs = dict(kwargs)
    parent = new_kwargs.get("parent") or get_safe_dialog_parent()
    new_kwargs["parent"] = prepare_dialog_parent(parent)
    return new_kwargs


def run_native_dialog_safely(dialog_callable, *, parent=None):
    """Run a native dialog with a visible real cursor and no blinking overlay."""
    parent = prepare_dialog_parent(parent)
    was_transparent = begin_native_dialog_cursor_mode()

    # begin_native_dialog_cursor_mode lowers the overlay root. Bring the actual
    # dialog parent back to the front after that, otherwise message boxes can
    # appear behind the CustomTkinter Control Panel and block the app invisibly.
    prepare_dialog_parent(parent)

    try:
        return dialog_callable()
    finally:
        end_native_dialog_cursor_mode(was_transparent)
        try:
            prepare_dialog_parent(parent)
        except Exception:
            pass


def safe_messagebox_showinfo(*args, **kwargs):
    kwargs = add_default_dialog_parent(kwargs)
    parent = kwargs.get("parent")
    return run_native_dialog_safely(lambda: messagebox.showinfo(*args, **kwargs), parent=parent)


def safe_messagebox_showerror(*args, **kwargs):
    kwargs = add_default_dialog_parent(kwargs)
    parent = kwargs.get("parent")
    return run_native_dialog_safely(lambda: messagebox.showerror(*args, **kwargs), parent=parent)


def safe_messagebox_showwarning(*args, **kwargs):
    kwargs = add_default_dialog_parent(kwargs)
    parent = kwargs.get("parent")
    return run_native_dialog_safely(lambda: messagebox.showwarning(*args, **kwargs), parent=parent)


def safe_messagebox_askyesno(*args, **kwargs):
    kwargs = add_default_dialog_parent(kwargs)
    parent = kwargs.get("parent")
    return run_native_dialog_safely(lambda: messagebox.askyesno(*args, **kwargs), parent=parent)


def safe_filedialog_askopenfilename(*args, **kwargs):
    kwargs = add_default_dialog_parent(kwargs)
    parent = kwargs.get("parent")
    return run_native_dialog_safely(lambda: filedialog.askopenfilename(*args, **kwargs), parent=parent)


def safe_filedialog_asksaveasfilename(*args, **kwargs):
    kwargs = add_default_dialog_parent(kwargs)
    parent = kwargs.get("parent")
    return run_native_dialog_safely(lambda: filedialog.asksaveasfilename(*args, **kwargs), parent=parent)


def safe_colorchooser_askcolor(*args, **kwargs):
    kwargs = add_default_dialog_parent(kwargs)
    parent = kwargs.get("parent")
    return run_native_dialog_safely(lambda: colorchooser.askcolor(*args, **kwargs), parent=parent)


def handle_tk_callback_exception(exc_type, exc_value, exc_traceback):
    """Fail safely if a Tk/CustomTkinter callback throws an unexpected error."""
    try:
        set_visible_mode()
        restore_cursors_safely()
    except Exception:
        pass

    try:
        traceback.print_exception(exc_type, exc_value, exc_traceback)
    except Exception:
        print(f"CursorSwarm callback error: {exc_value}")

    try:
        parent = get_safe_dialog_parent()
        messagebox.showerror(
            "CursorSwarm recovered from an error",
            "CursorSwarm hit an unexpected UI error and restored the Windows cursor for safety.\n\n"
            f"Error: {exc_value}",
            parent=parent,
        )
    except Exception:
        pass


try:
    root.report_callback_exception = handle_tk_callback_exception
except Exception:
    pass


def load_custom_cursor_image(path=None, *, show_messages=True):
    global PENDING_CUSTOM_CURSOR_IMAGE, PENDING_CUSTOM_CURSOR_IMAGE_PATH
    global PENDING_CUSTOM_CURSOR_SOURCE_LABEL, PENDING_RESET_TO_SYSTEM_CURSOR

    chosen_path = path

    if not chosen_path:
        chosen_path = safe_filedialog_askopenfilename(
            parent=control_panel if "control_panel" in globals() else root,
            title="Choose custom cursor image",
            filetypes=[
                ("Supported image/cursor files", "*.png *.jpg *.jpeg *.webp *.bmp *.gif *.ico *.cur *.ani"),
                ("PNG images", "*.png"),
                ("Cursor/icon files", "*.cur *.ico *.ani"),
                ("All files", "*.*"),
            ],
        )

    if not chosen_path:
        return False

    try:
        if str(chosen_path).lower().endswith('.ani'):
            ani_result = parse_ani_cursor_file(chosen_path, shape_name="Custom Image File")
            if not ani_result or not ani_result.get('frames'):
                raise RuntimeError('Could not parse animated cursor frames from that .ani file.')
            img = ani_result['frames'][0].copy()
        else:
            with Image.open(chosen_path) as opened:
                try:
                    opened.seek(0)
                except Exception:
                    pass
                img = opened.convert("RGBA")

        PENDING_CUSTOM_CURSOR_IMAGE = img.copy()
        PENDING_CUSTOM_CURSOR_IMAGE_PATH = str(chosen_path)
        PENDING_CUSTOM_CURSOR_SOURCE_LABEL = Path(chosen_path).name
        PENDING_RESET_TO_SYSTEM_CURSOR = False

        if "custom_cursor_enabled_var" in globals():
            custom_cursor_enabled_var.set(True)
        if "custom_cursor_path_var" in globals():
            custom_cursor_path_var.set(str(chosen_path))
        if "cursor_shape_mode_var" in globals():
            cursor_shape_mode_var.set("Custom Image File")

        mark_cursor_lab_pending(
            f"Pending custom cursor source: {Path(chosen_path).name}. Click Apply Cursor Lab to activate it."
        )

        if show_messages:
            safe_messagebox_showinfo(
                "Custom Cursor Staged",
                "Custom cursor image staged.\n\n"
                "It will not change the active cursor until you click Apply Cursor Lab."
            )
        return True

    except Exception as exc:
        if show_messages:
            safe_messagebox_showerror("Custom Cursor Load Failed", f"Could not load that image/cursor file:\n\n{exc}")
        return False


def reset_to_system_cursor_image(show_message=True):
    global PENDING_CUSTOM_CURSOR_IMAGE, PENDING_CUSTOM_CURSOR_IMAGE_PATH
    global PENDING_CUSTOM_CURSOR_SOURCE_LABEL, PENDING_RESET_TO_SYSTEM_CURSOR

    PENDING_CUSTOM_CURSOR_IMAGE = None
    PENDING_CUSTOM_CURSOR_IMAGE_PATH = ""
    PENDING_CUSTOM_CURSOR_SOURCE_LABEL = ""
    PENDING_RESET_TO_SYSTEM_CURSOR = True

    if "custom_cursor_enabled_var" in globals():
        custom_cursor_enabled_var.set(False)
    if "custom_cursor_path_var" in globals():
        custom_cursor_path_var.set("")
    if "cursor_shape_mode_var" in globals():
        cursor_shape_mode_var.set("Captured System Cursor")

    mark_cursor_lab_pending("Pending reset to captured system cursor. Click Apply Cursor Lab to activate it.")

    if show_message:
        safe_messagebox_showinfo(
            "System Cursor Reset Staged",
            "System cursor source reset is staged.\n\n"
            "It will not change the active cursor until you click Apply Cursor Lab."
        )


def commit_reset_to_system_cursor_image():
    global base_cursor_image, hotspot_x, hotspot_y
    global CUSTOM_CURSOR_ENABLED, CUSTOM_CURSOR_IMAGE_PATH, CUSTOM_CURSOR_SOURCE_LABEL, CURSOR_SHAPE_MODE
    global CURSOR_USE_REAL_WINDOWS_ANI, CURSOR_ANIMATION_SPEED_MODE

    CUSTOM_CURSOR_ENABLED = False
    CUSTOM_CURSOR_IMAGE_PATH = ""
    CUSTOM_CURSOR_SOURCE_LABEL = "System cursor"
    CURSOR_SHAPE_MODE = "Captured System Cursor"
    base_cursor_image = system_cursor_image.copy()
    hotspot_x = int(system_hotspot_x)
    hotspot_y = int(system_hotspot_y)
    invalidate_cursor_image_cache()


def create_generated_manual_cursor_shape(shape_name):
    """Create reliable built-in shapes when Windows stock extraction is invisible.

    Some thin Windows cursor shapes, especially I-Beam and Crosshair, can be
    returned as mask-only cursors. After CursorSwarm has replaced system cursor
    handles for transparent mode, extracting those shapes can produce a nearly
    transparent/empty image on some machines. These generated fallback shapes
    keep the manual library reliable while still supporting tint, multi-colour
    tint, resize, idle effects, and black outline.
    """
    shape_name = str(shape_name or "")
    if shape_name not in ("I-Beam", "Crosshair"):
        return None, None, None

    scale = 4
    size = 32
    img = Image.new("RGBA", (size * scale, size * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    def sx(value):
        return int(round(value * scale))

    def draw_contrast_line(points, outline_width=5, inner_width=3):
        scaled = [(sx(x), sx(y)) for x, y in points]
        draw.line(scaled, fill=(0, 0, 0, 255), width=max(1, sx(outline_width)), joint="curve")
        draw.line(scaled, fill=(255, 255, 255, 255), width=max(1, sx(inner_width)), joint="curve")

    if shape_name == "I-Beam":
        # Top/bottom bars plus a center stem. The hotspot stays near the center,
        # matching the practical clicking point for text selection.
        draw_contrast_line([(9, 5), (23, 5)], outline_width=4, inner_width=2)
        draw_contrast_line([(16, 5), (16, 27)], outline_width=5, inner_width=3)
        draw_contrast_line([(9, 27), (23, 27)], outline_width=4, inner_width=2)
        hotspot = (16, 16)
    else:
        # Crosshair with a tiny center gap so the target point remains readable.
        draw_contrast_line([(16, 4), (16, 12)], outline_width=4, inner_width=2)
        draw_contrast_line([(16, 20), (16, 28)], outline_width=4, inner_width=2)
        draw_contrast_line([(4, 16), (12, 16)], outline_width=4, inner_width=2)
        draw_contrast_line([(20, 16), (28, 16)], outline_width=4, inner_width=2)
        # Center dot gives a visible anchor without becoming a blob.
        draw.ellipse([sx(14.5), sx(14.5), sx(17.5), sx(17.5)], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=sx(1))
        hotspot = (16, 16)

    img = img.resize((size, size), Image.Resampling.LANCZOS)
    return img, hotspot[0], hotspot[1]


def get_windows_cursor_registry_path(cursor_name):
    cursor_name = str(cursor_name or "")
    cache_key = cursor_name.lower()
    if cache_key in SYSTEM_ANI_PATH_CACHE:
        return SYSTEM_ANI_PATH_CACHE[cache_key]

    resolved_path = ""
    if winreg is not None:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Cursors") as key:
                value, _ = winreg.QueryValueEx(key, cursor_name)
                resolved_path = os.path.expandvars(str(value or "").strip().strip('"'))
        except Exception:
            resolved_path = ""

    if not resolved_path:
        # Safe fallback for standard Windows Aero cursor names when the registry
        # stores only defaults or empty values.
        fallback_names = {
            "wait": "aero_busy.ani",
            "appstarting": "aero_working.ani",
        }
        fallback_name = fallback_names.get(cache_key)
        if fallback_name:
            candidate = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Cursors" / fallback_name
            if candidate.exists():
                resolved_path = str(candidate)

    if resolved_path and not Path(resolved_path).exists():
        resolved_path = ""

    SYSTEM_ANI_PATH_CACHE[cache_key] = resolved_path
    return resolved_path


def parse_cursor_hotspot_from_icon_bytes(icon_bytes):
    try:
        if len(icon_bytes) < 6:
            return None
        reserved, icon_type, count = struct.unpack_from('<HHH', icon_bytes, 0)
        if reserved != 0 or count < 1:
            return None
        if icon_type == 2 and len(icon_bytes) >= 14:
            x_hotspot, y_hotspot = struct.unpack_from('<HH', icon_bytes, 10)
            return int(x_hotspot), int(y_hotspot)
    except Exception:
        return None
    return None


def repair_ani_frame_alpha(frame, shape_name=None):
    """Repair ANI frames that decode with black background pixels.

    v13.9 removed only the edge-connected black square. Some Windows ANI
    frames also contain black background pixels inside the spinner ring. v13.9
    keeps the safer edge cleanup and then removes likely internal background
    components from the spinner area, while avoiding the arrow outline in the
    Working in Background cursor.
    """
    img = frame.convert("RGBA")
    width, height = img.size

    if width <= 1 or height <= 1:
        return img

    pixels = img.load()
    corner_samples = [
        pixels[0, 0],
        pixels[width - 1, 0],
        pixels[0, height - 1],
        pixels[width - 1, height - 1],
    ]
    bg_r = sum(sample[0] for sample in corner_samples) / 4.0
    bg_g = sum(sample[1] for sample in corner_samples) / 4.0
    bg_b = sum(sample[2] for sample in corner_samples) / 4.0

    # Only run the background repair when the corners look like a dark cursor
    # mask background. This avoids damaging normal full-colour cursor frames.
    if max(bg_r, bg_g, bg_b) > 58:
        return img

    def close_to_background(px):
        return (
            abs(px[0] - bg_r) <= 34
            and abs(px[1] - bg_g) <= 34
            and abs(px[2] - bg_b) <= 34
            and px[3] >= 220
        )

    visited = bytearray(width * height)
    stack = []

    def push_if_bg(x, y):
        idx = y * width + x
        if visited[idx]:
            return
        visited[idx] = 1
        if close_to_background(pixels[x, y]):
            stack.append((x, y))

    # First remove edge-connected background, the obvious square.
    for x in range(width):
        push_if_bg(x, 0)
        push_if_bg(x, height - 1)
    for y in range(height):
        push_if_bg(0, y)
        push_if_bg(width - 1, y)

    removed = 0
    while stack:
        x, y = stack.pop()
        r, g, b, a = pixels[x, y]
        pixels[x, y] = (r, g, b, 0)
        removed += 1
        if x > 0:
            push_if_bg(x - 1, y)
        if x + 1 < width:
            push_if_bg(x + 1, y)
        if y > 0:
            push_if_bg(x, y - 1)
        if y + 1 < height:
            push_if_bg(x, y + 1)

    # Then remove internal background components that are likely holes inside
    # the loading spinner. This fixes black regions inside the blue spinner.
    mode = str(shape_name or "")
    internal_visited = bytearray(width * height)

    def component_should_be_removed(component, min_x, min_y, max_x, max_y):
        area = len(component)
        if area < 3:
            return False
        center_x = (min_x + max_x) / 2.0
        center_y = (min_y + max_y) / 2.0
        if mode == "Busy / Loading":
            # Busy is only the spinner, so dark internal background pixels are
            # unwanted mask pixels.
            return True
        if mode == "Working in Background":
            # Real AppStarting.ani already contains the correct arrow+spinner
            # placement. Preserve the arrow outline, but remove black mask holes
            # in the spinner area near the upper-right of the arrow.
            spinner_zone = (
                center_x >= width * 0.18
                and center_x <= width * 0.78
                and center_y >= height * 0.02
                and center_y <= height * 0.62
            )
            return spinner_zone
        return False

    for start_y in range(height):
        for start_x in range(width):
            idx = start_y * width + start_x
            if internal_visited[idx]:
                continue
            internal_visited[idx] = 1
            if not close_to_background(pixels[start_x, start_y]):
                continue

            comp = []
            stack2 = [(start_x, start_y)]
            min_x = max_x = start_x
            min_y = max_y = start_y
            touches_edge = False

            while stack2:
                x, y = stack2.pop()
                comp.append((x, y))
                if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                    touches_edge = True
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)
                for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                    if 0 <= nx < width and 0 <= ny < height:
                        nidx = ny * width + nx
                        if not internal_visited[nidx]:
                            internal_visited[nidx] = 1
                            if close_to_background(pixels[nx, ny]):
                                stack2.append((nx, ny))

            if not touches_edge and component_should_be_removed(comp, min_x, min_y, max_x, max_y):
                for x, y in comp:
                    r, g, b, a = pixels[x, y]
                    pixels[x, y] = (r, g, b, 0)
                    removed += 1

    if removed < max(4, int(width * height * 0.01)):
        return frame.convert("RGBA")

    return img


def resize_ani_frame_for_cursor(frame, hotspot_x, hotspot_y, max_side=ANI_CURSOR_MAX_SIDE):
    """Keep real ANI frames close to normal cursor size.

    Some Windows themes store 48/64px animated cursor frames. CursorSwarm draws
    them as overlay images, so they can look too large compared with other
    cursor shapes. This normalizes them near normal cursor size while scaling
    the hotspot with the frame.
    """
    img = frame.convert("RGBA")
    max_dim = max(img.width, img.height)
    if max_dim <= max_side:
        return img, int(hotspot_x), int(hotspot_y)
    scale = float(max_side) / float(max_dim)
    new_w = max(1, int(round(img.width * scale)))
    new_h = max(1, int(round(img.height * scale)))
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    return resized, int(round(hotspot_x * scale)), int(round(hotspot_y * scale))


def clean_spinner_black_pixels(frame, shape_name=None):
    """Remove dark mask-fill pixels that survive ANI decoding.

    v13.9 is more aggressive for Busy/Loading because the real Windows ANI
    frames can decode with opaque black mask pixels inside the spinner ring. The
    actual Windows spinner is blue/white, so near-black, low-saturation pixels in
    the spinner frame are treated as transparent mask fill. Working in Background
    is now built from a clean arrow plus the Busy spinner, so this cleanup mainly
    touches the spinner frames before they are composited.
    """
    img = frame.convert("RGBA")
    pixels = img.load()
    width, height = img.size
    mode = str(shape_name or "")

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a < 120:
                continue
            max_c = max(r, g, b)
            min_c = min(r, g, b)
            saturation = max_c - min_c

            # Remove pure/near-black background, plus very dark low-saturation
            # fill. Keep blue spinner pixels because their blue channel and
            # saturation are much stronger.
            is_dark_fill = (
                max_c <= 72
                or (max_c <= 105 and saturation <= 28)
                or (r <= 52 and g <= 52 and b <= 52)
            )
            if not is_dark_fill:
                continue

            if mode == "Working in Background":
                # In real AppStarting.ani, the spinner is near the upper-right
                # shoulder of the arrow. Avoid removing the black arrow outline
                # outside that spinner zone.
                spinner_zone = (x >= width * 0.18 and x <= width * 0.78 and y <= height * 0.62)
                if not spinner_zone:
                    continue
            pixels[x, y] = (r, g, b, 0)
    return img


def trim_transparent_padding(img, padding=1):
    """Crop empty transparent padding so spinner graphics can be sized/placed accurately."""
    rgba = img.convert("RGBA")
    alpha = rgba.getchannel("A")
    bbox = alpha.getbbox()
    if not bbox:
        return rgba
    left, top, right, bottom = bbox
    left = max(0, left - int(padding))
    top = max(0, top - int(padding))
    right = min(rgba.width, right + int(padding))
    bottom = min(rgba.height, bottom + int(padding))
    return rgba.crop((left, top, right, bottom))


def create_working_frames_from_arrow_and_spinner(spinner_frames):
    """Use the reliable Arrow shape plus the real Windows busy spinner frames.

    v13.9 kept the arrow clean, but the spinner landed too low/far away. This
    version makes the spinner larger and tucks it closer to the arrow's right
    shoulder, matching the Windows Working in Background feel more closely.
    """
    arrow_img, arrow_hotspot_x, arrow_hotspot_y = load_stock_cursor_shape_image("Arrow")
    if arrow_img is None:
        arrow_img = system_cursor_image.copy()
        arrow_hotspot_x, arrow_hotspot_y = int(system_hotspot_x), int(system_hotspot_y)
    arrow_img = prepare_custom_cursor_image(arrow_img)

    target_spinner_side = 30
    prepared_spinners = []
    for spinner in spinner_frames:
        spin = clean_spinner_black_pixels(spinner.convert("RGBA"), shape_name="Busy / Loading")
        # Real ANI spinner frames often contain transparent padding. Crop that
        # padding first so the visible blue ring can be enlarged accurately.
        spin = trim_transparent_padding(spin, padding=1)
        max_dim = max(spin.width, spin.height, 1)
        if max_dim != target_spinner_side:
            scale = target_spinner_side / float(max_dim)
            spin = spin.resize((max(1, int(round(spin.width * scale))), max(1, int(round(spin.height * scale)))), Image.Resampling.LANCZOS)
        prepared_spinners.append(spin)

    canvas_w = max(arrow_img.width + int(target_spinner_side * 0.72) + 4, 48)
    canvas_h = max(arrow_img.height + 4, 42)
    frames = []
    for spinner in prepared_spinners:
        frame = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
        frame.alpha_composite(arrow_img, (0, 0))

        # Put the spinner at the upper-right of the pointer, closer to the
        # Windows Working in Background layout instead of below the arrow.
        spinner_x = min(canvas_w - spinner.width, max(8, int(arrow_img.width * 0.58)))
        spinner_y = min(canvas_h - spinner.height, max(0, int(arrow_img.height * 0.02)))
        frame.alpha_composite(spinner, (spinner_x, spinner_y))
        frames.append(frame)
    return frames, int(arrow_hotspot_x), int(arrow_hotspot_y)


def iter_riff_chunks(data, start_offset=12, end_offset=None):
    pos = int(start_offset)
    data_len = len(data) if end_offset is None else min(len(data), int(end_offset))
    while pos + 8 <= data_len:
        chunk_id = data[pos:pos+4]
        chunk_size = struct.unpack_from('<I', data, pos + 4)[0]
        chunk_data_start = pos + 8
        chunk_data_end = min(chunk_data_start + chunk_size, data_len)
        yield chunk_id, chunk_size, chunk_data_start, chunk_data_end
        pos = chunk_data_start + chunk_size + (chunk_size & 1)


def parse_ani_cursor_file(path_value, shape_name=None):
    cache_key = str(path_value or "") + "|" + str(shape_name or "")
    if cache_key in ANI_CURSOR_CACHE:
        return ANI_CURSOR_CACHE[cache_key]

    try:
        data = Path(str(path_value or "")).read_bytes()
    except Exception:
        ANI_CURSOR_CACHE[cache_key] = None
        return None

    if len(data) < 12 or data[:4] != b'RIFF' or data[8:12] != b'ACON':
        ANI_CURSOR_CACHE[cache_key] = None
        return None

    frames_raw = []
    frame_hotspots = []
    rate_values = []
    seq_values = []
    default_jif_rate = 6

    def walk_chunks(start_offset, end_offset):
        nonlocal default_jif_rate
        for chunk_id, chunk_size, chunk_data_start, chunk_data_end in iter_riff_chunks(data, start_offset, end_offset):
            if chunk_id == b'LIST':
                if chunk_data_start + 4 > chunk_data_end:
                    continue
                list_type = data[chunk_data_start:chunk_data_start+4]
                if list_type in (b'fram', b'INFO'):
                    walk_chunks(chunk_data_start + 4, chunk_data_end)
                else:
                    walk_chunks(chunk_data_start + 4, chunk_data_end)
            elif chunk_id == b'anih':
                payload = data[chunk_data_start:chunk_data_end]
                if len(payload) >= 36:
                    values = struct.unpack_from('<9I', payload, 0)
                    default_jif_rate = max(1, int(values[7]))
            elif chunk_id == b'rate':
                payload = data[chunk_data_start:chunk_data_end]
                rate_values[:] = [max(1, int(v)) for v in struct.unpack('<' + 'I' * (len(payload)//4), payload[:(len(payload)//4)*4])]
            elif chunk_id == b'seq ':
                payload = data[chunk_data_start:chunk_data_end]
                seq_values[:] = [max(0, int(v)) for v in struct.unpack('<' + 'I' * (len(payload)//4), payload[:(len(payload)//4)*4])]
            elif chunk_id == b'icon':
                icon_bytes = data[chunk_data_start:chunk_data_end]
                try:
                    with Image.open(io.BytesIO(icon_bytes)) as opened:
                        try:
                            opened.seek(0)
                        except Exception:
                            pass
                        frames_raw.append(clean_spinner_black_pixels(repair_ani_frame_alpha(opened.convert('RGBA'), shape_name=shape_name), shape_name=shape_name))
                        frame_hotspots.append(parse_cursor_hotspot_from_icon_bytes(icon_bytes))
                except Exception:
                    pass

    walk_chunks(12, len(data))

    if not frames_raw:
        ANI_CURSOR_CACHE[cache_key] = None
        return None

    if seq_values:
        ordered_frames = []
        ordered_hotspots = []
        for index in seq_values:
            if 0 <= index < len(frames_raw):
                ordered_frames.append(frames_raw[index])
                ordered_hotspots.append(frame_hotspots[index])
        if ordered_frames:
            frames_raw = ordered_frames
            frame_hotspots = ordered_hotspots

    prepared_frames = [prepare_custom_cursor_image(frame) for frame in frames_raw]
    hotspot = next((value for value in frame_hotspots if value is not None), None)
    if hotspot is None:
        hotspot_x = prepared_frames[0].width // 2
        hotspot_y = prepared_frames[0].height // 2
    else:
        hotspot_x, hotspot_y = hotspot

    # Real Windows ANI frames can be larger than the rest of CursorSwarm's
    # manual shape library. Normalize them so Busy/Working do not look oversized.
    resized_frames = []
    new_hotspot_x = int(hotspot_x)
    new_hotspot_y = int(hotspot_y)
    for frame_index, frame in enumerate(prepared_frames):
        resized, scaled_hotspot_x, scaled_hotspot_y = resize_ani_frame_for_cursor(frame, hotspot_x, hotspot_y)
        resized_frames.append(resized)
        if frame_index == 0:
            new_hotspot_x = scaled_hotspot_x
            new_hotspot_y = scaled_hotspot_y
    prepared_frames = resized_frames
    hotspot_x = new_hotspot_x
    hotspot_y = new_hotspot_y

    if not rate_values:
        rate_values = [default_jif_rate] * len(prepared_frames)
    if len(rate_values) < len(prepared_frames):
        rate_values.extend([rate_values[-1] if rate_values else default_jif_rate] * (len(prepared_frames) - len(rate_values)))
    durations = [max(0.02, float(rate) / 60.0) for rate in rate_values[:len(prepared_frames)]]

    result = {
        'frames': prepared_frames,
        'hotspot_x': int(hotspot_x),
        'hotspot_y': int(hotspot_y),
        'durations': durations,
        'source_path': str(path_value or ''),
    }
    ANI_CURSOR_CACHE[cache_key] = result
    return result


def get_system_ani_cursor_path(shape_name):
    if shape_name == 'Busy / Loading':
        return get_windows_cursor_registry_path('Wait')
    if shape_name == 'Working in Background':
        return get_windows_cursor_registry_path('AppStarting')
    return ''


def get_animation_speed_factor():
    return float(CURSOR_ANIMATION_SPEED_FACTORS.get(CURSOR_ANIMATION_SPEED_MODE, 1.0))


def apply_animation_speed_to_durations(durations):
    factor = get_animation_speed_factor()
    return [max(0.02, float(duration) * factor) for duration in (durations or [])]


def cursor_animation_source_status_text():
    lines = []
    for shape_name in ("Busy / Loading", "Working in Background"):
        if not CURSOR_USE_REAL_WINDOWS_ANI:
            lines.append(f"{shape_name}: generated fallback (real Windows ANI disabled)")
            continue
        system_path = get_system_ani_cursor_path(shape_name)
        ani_result = parse_ani_cursor_file(system_path, shape_name=shape_name) if system_path else None
        if ani_result and ani_result.get('frames'):
            lines.append(f"{shape_name}: real Windows ANI ({Path(system_path).name}, {len(ani_result.get('frames', []))} frames)")
        elif system_path:
            lines.append(f"{shape_name}: generated fallback (could not parse {Path(system_path).name})")
        else:
            lines.append(f"{shape_name}: generated fallback (no Windows ANI path found)")
    lines.append(f"Animation speed: {CURSOR_ANIMATION_SPEED_MODE}")
    return "\n".join(lines)


def select_animation_frame_index(durations, now_value):
    if not durations:
        return 0
    total = sum(max(0.02, float(d)) for d in durations)
    if total <= 0:
        return 0
    cursor_time = float(now_value) % total
    elapsed = 0.0
    for idx, duration in enumerate(durations):
        elapsed += max(0.02, float(duration))
        if cursor_time < elapsed:
            return idx
    return max(0, len(durations) - 1)


def create_spinner_frame(size=32, phase=0.0):
    """Generate a Windows-like blue loading spinner frame.

    v13.9's first spinner used white dots, which worked technically but did not
    look like the familiar Windows blue/shiny loading ring. This version draws a
    cleaner anti-aliased blue arc spinner with a subtle glow and highlight.
    """
    render_scale = 4
    big = max(16, int(size)) * render_scale
    img = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    margin = int(big * 0.17)
    bbox = [margin, margin, big - margin, big - margin]
    stroke = max(2, int(big * 0.105))

    # Soft outer blue halo so the spinner feels shiny instead of flat.
    halo_bbox = [margin - stroke // 2, margin - stroke // 2, big - margin + stroke // 2, big - margin + stroke // 2]
    draw.arc(halo_bbox, start=0, end=360, fill=(37, 99, 235, 72), width=max(1, stroke // 2))

    # Faint background ring, similar to the Windows busy cursor base circle.
    draw.arc(bbox, start=0, end=360, fill=(96, 165, 250, 95), width=max(1, stroke // 3))

    # Rotating bright arc. Pillow angles are degrees; negative phase spins clockwise.
    start = int(math.degrees(phase)) % 360
    arc_layers = [
        (start, 86, (30, 144, 255, 235), stroke),
        (start + 18, 54, (125, 211, 252, 245), max(1, int(stroke * 0.72))),
        (start + 42, 24, (255, 255, 255, 220), max(1, int(stroke * 0.38))),
    ]
    for arc_start, extent, color, width in arc_layers:
        draw.arc(bbox, start=arc_start, end=arc_start + extent, fill=color, width=width)

    # Tiny bright head dot for a more Windows-like shine.
    head_angle = math.radians(start + 86)
    cx = big / 2
    cy = big / 2
    radius = (big - margin * 2) / 2
    hx = cx + math.cos(head_angle) * radius
    hy = cy + math.sin(head_angle) * radius
    dot_r = max(2, int(stroke * 0.34))
    draw.ellipse([hx - dot_r, hy - dot_r, hx + dot_r, hy + dot_r], fill=(232, 249, 255, 235))

    return img.resize((size, size), Image.Resampling.LANCZOS)


def create_busy_cursor_animation_frames(size=32, frame_count=16):
    frames = []
    for i in range(frame_count):
        phase = -math.tau * (i / frame_count)
        frames.append(create_spinner_frame(size=size, phase=phase))
    return frames, size // 2, size // 2


def create_working_cursor_animation_frames(size=32, frame_count=16):
    arrow_img, arrow_hotspot_x, arrow_hotspot_y = load_stock_cursor_shape_image("Arrow")
    if arrow_img is None:
        arrow_img = system_cursor_image.copy()
        arrow_hotspot_x, arrow_hotspot_y = int(system_hotspot_x), int(system_hotspot_y)
    base_arrow = prepare_custom_cursor_image(arrow_img)

    # Make the generated fallback follow the same layout as the real ANI hybrid:
    # larger spinner, upper-right of the arrow, and slightly overlapping.
    spinner_size = max(24, min(30, int(size * 0.88)))
    canvas_w = max(base_arrow.width + int(spinner_size * 0.72) + 4, size + 12)
    canvas_h = max(base_arrow.height + 4, size + 6)
    spinner_x = max(8, min(canvas_w - spinner_size, int(base_arrow.width * 0.58)))
    spinner_y = max(0, min(canvas_h - spinner_size, int(base_arrow.height * 0.02)))

    frames = []
    for i in range(frame_count):
        frame = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
        frame.alpha_composite(base_arrow, (0, 0))
        spinner = create_spinner_frame(size=spinner_size, phase=-math.tau * (i / frame_count))
        frame.alpha_composite(spinner, (spinner_x, spinner_y))
        frames.append(frame)
    return frames, int(arrow_hotspot_x), int(arrow_hotspot_y)


def get_shape_animation_frames(shape_name):
    shape_name = str(shape_name or "")
    if CURSOR_USE_REAL_WINDOWS_ANI:
        system_ani_path = get_system_ani_cursor_path(shape_name)
        if system_ani_path:
            ani_result = parse_ani_cursor_file(system_ani_path, shape_name=shape_name)
            if ani_result and ani_result.get('frames'):
                durations = apply_animation_speed_to_durations(ani_result.get('durations', []))
                return ani_result.get('frames'), ani_result.get('hotspot_x', 0), ani_result.get('hotspot_y', 0), durations, f"ani:{Path(system_ani_path).name}"

        # Fallback only: if AppStarting.ani is unavailable or cannot be parsed,
        # build Working in Background from the clean arrow and Busy spinner.
        if shape_name == "Working in Background":
            wait_ani_path = get_system_ani_cursor_path("Busy / Loading")
            if wait_ani_path:
                busy_result = parse_ani_cursor_file(wait_ani_path, shape_name="Busy / Loading")
                if busy_result and busy_result.get('frames'):
                    frames, hx, hy = create_working_frames_from_arrow_and_spinner(busy_result.get('frames'))
                    durations = busy_result.get('durations', [])[:len(frames)] or [CURSOR_ANIMATION_SPEED] * len(frames)
                    return frames, hx, hy, apply_animation_speed_to_durations(durations), f"ani-working-fallback:{Path(wait_ani_path).name}"
    if shape_name == "Busy / Loading":
        frames, hx, hy = create_busy_cursor_animation_frames()
        return frames, hx, hy, apply_animation_speed_to_durations([CURSOR_ANIMATION_SPEED] * len(frames)), 'generated:busy'
    if shape_name == "Working in Background":
        frames, hx, hy = create_working_cursor_animation_frames()
        return frames, hx, hy, apply_animation_speed_to_durations([CURSOR_ANIMATION_SPEED] * len(frames)), 'generated:working'
    return None, None, None, None, None


def get_current_cursor_source_image_and_hotspot():
    if CURSOR_SHAPE_MODE in CURSOR_SHAPE_ANIMATED:
        frames, hx, hy, durations, source_tag = get_shape_animation_frames(CURSOR_SHAPE_MODE)
        if frames:
            idx = select_animation_frame_index(durations, time.time())
            return frames[idx], int(hx), int(hy), f"{CURSOR_SHAPE_MODE}:{source_tag}:{idx}"
    return base_cursor_image, int(hotspot_x), int(hotspot_y), f"{CURSOR_SHAPE_MODE}:static"


def load_stock_cursor_shape_image(shape_name):
    generated_img, generated_hotspot_x, generated_hotspot_y = create_generated_manual_cursor_shape(shape_name)
    if generated_img is not None:
        return generated_img, generated_hotspot_x, generated_hotspot_y

    cursor_id = CURSOR_SHAPE_CURSOR_IDS.get(str(shape_name))
    if not cursor_id:
        return None, None, None

    # Important v13.9 fix:
    # When CursorSwarm replacement mode is active, SetSystemCursor has already
    # replaced Windows stock cursor IDs with transparent cursors. Calling
    # LoadCursorW at that moment can return the transparent cursor, causing shape
    # changes to apply but draw nothing. Prefer the original backed-up cursor
    # handles captured at startup, and only fall back to LoadCursorW if a backup
    # is unavailable.
    hcursor = cursor_backups.get(cursor_id)
    if not hcursor:
        hcursor = user32.LoadCursorW(None, cursor_id)

    if not hcursor:
        return None, None, None

    shape_hotspot_x, shape_hotspot_y = get_cursor_hotspot(hcursor)
    shape_img = draw_cursor_to_image(hcursor, bg=(0, 0, 0, 0))
    shape_img = remove_alpha_glow(shape_img, threshold=120)
    return shape_img, int(shape_hotspot_x), int(shape_hotspot_y)


def commit_cursor_shape_mode(shape_name):
    """Apply a manual Cursor Lab shape source.

    v13.9 starts the Manual Cursor Shape Library animation step. Working in
    Background and Busy / Loading now use real system ANI parsing when available, generated animated fallback spinners, ANI source status, and animation speed control.
    """
    global base_cursor_image, hotspot_x, hotspot_y
    global CUSTOM_CURSOR_ENABLED, CUSTOM_CURSOR_IMAGE_PATH, CUSTOM_CURSOR_SOURCE_LABEL, CURSOR_SHAPE_MODE

    shape_name = str(shape_name or "Captured System Cursor")

    if shape_name == "Custom Image File":
        if CUSTOM_CURSOR_ENABLED:
            CURSOR_SHAPE_MODE = "Custom Image File"
            return True
        shape_name = "Captured System Cursor"

    if shape_name == "Captured System Cursor":
        commit_reset_to_system_cursor_image()
        return True

    if shape_name in CURSOR_SHAPE_ANIMATED:
        anim_frames, anim_hotspot_x, anim_hotspot_y, _anim_durations, _anim_source = get_shape_animation_frames(shape_name)
        if anim_frames:
            shape_img = anim_frames[0]
            shape_hotspot_x, shape_hotspot_y = int(anim_hotspot_x), int(anim_hotspot_y)
        else:
            shape_img, shape_hotspot_x, shape_hotspot_y = load_stock_cursor_shape_image(shape_name)
    else:
        shape_img, shape_hotspot_x, shape_hotspot_y = load_stock_cursor_shape_image(shape_name)

    if shape_img is None:
        return False

    CUSTOM_CURSOR_ENABLED = False
    CUSTOM_CURSOR_IMAGE_PATH = ""
    CUSTOM_CURSOR_SOURCE_LABEL = shape_name
    CURSOR_SHAPE_MODE = shape_name
    base_cursor_image = shape_img
    hotspot_x = int(shape_hotspot_x)
    hotspot_y = int(shape_hotspot_y)
    invalidate_cursor_image_cache()
    return True


def ensure_cursor_image_for_scale(scale, role="fake", alpha_factor=1.0):
    scale = cursor_scale_key(scale)
    role = str(role or "fake")
    if role not in ("drawn", "fake", "motion_trail"):
        role = "fake"
    alpha_factor = cursor_alpha_key(clamp(alpha_factor, 0.03, 1.0))
    source_image, _hx, _hy, render_key = get_current_cursor_source_image_and_hotspot()
    movement_color_key = movement_effect_cache_key("trail") if role == "motion_trail" else None
    cache_key = (scale, role, alpha_factor, render_key, movement_color_key)

    if cache_key not in tk_cursor_images:
        new_w = max(1, round(source_image.width * scale))
        new_h = max(1, round(source_image.height * scale))

        resized = source_image.resize((new_w, new_h), Image.Resampling.NEAREST)

        if not CUSTOM_CURSOR_ENABLED:
            resized = remove_alpha_glow(resized, threshold=120)

        if role == "motion_trail":
            resized = apply_movement_effect_tint_to_image(resized, "trail")
        else:
            resized = apply_cursor_tint_to_image(resized, role)

        if alpha_factor < 0.99:
            resized = resized.convert("RGBA")
            alpha = resized.getchannel("A").point(lambda value: int(value * alpha_factor))
            resized.putalpha(alpha)

        tk_cursor_images[cache_key] = ImageTk.PhotoImage(resized)

    return tk_cursor_images[cache_key]


for scale in sorted(set(CURSOR_SCALE_PRESETS + [REAL_DRAWN_CURSOR_SCALE])):
    ensure_cursor_image_for_scale(scale, "fake")
    ensure_cursor_image_for_scale(scale, "drawn")


def draw_cursor_image(x, y, scale, role="fake", alpha_factor=1.0):
    if str(role or "") == "motion_trail":
        # v13.9 cleanup: Motion Trail colour customization is disabled for now.
        # The trail now uses the current Cursor Lab drawn cursor image exactly,
        # which is stable and avoids the old partial-purple trail bug.
        image = ensure_cursor_image_for_scale(scale, "drawn", alpha_factor=alpha_factor)
        pad = cursor_outline_padding_for_role("drawn")
        canvas.create_image(round(x - pad), round(y - pad), image=image, anchor="nw")
        return

    image = ensure_cursor_image_for_scale(scale, role, alpha_factor=alpha_factor)
    pad = cursor_outline_padding_for_role(role)
    canvas.create_image(round(x - pad), round(y - pad), image=image, anchor="nw")


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
last_motion_time = time.time()
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
native_dialog_open = False
safe_shutdown_in_progress = False


def restore_and_quit():
    """Quit with defensive cursor restore even if one cleanup step fails."""
    global safe_shutdown_in_progress

    if safe_shutdown_in_progress:
        return

    safe_shutdown_in_progress = True

    try:
        if "save_app_settings" in globals():
            try:
                save_app_settings(update_last_state=True)
            except Exception as exc:
                print(f"CursorSwarm warning: could not save settings during quit: {exc}")

        try:
            set_visible_mode()
        except Exception as exc:
            print(f"CursorSwarm warning: visible cursor restore failed during quit: {exc}")

        try:
            restore_cursors_safely()
        except Exception as exc:
            print(f"CursorSwarm warning: backup cursor restore failed during quit: {exc}")

        try:
            root.destroy()
        except Exception as exc:
            print(f"CursorSwarm warning: root destroy failed during quit: {exc}")
            try:
                sys.exit(0)
            except Exception:
                os._exit(0)
    finally:
        safe_shutdown_in_progress = False



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
            "fake_cursor_scale_multiplier": float(FAKE_CURSOR_SCALE_MULTIPLIER),
            "cursor_tint_enabled": bool(CURSOR_TINT_ENABLED),
            "cursor_tint_style": str(CURSOR_TINT_STYLE),
            "cursor_tint_multi_preset": str(CURSOR_TINT_MULTI_PRESET),
            "cursor_tint_color": str(CURSOR_TINT_COLOR),
            "cursor_tint_strength": float(CURSOR_TINT_STRENGTH),
            "cursor_tint_bright_neon": bool(CURSOR_TINT_BRIGHT_NEON),
            "cursor_tint_neon_brightness": float(CURSOR_TINT_NEON_BRIGHTNESS),
            "cursor_tint_apply_drawn": bool(CURSOR_TINT_APPLY_DRAWN),
            "cursor_tint_apply_fake": bool(CURSOR_TINT_APPLY_FAKE),
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
    global FAKE_CURSOR_SCALE_MULTIPLIER, CURSOR_TINT_ENABLED, CURSOR_TINT_STYLE, CURSOR_TINT_MULTI_PRESET, CURSOR_TINT_COLOR, CURSOR_TINT_STRENGTH, CURSOR_TINT_BRIGHT_NEON, CURSOR_TINT_NEON_BRIGHTNESS
    global CURSOR_TINT_APPLY_DRAWN, CURSOR_TINT_APPLY_FAKE, CURSOR_TINT_BLACK_OUTLINE, CURSOR_TINT_OUTLINE_THICKNESS

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
    FAKE_CURSOR_SCALE_MULTIPLIER = max(0.25, min(3.0, float(state.get("fake_cursor_scale_multiplier", FAKE_CURSOR_SCALE_MULTIPLIER))))
    CURSOR_TINT_ENABLED = bool(state.get("cursor_tint_enabled", CURSOR_TINT_ENABLED))
    CURSOR_TINT_STYLE = str(state.get("cursor_tint_style", CURSOR_TINT_STYLE))
    CURSOR_TINT_MULTI_PRESET = str(state.get("cursor_tint_multi_preset", CURSOR_TINT_MULTI_PRESET))
    CURSOR_TINT_COLOR = str(state.get("cursor_tint_color", CURSOR_TINT_COLOR))
    CURSOR_TINT_STRENGTH = max(0.0, min(1.0, float(state.get("cursor_tint_strength", CURSOR_TINT_STRENGTH))))
    CURSOR_TINT_BRIGHT_NEON = bool(state.get("cursor_tint_bright_neon", CURSOR_TINT_BRIGHT_NEON))
    CURSOR_TINT_NEON_BRIGHTNESS = max(1.0, min(4.0, float(state.get("cursor_tint_neon_brightness", CURSOR_TINT_NEON_BRIGHTNESS))))
    CURSOR_TINT_APPLY_DRAWN = bool(state.get("cursor_tint_apply_drawn", CURSOR_TINT_APPLY_DRAWN))
    CURSOR_TINT_APPLY_FAKE = bool(state.get("cursor_tint_apply_fake", CURSOR_TINT_APPLY_FAKE))
    invalidate_cursor_image_cache()
    ensure_cursor_image_for_scale(REAL_DRAWN_CURSOR_SCALE, "drawn")

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

    if cursor_lab_drawn_replacement_active() and not bool(drawn_real_var.get()):
        show_drawn_real_cursor = True
        drawn_real_var.set(True)
        show_control_panel_hint(
            "Drawn cursor cannot be hidden while Cursor Lab replacement mode is active.",
            duration=5.0,
        )
        return

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
    global show_drawn_real_cursor

    manual_offset_x = safe_int_from_var(manual_offset_x_var, manual_offset_x, minimum=-200, maximum=200)
    manual_offset_y = safe_int_from_var(manual_offset_y_var, manual_offset_y, minimum=-200, maximum=200)
    REAL_DRAWN_CURSOR_SCALE = safe_float_from_var(real_cursor_scale_var, REAL_DRAWN_CURSOR_SCALE, minimum=0.25, maximum=3.0)
    REAL_DRAWN_CURSOR_SCALE = round(REAL_DRAWN_CURSOR_SCALE, 2)

    invalidate_cursor_image_cache()
    ensure_cursor_image_for_scale(REAL_DRAWN_CURSOR_SCALE, "drawn")

    if cursor_lab_drawn_replacement_active():
        show_drawn_real_cursor = True
        enforce_cursor_lab_replacement_visibility()

    CURRENT_PRESET_NAME = "Custom Cursor"
    set_cursor_polish_vars_from_globals()
    update_panel_status()


def reset_cursor_polish_fields_to_current():
    set_cursor_polish_vars_from_globals()


def set_cursor_lab_vars_from_globals():
    if "fake_cursor_scale_multiplier_var" not in globals():
        return

    fake_cursor_scale_multiplier_var.set(float(FAKE_CURSOR_SCALE_MULTIPLIER))
    fake_cursor_scale_multiplier_label_var.set(f"{FAKE_CURSOR_SCALE_MULTIPLIER:.2f}x")
    cursor_tint_enabled_var.set(bool(CURSOR_TINT_ENABLED))
    cursor_tint_style_var.set(str(CURSOR_TINT_STYLE))
    cursor_tint_multi_preset_var.set(str(CURSOR_TINT_MULTI_PRESET))
    cursor_tint_color_var.set(str(CURSOR_TINT_COLOR))
    cursor_tint_strength_var.set(float(CURSOR_TINT_STRENGTH))
    cursor_tint_strength_label_var.set(f"{CURSOR_TINT_STRENGTH:.2f}")
    cursor_tint_bright_neon_var.set(bool(CURSOR_TINT_BRIGHT_NEON))
    cursor_tint_neon_brightness_var.set(float(CURSOR_TINT_NEON_BRIGHTNESS))
    cursor_tint_neon_brightness_label_var.set(f"{CURSOR_TINT_NEON_BRIGHTNESS:.2f}x")
    cursor_tint_black_outline_var.set(bool(CURSOR_TINT_BLACK_OUTLINE))
    cursor_tint_outline_thickness_var.set(int(CURSOR_TINT_OUTLINE_THICKNESS))
    cursor_tint_outline_thickness_label_var.set(f"{CURSOR_TINT_OUTLINE_THICKNESS}px")
    cursor_tint_apply_drawn_var.set(bool(CURSOR_TINT_APPLY_DRAWN))
    cursor_tint_apply_fake_var.set(bool(CURSOR_TINT_APPLY_FAKE))
    custom_cursor_enabled_var.set(bool(CUSTOM_CURSOR_ENABLED))
    custom_cursor_path_var.set(str(CUSTOM_CURSOR_IMAGE_PATH))
    cursor_shape_mode_var.set(str(CURSOR_SHAPE_MODE))
    cursor_use_real_ani_var.set(bool(CURSOR_USE_REAL_WINDOWS_ANI))
    cursor_animation_speed_mode_var.set(str(CURSOR_ANIMATION_SPEED_MODE))
    cursor_animation_source_status_var.set(cursor_animation_source_status_text())
    custom_cursor_hotspot_mode_var.set(str(CUSTOM_CURSOR_HOTSPOT_MODE))
    idle_effect_enabled_var.set(bool(IDLE_EFFECT_ENABLED))
    idle_effect_style_var.set(str(IDLE_EFFECT_STYLE))
    idle_effect_delay_var.set(float(IDLE_EFFECT_DELAY))
    idle_effect_delay_label_var.set(f"{IDLE_EFFECT_DELAY:.2f}s")
    idle_effect_strength_var.set(float(IDLE_EFFECT_STRENGTH))
    idle_effect_strength_label_var.set(f"{IDLE_EFFECT_STRENGTH:.2f}")
    idle_neon_enabled_var.set(bool(IDLE_EFFECT_NEON_ENABLED))
    idle_neon_preset_var.set(str(IDLE_EFFECT_NEON_PRESET))
    idle_neon_color_var.set(str(IDLE_EFFECT_NEON_COLOR))
    custom_cursor_status_var.set(cursor_lab_status_text())


def cursor_lab_status_text():
    source = CUSTOM_CURSOR_SOURCE_LABEL or (Path(CUSTOM_CURSOR_IMAGE_PATH).name if CUSTOM_CURSOR_IMAGE_PATH else "System cursor")
    tint = "ON" if CURSOR_TINT_ENABLED else "OFF"
    custom = "Custom image" if CUSTOM_CURSOR_ENABLED else "System cursor"
    idle_text = "ON" if IDLE_EFFECT_ENABLED and IDLE_EFFECT_STYLE != "Disabled" else "OFF"
    return (
        f"Source: {custom} ({source}) | Shape: {CURSOR_SHAPE_MODE}\n"
        f"Active image size: {base_cursor_image.width}x{base_cursor_image.height} | Hotspot: ({hotspot_x}, {hotspot_y}) | Mode: {CUSTOM_CURSOR_HOTSPOT_MODE}\n"
        f"Drawn scale: {REAL_DRAWN_CURSOR_SCALE:.2f}x | Fake scale multiplier: {FAKE_CURSOR_SCALE_MULTIPLIER:.2f}x\n"
        f"Tint: {tint} | Style: {CURSOR_TINT_STYLE} | Preset: {CURSOR_TINT_MULTI_PRESET} | Color: {CURSOR_TINT_COLOR} | Strength: {CURSOR_TINT_STRENGTH:.2f} | Bright Neon: {CURSOR_TINT_BRIGHT_NEON} | Neon Intensity: {CURSOR_TINT_NEON_BRIGHTNESS:.2f}x | Black Outline: {CURSOR_TINT_BLACK_OUTLINE} ({CURSOR_TINT_OUTLINE_THICKNESS}px) | Drawn: {CURSOR_TINT_APPLY_DRAWN} | Fake: {CURSOR_TINT_APPLY_FAKE}\n"
        f"Idle Effects: {idle_text} | Style: {IDLE_EFFECT_STYLE} | Delay: {IDLE_EFFECT_DELAY:.2f}s | Strength: {IDLE_EFFECT_STRENGTH:.2f} | Neon: {IDLE_EFFECT_NEON_PRESET} ({IDLE_EFFECT_NEON_COLOR})"
    )


def ui_set_fake_cursor_scale_multiplier(value):
    fake_cursor_scale_multiplier_label_var.set(f"{float(value):.2f}x")
    mark_cursor_lab_pending("Fake cursor size changed. Click Apply Cursor Lab to activate it.")


def ui_set_cursor_tint_strength(value):
    cursor_tint_strength_label_var.set(f"{float(value):.2f}")
    mark_cursor_lab_pending("Tint strength changed. Click Apply Cursor Lab to activate it.")


def ui_set_cursor_tint_neon_brightness(value):
    cursor_tint_neon_brightness_label_var.set(f"{float(value):.2f}x")
    mark_cursor_lab_pending("Neon intensity changed. Click Apply Cursor Lab to activate it.")


def ui_set_cursor_tint_outline_thickness(value):
    try:
        cursor_tint_outline_thickness_label_var.set(f"{int(round(float(value)))}px")
    except Exception:
        cursor_tint_outline_thickness_label_var.set("2px")
    mark_cursor_lab_pending("Black outline thickness changed. Click Apply Cursor Lab to activate it.")


def ui_set_drawn_cursor_scale(value):
    real_cursor_scale_label_var.set(f"{float(value):.2f}x")
    mark_cursor_lab_pending("Drawn cursor size changed. Click Apply Cursor Lab to activate it.")


def ui_set_idle_effect_delay(value):
    idle_effect_delay_label_var.set(f"{float(value):.2f}s")
    mark_cursor_lab_pending("Idle effect delay changed. Click Apply Cursor Lab to activate it.")


def ui_set_idle_effect_strength(value):
    idle_effect_strength_label_var.set(f"{float(value):.2f}")
    mark_cursor_lab_pending("Idle effect strength changed. Click Apply Cursor Lab to activate it.")


def on_idle_effect_style_change(_value=None):
    mark_cursor_lab_pending("Idle effect style changed. Click Apply Cursor Lab to activate it.")


def on_idle_neon_preset_change(_value=None):
    preset_name = idle_neon_preset_var.get() or "Cyberpunk Neon"
    idle_neon_color_var.set(get_neon_preset_primary_color(preset_name))
    mark_cursor_lab_pending("Fancy neon preset changed. Click Apply Cursor Lab to activate it.")


def choose_idle_neon_color():
    chosen = safe_colorchooser_askcolor(
        parent=control_panel if "control_panel" in globals() else root,
        color=idle_neon_color_var.get(),
        title="Choose idle neon color",
    )
    if chosen and chosen[1]:
        fixed_hex, _rgb = parse_hex_color(chosen[1])
        fixed_hex = sanitize_neon_color(fixed_hex)
        idle_neon_color_var.set(fixed_hex)
        mark_cursor_lab_pending("Idle neon color changed. Click Apply Cursor Lab to activate it.")


def copy_neon_preset_to_tint():
    preset_name = idle_neon_preset_var.get() or "Cyberpunk Neon"
    fixed_hex = get_neon_preset_primary_color(preset_name)
    cursor_tint_color_var.set(fixed_hex)
    mark_cursor_lab_pending("Neon preset primary color copied to tint. Click Apply Cursor Lab to activate it.")


def on_cursor_tint_style_change(_value=None):
    mark_cursor_lab_pending("Tint style changed. Click Apply Cursor Lab to activate it.")


def on_cursor_tint_multi_preset_change(_value=None):
    mark_cursor_lab_pending("Multi-colour neon preset changed. Click Apply Cursor Lab to activate it.")


def copy_multi_preset_primary_to_tint():
    preset_name = cursor_tint_multi_preset_var.get() or "Cyberpunk Neon"
    cursor_tint_color_var.set(get_neon_preset_primary_color(preset_name))
    mark_cursor_lab_pending("Multi-colour preset primary color copied to tint. Click Apply Cursor Lab to activate it.")


def on_cursor_shape_mode_change(value=None):
    global PENDING_CUSTOM_CURSOR_IMAGE, PENDING_CUSTOM_CURSOR_IMAGE_PATH
    global PENDING_CUSTOM_CURSOR_SOURCE_LABEL, PENDING_RESET_TO_SYSTEM_CURSOR

    selected = str(value or (cursor_shape_mode_var.get() if "cursor_shape_mode_var" in globals() else "Captured System Cursor"))

    if selected != "Custom Image File":
        PENDING_CUSTOM_CURSOR_IMAGE = None
        PENDING_CUSTOM_CURSOR_IMAGE_PATH = ""
        PENDING_CUSTOM_CURSOR_SOURCE_LABEL = ""
        PENDING_RESET_TO_SYSTEM_CURSOR = (selected == "Captured System Cursor")
        if "custom_cursor_path_var" in globals() and selected != CURSOR_SHAPE_MODE:
            custom_cursor_path_var.set("")

    if "cursor_animation_source_status_var" in globals():
        try:
            cursor_animation_source_status_var.set(cursor_animation_source_status_text())
        except Exception:
            pass
    mark_cursor_lab_pending("Cursor shape changed. Click Apply Cursor Lab to activate it.")


def choose_cursor_tint_color():
    chosen = safe_colorchooser_askcolor(
        parent=control_panel if "control_panel" in globals() else root,
        color=cursor_tint_color_var.get(),
        title="Choose cursor tint color",
    )
    if chosen and chosen[1]:
        fixed_hex, _rgb = parse_hex_color(chosen[1])
        cursor_tint_color_var.set(fixed_hex)
        mark_cursor_lab_pending("Tint color changed. Click Apply Cursor Lab to activate it.")


def apply_cursor_lab_from_ui(show_message=False):
    global REAL_DRAWN_CURSOR_SCALE, FAKE_CURSOR_SCALE_MULTIPLIER
    global CURSOR_TINT_ENABLED, CURSOR_TINT_STYLE, CURSOR_TINT_MULTI_PRESET, CURSOR_TINT_COLOR, CURSOR_TINT_STRENGTH, CURSOR_TINT_BRIGHT_NEON, CURSOR_TINT_NEON_BRIGHTNESS, CURSOR_TINT_BLACK_OUTLINE, CURSOR_TINT_OUTLINE_THICKNESS
    global CURSOR_TINT_APPLY_DRAWN, CURSOR_TINT_APPLY_FAKE, CUSTOM_CURSOR_HOTSPOT_MODE, CURRENT_PRESET_NAME
    global CUSTOM_CURSOR_ENABLED, CUSTOM_CURSOR_IMAGE_PATH, CUSTOM_CURSOR_SOURCE_LABEL, CURSOR_SHAPE_MODE
    global CURSOR_USE_REAL_WINDOWS_ANI, CURSOR_ANIMATION_SPEED_MODE
    global PENDING_CUSTOM_CURSOR_IMAGE, PENDING_CUSTOM_CURSOR_IMAGE_PATH, PENDING_CUSTOM_CURSOR_SOURCE_LABEL
    global PENDING_RESET_TO_SYSTEM_CURSOR, CURSOR_LAB_DIRTY, show_drawn_real_cursor
    global IDLE_EFFECT_ENABLED, IDLE_EFFECT_STYLE, IDLE_EFFECT_DELAY, IDLE_EFFECT_STRENGTH
    global IDLE_EFFECT_NEON_ENABLED, IDLE_EFFECT_NEON_PRESET, IDLE_EFFECT_NEON_COLOR

    # Drawn cursor scale was the missing piece causing Cursor Lab resize to do
    # nothing. It must be copied from the shared slider into the active global.
    REAL_DRAWN_CURSOR_SCALE = safe_float_from_var(real_cursor_scale_var, REAL_DRAWN_CURSOR_SCALE, minimum=0.25, maximum=3.0)
    REAL_DRAWN_CURSOR_SCALE = round(REAL_DRAWN_CURSOR_SCALE, 2)

    FAKE_CURSOR_SCALE_MULTIPLIER = safe_float_from_var(fake_cursor_scale_multiplier_var, FAKE_CURSOR_SCALE_MULTIPLIER, minimum=0.25, maximum=3.0)
    FAKE_CURSOR_SCALE_MULTIPLIER = round(FAKE_CURSOR_SCALE_MULTIPLIER, 2)

    CURSOR_TINT_ENABLED = bool(cursor_tint_enabled_var.get())
    CURSOR_TINT_STYLE = cursor_tint_style_var.get() or "Single Colour"
    if CURSOR_TINT_STYLE not in CURSOR_TINT_STYLE_OPTIONS:
        CURSOR_TINT_STYLE = "Single Colour"
    CURSOR_TINT_MULTI_PRESET = stable_neon_preset_name(cursor_tint_multi_preset_var.get())
    CURSOR_TINT_COLOR, _rgb = parse_hex_color(cursor_tint_color_var.get())
    CURSOR_TINT_STRENGTH = safe_float_from_var(cursor_tint_strength_var, CURSOR_TINT_STRENGTH, minimum=0.0, maximum=1.0)
    CURSOR_TINT_STRENGTH = round(CURSOR_TINT_STRENGTH, 2)
    CURSOR_TINT_BRIGHT_NEON = bool(cursor_tint_bright_neon_var.get())
    CURSOR_TINT_NEON_BRIGHTNESS = round(safe_float_from_var(cursor_tint_neon_brightness_var, CURSOR_TINT_NEON_BRIGHTNESS, minimum=1.0, maximum=4.0), 2)
    CURSOR_TINT_BLACK_OUTLINE = bool(cursor_tint_black_outline_var.get())
    CURSOR_TINT_OUTLINE_THICKNESS = safe_int_from_var(cursor_tint_outline_thickness_var, CURSOR_TINT_OUTLINE_THICKNESS, minimum=1, maximum=6)
    CURSOR_TINT_APPLY_DRAWN = bool(cursor_tint_apply_drawn_var.get())
    CURSOR_TINT_APPLY_FAKE = bool(cursor_tint_apply_fake_var.get())

    IDLE_EFFECT_ENABLED = bool(idle_effect_enabled_var.get())
    IDLE_EFFECT_STYLE = idle_effect_style_var.get() or "Disabled"
    if IDLE_EFFECT_STYLE not in IDLE_EFFECT_OPTIONS:
        IDLE_EFFECT_STYLE = "Disabled"
    IDLE_EFFECT_DELAY = round(safe_float_from_var(idle_effect_delay_var, IDLE_EFFECT_DELAY, minimum=0.2, maximum=6.0), 2)
    IDLE_EFFECT_STRENGTH = round(safe_float_from_var(idle_effect_strength_var, IDLE_EFFECT_STRENGTH, minimum=0.0, maximum=1.0), 2)
    IDLE_EFFECT_NEON_ENABLED = bool(idle_neon_enabled_var.get())
    IDLE_EFFECT_NEON_PRESET = stable_neon_preset_name(idle_neon_preset_var.get())
    IDLE_EFFECT_NEON_COLOR = sanitize_neon_color(idle_neon_color_var.get() or get_neon_preset_primary_color(IDLE_EFFECT_NEON_PRESET))

    CURSOR_USE_REAL_WINDOWS_ANI = bool(cursor_use_real_ani_var.get())
    CURSOR_ANIMATION_SPEED_MODE = cursor_animation_speed_mode_var.get() or "Normal"
    if CURSOR_ANIMATION_SPEED_MODE not in CURSOR_ANIMATION_SPEED_OPTIONS:
        CURSOR_ANIMATION_SPEED_MODE = "Normal"

    CUSTOM_CURSOR_HOTSPOT_MODE = custom_cursor_hotspot_mode_var.get() or "Top-left"
    selected_cursor_shape = cursor_shape_mode_var.get() or "Captured System Cursor"

    if PENDING_RESET_TO_SYSTEM_CURSOR:
        commit_reset_to_system_cursor_image()
        PENDING_RESET_TO_SYSTEM_CURSOR = False

    if PENDING_CUSTOM_CURSOR_IMAGE is not None:
        CUSTOM_CURSOR_ENABLED = True
        CUSTOM_CURSOR_IMAGE_PATH = str(PENDING_CUSTOM_CURSOR_IMAGE_PATH)
        CUSTOM_CURSOR_SOURCE_LABEL = str(PENDING_CUSTOM_CURSOR_SOURCE_LABEL or "Custom image")
        set_active_cursor_image(
            PENDING_CUSTOM_CURSOR_IMAGE,
            hotspot_mode=CUSTOM_CURSOR_HOTSPOT_MODE,
            source_label=CUSTOM_CURSOR_SOURCE_LABEL,
        )
        CURSOR_SHAPE_MODE = "Custom Image File"
        PENDING_CUSTOM_CURSOR_IMAGE = None
        PENDING_CUSTOM_CURSOR_IMAGE_PATH = ""
        PENDING_CUSTOM_CURSOR_SOURCE_LABEL = ""
    elif selected_cursor_shape != "Custom Image File":
        if selected_cursor_shape != CURSOR_SHAPE_MODE or selected_cursor_shape == "Captured System Cursor":
            if not commit_cursor_shape_mode(selected_cursor_shape):
                safe_messagebox_showerror("Cursor Shape Failed", f"Could not load the selected cursor shape:\n\n{selected_cursor_shape}")
                commit_reset_to_system_cursor_image()
    elif CUSTOM_CURSOR_ENABLED:
        set_custom_cursor_hotspot_from_mode()
        CURSOR_SHAPE_MODE = "Custom Image File"

    invalidate_cursor_image_cache()
    ensure_cursor_image_for_scale(REAL_DRAWN_CURSOR_SCALE, "drawn")
    ensure_cursor_image_for_scale(REAL_DRAWN_CURSOR_SCALE * FAKE_CURSOR_SCALE_MULTIPLIER, "fake")

    if cursor_lab_drawn_replacement_active():
        show_drawn_real_cursor = True
        enforce_cursor_lab_replacement_visibility()
    else:
        # If a previous Cursor Lab replacement mode hid the real cursor, turning
        # tint/custom/idle effects off must return to a safe visible cursor state.
        # Also keep the drawn cursor enabled so Ctrl+Alt+H starts from a visible state.
        show_drawn_real_cursor = True
        set_visible_mode()

    CURRENT_PRESET_NAME = "Cursor Lab Custom"
    CURSOR_LAB_DIRTY = False
    set_cursor_polish_vars_from_globals()
    set_cursor_lab_vars_from_globals()
    update_panel_status()
    refresh_swarm_summary()

    if show_message:
        # Do not use a blocking message box here. A modal "Applied" dialog can
        # steal focus or sit behind the Control Panel, and Tkinter will not draw
        # the updated cursor until that hidden dialog is dismissed. Use the
        # Cursor Lab status area instead.
        try:
            custom_cursor_status_var.set(cursor_lab_status_text() + "\nStatus: Cursor Lab visual settings applied.")
        except Exception:
            pass
        try:
            prepare_dialog_parent(control_panel if "control_panel" in globals() else root)
        except Exception:
            pass


def reset_cursor_lab_visuals():
    global FAKE_CURSOR_SCALE_MULTIPLIER, CURSOR_TINT_ENABLED, CURSOR_TINT_STYLE, CURSOR_TINT_MULTI_PRESET, CURSOR_TINT_COLOR, CURSOR_TINT_STRENGTH, CURSOR_TINT_BRIGHT_NEON, CURSOR_TINT_NEON_BRIGHTNESS
    global CURSOR_TINT_APPLY_DRAWN, CURSOR_TINT_APPLY_FAKE, CURSOR_TINT_BLACK_OUTLINE, CURSOR_TINT_OUTLINE_THICKNESS
    global IDLE_EFFECT_ENABLED, IDLE_EFFECT_STYLE, IDLE_EFFECT_DELAY, IDLE_EFFECT_STRENGTH
    global IDLE_EFFECT_NEON_ENABLED, IDLE_EFFECT_NEON_PRESET, IDLE_EFFECT_NEON_COLOR

    FAKE_CURSOR_SCALE_MULTIPLIER = 1.0
    CURSOR_TINT_ENABLED = False
    CURSOR_TINT_STYLE = "Single Colour"
    CURSOR_TINT_MULTI_PRESET = "Cyberpunk Neon"
    CURSOR_TINT_COLOR = "#8b5cf6"
    CURSOR_TINT_STRENGTH = 0.65
    CURSOR_TINT_BRIGHT_NEON = False
    CURSOR_TINT_NEON_BRIGHTNESS = 1.20
    CURSOR_TINT_APPLY_DRAWN = True
    CURSOR_TINT_APPLY_FAKE = True
    CURSOR_TINT_BLACK_OUTLINE = False
    CURSOR_TINT_OUTLINE_THICKNESS = 2
    IDLE_EFFECT_ENABLED = False
    IDLE_EFFECT_STYLE = "Disabled"
    IDLE_EFFECT_DELAY = 1.20
    IDLE_EFFECT_STRENGTH = 0.55
    IDLE_EFFECT_NEON_ENABLED = True
    IDLE_EFFECT_NEON_PRESET = "Cyberpunk Neon"
    IDLE_EFFECT_NEON_COLOR = get_neon_preset_primary_color(IDLE_EFFECT_NEON_PRESET)
    invalidate_cursor_image_cache()
    set_cursor_lab_vars_from_globals()
    update_panel_status()
    refresh_swarm_summary()


def disable_cursor_lab_replacement_mode():
    """Return to the normal Windows cursor without resetting fake-only settings.

    This turns off the drawn cursor replacement behavior caused by custom cursor
    source, drawn tint, drawn resize, or manual drawn offset. Fake cursor settings
    such as fake scale and fake tint can remain active.
    """
    global REAL_DRAWN_CURSOR_SCALE, manual_offset_x, manual_offset_y
    global CURSOR_TINT_ENABLED, CURSOR_TINT_APPLY_DRAWN
    global CUSTOM_CURSOR_ENABLED, CUSTOM_CURSOR_IMAGE_PATH, CUSTOM_CURSOR_SOURCE_LABEL
    global PENDING_CUSTOM_CURSOR_IMAGE, PENDING_CUSTOM_CURSOR_IMAGE_PATH
    global PENDING_CUSTOM_CURSOR_SOURCE_LABEL, PENDING_RESET_TO_SYSTEM_CURSOR
    global show_drawn_real_cursor, CURRENT_PRESET_NAME, CURSOR_LAB_DIRTY

    PENDING_CUSTOM_CURSOR_IMAGE = None
    PENDING_CUSTOM_CURSOR_IMAGE_PATH = ""
    PENDING_CUSTOM_CURSOR_SOURCE_LABEL = ""
    PENDING_RESET_TO_SYSTEM_CURSOR = False

    commit_reset_to_system_cursor_image()

    REAL_DRAWN_CURSOR_SCALE = 1.0
    manual_offset_x = 0
    manual_offset_y = 0

    CURSOR_TINT_APPLY_DRAWN = False
    if not CURSOR_TINT_APPLY_FAKE:
        CURSOR_TINT_ENABLED = False

    show_drawn_real_cursor = True
    CURRENT_PRESET_NAME = "Cursor Lab Custom"
    CURSOR_LAB_DIRTY = False

    invalidate_cursor_image_cache()
    set_visible_mode()
    set_cursor_polish_vars_from_globals()
    set_cursor_lab_vars_from_globals()
    sync_ui_vars()
    update_panel_status()
    refresh_swarm_summary()

    safe_messagebox_showinfo(
        "Replacement Mode Off",
        "Cursor Lab replacement mode is off. The normal Windows cursor is visible again.\n\n"
        "Fake cursor size/tint settings were kept where possible."
    )


def apply_cursor_lab_config(config):
    global FAKE_CURSOR_SCALE_MULTIPLIER, CURSOR_TINT_ENABLED, CURSOR_TINT_STYLE, CURSOR_TINT_MULTI_PRESET, CURSOR_TINT_COLOR, CURSOR_TINT_STRENGTH, CURSOR_TINT_BRIGHT_NEON, CURSOR_TINT_NEON_BRIGHTNESS
    global CURSOR_TINT_BLACK_OUTLINE, CURSOR_TINT_OUTLINE_THICKNESS, CURSOR_TINT_APPLY_DRAWN, CURSOR_TINT_APPLY_FAKE, CUSTOM_CURSOR_HOTSPOT_MODE, CURSOR_SHAPE_MODE

    try:
        FAKE_CURSOR_SCALE_MULTIPLIER = max(0.25, min(3.0, float(config.get("fake_cursor_scale_multiplier", FAKE_CURSOR_SCALE_MULTIPLIER))))
    except (TypeError, ValueError):
        pass

    CURSOR_TINT_ENABLED = bool(config.get("cursor_tint_enabled", CURSOR_TINT_ENABLED))
    CURSOR_TINT_STYLE = str(config.get("cursor_tint_style", CURSOR_TINT_STYLE))
    CURSOR_TINT_MULTI_PRESET = str(config.get("cursor_tint_multi_preset", CURSOR_TINT_MULTI_PRESET))
    CURSOR_TINT_COLOR = str(config.get("cursor_tint_color", CURSOR_TINT_COLOR))
    try:
        CURSOR_TINT_STRENGTH = max(0.0, min(1.0, float(config.get("cursor_tint_strength", CURSOR_TINT_STRENGTH))))
    except (TypeError, ValueError):
        pass
    globals()["CURSOR_TINT_BRIGHT_NEON"] = bool(config.get("cursor_tint_bright_neon", CURSOR_TINT_BRIGHT_NEON))
    globals()["CURSOR_TINT_NEON_BRIGHTNESS"] = max(1.0, min(4.0, float(config.get("cursor_tint_neon_brightness", CURSOR_TINT_NEON_BRIGHTNESS))))
    CURSOR_TINT_BLACK_OUTLINE = bool(config.get("cursor_tint_black_outline", CURSOR_TINT_BLACK_OUTLINE))
    try:
        CURSOR_TINT_OUTLINE_THICKNESS = max(1, min(6, int(config.get("cursor_tint_outline_thickness", CURSOR_TINT_OUTLINE_THICKNESS))))
    except (TypeError, ValueError):
        pass
    CURSOR_TINT_APPLY_DRAWN = bool(config.get("cursor_tint_apply_drawn", CURSOR_TINT_APPLY_DRAWN))
    CURSOR_TINT_APPLY_FAKE = bool(config.get("cursor_tint_apply_fake", CURSOR_TINT_APPLY_FAKE))
    CUSTOM_CURSOR_HOTSPOT_MODE = str(config.get("custom_cursor_hotspot_mode", CUSTOM_CURSOR_HOTSPOT_MODE))
    CURSOR_SHAPE_MODE = str(config.get("cursor_shape_mode", CURSOR_SHAPE_MODE))
    globals()["CURSOR_USE_REAL_WINDOWS_ANI"] = bool(config.get("cursor_use_real_windows_ani", CURSOR_USE_REAL_WINDOWS_ANI))
    globals()["CURSOR_ANIMATION_SPEED_MODE"] = str(config.get("cursor_animation_speed_mode", CURSOR_ANIMATION_SPEED_MODE))
    if globals()["CURSOR_ANIMATION_SPEED_MODE"] not in CURSOR_ANIMATION_SPEED_OPTIONS:
        globals()["CURSOR_ANIMATION_SPEED_MODE"] = "Normal"

    custom_enabled = bool(config.get("custom_cursor_enabled", CUSTOM_CURSOR_ENABLED))
    custom_path = str(config.get("custom_cursor_image_path", "") or "")

    if custom_enabled and custom_path and Path(custom_path).exists():
        if load_custom_cursor_image(custom_path, show_messages=False):
            apply_cursor_lab_from_ui(show_message=False)
    elif not custom_enabled:
        if CURSOR_SHAPE_MODE in CURSOR_SHAPE_CURSOR_IDS:
            commit_cursor_shape_mode(CURSOR_SHAPE_MODE)
        else:
            commit_reset_to_system_cursor_image()
    elif CUSTOM_CURSOR_ENABLED:
        set_custom_cursor_hotspot_from_mode()
        CURSOR_SHAPE_MODE = "Custom Image File"

    invalidate_cursor_image_cache()
    set_cursor_lab_vars_from_globals()



def get_performance_frame_delay_ms():
    try:
        fps = int(PERFORMANCE_TARGET_FPS)
    except Exception:
        fps = 60
    fps = int(clamp(fps, 15, 60))
    return max(8, int(round(1000 / fps)))


def update_performance_idle_timer(real_distance, now):
    global performance_last_real_motion_time, performance_long_idle_is_active

    # Use a stronger threshold than MOVE_DISTANCE_THRESHOLD so tiny device jitter
    # does not prevent Battery Saver / long-idle pause from activating.
    try:
        movement_distance = float(real_distance)
    except Exception:
        movement_distance = 0.0

    if movement_distance >= 2.5:
        performance_last_real_motion_time = now
        performance_long_idle_is_active = False
        return

    performance_long_idle_is_active = performance_long_idle_active(now)


def performance_long_idle_active(now=None):
    # Long-idle detection is shared by both power-saving options:
    # 1) Hide Fake Cursors After Long Idle
    # 2) Pause Idle Effects After Long Idle
    # v12.9.5 accidentally depended only on the fake-cursor option, so idle
    # effects would not pause unless fake hiding was also enabled.
    if not (PERFORMANCE_PAUSE_SWARM_ON_LONG_IDLE or PERFORMANCE_PAUSE_IDLE_EFFECTS_ON_LONG_IDLE):
        return False
    try:
        current_time = time.time() if now is None else float(now)
        threshold = max(5.0, float(PERFORMANCE_LONG_IDLE_SECONDS))
        return (current_time - performance_last_real_motion_time) >= threshold
    except Exception:
        return False


def performance_summary_text():
    long_idle_swarm = "ON" if PERFORMANCE_PAUSE_SWARM_ON_LONG_IDLE else "OFF"
    long_idle_idle_effects = "ON" if PERFORMANCE_PAUSE_IDLE_EFFECTS_ON_LONG_IDLE else "OFF"
    glow = "Simple / Battery Saver" if PERFORMANCE_REDUCE_GLOW_QUALITY else "Full detail"
    active = "ACTIVE" if performance_long_idle_is_active else "waiting"
    return (
        f"Mode: {PERFORMANCE_MODE} | Active overlay FPS: {int(PERFORMANCE_TARGET_FPS)}\n"
        f"Glow drawing detail: {glow}\n"
        f"Hide fake cursors after long idle: {long_idle_swarm} after {PERFORMANCE_LONG_IDLE_SECONDS:.0f}s ({active})\n"
        f"Pause idle effects after long idle: {long_idle_idle_effects} after {PERFORMANCE_LONG_IDLE_SECONDS:.0f}s ({active})\n"
        "Tip: FPS affects CursorSwarm overlay drawings/fake cursors. It is easiest to see when fake cursors, drawn cursor, glow, or other effects are active."
    )


def refresh_performance_summary(message=None):
    if "performance_summary_var" in globals():
        text_value = performance_summary_text()
        if message:
            text_value += "\nStatus: " + str(message)
        performance_summary_var.set(text_value)


def set_performance_vars_from_globals():
    if "performance_mode_var" not in globals():
        return
    performance_mode_var.set(str(PERFORMANCE_MODE))
    performance_fps_var.set(int(PERFORMANCE_TARGET_FPS))
    performance_fps_label_var.set(f"{int(PERFORMANCE_TARGET_FPS)} FPS")
    reduce_glow_quality_var.set(bool(PERFORMANCE_REDUCE_GLOW_QUALITY))
    pause_swarm_long_idle_var.set(bool(PERFORMANCE_PAUSE_SWARM_ON_LONG_IDLE))
    pause_idle_effects_long_idle_var.set(bool(PERFORMANCE_PAUSE_IDLE_EFFECTS_ON_LONG_IDLE))
    long_idle_seconds_var.set(float(PERFORMANCE_LONG_IDLE_SECONDS))
    long_idle_seconds_label_var.set(f"{PERFORMANCE_LONG_IDLE_SECONDS:.0f}s")
    refresh_performance_summary()


def mark_performance_pending(message=None):
    refresh_performance_summary(message or "Performance changes pending. Click Apply Performance Settings to activate them.")


def ui_set_performance_fps(value):
    performance_fps_label_var.set(f"{int(float(value))} FPS")
    performance_mode_var.set("Custom")
    mark_performance_pending("Target FPS changed in the panel only. Click Apply Performance Settings to activate it.")


def ui_set_long_idle_seconds(value):
    long_idle_seconds_label_var.set(f"{float(value):.0f}s")
    mark_performance_pending("Long idle time changed in the panel only. Click Apply Performance Settings to activate it.")


def load_performance_preset_values_from_ui():
    mode = performance_mode_var.get() or "Smooth (60 FPS)"
    if mode == "Smooth (60 FPS)":
        performance_fps_var.set(60)
        reduce_glow_quality_var.set(False)
        pause_swarm_long_idle_var.set(False)
        pause_idle_effects_long_idle_var.set(False)
        long_idle_seconds_var.set(60.0)
    elif mode == "Balanced (45 FPS)":
        performance_fps_var.set(45)
        reduce_glow_quality_var.set(False)
        pause_swarm_long_idle_var.set(False)
        pause_idle_effects_long_idle_var.set(False)
        long_idle_seconds_var.set(60.0)
    elif mode == "Battery Saver (30 FPS)":
        performance_fps_var.set(30)
        reduce_glow_quality_var.set(True)
        pause_swarm_long_idle_var.set(True)
        pause_idle_effects_long_idle_var.set(True)
        long_idle_seconds_var.set(45.0)

    performance_fps_label_var.set(f"{int(float(performance_fps_var.get()))} FPS")
    long_idle_seconds_label_var.set(f"{float(long_idle_seconds_var.get()):.0f}s")
    if mode != "Custom":
        performance_mode_var.set(mode)
    mark_performance_pending("Preset values loaded only in the panel. Click Apply Performance Settings to activate them.")


def apply_performance_preset_from_ui():
    load_performance_preset_values_from_ui()


def apply_performance_settings_from_ui(show_message=False):
    global PERFORMANCE_MODE, PERFORMANCE_TARGET_FPS, PERFORMANCE_REDUCE_GLOW_QUALITY
    global PERFORMANCE_PAUSE_SWARM_ON_LONG_IDLE, PERFORMANCE_PAUSE_IDLE_EFFECTS_ON_LONG_IDLE
    global PERFORMANCE_LONG_IDLE_SECONDS, performance_last_real_motion_time, performance_long_idle_is_active

    PERFORMANCE_MODE = performance_mode_var.get() or "Custom"
    if PERFORMANCE_MODE not in PERFORMANCE_MODE_OPTIONS:
        PERFORMANCE_MODE = "Custom"

    PERFORMANCE_TARGET_FPS = int(safe_float_from_var(performance_fps_var, PERFORMANCE_TARGET_FPS, minimum=15, maximum=60))
    PERFORMANCE_REDUCE_GLOW_QUALITY = bool(reduce_glow_quality_var.get())
    PERFORMANCE_PAUSE_SWARM_ON_LONG_IDLE = bool(pause_swarm_long_idle_var.get())
    PERFORMANCE_PAUSE_IDLE_EFFECTS_ON_LONG_IDLE = bool(pause_idle_effects_long_idle_var.get())
    PERFORMANCE_LONG_IDLE_SECONDS = round(safe_float_from_var(long_idle_seconds_var, PERFORMANCE_LONG_IDLE_SECONDS, minimum=10, maximum=300), 0)

    # Restart the long-idle timer after applying, so a new setting does not
    # instantly activate based on an old timer state.
    performance_last_real_motion_time = time.time()
    performance_long_idle_is_active = False

    set_performance_vars_from_globals()
    update_panel_status()

    if show_message:
        refresh_performance_summary("Performance settings applied.")


def get_colors_from_neon_preset(preset_name):
    colors = NEON_COLOR_PRESETS.get(str(preset_name or ""))
    if isinstance(colors, (list, tuple)) and colors:
        return [sanitize_neon_color(color) for color in colors[:3]]
    return [sanitize_neon_color(get_neon_preset_primary_color("Cyberpunk Neon"))]


def get_cursor_lab_movement_colors():
    if CURSOR_TINT_STYLE == "Multi-Colour Neon Preset":
        colors = get_cursor_tint_gradient_colors()
    elif CURSOR_TINT_ENABLED:
        colors = [sanitize_neon_color(CURSOR_TINT_COLOR)]
    else:
        colors = get_neon_gradient_colors()
    return colors[:3] if colors else ["#22d3ee"]


def get_movement_effect_color_settings(effect_name):
    effect_name = str(effect_name or "")
    if effect_name == "trail":
        return MOTION_TRAIL_COLOR_MODE, MOTION_TRAIL_CUSTOM_COLOR, MOTION_TRAIL_SINGLE_PRESET, MOTION_TRAIL_NEON_PRESET
    if effect_name == "streak":
        return MOTION_STREAK_COLOR_MODE, MOTION_STREAK_CUSTOM_COLOR, MOTION_STREAK_SINGLE_PRESET, MOTION_STREAK_NEON_PRESET
    if effect_name == "spark":
        return SPARK_PARTICLE_COLOR_MODE, SPARK_PARTICLE_CUSTOM_COLOR, SPARK_PARTICLE_SINGLE_PRESET, SPARK_PARTICLE_NEON_PRESET
    if effect_name == "ripple":
        return RIPPLE_BURST_COLOR_MODE, RIPPLE_BURST_CUSTOM_COLOR, RIPPLE_BURST_SINGLE_PRESET, RIPPLE_BURST_NEON_PRESET
    if effect_name == "comet":
        return COMET_TAIL_COLOR_MODE, COMET_TAIL_CUSTOM_COLOR, COMET_TAIL_SINGLE_PRESET, COMET_TAIL_NEON_PRESET
    if effect_name == "lines":
        return SPEED_LINES_COLOR_MODE, SPEED_LINES_CUSTOM_COLOR, SPEED_LINES_SINGLE_PRESET, SPEED_LINES_NEON_PRESET
    if effect_name == "orbit":
        return MAGNETIC_ORBIT_COLOR_MODE, MAGNETIC_ORBIT_CUSTOM_COLOR, MAGNETIC_ORBIT_SINGLE_PRESET, MAGNETIC_ORBIT_NEON_PRESET
    if effect_name == "click":
        return CLICK_EFFECT_COLOR_MODE, CLICK_EFFECT_CUSTOM_COLOR, CLICK_EFFECT_SINGLE_PRESET, CLICK_EFFECT_NEON_PRESET
    return SPEED_GLOW_COLOR_MODE, SPEED_GLOW_CUSTOM_COLOR, SPEED_GLOW_SINGLE_PRESET, SPEED_GLOW_NEON_PRESET


def get_single_colour_preset_color(preset_name):
    return sanitize_neon_color(MOVEMENT_SINGLE_COLOR_PRESETS.get(str(preset_name or ""), MOVEMENT_SINGLE_COLOR_PRESETS[MOVEMENT_DEFAULT_SINGLE_PRESET]))


def get_movement_effect_colors(effect_name):
    mode, custom_color, single_preset, neon_preset = get_movement_effect_color_settings(effect_name)
    mode = str(mode or MOVEMENT_DEFAULT_COLOR_MODE)
    if mode == "Custom Color":
        return [sanitize_neon_color(custom_color or MOVEMENT_DEFAULT_CUSTOM_COLOR)]
    if mode == "Single Colour Preset":
        return [get_single_colour_preset_color(single_preset)]
    if mode in ("Neon Preset", "Multi-Colour Neon Preset"):
        return get_colors_from_neon_preset(neon_preset or MOVEMENT_DEFAULT_NEON_PRESET)
    return get_cursor_lab_movement_colors()


def movement_effect_cache_key(effect_name):
    """Return a compact cache key for effect-coloured cursor images.

    v13.9's trail colour bug was caused by image caching: once the purple
    motion-trail cursor was cached, changing the trail colour still reused the
    old cached PhotoImage. This key forces a new cached image whenever the
    movement effect colour settings change.
    """
    try:
        mode, custom_color, single_preset, neon_preset = get_movement_effect_color_settings(effect_name)
        colors = tuple(get_movement_effect_colors(effect_name))
        return (
            str(effect_name),
            str(mode),
            str(custom_color),
            str(single_preset),
            str(neon_preset),
            colors,
            bool(CURSOR_TINT_BLACK_OUTLINE),
            int(CURSOR_TINT_OUTLINE_THICKNESS),
        )
    except Exception:
        return (str(effect_name), "fallback")


def apply_movement_effect_tint_to_image_with_colors(img, colors):
    """Fill a cursor silhouette with explicit movement colours.

    v13.9 uses this direct colour path for Motion Trail so every ghost cursor
    is generated from the selected movement colour/preset instead of any cached
    Cursor Lab purple image.
    """
    if not colors:
        return img.convert("RGBA")

    source = img.convert("RGBA")
    width, height = source.size
    output = Image.new("RGBA", source.size, (0, 0, 0, 0))
    source_pixels = source.load()
    output_pixels = output.load()

    clean_colors = [sanitize_neon_color(color) for color in colors[:3]]
    if not clean_colors:
        clean_colors = [MOVEMENT_DEFAULT_CUSTOM_COLOR]

    for y in range(height):
        for x in range(width):
            _pr, _pg, _pb, pa = source_pixels[x, y]
            if pa == 0:
                continue

            if len(clean_colors) == 1:
                target_r, target_g, target_b = color_to_rgb(clean_colors[0])
            elif len(clean_colors) == 2:
                target_r, target_g, target_b = interpolate_rgb(clean_colors[0], clean_colors[1], y / max(1, height - 1))
            else:
                t = y / max(1, height - 1)
                if t <= 0.5:
                    target_r, target_g, target_b = interpolate_rgb(clean_colors[0], clean_colors[1], t / 0.5)
                else:
                    target_r, target_g, target_b = interpolate_rgb(clean_colors[1], clean_colors[2], (t - 0.5) / 0.5)

            if (target_r, target_g, target_b) == (255, 0, 255):
                target_r, target_g, target_b = 255, 1, 254
            output_pixels[x, y] = (int(target_r), int(target_g), int(target_b), pa)

    if CURSOR_TINT_BLACK_OUTLINE and CURSOR_TINT_APPLY_DRAWN:
        output = apply_black_outline_to_image(output, max(1, min(4, CURSOR_TINT_OUTLINE_THICKNESS)))
    return output


def apply_movement_effect_tint_to_image(img, effect_name="trail"):
    """Apply a movement-effect-specific colour to a cursor ghost image."""
    return apply_movement_effect_tint_to_image_with_colors(img, get_movement_effect_colors(effect_name))


def ensure_motion_trail_image_for_scale(scale, alpha_factor=1.0):
    """Dedicated Motion Trail image path.

    v13.9 avoids the generic drawn/fake cursor cache for trails. Every ghost
    frame uses this role-specific cache key and a forced movement-colour fill,
    so all trail ghosts use the selected trail colour instead of only the newest
    one changing while older ones remain purple.
    """
    scale = cursor_scale_key(scale)
    alpha_factor = cursor_alpha_key(clamp(alpha_factor, 0.03, 1.0))
    source_image, _hx, _hy, render_key = get_current_cursor_source_image_and_hotspot()
    colors = tuple(get_movement_effect_colors("trail"))
    mode, custom_color, single_preset, neon_preset = get_movement_effect_color_settings("trail")
    cache_key = (
        "motion_trail_direct",
        scale,
        alpha_factor,
        render_key,
        str(mode),
        str(custom_color),
        str(single_preset),
        str(neon_preset),
        colors,
        bool(CURSOR_TINT_BLACK_OUTLINE),
        int(CURSOR_TINT_OUTLINE_THICKNESS),
    )

    if cache_key not in tk_cursor_images:
        new_w = max(1, round(source_image.width * scale))
        new_h = max(1, round(source_image.height * scale))
        resized = source_image.resize((new_w, new_h), Image.Resampling.NEAREST)

        if not CUSTOM_CURSOR_ENABLED:
            resized = remove_alpha_glow(resized, threshold=120)

        recolored = apply_movement_effect_tint_to_image_with_colors(resized, colors)

        if alpha_factor < 0.99:
            recolored = recolored.convert("RGBA")
            alpha = recolored.getchannel("A").point(lambda value: int(value * alpha_factor))
            recolored.putalpha(alpha)

        tk_cursor_images[cache_key] = ImageTk.PhotoImage(recolored)

    return tk_cursor_images[cache_key]


def draw_motion_trail_image_direct(x, y, scale, alpha_factor=1.0):
    """Draw a Motion Trail ghost with no reusable cursor cache.

    v13.9 final trail-colour attempt: older ghosts were still visually using
    the previous purple cache on some runs. This path builds each trail ghost
    directly from the current source cursor and selected movement colours, then
    stores the PhotoImage only for the current frame. It is a little heavier,
    but Motion Trail length is limited and it guarantees every ghost uses the
    same selected trail colour.
    """
    global motion_trail_runtime_images

    try:
        source_image, _hx, _hy, _render_key = get_current_cursor_source_image_and_hotspot()
        scale = cursor_scale_key(scale)
        alpha_factor = cursor_alpha_key(clamp(alpha_factor, 0.03, 1.0))
        new_w = max(1, round(source_image.width * scale))
        new_h = max(1, round(source_image.height * scale))
        resized = source_image.resize((new_w, new_h), Image.Resampling.NEAREST)

        if not CUSTOM_CURSOR_ENABLED:
            resized = remove_alpha_glow(resized, threshold=120)

        colors = get_movement_effect_colors("trail")
        recolored = apply_movement_effect_tint_to_image_with_colors(resized, colors)

        if alpha_factor < 0.99:
            recolored = recolored.convert("RGBA")
            alpha = recolored.getchannel("A").point(lambda value: int(value * alpha_factor))
            recolored.putalpha(alpha)

        photo = ImageTk.PhotoImage(recolored)
        motion_trail_runtime_images.append(photo)
        pad = cursor_outline_padding_for_role("drawn") if (CURSOR_TINT_BLACK_OUTLINE and CURSOR_TINT_APPLY_DRAWN) else 0
        canvas.create_image(round(x - pad), round(y - pad), image=photo, anchor="nw")
        return True
    except Exception:
        return False


def draw_motion_trail_colour_glow(x, y, scale, alpha_factor):
    """v13.9: halo disabled for Motion Trail.

    The previous halo made trail colour changes visible, but it looked too much
    like Speed Glow. Motion Trail now recolours the ghost cursor itself instead.
    """
    return

def movement_effects_active():
    return bool(
        MOVEMENT_EFFECTS_ENABLED
        and (MOVEMENT_MOTION_TRAIL_ENABLED or MOVEMENT_SPEED_GLOW_ENABLED or MOVEMENT_MOTION_STREAK_ENABLED or MOVEMENT_SPARK_PARTICLES_ENABLED or MOVEMENT_RIPPLE_BURST_ENABLED or MOVEMENT_COMET_TAIL_ENABLED or MOVEMENT_SPEED_LINES_ENABLED or MOVEMENT_MAGNETIC_ORBIT_ENABLED or CLICK_EFFECTS_ENABLED)
    )


def motion_trail_active():
    return bool(MOVEMENT_EFFECTS_ENABLED and MOVEMENT_MOTION_TRAIL_ENABLED)


def speed_glow_active():
    return bool(MOVEMENT_EFFECTS_ENABLED and MOVEMENT_SPEED_GLOW_ENABLED)


def motion_streak_active():
    return bool(MOVEMENT_EFFECTS_ENABLED and MOVEMENT_MOTION_STREAK_ENABLED)


def spark_particles_active():
    return bool(MOVEMENT_EFFECTS_ENABLED and MOVEMENT_SPARK_PARTICLES_ENABLED)


def ripple_burst_active():
    return bool(MOVEMENT_EFFECTS_ENABLED and MOVEMENT_RIPPLE_BURST_ENABLED)


def comet_tail_active():
    return bool(MOVEMENT_EFFECTS_ENABLED and MOVEMENT_COMET_TAIL_ENABLED)


def speed_lines_active():
    return bool(MOVEMENT_EFFECTS_ENABLED and MOVEMENT_SPEED_LINES_ENABLED)


def magnetic_orbit_active():
    return bool(MOVEMENT_EFFECTS_ENABLED and MOVEMENT_MAGNETIC_ORBIT_ENABLED)


def click_effects_active():
    return bool(MOVEMENT_EFFECTS_ENABLED and CLICK_EFFECTS_ENABLED)


def clear_spark_particles():
    global spark_particles
    spark_particles = []


def clear_ripple_bursts():
    global ripple_bursts, last_ripple_burst_time
    ripple_bursts = []
    last_ripple_burst_time = 0.0


def clear_motion_trail():
    global motion_trail_points, last_motion_trail_x, last_motion_trail_y
    motion_trail_points = []
    last_motion_trail_x = None
    last_motion_trail_y = None


def movement_summary_text():
    enabled = "ON" if MOVEMENT_EFFECTS_ENABLED and MOVEMENT_EFFECT_STYLE != "Disabled" else "OFF"
    return (
        f"Movement Effects: {enabled} | Style: {MOVEMENT_EFFECT_STYLE}\n"
        f"Motion Trail length: {int(MOTION_TRAIL_LENGTH)} ghosts | Fade strength: {MOTION_TRAIL_FADE_STRENGTH:.2f}\n"
        f"Speed Glow strength: {SPEED_GLOW_STRENGTH:.2f} | Trigger speed: {int(SPEED_GLOW_THRESHOLD)} px/s\n"
        f"Click Effects: {'ON' if CLICK_EFFECTS_ENABLED else 'OFF'} | Style: {CLICK_EFFECT_STYLE}\n"
        "Motion Trail uses the current drawn cursor image. Speed Glow reacts to speed. Click Effects react to mouse clicks."
    )


def refresh_movement_summary(message=None):
    if "movement_summary_var" in globals():
        text_value = movement_summary_text()
        if message:
            text_value += "\nStatus: " + str(message)
        movement_summary_var.set(text_value)


def set_movement_vars_from_globals():
    if "movement_effects_enabled_var" not in globals():
        return
    movement_effects_enabled_var.set(bool(MOVEMENT_EFFECTS_ENABLED))
    movement_motion_trail_enabled_var.set(bool(MOVEMENT_MOTION_TRAIL_ENABLED))
    movement_speed_glow_enabled_var.set(bool(MOVEMENT_SPEED_GLOW_ENABLED))
    movement_motion_streak_enabled_var.set(bool(MOVEMENT_MOTION_STREAK_ENABLED))
    movement_spark_particles_enabled_var.set(bool(MOVEMENT_SPARK_PARTICLES_ENABLED))
    movement_ripple_burst_enabled_var.set(bool(MOVEMENT_RIPPLE_BURST_ENABLED))
    movement_comet_tail_enabled_var.set(bool(MOVEMENT_COMET_TAIL_ENABLED))
    movement_speed_lines_enabled_var.set(bool(MOVEMENT_SPEED_LINES_ENABLED))
    movement_magnetic_orbit_enabled_var.set(bool(MOVEMENT_MAGNETIC_ORBIT_ENABLED))
    click_effects_enabled_var.set(bool(CLICK_EFFECTS_ENABLED))
    click_effect_left_enabled_var.set(bool(CLICK_EFFECT_LEFT_ENABLED))
    click_effect_right_enabled_var.set(bool(CLICK_EFFECT_RIGHT_ENABLED))
    click_effect_style_var.set(str(CLICK_EFFECT_STYLE))
    click_effect_color_mode_var.set(str(CLICK_EFFECT_COLOR_MODE))
    click_effect_custom_color_var.set(str(CLICK_EFFECT_CUSTOM_COLOR))
    click_effect_single_preset_var.set(str(CLICK_EFFECT_SINGLE_PRESET))
    click_effect_neon_preset_var.set(str(CLICK_EFFECT_NEON_PRESET))
    if "movement_effect_style_var" in globals():
        movement_effect_style_var.set(str(MOVEMENT_EFFECT_STYLE))
    motion_trail_color_mode_var.set(str(MOTION_TRAIL_COLOR_MODE))
    motion_trail_custom_color_var.set(str(MOTION_TRAIL_CUSTOM_COLOR))
    motion_trail_single_preset_var.set(str(MOTION_TRAIL_SINGLE_PRESET))
    motion_trail_neon_preset_var.set(str(MOTION_TRAIL_NEON_PRESET))
    speed_glow_color_mode_var.set(str(SPEED_GLOW_COLOR_MODE))
    speed_glow_custom_color_var.set(str(SPEED_GLOW_CUSTOM_COLOR))
    speed_glow_single_preset_var.set(str(SPEED_GLOW_SINGLE_PRESET))
    speed_glow_neon_preset_var.set(str(SPEED_GLOW_NEON_PRESET))
    motion_streak_color_mode_var.set(str(MOTION_STREAK_COLOR_MODE))
    motion_streak_custom_color_var.set(str(MOTION_STREAK_CUSTOM_COLOR))
    motion_streak_single_preset_var.set(str(MOTION_STREAK_SINGLE_PRESET))
    motion_streak_neon_preset_var.set(str(MOTION_STREAK_NEON_PRESET))
    spark_particle_color_mode_var.set(str(SPARK_PARTICLE_COLOR_MODE))
    spark_particle_custom_color_var.set(str(SPARK_PARTICLE_CUSTOM_COLOR))
    spark_particle_single_preset_var.set(str(SPARK_PARTICLE_SINGLE_PRESET))
    spark_particle_neon_preset_var.set(str(SPARK_PARTICLE_NEON_PRESET))
    ripple_burst_color_mode_var.set(str(RIPPLE_BURST_COLOR_MODE))
    ripple_burst_custom_color_var.set(str(RIPPLE_BURST_CUSTOM_COLOR))
    ripple_burst_single_preset_var.set(str(RIPPLE_BURST_SINGLE_PRESET))
    ripple_burst_neon_preset_var.set(str(RIPPLE_BURST_NEON_PRESET))
    comet_tail_color_mode_var.set(str(COMET_TAIL_COLOR_MODE))
    comet_tail_custom_color_var.set(str(COMET_TAIL_CUSTOM_COLOR))
    comet_tail_single_preset_var.set(str(COMET_TAIL_SINGLE_PRESET))
    comet_tail_neon_preset_var.set(str(COMET_TAIL_NEON_PRESET))
    speed_lines_color_mode_var.set(str(SPEED_LINES_COLOR_MODE))
    speed_lines_custom_color_var.set(str(SPEED_LINES_CUSTOM_COLOR))
    speed_lines_single_preset_var.set(str(SPEED_LINES_SINGLE_PRESET))
    speed_lines_neon_preset_var.set(str(SPEED_LINES_NEON_PRESET))
    magnetic_orbit_color_mode_var.set(str(MAGNETIC_ORBIT_COLOR_MODE))
    magnetic_orbit_custom_color_var.set(str(MAGNETIC_ORBIT_CUSTOM_COLOR))
    magnetic_orbit_single_preset_var.set(str(MAGNETIC_ORBIT_SINGLE_PRESET))
    magnetic_orbit_neon_preset_var.set(str(MAGNETIC_ORBIT_NEON_PRESET))
    motion_trail_length_var.set(int(MOTION_TRAIL_LENGTH))
    motion_trail_length_label_var.set(f"{int(MOTION_TRAIL_LENGTH)}")
    motion_trail_fade_var.set(float(MOTION_TRAIL_FADE_STRENGTH))
    motion_trail_fade_label_var.set(f"{MOTION_TRAIL_FADE_STRENGTH:.2f}")
    speed_glow_strength_var.set(float(SPEED_GLOW_STRENGTH))
    speed_glow_strength_label_var.set(f"{SPEED_GLOW_STRENGTH:.2f}")
    speed_glow_threshold_var.set(float(SPEED_GLOW_THRESHOLD))
    speed_glow_threshold_label_var.set(f"{int(SPEED_GLOW_THRESHOLD)} px/s")
    motion_streak_strength_var.set(float(MOTION_STREAK_STRENGTH))
    motion_streak_strength_label_var.set(f"{MOTION_STREAK_STRENGTH:.2f}")
    motion_streak_threshold_var.set(float(MOTION_STREAK_THRESHOLD))
    motion_streak_threshold_label_var.set(f"{int(MOTION_STREAK_THRESHOLD)} px/s")
    motion_streak_length_var.set(int(MOTION_STREAK_LENGTH))
    motion_streak_length_label_var.set(f"{int(MOTION_STREAK_LENGTH)} px")
    spark_particle_strength_var.set(float(SPARK_PARTICLE_STRENGTH))
    spark_particle_strength_label_var.set(f"{SPARK_PARTICLE_STRENGTH:.2f}")
    spark_particle_threshold_var.set(float(SPARK_PARTICLE_THRESHOLD))
    spark_particle_threshold_label_var.set(f"{int(SPARK_PARTICLE_THRESHOLD)} px/s")
    spark_particle_amount_var.set(int(SPARK_PARTICLE_AMOUNT))
    spark_particle_amount_label_var.set(f"{int(SPARK_PARTICLE_AMOUNT)}")
    spark_particle_size_var.set(int(SPARK_PARTICLE_SIZE))
    spark_particle_size_label_var.set(f"{int(SPARK_PARTICLE_SIZE)} px")
    spark_particle_lifetime_var.set(float(SPARK_PARTICLE_LIFETIME))
    spark_particle_lifetime_label_var.set(f"{SPARK_PARTICLE_LIFETIME:.2f}s")
    ripple_burst_strength_var.set(float(RIPPLE_BURST_STRENGTH))
    ripple_burst_strength_label_var.set(f"{RIPPLE_BURST_STRENGTH:.2f}")
    ripple_burst_threshold_var.set(float(RIPPLE_BURST_THRESHOLD))
    ripple_burst_threshold_label_var.set(f"{int(RIPPLE_BURST_THRESHOLD)} px/s")
    ripple_burst_lifetime_var.set(float(RIPPLE_BURST_LIFETIME))
    ripple_burst_lifetime_label_var.set(f"{RIPPLE_BURST_LIFETIME:.2f}s")
    ripple_burst_radius_var.set(int(RIPPLE_BURST_RADIUS))
    ripple_burst_radius_label_var.set(f"{int(RIPPLE_BURST_RADIUS)} px")
    comet_tail_strength_var.set(float(COMET_TAIL_STRENGTH))
    comet_tail_strength_label_var.set(f"{COMET_TAIL_STRENGTH:.2f}")
    comet_tail_length_var.set(int(COMET_TAIL_LENGTH))
    comet_tail_length_label_var.set(f"{int(COMET_TAIL_LENGTH)} px")
    comet_tail_thickness_var.set(int(COMET_TAIL_THICKNESS))
    comet_tail_thickness_label_var.set(f"{int(COMET_TAIL_THICKNESS)} px")
    speed_lines_strength_var.set(float(SPEED_LINES_STRENGTH))
    speed_lines_strength_label_var.set(f"{SPEED_LINES_STRENGTH:.2f}")
    speed_lines_threshold_var.set(float(SPEED_LINES_THRESHOLD))
    speed_lines_threshold_label_var.set(f"{int(SPEED_LINES_THRESHOLD)} px/s")
    speed_lines_amount_var.set(int(SPEED_LINES_AMOUNT))
    speed_lines_amount_label_var.set(f"{int(SPEED_LINES_AMOUNT)}")
    speed_lines_length_var.set(int(SPEED_LINES_LENGTH))
    speed_lines_length_label_var.set(f"{int(SPEED_LINES_LENGTH)} px")
    magnetic_orbit_strength_var.set(float(MAGNETIC_ORBIT_STRENGTH))
    magnetic_orbit_strength_label_var.set(f"{MAGNETIC_ORBIT_STRENGTH:.2f}")
    magnetic_orbit_threshold_var.set(float(MAGNETIC_ORBIT_THRESHOLD))
    magnetic_orbit_threshold_label_var.set(f"{int(MAGNETIC_ORBIT_THRESHOLD)} px/s")
    magnetic_orbit_radius_var.set(int(MAGNETIC_ORBIT_RADIUS))
    magnetic_orbit_radius_label_var.set(f"{int(MAGNETIC_ORBIT_RADIUS)} px")
    magnetic_orbit_dots_var.set(int(MAGNETIC_ORBIT_DOTS))
    magnetic_orbit_dots_label_var.set(f"{int(MAGNETIC_ORBIT_DOTS)}")
    click_effect_strength_var.set(float(CLICK_EFFECT_STRENGTH))
    click_effect_strength_label_var.set(f"{CLICK_EFFECT_STRENGTH:.2f}")
    click_effect_radius_var.set(int(CLICK_EFFECT_RADIUS))
    click_effect_radius_label_var.set(f"{int(CLICK_EFFECT_RADIUS)} px")
    click_effect_lifetime_var.set(float(CLICK_EFFECT_LIFETIME))
    click_effect_lifetime_label_var.set(f"{CLICK_EFFECT_LIFETIME:.2f}s")
    click_effect_spark_amount_var.set(int(CLICK_EFFECT_SPARK_AMOUNT))
    click_effect_spark_amount_label_var.set(f"{int(CLICK_EFFECT_SPARK_AMOUNT)}")
    refresh_movement_summary()


def mark_movement_pending(message=None):
    refresh_movement_summary(message or "Movement effect changes pending. Click Apply Movement Settings to activate them.")


def on_movement_effect_style_change(_value=None):
    mark_movement_pending("Movement style changed in the panel only. Click Apply Movement Settings to activate it.")


def on_movement_effect_checkbox_change():
    mark_movement_pending("Movement effect selection changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_motion_trail_length(value):
    try:
        motion_trail_length_label_var.set(f"{int(round(float(value)))}")
    except Exception:
        motion_trail_length_label_var.set(str(MOTION_TRAIL_LENGTH))
    mark_movement_pending("Motion trail length changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_motion_trail_fade(value):
    try:
        motion_trail_fade_label_var.set(f"{float(value):.2f}")
    except Exception:
        motion_trail_fade_label_var.set(f"{MOTION_TRAIL_FADE_STRENGTH:.2f}")
    mark_movement_pending("Motion trail fade changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_speed_glow_strength(value):
    try:
        speed_glow_strength_label_var.set(f"{float(value):.2f}")
    except Exception:
        speed_glow_strength_label_var.set(f"{SPEED_GLOW_STRENGTH:.2f}")
    mark_movement_pending("Speed Glow strength changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_speed_glow_threshold(value):
    try:
        speed_glow_threshold_label_var.set(f"{int(round(float(value)))} px/s")
    except Exception:
        speed_glow_threshold_label_var.set(f"{int(SPEED_GLOW_THRESHOLD)} px/s")
    mark_movement_pending("Speed Glow trigger speed changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_motion_streak_strength(value):
    try:
        motion_streak_strength_label_var.set(f"{float(value):.2f}")
    except Exception:
        motion_streak_strength_label_var.set(f"{MOTION_STREAK_STRENGTH:.2f}")
    mark_movement_pending("Motion Streak strength changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_motion_streak_threshold(value):
    try:
        motion_streak_threshold_label_var.set(f"{int(round(float(value)))} px/s")
    except Exception:
        motion_streak_threshold_label_var.set(f"{int(MOTION_STREAK_THRESHOLD)} px/s")
    mark_movement_pending("Motion Streak trigger speed changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_motion_streak_length(value):
    try:
        motion_streak_length_label_var.set(f"{int(round(float(value)))} px")
    except Exception:
        motion_streak_length_label_var.set(f"{int(MOTION_STREAK_LENGTH)} px")
    mark_movement_pending("Motion Streak length changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_spark_particle_strength(value):
    try:
        spark_particle_strength_label_var.set(f"{float(value):.2f}")
    except Exception:
        spark_particle_strength_label_var.set(f"{SPARK_PARTICLE_STRENGTH:.2f}")
    mark_movement_pending("Spark strength changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_spark_particle_threshold(value):
    try:
        spark_particle_threshold_label_var.set(f"{int(round(float(value)))} px/s")
    except Exception:
        spark_particle_threshold_label_var.set(f"{int(SPARK_PARTICLE_THRESHOLD)} px/s")
    mark_movement_pending("Spark trigger speed changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_spark_particle_amount(value):
    try:
        spark_particle_amount_label_var.set(f"{int(round(float(value)))}")
    except Exception:
        spark_particle_amount_label_var.set(f"{int(SPARK_PARTICLE_AMOUNT)}")
    mark_movement_pending("Spark amount changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_spark_particle_size(value):
    try:
        spark_particle_size_label_var.set(f"{int(round(float(value)))} px")
    except Exception:
        spark_particle_size_label_var.set(f"{int(SPARK_PARTICLE_SIZE)} px")
    mark_movement_pending("Spark size changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_spark_particle_lifetime(value):
    try:
        spark_particle_lifetime_label_var.set(f"{float(value):.2f}s")
    except Exception:
        spark_particle_lifetime_label_var.set(f"{SPARK_PARTICLE_LIFETIME:.2f}s")
    mark_movement_pending("Spark lifetime changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_ripple_burst_strength(value):
    try:
        ripple_burst_strength_label_var.set(f"{float(value):.2f}")
    except Exception:
        ripple_burst_strength_label_var.set(f"{RIPPLE_BURST_STRENGTH:.2f}")
    mark_movement_pending("Ripple strength changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_ripple_burst_threshold(value):
    try:
        ripple_burst_threshold_label_var.set(f"{int(round(float(value)))} px/s")
    except Exception:
        ripple_burst_threshold_label_var.set(f"{int(RIPPLE_BURST_THRESHOLD)} px/s")
    mark_movement_pending("Ripple trigger speed changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_ripple_burst_lifetime(value):
    try:
        ripple_burst_lifetime_label_var.set(f"{float(value):.2f}s")
    except Exception:
        ripple_burst_lifetime_label_var.set(f"{RIPPLE_BURST_LIFETIME:.2f}s")
    mark_movement_pending("Ripple lifetime changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_ripple_burst_radius(value):
    try:
        ripple_burst_radius_label_var.set(f"{int(round(float(value)))} px")
    except Exception:
        ripple_burst_radius_label_var.set(f"{int(RIPPLE_BURST_RADIUS)} px")
    mark_movement_pending("Ripple radius changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_comet_tail_strength(value):
    try:
        comet_tail_strength_label_var.set(f"{float(value):.2f}")
    except Exception:
        comet_tail_strength_label_var.set(f"{COMET_TAIL_STRENGTH:.2f}")
    mark_movement_pending("Comet Tail strength changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_comet_tail_length(value):
    try:
        comet_tail_length_label_var.set(f"{int(round(float(value)))} px")
    except Exception:
        comet_tail_length_label_var.set(f"{int(COMET_TAIL_LENGTH)} px")
    mark_movement_pending("Comet Tail length changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_comet_tail_thickness(value):
    try:
        comet_tail_thickness_label_var.set(f"{int(round(float(value)))} px")
    except Exception:
        comet_tail_thickness_label_var.set(f"{int(COMET_TAIL_THICKNESS)} px")
    mark_movement_pending("Comet Tail thickness changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_speed_lines_strength(value):
    try:
        speed_lines_strength_label_var.set(f"{float(value):.2f}")
    except Exception:
        speed_lines_strength_label_var.set(f"{SPEED_LINES_STRENGTH:.2f}")
    mark_movement_pending("Speed Lines strength changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_speed_lines_threshold(value):
    try:
        speed_lines_threshold_label_var.set(f"{int(round(float(value)))} px/s")
    except Exception:
        speed_lines_threshold_label_var.set(f"{int(SPEED_LINES_THRESHOLD)} px/s")
    mark_movement_pending("Speed Lines trigger speed changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_speed_lines_amount(value):
    try:
        speed_lines_amount_label_var.set(f"{int(round(float(value)))}")
    except Exception:
        speed_lines_amount_label_var.set(f"{int(SPEED_LINES_AMOUNT)}")
    mark_movement_pending("Speed Lines amount changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_speed_lines_length(value):
    try:
        speed_lines_length_label_var.set(f"{int(round(float(value)))} px")
    except Exception:
        speed_lines_length_label_var.set(f"{int(SPEED_LINES_LENGTH)} px")
    mark_movement_pending("Speed Lines length changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_magnetic_orbit_strength(value):
    try:
        magnetic_orbit_strength_label_var.set(f"{float(value):.2f}")
    except Exception:
        magnetic_orbit_strength_label_var.set(f"{MAGNETIC_ORBIT_STRENGTH:.2f}")
    mark_movement_pending("Magnetic Orbit strength changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_magnetic_orbit_threshold(value):
    try:
        magnetic_orbit_threshold_label_var.set(f"{int(round(float(value)))} px/s")
    except Exception:
        magnetic_orbit_threshold_label_var.set(f"{int(MAGNETIC_ORBIT_THRESHOLD)} px/s")
    mark_movement_pending("Magnetic Orbit trigger speed changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_magnetic_orbit_radius(value):
    try:
        magnetic_orbit_radius_label_var.set(f"{int(round(float(value)))} px")
    except Exception:
        magnetic_orbit_radius_label_var.set(f"{int(MAGNETIC_ORBIT_RADIUS)} px")
    mark_movement_pending("Magnetic Orbit radius changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_magnetic_orbit_dots(value):
    try:
        magnetic_orbit_dots_label_var.set(f"{int(round(float(value)))}")
    except Exception:
        magnetic_orbit_dots_label_var.set(f"{int(MAGNETIC_ORBIT_DOTS)}")
    mark_movement_pending("Magnetic Orbit dot count changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_click_effect_strength(value):
    try:
        click_effect_strength_label_var.set(f"{float(value):.2f}")
    except Exception:
        click_effect_strength_label_var.set(f"{CLICK_EFFECT_STRENGTH:.2f}")
    mark_movement_pending("Click effect strength changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_click_effect_radius(value):
    try:
        click_effect_radius_label_var.set(f"{int(round(float(value)))} px")
    except Exception:
        click_effect_radius_label_var.set(f"{int(CLICK_EFFECT_RADIUS)} px")
    mark_movement_pending("Click effect radius changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_click_effect_lifetime(value):
    try:
        click_effect_lifetime_label_var.set(f"{float(value):.2f}s")
    except Exception:
        click_effect_lifetime_label_var.set(f"{CLICK_EFFECT_LIFETIME:.2f}s")
    mark_movement_pending("Click effect lifetime changed in the panel only. Click Apply Movement Settings to activate it.")


def ui_set_click_effect_spark_amount(value):
    try:
        click_effect_spark_amount_label_var.set(f"{int(round(float(value)))}")
    except Exception:
        click_effect_spark_amount_label_var.set(f"{int(CLICK_EFFECT_SPARK_AMOUNT)}")
    mark_movement_pending("Click spark amount changed in the panel only. Click Apply Movement Settings to activate it.")


def mark_movement_color_pending(_value=None):
    mark_movement_pending("Movement effect colour changed in the panel only. Click Apply Movement Settings to activate it.")


def choose_movement_custom_color(target):
    target = str(target or "trail")
    var_map = {
        "trail": motion_trail_custom_color_var,
        "speed": speed_glow_custom_color_var,
        "streak": motion_streak_custom_color_var,
        "spark": spark_particle_custom_color_var,
        "ripple": ripple_burst_custom_color_var,
        "comet": comet_tail_custom_color_var,
        "lines": speed_lines_custom_color_var,
        "orbit": magnetic_orbit_custom_color_var,
    }
    var = var_map.get(target, motion_trail_custom_color_var)
    chosen = safe_colorchooser_askcolor(
        parent=control_panel if "control_panel" in globals() else root,
        color=var.get(),
        title="Choose movement effect colour",
    )
    if chosen and chosen[1]:
        fixed_hex, _rgb = parse_hex_color(chosen[1])
        var.set(sanitize_neon_color(fixed_hex))
        mark_movement_color_pending()


def apply_movement_color_to_all(source):
    source = str(source or "trail")
    if source == "speed":
        mode = speed_glow_color_mode_var.get()
        custom = speed_glow_custom_color_var.get()
        single = speed_glow_single_preset_var.get()
        preset = speed_glow_neon_preset_var.get()
    elif source == "streak":
        mode = motion_streak_color_mode_var.get()
        custom = motion_streak_custom_color_var.get()
        single = motion_streak_single_preset_var.get()
        preset = motion_streak_neon_preset_var.get()
    elif source == "spark":
        mode = spark_particle_color_mode_var.get()
        custom = spark_particle_custom_color_var.get()
        single = spark_particle_single_preset_var.get()
        preset = spark_particle_neon_preset_var.get()
    elif source == "ripple":
        mode = ripple_burst_color_mode_var.get()
        custom = ripple_burst_custom_color_var.get()
        single = ripple_burst_single_preset_var.get()
        preset = ripple_burst_neon_preset_var.get()
    elif source == "comet":
        mode = comet_tail_color_mode_var.get()
        custom = comet_tail_custom_color_var.get()
        single = comet_tail_single_preset_var.get()
        preset = comet_tail_neon_preset_var.get()
    elif source == "lines":
        mode = speed_lines_color_mode_var.get()
        custom = speed_lines_custom_color_var.get()
        single = speed_lines_single_preset_var.get()
        preset = speed_lines_neon_preset_var.get()
    elif source == "orbit":
        mode = magnetic_orbit_color_mode_var.get()
        custom = magnetic_orbit_custom_color_var.get()
        single = magnetic_orbit_single_preset_var.get()
        preset = magnetic_orbit_neon_preset_var.get()
    elif source == "click":
        mode = click_effect_color_mode_var.get()
        custom = click_effect_custom_color_var.get()
        single = click_effect_single_preset_var.get()
        preset = click_effect_neon_preset_var.get()
    else:
        mode = motion_trail_color_mode_var.get()
        custom = motion_trail_custom_color_var.get()
        single = motion_trail_single_preset_var.get()
        preset = motion_trail_neon_preset_var.get()

    for mode_var, custom_var, single_var, preset_var in (
        (motion_trail_color_mode_var, motion_trail_custom_color_var, motion_trail_single_preset_var, motion_trail_neon_preset_var),
        (speed_glow_color_mode_var, speed_glow_custom_color_var, speed_glow_single_preset_var, speed_glow_neon_preset_var),
        (motion_streak_color_mode_var, motion_streak_custom_color_var, motion_streak_single_preset_var, motion_streak_neon_preset_var),
        (spark_particle_color_mode_var, spark_particle_custom_color_var, spark_particle_single_preset_var, spark_particle_neon_preset_var),
        (ripple_burst_color_mode_var, ripple_burst_custom_color_var, ripple_burst_single_preset_var, ripple_burst_neon_preset_var),
        (comet_tail_color_mode_var, comet_tail_custom_color_var, comet_tail_single_preset_var, comet_tail_neon_preset_var),
        (speed_lines_color_mode_var, speed_lines_custom_color_var, speed_lines_single_preset_var, speed_lines_neon_preset_var),
        (magnetic_orbit_color_mode_var, magnetic_orbit_custom_color_var, magnetic_orbit_single_preset_var, magnetic_orbit_neon_preset_var),
        (click_effect_color_mode_var, click_effect_custom_color_var, click_effect_single_preset_var, click_effect_neon_preset_var),
    ):
        mode_var.set(mode)
        custom_var.set(custom)
        single_var.set(single)
        preset_var.set(preset)
    mark_movement_pending("Movement colour copied to all effect sections. Click Apply Movement Settings to activate it.")


def reset_movement_defaults_from_ui():
    movement_effects_enabled_var.set(False)
    movement_motion_trail_enabled_var.set(True)
    movement_speed_glow_enabled_var.set(False)
    movement_motion_streak_enabled_var.set(False)
    movement_spark_particles_enabled_var.set(False)
    movement_ripple_burst_enabled_var.set(False)
    movement_comet_tail_enabled_var.set(False)
    movement_speed_lines_enabled_var.set(False)
    movement_magnetic_orbit_enabled_var.set(False)
    click_effects_enabled_var.set(False)
    click_effect_left_enabled_var.set(True)
    click_effect_right_enabled_var.set(True)
    click_effect_style_var.set("Ripple + Sparks")
    motion_trail_length_var.set(12)
    motion_trail_length_label_var.set("12")
    motion_trail_fade_var.set(0.65)
    motion_trail_fade_label_var.set("0.65")
    speed_glow_strength_var.set(0.65)
    speed_glow_strength_label_var.set("0.65")
    speed_glow_threshold_var.set(900.0)
    speed_glow_threshold_label_var.set("900 px/s")
    motion_streak_strength_var.set(0.65)
    motion_streak_strength_label_var.set("0.65")
    motion_streak_threshold_var.set(750.0)
    motion_streak_threshold_label_var.set("750 px/s")
    motion_streak_length_var.set(72)
    motion_streak_length_label_var.set("72 px")
    spark_particle_strength_var.set(0.70)
    spark_particle_strength_label_var.set("0.70")
    spark_particle_threshold_var.set(450.0)
    spark_particle_threshold_label_var.set("450 px/s")
    spark_particle_amount_var.set(4)
    spark_particle_amount_label_var.set("4")
    spark_particle_size_var.set(4)
    spark_particle_size_label_var.set("4 px")
    spark_particle_lifetime_var.set(0.60)
    spark_particle_lifetime_label_var.set("0.60s")
    ripple_burst_strength_var.set(0.70)
    ripple_burst_strength_label_var.set("0.70")
    ripple_burst_threshold_var.set(650.0)
    ripple_burst_threshold_label_var.set("650 px/s")
    ripple_burst_lifetime_var.set(0.75)
    ripple_burst_lifetime_label_var.set("0.75s")
    ripple_burst_radius_var.set(70)
    ripple_burst_radius_label_var.set("70 px")
    comet_tail_strength_var.set(0.65)
    comet_tail_strength_label_var.set("0.65")
    comet_tail_length_var.set(90)
    comet_tail_length_label_var.set("90 px")
    comet_tail_thickness_var.set(7)
    comet_tail_thickness_label_var.set("7 px")
    speed_lines_strength_var.set(0.65)
    speed_lines_strength_label_var.set("0.65")
    speed_lines_threshold_var.set(800.0)
    speed_lines_threshold_label_var.set("800 px/s")
    speed_lines_amount_var.set(5)
    speed_lines_amount_label_var.set("5")
    speed_lines_length_var.set(90)
    speed_lines_length_label_var.set("90 px")
    magnetic_orbit_strength_var.set(0.60)
    magnetic_orbit_strength_label_var.set("0.60")
    magnetic_orbit_threshold_var.set(250.0)
    magnetic_orbit_threshold_label_var.set("250 px/s")
    magnetic_orbit_radius_var.set(26)
    magnetic_orbit_radius_label_var.set("26 px")
    magnetic_orbit_dots_var.set(5)
    magnetic_orbit_dots_label_var.set("5")
    click_effect_strength_var.set(0.75)
    click_effect_strength_label_var.set("0.75")
    click_effect_radius_var.set(72)
    click_effect_radius_label_var.set("72 px")
    click_effect_lifetime_var.set(0.65)
    click_effect_lifetime_label_var.set("0.65s")
    click_effect_spark_amount_var.set(8)
    click_effect_spark_amount_label_var.set("8")
    for mode_var, custom_var, single_var, preset_var in (
        (motion_trail_color_mode_var, motion_trail_custom_color_var, motion_trail_single_preset_var, motion_trail_neon_preset_var),
        (speed_glow_color_mode_var, speed_glow_custom_color_var, speed_glow_single_preset_var, speed_glow_neon_preset_var),
        (motion_streak_color_mode_var, motion_streak_custom_color_var, motion_streak_single_preset_var, motion_streak_neon_preset_var),
        (spark_particle_color_mode_var, spark_particle_custom_color_var, spark_particle_single_preset_var, spark_particle_neon_preset_var),
        (ripple_burst_color_mode_var, ripple_burst_custom_color_var, ripple_burst_single_preset_var, ripple_burst_neon_preset_var),
        (comet_tail_color_mode_var, comet_tail_custom_color_var, comet_tail_single_preset_var, comet_tail_neon_preset_var),
        (speed_lines_color_mode_var, speed_lines_custom_color_var, speed_lines_single_preset_var, speed_lines_neon_preset_var),
        (magnetic_orbit_color_mode_var, magnetic_orbit_custom_color_var, magnetic_orbit_single_preset_var, magnetic_orbit_neon_preset_var),
        (click_effect_color_mode_var, click_effect_custom_color_var, click_effect_single_preset_var, click_effect_neon_preset_var),
    ):
        mode_var.set(MOVEMENT_DEFAULT_COLOR_MODE)
        custom_var.set(MOVEMENT_DEFAULT_CUSTOM_COLOR)
        single_var.set(MOVEMENT_DEFAULT_SINGLE_PRESET)
        preset_var.set(MOVEMENT_DEFAULT_NEON_PRESET)
    apply_movement_settings_from_ui(show_message=True)


def apply_movement_settings_from_ui(show_message=False):
    global MOVEMENT_EFFECTS_ENABLED, MOVEMENT_EFFECT_STYLE
    global MOVEMENT_MOTION_TRAIL_ENABLED, MOVEMENT_SPEED_GLOW_ENABLED, MOVEMENT_MOTION_STREAK_ENABLED, MOVEMENT_SPARK_PARTICLES_ENABLED
    global MOVEMENT_RIPPLE_BURST_ENABLED, MOVEMENT_COMET_TAIL_ENABLED, MOVEMENT_SPEED_LINES_ENABLED, MOVEMENT_MAGNETIC_ORBIT_ENABLED
    global CLICK_EFFECTS_ENABLED, CLICK_EFFECT_LEFT_ENABLED, CLICK_EFFECT_RIGHT_ENABLED, CLICK_EFFECT_STYLE
    global MOTION_TRAIL_COLOR_MODE, MOTION_TRAIL_CUSTOM_COLOR, MOTION_TRAIL_SINGLE_PRESET, MOTION_TRAIL_NEON_PRESET
    global SPEED_GLOW_COLOR_MODE, SPEED_GLOW_CUSTOM_COLOR, SPEED_GLOW_SINGLE_PRESET, SPEED_GLOW_NEON_PRESET
    global MOTION_STREAK_COLOR_MODE, MOTION_STREAK_CUSTOM_COLOR, MOTION_STREAK_SINGLE_PRESET, MOTION_STREAK_NEON_PRESET
    global SPARK_PARTICLE_COLOR_MODE, SPARK_PARTICLE_CUSTOM_COLOR, SPARK_PARTICLE_SINGLE_PRESET, SPARK_PARTICLE_NEON_PRESET
    global RIPPLE_BURST_COLOR_MODE, RIPPLE_BURST_CUSTOM_COLOR, RIPPLE_BURST_SINGLE_PRESET, RIPPLE_BURST_NEON_PRESET
    global COMET_TAIL_COLOR_MODE, COMET_TAIL_CUSTOM_COLOR, COMET_TAIL_SINGLE_PRESET, COMET_TAIL_NEON_PRESET
    global SPEED_LINES_COLOR_MODE, SPEED_LINES_CUSTOM_COLOR, SPEED_LINES_SINGLE_PRESET, SPEED_LINES_NEON_PRESET
    global MAGNETIC_ORBIT_COLOR_MODE, MAGNETIC_ORBIT_CUSTOM_COLOR, MAGNETIC_ORBIT_SINGLE_PRESET, MAGNETIC_ORBIT_NEON_PRESET
    global CLICK_EFFECT_COLOR_MODE, CLICK_EFFECT_CUSTOM_COLOR, CLICK_EFFECT_SINGLE_PRESET, CLICK_EFFECT_NEON_PRESET
    global MOTION_TRAIL_LENGTH, MOTION_TRAIL_FADE_STRENGTH
    global SPEED_GLOW_STRENGTH, SPEED_GLOW_THRESHOLD
    global MOTION_STREAK_STRENGTH, MOTION_STREAK_THRESHOLD, MOTION_STREAK_LENGTH
    global SPARK_PARTICLE_STRENGTH, SPARK_PARTICLE_THRESHOLD, SPARK_PARTICLE_AMOUNT, SPARK_PARTICLE_SIZE, SPARK_PARTICLE_LIFETIME
    global RIPPLE_BURST_STRENGTH, RIPPLE_BURST_THRESHOLD, RIPPLE_BURST_LIFETIME, RIPPLE_BURST_RADIUS
    global COMET_TAIL_STRENGTH, COMET_TAIL_LENGTH, COMET_TAIL_THICKNESS
    global SPEED_LINES_STRENGTH, SPEED_LINES_THRESHOLD, SPEED_LINES_AMOUNT, SPEED_LINES_LENGTH
    global MAGNETIC_ORBIT_STRENGTH, MAGNETIC_ORBIT_THRESHOLD, MAGNETIC_ORBIT_RADIUS, MAGNETIC_ORBIT_DOTS
    global CLICK_EFFECT_STRENGTH, CLICK_EFFECT_RADIUS, CLICK_EFFECT_LIFETIME, CLICK_EFFECT_SPARK_AMOUNT

    MOVEMENT_EFFECTS_ENABLED = bool(movement_effects_enabled_var.get())
    MOVEMENT_MOTION_TRAIL_ENABLED = bool(movement_motion_trail_enabled_var.get())
    MOVEMENT_SPEED_GLOW_ENABLED = bool(movement_speed_glow_enabled_var.get())
    MOVEMENT_MOTION_STREAK_ENABLED = bool(movement_motion_streak_enabled_var.get())
    MOVEMENT_SPARK_PARTICLES_ENABLED = bool(movement_spark_particles_enabled_var.get())
    MOVEMENT_RIPPLE_BURST_ENABLED = bool(movement_ripple_burst_enabled_var.get())
    MOVEMENT_COMET_TAIL_ENABLED = bool(movement_comet_tail_enabled_var.get())
    MOVEMENT_SPEED_LINES_ENABLED = bool(movement_speed_lines_enabled_var.get())
    MOVEMENT_MAGNETIC_ORBIT_ENABLED = bool(movement_magnetic_orbit_enabled_var.get())
    CLICK_EFFECTS_ENABLED = bool(click_effects_enabled_var.get())
    CLICK_EFFECT_LEFT_ENABLED = bool(click_effect_left_enabled_var.get())
    CLICK_EFFECT_RIGHT_ENABLED = bool(click_effect_right_enabled_var.get())
    CLICK_EFFECT_STYLE = click_effect_style_var.get() or "Ripple + Sparks"

    # Keep the old style string as a readable summary for older preset/config flows.
    active = []
    if MOVEMENT_MOTION_TRAIL_ENABLED:
        active.append("Motion Trail")
    if MOVEMENT_SPEED_GLOW_ENABLED:
        active.append("Speed Glow")
    if MOVEMENT_MOTION_STREAK_ENABLED:
        active.append("Motion Streak")
    if MOVEMENT_SPARK_PARTICLES_ENABLED:
        active.append("Spark Particles")
    if MOVEMENT_RIPPLE_BURST_ENABLED:
        active.append("Ripple Burst")
    if MOVEMENT_COMET_TAIL_ENABLED:
        active.append("Comet Tail")
    if MOVEMENT_SPEED_LINES_ENABLED:
        active.append("Speed Lines")
    if MOVEMENT_MAGNETIC_ORBIT_ENABLED:
        active.append("Magnetic Orbit")
    if CLICK_EFFECTS_ENABLED:
        active.append("Click Effects")
    MOVEMENT_EFFECT_STYLE = " + ".join(active) if active else "Disabled"

    MOTION_TRAIL_COLOR_MODE = motion_trail_color_mode_var.get() or MOVEMENT_DEFAULT_COLOR_MODE
    MOTION_TRAIL_CUSTOM_COLOR, _rgb = parse_hex_color(motion_trail_custom_color_var.get() or MOVEMENT_DEFAULT_CUSTOM_COLOR)
    MOTION_TRAIL_SINGLE_PRESET = motion_trail_single_preset_var.get() or MOVEMENT_DEFAULT_SINGLE_PRESET
    MOTION_TRAIL_NEON_PRESET = motion_trail_neon_preset_var.get() or MOVEMENT_DEFAULT_NEON_PRESET
    SPEED_GLOW_COLOR_MODE = speed_glow_color_mode_var.get() or MOVEMENT_DEFAULT_COLOR_MODE
    SPEED_GLOW_CUSTOM_COLOR, _rgb = parse_hex_color(speed_glow_custom_color_var.get() or MOVEMENT_DEFAULT_CUSTOM_COLOR)
    SPEED_GLOW_SINGLE_PRESET = speed_glow_single_preset_var.get() or MOVEMENT_DEFAULT_SINGLE_PRESET
    SPEED_GLOW_NEON_PRESET = speed_glow_neon_preset_var.get() or MOVEMENT_DEFAULT_NEON_PRESET
    MOTION_STREAK_COLOR_MODE = motion_streak_color_mode_var.get() or MOVEMENT_DEFAULT_COLOR_MODE
    MOTION_STREAK_CUSTOM_COLOR, _rgb = parse_hex_color(motion_streak_custom_color_var.get() or MOVEMENT_DEFAULT_CUSTOM_COLOR)
    MOTION_STREAK_SINGLE_PRESET = motion_streak_single_preset_var.get() or MOVEMENT_DEFAULT_SINGLE_PRESET
    MOTION_STREAK_NEON_PRESET = motion_streak_neon_preset_var.get() or MOVEMENT_DEFAULT_NEON_PRESET
    SPARK_PARTICLE_COLOR_MODE = spark_particle_color_mode_var.get() or MOVEMENT_DEFAULT_COLOR_MODE
    SPARK_PARTICLE_CUSTOM_COLOR, _rgb = parse_hex_color(spark_particle_custom_color_var.get() or MOVEMENT_DEFAULT_CUSTOM_COLOR)
    SPARK_PARTICLE_SINGLE_PRESET = spark_particle_single_preset_var.get() or MOVEMENT_DEFAULT_SINGLE_PRESET
    SPARK_PARTICLE_NEON_PRESET = spark_particle_neon_preset_var.get() or MOVEMENT_DEFAULT_NEON_PRESET
    RIPPLE_BURST_COLOR_MODE = ripple_burst_color_mode_var.get() or MOVEMENT_DEFAULT_COLOR_MODE
    RIPPLE_BURST_CUSTOM_COLOR, _rgb = parse_hex_color(ripple_burst_custom_color_var.get() or MOVEMENT_DEFAULT_CUSTOM_COLOR)
    RIPPLE_BURST_SINGLE_PRESET = ripple_burst_single_preset_var.get() or MOVEMENT_DEFAULT_SINGLE_PRESET
    RIPPLE_BURST_NEON_PRESET = ripple_burst_neon_preset_var.get() or MOVEMENT_DEFAULT_NEON_PRESET
    COMET_TAIL_COLOR_MODE = comet_tail_color_mode_var.get() or MOVEMENT_DEFAULT_COLOR_MODE
    COMET_TAIL_CUSTOM_COLOR, _rgb = parse_hex_color(comet_tail_custom_color_var.get() or MOVEMENT_DEFAULT_CUSTOM_COLOR)
    COMET_TAIL_SINGLE_PRESET = comet_tail_single_preset_var.get() or MOVEMENT_DEFAULT_SINGLE_PRESET
    COMET_TAIL_NEON_PRESET = comet_tail_neon_preset_var.get() or MOVEMENT_DEFAULT_NEON_PRESET
    SPEED_LINES_COLOR_MODE = speed_lines_color_mode_var.get() or MOVEMENT_DEFAULT_COLOR_MODE
    SPEED_LINES_CUSTOM_COLOR, _rgb = parse_hex_color(speed_lines_custom_color_var.get() or MOVEMENT_DEFAULT_CUSTOM_COLOR)
    SPEED_LINES_SINGLE_PRESET = speed_lines_single_preset_var.get() or MOVEMENT_DEFAULT_SINGLE_PRESET
    SPEED_LINES_NEON_PRESET = speed_lines_neon_preset_var.get() or MOVEMENT_DEFAULT_NEON_PRESET
    MAGNETIC_ORBIT_COLOR_MODE = magnetic_orbit_color_mode_var.get() or MOVEMENT_DEFAULT_COLOR_MODE
    MAGNETIC_ORBIT_CUSTOM_COLOR, _rgb = parse_hex_color(magnetic_orbit_custom_color_var.get() or MOVEMENT_DEFAULT_CUSTOM_COLOR)
    MAGNETIC_ORBIT_SINGLE_PRESET = magnetic_orbit_single_preset_var.get() or MOVEMENT_DEFAULT_SINGLE_PRESET
    MAGNETIC_ORBIT_NEON_PRESET = magnetic_orbit_neon_preset_var.get() or MOVEMENT_DEFAULT_NEON_PRESET
    CLICK_EFFECT_COLOR_MODE = click_effect_color_mode_var.get() or MOVEMENT_DEFAULT_COLOR_MODE
    CLICK_EFFECT_CUSTOM_COLOR, _rgb = parse_hex_color(click_effect_custom_color_var.get() or MOVEMENT_DEFAULT_CUSTOM_COLOR)
    CLICK_EFFECT_SINGLE_PRESET = click_effect_single_preset_var.get() or MOVEMENT_DEFAULT_SINGLE_PRESET
    CLICK_EFFECT_NEON_PRESET = click_effect_neon_preset_var.get() or MOVEMENT_DEFAULT_NEON_PRESET

    MOTION_TRAIL_LENGTH = safe_int_from_var(motion_trail_length_var, MOTION_TRAIL_LENGTH, minimum=3, maximum=40)
    MOTION_TRAIL_FADE_STRENGTH = round(safe_float_from_var(motion_trail_fade_var, MOTION_TRAIL_FADE_STRENGTH, minimum=0.10, maximum=1.0), 2)
    SPEED_GLOW_STRENGTH = round(safe_float_from_var(speed_glow_strength_var, SPEED_GLOW_STRENGTH, minimum=0.0, maximum=1.0), 2)
    SPEED_GLOW_THRESHOLD = round(safe_float_from_var(speed_glow_threshold_var, SPEED_GLOW_THRESHOLD, minimum=150.0, maximum=2500.0), 0)
    MOTION_STREAK_STRENGTH = round(safe_float_from_var(motion_streak_strength_var, MOTION_STREAK_STRENGTH, minimum=0.0, maximum=1.0), 2)
    MOTION_STREAK_THRESHOLD = round(safe_float_from_var(motion_streak_threshold_var, MOTION_STREAK_THRESHOLD, minimum=150.0, maximum=2500.0), 0)
    MOTION_STREAK_LENGTH = safe_int_from_var(motion_streak_length_var, MOTION_STREAK_LENGTH, minimum=20, maximum=180)
    SPARK_PARTICLE_STRENGTH = round(safe_float_from_var(spark_particle_strength_var, SPARK_PARTICLE_STRENGTH, minimum=0.0, maximum=1.0), 2)
    SPARK_PARTICLE_THRESHOLD = round(safe_float_from_var(spark_particle_threshold_var, SPARK_PARTICLE_THRESHOLD, minimum=100.0, maximum=2500.0), 0)
    SPARK_PARTICLE_AMOUNT = safe_int_from_var(spark_particle_amount_var, SPARK_PARTICLE_AMOUNT, minimum=1, maximum=12)
    SPARK_PARTICLE_SIZE = safe_int_from_var(spark_particle_size_var, SPARK_PARTICLE_SIZE, minimum=2, maximum=10)
    SPARK_PARTICLE_LIFETIME = round(safe_float_from_var(spark_particle_lifetime_var, SPARK_PARTICLE_LIFETIME, minimum=0.20, maximum=2.0), 2)
    RIPPLE_BURST_STRENGTH = round(safe_float_from_var(ripple_burst_strength_var, RIPPLE_BURST_STRENGTH, minimum=0.0, maximum=1.0), 2)
    RIPPLE_BURST_THRESHOLD = round(safe_float_from_var(ripple_burst_threshold_var, RIPPLE_BURST_THRESHOLD, minimum=100.0, maximum=3000.0), 0)
    RIPPLE_BURST_LIFETIME = round(safe_float_from_var(ripple_burst_lifetime_var, RIPPLE_BURST_LIFETIME, minimum=0.25, maximum=2.0), 2)
    RIPPLE_BURST_RADIUS = safe_int_from_var(ripple_burst_radius_var, RIPPLE_BURST_RADIUS, minimum=20, maximum=180)
    COMET_TAIL_STRENGTH = round(safe_float_from_var(comet_tail_strength_var, COMET_TAIL_STRENGTH, minimum=0.0, maximum=1.0), 2)
    COMET_TAIL_LENGTH = safe_int_from_var(comet_tail_length_var, COMET_TAIL_LENGTH, minimum=30, maximum=240)
    COMET_TAIL_THICKNESS = safe_int_from_var(comet_tail_thickness_var, COMET_TAIL_THICKNESS, minimum=2, maximum=18)
    SPEED_LINES_STRENGTH = round(safe_float_from_var(speed_lines_strength_var, SPEED_LINES_STRENGTH, minimum=0.0, maximum=1.0), 2)
    SPEED_LINES_THRESHOLD = round(safe_float_from_var(speed_lines_threshold_var, SPEED_LINES_THRESHOLD, minimum=150.0, maximum=3000.0), 0)
    SPEED_LINES_AMOUNT = safe_int_from_var(speed_lines_amount_var, SPEED_LINES_AMOUNT, minimum=1, maximum=12)
    SPEED_LINES_LENGTH = safe_int_from_var(speed_lines_length_var, SPEED_LINES_LENGTH, minimum=20, maximum=180)
    MAGNETIC_ORBIT_STRENGTH = round(safe_float_from_var(magnetic_orbit_strength_var, MAGNETIC_ORBIT_STRENGTH, minimum=0.0, maximum=1.0), 2)
    MAGNETIC_ORBIT_THRESHOLD = round(safe_float_from_var(magnetic_orbit_threshold_var, MAGNETIC_ORBIT_THRESHOLD, minimum=0.0, maximum=2000.0), 0)
    MAGNETIC_ORBIT_RADIUS = safe_int_from_var(magnetic_orbit_radius_var, MAGNETIC_ORBIT_RADIUS, minimum=8, maximum=80)
    MAGNETIC_ORBIT_DOTS = safe_int_from_var(magnetic_orbit_dots_var, MAGNETIC_ORBIT_DOTS, minimum=2, maximum=12)
    CLICK_EFFECT_STRENGTH = round(safe_float_from_var(click_effect_strength_var, CLICK_EFFECT_STRENGTH, minimum=0.0, maximum=1.0), 2)
    CLICK_EFFECT_RADIUS = safe_int_from_var(click_effect_radius_var, CLICK_EFFECT_RADIUS, minimum=20, maximum=180)
    CLICK_EFFECT_LIFETIME = round(safe_float_from_var(click_effect_lifetime_var, CLICK_EFFECT_LIFETIME, minimum=0.20, maximum=2.0), 2)
    CLICK_EFFECT_SPARK_AMOUNT = safe_int_from_var(click_effect_spark_amount_var, CLICK_EFFECT_SPARK_AMOUNT, minimum=1, maximum=20)

    # Movement effect colours can affect cached cursor images, especially the
    # Motion Trail ghost cursor. Clear both trail points and image cache after
    # applying movement settings so colour changes take effect immediately.
    invalidate_cursor_image_cache()
    clear_motion_trail()
    clear_spark_particles()
    clear_ripple_bursts()
    clear_click_effects()
    set_movement_vars_from_globals()
    update_panel_status()
    if show_message:
        refresh_movement_summary("Movement settings applied.")


def add_motion_trail_point(x, y, scale, now, moving):
    global last_motion_trail_x, last_motion_trail_y

    if not motion_trail_active() and not comet_tail_active():
        clear_motion_trail()
        return

    if not moving:
        return

    try:
        x = float(x)
        y = float(y)
        scale = float(scale)
    except Exception:
        return

    if last_motion_trail_x is not None and last_motion_trail_y is not None:
        if math.hypot(x - last_motion_trail_x, y - last_motion_trail_y) < MOTION_TRAIL_MIN_DISTANCE:
            return

    motion_trail_points.append({"x": x, "y": y, "scale": scale, "time": float(now)})
    last_motion_trail_x = x
    last_motion_trail_y = y

    max_len = int(max(3, min(40, MOTION_TRAIL_LENGTH)))
    if len(motion_trail_points) > max_len:
        del motion_trail_points[:-max_len]


def build_motion_trail_draw_items(now):
    if not motion_trail_active() or not motion_trail_points:
        return []

    max_len = max(1, len(motion_trail_points))
    fade_strength = clamp(float(MOTION_TRAIL_FADE_STRENGTH), 0.10, 1.0)
    result = []

    # Draw oldest first so the newest ghost appears closest to the cursor.
    for index, point in enumerate(motion_trail_points):
        age_factor = (index + 1) / max_len
        alpha = (age_factor ** (0.75 + (1.0 - fade_strength) * 1.6)) * (0.12 + 0.55 * fade_strength)
        # Fade out old trail points while stopped instead of leaving a hard tail.
        time_age = max(0.0, float(now) - float(point.get("time", now)))
        alpha *= max(0.0, 1.0 - time_age * 0.80)
        if alpha <= 0.03:
            continue
        scale = float(point.get("scale", REAL_DRAWN_CURSOR_SCALE)) * (0.82 + 0.18 * age_factor)
        result.append((float(point.get("x", 0)), float(point.get("y", 0)), scale, "motion_trail", alpha))

    # Drop fully aged points occasionally to keep the list light.
    if len(motion_trail_points) > int(max(3, min(40, MOTION_TRAIL_LENGTH))):
        del motion_trail_points[:-int(MOTION_TRAIL_LENGTH)]
    return result



def speed_glow_intensity(real_distance, dt):
    if not speed_glow_active():
        return 0.0
    try:
        speed = float(real_distance) / max(0.001, float(dt))
        threshold = max(150.0, float(SPEED_GLOW_THRESHOLD))
        strength = clamp(float(SPEED_GLOW_STRENGTH), 0.0, 1.0)
    except Exception:
        return 0.0
    if speed <= threshold * 0.45:
        return 0.0
    return clamp(((speed - threshold * 0.45) / max(1.0, threshold * 1.10)) * strength, 0.0, 1.0)


def motion_streak_intensity(real_distance, dt):
    if not motion_streak_active():
        return 0.0
    try:
        speed = float(real_distance) / max(0.001, float(dt))
        threshold = max(150.0, float(MOTION_STREAK_THRESHOLD))
        strength = clamp(float(MOTION_STREAK_STRENGTH), 0.0, 1.0)
    except Exception:
        return 0.0
    if speed <= threshold * 0.55:
        return 0.0
    return clamp(((speed - threshold * 0.55) / max(1.0, threshold * 1.15)) * strength, 0.0, 1.0)


def get_speed_glow_colors():
    return get_movement_effect_colors("speed")


def draw_speed_glow(center_x, center_y, cursor_width, cursor_height, intensity, now):
    intensity = clamp(float(intensity), 0.0, 1.0)
    if intensity <= 0.02:
        return

    colors = get_speed_glow_colors()
    pulse = 0.5 + 0.5 * math.sin(now * 10.0)
    expand = 8 + 22 * intensity + 4 * pulse
    x1 = center_x - expand
    y1 = center_y - expand
    x2 = center_x + cursor_width + expand
    y2 = center_y + cursor_height + expand

    if PERFORMANCE_REDUCE_GLOW_QUALITY:
        color = colors[0]
        canvas.create_oval(x1, y1, x2, y2, outline=color, width=max(1, int(1 + 3 * intensity)))
        return

    for idx, color in enumerate(reversed(colors)):
        offset = 5 + idx * (4 + 4 * intensity)
        darker = mix_colors(color, "#000000", 0.18 + idx * 0.08)
        canvas.create_oval(
            x1 - offset,
            y1 - offset,
            x2 + offset,
            y2 + offset,
            outline=darker,
            width=max(1, int(1 + 3 * intensity)),
        )

    for idx, color in enumerate(colors):
        offset = idx * (3 + 3 * intensity)
        canvas.create_oval(
            x1 + offset,
            y1 + offset,
            x2 - offset,
            y2 - offset,
            outline=mix_colors(color, "#ffffff", 0.10),
            width=max(1, int(1 + 4 * intensity)),
        )

    if len(colors) > 1:
        start = int((now * 220) % 360)
        for idx, color in enumerate(colors):
            canvas.create_arc(
                x1 - idx * 3,
                y1 - idx * 3,
                x2 + idx * 3,
                y2 + idx * 3,
                start=start + idx * 120,
                extent=50 + int(35 * intensity),
                style="arc",
                outline=mix_colors(color, "#ffffff", 0.18),
                width=max(1, int(1 + 4 * intensity)),
            )

def draw_motion_streak(center_x, center_y, cursor_width, cursor_height, dx, dy, intensity, now):
    intensity = clamp(float(intensity), 0.0, 1.0)
    if intensity <= 0.02:
        return

    distance = math.hypot(dx, dy)
    if distance <= 0.01:
        return

    ux = float(dx) / distance
    uy = float(dy) / distance
    colors = get_movement_effect_colors("streak")
    if not colors:
        colors = ["#22d3ee"]

    cx = float(center_x) + float(cursor_width) * 0.5
    cy = float(center_y) + float(cursor_height) * 0.5
    length = clamp(float(MOTION_STREAK_LENGTH), 20.0, 180.0) * (0.45 + 0.75 * intensity)
    start_x = cx - ux * (float(cursor_width) * 0.15)
    start_y = cy - uy * (float(cursor_height) * 0.15)
    end_x = cx - ux * length
    end_y = cy - uy * length

    px = -uy
    py = ux
    pulse = 0.5 + 0.5 * math.sin(now * 14.0)

    if PERFORMANCE_REDUCE_GLOW_QUALITY:
        canvas.create_line(end_x, end_y, start_x, start_y, fill=colors[0], width=max(1, int(2 + 5 * intensity)), capstyle="round")
        return

    for idx, color in enumerate(reversed(colors)):
        spread = (idx + 1) * (2 + 5 * intensity)
        width = max(1, int(2 + 7 * intensity - idx))
        darker = mix_colors(color, "#000000", 0.18 + idx * 0.08)
        canvas.create_line(
            end_x + px * spread,
            end_y + py * spread,
            start_x + px * (spread * 0.25),
            start_y + py * (spread * 0.25),
            fill=darker,
            width=width,
            capstyle="round",
        )

    for idx, color in enumerate(colors):
        spread = (idx - (len(colors) - 1) / 2.0) * (2 + 3 * intensity)
        width = max(1, int(1 + 5 * intensity + pulse))
        canvas.create_line(
            end_x + px * spread,
            end_y + py * spread,
            start_x + px * (spread * 0.25),
            start_y + py * (spread * 0.25),
            fill=mix_colors(color, "#ffffff", 0.12),
            width=width,
            capstyle="round",
        )


def spark_particle_intensity(distance, dt):
    if not spark_particles_active() or dt <= 0:
        return 0.0
    speed = float(distance) / max(0.001, float(dt))
    threshold = max(1.0, float(SPARK_PARTICLE_THRESHOLD))
    if speed < threshold:
        return 0.0
    return clamp((speed - threshold) / max(1.0, threshold * 1.8), 0.0, 1.0) * clamp(SPARK_PARTICLE_STRENGTH, 0.0, 1.0)


def spawn_spark_particles(center_x, center_y, dx, dy, intensity, now):
    global spark_particles
    if intensity <= 0.02:
        return
    speed = math.hypot(dx, dy)
    if speed <= 0.01:
        return
    ux = -dx / speed
    uy = -dy / speed
    side_x = -uy
    side_y = ux
    colors = get_movement_effect_colors("spark")
    if not colors:
        colors = [MOVEMENT_DEFAULT_CUSTOM_COLOR]
    amount = max(1, int(round(SPARK_PARTICLE_AMOUNT * (0.35 + intensity))))
    for i in range(amount):
        jitter = random.uniform(-10.0, 10.0)
        back = random.uniform(4.0, 18.0)
        x = center_x + ux * back + side_x * jitter
        y = center_y + uy * back + side_y * jitter
        velocity = random.uniform(35.0, 130.0) * (0.35 + intensity)
        scatter = random.uniform(-0.75, 0.75)
        vx = ux * velocity + side_x * scatter * velocity
        vy = uy * velocity + side_y * scatter * velocity
        color = colors[(len(spark_particles) + i) % len(colors)]
        spark_particles.append({
            "x": float(x),
            "y": float(y),
            "vx": float(vx),
            "vy": float(vy),
            "birth": float(now),
            "life": float(SPARK_PARTICLE_LIFETIME) * random.uniform(0.75, 1.15),
            "size": float(SPARK_PARTICLE_SIZE) * random.uniform(0.75, 1.25),
            "color": sanitize_neon_color(color),
        })
    if len(spark_particles) > 220:
        spark_particles = spark_particles[-220:]


def draw_spark_particles(now):
    global spark_particles
    if not spark_particles:
        return
    alive = []
    for particle in spark_particles:
        age = float(now) - float(particle.get("birth", now))
        life = max(0.05, float(particle.get("life", SPARK_PARTICLE_LIFETIME)))
        if age >= life:
            continue
        alpha = clamp(1.0 - (age / life), 0.0, 1.0)
        x = float(particle.get("x", 0.0)) + float(particle.get("vx", 0.0)) * age
        y = float(particle.get("y", 0.0)) + float(particle.get("vy", 0.0)) * age
        size = max(1.0, float(particle.get("size", SPARK_PARTICLE_SIZE)) * (0.35 + alpha * 0.85))
        color = sanitize_neon_color(particle.get("color", MOVEMENT_DEFAULT_CUSTOM_COLOR))
        # Tk canvas has no real alpha for ovals, so fade by mixing toward dark.
        fade_color = mix_colors(color, "#000000", 0.70 * (1.0 - alpha))
        canvas.create_oval(x - size, y - size, x + size, y + size, fill=fade_color, outline="")
        if alpha > 0.45 and size >= 2:
            inner = mix_colors(color, "#ffffff", 0.25)
            inner_size = size * 0.45
            canvas.create_oval(x - inner_size, y - inner_size, x + inner_size, y + inner_size, fill=inner, outline="")
        alive.append(particle)
    spark_particles = alive


def movement_speed_intensity(distance, dt, threshold, strength):
    if dt <= 0:
        return 0.0
    speed = float(distance) / max(0.001, float(dt))
    threshold = max(1.0, float(threshold))
    if speed < threshold:
        return 0.0
    return clamp((speed - threshold) / max(1.0, threshold * 1.5), 0.0, 1.0) * clamp(float(strength), 0.0, 1.0)


def ripple_burst_intensity(distance, dt):
    if not ripple_burst_active():
        return 0.0
    return movement_speed_intensity(distance, dt, RIPPLE_BURST_THRESHOLD, RIPPLE_BURST_STRENGTH)


def speed_lines_intensity(distance, dt):
    if not speed_lines_active():
        return 0.0
    return movement_speed_intensity(distance, dt, SPEED_LINES_THRESHOLD, SPEED_LINES_STRENGTH)


def magnetic_orbit_intensity(distance, dt):
    if not magnetic_orbit_active():
        return 0.0
    return movement_speed_intensity(distance, dt, max(1.0, MAGNETIC_ORBIT_THRESHOLD), MAGNETIC_ORBIT_STRENGTH)


def spawn_ripple_burst(center_x, center_y, intensity, now):
    global ripple_bursts, last_ripple_burst_time
    if intensity <= 0.05:
        return
    if float(now) - float(last_ripple_burst_time) < 0.12:
        return
    colors = get_movement_effect_colors("ripple") or [MOVEMENT_DEFAULT_CUSTOM_COLOR]
    ripple_bursts.append({
        "x": float(center_x),
        "y": float(center_y),
        "birth": float(now),
        "life": float(RIPPLE_BURST_LIFETIME),
        "radius": float(RIPPLE_BURST_RADIUS) * (0.55 + 0.75 * intensity),
        "intensity": float(intensity),
        "colors": [sanitize_neon_color(c) for c in colors],
    })
    last_ripple_burst_time = float(now)
    if len(ripple_bursts) > 24:
        ripple_bursts = ripple_bursts[-24:]


def draw_ripple_bursts(now):
    global ripple_bursts
    if not ripple_bursts:
        return
    alive = []
    for burst in ripple_bursts:
        age = float(now) - float(burst.get("birth", now))
        life = max(0.05, float(burst.get("life", RIPPLE_BURST_LIFETIME)))
        if age >= life:
            continue
        progress = clamp(age / life, 0.0, 1.0)
        alpha = 1.0 - progress
        radius = float(burst.get("radius", RIPPLE_BURST_RADIUS)) * (0.25 + 0.85 * progress)
        x = float(burst.get("x", 0.0))
        y = float(burst.get("y", 0.0))
        colors = burst.get("colors") or [MOVEMENT_DEFAULT_CUSTOM_COLOR]
        width = max(1, int(1 + 5 * alpha * float(burst.get("intensity", 0.7))))
        for idx, color in enumerate(colors[:3]):
            offset = idx * (3 + 4 * progress)
            fade_color = mix_colors(color, "#000000", 0.70 * (1.0 - alpha))
            canvas.create_oval(x - radius - offset, y - radius - offset, x + radius + offset, y + radius + offset, outline=fade_color, width=width)
        alive.append(burst)
    ripple_bursts = alive


def spawn_click_effect(center_x, center_y, button_name, now):
    global click_effect_ripples, click_effect_sparks
    if not click_effects_active():
        return
    colors = get_movement_effect_colors("click") or [MOVEMENT_DEFAULT_CUSTOM_COLOR]
    style = str(CLICK_EFFECT_STYLE or "Ripple + Sparks")
    strength = clamp(float(CLICK_EFFECT_STRENGTH), 0.0, 1.0)
    radius = float(CLICK_EFFECT_RADIUS) * (0.70 + 0.60 * strength)
    if style in ("Ripple", "Burst Ring", "Ripple + Sparks"):
        click_effect_ripples.append({
            "x": float(center_x),
            "y": float(center_y),
            "birth": float(now),
            "life": float(CLICK_EFFECT_LIFETIME),
            "radius": radius,
            "strength": strength,
            "button": str(button_name),
            "colors": [sanitize_neon_color(c) for c in colors],
        })
    if style in ("Sparks", "Ripple + Sparks"):
        amount = max(1, int(round(float(CLICK_EFFECT_SPARK_AMOUNT) * (0.55 + strength))))
        for i in range(amount):
            angle = (math.tau * i / max(1, amount)) + random.uniform(-0.22, 0.22)
            speed = random.uniform(60.0, 180.0) * (0.45 + strength)
            color = sanitize_neon_color(colors[i % len(colors)])
            click_effect_sparks.append({
                "x": float(center_x),
                "y": float(center_y),
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "birth": float(now),
                "life": float(CLICK_EFFECT_LIFETIME) * random.uniform(0.75, 1.20),
                "size": random.uniform(2.0, 5.5) * (0.60 + strength),
                "color": color,
            })
    if len(click_effect_ripples) > 36:
        click_effect_ripples = click_effect_ripples[-36:]
    if len(click_effect_sparks) > 260:
        click_effect_sparks = click_effect_sparks[-260:]


def update_click_effect_detection(center_x, center_y, now):
    global last_left_click_down, last_right_click_down
    if not click_effects_active():
        last_left_click_down = bool(key_down(VK_LBUTTON))
        last_right_click_down = bool(key_down(VK_RBUTTON))
        return
    left_down = bool(key_down(VK_LBUTTON))
    right_down = bool(key_down(VK_RBUTTON))
    if CLICK_EFFECT_LEFT_ENABLED and left_down and not last_left_click_down:
        spawn_click_effect(center_x, center_y, "left", now)
    if CLICK_EFFECT_RIGHT_ENABLED and right_down and not last_right_click_down:
        spawn_click_effect(center_x, center_y, "right", now)
    last_left_click_down = left_down
    last_right_click_down = right_down


def draw_click_effects(now):
    global click_effect_ripples, click_effect_sparks
    if click_effect_ripples:
        alive_ripples = []
        for ripple in click_effect_ripples:
            age = float(now) - float(ripple.get("birth", now))
            life = max(0.05, float(ripple.get("life", CLICK_EFFECT_LIFETIME)))
            if age >= life:
                continue
            progress = clamp(age / life, 0.0, 1.0)
            alpha = 1.0 - progress
            radius = float(ripple.get("radius", CLICK_EFFECT_RADIUS)) * (0.18 + progress * 1.05)
            x = float(ripple.get("x", 0.0))
            y = float(ripple.get("y", 0.0))
            colors = ripple.get("colors") or [MOVEMENT_DEFAULT_CUSTOM_COLOR]
            strength = clamp(float(ripple.get("strength", CLICK_EFFECT_STRENGTH)), 0.0, 1.0)
            style = str(CLICK_EFFECT_STYLE or "Ripple + Sparks")
            width_boost = 1.35 if style == "Burst Ring" else 1.0
            width = max(1, int((1 + 6 * alpha * strength) * width_boost))
            for idx, color in enumerate(colors[:3]):
                offset = idx * (4 + 5 * progress)
                fade_color = mix_colors(color, "#000000", 0.65 * (1.0 - alpha))
                canvas.create_oval(x - radius - offset, y - radius - offset, x + radius + offset, y + radius + offset, outline=fade_color, width=width)
            alive_ripples.append(ripple)
        click_effect_ripples = alive_ripples

    if click_effect_sparks:
        alive_sparks = []
        for spark in click_effect_sparks:
            age = float(now) - float(spark.get("birth", now))
            life = max(0.05, float(spark.get("life", CLICK_EFFECT_LIFETIME)))
            if age >= life:
                continue
            progress = clamp(age / life, 0.0, 1.0)
            alpha = 1.0 - progress
            x = float(spark.get("x", 0.0)) + float(spark.get("vx", 0.0)) * age
            y = float(spark.get("y", 0.0)) + float(spark.get("vy", 0.0)) * age
            size = max(1.0, float(spark.get("size", 4.0)) * (0.45 + alpha * 0.75))
            color = sanitize_neon_color(spark.get("color", MOVEMENT_DEFAULT_CUSTOM_COLOR))
            fade_color = mix_colors(color, "#000000", 0.70 * (1.0 - alpha))
            canvas.create_oval(x - size, y - size, x + size, y + size, fill=fade_color, outline="")
            if alpha > 0.45:
                inner = mix_colors(color, "#ffffff", 0.25)
                inner_size = max(0.8, size * 0.42)
                canvas.create_oval(x - inner_size, y - inner_size, x + inner_size, y + inner_size, fill=inner, outline="")
            alive_sparks.append(spark)
        click_effect_sparks = alive_sparks


def clear_click_effects():
    global click_effect_ripples, click_effect_sparks
    click_effect_ripples = []
    click_effect_sparks = []


def draw_comet_tail(now):
    if not comet_tail_active() or len(motion_trail_points) < 2:
        return
    colors = get_movement_effect_colors("comet") or [MOVEMENT_DEFAULT_CUSTOM_COLOR]
    pts = motion_trail_points[-max(3, int(COMET_TAIL_LENGTH / 8)):]
    max_pairs = max(1, len(pts) - 1)
    strength = clamp(COMET_TAIL_STRENGTH, 0.0, 1.0)
    for idx in range(1, len(pts)):
        p0 = pts[idx - 1]
        p1 = pts[idx]
        age_factor = idx / max_pairs
        time_age = max(0.0, float(now) - float(p1.get("time", now)))
        fade = clamp((age_factor ** 1.4) * max(0.0, 1.0 - time_age * 0.70) * strength, 0.0, 1.0)
        if fade <= 0.04:
            continue
        color = sanitize_neon_color(colors[idx % len(colors)])
        draw_color = mix_colors(color, "#000000", 0.65 * (1.0 - fade))
        width = max(1, int(COMET_TAIL_THICKNESS * (0.35 + fade)))
        canvas.create_line(float(p0["x"]), float(p0["y"]), float(p1["x"]), float(p1["y"]), fill=draw_color, width=width, capstyle="round", smooth=True)


def draw_speed_lines(center_x, center_y, cursor_width, cursor_height, dx, dy, intensity, now):
    intensity = clamp(float(intensity), 0.0, 1.0)
    if intensity <= 0.03:
        return
    distance = math.hypot(dx, dy)
    if distance <= 0.01:
        return
    ux = float(dx) / distance
    uy = float(dy) / distance
    side_x = -uy
    side_y = ux
    colors = get_movement_effect_colors("lines") or [MOVEMENT_DEFAULT_CUSTOM_COLOR]
    amount = max(1, int(SPEED_LINES_AMOUNT))
    base_x = float(center_x) + float(cursor_width) * 0.5
    base_y = float(center_y) + float(cursor_height) * 0.5
    length = float(SPEED_LINES_LENGTH) * (0.45 + 0.85 * intensity)
    for i in range(amount):
        spread = (i - (amount - 1) / 2.0) * (5 + 8 * intensity)
        back = 8 + i * 3
        start_x = base_x - ux * back + side_x * spread
        start_y = base_y - uy * back + side_y * spread
        end_x = start_x - ux * length
        end_y = start_y - uy * length
        color = colors[i % len(colors)]
        width = max(1, int(1 + 4 * intensity * (1.0 - i / max(1, amount * 1.5))))
        canvas.create_line(end_x, end_y, start_x, start_y, fill=mix_colors(color, "#ffffff", 0.08), width=width, capstyle="round")


def draw_magnetic_orbit(center_x, center_y, cursor_width, cursor_height, intensity, now):
    intensity = clamp(float(intensity), 0.0, 1.0)
    if intensity <= 0.03:
        return
    colors = get_movement_effect_colors("orbit") or [MOVEMENT_DEFAULT_CUSTOM_COLOR]
    count = max(2, int(MAGNETIC_ORBIT_DOTS))
    radius = float(MAGNETIC_ORBIT_RADIUS) * (0.75 + intensity * 0.55)
    cx = float(center_x) + float(cursor_width) * 0.5
    cy = float(center_y) + float(cursor_height) * 0.5
    spin = now * (4.0 + 7.0 * intensity)
    for i in range(count):
        angle = spin + math.tau * i / count
        x = cx + math.cos(angle) * radius
        y = cy + math.sin(angle) * radius
        color = sanitize_neon_color(colors[i % len(colors)])
        dot_size = 2.0 + 4.0 * intensity * (0.65 + 0.35 * math.sin(angle + now * 3.0))
        canvas.create_oval(x - dot_size, y - dot_size, x + dot_size, y + dot_size, fill=color, outline="")
        if dot_size > 2.5:
            inner = mix_colors(color, "#ffffff", 0.30)
            canvas.create_oval(x - dot_size*0.4, y - dot_size*0.4, x + dot_size*0.4, y + dot_size*0.4, fill=inner, outline="")


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
        f"Movement Threshold: {MOVE_DISTANCE_THRESHOLD:.2f} | Wobble: {FAKE_CURSOR_WOBBLE:.2f}x | Fake Scale: {FAKE_CURSOR_SCALE_MULTIPLIER:.2f}x | Randomize Draw Order: {RANDOMIZE_DRAW_ORDER}"
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
    if "apply_cursor_lab_from_ui" in globals():
        apply_cursor_lab_from_ui(show_message=False)
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
        "fake_cursor_scale_multiplier": float(FAKE_CURSOR_SCALE_MULTIPLIER),
        "cursor_tint_enabled": bool(CURSOR_TINT_ENABLED),
        "cursor_tint_style": str(CURSOR_TINT_STYLE),
        "cursor_tint_multi_preset": str(CURSOR_TINT_MULTI_PRESET),
        "cursor_tint_color": str(CURSOR_TINT_COLOR),
        "cursor_tint_strength": float(CURSOR_TINT_STRENGTH),
        "cursor_tint_bright_neon": bool(CURSOR_TINT_BRIGHT_NEON),
        "cursor_tint_neon_brightness": float(CURSOR_TINT_NEON_BRIGHTNESS),
        "cursor_tint_black_outline": bool(CURSOR_TINT_BLACK_OUTLINE),
        "cursor_tint_outline_thickness": int(CURSOR_TINT_OUTLINE_THICKNESS),
        "cursor_tint_apply_drawn": bool(CURSOR_TINT_APPLY_DRAWN),
        "cursor_tint_apply_fake": bool(CURSOR_TINT_APPLY_FAKE),
        "custom_cursor_enabled": bool(CUSTOM_CURSOR_ENABLED),
        "custom_cursor_image_path": str(CUSTOM_CURSOR_IMAGE_PATH),
        "custom_cursor_hotspot_mode": str(CUSTOM_CURSOR_HOTSPOT_MODE),
        "cursor_shape_mode": str(CURSOR_SHAPE_MODE),
        "cursor_use_real_windows_ani": bool(CURSOR_USE_REAL_WINDOWS_ANI),
        "cursor_animation_speed_mode": str(CURSOR_ANIMATION_SPEED_MODE),
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
        f"Real Cursor Scale: {float(config.get('real_drawn_cursor_scale', REAL_DRAWN_CURSOR_SCALE)):.2f}x | Fake Scale: {float(config.get('fake_cursor_scale_multiplier', FAKE_CURSOR_SCALE_MULTIPLIER)):.2f}x | Manual Offset: ({int(config.get('manual_offset_x', manual_offset_x))}, {int(config.get('manual_offset_y', manual_offset_y))})\n"
        f"Cursor Lab: Tint {config.get('cursor_tint_enabled', CURSOR_TINT_ENABLED)} {config.get('cursor_tint_color', CURSOR_TINT_COLOR)} | Custom Image: {config.get('custom_cursor_enabled', CUSTOM_CURSOR_ENABLED)}"
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
        ensure_cursor_image_for_scale(REAL_DRAWN_CURSOR_SCALE, "drawn")
    except (TypeError, ValueError):
        pass

    apply_cursor_lab_config(config)

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



# -----------------------------
# Full Cursor Theme system (v13.9)
# -----------------------------
THEME_EXTRA_GLOBAL_KEYS = [
    "IDLE_EFFECT_ENABLED", "IDLE_EFFECT_STYLE", "IDLE_EFFECT_DELAY", "IDLE_EFFECT_STRENGTH",
    "IDLE_EFFECT_NEON_ENABLED", "IDLE_EFFECT_NEON_PRESET", "IDLE_EFFECT_NEON_COLOR",
    "PERFORMANCE_MODE", "PERFORMANCE_TARGET_FPS", "PERFORMANCE_REDUCE_GLOW_QUALITY",
    "PERFORMANCE_PAUSE_SWARM_ON_LONG_IDLE", "PERFORMANCE_PAUSE_IDLE_EFFECTS_ON_LONG_IDLE", "PERFORMANCE_LONG_IDLE_SECONDS",
    "MOVEMENT_EFFECTS_ENABLED", "MOVEMENT_EFFECT_STYLE", "MOVEMENT_MOTION_TRAIL_ENABLED", "MOVEMENT_SPEED_GLOW_ENABLED",
    "MOVEMENT_MOTION_STREAK_ENABLED", "MOVEMENT_SPARK_PARTICLES_ENABLED", "MOVEMENT_RIPPLE_BURST_ENABLED",
    "MOVEMENT_COMET_TAIL_ENABLED", "MOVEMENT_SPEED_LINES_ENABLED", "MOVEMENT_MAGNETIC_ORBIT_ENABLED",
    "MOTION_TRAIL_LENGTH", "MOTION_TRAIL_FADE_STRENGTH",
    "SPEED_GLOW_STRENGTH", "SPEED_GLOW_THRESHOLD", "SPEED_GLOW_COLOR_MODE", "SPEED_GLOW_CUSTOM_COLOR", "SPEED_GLOW_SINGLE_PRESET", "SPEED_GLOW_NEON_PRESET",
    "MOTION_STREAK_STRENGTH", "MOTION_STREAK_THRESHOLD", "MOTION_STREAK_LENGTH", "MOTION_STREAK_COLOR_MODE", "MOTION_STREAK_CUSTOM_COLOR", "MOTION_STREAK_SINGLE_PRESET", "MOTION_STREAK_NEON_PRESET",
    "SPARK_PARTICLE_STRENGTH", "SPARK_PARTICLE_THRESHOLD", "SPARK_PARTICLE_AMOUNT", "SPARK_PARTICLE_SIZE", "SPARK_PARTICLE_LIFETIME", "SPARK_PARTICLE_COLOR_MODE", "SPARK_PARTICLE_CUSTOM_COLOR", "SPARK_PARTICLE_SINGLE_PRESET", "SPARK_PARTICLE_NEON_PRESET",
    "RIPPLE_BURST_STRENGTH", "RIPPLE_BURST_THRESHOLD", "RIPPLE_BURST_LIFETIME", "RIPPLE_BURST_RADIUS", "RIPPLE_BURST_COLOR_MODE", "RIPPLE_BURST_CUSTOM_COLOR", "RIPPLE_BURST_SINGLE_PRESET", "RIPPLE_BURST_NEON_PRESET",
    "COMET_TAIL_STRENGTH", "COMET_TAIL_LENGTH", "COMET_TAIL_THICKNESS", "COMET_TAIL_COLOR_MODE", "COMET_TAIL_CUSTOM_COLOR", "COMET_TAIL_SINGLE_PRESET", "COMET_TAIL_NEON_PRESET",
    "SPEED_LINES_STRENGTH", "SPEED_LINES_THRESHOLD", "SPEED_LINES_AMOUNT", "SPEED_LINES_LENGTH", "SPEED_LINES_COLOR_MODE", "SPEED_LINES_CUSTOM_COLOR", "SPEED_LINES_SINGLE_PRESET", "SPEED_LINES_NEON_PRESET",
    "MAGNETIC_ORBIT_STRENGTH", "MAGNETIC_ORBIT_THRESHOLD", "MAGNETIC_ORBIT_RADIUS", "MAGNETIC_ORBIT_DOTS", "MAGNETIC_ORBIT_COLOR_MODE", "MAGNETIC_ORBIT_CUSTOM_COLOR", "MAGNETIC_ORBIT_SINGLE_PRESET", "MAGNETIC_ORBIT_NEON_PRESET",
    "CLICK_EFFECTS_ENABLED", "CLICK_EFFECT_LEFT_ENABLED", "CLICK_EFFECT_RIGHT_ENABLED", "CLICK_EFFECT_STYLE", "CLICK_EFFECT_STRENGTH", "CLICK_EFFECT_RADIUS", "CLICK_EFFECT_LIFETIME", "CLICK_EFFECT_SPARK_AMOUNT", "CLICK_EFFECT_COLOR_MODE", "CLICK_EFFECT_CUSTOM_COLOR", "CLICK_EFFECT_SINGLE_PRESET", "CLICK_EFFECT_NEON_PRESET",
]


def theme_slot_display_values():
    return [str(i) for i in range(1, MAX_CUSTOM_THEMES + 1)]


def theme_slot_key(value):
    text_value = str(value).strip()
    if text_value.lower().startswith("theme "):
        suffix = text_value.split(" ", 1)[1].strip()
        if suffix.isdigit():
            return f"Theme {int(suffix)}"
        return text_value
    if text_value.isdigit():
        return f"Theme {int(text_value)}"
    return text_value


def theme_slot_display_from_key(key):
    text_value = str(key).strip()
    if text_value.lower().startswith("theme "):
        suffix = text_value.split(" ", 1)[1].strip()
        if suffix.isdigit():
            return str(int(suffix))
    return text_value


def capture_current_theme(display_name=None):
    theme = capture_current_config(display_name=display_name or CURRENT_PRESET_NAME, danger_level="Theme")
    theme["type"] = "cursor_swarm_full_theme"
    theme["theme_version"] = APP_VERSION
    for global_name in THEME_EXTRA_GLOBAL_KEYS:
        try:
            value = globals().get(global_name)
            if isinstance(value, (str, int, float, bool)) or value is None:
                theme[global_name.lower()] = value
        except Exception:
            pass
    return theme


def default_custom_themes():
    themes = {}
    for i in range(1, MAX_CUSTOM_THEMES + 1):
        key = f"Theme {i}"
        base = capture_current_theme(display_name=key)
        base["display_name"] = key
        themes[key] = base
    return themes


def load_custom_themes():
    if not THEME_FILE.exists():
        themes = default_custom_themes()
        save_custom_themes(themes)
        return themes
    try:
        data = json.loads(THEME_FILE.read_text(encoding="utf-8"))
    except Exception:
        data = {}
    themes = default_custom_themes()
    if isinstance(data, dict):
        raw_themes = data.get("custom_themes", data)
        if isinstance(raw_themes, dict):
            for key, cfg in raw_themes.items():
                if key in themes and isinstance(cfg, dict):
                    merged = dict(themes[key])
                    merged.update(cfg)
                    merged["display_name"] = str(merged.get("display_name", key))
                    themes[key] = merged
    return themes


def save_custom_themes(themes=None):
    themes = themes if themes is not None else custom_themes
    payload = {
        "version": APP_VERSION,
        "max_custom_themes": MAX_CUSTOM_THEMES,
        "custom_themes": themes,
    }
    write_json_file_safely(THEME_FILE, payload)


def theme_preview_text(theme):
    if not isinstance(theme, dict):
        return "No theme selected."
    movement_flags = []
    for label, key in (
        ("Trail", "movement_motion_trail_enabled"),
        ("Glow", "movement_speed_glow_enabled"),
        ("Streak", "movement_motion_streak_enabled"),
        ("Sparks", "movement_spark_particles_enabled"),
        ("Ripple", "movement_ripple_burst_enabled"),
        ("Comet", "movement_comet_tail_enabled"),
        ("Lines", "movement_speed_lines_enabled"),
        ("Orbit", "movement_magnetic_orbit_enabled"),
        ("Click", "click_effects_enabled"),
    ):
        if theme.get(key, False):
            movement_flags.append(label)
    movement_text = ", ".join(movement_flags) if movement_flags else "Off"
    return (
        f"Theme: {theme.get('display_name', 'Unnamed')}\n"
        f"Shape: {theme.get('cursor_shape_mode', 'Captured System Cursor')} | Tint: {theme.get('cursor_tint_enabled', False)} | Style: {theme.get('cursor_tint_style', 'Single Colour')} | Outline: {theme.get('cursor_tint_black_outline', False)}\n"
        f"Idle: {theme.get('idle_effect_style', 'Disabled')} | Movement: {movement_text}\n"
        f"Performance: {theme.get('performance_mode', PERFORMANCE_MODE)} @ {theme.get('performance_target_fps', PERFORMANCE_TARGET_FPS)} FPS\n"
        f"Custom cursor image: {theme.get('custom_cursor_image_path', '') or 'None'}"
    )


def apply_theme_globals(config):
    for global_name in THEME_EXTRA_GLOBAL_KEYS:
        key = global_name.lower()
        if key not in config:
            continue
        current_value = globals().get(global_name)
        raw_value = config.get(key)
        try:
            if isinstance(current_value, bool):
                globals()[global_name] = bool(raw_value)
            elif isinstance(current_value, int) and not isinstance(current_value, bool):
                globals()[global_name] = int(raw_value)
            elif isinstance(current_value, float):
                globals()[global_name] = float(raw_value)
            elif isinstance(current_value, str):
                globals()[global_name] = str(raw_value)
            else:
                globals()[global_name] = raw_value
        except Exception:
            pass


def apply_full_cursor_theme_config(config, source_name=None):
    if not isinstance(config, dict):
        safe_messagebox_showerror("Theme Error", "Selected theme is invalid.")
        return False
    apply_preset_config(dict(config), source_name=source_name or config.get("display_name", "Cursor Theme"))
    apply_theme_globals(config)
    invalidate_cursor_image_cache()
    clear_motion_trail()
    clear_spark_particles()
    clear_ripple_bursts()
    if "clear_click_effects" in globals():
        clear_click_effects()
    if "set_cursor_lab_vars_from_globals" in globals():
        set_cursor_lab_vars_from_globals()
    if "set_movement_vars_from_globals" in globals():
        set_movement_vars_from_globals()
    if "refresh_movement_summary" in globals():
        refresh_movement_summary("Theme loaded.")
    if "set_performance_vars_from_globals" in globals():
        set_performance_vars_from_globals()
    if "refresh_performance_summary" in globals():
        refresh_performance_summary("Theme loaded.")
    sync_ui_vars()
    update_panel_status()
    return True


def on_theme_slot_changed(_event=None):
    if "theme_slot_var" not in globals():
        return
    key = theme_slot_key(theme_slot_var.get())
    theme = custom_themes.get(key, {})
    theme_name_var.set(theme.get("display_name", key))
    theme_preview_var.set(theme_preview_text(theme))


def load_selected_theme():
    key = theme_slot_key(theme_slot_var.get())
    theme = custom_themes.get(key)
    if not isinstance(theme, dict):
        safe_messagebox_showerror("Theme Error", "Selected theme slot was not found.")
        return
    apply_full_cursor_theme_config(dict(theme), source_name=theme.get("display_name", key))
    theme_name_var.set(theme.get("display_name", key))
    theme_preview_var.set(theme_preview_text(theme))


def save_current_to_theme_slot():
    key = theme_slot_key(theme_slot_var.get())
    if key not in custom_themes:
        safe_messagebox_showerror("Theme Error", "Selected theme slot was not found.")
        return
    name = theme_name_var.get().strip() or key
    theme = capture_current_theme(display_name=name)
    theme["display_name"] = name
    custom_themes[key] = theme
    save_custom_themes()
    theme_preview_var.set(theme_preview_text(theme))
    safe_messagebox_showinfo("Theme Saved", f"Saved current visual setup into {theme_slot_display_from_key(key)}.")


def rename_selected_theme():
    key = theme_slot_key(theme_slot_var.get())
    if key not in custom_themes:
        safe_messagebox_showerror("Theme Error", "Selected theme slot was not found.")
        return
    name = theme_name_var.get().strip() or key
    custom_themes[key]["display_name"] = name
    save_custom_themes()
    theme_preview_var.set(theme_preview_text(custom_themes[key]))


def delete_selected_theme():
    key = theme_slot_key(theme_slot_var.get())
    if key not in custom_themes:
        safe_messagebox_showerror("Theme Error", "Selected theme slot was not found.")
        return
    if not safe_messagebox_askyesno("Reset Theme Slot", f"Reset {theme_slot_display_from_key(key)} to the current safe default theme?"):
        return
    replacement = capture_current_theme(display_name=key)
    replacement["display_name"] = key
    custom_themes[key] = replacement
    theme_name_var.set(key)
    save_custom_themes()
    theme_preview_var.set(theme_preview_text(replacement))


def export_selected_theme():
    key = theme_slot_key(theme_slot_var.get())
    theme = custom_themes.get(key)
    if not isinstance(theme, dict):
        safe_messagebox_showerror("Theme Error", "Selected theme slot was not found.")
        return
    safe_name = str(theme.get("display_name", key)).replace(" ", "_")
    filename = safe_filedialog_asksaveasfilename(
        title="Export Selected Theme",
        defaultextension=".json",
        initialfile=f"cursor_swarm_theme_{theme_slot_display_from_key(key)}_{safe_name}.json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
    )
    if not filename:
        return
    payload = {
        "type": "cursor_swarm_full_theme",
        "version": APP_VERSION,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "slot": theme_slot_display_from_key(key),
        "theme": theme,
    }
    if write_json_file(filename, payload):
        safe_messagebox_showinfo("Export Complete", f"Theme exported to:\n{filename}")


def import_selected_theme():
    key = theme_slot_key(theme_slot_var.get())
    if key not in custom_themes:
        safe_messagebox_showerror("Theme Error", "Selected theme slot was not found.")
        return
    filename = safe_filedialog_askopenfilename(
        title="Import Theme Into Selected Slot",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
    )
    if not filename:
        return
    data = read_json_file(filename)
    if not isinstance(data, dict):
        return
    theme = data.get("theme", data)
    if not isinstance(theme, dict):
        safe_messagebox_showerror("Invalid Theme", "This file does not contain a valid CursorSwarm theme.")
        return
    if not safe_messagebox_askyesno("Import Theme", f"Import this theme into slot {theme_slot_display_from_key(key)}?\n\nThis will overwrite the selected theme slot."):
        return
    theme["display_name"] = str(theme.get("display_name", key))
    custom_themes[key] = theme
    save_custom_themes()
    on_theme_slot_changed()
    safe_messagebox_showinfo("Import Complete", f"Theme imported into slot {theme_slot_display_from_key(key)}.")


def reset_all_custom_themes():
    global custom_themes
    if not safe_messagebox_askyesno("Reset All Themes", "This will reset all custom theme slots to the current safe default theme.\n\nContinue?"):
        return
    custom_themes = default_custom_themes()
    save_custom_themes()
    if "theme_slot_var" in globals():
        theme_slot_var.set("1")
    on_theme_slot_changed()
    safe_messagebox_showinfo("Themes Reset", "All custom theme slots were reset.")


# -----------------------------
# Custom Multi-Colour Preset UI helpers (v13.11.2+)
# -----------------------------
def custom_multi_slot_display_values():
    return [str(i) for i in range(1, MAX_CUSTOM_MULTI_COLOUR_PRESETS + 1)]


def custom_multi_slot_key(value):
    text_value = str(value).strip()
    if text_value.lower().startswith("custom multi "):
        suffix = text_value.rsplit(" ", 1)[-1].strip()
        if suffix.isdigit():
            return f"Custom Multi {int(suffix)}"
        return text_value
    if text_value.isdigit():
        return f"Custom Multi {int(text_value)}"
    return text_value


def custom_multi_slot_display_from_key(key):
    text_value = str(key).strip()
    if text_value.lower().startswith("custom multi "):
        suffix = text_value.rsplit(" ", 1)[-1].strip()
        if suffix.isdigit():
            return str(int(suffix))
    return text_value


def custom_multi_preview_text(config):
    if not isinstance(config, dict):
        return "No custom multi-colour preset selected."
    colors = sanitize_multi_colour_list(config.get("colors"))
    status = "Shown in dropdowns" if config.get("enabled", False) else "Hidden from dropdowns"
    return (
        f"Preset: {config.get('display_name', 'Unnamed')} ({status})\n"
        f"Colours: {colors[0]}  →  {colors[1]}  →  {colors[2]}\n"
        "These colours can be used by Cursor Lab tint, idle glow, movement effects, and click effects."
    )


def refresh_multi_colour_dropdown_values():
    """Refresh every Multi-Colour Neon Preset dropdown after custom preset edits."""
    values = list(NEON_COLOR_PRESETS.keys())
    fallback = values[0] if values else "Cyberpunk Neon"

    combo_names = [
        "cursor_tint_multi_combo",
        "idle_neon_combo",
        "speed_glow_neon_combo",
        "motion_streak_neon_combo",
        "spark_particle_neon_combo",
        "ripple_burst_neon_combo",
        "comet_tail_neon_combo",
        "speed_lines_neon_combo",
        "magnetic_orbit_neon_combo",
        "click_effect_neon_combo",
    ]
    for combo_name in combo_names:
        combo = globals().get(combo_name)
        try:
            if combo is not None:
                combo.configure(values=values)
        except Exception:
            pass

    var_names = [
        "cursor_tint_multi_preset_var",
        "idle_neon_preset_var",
        "speed_glow_neon_preset_var",
        "motion_streak_neon_preset_var",
        "spark_particle_neon_preset_var",
        "ripple_burst_neon_preset_var",
        "comet_tail_neon_preset_var",
        "speed_lines_neon_preset_var",
        "magnetic_orbit_neon_preset_var",
        "click_effect_neon_preset_var",
    ]
    for var_name in var_names:
        var = globals().get(var_name)
        try:
            if var is not None and var.get() not in NEON_COLOR_PRESETS:
                var.set(fallback)
        except Exception:
            pass

    try:
        if "custom_multi_combo" in globals():
            custom_multi_combo.configure(values=custom_multi_slot_display_values())
    except Exception:
        pass


def on_custom_multi_slot_changed(_event=None):
    if "custom_multi_slot_var" not in globals():
        return
    key = custom_multi_slot_key(custom_multi_slot_var.get())
    config = custom_multi_colour_presets.get(key, default_custom_multi_colour_presets().get(key, {}))
    colors = sanitize_multi_colour_list(config.get("colors"))
    custom_multi_name_var.set(str(config.get("display_name", key)))
    custom_multi_color1_var.set(colors[0])
    custom_multi_color2_var.set(colors[1])
    custom_multi_color3_var.set(colors[2])
    custom_multi_enabled_var.set(bool(config.get("enabled", False)))
    custom_multi_preview_var.set(custom_multi_preview_text(config))


def choose_custom_multi_colour(index):
    var_map = {
        1: custom_multi_color1_var,
        2: custom_multi_color2_var,
        3: custom_multi_color3_var,
    }
    color_var = var_map.get(int(index))
    if color_var is None:
        return
    chosen = safe_colorchooser_askcolor(
        parent=control_panel if "control_panel" in globals() else root,
        color=color_var.get(),
        title=f"Choose custom multi-colour {index}",
    )
    if chosen and chosen[1]:
        fixed_hex, _rgb = parse_hex_color(chosen[1])
        color_var.set(sanitize_neon_color(fixed_hex))
        temp_config = {
            "display_name": custom_multi_name_var.get().strip() or custom_multi_slot_key(custom_multi_slot_var.get()),
            "colors": [custom_multi_color1_var.get(), custom_multi_color2_var.get(), custom_multi_color3_var.get()],
            "enabled": bool(custom_multi_enabled_var.get()),
        }
        custom_multi_preview_var.set(custom_multi_preview_text(temp_config))


def save_custom_multi_colour_slot(show_message=True):
    global custom_multi_colour_presets
    key = custom_multi_slot_key(custom_multi_slot_var.get())
    if key not in custom_multi_colour_presets:
        safe_messagebox_showerror("Custom Preset Error", "Selected custom multi-colour slot was not found.")
        return False

    name = custom_multi_name_var.get().strip() or key
    colors = sanitize_multi_colour_list([
        custom_multi_color1_var.get(),
        custom_multi_color2_var.get(),
        custom_multi_color3_var.get(),
    ])
    custom_multi_colour_presets[key] = {
        "display_name": name,
        "colors": colors,
        "enabled": bool(custom_multi_enabled_var.get()),
    }
    save_custom_multi_colour_presets(custom_multi_colour_presets)
    rebuild_neon_color_presets()
    refresh_multi_colour_dropdown_values()
    custom_multi_preview_var.set(custom_multi_preview_text(custom_multi_colour_presets[key]))
    if show_message:
        safe_messagebox_showinfo("Custom Multi-Colour Preset Saved", f"Saved {name} into slot {custom_multi_slot_display_from_key(key)}.")
    return True


def use_custom_multi_colour_in_cursor_lab():
    if not save_custom_multi_colour_slot(show_message=False):
        return
    key = custom_multi_slot_key(custom_multi_slot_var.get())
    config = custom_multi_colour_presets.get(key, {})
    preset_name = str(config.get("display_name", key)).strip() or key
    if preset_name not in NEON_COLOR_PRESETS:
        # If the display name collided and rebuild_neon_color_presets renamed it,
        # choose the matching custom alias.
        preset_name = f"Custom: {preset_name}"
    if preset_name not in NEON_COLOR_PRESETS:
        safe_messagebox_showerror("Preset Hidden", "Enable/show this preset in dropdowns before using it in Cursor Lab.")
        return
    cursor_tint_enabled_var.set(True)
    cursor_tint_style_var.set("Multi-Colour Neon Preset")
    cursor_tint_multi_preset_var.set(preset_name)
    mark_cursor_lab_pending("Custom multi-colour preset selected. Click Apply Cursor Lab to activate it.")
    safe_messagebox_showinfo("Preset Selected", f"Selected {preset_name} for Cursor Lab multi-colour tint.")


def delete_custom_multi_colour_slot():
    global custom_multi_colour_presets
    key = custom_multi_slot_key(custom_multi_slot_var.get())
    if key not in custom_multi_colour_presets:
        safe_messagebox_showerror("Custom Preset Error", "Selected custom multi-colour slot was not found.")
        return
    if not safe_messagebox_askyesno("Hide Custom Multi-Colour Preset", f"Hide/reset slot {custom_multi_slot_display_from_key(key)}?\n\nThe slot will be reset and removed from dropdowns."):
        return
    custom_multi_colour_presets[key] = {
        "display_name": key,
        "colors": sanitize_multi_colour_list(["#22d3ee", "#8b5cf6", "#ff4fd8"]),
        "enabled": False,
    }
    save_custom_multi_colour_presets(custom_multi_colour_presets)
    rebuild_neon_color_presets()
    refresh_multi_colour_dropdown_values()
    on_custom_multi_slot_changed()


def export_custom_multi_colour_presets():
    filename = safe_filedialog_asksaveasfilename(
        title="Export Custom Multi-Colour Presets",
        defaultextension=".json",
        initialfile="cursor_swarm_custom_multi_colour_presets.json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
    )
    if not filename:
        return
    payload = {
        "type": "cursor_swarm_custom_multi_colour_presets",
        "version": APP_VERSION,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "custom_multi_colour_presets": custom_multi_colour_presets,
    }
    if write_json_file(filename, payload):
        safe_messagebox_showinfo("Export Complete", f"Custom multi-colour presets exported to:\n{filename}")


def import_custom_multi_colour_presets():
    global custom_multi_colour_presets
    filename = safe_filedialog_askopenfilename(
        title="Import Custom Multi-Colour Presets",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
    )
    if not filename:
        return
    data = read_json_file(filename)
    if not isinstance(data, dict):
        return
    raw = data.get("custom_multi_colour_presets", data)
    if not isinstance(raw, dict):
        safe_messagebox_showerror("Invalid Preset File", "This file does not contain custom multi-colour presets.")
        return
    if not safe_messagebox_askyesno("Import Custom Multi-Colour Presets", "Import presets into the 10 custom multi-colour slots?\n\nMatching slots will be overwritten."):
        return
    merged = default_custom_multi_colour_presets()
    merged.update(custom_multi_colour_presets)
    for key, cfg in raw.items():
        if key not in merged or not isinstance(cfg, dict):
            continue
        merged[key] = {
            "display_name": str(cfg.get("display_name", key)).strip() or key,
            "colors": sanitize_multi_colour_list(cfg.get("colors")),
            "enabled": bool(cfg.get("enabled", True)),
        }
    custom_multi_colour_presets = merged
    save_custom_multi_colour_presets(custom_multi_colour_presets)
    rebuild_neon_color_presets()
    refresh_multi_colour_dropdown_values()
    on_custom_multi_slot_changed()
    safe_messagebox_showinfo("Import Complete", "Custom multi-colour presets imported.")


def reset_all_custom_multi_colour_presets():
    global custom_multi_colour_presets
    if not safe_messagebox_askyesno("Reset Custom Multi-Colour Presets", "Reset all 10 custom multi-colour preset slots?"):
        return
    custom_multi_colour_presets = default_custom_multi_colour_presets()
    save_custom_multi_colour_presets(custom_multi_colour_presets)
    rebuild_neon_color_presets()
    refresh_multi_colour_dropdown_values()
    if "custom_multi_slot_var" in globals():
        custom_multi_slot_var.set("1")
    on_custom_multi_slot_changed()
    safe_messagebox_showinfo("Custom Multi-Colour Presets Reset", "All custom multi-colour preset slots were reset.")


custom_presets = load_custom_presets()
custom_multi_colour_presets = load_custom_multi_colour_presets()
rebuild_neon_color_presets()
custom_themes = load_custom_themes()

def save_app_settings(update_last_state=True):
    global app_settings

    app_settings["startup_mode"] = startup_mode_var.get() if "startup_mode_var" in globals() else app_settings.get("startup_mode", "Fresh Safe Defaults")
    app_settings["startup_builtin_preset"] = startup_builtin_var.get() if "startup_builtin_var" in globals() else app_settings.get("startup_builtin_preset", "Legendary")
    app_settings["startup_custom_slot"] = startup_custom_slot_var.get() if "startup_custom_slot_var" in globals() else app_settings.get("startup_custom_slot", "1")
    app_settings["startup_theme_slot"] = startup_theme_slot_var.get() if "startup_theme_slot_var" in globals() else app_settings.get("startup_theme_slot", "1")
    app_settings["show_startup_help"] = bool(show_startup_help)
    app_settings["runtime_hud_visible"] = bool(runtime_hud_visible)

    if update_last_state:
        # v13.11: Last Used Settings must save the full visual/theme state,
        # not only the older swarm preset fields. This includes Cursor Lab,
        # ANI animation options, idle effects, movement effects, movement colors,
        # and performance settings.
        if "capture_current_theme" in globals():
            app_settings["last_state"] = capture_current_theme(display_name="Last Used Settings")
            app_settings["last_state"]["danger_level"] = "Last Used"
            app_settings["last_state"]["type"] = "cursor_swarm_last_used_state"
        else:
            app_settings["last_state"] = capture_current_config(
                display_name="Last Used Settings",
                danger_level="Last Used",
            )

    try:
        write_json_file_safely(SETTINGS_FILE, app_settings)
    except Exception as exc:
        print(f"CursorSwarm settings save failed: {exc}")


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
    mode = STARTUP_MODE_ALIASES.get(app_settings.get("startup_mode", "Fresh Safe Defaults"), app_settings.get("startup_mode", "Fresh Safe Defaults"))

    # Startup is intentionally safe-first: the script finishes setup before this runs.
    if mode == "Fresh Safe Defaults":
        startup_safe_mode()

    elif mode == "Last Used Settings":
        last_state = app_settings.get("last_state")
        if isinstance(last_state, dict):
            # v13.11: restore full last-used visual state when available.
            # Old saved last_state payloads still load through the legacy preset path.
            if "apply_full_cursor_theme_config" in globals() and (
                last_state.get("type") in ("cursor_swarm_full_theme", "cursor_swarm_last_used_state")
                or any(key in last_state for key in ("movement_effects_enabled", "idle_effect_enabled", "performance_target_fps"))
            ):
                apply_full_cursor_theme_config(dict(last_state), source_name=last_state.get("display_name", "Last Used Settings"))
            else:
                apply_preset_config(dict(last_state), source_name=last_state.get("display_name", "Last Used Settings"))
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

    elif mode == "Selected Theme":
        key = theme_slot_key(app_settings.get("startup_theme_slot", "1"))
        theme = custom_themes.get(key)
        if isinstance(theme, dict):
            apply_full_cursor_theme_config(dict(theme), source_name=theme.get("display_name", key))
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

        safe_messagebox_showwarning(
            "Startup Safety Fallback",
            "Startup mode failed, so Cursor Swarm opened in Safe Mode.\n\n"
            f"{exc}"
        )

def ui_save_startup_settings():
    app_settings["startup_mode"] = startup_mode_var.get()
    app_settings["startup_builtin_preset"] = startup_builtin_var.get()
    app_settings["startup_custom_slot"] = startup_custom_slot_var.get()
    app_settings["startup_theme_slot"] = startup_theme_slot_var.get()
    app_settings["show_startup_help"] = bool(show_startup_help)
    app_settings["runtime_hud_visible"] = bool(runtime_hud_visible)
    save_app_settings(update_last_state=True)
    safe_messagebox_showinfo("Startup Settings", f"Startup settings saved to:\n{SETTINGS_FILE}")


def ui_apply_startup_now():
    app_settings["startup_mode"] = startup_mode_var.get()
    app_settings["startup_builtin_preset"] = startup_builtin_var.get()
    app_settings["startup_custom_slot"] = startup_custom_slot_var.get()
    app_settings["startup_theme_slot"] = startup_theme_slot_var.get()
    apply_startup_mode()


def generate_emergency_restore_script(show_message=True):
    """Create/update the emergency restore helper in the same folder.

    This is intentionally small and standalone so it can still be run if the
    main app is closed while the Windows cursor is hidden.
    """
    restore_path = RESTORE_SCRIPT_FILE

    script = f"""import ctypes

# Emergency cursor restore script for CursorSwarm {APP_VERSION}.
# Copyright (C) 2026 Palugula Tharun Kumar.
# Run this if CursorSwarm closes while the Windows system cursor is hidden.
# It asks Windows to reload the normal cursor scheme.
# This helper does not collect data and does not connect to the internet.
SPI_SETCURSORS = 0x0057
user32 = ctypes.windll.user32

try:
    user32.SystemParametersInfoW(SPI_SETCURSORS, 0, None, 0)
    print("CursorSwarm emergency restore requested Windows to reload the system cursor scheme.")
except Exception as exc:
    print(f"CursorSwarm emergency restore failed: {{exc}}")

input("Press Enter to close...")
"""

    try:
        restore_path.write_text(script, encoding="utf-8")
    except Exception as exc:
        if show_message:
            safe_messagebox_showerror(
                "Emergency Restore Script",
                f"Could not create emergency restore script:\n{restore_path}\n\n{exc}"
            )
        return None

    if show_message:
        safe_messagebox_showinfo("Emergency Restore Script", f"Created/updated:\n{restore_path}")

    return restore_path


def ensure_emergency_restore_script():
    """Quietly create the restore helper during startup."""
    return generate_emergency_restore_script(show_message=False)


README_TEXT = """CursorSwarm v13.12
===================

CursorSwarm is a Windows cursor effects app for fake cursors, mirror movement, transparent cursor modes, Cursor Lab customization, animated cursor shapes, idle/movement/click effects, presets, and full visual themes.

WHAT IS NEW IN v13.12
---------------------
CursorSwarm v13.12 is a final polish and release-prep checkpoint for the current v13 feature set. It updates version labels, generated documentation, release notes, build references, safety/recovery notes, and Microsoft Store packaging notes while keeping the implemented feature set stable.

CURRENT FEATURE SET
-------------------
Core controls and safety:
- CustomTkinter Control Panel with fixed two-row main tab layout.
- Floating CS button to reopen the Control Panel.
- Ctrl + Alt + C to toggle the Control Panel.
- Ctrl + Alt + Space for Safe Mode / Resume Previous Mode.
- Ctrl + Alt + Q to Quit Safely and restore the Windows cursor.
- Ctrl + Alt + R to toggle the real Windows cursor visible/transparent.
- Emergency restore helper script/exe support.
- Run Stability Check for cursor restore, JSON/settings health, themes, and custom colour preset status.

Cursor Lab:
- Custom image cursor support.
- Manual Cursor Shape Library: Captured System Cursor, Arrow, Hand, I-Beam, Crosshair, resize cursors, Working in Background, Busy / Loading, and Custom Image File.
- Reliable generated fallback I-Beam and Crosshair shapes.
- Real Windows ANI support for Busy / Loading and Working in Background when available.
- Generated fallback spinner support when real ANI files are unavailable.
- Animation source status, real-ANI toggle, and Slow/Normal/Fast animation speed.
- Cursor tint, bright neon tint, single-colour tint, multi-colour neon tint, custom multi-colour presets, black outline, drawn cursor resize, fake cursor size multiplier, and manual hotspot/offset controls.
- Native dialog safety so file/color picker dialogs temporarily restore the normal Windows cursor.

Idle effects:
- Pulse, Glow Ring, Fade, and Wobble idle styles.
- Idle delay and strength controls.
- Neon glow presets and custom neon colours.
- Optional pause of idle effects after long idle.

Movement and click effects:
- Checkbox-stackable movement effects: Motion Trail, Speed Glow, Motion Streak, Spark Particles, Ripple Burst, Comet Tail, Speed Lines, and Magnetic Orbit.
- Per-effect controls and colour modes for supported effects: Cursor Lab Colors, Custom Color, Single Colour Preset, and Multi-Colour Neon Preset.
- Click Effects with left/right click support: Ripple, Burst Ring, Sparks, and Ripple + Sparks.
- Shift + mouse wheel horizontal scrolling in dense Movement/Cursor Lab sections.

Presets, themes, and startup:
- Built-in swarm presets and custom swarm presets.
- Full Cursor Themes with 10 theme slots.
- Save, load, rename, delete/reset, export, import, and reset theme actions.
- Custom Multi-Colour Presets with 10 slots, 3 editable colours, enable/show toggle, import/export/reset, and shared dropdown integration.
- Startup behavior: Fresh Safe Defaults, Last Used Settings, Built-in Preset, Custom Preset, or Selected Theme.
- Full backup support for presets, settings, themes, and custom multi-colour presets.

Performance and stability:
- Target overlay FPS.
- Performance presets.
- Battery Saver Glow Mode.
- Hide Fake Cursors After Long Idle.
- Pause Idle Effects After Long Idle.
- Safer JSON saving/loading with backup handling for broken settings/preset/theme files.

IMPORTANT SAFETY NOTE
---------------------
CursorSwarm can hide the real Windows cursor and intentionally make cursor movement visually confusing. Always keep the recovery controls in mind.

Recovery controls:
Ctrl + Alt + C      = Open / close Control Panel
Floating CS button  = Reopen or focus Control Panel
Ctrl + Alt + Space  = Safe Mode / Resume Previous Mode
Ctrl + Alt + Q      = Quit Safely and restore cursor
Ctrl + Alt + R      = Toggle real system cursor visible / transparent
Hold Shift          = Temporary cursor hint / normal movement in some modes

If your cursor is still hidden after closing the app, run restore_cursor_emergency.exe or restore_cursor_emergency.py.

DEVELOPER BUILD NOTE
--------------------
Required packages:
pip install customtkinter pillow

Example PyInstaller command:
pyinstaller --onefile --noconsole --icon=cursor_swarm.ico --version-file=cursor_swarm_version_info_v13_12.txt --collect-data customtkinter cursor_swarm_v13_12.py

PACKAGING / STORE NOTES
-----------------------
Recommended app description:
CursorSwarm is a local Windows desktop cursor effects app with fake cursor swarms, mirror movement, custom cursor visuals, animated cursor shapes, idle/movement/click effects, presets, themes, startup modes, and safety recovery controls.

MSIX installer arguments:
No special installer arguments are required for the packaged executable unless the packaging tool specifically requires them. CursorSwarm stores writable local settings in a safe app-data folder when installed in a read-only package location.

Microsoft Store runFullTrust explanation:
CursorSwarm is a packaged Win32/Python desktop application. It requires the runFullTrust capability to run its local desktop process, display transparent/topmost cursor overlays, read local mouse state for visual effects, register global hotkeys, use Windows cursor APIs for hide/restore behavior, and provide emergency recovery controls. CursorSwarm does not collect, upload, sell, or share personal data.
"""



PRIVACY_POLICY_TEXT = """CursorSwarm Privacy Policy
==========================

Effective Version: CursorSwarm v13.12
Copyright (C) 2026 Palugula Tharun Kumar.

CursorSwarm does not collect, transmit, sell, rent, or share personal data.

CursorSwarm is designed to run locally on the user's Windows device. It does not require an account, does not send analytics, and does not upload cursor images, settings, themes, presets, movement effect settings, click effect settings, or custom colour presets.

CursorSwarm may store local files on the device, including:
- cursor_settings.json
- cursor_presets.json
- cursor_themes.json
- cursor_color_presets.json
- README.txt
- Release_Notes.txt
- Privacy_Policy.txt
- Terms_and_Safety.txt
- restore_cursor_emergency.py / restore_cursor_emergency.exe

These files are used only for local app settings, recovery, themes, presets, and documentation. If CursorSwarm is installed as an MSIX/package where the install folder is read-only, these files may be stored in the user's local app data folder instead of beside the executable.

Custom images, cursor files, and ANI cursor files are used locally for Cursor Lab. File paths may be stored locally so the app can reload user-selected settings, but CursorSwarm does not upload those files or paths.

CursorSwarm uses local Windows APIs for cursor display, hotkeys, mouse state, overlay drawing, and recovery. These APIs are used to provide the app's visual cursor effects and safety controls.
"""



TERMS_SAFETY_TEXT = """CursorSwarm Terms and Safety Notice
===================================

Effective Version: CursorSwarm v13.12
Copyright (C) 2026 Palugula Tharun Kumar.

CursorSwarm is a Windows cursor effects app made for fun, experimentation, visual customization, and cursor confusion effects.

CursorSwarm can hide the real Windows cursor, draw replacement cursors, display fake cursors, show movement/click/idle effects, and change how the cursor appears visually. Use stronger modes carefully and avoid enabling confusing modes during important work, online exams, presentations, accessibility-critical tasks, or any situation where losing cursor visibility may cause problems.

Important recovery controls:
Ctrl + Alt + C      = Open / close Control Panel
Floating CS button  = Reopen or focus Control Panel
Ctrl + Alt + Space  = Safe Mode / Resume Previous Mode
Ctrl + Alt + Q      = Quit Safely and restore cursor
Ctrl + Alt + R      = Toggle real system cursor visible / transparent
Hold Shift          = Temporary cursor hint / normal movement in some modes

If the cursor remains hidden after closing CursorSwarm, run restore_cursor_emergency.exe or restore_cursor_emergency.py to request Windows to reload the normal cursor scheme.

CursorSwarm is provided as a local desktop utility. The user is responsible for testing settings safely and keeping the emergency restore helper available.
"""



RELEASE_NOTES_TEXT = """CursorSwarm v13.12 Release Notes
================================

Release type: Final polish and release-prep checkpoint

Highlights:
- Updated app version to v13.12.
- Refreshed generated README, release notes, privacy policy, terms/safety notice, and emergency restore helper text.
- Updated build references to v13.12 file/version-info names.
- Added clearer packaging and Microsoft Store runFullTrust notes to the README.
- Cleaned final release wording for the full v13 feature set.
- Fixed a small Advanced tab button layout overlap in the Config / Backup section.
- Expanded Stability Check output to report release document presence.

Major implemented feature areas covered in this release:
- CustomTkinter Control Panel and fixed two-row main tab layout.
- Floating CS button and recovery hotkeys.
- Cursor Lab with custom image cursor, manual cursor shape library, real Windows ANI Busy/Working cursors, generated fallback cursor shapes/spinners, tint, bright neon tint, multi-colour tint, black outline, resize, and hotspot/offset controls.
- Idle effects: Pulse, Glow Ring, Fade, and Wobble.
- Movement effects: Motion Trail, Speed Glow, Motion Streak, Spark Particles, Ripple Burst, Comet Tail, Speed Lines, and Magnetic Orbit.
- Click Effects with left/right click support and ripple/burst/sparks styles.
- Presets & Themes with built-in presets, custom presets, full cursor themes, startup behavior, and full backup support.
- Custom Multi-Colour Presets with 10 slots, import/export/reset, and shared dropdown integration.
- Performance tab with target overlay FPS, Battery Saver Glow Mode, long-idle fake cursor hiding, and long-idle idle effect pause.
- Stability improvements including safer JSON writes/loads, broken JSON backup handling, preset fallback validation, and expanded Run Stability Check.

Notes:
- This patch is intended as a release-prep checkpoint. It does not intentionally add new visual effects.
- v13.11.1 fixed the custom multi-colour helper startup NameError.
- v13.11.2 added safer JSON handling and expanded stability checks.
- v13.11.3 refreshed generated documentation/release text.
- v13.12 polishes release readiness and packaging notes for the current stable v13 feature set.
"""



def generate_readme_file(show_message=True, overwrite=False):
    """Create README.txt beside the app.

    By default this does not overwrite an existing README, so manual edits are kept.
    """
    readme_path = README_FILE

    if readme_path.exists() and not overwrite:
        if show_message:
            safe_messagebox_showinfo(
                "README",
                f"README already exists and was left unchanged:\n{readme_path}"
            )
        return readme_path

    try:
        readme_path.write_text(README_TEXT, encoding="utf-8")
    except Exception as exc:
        if show_message:
            safe_messagebox_showerror(
                "README",
                f"Could not create README file:\n{readme_path}\n\n{exc}"
            )
        return None

    if show_message:
        safe_messagebox_showinfo("README", f"Created README file:\n{readme_path}")

    return readme_path


def document_needs_version_refresh(path, expected_header, old_markers):
    path = Path(path)
    if not path.exists():
        return False

    try:
        sample = path.read_text(encoding="utf-8", errors="ignore")[:800]
    except Exception:
        return False

    # Refresh known app-generated old release files, even when their title line
    # is the same as the new document title (for example the privacy policy).
    if any(marker in sample for marker in old_markers):
        return True

    if sample.startswith(expected_header):
        return False

    return False


def ensure_readme_file():
    """Quietly create or refresh README.txt during startup."""
    refresh_old = document_needs_version_refresh(
        README_FILE,
        "CursorSwarm v13.12",
        [
            "CursorSwarm v10.8",
            "CursorSwarm v10.9",
            "CursorSwarm v11.0",
            "WHAT IS NEW IN v12.9.9",
            "New v13.9 features",
            "cursor_swarm_version_info_v13_0.txt",
            "Manual Cursor Shape Library while keeping",
            "CursorSwarm v13.11.3",
        ],
    )
    return generate_readme_file(show_message=False, overwrite=refresh_old)


def generate_text_document(path, content, title, show_message=True, overwrite=False):
    """Create a text document beside the app without overwriting manual edits by default."""
    path = Path(path)

    if path.exists() and not overwrite:
        if show_message:
            safe_messagebox_showinfo(
                title,
                f"{title} already exists and was left unchanged:\n{path}"
            )
        return path

    try:
        path.write_text(content, encoding="utf-8")
    except Exception as exc:
        if show_message:
            safe_messagebox_showerror(
                title,
                f"Could not create {title}:\n{path}\n\n{exc}"
            )
        return None

    if show_message:
        safe_messagebox_showinfo(title, f"Created/updated:\n{path}")

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
    """Quietly create or refresh release documents during startup."""
    old_markers = [
        "CursorSwarm v10.8",
        "CursorSwarm v10.9",
        "CursorSwarm v11.0",
        "CursorSwarm v12.",
        "CursorSwarm v13.0",
        "CursorSwarm v13.9",
        "CursorSwarm v13.11.2",
        "Effective Version: CursorSwarm v10.9",
        "Effective Version: CursorSwarm v13.11.2",
        "Release type: Manual cursor shape library update",
        "Updated app version to v13.9",
    ]
    generate_privacy_policy_file(
        show_message=False,
        overwrite=document_needs_version_refresh(PRIVACY_POLICY_FILE, "CursorSwarm Privacy Policy", old_markers),
    )
    generate_terms_safety_file(
        show_message=False,
        overwrite=document_needs_version_refresh(TERMS_SAFETY_FILE, "CursorSwarm Terms and Safety Notice", old_markers),
    )
    generate_release_notes_file(
        show_message=False,
        overwrite=document_needs_version_refresh(RELEASE_NOTES_FILE, "CursorSwarm v13.12 Release Notes", old_markers),
    )

# -----------------------------
# Import / Export and config reset
# -----------------------------
def backup_timestamp():
    return time.strftime("%Y%m%d_%H%M%S")


def read_json_file(json_path):
    try:
        return json.loads(Path(json_path).read_text(encoding="utf-8"))
    except Exception as exc:
        safe_messagebox_showerror("JSON Error", f"Could not read JSON file:\n{json_path}\n\n{exc}")
        return None


def write_json_file(json_path, payload):
    try:
        Path(json_path).write_text(json.dumps(payload, indent=4), encoding="utf-8")
        return True
    except Exception as exc:
        safe_messagebox_showerror("Save Error", f"Could not write JSON file:\n{json_path}\n\n{exc}")
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

    settings["startup_mode"] = STARTUP_MODE_ALIASES.get(settings.get("startup_mode"), settings.get("startup_mode"))
    if settings.get("startup_mode") not in STARTUP_MODE_OPTIONS:
        settings["startup_mode"] = "Fresh Safe Defaults"

    settings["startup_builtin_preset"] = str(settings.get("startup_builtin_preset", "Legendary"))
    settings["startup_custom_slot"] = str(settings.get("startup_custom_slot", "1"))
    settings["startup_theme_slot"] = str(settings.get("startup_theme_slot", "1"))
    settings["show_startup_help"] = bool(settings.get("show_startup_help", True))
    settings["runtime_hud_visible"] = bool(settings.get("runtime_hud_visible", False))

    return settings


def export_full_backup():
    # Capture the current state before exporting.
    if "save_app_settings" in globals():
        save_app_settings(update_last_state=True)

    default_name = f"cursor_swarm_full_backup_{backup_timestamp()}.json"
    filename = safe_filedialog_asksaveasfilename(
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
        "custom_themes": custom_themes,
        "custom_multi_colour_presets": custom_multi_colour_presets,
    }

    if write_json_file(filename, payload):
        safe_messagebox_showinfo("Export Complete", f"Full backup exported to:\n{filename}")


def import_full_backup():
    global app_settings, custom_presets, custom_themes, custom_multi_colour_presets, runtime_hud_visible, show_startup_help

    filename = safe_filedialog_askopenfilename(
        title="Import Cursor Swarm Backup",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
    )

    if not filename:
        return

    data = read_json_file(filename)
    if not isinstance(data, dict):
        return

    raw_presets = data.get("custom_presets")
    raw_themes = data.get("custom_themes")
    raw_multi_colours = data.get("custom_multi_colour_presets")
    raw_settings = data.get("app_settings")

    if not isinstance(raw_presets, dict) and not isinstance(raw_themes, dict) and not isinstance(raw_multi_colours, dict) and not isinstance(raw_settings, dict):
        safe_messagebox_showerror(
            "Invalid Backup",
            "This file does not look like a Cursor Swarm full backup."
        )
        return

    if not safe_messagebox_askyesno(
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

    if THEME_FILE.exists():
        THEME_FILE.with_name(f"cursor_themes_before_import_{backup_timestamp()}.json").write_text(
            THEME_FILE.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    if COLOR_PRESET_FILE.exists():
        COLOR_PRESET_FILE.with_name(f"cursor_color_presets_before_import_{backup_timestamp()}.json").write_text(
            COLOR_PRESET_FILE.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    if isinstance(raw_presets, dict):
        custom_presets = normalize_imported_presets(raw_presets)
        save_custom_presets(custom_presets)

    if isinstance(raw_themes, dict):
        merged_themes = default_custom_themes()
        for key, cfg in raw_themes.items():
            if key in merged_themes and isinstance(cfg, dict):
                merged = dict(merged_themes[key])
                merged.update(cfg)
                merged["display_name"] = str(merged.get("display_name", key))
                merged_themes[key] = merged
        custom_themes = merged_themes
        save_custom_themes(custom_themes)

    if isinstance(raw_multi_colours, dict):
        merged_multi = default_custom_multi_colour_presets()
        for key, cfg in raw_multi_colours.items():
            if key in merged_multi and isinstance(cfg, dict):
                merged = dict(merged_multi[key])
                merged.update(cfg)
                merged["display_name"] = str(merged.get("display_name", key)).strip() or key
                merged["colors"] = sanitize_multi_colour_list(merged.get("colors"))
                merged["enabled"] = bool(merged.get("enabled", True))
                merged_multi[key] = merged
        custom_multi_colour_presets = merged_multi
        save_custom_multi_colour_presets(custom_multi_colour_presets)
        rebuild_neon_color_presets()

    if isinstance(raw_settings, dict):
        app_settings = normalize_imported_app_settings(raw_settings)
        runtime_hud_visible = bool(app_settings.get("runtime_hud_visible", False))
        show_startup_help = bool(app_settings.get("show_startup_help", True))
        try:
            write_json_file_safely(SETTINGS_FILE, app_settings)
        except Exception as exc:
            print(f"CursorSwarm settings save failed: {exc}")

    if "custom_preset_slot_var" in globals():
        custom_preset_slot_var.set("1")
    if "theme_slot_var" in globals():
        theme_slot_var.set("1")

    sync_ui_vars()
    safe_messagebox_showinfo("Import Complete", "Backup imported successfully.")


def export_selected_custom_preset():
    key = preset_slot_key(custom_preset_slot_var.get())

    if key not in custom_presets:
        safe_messagebox_showerror("Preset Error", "Selected custom preset slot was not found.")
        return

    preset_name = str(custom_presets[key].get("display_name", key)).replace(" ", "_")
    default_name = f"cursor_swarm_preset_{preset_slot_display_from_key(key)}_{preset_name}.json"

    filename = safe_filedialog_asksaveasfilename(
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
        safe_messagebox_showinfo("Export Complete", f"Preset exported to:\n{filename}")


def import_selected_custom_preset():
    key = preset_slot_key(custom_preset_slot_var.get())

    if key not in custom_presets:
        safe_messagebox_showerror("Preset Error", "Selected custom preset slot was not found.")
        return

    filename = safe_filedialog_askopenfilename(
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
        safe_messagebox_showerror("Invalid Preset", "This file does not contain a valid preset.")
        return

    if not safe_messagebox_askyesno(
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
    safe_messagebox_showinfo("Import Complete", f"Preset imported into slot {preset_slot_display_from_key(key)}.")


def reset_app_settings_to_default():
    global app_settings, runtime_hud_visible, show_startup_help

    if not safe_messagebox_askyesno(
        "Reset App Settings",
        "Reset startup settings, HUD visibility, and app-level settings to defaults?\n\n"
        "Custom presets will not be deleted."
    ):
        return

    app_settings = dict(DEFAULT_APP_SETTINGS)
    runtime_hud_visible = bool(app_settings.get("runtime_hud_visible", False))
    show_startup_help = bool(app_settings.get("show_startup_help", True))
    try:
        write_json_file_safely(SETTINGS_FILE, app_settings)
    except Exception as exc:
        print(f"CursorSwarm settings save failed: {exc}")
    sync_ui_vars()
    safe_messagebox_showinfo("Settings Reset", "App settings were reset to defaults.")


def reset_all_custom_presets():
    global custom_presets

    if not safe_messagebox_askyesno(
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
    safe_messagebox_showinfo("Presets Reset", "All custom preset slots were reset.")


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
        startup_mode_var.set(app_settings.get("startup_mode", "Fresh Safe Defaults"))
    if "startup_builtin_var" in globals():
        startup_builtin_var.set(app_settings.get("startup_builtin_preset", "Legendary"))
    if "startup_custom_slot_var" in globals():
        startup_custom_slot_var.set(str(app_settings.get("startup_custom_slot", "1")))
    if "startup_theme_slot_var" in globals():
        startup_theme_slot_var.set(str(app_settings.get("startup_theme_slot", "1")))
    if "set_swarm_count_vars_from_globals" in globals():
        set_swarm_count_vars_from_globals()
    if "set_cursor_polish_vars_from_globals" in globals():
        set_cursor_polish_vars_from_globals()
    if "set_cursor_lab_vars_from_globals" in globals():
        set_cursor_lab_vars_from_globals()
    update_panel_status()
    if "update_panic_button_labels" in globals():
        update_panic_button_labels()
    if "selected_builtin_preview_var" in globals():
        reset_builtin_preview()
    if "custom_preset_preview_var" in globals():
        on_custom_slot_changed()
    if "theme_preview_var" in globals():
        on_theme_slot_changed()
    if "refresh_swarm_summary" in globals():
        refresh_swarm_summary()


def update_panel_status():
    transparent_text = "TRANSPARENT" if transparent_active else "VISIBLE"
    mirror_text = "ON" if MIRROR_ENABLED else "OFF"
    swarm_text = "PAUSED" if swarm_paused else "RUNNING"
    real_text = "VISIBLE" if show_drawn_real_cursor else "HIDDEN"
    fake_text = "VISIBLE" if show_fake_cursors else "HIDDEN"
    nightmare_text = nightmare_mode if nightmare_mode != "Disabled" else "OFF"

    lab_text = "CUSTOM" if CUSTOM_CURSOR_ENABLED else "SYSTEM"
    tint_text = "TINT" if CURSOR_TINT_ENABLED else "NO TINT"

    panel_status_var.set(
        f"Preset: {CURRENT_PRESET_NAME} | Cursor: {transparent_text} | "
        f"Mirror: {mirror_text} | Swarm: {swarm_text} | "
        f"RealDrawn: {real_text} | Fake: {fake_text} | Nightmare: {nightmare_text} | "
        f"Cursor Lab: {lab_text}, {tint_text}, Fake {FAKE_CURSOR_SCALE_MULTIPLIER:.2f}x"
    )



def make_section(parent, title):
    """Create a modern CustomTkinter card section for v12.2."""
    outer = ctk.CTkFrame(
        parent,
        corner_radius=14,
        border_width=1,
        border_color="#334155",
        fg_color="#111827",
    )
    outer.pack(fill="x", padx=10, pady=8)
    outer.grid_columnconfigure(0, weight=1)

    header = ctk.CTkLabel(
        outer,
        text=title,
        font=("Segoe UI", 14, "bold"),
        text_color="#f8fafc",
        anchor="w",
    )
    header.grid(row=0, column=0, sticky="ew", padx=14, pady=(10, 4))

    body = ctk.CTkFrame(outer, fg_color="transparent")
    body.grid(row=1, column=0, sticky="ew", padx=10, pady=(2, 12))

    for column in range(8):
        body.grid_columnconfigure(column, weight=0)

    return body


def make_hscroll_section(parent, title):
    """Create a card section with a horizontal scrollbar for dense Cursor Lab rows."""
    outer = ctk.CTkFrame(
        parent,
        corner_radius=14,
        border_width=1,
        border_color="#334155",
        fg_color="#111827",
    )
    outer.pack(fill="x", padx=10, pady=8)
    outer.grid_columnconfigure(0, weight=1)

    header = ctk.CTkLabel(
        outer,
        text=title,
        font=("Segoe UI", 14, "bold"),
        text_color="#f8fafc",
        anchor="w",
    )
    header.grid(row=0, column=0, sticky="ew", padx=14, pady=(10, 4))

    scroll_area = ctk.CTkFrame(outer, fg_color="transparent")
    scroll_area.grid(row=1, column=0, sticky="ew", padx=10, pady=(2, 12))
    scroll_area.grid_columnconfigure(0, weight=1)

    # Use a plain Tk canvas here because CustomTkinter's scrollable frame is
    # vertical-first. This gives Cursor Lab sections a real horizontal scrollbar
    # so wide rows remain reachable when the Control Panel is narrow.
    h_canvas = tk.Canvas(
        scroll_area,
        bg="#111827",
        highlightthickness=0,
        bd=0,
        height=80,
    )
    h_scroll = ttk.Scrollbar(scroll_area, orient="horizontal", command=h_canvas.xview)
    h_canvas.configure(xscrollcommand=h_scroll.set)
    h_canvas.grid(row=0, column=0, sticky="ew")
    h_scroll.grid(row=1, column=0, sticky="ew", pady=(2, 0))

    body = ctk.CTkFrame(h_canvas, fg_color="transparent")
    body_window = h_canvas.create_window((0, 0), window=body, anchor="nw")

    def update_hscroll_region(_event=None):
        try:
            h_canvas.configure(scrollregion=h_canvas.bbox("all"))
            required_height = max(42, body.winfo_reqheight() + 6)
            h_canvas.configure(height=required_height)
        except Exception:
            pass

    def update_body_width(event):
        try:
            required_width = body.winfo_reqwidth()
            h_canvas.itemconfigure(body_window, width=max(event.width, required_width))
            update_hscroll_region()
        except Exception:
            pass

    def shift_mousewheel_horizontal(event):
        try:
            if not (event.state & 0x0001):
                return None
            if getattr(event, "delta", 0):
                h_canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
            else:
                direction = -1 if getattr(event, "num", None) == 4 else 1
                h_canvas.xview_scroll(direction, "units")
            return "break"
        except Exception:
            return None

    body.bind("<Configure>", update_hscroll_region)
    h_canvas.bind("<Configure>", update_body_width)
    h_canvas.bind("<Shift-MouseWheel>", shift_mousewheel_horizontal)
    body.bind("<Shift-MouseWheel>", shift_mousewheel_horizontal)
    h_canvas.bind("<Shift-Button-4>", shift_mousewheel_horizontal)
    h_canvas.bind("<Shift-Button-5>", shift_mousewheel_horizontal)
    body.bind("<Shift-Button-4>", shift_mousewheel_horizontal)
    body.bind("<Shift-Button-5>", shift_mousewheel_horizontal)

    for column in range(12):
        body.grid_columnconfigure(column, weight=0)

    return body


def ui_label(parent, text=None, textvariable=None, *, size=13, weight="normal", wraplength=None):
    kwargs = {
        "font": ("Segoe UI", size, weight),
        "text_color": "#e5e7eb",
        "anchor": "w",
        "justify": "left",
    }
    if wraplength is not None:
        kwargs["wraplength"] = wraplength
    if textvariable is not None:
        kwargs["textvariable"] = textvariable
        kwargs["text"] = ""
    else:
        kwargs["text"] = text or ""
    return ctk.CTkLabel(parent, **kwargs)


def ui_button(parent, text, command=None, *, danger=False, secondary=False, width=150):
    fg = "#dc2626" if danger else ("#334155" if secondary else "#2563eb")
    hover = "#b91c1c" if danger else ("#475569" if secondary else "#1d4ed8")
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width,
        height=34,
        corner_radius=10,
        fg_color=fg,
        hover_color=hover,
        text_color="#ffffff",
        font=("Segoe UI", 13, "bold"),
    )


def ui_checkbox(parent, text, variable, command=None):
    return ctk.CTkCheckBox(
        parent,
        text=text,
        variable=variable,
        command=command,
        corner_radius=6,
        border_width=2,
        fg_color="#2563eb",
        hover_color="#1d4ed8",
        text_color="#e5e7eb",
        font=("Segoe UI", 13),
    )


def ui_entry(parent, variable, width=220):
    return ctk.CTkEntry(
        parent,
        textvariable=variable,
        width=width,
        height=32,
        corner_radius=9,
        fg_color="#0f172a",
        border_color="#334155",
        text_color="#f8fafc",
        font=("Segoe UI", 13),
    )


def ui_combo(parent, variable, values, width=180, command=None):
    return ctk.CTkComboBox(
        parent,
        variable=variable,
        values=list(values),
        width=width,
        height=32,
        corner_radius=9,
        state="readonly",
        command=command,
        fg_color="#0f172a",
        border_color="#334155",
        button_color="#2563eb",
        button_hover_color="#1d4ed8",
        dropdown_fg_color="#0f172a",
        dropdown_hover_color="#1e293b",
        dropdown_text_color="#f8fafc",
        text_color="#f8fafc",
        font=("Segoe UI", 13),
        dropdown_font=("Segoe UI", 13),
    )


def ui_slider(parent, variable, from_, to, command=None, width=240):
    return ctk.CTkSlider(
        parent,
        variable=variable,
        from_=from_,
        to=to,
        command=command,
        width=width,
        progress_color="#2563eb",
        button_color="#60a5fa",
        button_hover_color="#93c5fd",
        fg_color="#334155",
    )


def ui_spinbox(parent, variable, from_, to, *, increment=1, width=8):
    # CustomTkinter does not include a native spinbox, so this small classic
    # Spinbox is dark-styled and embedded inside the v12.1 CTk cards.
    return tk.Spinbox(
        parent,
        from_=from_,
        to=to,
        increment=increment,
        textvariable=variable,
        width=width,
        bg="#0f172a",
        fg="#f8fafc",
        insertbackground="#f8fafc",
        buttonbackground="#334155",
        relief="flat",
        highlightthickness=1,
        highlightbackground="#334155",
        highlightcolor="#60a5fa",
        font=("Segoe UI", 11),
    )


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

control_panel = ctk.CTkToplevel(root)
control_panel.title("Cursor Swarm v12.2 Control Panel")
control_panel.geometry("860x640+120+80")
control_panel.minsize(660, 480)
control_panel.attributes("-topmost", True)
control_panel.configure(fg_color="#020617")
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
startup_mode_var = tk.StringVar(value=app_settings.get("startup_mode", "Fresh Safe Defaults"))
startup_builtin_var = tk.StringVar(value=app_settings.get("startup_builtin_preset", "Legendary"))
startup_custom_slot_var = tk.StringVar(value=str(app_settings.get("startup_custom_slot", "1")))
startup_theme_slot_var = tk.StringVar(value=str(app_settings.get("startup_theme_slot", "1")))
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
theme_slot_var = tk.StringVar(value="1")
theme_name_var = tk.StringVar(value=custom_themes["Theme 1"].get("display_name", "Theme 1"))
theme_preview_var = tk.StringVar(value=theme_preview_text(custom_themes["Theme 1"]))
custom_multi_slot_var = tk.StringVar(value="1")
custom_multi_name_var = tk.StringVar(value=custom_multi_colour_presets["Custom Multi 1"].get("display_name", "Custom Multi 1"))
custom_multi_color1_var = tk.StringVar(value=sanitize_multi_colour_list(custom_multi_colour_presets["Custom Multi 1"].get("colors"))[0])
custom_multi_color2_var = tk.StringVar(value=sanitize_multi_colour_list(custom_multi_colour_presets["Custom Multi 1"].get("colors"))[1])
custom_multi_color3_var = tk.StringVar(value=sanitize_multi_colour_list(custom_multi_colour_presets["Custom Multi 1"].get("colors"))[2])
custom_multi_enabled_var = tk.BooleanVar(value=bool(custom_multi_colour_presets["Custom Multi 1"].get("enabled", False)))
custom_multi_preview_var = tk.StringVar(value=custom_multi_preview_text(custom_multi_colour_presets["Custom Multi 1"]))
fake_cursor_scale_multiplier_var = tk.DoubleVar(value=FAKE_CURSOR_SCALE_MULTIPLIER)
fake_cursor_scale_multiplier_label_var = tk.StringVar(value=f"{FAKE_CURSOR_SCALE_MULTIPLIER:.2f}x")
cursor_tint_enabled_var = tk.BooleanVar(value=CURSOR_TINT_ENABLED)
cursor_tint_style_var = tk.StringVar(value=CURSOR_TINT_STYLE)
cursor_tint_multi_preset_var = tk.StringVar(value=CURSOR_TINT_MULTI_PRESET)
cursor_tint_color_var = tk.StringVar(value=CURSOR_TINT_COLOR)
cursor_tint_strength_var = tk.DoubleVar(value=CURSOR_TINT_STRENGTH)
cursor_tint_strength_label_var = tk.StringVar(value=f"{CURSOR_TINT_STRENGTH:.2f}")
cursor_tint_bright_neon_var = tk.BooleanVar(value=CURSOR_TINT_BRIGHT_NEON)
cursor_tint_neon_brightness_var = tk.DoubleVar(value=CURSOR_TINT_NEON_BRIGHTNESS)
cursor_tint_neon_brightness_label_var = tk.StringVar(value=f"{CURSOR_TINT_NEON_BRIGHTNESS:.2f}x")
cursor_tint_black_outline_var = tk.BooleanVar(value=CURSOR_TINT_BLACK_OUTLINE)
cursor_tint_outline_thickness_var = tk.IntVar(value=CURSOR_TINT_OUTLINE_THICKNESS)
cursor_tint_outline_thickness_label_var = tk.StringVar(value=f"{CURSOR_TINT_OUTLINE_THICKNESS}px")
cursor_tint_apply_drawn_var = tk.BooleanVar(value=CURSOR_TINT_APPLY_DRAWN)
cursor_tint_apply_fake_var = tk.BooleanVar(value=CURSOR_TINT_APPLY_FAKE)
custom_cursor_enabled_var = tk.BooleanVar(value=CUSTOM_CURSOR_ENABLED)
custom_cursor_path_var = tk.StringVar(value=CUSTOM_CURSOR_IMAGE_PATH)
cursor_shape_mode_var = tk.StringVar(value=CURSOR_SHAPE_MODE)
cursor_use_real_ani_var = tk.BooleanVar(value=CURSOR_USE_REAL_WINDOWS_ANI)
cursor_animation_speed_mode_var = tk.StringVar(value=CURSOR_ANIMATION_SPEED_MODE)
cursor_animation_source_status_var = tk.StringVar(value=cursor_animation_source_status_text())
custom_cursor_hotspot_mode_var = tk.StringVar(value=CUSTOM_CURSOR_HOTSPOT_MODE)
idle_effect_enabled_var = tk.BooleanVar(value=IDLE_EFFECT_ENABLED)
idle_effect_style_var = tk.StringVar(value=IDLE_EFFECT_STYLE)
idle_effect_delay_var = tk.DoubleVar(value=IDLE_EFFECT_DELAY)
idle_effect_delay_label_var = tk.StringVar(value=f"{IDLE_EFFECT_DELAY:.2f}s")
idle_effect_strength_var = tk.DoubleVar(value=IDLE_EFFECT_STRENGTH)
idle_effect_strength_label_var = tk.StringVar(value=f"{IDLE_EFFECT_STRENGTH:.2f}")
idle_neon_enabled_var = tk.BooleanVar(value=IDLE_EFFECT_NEON_ENABLED)
idle_neon_preset_var = tk.StringVar(value=IDLE_EFFECT_NEON_PRESET)
idle_neon_color_var = tk.StringVar(value=IDLE_EFFECT_NEON_COLOR)
custom_cursor_status_var = tk.StringVar(value=cursor_lab_status_text())
performance_mode_var = tk.StringVar(value=PERFORMANCE_MODE)
performance_fps_var = tk.IntVar(value=PERFORMANCE_TARGET_FPS)
performance_fps_label_var = tk.StringVar(value=f"{PERFORMANCE_TARGET_FPS} FPS")
reduce_glow_quality_var = tk.BooleanVar(value=PERFORMANCE_REDUCE_GLOW_QUALITY)
pause_swarm_long_idle_var = tk.BooleanVar(value=PERFORMANCE_PAUSE_SWARM_ON_LONG_IDLE)
pause_idle_effects_long_idle_var = tk.BooleanVar(value=PERFORMANCE_PAUSE_IDLE_EFFECTS_ON_LONG_IDLE)
long_idle_seconds_var = tk.DoubleVar(value=PERFORMANCE_LONG_IDLE_SECONDS)
long_idle_seconds_label_var = tk.StringVar(value=f"{PERFORMANCE_LONG_IDLE_SECONDS:.0f}s")
performance_summary_var = tk.StringVar(value=performance_summary_text())
movement_effects_enabled_var = tk.BooleanVar(value=MOVEMENT_EFFECTS_ENABLED)
movement_effect_style_var = tk.StringVar(value=MOVEMENT_EFFECT_STYLE)
movement_motion_trail_enabled_var = tk.BooleanVar(value=MOVEMENT_MOTION_TRAIL_ENABLED)
movement_speed_glow_enabled_var = tk.BooleanVar(value=MOVEMENT_SPEED_GLOW_ENABLED)
movement_motion_streak_enabled_var = tk.BooleanVar(value=MOVEMENT_MOTION_STREAK_ENABLED)
movement_spark_particles_enabled_var = tk.BooleanVar(value=MOVEMENT_SPARK_PARTICLES_ENABLED)
movement_ripple_burst_enabled_var = tk.BooleanVar(value=MOVEMENT_RIPPLE_BURST_ENABLED)
movement_comet_tail_enabled_var = tk.BooleanVar(value=MOVEMENT_COMET_TAIL_ENABLED)
movement_speed_lines_enabled_var = tk.BooleanVar(value=MOVEMENT_SPEED_LINES_ENABLED)
movement_magnetic_orbit_enabled_var = tk.BooleanVar(value=MOVEMENT_MAGNETIC_ORBIT_ENABLED)
click_effects_enabled_var = tk.BooleanVar(value=CLICK_EFFECTS_ENABLED)
click_effect_left_enabled_var = tk.BooleanVar(value=CLICK_EFFECT_LEFT_ENABLED)
click_effect_right_enabled_var = tk.BooleanVar(value=CLICK_EFFECT_RIGHT_ENABLED)
click_effect_style_var = tk.StringVar(value=CLICK_EFFECT_STYLE)
motion_trail_color_mode_var = tk.StringVar(value=MOTION_TRAIL_COLOR_MODE)
motion_trail_custom_color_var = tk.StringVar(value=MOTION_TRAIL_CUSTOM_COLOR)
motion_trail_single_preset_var = tk.StringVar(value=MOTION_TRAIL_SINGLE_PRESET)
motion_trail_neon_preset_var = tk.StringVar(value=MOTION_TRAIL_NEON_PRESET)
speed_glow_color_mode_var = tk.StringVar(value=SPEED_GLOW_COLOR_MODE)
speed_glow_custom_color_var = tk.StringVar(value=SPEED_GLOW_CUSTOM_COLOR)
speed_glow_single_preset_var = tk.StringVar(value=SPEED_GLOW_SINGLE_PRESET)
speed_glow_neon_preset_var = tk.StringVar(value=SPEED_GLOW_NEON_PRESET)
motion_streak_color_mode_var = tk.StringVar(value=MOTION_STREAK_COLOR_MODE)
motion_streak_custom_color_var = tk.StringVar(value=MOTION_STREAK_CUSTOM_COLOR)
motion_streak_single_preset_var = tk.StringVar(value=MOTION_STREAK_SINGLE_PRESET)
motion_streak_neon_preset_var = tk.StringVar(value=MOTION_STREAK_NEON_PRESET)
spark_particle_color_mode_var = tk.StringVar(value=SPARK_PARTICLE_COLOR_MODE)
spark_particle_custom_color_var = tk.StringVar(value=SPARK_PARTICLE_CUSTOM_COLOR)
spark_particle_single_preset_var = tk.StringVar(value=SPARK_PARTICLE_SINGLE_PRESET)
spark_particle_neon_preset_var = tk.StringVar(value=SPARK_PARTICLE_NEON_PRESET)
ripple_burst_color_mode_var = tk.StringVar(value=RIPPLE_BURST_COLOR_MODE)
ripple_burst_custom_color_var = tk.StringVar(value=RIPPLE_BURST_CUSTOM_COLOR)
ripple_burst_single_preset_var = tk.StringVar(value=RIPPLE_BURST_SINGLE_PRESET)
ripple_burst_neon_preset_var = tk.StringVar(value=RIPPLE_BURST_NEON_PRESET)
comet_tail_color_mode_var = tk.StringVar(value=COMET_TAIL_COLOR_MODE)
comet_tail_custom_color_var = tk.StringVar(value=COMET_TAIL_CUSTOM_COLOR)
comet_tail_single_preset_var = tk.StringVar(value=COMET_TAIL_SINGLE_PRESET)
comet_tail_neon_preset_var = tk.StringVar(value=COMET_TAIL_NEON_PRESET)
speed_lines_color_mode_var = tk.StringVar(value=SPEED_LINES_COLOR_MODE)
speed_lines_custom_color_var = tk.StringVar(value=SPEED_LINES_CUSTOM_COLOR)
speed_lines_single_preset_var = tk.StringVar(value=SPEED_LINES_SINGLE_PRESET)
speed_lines_neon_preset_var = tk.StringVar(value=SPEED_LINES_NEON_PRESET)
magnetic_orbit_color_mode_var = tk.StringVar(value=MAGNETIC_ORBIT_COLOR_MODE)
magnetic_orbit_custom_color_var = tk.StringVar(value=MAGNETIC_ORBIT_CUSTOM_COLOR)
magnetic_orbit_single_preset_var = tk.StringVar(value=MAGNETIC_ORBIT_SINGLE_PRESET)
magnetic_orbit_neon_preset_var = tk.StringVar(value=MAGNETIC_ORBIT_NEON_PRESET)
click_effect_color_mode_var = tk.StringVar(value=CLICK_EFFECT_COLOR_MODE)
click_effect_custom_color_var = tk.StringVar(value=CLICK_EFFECT_CUSTOM_COLOR)
click_effect_single_preset_var = tk.StringVar(value=CLICK_EFFECT_SINGLE_PRESET)
click_effect_neon_preset_var = tk.StringVar(value=CLICK_EFFECT_NEON_PRESET)
motion_trail_length_var = tk.IntVar(value=MOTION_TRAIL_LENGTH)
motion_trail_length_label_var = tk.StringVar(value=f"{MOTION_TRAIL_LENGTH}")
motion_trail_fade_var = tk.DoubleVar(value=MOTION_TRAIL_FADE_STRENGTH)
motion_trail_fade_label_var = tk.StringVar(value=f"{MOTION_TRAIL_FADE_STRENGTH:.2f}")
speed_glow_strength_var = tk.DoubleVar(value=SPEED_GLOW_STRENGTH)
speed_glow_strength_label_var = tk.StringVar(value=f"{SPEED_GLOW_STRENGTH:.2f}")
speed_glow_threshold_var = tk.DoubleVar(value=SPEED_GLOW_THRESHOLD)
speed_glow_threshold_label_var = tk.StringVar(value=f"{int(SPEED_GLOW_THRESHOLD)} px/s")
motion_streak_strength_var = tk.DoubleVar(value=MOTION_STREAK_STRENGTH)
motion_streak_strength_label_var = tk.StringVar(value=f"{MOTION_STREAK_STRENGTH:.2f}")
motion_streak_threshold_var = tk.DoubleVar(value=MOTION_STREAK_THRESHOLD)
motion_streak_threshold_label_var = tk.StringVar(value=f"{int(MOTION_STREAK_THRESHOLD)} px/s")
motion_streak_length_var = tk.IntVar(value=MOTION_STREAK_LENGTH)
motion_streak_length_label_var = tk.StringVar(value=f"{int(MOTION_STREAK_LENGTH)} px")
spark_particle_strength_var = tk.DoubleVar(value=SPARK_PARTICLE_STRENGTH)
spark_particle_strength_label_var = tk.StringVar(value=f"{SPARK_PARTICLE_STRENGTH:.2f}")
spark_particle_threshold_var = tk.DoubleVar(value=SPARK_PARTICLE_THRESHOLD)
spark_particle_threshold_label_var = tk.StringVar(value=f"{int(SPARK_PARTICLE_THRESHOLD)} px/s")
spark_particle_amount_var = tk.IntVar(value=SPARK_PARTICLE_AMOUNT)
spark_particle_amount_label_var = tk.StringVar(value=f"{int(SPARK_PARTICLE_AMOUNT)}")
spark_particle_size_var = tk.IntVar(value=SPARK_PARTICLE_SIZE)
spark_particle_size_label_var = tk.StringVar(value=f"{int(SPARK_PARTICLE_SIZE)} px")
spark_particle_lifetime_var = tk.DoubleVar(value=SPARK_PARTICLE_LIFETIME)
spark_particle_lifetime_label_var = tk.StringVar(value=f"{SPARK_PARTICLE_LIFETIME:.2f}s")
ripple_burst_strength_var = tk.DoubleVar(value=RIPPLE_BURST_STRENGTH)
ripple_burst_strength_label_var = tk.StringVar(value=f"{RIPPLE_BURST_STRENGTH:.2f}")
ripple_burst_threshold_var = tk.DoubleVar(value=RIPPLE_BURST_THRESHOLD)
ripple_burst_threshold_label_var = tk.StringVar(value=f"{int(RIPPLE_BURST_THRESHOLD)} px/s")
ripple_burst_lifetime_var = tk.DoubleVar(value=RIPPLE_BURST_LIFETIME)
ripple_burst_lifetime_label_var = tk.StringVar(value=f"{RIPPLE_BURST_LIFETIME:.2f}s")
ripple_burst_radius_var = tk.IntVar(value=RIPPLE_BURST_RADIUS)
ripple_burst_radius_label_var = tk.StringVar(value=f"{int(RIPPLE_BURST_RADIUS)} px")
comet_tail_strength_var = tk.DoubleVar(value=COMET_TAIL_STRENGTH)
comet_tail_strength_label_var = tk.StringVar(value=f"{COMET_TAIL_STRENGTH:.2f}")
comet_tail_length_var = tk.IntVar(value=COMET_TAIL_LENGTH)
comet_tail_length_label_var = tk.StringVar(value=f"{int(COMET_TAIL_LENGTH)} px")
comet_tail_thickness_var = tk.IntVar(value=COMET_TAIL_THICKNESS)
comet_tail_thickness_label_var = tk.StringVar(value=f"{int(COMET_TAIL_THICKNESS)} px")
speed_lines_strength_var = tk.DoubleVar(value=SPEED_LINES_STRENGTH)
speed_lines_strength_label_var = tk.StringVar(value=f"{SPEED_LINES_STRENGTH:.2f}")
speed_lines_threshold_var = tk.DoubleVar(value=SPEED_LINES_THRESHOLD)
speed_lines_threshold_label_var = tk.StringVar(value=f"{int(SPEED_LINES_THRESHOLD)} px/s")
speed_lines_amount_var = tk.IntVar(value=SPEED_LINES_AMOUNT)
speed_lines_amount_label_var = tk.StringVar(value=f"{int(SPEED_LINES_AMOUNT)}")
speed_lines_length_var = tk.IntVar(value=SPEED_LINES_LENGTH)
speed_lines_length_label_var = tk.StringVar(value=f"{int(SPEED_LINES_LENGTH)} px")
magnetic_orbit_strength_var = tk.DoubleVar(value=MAGNETIC_ORBIT_STRENGTH)
magnetic_orbit_strength_label_var = tk.StringVar(value=f"{MAGNETIC_ORBIT_STRENGTH:.2f}")
magnetic_orbit_threshold_var = tk.DoubleVar(value=MAGNETIC_ORBIT_THRESHOLD)
magnetic_orbit_threshold_label_var = tk.StringVar(value=f"{int(MAGNETIC_ORBIT_THRESHOLD)} px/s")
magnetic_orbit_radius_var = tk.IntVar(value=MAGNETIC_ORBIT_RADIUS)
magnetic_orbit_radius_label_var = tk.StringVar(value=f"{int(MAGNETIC_ORBIT_RADIUS)} px")
magnetic_orbit_dots_var = tk.IntVar(value=MAGNETIC_ORBIT_DOTS)
magnetic_orbit_dots_label_var = tk.StringVar(value=f"{int(MAGNETIC_ORBIT_DOTS)}")
click_effect_strength_var = tk.DoubleVar(value=CLICK_EFFECT_STRENGTH)
click_effect_strength_label_var = tk.StringVar(value=f"{CLICK_EFFECT_STRENGTH:.2f}")
click_effect_radius_var = tk.IntVar(value=CLICK_EFFECT_RADIUS)
click_effect_radius_label_var = tk.StringVar(value=f"{int(CLICK_EFFECT_RADIUS)} px")
click_effect_lifetime_var = tk.DoubleVar(value=CLICK_EFFECT_LIFETIME)
click_effect_lifetime_label_var = tk.StringVar(value=f"{CLICK_EFFECT_LIFETIME:.2f}s")
click_effect_spark_amount_var = tk.IntVar(value=CLICK_EFFECT_SPARK_AMOUNT)
click_effect_spark_amount_label_var = tk.StringVar(value=f"{int(CLICK_EFFECT_SPARK_AMOUNT)}")
movement_summary_var = tk.StringVar(value=movement_summary_text())

# Top bar
top_frame = ctk.CTkFrame(control_panel, fg_color="#0f172a", corner_radius=0)
top_frame.pack(fill="x", padx=0, pady=0)

brand_box = ctk.CTkFrame(top_frame, fg_color="transparent")
brand_box.pack(side="left", fill="x", expand=True, padx=16, pady=12)
ctk.CTkLabel(
    brand_box,
    text="CursorSwarm v13.12",
    font=("Segoe UI", 21, "bold"),
    text_color="#f8fafc",
    anchor="w",
).pack(anchor="w")
ctk.CTkLabel(
    brand_box,
    text="CustomTkinter control panel • Cursor Lab • themes • movement/click effects • animated cursors",
    font=("Segoe UI", 12),
    text_color="#94a3b8",
    anchor="w",
).pack(anchor="w", pady=(2, 0))

ui_button(top_frame, "Hide Panel", hide_control_panel, secondary=True, width=120).pack(side="right", padx=(6, 16), pady=14)
ui_button(top_frame, "Quit Safely", restore_and_quit, danger=True, width=120).pack(side="right", padx=6, pady=14)

status_card = ctk.CTkFrame(control_panel, fg_color="#111827", corner_radius=12, border_width=1, border_color="#1e293b")
status_card.pack(fill="x", padx=14, pady=(12, 4))
status_label = ctk.CTkLabel(
    status_card,
    textvariable=panel_status_var,
    font=("Segoe UI", 12),
    text_color="#cbd5e1",
    anchor="w",
    justify="left",
    wraplength=780,
)
status_label.pack(fill="x", padx=12, pady=10)

main_tab_nav_frame = ctk.CTkFrame(
    control_panel,
    fg_color="#020617",
    corner_radius=12,
    border_width=1,
    border_color="#1e293b",
)
main_tab_nav_frame.pack(fill="x", padx=14, pady=(8, 0))

notebook = ctk.CTkTabview(
    control_panel,
    width=820,
    height=420,
    corner_radius=14,
    fg_color="#020617",
    segmented_button_fg_color="#0f172a",
    segmented_button_selected_color="#2563eb",
    segmented_button_selected_hover_color="#1d4ed8",
    segmented_button_unselected_color="#111827",
    segmented_button_unselected_hover_color="#1e293b",
    text_color="#f8fafc",
)
notebook.pack(fill="both", expand=True, padx=14, pady=(4, 10))


def create_scrollable_tab(book, title):
    book.add(title)
    container = book.tab(title)
    content = ctk.CTkScrollableFrame(
        container,
        fg_color="#020617",
        corner_radius=0,
        scrollbar_button_color="#334155",
        scrollbar_button_hover_color="#475569",
    )
    content.pack(fill="both", expand=True, padx=4, pady=4)
    return content


MAIN_TAB_TITLES = [
    "Dashboard",
    "Cursor",
    "Cursor Lab",
    "Mirror",
    "Swarm",
    "Performance",
    "Movement",
    "Presets & Themes",
    "Safety",
    "Advanced",
]
main_tab_buttons = {}
main_tab_last_layout_cols = None
main_tab_resize_after_id = None


def update_main_tab_nav_selection(selected_title=None):
    if selected_title is None:
        try:
            selected_title = notebook.get()
        except Exception:
            selected_title = "Dashboard"

    for title, button in main_tab_buttons.items():
        try:
            if title == selected_title:
                button.configure(fg_color="#2563eb", hover_color="#1d4ed8", text_color="#ffffff")
            else:
                button.configure(fg_color="#111827", hover_color="#1e293b", text_color="#cbd5e1")
        except Exception:
            pass


def switch_main_tab(title):
    try:
        notebook.set(title)
    except Exception:
        return
    update_main_tab_nav_selection(title)


def rebuild_main_tab_nav(force=False):
    global main_tab_last_layout_cols

    if not main_tab_buttons:
        return

    # v13.11: Always use a simple two-row layout with 5 tabs per row.
    # The adaptive single-row layout could behave oddly on some window sizes,
    # while this fixed layout keeps every tab name readable.
    cols = 5
    if not force and main_tab_last_layout_cols == cols:
        update_main_tab_nav_selection()
        return

    main_tab_last_layout_cols = cols

    for button in main_tab_buttons.values():
        try:
            button.grid_forget()
        except Exception:
            pass

    for col in range(len(MAIN_TAB_TITLES)):
        try:
            main_tab_nav_frame.grid_columnconfigure(col, weight=0)
        except Exception:
            pass

    for index, title in enumerate(MAIN_TAB_TITLES):
        row = index // cols
        col = index % cols
        button = main_tab_buttons[title]
        button.grid(row=row, column=col, sticky="ew", padx=4, pady=4)

    for col in range(cols):
        try:
            main_tab_nav_frame.grid_columnconfigure(col, weight=1, uniform="main_tabs")
        except Exception:
            pass

    update_main_tab_nav_selection()


def schedule_main_tab_nav_rebuild(_event=None):
    global main_tab_resize_after_id
    try:
        if main_tab_resize_after_id is not None:
            control_panel.after_cancel(main_tab_resize_after_id)
    except Exception:
        pass
    try:
        main_tab_resize_after_id = control_panel.after(80, lambda: rebuild_main_tab_nav(force=False))
    except Exception:
        rebuild_main_tab_nav(force=False)


def setup_main_tab_navigation():
    # Hide CTkTabview's built-in segmented button. The custom nav below uses
    # a fixed 2-row layout with 5 tab names per row so names do not get cut off.
    try:
        notebook._segmented_button.grid_forget()
    except Exception:
        pass

    for title in MAIN_TAB_TITLES:
        if title not in main_tab_buttons:
            main_tab_buttons[title] = ctk.CTkButton(
                main_tab_nav_frame,
                text=title,
                command=lambda value=title: switch_main_tab(value),
                height=30,
                corner_radius=10,
                fg_color="#111827",
                hover_color="#1e293b",
                text_color="#cbd5e1",
                font=("Segoe UI", 11, "bold"),
            )

    rebuild_main_tab_nav(force=True)


# Dashboard tab
dashboard_tab = create_scrollable_tab(notebook, "Dashboard")

quick = make_section(dashboard_tab, "Quick Controls")
ui_checkbox(quick, "Transparent System Cursor", transparent_var, ui_toggle_transparent).grid(row=0, column=0, sticky="w", padx=8, pady=5)
ui_checkbox(quick, "Show Fake Cursors", show_fake_var, ui_toggle_fake_cursors).grid(row=0, column=1, sticky="w", padx=8, pady=5)
ui_checkbox(quick, "Show Drawn-Real Cursor", drawn_real_var, ui_toggle_drawn_real).grid(row=1, column=0, sticky="w", padx=8, pady=5)
ui_checkbox(quick, "Mirror Mode", mirror_enabled_var, ui_toggle_mirror).grid(row=1, column=1, sticky="w", padx=8, pady=5)
ui_checkbox(quick, "Pause Swarm", pause_var, ui_toggle_pause).grid(row=2, column=0, sticky="w", padx=8, pady=5)
ui_checkbox(quick, "Runtime HUD", runtime_hud_var, ui_toggle_runtime_hud).grid(row=2, column=1, sticky="w", padx=8, pady=5)
ui_checkbox(quick, "Startup Help Text", startup_help_var, ui_toggle_startup_help).grid(row=3, column=0, sticky="w", padx=8, pady=5)

quick_buttons = make_section(dashboard_tab, "Important Actions")
dashboard_panic_toggle_button = ui_button(quick_buttons, "SAFE MODE / PANIC", panic_resume_toggle, danger=True, width=180)
dashboard_panic_toggle_button.grid(row=0, column=0, padx=6, pady=6)
ui_button(quick_buttons, "Resume Previous", resume_previous_mode, secondary=True).grid(row=1, column=0, padx=6, pady=6)
ui_button(quick_buttons, "Restore Cursor", ui_restore_cursor).grid(row=0, column=1, padx=6, pady=6)
ui_button(quick_buttons, "Disable Mirror", ui_disable_mirror, secondary=True).grid(row=0, column=2, padx=6, pady=6)
ui_button(quick_buttons, "Hide Panel", hide_control_panel, secondary=True).grid(row=0, column=3, padx=6, pady=6)

# Cursor tab
cursor_tab = create_scrollable_tab(notebook, "Cursor")

system_cursor_box = make_section(cursor_tab, "System Cursor")
ui_checkbox(system_cursor_box, "Transparent System Cursor", transparent_var, ui_toggle_transparent).grid(row=0, column=0, sticky="w", padx=8, pady=5)
ui_button(system_cursor_box, "Restore System Cursor", ui_restore_cursor).grid(row=0, column=1, padx=8, pady=5)
ui_button(system_cursor_box, "Make Cursor Transparent", ui_make_transparent, secondary=True, width=185).grid(row=0, column=2, padx=8, pady=5)

drawn_box = make_section(cursor_tab, "Drawn-Real Cursor")
ui_checkbox(drawn_box, "Show Drawn-Real Cursor", drawn_real_var, ui_toggle_drawn_real).grid(row=0, column=0, sticky="w", padx=8, pady=5)

ui_label(drawn_box, "Manual Offset X:").grid(row=1, column=0, sticky="w", padx=8, pady=5)
ui_spinbox(drawn_box, manual_offset_x_var, -200, 200).grid(row=1, column=1, sticky="w", padx=8, pady=5)
ui_label(drawn_box, "Manual Offset Y:").grid(row=2, column=0, sticky="w", padx=8, pady=5)
ui_spinbox(drawn_box, manual_offset_y_var, -200, 200).grid(row=2, column=1, sticky="w", padx=8, pady=5)

ui_label(drawn_box, "Drawn Cursor Scale:").grid(row=3, column=0, sticky="w", padx=8, pady=5)
ui_slider(drawn_box, real_cursor_scale_var, 0.25, 3.0, lambda value: real_cursor_scale_label_var.set(f"{float(value):.2f}x"), width=250).grid(row=3, column=1, sticky="w", padx=8, pady=5)
ui_label(drawn_box, textvariable=real_cursor_scale_label_var).grid(row=3, column=2, sticky="w", padx=8, pady=5)

ui_button(drawn_box, "Apply Cursor Settings", apply_cursor_polish_from_ui, width=180).grid(row=4, column=0, padx=8, pady=7)
ui_button(drawn_box, "Reset Fields", reset_cursor_polish_fields_to_current, secondary=True).grid(row=4, column=1, padx=8, pady=7)

ui_label(drawn_box, f"Detected Hotspot: ({hotspot_x}, {hotspot_y})  |  Hold Shift = temporary hint", wraplength=650).grid(row=5, column=0, columnspan=3, sticky="w", padx=8, pady=5)

nightmare_box = make_section(cursor_tab, "Nightmare Behavior")
ui_label(nightmare_box, "Nightmare Mode:").grid(row=0, column=0, sticky="w", padx=8, pady=5)
nightmare_combo = ui_combo(nightmare_box, nightmare_mode_var, NIGHTMARE_MODE_OPTIONS, width=220)
nightmare_combo.grid(row=0, column=1, sticky="w", padx=8, pady=5)
ui_button(nightmare_box, "Apply Mode", ui_apply_nightmare_mode).grid(row=0, column=2, padx=8, pady=5)
ui_button(nightmare_box, "Disable Nightmare", ui_disable_nightmare_mode, danger=True, width=170).grid(row=0, column=3, padx=8, pady=5)
ui_label(
    nightmare_box,
    "Blind Mode: transparent cursor + no fake cursors + no drawn-real cursor.\n"
    "Fake-only Mode: fake cursors visible, but your drawn-real cursor is hidden.\n"
    "Flicker Hint Mode: fake-only base, with a brief real-cursor hint every few seconds.\n"
    "Hold Shift always temporarily shows the drawn-real cursor. Panic/Safe Mode disables Nightmare.",
    wraplength=720,
).grid(row=1, column=0, columnspan=4, sticky="w", padx=8, pady=5)

# Cursor Lab tab
cursor_lab_tab = create_scrollable_tab(notebook, "Cursor Lab")

lab_source_box = make_hscroll_section(cursor_lab_tab, "Custom Cursor Source")
ui_label(
    lab_source_box,
    "v13.9 Manual Cursor Shape Library: choose a built-in Windows cursor shape or load a custom image. Working/Busy use real Windows ANI when available, with generated fallback animation.",
    wraplength=760,
).grid(row=0, column=0, columnspan=4, sticky="w", padx=8, pady=5)
ui_label(lab_source_box, "Cursor shape:").grid(row=1, column=0, sticky="w", padx=8, pady=5)
ui_combo(lab_source_box, cursor_shape_mode_var, CURSOR_SHAPE_OPTIONS, width=260, command=on_cursor_shape_mode_change).grid(row=1, column=1, sticky="w", padx=8, pady=5)
ui_checkbox(lab_source_box, "Use real Windows ANI when available", cursor_use_real_ani_var, lambda: mark_cursor_lab_pending("ANI source setting changed. Click Apply Cursor Lab to activate it.")).grid(row=1, column=2, sticky="w", padx=8, pady=5)
ui_label(lab_source_box, "Animation speed:").grid(row=2, column=0, sticky="w", padx=8, pady=5)
ui_combo(lab_source_box, cursor_animation_speed_mode_var, CURSOR_ANIMATION_SPEED_OPTIONS, width=160, command=lambda _value: mark_cursor_lab_pending("Animation speed changed. Click Apply Cursor Lab to activate it.")).grid(row=2, column=1, sticky="w", padx=8, pady=5)
ui_button(lab_source_box, "Load Image / Cursor File", load_custom_cursor_image, width=230).grid(row=3, column=0, padx=8, pady=7)
ui_button(lab_source_box, "Reset to Captured System Cursor", reset_to_system_cursor_image, secondary=True, width=260).grid(row=3, column=1, padx=8, pady=7)
ui_label(lab_source_box, "Hotspot mode:").grid(row=4, column=0, sticky="w", padx=8, pady=5)
ui_combo(lab_source_box, custom_cursor_hotspot_mode_var, ["Top-left", "Center", "Bottom-center"], width=180, command=lambda _value: mark_cursor_lab_pending("Hotspot mode changed. Click Apply Cursor Lab to activate it.")).grid(row=4, column=1, sticky="w", padx=8, pady=5)
ui_label(lab_source_box, "Custom path:").grid(row=5, column=0, sticky="w", padx=8, pady=5)
ui_entry(lab_source_box, custom_cursor_path_var, width=430).grid(row=5, column=1, columnspan=3, sticky="w", padx=8, pady=5)
ui_label(lab_source_box, "Animation source status:").grid(row=6, column=0, sticky="nw", padx=8, pady=5)
ui_label(lab_source_box, textvariable=cursor_animation_source_status_var, wraplength=760).grid(row=6, column=1, columnspan=3, sticky="w", padx=8, pady=5)
ui_label(lab_source_box, textvariable=custom_cursor_status_var, wraplength=760).grid(row=7, column=0, columnspan=4, sticky="w", padx=8, pady=5)

lab_scale_box = make_hscroll_section(cursor_lab_tab, "Cursor Size Controls")
ui_label(lab_scale_box, "Drawn-real cursor size:").grid(row=0, column=0, sticky="w", padx=8, pady=5)
ui_slider(lab_scale_box, real_cursor_scale_var, 0.25, 3.0, ui_set_drawn_cursor_scale, width=270).grid(row=0, column=1, sticky="w", padx=8, pady=5)
ui_label(lab_scale_box, textvariable=real_cursor_scale_label_var).grid(row=0, column=2, sticky="w", padx=8, pady=5)
ui_label(lab_scale_box, "Fake cursor size multiplier:").grid(row=1, column=0, sticky="w", padx=8, pady=5)
ui_slider(lab_scale_box, fake_cursor_scale_multiplier_var, 0.25, 3.0, ui_set_fake_cursor_scale_multiplier, width=270).grid(row=1, column=1, sticky="w", padx=8, pady=5)
ui_label(lab_scale_box, textvariable=fake_cursor_scale_multiplier_label_var).grid(row=1, column=2, sticky="w", padx=8, pady=5)
ui_label(lab_scale_box, "Drawn scale affects the real cursor hint. Fake multiplier affects every swarm cursor without changing cursor count.", wraplength=720).grid(row=2, column=0, columnspan=3, sticky="w", padx=8, pady=5)

lab_color_box = make_hscroll_section(cursor_lab_tab, "Colored Cursor / Tint")
ui_checkbox(lab_color_box, "Enable cursor tint", cursor_tint_enabled_var, lambda: mark_cursor_lab_pending("Tint setting changed. Click Apply Cursor Lab to activate it.")).grid(row=0, column=0, sticky="w", padx=8, pady=5)
ui_checkbox(lab_color_box, "Tint drawn-real cursor", cursor_tint_apply_drawn_var, lambda: mark_cursor_lab_pending("Drawn tint target changed. Click Apply Cursor Lab to activate it.")).grid(row=0, column=1, sticky="w", padx=8, pady=5)
ui_checkbox(lab_color_box, "Tint fake cursors", cursor_tint_apply_fake_var, lambda: mark_cursor_lab_pending("Fake tint target changed. Click Apply Cursor Lab to activate it.")).grid(row=0, column=2, sticky="w", padx=8, pady=5)
ui_checkbox(lab_color_box, "Bright neon tint", cursor_tint_bright_neon_var, lambda: mark_cursor_lab_pending("Bright neon tint changed. Click Apply Cursor Lab to activate it.")).grid(row=0, column=3, sticky="w", padx=8, pady=5)
ui_label(lab_color_box, "Tint style:").grid(row=1, column=0, sticky="w", padx=8, pady=5)
ui_combo(lab_color_box, cursor_tint_style_var, CURSOR_TINT_STYLE_OPTIONS, width=220, command=on_cursor_tint_style_change).grid(row=1, column=1, sticky="w", padx=8, pady=5)
ui_label(lab_color_box, "Multi-colour preset:").grid(row=1, column=2, sticky="w", padx=8, pady=5)
cursor_tint_multi_combo = ui_combo(lab_color_box, cursor_tint_multi_preset_var, list(NEON_COLOR_PRESETS.keys()), width=220, command=on_cursor_tint_multi_preset_change)
cursor_tint_multi_combo.grid(row=1, column=3, sticky="w", padx=8, pady=5)
ui_label(lab_color_box, "Tint color:").grid(row=2, column=0, sticky="w", padx=8, pady=5)
ui_entry(lab_color_box, cursor_tint_color_var, width=120).grid(row=2, column=1, sticky="w", padx=8, pady=5)
ui_button(lab_color_box, "Choose Color", choose_cursor_tint_color, secondary=True, width=150).grid(row=2, column=2, sticky="w", padx=8, pady=5)
ui_button(lab_color_box, "Copy Preset Primary to Tint", copy_multi_preset_primary_to_tint, secondary=True, width=220).grid(row=2, column=3, sticky="w", padx=8, pady=5)
ui_label(lab_color_box, "Tint strength:").grid(row=3, column=0, sticky="w", padx=8, pady=5)
ui_slider(lab_color_box, cursor_tint_strength_var, 0.0, 1.0, ui_set_cursor_tint_strength, width=270).grid(row=3, column=1, sticky="w", padx=8, pady=5)
ui_label(lab_color_box, textvariable=cursor_tint_strength_label_var).grid(row=3, column=2, sticky="w", padx=8, pady=5)
ui_label(lab_color_box, "Neon intensity:").grid(row=4, column=0, sticky="w", padx=8, pady=5)
ui_slider(lab_color_box, cursor_tint_neon_brightness_var, 1.0, 4.0, ui_set_cursor_tint_neon_brightness, width=270).grid(row=4, column=1, sticky="w", padx=8, pady=5)
ui_label(lab_color_box, textvariable=cursor_tint_neon_brightness_label_var).grid(row=4, column=2, sticky="w", padx=8, pady=5)
ui_checkbox(lab_color_box, "Black outline", cursor_tint_black_outline_var, lambda: mark_cursor_lab_pending("Black outline changed. Click Apply Cursor Lab to activate it.")).grid(row=5, column=0, sticky="w", padx=8, pady=5)
ui_label(lab_color_box, "Outline thickness:").grid(row=6, column=0, sticky="w", padx=8, pady=5)
ui_slider(lab_color_box, cursor_tint_outline_thickness_var, 1, 6, ui_set_cursor_tint_outline_thickness, width=270).grid(row=6, column=1, sticky="w", padx=8, pady=5)
ui_label(lab_color_box, textvariable=cursor_tint_outline_thickness_label_var).grid(row=6, column=2, sticky="w", padx=8, pady=5)
ui_label(lab_color_box, "Single Colour keeps your chosen tint color. Multi-Colour Neon Preset applies a vertical neon gradient using preset palettes like Cyberpunk, Toxic Plasma, Lava Circuit, and Electric Ice. Black outline uses the same drawn/fake target checkboxes above.", wraplength=720).grid(row=7, column=0, columnspan=4, sticky="w", padx=8, pady=5)

lab_idle_box = make_hscroll_section(cursor_lab_tab, "Idle Effects + Neon")
ui_checkbox(lab_idle_box, "Enable idle effects", idle_effect_enabled_var, lambda: mark_cursor_lab_pending("Idle effects changed. Click Apply Cursor Lab to activate it.")).grid(row=0, column=0, sticky="w", padx=8, pady=5)
ui_label(lab_idle_box, "Idle effect style:").grid(row=1, column=0, sticky="w", padx=8, pady=5)
ui_combo(lab_idle_box, idle_effect_style_var, IDLE_EFFECT_OPTIONS, width=180, command=on_idle_effect_style_change).grid(row=1, column=1, sticky="w", padx=8, pady=5)
ui_label(lab_idle_box, "Idle delay:").grid(row=2, column=0, sticky="w", padx=8, pady=5)
ui_slider(lab_idle_box, idle_effect_delay_var, 0.20, 6.0, ui_set_idle_effect_delay, width=270).grid(row=2, column=1, sticky="w", padx=8, pady=5)
ui_label(lab_idle_box, textvariable=idle_effect_delay_label_var).grid(row=2, column=2, sticky="w", padx=8, pady=5)
ui_label(lab_idle_box, "Effect strength:").grid(row=3, column=0, sticky="w", padx=8, pady=5)
ui_slider(lab_idle_box, idle_effect_strength_var, 0.0, 1.0, ui_set_idle_effect_strength, width=270).grid(row=3, column=1, sticky="w", padx=8, pady=5)
ui_label(lab_idle_box, textvariable=idle_effect_strength_label_var).grid(row=3, column=2, sticky="w", padx=8, pady=5)
ui_checkbox(lab_idle_box, "Enable neon glow colors", idle_neon_enabled_var, lambda: mark_cursor_lab_pending("Idle neon mode changed. Click Apply Cursor Lab to activate it.")).grid(row=4, column=0, sticky="w", padx=8, pady=5)
ui_label(lab_idle_box, "Fancy neon preset:").grid(row=5, column=0, sticky="w", padx=8, pady=5)
idle_neon_combo = ui_combo(lab_idle_box, idle_neon_preset_var, list(NEON_COLOR_PRESETS.keys()), width=180, command=on_idle_neon_preset_change)
idle_neon_combo.grid(row=5, column=1, sticky="w", padx=8, pady=5)
ui_entry(lab_idle_box, idle_neon_color_var, width=140).grid(row=5, column=2, sticky="w", padx=8, pady=5)
ui_button(lab_idle_box, "Choose Neon Color", choose_idle_neon_color, secondary=True, width=170).grid(row=5, column=3, sticky="w", padx=8, pady=5)
ui_button(lab_idle_box, "Copy Primary Neon to Tint", copy_neon_preset_to_tint, secondary=True, width=220).grid(row=6, column=0, padx=8, pady=7)
ui_label(lab_idle_box, "Pulse = breathing cursor. Glow Ring = layered multi-color neon ring. Fade = cursor gently fades. Wobble = cursor lightly floats in place when idle.", wraplength=720).grid(row=7, column=0, columnspan=4, sticky="w", padx=8, pady=5)

lab_actions_box = make_hscroll_section(cursor_lab_tab, "Apply / Reset Cursor Lab")
ui_button(lab_actions_box, "Apply Cursor Lab", lambda: apply_cursor_lab_from_ui(show_message=True), width=180).grid(row=0, column=0, padx=8, pady=7)
ui_button(lab_actions_box, "Turn Off Replacement Mode", disable_cursor_lab_replacement_mode, secondary=True, width=245).grid(row=0, column=1, padx=8, pady=7)
ui_button(lab_actions_box, "Reset Color + Fake Size", reset_cursor_lab_visuals, secondary=True, width=210).grid(row=0, column=2, padx=8, pady=7)
ui_button(lab_actions_box, "Reset Source to System", reset_to_system_cursor_image, secondary=True, width=210).grid(row=1, column=0, padx=8, pady=7)
ui_label(
    lab_actions_box,
    "Use Turn Off Replacement Mode to return to the normal Windows cursor after testing custom source, tint, resize, or offset replacement features.",
    wraplength=720,
).grid(row=2, column=0, columnspan=4, sticky="w", padx=8, pady=5)

# Mirror tab
mirror_tab = create_scrollable_tab(notebook, "Mirror")

mirror_box = make_section(mirror_tab, "Raw Input Mirror Mode")
ui_checkbox(mirror_box, "Mirror Enabled", mirror_enabled_var, ui_toggle_mirror).grid(row=0, column=0, sticky="w", padx=8, pady=5)
ui_checkbox(mirror_box, "Mirror X", mirror_x_var, ui_toggle_mirror_x).grid(row=1, column=0, sticky="w", padx=8, pady=5)
ui_checkbox(mirror_box, "Mirror Y", mirror_y_var, ui_toggle_mirror_y).grid(row=1, column=1, sticky="w", padx=8, pady=5)
ui_label(mirror_box, "Mirror Strength:").grid(row=2, column=0, sticky="w", padx=8, pady=8)
ui_slider(mirror_box, mirror_strength_var, 0.25, 2.0, ui_set_mirror_strength, width=270).grid(row=2, column=1, sticky="w", padx=8, pady=8)
ui_label(mirror_box, textvariable=mirror_strength_label_var).grid(row=2, column=2, sticky="w", padx=8, pady=8)
ui_button(mirror_box, "Disable Mirror", ui_disable_mirror, secondary=True).grid(row=3, column=0, padx=8, pady=7)
ui_label(mirror_box, "Hold Shift = temporary normal movement", wraplength=650).grid(row=4, column=0, columnspan=3, sticky="w", padx=8, pady=5)

# Swarm tab
swarm_tab = create_scrollable_tab(notebook, "Swarm")

swarm_box = make_section(swarm_tab, "Swarm Controls")
ui_checkbox(swarm_box, "Show Fake Cursors", show_fake_var, ui_toggle_fake_cursors).grid(row=0, column=0, sticky="w", padx=8, pady=5)
ui_checkbox(swarm_box, "Pause Swarm", pause_var, ui_toggle_pause).grid(row=0, column=1, sticky="w", padx=8, pady=5)
ui_checkbox(swarm_box, "Randomize Draw Order", randomize_draw_order_var, apply_swarm_settings_from_ui).grid(row=0, column=2, sticky="w", padx=8, pady=5)
ui_button(swarm_box, "Resume Swarm", ui_resume_swarm).grid(row=1, column=0, padx=8, pady=7)
ui_button(swarm_box, "Pause Swarm", ui_pause_swarm, secondary=True).grid(row=1, column=1, padx=8, pady=7)

density_box = make_section(swarm_tab, "Screen Density Preset")
ui_label(density_box, "Screen Density:").grid(row=0, column=0, sticky="w", padx=8, pady=5)
density_combo = ui_combo(density_box, density_preset_var, ["Custom"] + list(SCREEN_DENSITY_PRESETS.keys()), width=180)
density_combo.grid(row=0, column=1, sticky="w", padx=8, pady=5)
ui_button(density_box, "Apply Density", apply_density_preset_from_ui).grid(row=0, column=2, padx=8, pady=5)
ui_label(density_box, "Density spreads cursors globally across the whole screen, not around the real cursor.", wraplength=650).grid(row=1, column=0, columnspan=3, sticky="w", padx=8, pady=5)

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
    ui_label(count_box, f"{label_text}:").grid(row=row, column=col, sticky="w", padx=8, pady=5)
    ui_spinbox(count_box, variable, 0, 500).grid(row=row, column=col + 1, sticky="w", padx=8, pady=5)

ui_label(count_box, "Movement Threshold:").grid(row=3, column=0, sticky="w", padx=8, pady=5)
ui_spinbox(count_box, movement_threshold_var, 0.0, 10.0, increment=0.1).grid(row=3, column=1, sticky="w", padx=8, pady=5)
ui_label(count_box, "Movement Randomness / Wobble:").grid(row=3, column=2, sticky="w", padx=8, pady=5)
ui_slider(count_box, fake_cursor_wobble_var, 0.0, 2.5, lambda value: fake_cursor_wobble_label_var.set(f"{float(value):.2f}x"), width=200).grid(row=3, column=3, sticky="w", padx=8, pady=5)
ui_label(count_box, textvariable=fake_cursor_wobble_label_var).grid(row=3, column=4, sticky="w", padx=8, pady=5)

count_buttons = make_section(swarm_tab, "Apply / Reset")
ui_button(count_buttons, "Apply Swarm Settings", apply_swarm_settings_from_ui, width=185).grid(row=0, column=0, padx=8, pady=7)
ui_button(count_buttons, "Reset Fields to Current", reset_swarm_entries_to_current, secondary=True, width=195).grid(row=0, column=1, padx=8, pady=7)
ui_button(count_buttons, "Rebuild Cursor Swarm", rebuild_fake_cursors, secondary=True, width=185).grid(row=0, column=2, padx=8, pady=7)

summary_box = make_section(swarm_tab, "Current Swarm Summary")
ui_label(summary_box, textvariable=swarm_summary_var, wraplength=720).pack(anchor="w", padx=8, pady=5)

# Performance tab
performance_tab = create_scrollable_tab(notebook, "Performance")

perf_mode_box = make_section(performance_tab, "Performance Mode")
ui_label(perf_mode_box, "Performance preset:").grid(row=0, column=0, sticky="w", padx=8, pady=5)
performance_mode_combo = ui_combo(perf_mode_box, performance_mode_var, PERFORMANCE_MODE_OPTIONS, width=220, command=lambda _value: mark_performance_pending("Preset selected. Click Load Preset Values, then Apply Performance Settings."))
performance_mode_combo.grid(row=0, column=1, sticky="w", padx=8, pady=5)
ui_button(perf_mode_box, "Load Preset Values", load_performance_preset_values_from_ui, width=180).grid(row=0, column=2, padx=8, pady=5)
ui_label(perf_mode_box, "Smooth = best overlay animation. Balanced = lighter. Battery Saver = lower overlay FPS + simple glow drawing + idle-saving options. Presets are staged until you apply them.", wraplength=720).grid(row=1, column=0, columnspan=4, sticky="w", padx=8, pady=5)

perf_fps_box = make_section(performance_tab, "Frame Rate / Battery")
ui_label(perf_fps_box, "Target overlay FPS:").grid(row=0, column=0, sticky="w", padx=8, pady=5)
ui_slider(perf_fps_box, performance_fps_var, 15, 60, ui_set_performance_fps, width=270).grid(row=0, column=1, sticky="w", padx=8, pady=5)
ui_label(perf_fps_box, textvariable=performance_fps_label_var).grid(row=0, column=2, sticky="w", padx=8, pady=5)
ui_checkbox(perf_fps_box, "Battery Saver Glow Mode (simpler glow drawing)", reduce_glow_quality_var, lambda: mark_performance_pending("Glow drawing detail changed in the panel only. Click Apply Performance Settings.")).grid(row=1, column=0, columnspan=2, sticky="w", padx=8, pady=5)
ui_checkbox(perf_fps_box, "Hide Fake Cursors After Long Idle", pause_swarm_long_idle_var, lambda: mark_performance_pending("Fake swarm long-idle behavior changed in the panel only. Click Apply Performance Settings.")).grid(row=2, column=0, columnspan=2, sticky="w", padx=8, pady=5)
ui_checkbox(perf_fps_box, "Pause Idle Effects After Long Idle", pause_idle_effects_long_idle_var, lambda: mark_performance_pending("Idle effect long-idle behavior changed in the panel only. Click Apply Performance Settings.")).grid(row=3, column=0, columnspan=2, sticky="w", padx=8, pady=5)
ui_label(perf_fps_box, "Long idle time:").grid(row=4, column=0, sticky="w", padx=8, pady=5)
ui_slider(perf_fps_box, long_idle_seconds_var, 10, 300, ui_set_long_idle_seconds, width=270).grid(row=4, column=1, sticky="w", padx=8, pady=5)
ui_label(perf_fps_box, textvariable=long_idle_seconds_label_var).grid(row=4, column=2, sticky="w", padx=8, pady=5)
ui_button(perf_fps_box, "Apply Performance Settings", lambda: apply_performance_settings_from_ui(show_message=True), width=230).grid(row=5, column=0, padx=8, pady=7)
ui_button(perf_fps_box, "Reset to Smooth", lambda: (performance_mode_var.set("Smooth (60 FPS)"), load_performance_preset_values_from_ui()), secondary=True, width=170).grid(row=5, column=1, padx=8, pady=7)

perf_summary_box = make_section(performance_tab, "Current Performance Summary")
ui_label(perf_summary_box, textvariable=performance_summary_var, wraplength=720).pack(anchor="w", padx=8, pady=5)

# Movement tab
movement_tab = create_scrollable_tab(notebook, "Movement")

movement_main_box = make_hscroll_section(movement_tab, "Movement Effects")
ui_checkbox(movement_main_box, "Enable Movement Effects", movement_effects_enabled_var, lambda: mark_movement_pending("Movement effects changed in the panel only. Click Apply Movement Settings.")).grid(row=0, column=0, sticky="w", padx=8, pady=5)
ui_checkbox(movement_main_box, "Motion Trail", movement_motion_trail_enabled_var, on_movement_effect_checkbox_change).grid(row=1, column=0, sticky="w", padx=8, pady=5)
ui_checkbox(movement_main_box, "Speed Glow", movement_speed_glow_enabled_var, on_movement_effect_checkbox_change).grid(row=1, column=1, sticky="w", padx=8, pady=5)
ui_checkbox(movement_main_box, "Motion Streak", movement_motion_streak_enabled_var, on_movement_effect_checkbox_change).grid(row=1, column=2, sticky="w", padx=8, pady=5)
ui_checkbox(movement_main_box, "Spark Particles", movement_spark_particles_enabled_var, on_movement_effect_checkbox_change).grid(row=1, column=3, sticky="w", padx=8, pady=5)
ui_checkbox(movement_main_box, "Ripple Burst", movement_ripple_burst_enabled_var, on_movement_effect_checkbox_change).grid(row=2, column=0, sticky="w", padx=8, pady=5)
ui_checkbox(movement_main_box, "Comet Tail", movement_comet_tail_enabled_var, on_movement_effect_checkbox_change).grid(row=2, column=1, sticky="w", padx=8, pady=5)
ui_checkbox(movement_main_box, "Speed Lines", movement_speed_lines_enabled_var, on_movement_effect_checkbox_change).grid(row=2, column=2, sticky="w", padx=8, pady=5)
ui_checkbox(movement_main_box, "Magnetic Orbit", movement_magnetic_orbit_enabled_var, on_movement_effect_checkbox_change).grid(row=2, column=3, sticky="w", padx=8, pady=5)
ui_checkbox(movement_main_box, "Click Effects", click_effects_enabled_var, on_movement_effect_checkbox_change).grid(row=3, column=0, sticky="w", padx=8, pady=5)
ui_label(movement_main_box, "Choose effects with checkboxes, then open each sub-tab below to tune that effect. Settings are staged until Apply Movement Settings.", wraplength=720).grid(row=4, column=0, columnspan=4, sticky="w", padx=8, pady=5)

movement_settings_box = make_hscroll_section(movement_tab, "Movement Effect Settings")
movement_effect_tabs = ctk.CTkTabview(
    movement_settings_box,
    fg_color="#111827",
    border_color="#334155",
    border_width=1,
    segmented_button_fg_color="#0f172a",
    segmented_button_selected_color="#2563eb",
    segmented_button_selected_hover_color="#1d4ed8",
    segmented_button_unselected_color="#1e293b",
    segmented_button_unselected_hover_color="#334155",
    text_color="#f8fafc",
)
movement_effect_tabs.grid(row=0, column=0, sticky="ew", padx=0, pady=4)
movement_settings_box.grid_columnconfigure(0, weight=1)
try:
    movement_effect_tabs._segmented_button.grid_configure(padx=0, sticky="w")
except Exception:
    pass
trail_tab = movement_effect_tabs.add("Motion Trail")
speed_tab = movement_effect_tabs.add("Speed Glow")
streak_tab = movement_effect_tabs.add("Motion Streak")
spark_tab = movement_effect_tabs.add("Spark Particles")
ripple_tab = movement_effect_tabs.add("Ripple Burst")
comet_tab = movement_effect_tabs.add("Comet Tail")
lines_tab = movement_effect_tabs.add("Speed Lines")
orbit_tab = movement_effect_tabs.add("Magnetic Orbit")
click_tab = movement_effect_tabs.add("Click Effects")

for _movement_sub_tab in (trail_tab, speed_tab, streak_tab, spark_tab, ripple_tab, comet_tab, lines_tab, orbit_tab, click_tab):
    try:
        _movement_sub_tab.configure(fg_color="#111827")
    except Exception:
        pass

# Remove the extra left padding before Movement sub-tab names so the tab row
# starts closer to the left edge, especially inside the horizontal-scroll box.
try:
    movement_effect_tabs._segmented_button.grid_configure(padx=0, sticky="w")
    movement_effect_tabs._segmented_button.configure(corner_radius=8)
except Exception:
    pass

# Motion Trail settings
ui_label(trail_tab, "Trail length:").grid(row=0, column=0, sticky="w", padx=8, pady=5)
ui_slider(trail_tab, motion_trail_length_var, 3, 40, ui_set_motion_trail_length, width=270).grid(row=0, column=1, sticky="w", padx=8, pady=5)
ui_label(trail_tab, textvariable=motion_trail_length_label_var).grid(row=0, column=2, sticky="w", padx=8, pady=5)
ui_label(trail_tab, "Trail fade strength:").grid(row=1, column=0, sticky="w", padx=8, pady=5)
ui_slider(trail_tab, motion_trail_fade_var, 0.10, 1.0, ui_set_motion_trail_fade, width=270).grid(row=1, column=1, sticky="w", padx=8, pady=5)
ui_label(trail_tab, textvariable=motion_trail_fade_label_var).grid(row=1, column=2, sticky="w", padx=8, pady=5)
ui_button(trail_tab, "Clear Trail", clear_motion_trail, secondary=True, width=140).grid(row=2, column=0, padx=8, pady=7)
ui_label(trail_tab, "Motion Trail uses the current Cursor Lab drawn cursor appearance. Separate Trail Colour controls were removed for now because they caused inconsistent trail ghost colours.", wraplength=720).grid(row=3, column=0, columnspan=4, sticky="w", padx=8, pady=5)

# Speed Glow settings
ui_label(speed_tab, "Glow strength:").grid(row=0, column=0, sticky="w", padx=8, pady=5)
ui_slider(speed_tab, speed_glow_strength_var, 0.0, 1.0, ui_set_speed_glow_strength, width=270).grid(row=0, column=1, sticky="w", padx=8, pady=5)
ui_label(speed_tab, textvariable=speed_glow_strength_label_var).grid(row=0, column=2, sticky="w", padx=8, pady=5)
ui_label(speed_tab, "Trigger speed:").grid(row=1, column=0, sticky="w", padx=8, pady=5)
ui_slider(speed_tab, speed_glow_threshold_var, 150, 2500, ui_set_speed_glow_threshold, width=270).grid(row=1, column=1, sticky="w", padx=8, pady=5)
ui_label(speed_tab, textvariable=speed_glow_threshold_label_var).grid(row=1, column=2, sticky="w", padx=8, pady=5)
ui_label(speed_tab, "Glow colour mode:").grid(row=2, column=0, sticky="w", padx=8, pady=5)
ui_combo(speed_tab, speed_glow_color_mode_var, MOVEMENT_COLOR_MODE_OPTIONS, width=230, command=mark_movement_color_pending).grid(row=2, column=1, sticky="w", padx=8, pady=5)
ui_entry(speed_tab, speed_glow_custom_color_var, width=120).grid(row=2, column=2, sticky="w", padx=8, pady=5)
ui_button(speed_tab, "Choose", lambda: choose_movement_custom_color("speed"), secondary=True, width=100).grid(row=2, column=3, padx=8, pady=5)
ui_label(speed_tab, "Single colour preset:").grid(row=3, column=0, sticky="w", padx=8, pady=5)
ui_combo(speed_tab, speed_glow_single_preset_var, list(MOVEMENT_SINGLE_COLOR_PRESETS.keys()), width=220, command=mark_movement_color_pending).grid(row=3, column=1, sticky="w", padx=8, pady=5)
ui_label(speed_tab, "Multi-colour preset:").grid(row=4, column=0, sticky="w", padx=8, pady=5)
speed_glow_neon_combo = ui_combo(speed_tab, speed_glow_neon_preset_var, list(NEON_COLOR_PRESETS.keys()), width=220, command=mark_movement_color_pending)
speed_glow_neon_combo.grid(row=4, column=1, sticky="w", padx=8, pady=5)
ui_button(speed_tab, "Apply This Colour To All", lambda: apply_movement_color_to_all("speed"), secondary=True, width=210).grid(row=4, column=2, padx=8, pady=5)
ui_label(speed_tab, "Speed Glow gets stronger when you move faster.", wraplength=720).grid(row=5, column=0, columnspan=4, sticky="w", padx=8, pady=5)

# Motion Streak settings
ui_label(streak_tab, "Streak strength:").grid(row=0, column=0, sticky="w", padx=8, pady=5)
ui_slider(streak_tab, motion_streak_strength_var, 0.0, 1.0, ui_set_motion_streak_strength, width=270).grid(row=0, column=1, sticky="w", padx=8, pady=5)
ui_label(streak_tab, textvariable=motion_streak_strength_label_var).grid(row=0, column=2, sticky="w", padx=8, pady=5)
ui_label(streak_tab, "Trigger speed:").grid(row=1, column=0, sticky="w", padx=8, pady=5)
ui_slider(streak_tab, motion_streak_threshold_var, 150, 2500, ui_set_motion_streak_threshold, width=270).grid(row=1, column=1, sticky="w", padx=8, pady=5)
ui_label(streak_tab, textvariable=motion_streak_threshold_label_var).grid(row=1, column=2, sticky="w", padx=8, pady=5)
ui_label(streak_tab, "Streak length:").grid(row=2, column=0, sticky="w", padx=8, pady=5)
ui_slider(streak_tab, motion_streak_length_var, 20, 180, ui_set_motion_streak_length, width=270).grid(row=2, column=1, sticky="w", padx=8, pady=5)
ui_label(streak_tab, textvariable=motion_streak_length_label_var).grid(row=2, column=2, sticky="w", padx=8, pady=5)
ui_label(streak_tab, "Streak colour mode:").grid(row=3, column=0, sticky="w", padx=8, pady=5)
ui_combo(streak_tab, motion_streak_color_mode_var, MOVEMENT_COLOR_MODE_OPTIONS, width=230, command=mark_movement_color_pending).grid(row=3, column=1, sticky="w", padx=8, pady=5)
ui_entry(streak_tab, motion_streak_custom_color_var, width=120).grid(row=3, column=2, sticky="w", padx=8, pady=5)
ui_button(streak_tab, "Choose", lambda: choose_movement_custom_color("streak"), secondary=True, width=100).grid(row=3, column=3, padx=8, pady=5)
ui_label(streak_tab, "Single colour preset:").grid(row=4, column=0, sticky="w", padx=8, pady=5)
ui_combo(streak_tab, motion_streak_single_preset_var, list(MOVEMENT_SINGLE_COLOR_PRESETS.keys()), width=220, command=mark_movement_color_pending).grid(row=4, column=1, sticky="w", padx=8, pady=5)
ui_label(streak_tab, "Multi-colour preset:").grid(row=5, column=0, sticky="w", padx=8, pady=5)
motion_streak_neon_combo = ui_combo(streak_tab, motion_streak_neon_preset_var, list(NEON_COLOR_PRESETS.keys()), width=220, command=mark_movement_color_pending)
motion_streak_neon_combo.grid(row=5, column=1, sticky="w", padx=8, pady=5)
ui_button(streak_tab, "Apply This Colour To All", lambda: apply_movement_color_to_all("streak"), secondary=True, width=210).grid(row=5, column=2, padx=8, pady=5)
ui_label(streak_tab, "Motion Streak draws a directional neon slash behind the cursor when movement speed crosses the trigger speed.", wraplength=720).grid(row=6, column=0, columnspan=4, sticky="w", padx=8, pady=5)

# Spark Particle settings
ui_label(spark_tab, "Spark strength:").grid(row=0, column=0, sticky="w", padx=8, pady=5)
ui_slider(spark_tab, spark_particle_strength_var, 0.0, 1.0, ui_set_spark_particle_strength, width=270).grid(row=0, column=1, sticky="w", padx=8, pady=5)
ui_label(spark_tab, textvariable=spark_particle_strength_label_var).grid(row=0, column=2, sticky="w", padx=8, pady=5)
ui_label(spark_tab, "Trigger speed:").grid(row=1, column=0, sticky="w", padx=8, pady=5)
ui_slider(spark_tab, spark_particle_threshold_var, 100, 2500, ui_set_spark_particle_threshold, width=270).grid(row=1, column=1, sticky="w", padx=8, pady=5)
ui_label(spark_tab, textvariable=spark_particle_threshold_label_var).grid(row=1, column=2, sticky="w", padx=8, pady=5)
ui_label(spark_tab, "Particle amount:").grid(row=2, column=0, sticky="w", padx=8, pady=5)
ui_slider(spark_tab, spark_particle_amount_var, 1, 12, ui_set_spark_particle_amount, width=270).grid(row=2, column=1, sticky="w", padx=8, pady=5)
ui_label(spark_tab, textvariable=spark_particle_amount_label_var).grid(row=2, column=2, sticky="w", padx=8, pady=5)
ui_label(spark_tab, "Particle size:").grid(row=3, column=0, sticky="w", padx=8, pady=5)
ui_slider(spark_tab, spark_particle_size_var, 2, 10, ui_set_spark_particle_size, width=270).grid(row=3, column=1, sticky="w", padx=8, pady=5)
ui_label(spark_tab, textvariable=spark_particle_size_label_var).grid(row=3, column=2, sticky="w", padx=8, pady=5)
ui_label(spark_tab, "Particle lifetime:").grid(row=4, column=0, sticky="w", padx=8, pady=5)
ui_slider(spark_tab, spark_particle_lifetime_var, 0.20, 2.0, ui_set_spark_particle_lifetime, width=270).grid(row=4, column=1, sticky="w", padx=8, pady=5)
ui_label(spark_tab, textvariable=spark_particle_lifetime_label_var).grid(row=4, column=2, sticky="w", padx=8, pady=5)
ui_label(spark_tab, "Spark colour mode:").grid(row=5, column=0, sticky="w", padx=8, pady=5)
ui_combo(spark_tab, spark_particle_color_mode_var, MOVEMENT_COLOR_MODE_OPTIONS, width=230, command=mark_movement_color_pending).grid(row=5, column=1, sticky="w", padx=8, pady=5)
ui_entry(spark_tab, spark_particle_custom_color_var, width=120).grid(row=5, column=2, sticky="w", padx=8, pady=5)
ui_button(spark_tab, "Choose", lambda: choose_movement_custom_color("spark"), secondary=True, width=100).grid(row=5, column=3, padx=8, pady=5)
ui_label(spark_tab, "Single colour preset:").grid(row=6, column=0, sticky="w", padx=8, pady=5)
ui_combo(spark_tab, spark_particle_single_preset_var, list(MOVEMENT_SINGLE_COLOR_PRESETS.keys()), width=220, command=mark_movement_color_pending).grid(row=6, column=1, sticky="w", padx=8, pady=5)
ui_label(spark_tab, "Multi-colour preset:").grid(row=7, column=0, sticky="w", padx=8, pady=5)
spark_particle_neon_combo = ui_combo(spark_tab, spark_particle_neon_preset_var, list(NEON_COLOR_PRESETS.keys()), width=220, command=mark_movement_color_pending)
spark_particle_neon_combo.grid(row=7, column=1, sticky="w", padx=8, pady=5)
ui_button(spark_tab, "Apply This Colour To All", lambda: apply_movement_color_to_all("spark"), secondary=True, width=210).grid(row=7, column=2, padx=8, pady=5)
ui_label(spark_tab, "Spark Particles create tiny neon dots behind the cursor while moving quickly. Use lower amount/lifetime for battery saver mode.", wraplength=720).grid(row=8, column=0, columnspan=4, sticky="w", padx=8, pady=5)


# Ripple Burst settings
ui_label(ripple_tab, "Ripple strength:").grid(row=0, column=0, sticky="w", padx=8, pady=5)
ui_slider(ripple_tab, ripple_burst_strength_var, 0.0, 1.0, ui_set_ripple_burst_strength, width=270).grid(row=0, column=1, sticky="w", padx=8, pady=5)
ui_label(ripple_tab, textvariable=ripple_burst_strength_label_var).grid(row=0, column=2, sticky="w", padx=8, pady=5)
ui_label(ripple_tab, "Trigger speed:").grid(row=1, column=0, sticky="w", padx=8, pady=5)
ui_slider(ripple_tab, ripple_burst_threshold_var, 100, 3000, ui_set_ripple_burst_threshold, width=270).grid(row=1, column=1, sticky="w", padx=8, pady=5)
ui_label(ripple_tab, textvariable=ripple_burst_threshold_label_var).grid(row=1, column=2, sticky="w", padx=8, pady=5)
ui_label(ripple_tab, "Lifetime:").grid(row=2, column=0, sticky="w", padx=8, pady=5)
ui_slider(ripple_tab, ripple_burst_lifetime_var, 0.25, 2.0, ui_set_ripple_burst_lifetime, width=270).grid(row=2, column=1, sticky="w", padx=8, pady=5)
ui_label(ripple_tab, textvariable=ripple_burst_lifetime_label_var).grid(row=2, column=2, sticky="w", padx=8, pady=5)
ui_label(ripple_tab, "Max radius:").grid(row=3, column=0, sticky="w", padx=8, pady=5)
ui_slider(ripple_tab, ripple_burst_radius_var, 20, 180, ui_set_ripple_burst_radius, width=270).grid(row=3, column=1, sticky="w", padx=8, pady=5)
ui_label(ripple_tab, textvariable=ripple_burst_radius_label_var).grid(row=3, column=2, sticky="w", padx=8, pady=5)
ui_label(ripple_tab, "Ripple colour mode:").grid(row=4, column=0, sticky="w", padx=8, pady=5)
ui_combo(ripple_tab, ripple_burst_color_mode_var, MOVEMENT_COLOR_MODE_OPTIONS, width=230, command=mark_movement_color_pending).grid(row=4, column=1, sticky="w", padx=8, pady=5)
ui_entry(ripple_tab, ripple_burst_custom_color_var, width=120).grid(row=4, column=2, sticky="w", padx=8, pady=5)
ui_button(ripple_tab, "Choose", lambda: choose_movement_custom_color("ripple"), secondary=True, width=100).grid(row=4, column=3, padx=8, pady=5)
ui_label(ripple_tab, "Single colour preset:").grid(row=5, column=0, sticky="w", padx=8, pady=5)
ui_combo(ripple_tab, ripple_burst_single_preset_var, list(MOVEMENT_SINGLE_COLOR_PRESETS.keys()), width=220, command=mark_movement_color_pending).grid(row=5, column=1, sticky="w", padx=8, pady=5)
ui_label(ripple_tab, "Multi-colour preset:").grid(row=6, column=0, sticky="w", padx=8, pady=5)
ripple_burst_neon_combo = ui_combo(ripple_tab, ripple_burst_neon_preset_var, list(NEON_COLOR_PRESETS.keys()), width=220, command=mark_movement_color_pending)
ripple_burst_neon_combo.grid(row=6, column=1, sticky="w", padx=8, pady=5)
ui_button(ripple_tab, "Apply This Colour To All", lambda: apply_movement_color_to_all("ripple"), secondary=True, width=210).grid(row=6, column=2, padx=8, pady=5)

# Comet Tail settings
ui_label(comet_tab, "Comet strength:").grid(row=0, column=0, sticky="w", padx=8, pady=5)
ui_slider(comet_tab, comet_tail_strength_var, 0.0, 1.0, ui_set_comet_tail_strength, width=270).grid(row=0, column=1, sticky="w", padx=8, pady=5)
ui_label(comet_tab, textvariable=comet_tail_strength_label_var).grid(row=0, column=2, sticky="w", padx=8, pady=5)
ui_label(comet_tab, "Tail length:").grid(row=1, column=0, sticky="w", padx=8, pady=5)
ui_slider(comet_tab, comet_tail_length_var, 30, 240, ui_set_comet_tail_length, width=270).grid(row=1, column=1, sticky="w", padx=8, pady=5)
ui_label(comet_tab, textvariable=comet_tail_length_label_var).grid(row=1, column=2, sticky="w", padx=8, pady=5)
ui_label(comet_tab, "Tail thickness:").grid(row=2, column=0, sticky="w", padx=8, pady=5)
ui_slider(comet_tab, comet_tail_thickness_var, 2, 18, ui_set_comet_tail_thickness, width=270).grid(row=2, column=1, sticky="w", padx=8, pady=5)
ui_label(comet_tab, textvariable=comet_tail_thickness_label_var).grid(row=2, column=2, sticky="w", padx=8, pady=5)
ui_label(comet_tab, "Comet colour mode:").grid(row=3, column=0, sticky="w", padx=8, pady=5)
ui_combo(comet_tab, comet_tail_color_mode_var, MOVEMENT_COLOR_MODE_OPTIONS, width=230, command=mark_movement_color_pending).grid(row=3, column=1, sticky="w", padx=8, pady=5)
ui_entry(comet_tab, comet_tail_custom_color_var, width=120).grid(row=3, column=2, sticky="w", padx=8, pady=5)
ui_button(comet_tab, "Choose", lambda: choose_movement_custom_color("comet"), secondary=True, width=100).grid(row=3, column=3, padx=8, pady=5)
ui_label(comet_tab, "Single colour preset:").grid(row=4, column=0, sticky="w", padx=8, pady=5)
ui_combo(comet_tab, comet_tail_single_preset_var, list(MOVEMENT_SINGLE_COLOR_PRESETS.keys()), width=220, command=mark_movement_color_pending).grid(row=4, column=1, sticky="w", padx=8, pady=5)
ui_label(comet_tab, "Multi-colour preset:").grid(row=5, column=0, sticky="w", padx=8, pady=5)
comet_tail_neon_combo = ui_combo(comet_tab, comet_tail_neon_preset_var, list(NEON_COLOR_PRESETS.keys()), width=220, command=mark_movement_color_pending)
comet_tail_neon_combo.grid(row=5, column=1, sticky="w", padx=8, pady=5)
ui_button(comet_tab, "Apply This Colour To All", lambda: apply_movement_color_to_all("comet"), secondary=True, width=210).grid(row=5, column=2, padx=8, pady=5)

# Speed Lines settings
ui_label(lines_tab, "Lines strength:").grid(row=0, column=0, sticky="w", padx=8, pady=5)
ui_slider(lines_tab, speed_lines_strength_var, 0.0, 1.0, ui_set_speed_lines_strength, width=270).grid(row=0, column=1, sticky="w", padx=8, pady=5)
ui_label(lines_tab, textvariable=speed_lines_strength_label_var).grid(row=0, column=2, sticky="w", padx=8, pady=5)
ui_label(lines_tab, "Trigger speed:").grid(row=1, column=0, sticky="w", padx=8, pady=5)
ui_slider(lines_tab, speed_lines_threshold_var, 150, 3000, ui_set_speed_lines_threshold, width=270).grid(row=1, column=1, sticky="w", padx=8, pady=5)
ui_label(lines_tab, textvariable=speed_lines_threshold_label_var).grid(row=1, column=2, sticky="w", padx=8, pady=5)
ui_label(lines_tab, "Line amount:").grid(row=2, column=0, sticky="w", padx=8, pady=5)
ui_slider(lines_tab, speed_lines_amount_var, 1, 12, ui_set_speed_lines_amount, width=270).grid(row=2, column=1, sticky="w", padx=8, pady=5)
ui_label(lines_tab, textvariable=speed_lines_amount_label_var).grid(row=2, column=2, sticky="w", padx=8, pady=5)
ui_label(lines_tab, "Line length:").grid(row=3, column=0, sticky="w", padx=8, pady=5)
ui_slider(lines_tab, speed_lines_length_var, 20, 180, ui_set_speed_lines_length, width=270).grid(row=3, column=1, sticky="w", padx=8, pady=5)
ui_label(lines_tab, textvariable=speed_lines_length_label_var).grid(row=3, column=2, sticky="w", padx=8, pady=5)
ui_label(lines_tab, "Lines colour mode:").grid(row=4, column=0, sticky="w", padx=8, pady=5)
ui_combo(lines_tab, speed_lines_color_mode_var, MOVEMENT_COLOR_MODE_OPTIONS, width=230, command=mark_movement_color_pending).grid(row=4, column=1, sticky="w", padx=8, pady=5)
ui_entry(lines_tab, speed_lines_custom_color_var, width=120).grid(row=4, column=2, sticky="w", padx=8, pady=5)
ui_button(lines_tab, "Choose", lambda: choose_movement_custom_color("lines"), secondary=True, width=100).grid(row=4, column=3, padx=8, pady=5)
ui_label(lines_tab, "Single colour preset:").grid(row=5, column=0, sticky="w", padx=8, pady=5)
ui_combo(lines_tab, speed_lines_single_preset_var, list(MOVEMENT_SINGLE_COLOR_PRESETS.keys()), width=220, command=mark_movement_color_pending).grid(row=5, column=1, sticky="w", padx=8, pady=5)
ui_label(lines_tab, "Multi-colour preset:").grid(row=6, column=0, sticky="w", padx=8, pady=5)
speed_lines_neon_combo = ui_combo(lines_tab, speed_lines_neon_preset_var, list(NEON_COLOR_PRESETS.keys()), width=220, command=mark_movement_color_pending)
speed_lines_neon_combo.grid(row=6, column=1, sticky="w", padx=8, pady=5)
ui_button(lines_tab, "Apply This Colour To All", lambda: apply_movement_color_to_all("lines"), secondary=True, width=210).grid(row=6, column=2, padx=8, pady=5)

# Magnetic Orbit settings
ui_label(orbit_tab, "Orbit strength:").grid(row=0, column=0, sticky="w", padx=8, pady=5)
ui_slider(orbit_tab, magnetic_orbit_strength_var, 0.0, 1.0, ui_set_magnetic_orbit_strength, width=270).grid(row=0, column=1, sticky="w", padx=8, pady=5)
ui_label(orbit_tab, textvariable=magnetic_orbit_strength_label_var).grid(row=0, column=2, sticky="w", padx=8, pady=5)
ui_label(orbit_tab, "Trigger speed:").grid(row=1, column=0, sticky="w", padx=8, pady=5)
ui_slider(orbit_tab, magnetic_orbit_threshold_var, 0, 2000, ui_set_magnetic_orbit_threshold, width=270).grid(row=1, column=1, sticky="w", padx=8, pady=5)
ui_label(orbit_tab, textvariable=magnetic_orbit_threshold_label_var).grid(row=1, column=2, sticky="w", padx=8, pady=5)
ui_label(orbit_tab, "Orbit radius:").grid(row=2, column=0, sticky="w", padx=8, pady=5)
ui_slider(orbit_tab, magnetic_orbit_radius_var, 8, 80, ui_set_magnetic_orbit_radius, width=270).grid(row=2, column=1, sticky="w", padx=8, pady=5)
ui_label(orbit_tab, textvariable=magnetic_orbit_radius_label_var).grid(row=2, column=2, sticky="w", padx=8, pady=5)
ui_label(orbit_tab, "Orbit dots:").grid(row=3, column=0, sticky="w", padx=8, pady=5)
ui_slider(orbit_tab, magnetic_orbit_dots_var, 2, 12, ui_set_magnetic_orbit_dots, width=270).grid(row=3, column=1, sticky="w", padx=8, pady=5)
ui_label(orbit_tab, textvariable=magnetic_orbit_dots_label_var).grid(row=3, column=2, sticky="w", padx=8, pady=5)
ui_label(orbit_tab, "Orbit colour mode:").grid(row=4, column=0, sticky="w", padx=8, pady=5)
ui_combo(orbit_tab, magnetic_orbit_color_mode_var, MOVEMENT_COLOR_MODE_OPTIONS, width=230, command=mark_movement_color_pending).grid(row=4, column=1, sticky="w", padx=8, pady=5)
ui_entry(orbit_tab, magnetic_orbit_custom_color_var, width=120).grid(row=4, column=2, sticky="w", padx=8, pady=5)
ui_button(orbit_tab, "Choose", lambda: choose_movement_custom_color("orbit"), secondary=True, width=100).grid(row=4, column=3, padx=8, pady=5)
ui_label(orbit_tab, "Single colour preset:").grid(row=5, column=0, sticky="w", padx=8, pady=5)
ui_combo(orbit_tab, magnetic_orbit_single_preset_var, list(MOVEMENT_SINGLE_COLOR_PRESETS.keys()), width=220, command=mark_movement_color_pending).grid(row=5, column=1, sticky="w", padx=8, pady=5)
ui_label(orbit_tab, "Multi-colour preset:").grid(row=6, column=0, sticky="w", padx=8, pady=5)
magnetic_orbit_neon_combo = ui_combo(orbit_tab, magnetic_orbit_neon_preset_var, list(NEON_COLOR_PRESETS.keys()), width=220, command=mark_movement_color_pending)
magnetic_orbit_neon_combo.grid(row=6, column=1, sticky="w", padx=8, pady=5)
ui_button(orbit_tab, "Apply This Colour To All", lambda: apply_movement_color_to_all("orbit"), secondary=True, width=210).grid(row=6, column=2, padx=8, pady=5)

# Click Effects settings
ui_checkbox(click_tab, "Enable left-click effect", click_effect_left_enabled_var, on_movement_effect_checkbox_change).grid(row=0, column=0, sticky="w", padx=8, pady=5)
ui_checkbox(click_tab, "Enable right-click effect", click_effect_right_enabled_var, on_movement_effect_checkbox_change).grid(row=0, column=1, sticky="w", padx=8, pady=5)
ui_label(click_tab, "Click effect style:").grid(row=1, column=0, sticky="w", padx=8, pady=5)
ui_combo(click_tab, click_effect_style_var, CLICK_EFFECT_STYLE_OPTIONS, width=220, command=on_movement_effect_style_change).grid(row=1, column=1, sticky="w", padx=8, pady=5)
ui_label(click_tab, "Effect strength:").grid(row=2, column=0, sticky="w", padx=8, pady=5)
ui_slider(click_tab, click_effect_strength_var, 0.0, 1.0, ui_set_click_effect_strength, width=270).grid(row=2, column=1, sticky="w", padx=8, pady=5)
ui_label(click_tab, textvariable=click_effect_strength_label_var).grid(row=2, column=2, sticky="w", padx=8, pady=5)
ui_label(click_tab, "Ripple radius:").grid(row=3, column=0, sticky="w", padx=8, pady=5)
ui_slider(click_tab, click_effect_radius_var, 20, 180, ui_set_click_effect_radius, width=270).grid(row=3, column=1, sticky="w", padx=8, pady=5)
ui_label(click_tab, textvariable=click_effect_radius_label_var).grid(row=3, column=2, sticky="w", padx=8, pady=5)
ui_label(click_tab, "Effect lifetime:").grid(row=4, column=0, sticky="w", padx=8, pady=5)
ui_slider(click_tab, click_effect_lifetime_var, 0.20, 2.0, ui_set_click_effect_lifetime, width=270).grid(row=4, column=1, sticky="w", padx=8, pady=5)
ui_label(click_tab, textvariable=click_effect_lifetime_label_var).grid(row=4, column=2, sticky="w", padx=8, pady=5)
ui_label(click_tab, "Spark amount:").grid(row=5, column=0, sticky="w", padx=8, pady=5)
ui_slider(click_tab, click_effect_spark_amount_var, 1, 20, ui_set_click_effect_spark_amount, width=270).grid(row=5, column=1, sticky="w", padx=8, pady=5)
ui_label(click_tab, textvariable=click_effect_spark_amount_label_var).grid(row=5, column=2, sticky="w", padx=8, pady=5)
ui_label(click_tab, "Click colour mode:").grid(row=6, column=0, sticky="w", padx=8, pady=5)
ui_combo(click_tab, click_effect_color_mode_var, MOVEMENT_COLOR_MODE_OPTIONS, width=230, command=mark_movement_color_pending).grid(row=6, column=1, sticky="w", padx=8, pady=5)
ui_entry(click_tab, click_effect_custom_color_var, width=120).grid(row=6, column=2, sticky="w", padx=8, pady=5)
ui_button(click_tab, "Choose", lambda: choose_movement_custom_color("click"), secondary=True, width=100).grid(row=6, column=3, padx=8, pady=5)
ui_label(click_tab, "Single colour preset:").grid(row=7, column=0, sticky="w", padx=8, pady=5)
ui_combo(click_tab, click_effect_single_preset_var, list(MOVEMENT_SINGLE_COLOR_PRESETS.keys()), width=220, command=mark_movement_color_pending).grid(row=7, column=1, sticky="w", padx=8, pady=5)
ui_label(click_tab, "Multi-colour preset:").grid(row=8, column=0, sticky="w", padx=8, pady=5)
click_effect_neon_combo = ui_combo(click_tab, click_effect_neon_preset_var, list(NEON_COLOR_PRESETS.keys()), width=220, command=mark_movement_color_pending)
click_effect_neon_combo.grid(row=8, column=1, sticky="w", padx=8, pady=5)
ui_button(click_tab, "Apply This Colour To All", lambda: apply_movement_color_to_all("click"), secondary=True, width=210).grid(row=8, column=2, padx=8, pady=5)
ui_button(click_tab, "Clear Click Effects", clear_click_effects, secondary=True, width=180).grid(row=9, column=0, padx=8, pady=7)
ui_label(click_tab, "Click Effects draw neon ripple rings and/or spark bursts on left and right mouse clicks. They are visual-only and do not change mouse behavior.", wraplength=720).grid(row=10, column=0, columnspan=4, sticky="w", padx=8, pady=5)

movement_actions_box = make_hscroll_section(movement_tab, "Movement Actions")
ui_button(movement_actions_box, "Apply Movement Settings", lambda: apply_movement_settings_from_ui(show_message=True), width=230).grid(row=0, column=0, padx=8, pady=7)
ui_button(movement_actions_box, "Clear Trail", clear_motion_trail, secondary=True, width=150).grid(row=0, column=1, padx=8, pady=7)
ui_button(movement_actions_box, "Clear Click Effects", clear_click_effects, secondary=True, width=180).grid(row=0, column=2, padx=8, pady=7)
ui_button(movement_actions_box, "Restore Movement Defaults", reset_movement_defaults_from_ui, danger=True, width=230).grid(row=0, column=3, padx=8, pady=7)

movement_summary_box = make_hscroll_section(movement_tab, "Current Movement Summary")
ui_label(movement_summary_box, textvariable=movement_summary_var, wraplength=720).pack(anchor="w", padx=8, pady=5)

# Presets tab
presets_tab = create_scrollable_tab(notebook, "Presets & Themes")

builtin_box = make_section(presets_tab, "Built-in Presets")
ui_label(builtin_box, "Built-in Preset:").grid(row=0, column=0, sticky="w", padx=8, pady=5)
builtin_combo = ui_combo(builtin_box, built_in_preset_var, list(BUILT_IN_PRESETS.keys()), width=220, command=lambda _value: on_builtin_changed())
builtin_combo.grid(row=0, column=1, sticky="w", padx=8, pady=5)
ui_button(builtin_box, "Load Built-in", load_builtin_preset).grid(row=0, column=2, padx=8, pady=5)
ui_label(builtin_box, "Preview:").grid(row=1, column=0, sticky="nw", padx=8, pady=(8, 5))
ui_label(builtin_box, textvariable=selected_builtin_preview_var, wraplength=680).grid(row=1, column=1, columnspan=3, sticky="w", padx=8, pady=(8, 5))

custom_box = make_section(presets_tab, "Custom Preset Slots")
ui_label(custom_box, "Custom Slot:").grid(row=1, column=0, sticky="w", padx=8, pady=5)
custom_combo = ui_combo(custom_box, custom_preset_slot_var, preset_slot_display_values(), width=240, command=lambda _value: on_custom_slot_changed())
custom_combo.grid(row=1, column=1, sticky="w", padx=8, pady=5)

ui_label(custom_box, "Preset name:").grid(row=2, column=0, sticky="w", padx=8, pady=5)
ui_entry(custom_box, custom_preset_name_var, width=300).grid(row=2, column=1, columnspan=2, sticky="w", padx=8, pady=5)

ui_button(custom_box, "Load", load_custom_preset).grid(row=3, column=0, padx=6, pady=7)
ui_button(custom_box, "Save Current", save_current_to_custom_slot).grid(row=3, column=1, padx=6, pady=7)
ui_button(custom_box, "Rename", rename_custom_preset, secondary=True).grid(row=3, column=2, padx=6, pady=7)
ui_button(custom_box, "Delete / Reset Slot", delete_custom_preset, danger=True, width=170).grid(row=3, column=3, padx=6, pady=7)
ui_button(custom_box, "Restore Saved Version", load_custom_preset, secondary=True, width=190).grid(row=4, column=0, columnspan=2, sticky="w", padx=6, pady=7)

ui_label(custom_box, "Preset Preview:").grid(row=5, column=0, sticky="nw", padx=8, pady=(8, 5))
ui_label(custom_box, textvariable=custom_preset_preview_var, wraplength=680).grid(row=5, column=1, columnspan=3, sticky="w", padx=8, pady=(8, 5))

preset_io_box = make_section(presets_tab, "Import / Export Presets")
ui_button(preset_io_box, "Export Selected Preset", export_selected_custom_preset, width=190).grid(row=0, column=0, padx=8, pady=7)
ui_button(preset_io_box, "Import Into Selected Slot", import_selected_custom_preset, width=200).grid(row=0, column=1, padx=8, pady=7)
ui_button(preset_io_box, "Export Full Backup", export_full_backup, secondary=True, width=180).grid(row=1, column=0, padx=8, pady=7)
ui_button(preset_io_box, "Import Full Backup", import_full_backup, secondary=True, width=180).grid(row=1, column=1, padx=8, pady=7)
ui_button(preset_io_box, "Reset All Custom Presets", reset_all_custom_presets, danger=True, width=210).grid(row=2, column=0, padx=8, pady=7)
ui_label(preset_io_box, "Full backup includes custom presets, themes, custom multi-colour presets, and app settings. Single preset import overwrites only the selected slot.", wraplength=700).grid(row=3, column=0, columnspan=3, sticky="w", padx=8, pady=5)

theme_box = make_section(presets_tab, "Full Cursor Themes")
ui_label(theme_box, "Theme Slot:").grid(row=0, column=0, sticky="w", padx=8, pady=5)
theme_combo = ui_combo(theme_box, theme_slot_var, theme_slot_display_values(), width=220, command=lambda _value: on_theme_slot_changed())
theme_combo.grid(row=0, column=1, sticky="w", padx=8, pady=5)
ui_label(theme_box, "Theme name:").grid(row=1, column=0, sticky="w", padx=8, pady=5)
ui_entry(theme_box, theme_name_var, width=300).grid(row=1, column=1, columnspan=2, sticky="w", padx=8, pady=5)
ui_button(theme_box, "Load Theme", load_selected_theme, width=150).grid(row=2, column=0, padx=6, pady=7)
ui_button(theme_box, "Save Current Theme", save_current_to_theme_slot, width=190).grid(row=2, column=1, padx=6, pady=7)
ui_button(theme_box, "Rename Theme", rename_selected_theme, secondary=True, width=170).grid(row=2, column=2, padx=6, pady=7)
ui_button(theme_box, "Delete / Reset Theme", delete_selected_theme, danger=True, width=190).grid(row=2, column=3, padx=6, pady=7)
ui_button(theme_box, "Export Theme", export_selected_theme, secondary=True, width=160).grid(row=3, column=0, padx=6, pady=7)
ui_button(theme_box, "Import Theme", import_selected_theme, secondary=True, width=160).grid(row=3, column=1, padx=6, pady=7)
ui_button(theme_box, "Reset All Themes", reset_all_custom_themes, danger=True, width=170).grid(row=3, column=2, padx=6, pady=7)
ui_label(theme_box, "Theme Preview:").grid(row=4, column=0, sticky="nw", padx=8, pady=(8, 5))
ui_label(theme_box, textvariable=theme_preview_var, wraplength=700).grid(row=4, column=1, columnspan=4, sticky="w", padx=8, pady=(8, 5))
ui_label(theme_box, "Themes save the full visual setup: Cursor Lab, animated cursor shape, idle effects, movement effects, colours, and performance options.", wraplength=720).grid(row=5, column=0, columnspan=5, sticky="w", padx=8, pady=5)

multi_colour_box = make_section(presets_tab, "Custom Multi-Colour Presets")
ui_label(multi_colour_box, "Custom Slot:").grid(row=0, column=0, sticky="w", padx=8, pady=5)
custom_multi_combo = ui_combo(multi_colour_box, custom_multi_slot_var, custom_multi_slot_display_values(), width=220, command=lambda _value: on_custom_multi_slot_changed())
custom_multi_combo.grid(row=0, column=1, sticky="w", padx=8, pady=5)
ui_checkbox(multi_colour_box, "Enable / show in dropdowns", custom_multi_enabled_var, lambda: None).grid(row=0, column=2, sticky="w", padx=8, pady=5)
ui_label(multi_colour_box, "Preset name:").grid(row=1, column=0, sticky="w", padx=8, pady=5)
ui_entry(multi_colour_box, custom_multi_name_var, width=300).grid(row=1, column=1, columnspan=2, sticky="w", padx=8, pady=5)
ui_label(multi_colour_box, "Colour 1:").grid(row=2, column=0, sticky="w", padx=8, pady=5)
ui_entry(multi_colour_box, custom_multi_color1_var, width=120).grid(row=2, column=1, sticky="w", padx=8, pady=5)
ui_button(multi_colour_box, "Pick 1", lambda: choose_custom_multi_colour(1), secondary=True, width=100).grid(row=2, column=2, sticky="w", padx=8, pady=5)
ui_label(multi_colour_box, "Colour 2:").grid(row=3, column=0, sticky="w", padx=8, pady=5)
ui_entry(multi_colour_box, custom_multi_color2_var, width=120).grid(row=3, column=1, sticky="w", padx=8, pady=5)
ui_button(multi_colour_box, "Pick 2", lambda: choose_custom_multi_colour(2), secondary=True, width=100).grid(row=3, column=2, sticky="w", padx=8, pady=5)
ui_label(multi_colour_box, "Colour 3:").grid(row=4, column=0, sticky="w", padx=8, pady=5)
ui_entry(multi_colour_box, custom_multi_color3_var, width=120).grid(row=4, column=1, sticky="w", padx=8, pady=5)
ui_button(multi_colour_box, "Pick 3", lambda: choose_custom_multi_colour(3), secondary=True, width=100).grid(row=4, column=2, sticky="w", padx=8, pady=5)
ui_button(multi_colour_box, "Save Custom Multi-Colour Preset", save_custom_multi_colour_slot, width=260).grid(row=5, column=0, padx=6, pady=7)
ui_button(multi_colour_box, "Use in Cursor Lab", use_custom_multi_colour_in_cursor_lab, secondary=True, width=180).grid(row=5, column=1, padx=6, pady=7)
ui_button(multi_colour_box, "Delete / Hide Slot", delete_custom_multi_colour_slot, danger=True, width=170).grid(row=5, column=2, padx=6, pady=7)
ui_button(multi_colour_box, "Export Multi-Colour Presets", export_custom_multi_colour_presets, secondary=True, width=230).grid(row=6, column=0, padx=6, pady=7)
ui_button(multi_colour_box, "Import Multi-Colour Presets", import_custom_multi_colour_presets, secondary=True, width=230).grid(row=6, column=1, padx=6, pady=7)
ui_button(multi_colour_box, "Reset Multi-Colour Presets", reset_all_custom_multi_colour_presets, danger=True, width=230).grid(row=6, column=2, padx=6, pady=7)
ui_label(multi_colour_box, "Preview:").grid(row=7, column=0, sticky="nw", padx=8, pady=(8, 5))
ui_label(multi_colour_box, textvariable=custom_multi_preview_var, wraplength=720).grid(row=7, column=1, columnspan=4, sticky="w", padx=8, pady=(8, 5))
ui_label(multi_colour_box, "Saved custom multi-colour presets appear anywhere Multi-Colour Neon Presets are used: cursor tint, idle glow, movement effects, and click effects.", wraplength=720).grid(row=8, column=0, columnspan=5, sticky="w", padx=8, pady=5)

def run_stability_check():
    """Run a lightweight safety/stability check without changing active effects."""
    checks = []
    warnings = []

    checks.append(f"App version: {APP_VERSION}")
    checks.append(f"App data folder: {APP_DIR}")
    checks.append(f"Cursor backups captured: {len(cursor_backups)}")
    checks.append(f"Transparent cursor currently active: {transparent_active}")
    checks.append(f"Cursor Lab replacement active: {cursor_lab_drawn_replacement_active()}")
    checks.append(f"Performance target overlay FPS: {PERFORMANCE_TARGET_FPS}")
    checks.append(f"Fake cursor count: {total_fake_cursor_count()}")
    checks.append(f"Custom multi-colour presets enabled: {sum(1 for cfg in custom_multi_colour_presets.values() if isinstance(cfg, dict) and cfg.get('enabled', False))}")
    checks.append(f"Full cursor theme slots: {len(custom_themes)}")

    if len(cursor_backups) == 0:
        warnings.append("No system cursor backups are available. Restart CursorSwarm before using strong modes.")

    try:
        APP_DIR.mkdir(parents=True, exist_ok=True)
        probe_file = APP_DIR / "cursor_swarm_write_test.tmp"
        probe_file.write_text("ok", encoding="utf-8")
        probe_file.unlink(missing_ok=True)
        checks.append("App data folder write test: OK")
    except Exception as exc:
        warnings.append(f"App data folder write test failed: {exc}")

    for json_name, json_file in [
        ("settings", SETTINGS_FILE),
        ("custom presets", PRESET_FILE),
        ("custom themes", THEME_FILE),
        ("custom multi-colour presets", COLOR_PRESET_FILE),
    ]:
        if json_file.exists() and read_json_file_safely(json_file, default_value=None, backup_broken=False) is None:
            warnings.append(f"{json_name} JSON file looks invalid. Restart will use safe defaults unless repaired.")
        else:
            checks.append(f"{json_name} JSON: OK")

    if not RESTORE_SCRIPT_FILE.exists():
        warnings.append("Fallback restore script is missing. Use Generate Fallback Restore Script if needed.")
    else:
        checks.append("Fallback restore script: present")

    if RESTORE_EXE_FILE.exists():
        checks.append("Standalone restore EXE: present")
    else:
        checks.append("Standalone restore EXE: not found in this dev/source folder")

    for doc_name, doc_path in [
        ("README", README_FILE),
        ("Privacy Policy", PRIVACY_POLICY_FILE),
        ("Terms/Safety", TERMS_SAFETY_FILE),
        ("Release Notes", RELEASE_NOTES_FILE),
    ]:
        if Path(doc_path).exists():
            checks.append(f"{doc_name}: present")
        else:
            warnings.append(f"{doc_name} document is missing. It should be regenerated before packaging.")

    if CURSOR_TINT_BLACK_OUTLINE and CURSOR_TINT_OUTLINE_THICKNESS > 4:
        warnings.append("Very thick outline is enabled; 1-3px usually looks cleaner.")

    if PERFORMANCE_TARGET_FPS > 45 and not PERFORMANCE_REDUCE_GLOW_QUALITY:
        checks.append("Tip: Battery Saver Glow Mode can reduce drawing work on battery.")

    result = "CursorSwarm stability check completed."
    if warnings:
        result += "\n\nWarnings / notes:\n- " + "\n- ".join(warnings)
    else:
        result += "\n\nNo major issues found."

    result += "\n\nChecks:\n- " + "\n- ".join(checks)
    safe_messagebox_showinfo("CursorSwarm Stability Check", result)


# Safety tab
safety_tab = create_scrollable_tab(notebook, "Safety")

panic_box = make_section(safety_tab, "Emergency Actions")
safety_panic_toggle_button = ui_button(panic_box, "BIG SAFE MODE / PANIC", panic_resume_toggle, danger=True, width=210)
safety_panic_toggle_button.grid(row=0, column=0, padx=8, pady=7)
ui_button(panic_box, "Resume Previous", resume_previous_mode, secondary=True, width=170).grid(row=2, column=0, padx=8, pady=7)
ui_button(panic_box, "Restore Cursor", ui_restore_cursor).grid(row=0, column=1, padx=8, pady=7)
ui_button(panic_box, "Disable Mirror", ui_disable_mirror, secondary=True).grid(row=0, column=2, padx=8, pady=7)
ui_button(panic_box, "Show Drawn-Real", ui_show_drawn_real).grid(row=1, column=0, padx=8, pady=7)
ui_button(panic_box, "Pause Swarm", ui_pause_swarm, secondary=True).grid(row=1, column=1, padx=8, pady=7)
ui_button(panic_box, "Quit Safely", restore_and_quit, danger=True).grid(row=1, column=2, padx=8, pady=7)
ui_button(panic_box, "Run Stability Check", run_stability_check, secondary=True, width=190).grid(row=2, column=1, padx=8, pady=7)

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
ui_label(hotkey_box, hotkey_text, wraplength=700).pack(anchor="w", padx=8, pady=5)

safety_options_box = make_section(safety_tab, "Display Options")
ui_checkbox(safety_options_box, "Show runtime HUD", runtime_hud_var, ui_toggle_runtime_hud).grid(row=0, column=0, sticky="w", padx=8, pady=5)
ui_checkbox(safety_options_box, "Show startup help text", startup_help_var, ui_toggle_startup_help).grid(row=1, column=0, sticky="w", padx=8, pady=5)

startup_box = make_section(safety_tab, "Startup / Recovery")
ui_label(startup_box, "Startup Mode:").grid(row=0, column=0, sticky="w", padx=8, pady=5)
startup_mode_combo = ui_combo(startup_box, startup_mode_var, STARTUP_MODE_OPTIONS, width=220)
startup_mode_combo.grid(row=0, column=1, sticky="w", padx=8, pady=5)

ui_label(startup_box, "Built-in Startup Preset:").grid(row=1, column=0, sticky="w", padx=8, pady=5)
startup_builtin_combo = ui_combo(startup_box, startup_builtin_var, list(BUILT_IN_PRESETS.keys()), width=220)
startup_builtin_combo.grid(row=1, column=1, sticky="w", padx=8, pady=5)

ui_label(startup_box, "Custom Startup Slot:").grid(row=2, column=0, sticky="w", padx=8, pady=5)
startup_custom_combo = ui_combo(startup_box, startup_custom_slot_var, preset_slot_display_values(), width=220)
startup_custom_combo.grid(row=2, column=1, sticky="w", padx=8, pady=5)

ui_label(startup_box, "Theme Startup Slot:").grid(row=3, column=0, sticky="w", padx=8, pady=5)
startup_theme_combo = ui_combo(startup_box, startup_theme_slot_var, theme_slot_display_values(), width=220)
startup_theme_combo.grid(row=3, column=1, sticky="w", padx=8, pady=5)

ui_button(startup_box, "Save Startup Settings", ui_save_startup_settings, width=190).grid(row=4, column=0, padx=8, pady=7)
ui_button(startup_box, "Apply Startup Mode Now", ui_apply_startup_now, secondary=True, width=205).grid(row=4, column=1, padx=8, pady=7)
ui_button(startup_box, "Generate Fallback Restore Script", generate_emergency_restore_script, secondary=True, width=260).grid(row=5, column=0, columnspan=2, sticky="w", padx=8, pady=7)
ui_label(startup_box, "Fresh Safe Defaults starts visible and safe. Last Used Settings restores the last safely saved state. Selected Theme loads a saved full cursor theme on startup.", wraplength=700).grid(row=6, column=0, columnspan=3, sticky="w", padx=8, pady=5)

# Advanced tab
advanced_tab = create_scrollable_tab(notebook, "Advanced")

advanced_box = make_section(advanced_tab, "Debug Info")
advanced_info_var = tk.StringVar(value="Debug info will update while the app is running.")
ui_label(advanced_box, textvariable=advanced_info_var, wraplength=720).pack(anchor="w", padx=8, pady=5)

about_box = make_section(advanced_tab, "App Info / About")
about_text = (
    f"Cursor Swarm {APP_VERSION}\n"
    "v13.12 is a final polish/release-prep checkpoint for the current stable v13 feature set.\n\n"
    "Main hotkeys:\n"
    "Ctrl+Alt+C = Control Panel\n"
    "Ctrl+Alt+Space = Safe Mode / Resume\n"
    "Ctrl+Alt+Q = Quit Safely\n\n"
    "Privacy summary: CursorSwarm stores settings locally and does not collect, upload, sell, or share personal data.\n\n"
    f"Preset file: {PRESET_FILE}\n"
    f"Theme file: {THEME_FILE}\n"
    f"Settings file: {SETTINGS_FILE}\n"
    f"Emergency restore EXE: {RESTORE_EXE_FILE}\n"
    f"Fallback restore script: {RESTORE_SCRIPT_FILE}\n"
    f"README file: {README_FILE}\n"
    f"Privacy policy: {PRIVACY_POLICY_FILE}\n"
    f"Terms / Safety: {TERMS_SAFETY_FILE}\n"
    f"Release notes: {RELEASE_NOTES_FILE}"
)
ui_label(about_box, about_text, wraplength=720).pack(anchor="w", padx=8, pady=5)

config_box = make_section(advanced_tab, "Config / Backup")
ui_label(
    config_box,
    f"Preset file: {PRESET_FILE}\nTheme file: {THEME_FILE}\nSettings file: {SETTINGS_FILE}\nEmergency restore EXE: {RESTORE_EXE_FILE}\nFallback restore script: {RESTORE_SCRIPT_FILE}\nREADME file: {README_FILE}\nPrivacy policy: {PRIVACY_POLICY_FILE}\nTerms / Safety: {TERMS_SAFETY_FILE}\nRelease notes: {RELEASE_NOTES_FILE}",
    wraplength=720,
).grid(row=0, column=0, columnspan=3, sticky="w", padx=8, pady=5)
ui_button(config_box, "Export Full Backup", export_full_backup, width=180).grid(row=1, column=0, padx=8, pady=7)
ui_button(config_box, "Import Full Backup", import_full_backup, width=180).grid(row=1, column=1, padx=8, pady=7)
ui_button(config_box, "Reset App Settings", reset_app_settings_to_default, secondary=True, width=180).grid(row=2, column=0, padx=8, pady=7)
ui_button(config_box, "Reset Custom Presets", reset_all_custom_presets, danger=True, width=190).grid(row=2, column=1, padx=8, pady=7)
ui_button(config_box, "Reset Custom Themes", reset_all_custom_themes, danger=True, width=190).grid(row=2, column=2, padx=8, pady=7)
ui_button(config_box, "Reset Multi-Colour Presets", reset_all_custom_multi_colour_presets, danger=True, width=230).grid(row=3, column=0, padx=8, pady=7)
ui_button(config_box, "Generate Fallback Restore Script", generate_emergency_restore_script, secondary=True, width=260).grid(row=3, column=1, sticky="w", padx=8, pady=7)
ui_button(config_box, "Create README", generate_readme_file, secondary=True).grid(row=3, column=2, sticky="w", padx=8, pady=7)
ui_button(config_box, "Create Privacy Policy", generate_privacy_policy_file, secondary=True, width=185).grid(row=4, column=0, sticky="w", padx=8, pady=7)
ui_button(config_box, "Create Terms/Safety", generate_terms_safety_file, secondary=True, width=185).grid(row=4, column=1, sticky="w", padx=8, pady=7)
ui_button(config_box, "Create Release Notes", generate_release_notes_file, secondary=True, width=185).grid(row=4, column=2, sticky="w", padx=8, pady=7)

setup_main_tab_navigation()

# Bottom action bar
bottom_frame = ctk.CTkFrame(control_panel, fg_color="#0f172a", corner_radius=0)
bottom_frame.pack(fill="x", padx=0, pady=0)
ui_button(bottom_frame, "Apply Changes", apply_all_changes).pack(side="left", padx=(16, 6), pady=12)
ui_button(bottom_frame, "Restore Preset", load_custom_preset, secondary=True).pack(side="left", padx=6, pady=12)
bottom_panic_toggle_button = ui_button(bottom_frame, "Safe Mode", panic_resume_toggle, danger=True, width=170)
bottom_panic_toggle_button.pack(side="left", padx=6, pady=12)
ui_button(bottom_frame, "Resume Previous", resume_previous_mode, secondary=True, width=160).pack(side="left", padx=6, pady=12)
ui_button(bottom_frame, "Hide Panel", hide_control_panel, secondary=True, width=120).pack(side="right", padx=6, pady=12)
ui_button(bottom_frame, "Quit Safely", restore_and_quit, danger=True, width=120).pack(side="right", padx=(6, 16), pady=12)

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
    global native_dialog_open, last_motion_time, current_cursor_animation_frame_index
    global performance_last_real_motion_time, performance_long_idle_is_active, motion_trail_runtime_images

    now = time.time()
    dt = now - last_time
    last_time = now

    dt = min(dt, 0.035)

    if CURSOR_SHAPE_MODE in CURSOR_SHAPE_ANIMATED:
        try:
            current_cursor_animation_frame_index = int(now / max(0.03, CURSOR_ANIMATION_SPEED))
        except Exception:
            current_cursor_animation_frame_index = 0
    else:
        current_cursor_animation_frame_index = 0

    if native_dialog_open:
        try:
            canvas.delete("all")
        except Exception:
            pass
        root.after(get_performance_frame_delay_ms(), update)
        return

    real_x, real_y = get_mouse_position()

    real_dx = real_x - prev_real_x
    real_dy = real_y - prev_real_y

    real_distance = math.hypot(real_dx, real_dy)
    moving = real_distance > MOVE_DISTANCE_THRESHOLD

    if moving:
        last_motion_time = now

    update_performance_idle_timer(real_distance, now)

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
        if cursor_lab_drawn_replacement_active():
            show_drawn_real_cursor = True
            show_control_panel_hint(
                "Drawn cursor is locked on while Cursor Lab replacement mode is active.",
                duration=5.0,
            )
        else:
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

    enforce_cursor_lab_replacement_visibility()

    canvas.delete("all")
    motion_trail_runtime_images = []

    long_idle_active_now = performance_long_idle_active(now)
    long_idle_swarm_hidden = bool(PERFORMANCE_PAUSE_SWARM_ON_LONG_IDLE and long_idle_active_now)
    long_idle_idle_effects_paused = bool(PERFORMANCE_PAUSE_IDLE_EFFECTS_ON_LONG_IDLE and long_idle_active_now)

    if long_idle_idle_effects_paused:
        idle_state = {
            "idle_active": False,
            "style": "Disabled",
            "pulse_scale": 1.0,
            "wobble_x": 0.0,
            "wobble_y": 0.0,
            "alpha_factor": 1.0,
            "strength": 0.0,
            "delay": IDLE_EFFECT_DELAY,
        }
    else:
        idle_state = get_idle_effect_state(now, moving)
    draw_items = []
    click_center_x = float(real_x)
    click_center_y = float(real_y)
    trail_draw_items = build_motion_trail_draw_items(now)
    speed_glow_value = speed_glow_intensity(real_distance, dt)
    motion_streak_value = motion_streak_intensity(real_distance, dt)
    spark_particle_value = spark_particle_intensity(real_distance, dt)
    ripple_burst_value = ripple_burst_intensity(real_distance, dt)
    speed_lines_value = speed_lines_intensity(real_distance, dt)
    magnetic_orbit_value = magnetic_orbit_intensity(real_distance, dt)

    effective_show_fake_cursors = show_fake_cursors and nightmare_mode != "Blind Mode"

    if effective_show_fake_cursors and not swarm_paused:
        if not long_idle_swarm_hidden:
            for cursor in fake_cursors:
                cursor.update(moving, real_dx, real_dy, dt)
                draw_items.append((cursor.x, cursor.y, cursor.scale * FAKE_CURSOR_SCALE_MULTIPLIER, "fake"))
        # When fake-cursor long-idle hiding is active, skip drawing the fake swarm entirely.
        # This makes the power-saving state obvious and reduces overlay work.

    # Drawn-real cursor
    # Ctrl + Alt + H toggles this.
    # Hold Shift temporarily shows it for safety/hint mode.
    flicker_hint_active = (
        nightmare_mode == "Flicker Hint Mode"
        and ((now - start_time) % NIGHTMARE_FLICKER_INTERVAL) < NIGHTMARE_FLICKER_DURATION
    )
    idle_effect_visual_active = bool(
        IDLE_EFFECT_ENABLED
        and IDLE_EFFECT_STYLE != "Disabled"
        and not long_idle_idle_effects_paused
        and idle_state.get("idle_active")
    )

    should_draw_real_cursor = (
        cursor_lab_drawn_replacement_active()
        or idle_effect_visual_active
        or key_down(VK_SHIFT)
        or flicker_hint_active
        or (nightmare_mode == "Disabled" and show_drawn_real_cursor)
    )

    if should_draw_real_cursor:
        drawn_scale = REAL_DRAWN_CURSOR_SCALE * idle_state.get("pulse_scale", 1.0)
        real_draw_x = real_x - (hotspot_x * drawn_scale) + manual_offset_x + idle_state.get("wobble_x", 0.0)
        real_draw_y = real_y - (hotspot_y * drawn_scale) + manual_offset_y + idle_state.get("wobble_y", 0.0)
        current_source_image, _current_hotspot_x, _current_hotspot_y, _current_render_key = get_current_cursor_source_image_and_hotspot()
        drawn_width = current_source_image.width * drawn_scale
        drawn_height = current_source_image.height * drawn_scale
        click_center_x = real_draw_x + drawn_width / 2
        click_center_y = real_draw_y + drawn_height / 2

        if speed_lines_value > 0.02:
            draw_speed_lines(real_draw_x, real_draw_y, drawn_width, drawn_height, real_dx, real_dy, speed_lines_value, now)

        if motion_streak_value > 0.02:
            draw_motion_streak(real_draw_x, real_draw_y, drawn_width, drawn_height, real_dx, real_dy, motion_streak_value, now)

        if speed_glow_value > 0.02:
            draw_speed_glow(real_draw_x, real_draw_y, drawn_width, drawn_height, speed_glow_value, now)

        if magnetic_orbit_value > 0.02:
            draw_magnetic_orbit(real_draw_x, real_draw_y, drawn_width, drawn_height, magnetic_orbit_value, now)

        if idle_state.get("idle_active") and idle_state.get("style") == "Glow Ring":
            draw_idle_glow_ring(real_draw_x, real_draw_y, drawn_width, drawn_height, now, idle_state.get("strength", 0.55))

        if spark_particle_value > 0.02:
            spawn_spark_particles(real_draw_x + drawn_width / 2, real_draw_y + drawn_height / 2, real_dx, real_dy, spark_particle_value, now)
        if ripple_burst_value > 0.02:
            spawn_ripple_burst(real_draw_x + drawn_width / 2, real_draw_y + drawn_height / 2, ripple_burst_value, now)

        add_motion_trail_point(real_draw_x, real_draw_y, drawn_scale, now, moving)
        draw_items.append((real_draw_x, real_draw_y, drawn_scale, "drawn", idle_state.get("alpha_factor", 1.0)))
    elif movement_effects_active():
        # Movement trail can still work behind the normal Windows cursor even if
        # Cursor Lab replacement mode is not active.
        drawn_scale = REAL_DRAWN_CURSOR_SCALE
        real_draw_x = real_x - (hotspot_x * drawn_scale) + manual_offset_x
        real_draw_y = real_y - (hotspot_y * drawn_scale) + manual_offset_y
        current_source_image, _current_hotspot_x, _current_hotspot_y, _current_render_key = get_current_cursor_source_image_and_hotspot()
        drawn_width = current_source_image.width * drawn_scale
        drawn_height = current_source_image.height * drawn_scale
        click_center_x = real_draw_x + drawn_width / 2
        click_center_y = real_draw_y + drawn_height / 2
        if speed_lines_value > 0.02:
            draw_speed_lines(real_draw_x, real_draw_y, drawn_width, drawn_height, real_dx, real_dy, speed_lines_value, now)
        if motion_streak_value > 0.02:
            draw_motion_streak(real_draw_x, real_draw_y, drawn_width, drawn_height, real_dx, real_dy, motion_streak_value, now)
        if speed_glow_value > 0.02:
            draw_speed_glow(real_draw_x, real_draw_y, drawn_width, drawn_height, speed_glow_value, now)
        if magnetic_orbit_value > 0.02:
            draw_magnetic_orbit(real_draw_x, real_draw_y, drawn_width, drawn_height, magnetic_orbit_value, now)
        if spark_particle_value > 0.02:
            spawn_spark_particles(real_draw_x + drawn_width / 2, real_draw_y + drawn_height / 2, real_dx, real_dy, spark_particle_value, now)
        if ripple_burst_value > 0.02:
            spawn_ripple_burst(real_draw_x + drawn_width / 2, real_draw_y + drawn_height / 2, ripple_burst_value, now)
        add_motion_trail_point(real_draw_x, real_draw_y, drawn_scale, now, moving)

    if RANDOMIZE_DRAW_ORDER:
        random.shuffle(draw_items)

    update_click_effect_detection(click_center_x, click_center_y, now)
    draw_comet_tail(now)
    draw_ripple_bursts(now)
    draw_click_effects(now)
    draw_spark_particles(now)

    for item in trail_draw_items:
        x, y, scale, role, alpha_factor = item
        draw_cursor_image(x, y, scale, role, alpha_factor=alpha_factor)

    for item in draw_items:
        if len(item) == 5:
            x, y, scale, role, alpha_factor = item
        else:
            x, y, scale, role = item
            alpha_factor = 1.0
        draw_cursor_image(x, y, scale, role, alpha_factor=alpha_factor)

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
            text="CursorSwarm v13.12 — Ctrl+Alt+C panel | Ctrl+Alt+Space Safe Mode | Ctrl+Alt+Q Quit Safely",
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
        idle_runtime = f"Idle:{IDLE_EFFECT_STYLE}" if IDLE_EFFECT_ENABLED and IDLE_EFFECT_STYLE != "Disabled" else "Idle:OFF"
        movement_runtime = f"Move:{MOVEMENT_EFFECT_STYLE}" if movement_effects_active() else "Move:OFF"
        hud_text = (
            f"Preset: {CURRENT_PRESET_NAME} | Cursor: {transparent_text} | "
            f"Mirror: {mirror_text} | Swarm: {pause_text} | "
            f"Fake: {fake_text} | RealDrawn: {drawn_real_text} | Nightmare: {nightmare_text} | {idle_runtime} | {movement_runtime}"
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
        f"Performance: {PERFORMANCE_MODE} at {PERFORMANCE_TARGET_FPS} FPS | Glow reduced: {PERFORMANCE_REDUCE_GLOW_QUALITY} | Hide fake after idle: {PERFORMANCE_PAUSE_SWARM_ON_LONG_IDLE} | Pause idle effects: {PERFORMANCE_PAUSE_IDLE_EFFECTS_ON_LONG_IDLE}\\n"
        f"Startup help text: {show_startup_help}\\n"
        f"Startup mode: {app_settings.get('startup_mode', 'Safe Mode')}\\n"
        f"Settings file: {SETTINGS_FILE}\\n"
        f"Panic state saved: {pre_panic_state is not None}\\n"
        f"Fake cursor total: {total_fake_cursor_count()}\\n"
        f"Counts: static {STATIC_COUNT}, slow {SLOW_CLONE_COUNT}, same {SAME_SPEED_CLONE_COUNT}, fast {FAST_CLONE_COUNT}, random {RANDOM_MOVER_COUNT}, target {TARGET_MOVER_COUNT}\\n"
        f"Movement threshold: {MOVE_DISTANCE_THRESHOLD:.2f}\\n"
        f"Nightmare mode: {nightmare_mode}"
    )

    root.after(get_performance_frame_delay_ms(), update)

try:
    update()
    root.mainloop()
finally:
    restore_cursors_safely()