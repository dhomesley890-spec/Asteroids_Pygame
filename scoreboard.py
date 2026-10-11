import json
import pygame
import constants

SCORES_FILE = "scores.json"
MAX_SCORES = 10


def load_scores() -> list[int]:
    try:
        with open(SCORES_FILE) as f:
            scores = json.load(f)
        return sorted((int(s) for s in scores), reverse=True)[:MAX_SCORES]
    except (FileNotFoundError, ValueError, TypeError):
        return []


def add_score(score: int) -> None:
    if score <= 0:
        return
    scores = load_scores()
    scores.append(score)
    scores.sort(reverse=True)
    with open(SCORES_FILE, "w") as f:
        json.dump(scores[:MAX_SCORES], f)


def points_for(radius: float) -> int:
    kind = round(radius / constants.ASTEROID_MIN_RADIUS)  # 1 = small, 3 = large
    return {1: 100, 2: 50, 3: 20}.get(kind, 20)


def draw_scoreboard(screen, font, score: int, high_score: int) -> None:
    score_text = font.render(f"SCORE: {score}", True, "white")
    high_text = font.render(f"HIGH: {high_score}", True, "white")
    screen.blit(score_text, (20, 15))
    screen.blit(high_text, high_text.get_rect(topright=(constants.SCREEN_WIDTH - 20, 15)))
