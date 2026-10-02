from __future__ import annotations

import configparser
import ctypes
import locale
import os
import platform
import subprocess
import shutil
import sys
import threading
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

from PyQt5.QtCore import QThread, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QFontMetrics, QIcon, QPalette
from PyQt5.QtWidgets import (
    QAction,
    QActionGroup,
    QAbstractItemView,
    QApplication,
    QComboBox,
    QDialog,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QStyleFactory,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

APP_NAME = "ECOMTECH Boot Fixer"
APP_VERSION = "1.3.3"
LOCALE = "en-US"
DEFAULT_THEME_CODE = "light"
THEME_ORDER = ("light", "dark", "blue", "purple", "red", "orange", "classic")

THEME_OPTIONS = {
    "light": {
        "label": "LIGHT", "window": "#f3f6fa", "panel": "#ffffff", "panel_alt": "#f8fafc",
        "surface": "#e8eef5", "surface_hover": "#dce6f1", "surface_pressed": "#cbd8e6",
        "input": "#ffffff", "text": "#17202a", "muted": "#5f6b7a", "border": "#c4cfdb",
        "border_strong": "#9eacbc", "accent": "#2563eb", "accent_hover": "#1d4ed8",
        "accent_pressed": "#1e40af", "accent_text": "#ffffff", "tab_selected": "#dbeafe",
        "header": "#e5ebf2", "selection": "#2563eb", "disabled_bg": "#e5e9ef",
        "disabled_text": "#8a94a3", "menu": "#ffffff", "scroll_bg": "#e7ecf2",
        "scroll_handle": "#aab5c2", "tooltip": "#1f2937", "tooltip_text": "#ffffff",
        "danger": "#c62828", "success": "#2e7d32", "warning": "#b26a00", "neutral": "#657384",
        "radius": "4px", "group_radius": "6px",
    },
    "dark": {
        "label": "DARK", "window": "#0f141a", "panel": "#111820", "panel_alt": "#111a23",
        "surface": "#263445", "surface_hover": "#32455c", "surface_pressed": "#1c2938",
        "input": "#0b1117", "text": "#e6edf3", "muted": "#aeb8c4", "border": "#364250",
        "border_strong": "#4d6075", "accent": "#1f6feb", "accent_hover": "#3d8bfd",
        "accent_pressed": "#1557b0", "accent_text": "#ffffff", "tab_selected": "#243447",
        "header": "#1b2735", "selection": "#1f6feb", "disabled_bg": "#121820",
        "disabled_text": "#697586", "menu": "#161d26", "scroll_bg": "#10171f",
        "scroll_handle": "#3b4858", "tooltip": "#243447", "tooltip_text": "#ffffff",
        "danger": "#b4232c", "success": "#238636", "warning": "#9e6a03", "neutral": "#46515f",
        "radius": "4px", "group_radius": "6px",
    },
    "blue": {
        "label": "BLUE", "window": "#071522", "panel": "#0b1d2e", "panel_alt": "#0d2438",
        "surface": "#123653", "surface_hover": "#194b70", "surface_pressed": "#0c2941",
        "input": "#06111c", "text": "#e8f4ff", "muted": "#a9c5dc", "border": "#24506f",
        "border_strong": "#39769e", "accent": "#2196f3", "accent_hover": "#42a5f5",
        "accent_pressed": "#1475bd", "accent_text": "#ffffff", "tab_selected": "#154365",
        "header": "#10304a", "selection": "#1976d2", "disabled_bg": "#10202e",
        "disabled_text": "#66859d", "menu": "#0d2335", "scroll_bg": "#091a28",
        "scroll_handle": "#2c5f82", "tooltip": "#16466a", "tooltip_text": "#ffffff",
        "danger": "#c0394b", "success": "#168f63", "warning": "#aa7700", "neutral": "#41657c",
        "radius": "4px", "group_radius": "6px",
    },
    "purple": {
        "label": "PURPLE", "window": "#160f21", "panel": "#1d142b", "panel_alt": "#241833",
        "surface": "#44265f", "surface_hover": "#593278", "surface_pressed": "#351d4b",
        "input": "#100b18", "text": "#f2eaff", "muted": "#c6afd8", "border": "#5b3a70",
        "border_strong": "#7b5293", "accent": "#9c4dcc", "accent_hover": "#b264df",
        "accent_pressed": "#75369f", "accent_text": "#ffffff", "tab_selected": "#4a2864",
        "header": "#342047", "selection": "#8e44ad", "disabled_bg": "#21172c",
        "disabled_text": "#826d92", "menu": "#21162f", "scroll_bg": "#180f22",
        "scroll_handle": "#654079", "tooltip": "#4b2963", "tooltip_text": "#ffffff",
        "danger": "#bd334f", "success": "#2b8f68", "warning": "#a76c00", "neutral": "#63506f",
        "radius": "4px", "group_radius": "6px",
    },
    "red": {
        "label": "RED", "window": "#1b0d10", "panel": "#241115", "panel_alt": "#2c151a",
        "surface": "#5a252d", "surface_hover": "#74313b", "surface_pressed": "#461b22",
        "input": "#13090b", "text": "#fff0f1", "muted": "#d9afb4", "border": "#71343d",
        "border_strong": "#934955", "accent": "#e53935", "accent_hover": "#ef5350",
        "accent_pressed": "#b71c1c", "accent_text": "#ffffff", "tab_selected": "#612832",
        "header": "#451e25", "selection": "#d32f2f", "disabled_bg": "#281417",
        "disabled_text": "#926d72", "menu": "#291317", "scroll_bg": "#1c0d10",
        "scroll_handle": "#74323b", "tooltip": "#642a33", "tooltip_text": "#ffffff",
        "danger": "#d32f2f", "success": "#2e7d55", "warning": "#a96e00", "neutral": "#715158",
        "radius": "4px", "group_radius": "6px",
    },
    "orange": {
        "label": "ORANGE", "window": "#1a120a", "panel": "#24180d", "panel_alt": "#2c1d10",
        "surface": "#5b3818", "surface_hover": "#754a20", "surface_pressed": "#462a12",
        "input": "#120c07", "text": "#fff4e8", "muted": "#d7b997", "border": "#714823",
        "border_strong": "#966234", "accent": "#f57c00", "accent_hover": "#fb8c00",
        "accent_pressed": "#c65f00", "accent_text": "#ffffff", "tab_selected": "#633d1a",
        "header": "#472c14", "selection": "#ef6c00", "disabled_bg": "#281b10",
        "disabled_text": "#92785e", "menu": "#291b0f", "scroll_bg": "#1c1209",
        "scroll_handle": "#76502c", "tooltip": "#68401b", "tooltip_text": "#ffffff",
        "danger": "#c43b32", "success": "#2d8756", "warning": "#d87800", "neutral": "#715d49",
        "radius": "4px", "group_radius": "6px",
    },
    "classic": {
        "label": "CLASSIC", "window": "#d4d0c8", "panel": "#ece9d8", "panel_alt": "#f5f3e8",
        "surface": "#ece9d8", "surface_hover": "#f7f5ec", "surface_pressed": "#c8c4bb",
        "input": "#ffffff", "text": "#000000", "muted": "#404040", "border": "#9a9a9a",
        "border_strong": "#6f6f6f", "accent": "#0a64ad", "accent_hover": "#1976bd",
        "accent_pressed": "#064b82", "accent_text": "#ffffff", "tab_selected": "#ffffff",
        "header": "#d4d0c8", "selection": "#0a64ad", "disabled_bg": "#d4d0c8",
        "disabled_text": "#777777", "menu": "#ece9d8", "scroll_bg": "#d4d0c8",
        "scroll_handle": "#a0a0a0", "tooltip": "#ffffe1", "tooltip_text": "#000000",
        "danger": "#b00020", "success": "#2e7d32", "warning": "#9a6100", "neutral": "#777777",
        "radius": "1px", "group_radius": "2px",
    },
}


def get_theme_config(theme_code: str | None = None) -> dict[str, str]:
    code = str(theme_code or DEFAULT_THEME_CODE).strip().lower()
    return THEME_OPTIONS.get(code, THEME_OPTIONS[DEFAULT_THEME_CODE])


def build_theme_stylesheet(theme_code: str | None = None) -> str:
    code = str(theme_code or DEFAULT_THEME_CODE).strip().lower()
    p = get_theme_config(code)
    arrow_tone = "dark" if code in {"light", "classic"} else "light"
    icon_dir = RESOURCE_DIR / "icons"
    down_arrow = (icon_dir / f"arrow_down_{arrow_tone}.png").as_posix()
    up_arrow = (icon_dir / f"arrow_up_{arrow_tone}.png").as_posix()
    return f"""
        QWidget {{ color: {p['text']}; background-color: transparent; font-family: 'Segoe UI'; font-size: 7pt; }}
        QMainWindow, QDialog {{ background-color: {p['window']}; color: {p['text']}; }}
        QMainWindow > QWidget, QTabWidget {{ background-color: {p['window']}; }}
        QMenuBar {{ background-color: {p['menu']}; color: {p['text']}; border-bottom: 1px solid {p['border']}; }}
        QMenuBar::item {{ background-color: {p['menu']}; padding: 3px 6px; }}
        QMenuBar::item:selected, QMenu::item:selected {{ background-color: {p['surface_hover']}; color: {p['text']}; }}
        QMenu {{ background-color: {p['menu']}; color: {p['text']}; border: 1px solid {p['border_strong']}; padding: 3px; }}
        QMenu::item {{ padding: 4px 18px 4px 7px; }}
        QMenu::separator {{ height: 1px; background-color: {p['border']}; margin: 4px 7px; }}
        QTabWidget::pane {{ border: 1px solid {p['border']}; background-color: {p['window']}; }}
        QTabBar::tab {{ min-width: 100px; background-color: {p['menu']}; color: {p['muted']}; border: 1px solid {p['border']}; padding: 5px 10px; margin-right: 1px; font-weight: 600; }}
        QTabBar::tab:selected {{ background-color: {p['tab_selected']}; color: {p['text']}; border-bottom: 2px solid {p['accent']}; }}
        QTabBar::tab:hover:!selected {{ background-color: {p['surface_hover']}; color: {p['text']}; border-color: {p['accent']}; }}
        #panel, #statusCard, #actionCard {{ background-color: {p['panel']}; border: 1px solid {p['border']}; border-radius: {p['group_radius']}; }}
        #statusCard[locked='true'] {{ background-color: {p['surface']}; border-style: dashed; }}
        #appTitle {{ color: {p['accent']}; font-size: 11pt; font-weight: 700; }}
        #appSubtitle, #pageDescription, #statusDetail, #actionDescription {{ color: {p['muted']}; }}
        #pageTitle {{ color: {p['text']}; font-size: 10pt; font-weight: 700; }}
        #statusCard[state='ok'] {{ border-left: 4px solid {p['success']}; }}
        #statusCard[state='warn'] {{ border-left: 4px solid {p['warning']}; }}
        #statusCard[state='error'] {{ border-left: 4px solid {p['danger']}; }}
        #statusCard[state='locked'] {{ border-left: 4px solid {p['neutral']}; }}
        #statusTitle, #fieldLabel, #sectionTitle {{ color: {p['muted']}; font-weight: 600; }}
        #statusValue {{ color: {p['text']}; font-size: 8pt; font-weight: 700; }}
        #statusCard[locked='true'] #statusValue {{ color: {p['neutral']}; }}
        #actionTitle {{ color: {p['text']}; font-size: 8pt; font-weight: 700; }}
        #warningPanel {{ background-color: {p['panel_alt']}; border: 1px solid {p['warning']}; border-radius: {p['group_radius']}; }}
        #warningTitle {{ color: {p['warning']}; font-weight: 700; }}
        #warningText {{ color: {p['text']}; }}
        #adminBadge, #localeBadge {{ padding: 3px 8px; border: 1px solid {p['border_strong']}; border-radius: {p['radius']}; font-weight: 600; background-color: {p['surface']}; }}
        #adminBadge[state='ok'] {{ color: {p['success']}; }}
        #adminBadge[state='warn'] {{ color: {p['warning']}; }}
        QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QListWidget, QTreeWidget {{ min-height: 20px; padding: 2px 5px; border: 1px solid {p['border_strong']}; border-radius: {p['radius']}; background-color: {p['input']}; color: {p['text']}; selection-background-color: {p['selection']}; selection-color: {p['accent_text']}; }}
        QComboBox {{ padding-right: 32px; }}
        QComboBox::drop-down {{ subcontrol-origin: padding; subcontrol-position: top right; width: 27px; border-left: 1px solid {p['border']}; background-color: {p['surface']}; }}
        QComboBox::drop-down:hover {{ background-color: {p['surface_hover']}; }}
        QComboBox::down-arrow {{ image: url("{down_arrow}"); width: 11px; height: 11px; }}
        QComboBox QAbstractItemView {{ background-color: {p['panel']}; color: {p['text']}; border: 1px solid {p['border_strong']}; selection-background-color: {p['selection']}; selection-color: {p['accent_text']}; }}
        QSpinBox, QDoubleSpinBox {{ padding-right: 29px; }}
        QSpinBox::up-button, QDoubleSpinBox::up-button {{ subcontrol-origin: border; subcontrol-position: top right; width: 25px; height: 13px; border-left: 1px solid {p['border']}; border-bottom: 1px solid {p['border']}; background-color: {p['surface']}; }}
        QSpinBox::down-button, QDoubleSpinBox::down-button {{ subcontrol-origin: border; subcontrol-position: bottom right; width: 25px; height: 13px; border-left: 1px solid {p['border']}; background-color: {p['surface']}; }}
        QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover, QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{ background-color: {p['surface_hover']}; }}
        QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{ image: url("{up_arrow}"); width: 9px; height: 9px; }}
        QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{ image: url("{down_arrow}"); width: 9px; height: 9px; }}
        QPushButton, QToolButton {{ min-height: 21px; padding: 2px 7px; border: 1px solid {p['border_strong']}; border-radius: {p['radius']}; background-color: {p['surface']}; color: {p['text']}; font-weight: 600; }}
        QPushButton:hover, QToolButton:hover {{ background-color: {p['surface_hover']}; border-color: {p['accent']}; }}
        QPushButton:pressed, QToolButton:pressed {{ background-color: {p['surface_pressed']}; }}
        QPushButton:disabled {{ background-color: {p['disabled_bg']}; color: {p['disabled_text']}; border-color: {p['border']}; }}
        QPushButton#primaryButton {{ background-color: {p['accent']}; border-color: {p['accent_hover']}; color: {p['accent_text']}; }}
        QPushButton#primaryButton:hover {{ background-color: {p['accent_hover']}; }}
        QPushButton#dangerButton {{ background-color: {p['danger']}; color: #ffffff; }}
        QPushButton#warningButton, QPushButton#elevateButton {{ background-color: {p['warning']}; color: #ffffff; }}
        QPushButton#successButton {{ background-color: {p['success']}; color: #ffffff; }}
        QTableWidget, QTableView {{ background-color: {p['input']}; alternate-background-color: {p['panel_alt']}; gridline-color: {p['border']}; border: 1px solid {p['border']}; selection-background-color: {p['selection']}; selection-color: {p['accent_text']}; }}
        QTableWidget::item, QTableView::item {{ padding: 1px; }}
        QTableWidget, QTableView {{ font-size: 7pt; }}
        QHeaderView::section, QTableCornerButton::section {{ background-color: {p['header']}; color: {p['text']}; padding: 3px; border: 0; border-right: 1px solid {p['border']}; border-bottom: 1px solid {p['border']}; font-weight: 600; }}
        #logView {{ background-color: {p['input']}; color: {p['text']}; border: 1px solid {p['border_strong']}; border-radius: {p['radius']}; padding: 6px; }}
        QScrollBar:vertical {{ background-color: {p['scroll_bg']}; width: 12px; margin: 0; }}
        QScrollBar::handle:vertical {{ background-color: {p['scroll_handle']}; min-height: 28px; border-radius: 5px; }}
        QScrollBar:horizontal {{ background-color: {p['scroll_bg']}; height: 12px; margin: 0; }}
        QScrollBar::handle:horizontal {{ background-color: {p['scroll_handle']}; min-width: 28px; border-radius: 5px; }}
        QScrollBar::handle:hover {{ background-color: {p['accent']}; }}
        QScrollBar::add-line, QScrollBar::sub-line {{ width: 0; height: 0; }}
        QStatusBar {{ background-color: {p['menu']}; color: {p['muted']}; border-top: 1px solid {p['border']}; }}
        QStatusBar::item {{ border: 0; }}
        QToolTip {{ background-color: {p['tooltip']}; color: {p['tooltip_text']}; border: 1px solid {p['border_strong']}; padding: 3px; }}
        QMessageBox {{ background-color: {p['window']}; }}
    """


def apply_application_theme(app: QApplication, theme_code: str | None = None) -> str:
    code = str(theme_code or DEFAULT_THEME_CODE).strip().lower()
    if code not in THEME_OPTIONS:
        code = DEFAULT_THEME_CODE
    p = THEME_OPTIONS[code]
    available = {name.lower(): name for name in QStyleFactory.keys()}
    preferred = "windows" if code == "classic" else "fusion"
    style_name = available.get(preferred) or available.get("fusion")
    if style_name:
        app.setStyle(style_name)
    palette = QPalette()
    for role, color in {
        QPalette.Window: p["window"], QPalette.WindowText: p["text"],
        QPalette.Base: p["input"], QPalette.AlternateBase: p["panel_alt"],
        QPalette.ToolTipBase: p["tooltip"], QPalette.ToolTipText: p["tooltip_text"],
        QPalette.Text: p["text"], QPalette.Button: p["surface"],
        QPalette.ButtonText: p["text"], QPalette.BrightText: p["danger"],
        QPalette.Highlight: p["selection"], QPalette.HighlightedText: p["accent_text"],
        QPalette.Link: p["accent"], QPalette.PlaceholderText: p["muted"],
    }.items():
        palette.setColor(role, QColor(color))
    app.setPalette(palette)
    app.setStyleSheet(build_theme_stylesheet(code))
    app.setProperty("themeCode", code)
    return code


def application_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def resource_dir() -> Path:
    bundled = getattr(sys, "_MEIPASS", None)
    return Path(bundled).resolve() if bundled else application_dir()


APP_DIR = application_dir()
RESOURCE_DIR = resource_dir()
SETTINGS_PATH = APP_DIR / "setting.ini"


@dataclass(frozen=True)
class DriveInfo:
    letter: str
    label: str
    drive_type: str
    has_windows: bool
    has_bios_boot: bool
    has_efi_boot: bool

    @property
    def windows_path(self) -> str:
        return f"{self.letter}\\Windows"

    @property
    def display_name(self) -> str:
        label = f" — {self.label}" if self.label else ""
        markers: list[str] = []
        if self.has_windows:
            markers.append("Windows")
        if self.has_efi_boot:
            markers.append("EFI boot")
        if self.has_bios_boot:
            markers.append("BIOS boot")
        suffix = f" [{', '.join(markers)}]" if markers else ""
        return f"{self.letter}{label}{suffix}"


def is_windows() -> bool:
    return os.name == "nt"


def is_admin() -> bool:
    if not is_windows():
        return False
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except (AttributeError, OSError):
        return False


def is_winpe() -> bool:
    if not is_windows():
        return False
    if os.environ.get("SystemDrive", "").upper() == "X:":
        return True
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\MiniNT"):
            return True
    except (ImportError, FileNotFoundError, OSError):
        return False


def firmware_type() -> str:
    if not is_windows():
        return "Unsupported"
    try:
        value = ctypes.c_uint(0)
        result = ctypes.windll.kernel32.GetFirmwareType(ctypes.byref(value))
        if result:
            return {1: "BIOS", 2: "UEFI"}.get(value.value, "Unknown")
    except (AttributeError, OSError):
        pass
    return "Unknown"


def restart_as_admin() -> bool:
    if not is_windows():
        return False
    if getattr(sys, "frozen", False):
        executable = str(Path(sys.executable).resolve())
        arguments = subprocess.list2cmdline(sys.argv[1:])
    else:
        executable = str(Path(sys.executable).resolve())
        arguments = subprocess.list2cmdline([str(Path(__file__).resolve()), *sys.argv[1:]])
    result = ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, arguments, str(APP_DIR), 1)
    return int(result) > 32


