import json
import pygame

SETTINGS_FILE = "settings.json"
_state = {"fullscreen": False}


def load_settings() -> None:
    try:
        with open(SETTINGS_FILE) as f:
            _state["fullscreen"] = bool(json.load(f).get("fullscreen", False))
    except (FileNotFoundError, ValueError, AttributeError):
        pass


def is_fullscreen() -> bool:
    return _state["fullscreen"]


def toggle_fullscreen() -> None:
    pygame.display.toggle_fullscreen()
    _state["fullscreen"] = not _state["fullscreen"]
    with open(SETTINGS_FILE, "w") as f:
        json.dump(_state, f)
