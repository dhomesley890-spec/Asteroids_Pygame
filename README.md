# Asteroids

A classic Asteroids-style arcade game built with Python and [pygame](https://www.pygame.org/). Pilot a triangular ship, shoot lumpy asteroids that split into smaller pieces, and climb the top-ten scoreboard.

Built as part of the [Boot.dev](https://www.boot.dev/) Python course, then extended with a main menu, scoreboard, starfield, and fullscreen support.

## Features

- Rotating ship with shooting
- Lumpy, procedurally shaped asteroids that split into smaller ones when shot
- Points by asteroid size (smaller asteroids are worth more)
- Main menu with animated asteroids drifting in the background
- Persistent top-ten scoreboard
- Minimal procedural starfield background
- Windowed and fullscreen modes (menu button or `F11`), remembered between runs
- Dying returns you to the main menu

## Requirements

- Python 3.10+
- pygame

## Installation

```bash
git clone <your-repo-url>
cd Asteroids
pip install pygame
```

If you use [uv](https://docs.astral.sh/uv/), dependencies are handled for you.

## Running the game

```bash
python3 main.py
```

or, with uv:

```bash
uv run main.py
```

## Controls

| Key | Action |
| --- | --- |
| `A` / `D` | Rotate left / right |
| `Space` | Shoot |
| `F11` | Toggle fullscreen |
| `Enter` / `Space` (menu) | Start game |
| `Esc` | Quit (menu) / back (scoreboard) |

The menu and scoreboard buttons also work with the mouse.

## Scoring

| Asteroid size | Points |
| --- | --- |
| Small | 100 |
| Medium | 50 |
| Large | 20 |

Large asteroids split into medium ones, and medium ones into small ones, so you earn points at every stage. Your top ten scores are saved to `scores.json`.

## Project structure

```
.
├── main.py          # Game loop and menu/game flow
├── menu.py          # Main menu, scoreboard screen, block-letter title
├── player.py        # Player ship
├── asteroid.py      # Lumpy asteroids and splitting
├── asteroidfield.py # Asteroid spawning during play
├── shot.py          # Projectiles
├── circleshape.py   # Base class for circular game objects
├── scoreboard.py    # Top-ten scores and in-game score display
├── starfield.py     # Procedural star background
├── settings.py      # Fullscreen setting persistence
├── logger.py        # State/event logging (used by Boot.dev tests)
└── constants.py     # Screen size, speeds, radii, and other tuning values
```

## Configuration

Gameplay values live in `constants.py`, including screen size (1280x720), player speed, shot speed, asteroid sizes, and spawn rate. The game always renders at the logical screen size and uses pygame's `SCALED` flag to fit your monitor in fullscreen, adding black bars on non-16:9 displays.

## Generated files

These are created while playing and should be listed in `.gitignore`:

```
scores.json
settings.json
game_state.jsonl
game_events.jsonl
```

## Credits

Based on the Asteroids guided project from [Boot.dev](https://www.boot.dev/).