def logical_drives() -> list[DriveInfo]:
    if not is_windows():
        return []
    drive_type_names = {0: "Unknown", 1: "Invalid", 2: "Removable", 3: "Fixed", 4: "Network", 5: "Optical", 6: "RAM disk"}
    kernel32 = ctypes.windll.kernel32
    mask = kernel32.GetLogicalDrives()
    result: list[DriveInfo] = []
    for index in range(26):
        if not (mask & (1 << index)):
            continue
        letter = f"{chr(65 + index)}:"
        root = f"{letter}\\"
        kind = kernel32.GetDriveTypeW(root)
        if kind in (0, 1, 4, 5):
            continue
        label_buffer = ctypes.create_unicode_buffer(261)
        fs_buffer = ctypes.create_unicode_buffer(261)
        serial = ctypes.c_uint(0)
        max_component = ctypes.c_uint(0)
        flags = ctypes.c_uint(0)
        label = ""
        try:
            ok = kernel32.GetVolumeInformationW(root, label_buffer, len(label_buffer), ctypes.byref(serial), ctypes.byref(max_component), ctypes.byref(flags), fs_buffer, len(fs_buffer))
            if ok:
                label = label_buffer.value
        except OSError:
            pass
        root_path = Path(root)
        result.append(DriveInfo(
            letter=letter,
            label=label,
            drive_type=drive_type_names.get(kind, "Unknown"),
            has_windows=(root_path / "Windows" / "System32" / "Config" / "SYSTEM").exists(),
            has_bios_boot=(root_path / "Boot" / "BCD").exists() or (root_path / "bootmgr").exists(),
            has_efi_boot=(root_path / "EFI" / "Microsoft" / "Boot" / "BCD").exists(),
        ))
    return result


class BootEngineError(RuntimeError):
    pass


class BootEngineCancelled(BootEngineError):
    pass


@dataclass(frozen=True)
class EngineRequest:
    mode: str
    windows_path: str = ""
    system_drive: str = "AUTO"
    firmware: str = "Auto"
    backup_path: str = ""


class NativeBootEngine:
    """Runs Windows/WinPE boot tools directly; PowerShell is not required."""

    def __init__(self, request: EngineRequest, logger) -> None:
        self.request = request
        self.log = logger
        self._cancel_event = threading.Event()
        self._process_lock = threading.Lock()
        self._process: subprocess.Popen | None = None
        self._mounted_efi_drive = ""

    def cancel(self) -> None:
        self._cancel_event.set()
        with self._process_lock:
            process = self._process
        if process is not None and process.poll() is None:
            try:
                process.terminate()
            except OSError:
                pass

    def _check_cancelled(self) -> None:
        if self._cancel_event.is_set():
            raise BootEngineCancelled("Operation cancelled by the user.")

    @staticmethod
    def normalize_drive(value: str) -> str:
        drive = str(value or "").strip().rstrip("\\/").upper()
        if len(drive) == 2 and drive[0].isalpha() and drive[1] == ":":
            return drive
        raise BootEngineError(f"Invalid drive value: {value}")

    @staticmethod
    def find_native_tool(name: str) -> str:
        candidates: list[Path] = []
        system_root = Path(os.environ.get("SystemRoot", r"X:\\Windows"))
        system_drive = os.environ.get("SystemDrive", "X:")
        candidates.extend([
            system_root / "System32" / name,
            system_root / "Sysnative" / name,
            Path(system_drive + "\\") / "boot" / name,
            APP_DIR / name,
        ])
        if is_windows():
            try:
                mask = ctypes.windll.kernel32.GetLogicalDrives()
                for index in range(26):
                    if mask & (1 << index):
                        root = Path(f"{chr(65 + index)}:\\")
                        candidates.extend([root / "boot" / name, root / "sources" / name])
            except (AttributeError, OSError):
                pass
        for candidate in candidates:
            try:
                if candidate.is_file():
                    return str(candidate)
            except OSError:
                continue
        return shutil.which(name) or ""

    def run_native(self, tool: str, arguments: list[str], allow_failure: bool = False) -> int:
        self._check_cancelled()
        tool_path = self.find_native_tool(tool) if not Path(tool).is_file() else tool
        if not tool_path:
            raise BootEngineError(f"{tool} was not found.")
        command = [tool_path, *arguments]
        self.log(f"[INFO] RUN: {subprocess.list2cmdline(command)}")
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        encoding = locale.getpreferredencoding(False) or "utf-8"
        try:
            process = subprocess.Popen(
                command,
                cwd=str(APP_DIR),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
                text=True,
                encoding=encoding,
                errors="replace",
                creationflags=creationflags,
            )
        except OSError as exc:
            raise BootEngineError(f"Unable to start {tool}: {exc}") from exc
        with self._process_lock:
            self._process = process
        try:
            if process.stdout is not None:
                for raw_line in process.stdout:
                    line = raw_line.rstrip("\r\n")
                    if line:
                        self.log(line)
                    self._check_cancelled()
            code = process.wait()
        finally:
            with self._process_lock:
                self._process = None
        if code != 0 and not allow_failure:
            raise BootEngineError(f"Command failed with exit code {code}: {tool_path}")
        return int(code)

    def effective_firmware(self) -> str:
        requested = self.request.firmware.strip().upper()
        if requested != "AUTO":
            if requested not in {"UEFI", "BIOS", "ALL"}:
                raise BootEngineError(f"Invalid firmware target: {requested}")
            return requested
        detected = firmware_type()
        if detected in {"UEFI", "BIOS"}:
            return detected
        self.log("[WARN] Firmware type could not be detected; defaulting BCDBoot to ALL.")
        return "ALL"

    def get_free_drive_letter(self) -> str:
        for code in range(ord("Z"), ord("C"), -1):
            drive = f"{chr(code)}:"
            if not Path(drive + "\\").exists():
                return drive
        raise BootEngineError("No free drive letter is available for the EFI System Partition.")

    def mount_efi_system_partition(self) -> str:
        drive = self.get_free_drive_letter()
        self.run_native("mountvol.exe", [drive + "\\", "/S"])
        if not Path(drive + "\\").exists():
            raise BootEngineError(f"The EFI System Partition could not be mounted as {drive}")
        self._mounted_efi_drive = drive
        self.log(f"[OK] Mounted the EFI System Partition as {drive}")
        return drive

    def dismount_efi_system_partition(self) -> None:
        if not self._mounted_efi_drive:
            return
        drive = self._mounted_efi_drive
        was_cancelled = self._cancel_event.is_set()
        if was_cancelled:
            self._cancel_event.clear()
        try:
            self.run_native("mountvol.exe", [drive + "\\", "/D"], allow_failure=True)
            self.log(f"[INFO] Released temporary EFI mount {drive}")
        except BootEngineError as exc:
            self.log(f"[WARN] Could not release temporary EFI mount {drive}: {exc}")
        finally:
            if was_cancelled:
                self._cancel_event.set()
            self._mounted_efi_drive = ""

    def resolve_system_target(self, firmware: str) -> str:
        requested = self.request.system_drive.strip().upper()
        if requested and requested != "AUTO":
            drive = self.normalize_drive(requested)
            if not Path(drive + "\\").exists():
                raise BootEngineError(f"Target drive is not accessible: {drive}")
            return drive
        if firmware == "UEFI":
            return self.mount_efi_system_partition()
        return ""

    @staticmethod
    def get_bcd_store_path(target_drive: str, firmware: str) -> Path | None:
        if not target_drive:
            return None
        root = Path(target_drive + "\\")
        if firmware == "UEFI":
            return root / "EFI" / "Microsoft" / "Boot" / "BCD"
        if firmware == "BIOS":
            return root / "Boot" / "BCD"
        uefi = root / "EFI" / "Microsoft" / "Boot" / "BCD"
        return uefi if uefi.is_file() else root / "Boot" / "BCD"

    def backup_bcd_store(self, store_path: Path | None) -> Path | None:
        if store_path is None:
            self.log("[WARN] No explicit BCD store was resolved; BCDBoot will manage the active system store.")
            return None
        if not store_path.is_file():
            self.log(f"[INFO] No existing BCD store found at {store_path}")
            return None
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = Path(str(store_path) + f".backup-{stamp}")
        try:
            shutil.copy2(store_path, backup)
        except OSError as exc:
            raise BootEngineError(f"Unable to back up BCD store: {exc}") from exc
        self.log(f"[OK] BCD backup created: {backup}")
        return backup

    def move_bcd_store_aside(self, store_path: Path | None) -> None:
        if store_path is None:
            self.log("[WARN] No explicit BCD store was resolved; using BCDBoot /c without renaming a store.")
            return
        if not store_path.is_file():
            return
        attrib = self.find_native_tool("attrib.exe")
        if attrib:
            self.run_native(attrib, ["-h", "-s", "-r", str(store_path)], allow_failure=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        destination = store_path.with_name(store_path.name + f".pre-rebuild-{stamp}")
        try:
            store_path.replace(destination)
        except OSError as exc:
            raise BootEngineError(f"Unable to move the previous BCD store aside: {exc}") from exc
        self.log(f"[OK] Previous BCD store moved aside as {destination.name}")

    def invoke_bcdboot(self, windows_directory: str, target_drive: str, firmware: str, clean_store: bool = False) -> None:
        arguments = [windows_directory]
        if target_drive:
            arguments.extend(["/s", target_drive])
        arguments.extend(["/f", firmware])
        if clean_store:
            arguments.append("/c")
        arguments.append("/v")
        self.run_native("bcdboot.exe", arguments)
        self.log("[OK] Windows boot files were installed successfully.")

    def invoke_bootsect(self, style: str, target_drive: str, write_mbr: bool = False) -> None:
        bootsect = self.find_native_tool("bootsect.exe")
        if not bootsect:
            raise BootEngineError(
                "bootsect.exe was not found. Use Windows installation media or place bootsect.exe beside the app."
            )
        arguments = [f"/{style}", target_drive]
        if write_mbr:
            arguments.append("/mbr")
        arguments.append("/force")
        self.run_native(bootsect, arguments)
        self.log(f"[OK] Bootsect completed for {target_drive}")

    def show_diagnostics(self) -> None:
        self.log("NT Boot Fixer WinPE diagnostics")
        self.log("-" * 60)
        self.log(f"[INFO] Engine: embedded Python worker (PowerShell not required)")
        self.log(f"[INFO] Operating system: {platform.platform()}")
        self.log(f"[INFO] Windows PE: {is_winpe()}")
        self.log(f"[INFO] Administrator: {is_admin()}")
        self.log(f"[INFO] Firmware: {firmware_type()}")
        self.log(f"[INFO] SystemRoot: {os.environ.get('SystemRoot', '')}")
        for name in ("bcdboot.exe", "bcdedit.exe", "bootsect.exe", "mountvol.exe", "attrib.exe"):
            found = self.find_native_tool(name)
            self.log(f"[OK] {name} = {found}" if found else f"[WARN] {name} was not found")
        if self.request.windows_path:
            valid = (Path(self.request.windows_path) / "System32" / "Config" / "SYSTEM").is_file()
            self.log(f"[INFO] Selected Windows path: {self.request.windows_path} (valid={valid})")
        self.log(f"[INFO] Selected system drive: {self.request.system_drive}")
        self.log(f"[INFO] Requested firmware: {self.request.firmware}")

    def run(self) -> int:
        mode = self.request.mode
        self.log(f"[INFO] Mode: {mode}")
        try:
            if mode == "diagnose":
                self.show_diagnostics()
                return 0
            if mode == "bcd-list":
                self.run_native("bcdedit.exe", ["/enum", "all", "/v"])
                return 0
            if mode == "bcd-export":
                if not is_admin():
                    raise BootEngineError("Administrator privileges are required.")
                if not self.request.backup_path:
                    raise BootEngineError("A backup destination is required for BCD export.")
                output = Path(self.request.backup_path)
                output.parent.mkdir(parents=True, exist_ok=True)
                self.run_native("bcdedit.exe", ["/export", str(output)])
                self.log(f"[OK] System BCD exported to {output}")
                return 0
            if not is_admin():
                raise BootEngineError("Administrator privileges are required for this operation.")

            firmware = self.effective_firmware()
            self.log(f"[INFO] Effective firmware target: {firmware}")

            if mode in {"nt60", "nt52", "mbr"}:
                if self.request.system_drive.strip().upper() == "AUTO":
                    raise BootEngineError("An explicit target partition is required for boot-code operations.")
                target = self.normalize_drive(self.request.system_drive)
                if mode == "nt60":
                    self.invoke_bootsect("nt60", target)
                elif mode == "nt52":
                    self.invoke_bootsect("nt52", target)
                else:
                    self.invoke_bootsect("nt60", target, write_mbr=True)
                return 0

            windows_path = self.request.windows_path
            if not windows_path or not (Path(windows_path) / "System32" / "Config" / "SYSTEM").is_file():
                raise BootEngineError(f"The selected Windows installation is invalid: {windows_path}")

            target_drive = self.resolve_system_target(firmware)
            self.log(f"[INFO] Resolved system target: {target_drive}" if target_drive else "[INFO] System target: automatic Windows selection")
            store_path = self.get_bcd_store_path(target_drive, firmware)
            if store_path is not None:
                self.log(f"[INFO] Resolved BCD store: {store_path}")

            if mode == "bootfiles":
                self.invoke_bcdboot(windows_path, target_drive, firmware)
                return 0

            self.backup_bcd_store(store_path)
            if mode == "rebuild":
                if store_path is not None:
                    self.move_bcd_store_aside(store_path)
                    self.invoke_bcdboot(windows_path, target_drive, firmware)
                else:
                    self.invoke_bcdboot(windows_path, target_drive, firmware, clean_store=True)
                return 0
            if mode == "auto":
                self.invoke_bcdboot(windows_path, target_drive, firmware)
                if firmware in {"BIOS", "ALL"} and target_drive:
                    if self.find_native_tool("bootsect.exe"):
                        self.invoke_bootsect("nt60", target_drive)
                    else:
                        self.log("[WARN] bootsect.exe is unavailable; boot files were installed but BIOS partition boot code was not rewritten.")
                self.log("[OK] Recommended repair completed.")
                return 0
            raise BootEngineError(f"Unsupported mode: {mode}")
        finally:
            self.dismount_efi_system_partition()


class EngineWorker(QThread):
    line_ready = pyqtSignal(str)
    completed = pyqtSignal(int)

    def __init__(self, request: EngineRequest, parent=None) -> None:
        super().__init__(parent)
        self.engine = NativeBootEngine(request, self.line_ready.emit)

    def request_stop(self) -> None:
        self.engine.cancel()

    def run(self) -> None:
        code = 0
        try:
            code = self.engine.run()
        except BootEngineCancelled as exc:
            code = 2
            self.line_ready.emit(f"[WARN] {exc}")
        except Exception as exc:  # worker boundary: always report to the GUI
            code = 1
            self.line_ready.emit(f"[ERROR] {exc}")
        self.completed.emit(code)


def fit_button_text(button: QPushButton, extra_padding: int = 30) -> None:
    """Keep button captions fully visible across DPI settings and Qt themes."""
    button.ensurePolished()
    metrics = QFontMetrics(button.font())
    icon_width = button.iconSize().width() + 7 if not button.icon().isNull() else 0
    required_width = metrics.horizontalAdvance(button.text()) + extra_padding + icon_width
    required_height = metrics.height() + 10
    button.setMinimumWidth(max(button.minimumWidth(), required_width))
    button.setMinimumHeight(max(button.minimumHeight(), min(required_height, 24)))
    button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)


class StatusCard(QFrame):
    def __init__(self, title: str, parent: QWidget | None = None, locked: bool = False) -> None:
        super().__init__(parent)
        self.setObjectName("statusCard")
        self.setMinimumHeight(60)
        self.setMaximumHeight(60)
        self.setProperty("locked", "true" if locked else "false")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(1)

        title_label = QLabel(title)
        title_label.setObjectName("statusTitle")
        self.value_label = QLabel("—")
        self.value_label.setObjectName("statusValue")
        self.detail_label = QLabel("")
        self.detail_label.setObjectName("statusDetail")
        self.detail_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.detail_label)

    def set_status(self, value: str, detail: str = "", state: str = "neutral") -> None:
        self.value_label.setText(value)
        self.detail_label.setText(detail)
        self.setProperty("state", state)
        self.style().unpolish(self)
        self.style().polish(self)


class ActionCard(QFrame):
    def __init__(
        self,
        title: str,
        description: str,
        button_text: str,
        callback,
        parent: QWidget | None = None,
        danger: bool = False,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("actionCard")
        self.setMinimumHeight(76)
        self.setMaximumHeight(76)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(7, 5, 7, 5)
        layout.setSpacing(2)

        title_label = QLabel(title)
        title_label.setObjectName("actionTitle")
        description_label = QLabel(description)
        description_label.setObjectName("actionDescription")
        description_label.setWordWrap(True)
        description_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        button = QPushButton(button_text)
        button.setCursor(Qt.PointingHandCursor)
        if danger:
            button.setObjectName("dangerButton")
        button.clicked.connect(callback)
        fit_button_text(button)

        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addWidget(button, 0, Qt.AlignLeft)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.theme_code = self._load_theme_code()
        app = QApplication.instance()
        if app is not None:
            apply_application_theme(app, self.theme_code)

        self.setWindowTitle(f"{APP_NAME} {APP_VERSION}")
        self.resize(1024, 700)
        self.setMinimumSize(920, 620)
        self.setMaximumSize(1600, 1000)
        self._apply_app_icon()

        self.worker: EngineWorker | None = None
        self.current_operation = ""
        self.drives: list[DriveInfo] = []

        self._build_menu()
        self._build_ui()
        self.refresh_system()

    def _load_theme_code(self) -> str:
        parser = configparser.ConfigParser()
        try:
            parser.read(SETTINGS_PATH, encoding="utf-8")
            code = parser.get("UI", "theme", fallback=DEFAULT_THEME_CODE).strip().lower()
        except (OSError, configparser.Error):
            code = DEFAULT_THEME_CODE
        return code if code in THEME_OPTIONS else DEFAULT_THEME_CODE

    def _save_theme_code(self) -> None:
        parser = configparser.ConfigParser()
        try:
            if SETTINGS_PATH.is_file():
                parser.read(SETTINGS_PATH, encoding="utf-8")
            if not parser.has_section("UI"):
                parser.add_section("UI")
            parser.set("UI", "theme", self.theme_code)
            with SETTINGS_PATH.open("w", encoding="utf-8") as stream:
                parser.write(stream)
        except OSError:
            pass

    def _apply_app_icon(self) -> None:
        icon_path = RESOURCE_DIR / "icon.ico"
        if icon_path.is_file():
            icon = QIcon(str(icon_path))
            self.setWindowIcon(icon)
            app = QApplication.instance()
            if app is not None:
                app.setWindowIcon(icon)

    def set_theme(self, theme_code: str) -> None:
        code = str(theme_code).strip().lower()
        if code not in THEME_OPTIONS:
            return
        self.theme_code = code
        app = QApplication.instance()
        if app is not None:
            apply_application_theme(app, code)
        for action_code, action in self.theme_actions.items():
            action.setChecked(action_code == code)
        self._save_theme_code()
        if hasattr(self, "tab_widget"):
            QTimer.singleShot(0, self._fit_ui_text)
        if hasattr(self, "status_bar"):
            self.status_bar.showMessage(f"THEME: {THEME_OPTIONS[code]['label']}", 3000)

    def _build_menu(self) -> None:
        file_menu = self.menuBar().addMenu("FILE")
        save_action = QAction("SAVE ACTIVITY LOG", self)
        save_action.triggered.connect(self.save_log)
        export_action = QAction("EXPORT SYSTEM BCD", self)
        export_action.triggered.connect(self.export_bcd)
        exit_action = QAction("EXIT", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(save_action)
        file_menu.addAction(export_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        theme_menu = self.menuBar().addMenu("THEME")
        self.theme_action_group = QActionGroup(self)
        self.theme_action_group.setExclusive(True)
        self.theme_actions: dict[str, QAction] = {}
        for code in THEME_ORDER:
            action = QAction(THEME_OPTIONS[code]["label"], self)
            action.setCheckable(True)
            action.setChecked(code == self.theme_code)
            action.triggered.connect(lambda checked=False, selected=code: self.set_theme(selected))
            self.theme_action_group.addAction(action)
            theme_menu.addAction(action)
            self.theme_actions[code] = action

        about_menu = self.menuBar().addMenu("ABOUT")
        about_action = QAction(f"ABOUT {APP_NAME.upper()}", self)
        about_action.triggered.connect(self.show_about)
        about_menu.addAction(about_action)

    def _build_ui(self) -> None:
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        self.tab_widget.addTab(self._create_dashboard_page(), "DASHBOARD")
        self.tab_widget.addTab(self._create_log_page(), "ACTIVITY LOG")
        self.tab_widget.currentChanged.connect(self._tab_changed)
        tab_bar = self.tab_widget.tabBar()
        tab_bar.setElideMode(Qt.ElideNone)
        tab_bar.setUsesScrollButtons(False)
        tab_bar.setExpanding(True)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("READY")
        self.locale_badge = QLabel(LOCALE)
        self.locale_badge.setObjectName("localeBadge")
        self.admin_badge = QLabel("STANDARD USER")
        self.admin_badge.setObjectName("adminBadge")
        self.status_bar.addPermanentWidget(self.locale_badge)
        self.status_bar.addPermanentWidget(self.admin_badge)
        QTimer.singleShot(0, self._fit_ui_text)

    def _fit_ui_text(self) -> None:
        for button in self.findChildren(QPushButton):
            fit_button_text(button)

        if not hasattr(self, "tab_widget"):
            return
        tab_bar = self.tab_widget.tabBar()
        tab_bar.ensurePolished()
        metrics = QFontMetrics(tab_bar.font())
        required_width = 0
        for index in range(self.tab_widget.count()):
            required_width += metrics.horizontalAdvance(self.tab_widget.tabText(index)) + 52
        required_width += max(0, self.tab_widget.count() - 1) * 2
        tab_bar.setMinimumWidth(required_width)

    def _tab_changed(self, index: int) -> None:
        labels = ("DASHBOARD", "ACTIVITY LOG")
        if 0 <= index < len(labels) and not self._operation_running():
            self.status_bar.showMessage(labels[index])

    def _page_heading(self, title: str, description: str) -> tuple[QVBoxLayout, QWidget]:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(3)
        heading = QLabel(title.upper())
        heading.setObjectName("pageTitle")
        detail = QLabel(description)
        detail.setObjectName("pageDescription")
        detail.setWordWrap(True)
        layout.addWidget(heading)
        layout.addWidget(detail)
        return layout, page

    def _create_dashboard_page(self) -> QWidget:
        layout, page = self._page_heading(
            "System overview & repair",
            "Review the recovery environment, select the Windows installation and system partition, then run the manual boot repair.",
        )

        cards = QGridLayout()
        cards.setHorizontalSpacing(4)
        cards.setVerticalSpacing(4)
        self.platform_card = StatusCard("ENVIRONMENT")
        self.firmware_card = StatusCard("FIRMWARE")
        self.support_card = StatusCard("RECOVERY ENGINE", locked=True)
        self.target_card = StatusCard("DETECTED WINDOWS")
        cards.addWidget(self.platform_card, 0, 0)
        cards.addWidget(self.firmware_card, 0, 1)
        cards.addWidget(self.support_card, 0, 2)
        cards.addWidget(self.target_card, 0, 3)
        layout.addLayout(cards)

        selector = QFrame()
        selector.setObjectName("panel")
        selector_layout = QGridLayout(selector)
        selector_layout.setContentsMargins(6, 5, 6, 5)
        selector_layout.setHorizontalSpacing(4)
        selector_layout.setVerticalSpacing(2)

        win_label = QLabel("WINDOWS INSTALLATION")
        win_label.setObjectName("fieldLabel")
        self.windows_combo = QComboBox()
        self.windows_combo.currentIndexChanged.connect(self._update_target_summary)

        system_label = QLabel("SYSTEM PARTITION")
        system_label.setObjectName("fieldLabel")
        self.system_combo = QComboBox()
        self.system_combo.currentIndexChanged.connect(self._update_target_summary)

        firmware_label = QLabel("FIRMWARE TARGET")
        firmware_label.setObjectName("fieldLabel")
        self.firmware_combo = QComboBox()
        self.firmware_combo.addItems(["AUTO", "UEFI", "BIOS", "ALL"])
        self.firmware_combo.currentIndexChanged.connect(self._update_target_summary)

        # Empty header label above the button keeps the 4-column grid visually aligned.
        action_label = QLabel("")
        action_label.setObjectName("fieldLabel")

        self.rebuild_button = QPushButton("REPAIR BOOT CODE")
        self.rebuild_button.setObjectName("dangerButton")
        self.rebuild_button.clicked.connect(self.run_rebuild_bcd)
        self.rebuild_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        selector_layout.addWidget(win_label, 0, 0)
        selector_layout.addWidget(system_label, 0, 1)
        selector_layout.addWidget(firmware_label, 0, 2)
        selector_layout.addWidget(action_label, 0, 3)
        selector_layout.addWidget(self.windows_combo, 1, 0)
        selector_layout.addWidget(self.system_combo, 1, 1)
        selector_layout.addWidget(self.firmware_combo, 1, 2)
        selector_layout.addWidget(self.rebuild_button, 1, 3)

        # Equal stretch on all four columns -> each widget gets exactly 1/4 of the row width,
        # so the REPAIR BOOT CODE button matches the combo boxes in BOTH width and height.
        selector_layout.setColumnStretch(0, 1)
        selector_layout.setColumnStretch(1, 1)
        selector_layout.setColumnStretch(2, 1)
        selector_layout.setColumnStretch(3, 1)

        unified_row_height = 24
        for widget in (
            self.windows_combo,
            self.system_combo,
            self.firmware_combo,
            self.rebuild_button,
        ):
            widget.setMinimumHeight(unified_row_height)
            widget.setMaximumHeight(unified_row_height)

        layout.addWidget(selector)

        warning = QFrame()
        warning.setObjectName("warningPanel")
        warning_layout = QVBoxLayout(warning)
        warning_layout.setContentsMargins(8, 5, 8, 5)
        warning_title = QLabel("BEFORE YOU CONTINUE")
        warning_title.setObjectName("warningTitle")
        warning_text = QLabel(
            "Choose the correct Windows installation. On UEFI systems, leave System partition on AUTO "
            "to mount the EFI System Partition temporarily. Disconnect unrelated external disks when possible."
        )
        warning_text.setObjectName("warningText")
        warning_text.setWordWrap(True)
        warning_layout.addWidget(warning_title)
        warning_layout.addWidget(warning_text)
        layout.addWidget(warning)

        table_panel = QFrame()
        table_panel.setObjectName("panel")
        table_layout = QVBoxLayout(table_panel)
        table_layout.setContentsMargins(6, 4, 6, 5)
        table_title = QLabel("DETECTED VOLUMES — DOUBLE-CLICK A WINDOWS ROW TO SELECT")
        table_title.setObjectName("sectionTitle")
        table_layout.addWidget(table_title)
        self.drive_table = QTableWidget(0, 5)
        self.drive_table.setHorizontalHeaderLabels(["VOLUME", "LABEL", "TYPE", "WINDOWS", "BOOT FILES"])
        self.drive_table.verticalHeader().setVisible(False)
        self.drive_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.drive_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.drive_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.drive_table.setAlternatingRowColors(True)
        self.drive_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.drive_table.setMinimumHeight(62)
        self.drive_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.drive_table.cellDoubleClicked.connect(self._select_installation_from_table)
        table_layout.addWidget(self.drive_table, 1)
        layout.addWidget(table_panel, 1)

        advanced_panel = QFrame()
        advanced_panel.setObjectName("panel")
        advanced_layout = QVBoxLayout(advanced_panel)
        advanced_layout.setContentsMargins(6, 5, 6, 5)
        advanced_layout.setSpacing(2)

        advanced_title = QLabel("ADVANCED TOOLS")
        advanced_title.setObjectName("pageTitle")
        advanced_layout.addWidget(advanced_title)

        advanced_description = QLabel(
            "Use individual recovery actions for targeted troubleshooting. Boot-code operations require an explicit target partition."
        )
        advanced_description.setObjectName("pageDescription")
        advanced_description.setWordWrap(True)
        advanced_layout.addWidget(advanced_description)

        advanced_grid = QGridLayout()
        advanced_grid.setHorizontalSpacing(3)
        advanced_grid.setVerticalSpacing(3)
        advanced_cards = [
            ActionCard("INSTALL BOOT FILES", "Run BCDBoot for the selected Windows installation without intentionally deleting the current BCD store.", "INSTALL BOOT FILES", lambda: self.run_engine_mode("bootfiles", "Install Windows boot files?")),
            ActionCard("VIEW BCD CONFIGURATION", "Enumerate the current system BCD store and write the complete output to the Activity Log.", "READ BCD", lambda: self.run_engine_mode("bcd-list", "")),
            ActionCard("EXPORT SYSTEM BCD", "Create a BCDEdit export file at a location you choose. This exports the currently active system store.", "EXPORT BCD...", self.export_bcd),
            ActionCard("WRITE NT6 BOOT CODE", "Use Bootsect /nt60 on the selected partition. Intended for Windows Vista and later BIOS-style boot code.", "WRITE NT60 PBR", lambda: self.run_engine_mode("nt60", "Write NT60 boot code to the selected partition?"), danger=True),
            ActionCard("WRITE NT5 BOOT CODE", "Use Bootsect /nt52 on the selected partition. Intended only for legacy NTLDR-based Windows systems.", "WRITE NT52 PBR", lambda: self.run_engine_mode("nt52", "Write legacy NT52 boot code to the selected partition?"), danger=True),
            ActionCard("WRITE BIOS MBR", "Use Bootsect /nt60 /mbr. Do not use this on a disk that should remain GPT/UEFI-only.", "WRITE MBR", lambda: self.run_engine_mode("mbr", "Write Windows-compatible BIOS MBR code?"), danger=True),
            ActionCard("ENGINE DIAGNOSTICS", "Check administrator state, firmware detection, and the availability of Windows recovery tools.", "RUN DIAGNOSTICS", lambda: self.run_engine_mode("diagnose", "")),
        ]
        for index, card in enumerate(advanced_cards):
            advanced_grid.addWidget(card, index // 4, index % 4)
        advanced_layout.addLayout(advanced_grid)
        layout.addWidget(advanced_panel)

        # Keep the merged Dashboard compact enough to fit the default window without a page scrollbar.
        return page

    def _create_log_page(self) -> QWidget:
        layout, page = self._page_heading(
            "Activity log",
            "Command output is captured here. Save the log before rebooting when you need a recovery record.",
        )
        toolbar = QHBoxLayout()
        clear_button = QPushButton("CLEAR LOG")
        clear_button.clicked.connect(lambda: self.log_edit.clear())
        save_button = QPushButton("SAVE LOG...")
        save_button.clicked.connect(self.save_log)
        diagnostics_button = QPushButton("RUN DIAGNOSTICS")
        diagnostics_button.setObjectName("primaryButton")
        diagnostics_button.clicked.connect(lambda: self.run_engine_mode("diagnose", ""))
        toolbar.addWidget(clear_button)
        toolbar.addWidget(save_button)
        toolbar.addWidget(diagnostics_button)
        toolbar.addStretch()
        layout.addLayout(toolbar)
        self.log_edit = QTextEdit()
        self.log_edit.setReadOnly(True)
        self.log_edit.setObjectName("logView")
        self.log_edit.setFont(QFont("Consolas", 8))
        layout.addWidget(self.log_edit, 1)
        return page

    def show_page(self, index: int) -> None:
        self.tab_widget.setCurrentIndex(index)

    def refresh_system(self) -> None:
        # The recovery engine is embedded and locked; its status never changes.
        self.support_card.set_status(
            "Embedded engine",
            "Built-in native worker. This engine is locked and cannot be modified.",
            "locked",
        )

        admin = is_admin()
        self.admin_badge.setText("ADMINISTRATOR" if admin else "STANDARD USER")
        self.admin_badge.setProperty("state", "ok" if admin else "warn")
        self.admin_badge.style().unpolish(self.admin_badge)
        self.admin_badge.style().polish(self.admin_badge)

        if not is_windows():
            self.platform_card.set_status("Unsupported host", platform.system(), "error")
            self.firmware_card.set_status("Unavailable", "Run this application on Windows or Windows PE.", "error")
            self.target_card.set_status("0 found", "Windows volumes can only be scanned on Windows.", "warn")
            self.drives = []
            self._populate_drive_controls()
            self.append_log("[WARN] This GUI is designed to run on Windows or Windows PE.")
            return

        environment = "Windows PE" if is_winpe() else "Full Windows"
        version = platform.platform(terse=True)
        self.platform_card.set_status(environment, version, "ok")

        firmware = firmware_type()
        firmware_state = "ok" if firmware in {"UEFI", "BIOS"} else "warn"
        self.firmware_card.set_status(firmware, "Detected through the Windows firmware API.", firmware_state)

        self.drives = logical_drives()
        installations = sum(1 for drive in self.drives if drive.has_windows)
        state = "ok" if installations else "warn"
        self.target_card.set_status(
            f"{installations} found",
            "Double-click a detected Windows volume to select it." if installations else "Select or mount a Windows volume, then refresh.",
            state,
        )
        self._populate_drive_controls()
        self.append_log(
            f"[INFO] System scan refreshed: {environment}, firmware={firmware}, administrator={admin}, Windows installations={installations}."
        )

    def _populate_drive_controls(self) -> None:
        previous_windows = self.windows_combo.currentData()
        previous_system = self.system_combo.currentData()

        self.windows_combo.blockSignals(True)
        self.windows_combo.clear()
        windows_drives = [drive for drive in self.drives if drive.has_windows]
        for drive in windows_drives:
            self.windows_combo.addItem(drive.display_name, drive.windows_path)
        if not windows_drives:
            self.windows_combo.addItem("No Windows installation detected", "")
        previous_index = self.windows_combo.findData(previous_windows)
        if previous_index >= 0:
            self.windows_combo.setCurrentIndex(previous_index)
        self.windows_combo.blockSignals(False)

        self.system_combo.clear()
        self.system_combo.addItem("AUTO (recommended for UEFI)", "AUTO")
        candidates = sorted(
            self.drives,
            key=lambda item: (not (item.has_efi_boot or item.has_bios_boot), item.letter),
        )
        for drive in candidates:
            self.system_combo.addItem(drive.display_name, drive.letter)
        previous_index = self.system_combo.findData(previous_system)
        if previous_index >= 0:
            self.system_combo.setCurrentIndex(previous_index)
        else:
            detected_firmware = firmware_type()
            if detected_firmware == "BIOS":
                preferred = next((d for d in candidates if d.has_bios_boot), None)
                if preferred is None:
                    preferred = next((d for d in candidates if d.has_windows), None)
                if preferred is not None:
                    index = self.system_combo.findData(preferred.letter)
                    if index >= 0:
                        self.system_combo.setCurrentIndex(index)

        self.drive_table.setRowCount(len(self.drives))
        for row, drive in enumerate(self.drives):
            boot_files = []
            if drive.has_efi_boot:
                boot_files.append("EFI")
            if drive.has_bios_boot:
                boot_files.append("BIOS")
            values = [
                drive.letter,
                drive.label or "—",
                drive.drive_type,
                "Yes" if drive.has_windows else "No",
                ", ".join(boot_files) if boot_files else "—",
            ]
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                if column in (0, 3, 4):
                    item.setTextAlignment(Qt.AlignCenter)
                self.drive_table.setItem(row, column, item)

        self._update_target_summary()

    def _select_installation_from_table(self, row: int, _column: int) -> None:
        if row < 0 or row >= len(self.drives):
            return
        drive = self.drives[row]
        if drive.has_windows:
            index = self.windows_combo.findData(drive.windows_path)
            if index >= 0:
                self.windows_combo.setCurrentIndex(index)

    def _update_target_summary(self) -> None:
        # Selector values are read on demand; kept as a slot for combo signals.
        pass

    def selected_windows_path(self) -> str:
        return str(self.windows_combo.currentData() or "")

    def selected_system_drive(self) -> str:
        return str(self.system_combo.currentData() or "AUTO")

    def selected_firmware(self) -> str:
        return self.firmware_combo.currentText()

    def run_rebuild_bcd(self) -> None:
        self.run_engine_mode(
            "rebuild",
            "WARNING: This will rebuild the selected BCD store. The current store will be "
            "backed up and moved aside before rebuilding.\n\n"
            "Do you want to continue?",
        )

    def _operation_running(self) -> bool:
        return self.worker is not None and self.worker.isRunning()

    def run_engine_mode(
        self,
        mode: str,
        confirmation: str,
        extra_args: Iterable[str] | None = None,
    ) -> None:
        if self._operation_running():
            QMessageBox.information(self, APP_NAME, "Another operation is already running.")
            return
        if not is_windows():
            QMessageBox.critical(self, APP_NAME, "This operation is only available on Windows or Windows PE.")
            return

        admin_modes = {"auto", "bootfiles", "rebuild", "nt60", "nt52", "mbr", "bcd-export"}
        if mode in admin_modes and not is_admin():
            response = QMessageBox.question(
                self,
                "Administrator required",
                "This operation requires administrator privileges. Restart the application as administrator now?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes,
            )
            if response == QMessageBox.Yes:
                self.request_elevation()
            return

        if mode in {"auto", "bootfiles", "rebuild"} and not self.selected_windows_path():
            QMessageBox.warning(self, APP_NAME, "Select a valid Windows installation first.")
            return

        if mode in {"nt60", "nt52", "mbr"} and self.selected_system_drive() == "AUTO":
            QMessageBox.warning(self, APP_NAME, "Select an explicit target partition for boot-code operations.")
            return

        if confirmation:
            response = QMessageBox.warning(
                self,
                "Confirm boot repair",
                confirmation,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if response != QMessageBox.Yes:
                return

        backup_path = ""
        extras = list(extra_args or [])
        for index, value in enumerate(extras[:-1]):
            if value.lower() in {"-backuppath", "--backup-path"}:
                backup_path = extras[index + 1]
                break

        request = EngineRequest(
            mode=mode,
            windows_path=self.selected_windows_path() if mode in {"auto", "bootfiles", "rebuild"} else "",
            system_drive=self.selected_system_drive(),
            firmware=self.selected_firmware(),
            backup_path=backup_path,
        )
        self.current_operation = mode
        self.append_log("")
        self.append_log("=" * 78)
        self.append_log(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting operation: {mode}")
        self.append_log("[INFO] Engine: embedded WinPE-native worker; PowerShell is not required.")
        self.show_page(1)
        self._set_busy(True)

        self.worker = EngineWorker(request, self)
        self.worker.line_ready.connect(self.append_log)
        self.worker.started.connect(self._worker_started)
        self.worker.completed.connect(self._worker_finished)
        self.worker.finished.connect(self._worker_cleanup)
        self.worker.start()

    def _set_busy(self, busy: bool) -> None:
        self.rebuild_button.setEnabled(not busy)
        for index in range(self.tab_widget.count()):
            self.tab_widget.setTabEnabled(index, (not busy) or index == 1)
        if busy:
            self.tab_widget.setCurrentIndex(1)
            self.status_bar.showMessage(f"RUNNING: {self.current_operation.upper()}")
        else:
            self.status_bar.showMessage("READY")

    def _worker_started(self) -> None:
        self.append_log("[INFO] Worker started.")
        self.status_bar.showMessage(f"RUNNING: {self.current_operation.upper()}")

    def _worker_finished(self, exit_code: int) -> None:
        operation = self.current_operation
        if exit_code == 0:
            self.append_log(f"[OK] Operation '{operation}' completed successfully.")
            if operation not in {"diagnose", "bcd-list"}:
                QMessageBox.information(self, APP_NAME, "The operation completed successfully. Review the Activity Log before rebooting.")
        elif exit_code == 2:
            self.append_log(f"[WARN] Operation '{operation}' was cancelled.")
        else:
            self.append_log(f"[ERROR] Operation '{operation}' failed with exit code {exit_code}.")
            QMessageBox.critical(self, APP_NAME, "The operation failed. Review the Activity Log for details.")
        self.current_operation = ""
        self._set_busy(False)
        if is_windows():
            QTimer.singleShot(350, self.refresh_system)

    def _worker_cleanup(self) -> None:
        worker = self.worker
        self.worker = None
        if worker is not None:
            worker.deleteLater()

    def append_log(self, text: str) -> None:
        self.log_edit.append(text.replace("\x00", ""))
        scrollbar = self.log_edit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def export_bcd(self) -> None:
        default_name = f"BCD-export-{datetime.now().strftime('%Y%m%d-%H%M%S')}.bak"
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export system BCD",
            str(APP_DIR / default_name),
            "BCD backup (*.bak);;All files (*.*)",
        )
        if not path:
            return
        self.run_engine_mode(
            "bcd-export",
            "Export the currently active system BCD store?",
            ["-BackupPath", path],
        )

    def save_log(self) -> None:
        default_name = f"NTBootFixer-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save activity log",
            str(APP_DIR / default_name),
            "Log files (*.log);;Text files (*.txt);;All files (*.*)",
        )
        if not path:
            return
        try:
            Path(path).write_text(self.log_edit.toPlainText(), encoding="utf-8")
        except OSError as exc:
            QMessageBox.critical(self, APP_NAME, f"Unable to save the log:\n{exc}")

    def request_elevation(self) -> None:
        if is_admin():
            QMessageBox.information(self, APP_NAME, "The application is already running as administrator.")
            return
        try:
            if restart_as_admin():
                QApplication.instance().quit()
            else:
                QMessageBox.critical(self, APP_NAME, "Windows did not start the elevated process.")
        except OSError as exc:
            QMessageBox.critical(self, APP_NAME, f"Elevation failed:\n{exc}")

    def show_about(self) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle(f"About {APP_NAME}")
        dialog.setModal(True)
        dialog.setMinimumWidth(480)
        dialog.setWindowIcon(self.windowIcon())

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(18, 16, 18, 14)
        layout.setSpacing(9)

        title = QLabel(f"{APP_NAME.upper()} {APP_VERSION}")
        title.setObjectName("appTitle")
        title.setAlignment(Qt.AlignCenter)

        about_text = QLabel()
        about_text.setAlignment(Qt.AlignCenter)
        about_text.setWordWrap(True)
        about_text.setTextFormat(Qt.RichText)
        about_text.setOpenExternalLinks(True)
        about_text.setText(
            "<div style='text-align:center; line-height:145%;'>"
            "<b>Created by:</b><br>"
            "rahfie27<br>"
            "E-COMPUTER<br>"
            "SERVICE KOMPUTER PANGGILAN BOGOR<br>"
            "Copyright © ECOMTECH 2026 - All Rights Reserved<br><br>"

            "<b>Contact:</b><br>"
            "<a href='mailto:e-comtech@mail.com'>e-comtech@mail.com</a> / "
            "<a href='mailto:rahfie27@gmail.com'>rahfie27@gmail.com</a><br><br>"

            "<b>Donation:</b><br>"
            "<a href='https://paypal.me/rahfie'>paypal.me/rahfie</a><br><br>"

            "<b>WARNING!</b><br>"
            "This software is provided as-is without warranty.<br><br>"

            "<b>THANKS TO:</b><br>"
            "NSANE FORUM ADMIN, STAFF, MOD, MEMBER, AND VISITOR.<br>"
            "<a href='https://nsaneforums.com'>https://nsaneforums.com</a>"
            "</div>"
        )

        close_button = QPushButton("CLOSE")
        close_button.clicked.connect(dialog.accept)
        fit_button_text(close_button, 42)

        button_row = QHBoxLayout()
        button_row.addStretch()
        button_row.addWidget(close_button)
        button_row.addStretch()

        layout.addWidget(title)
        layout.addWidget(about_text)
        layout.addLayout(button_row)
        dialog.exec_()

    def closeEvent(self, event) -> None:  # noqa: N802 - Qt naming convention
        if self._operation_running():
            response = QMessageBox.question(
                self,
                "Operation in progress",
                "A recovery operation is still running. Stop it and exit?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if response != QMessageBox.Yes:
                event.ignore()
                return
            assert self.worker is not None
            self.worker.request_stop()
            if not self.worker.wait(3000):
                QMessageBox.warning(self, APP_NAME, "The native recovery command has not stopped yet. Close the application after it finishes.")
                event.ignore()
                return
        event.accept()


def main() -> int:
    if hasattr(Qt, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName("ECOMTECH")

    window = MainWindow()

    # 17-inch / 1366x768 friendly sizing: keep the full dashboard visible while
    # still allowing larger displays to use additional space.
    screen = app.primaryScreen()
    if screen is not None:
        available = screen.availableGeometry()
        width = min(1024, max(920, available.width() - 40))
        height = min(700, max(620, available.height() - 28))
        window.resize(width, height)
        window.move(
            available.x() + max(0, (available.width() - width) // 2),
            available.y() + max(0, (available.height() - height) // 2),
        )

    window.show()
    QTimer.singleShot(0, window._fit_ui_text)
    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(main())