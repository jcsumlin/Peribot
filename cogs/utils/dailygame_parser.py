import re
from dataclasses import dataclass
from typing import Optional

# "I found #Narutodle character #883 in classic mode in 5 shots (easy) 🍥"
# Shared by the *dle family (Narutodle, Loldle, Pokedle, ...)
FOUND_PATTERN = re.compile(
    r"I found #(?P<game>\w+) (?P<subject>[\w ]+?) #(?P<number>\d+) in (?P<mode>[\w ]+?) mode "
    r"in (?P<attempts>\d+) shots?(?: \((?P<difficulty>[^)]+)\))?",
    re.IGNORECASE)

# "Wordle 1,234 4/6*" or "#Worldle #123 X/6"
SCORE_PATTERN = re.compile(
    r"^#?(?P<game>[A-Za-z][\w]{1,30}) #?(?P<number>\d[\d,.]*) (?P<score>[\dXx])/(?P<max>\d+)(?P<hard>\*)?\s*$",
    re.MULTILINE)

URL_PATTERN = re.compile(r"https?://\S+")
ASCII_ALNUM = re.compile(r"[A-Za-z0-9]")


@dataclass
class GameResult:
    game: str
    number: int
    attempts: int
    solved: bool
    mode: Optional[str] = None
    max_attempts: Optional[int] = None
    difficulty: Optional[str] = None
    grid: str = ""
    url: Optional[str] = None

    @property
    def game_key(self):
        return self.game.lower()

    @property
    def score_display(self):
        if self.max_attempts is None:
            return f"{self.attempts} shot{'s' if self.attempts != 1 else ''}"
        return f"{self.attempts if self.solved else 'X'}/{self.max_attempts}"


def _extract_grid(content: str):
    """Keep only the emoji result lines (no letters or digits)."""
    lines = [line.strip() for line in content.splitlines()]
    return "\n".join(line for line in lines if line and not ASCII_ALNUM.search(line))


def _extract_url(content: str):
    match = URL_PATTERN.search(content)
    return match.group(0) if match else None


def parse_game_message(content: str) -> Optional[GameResult]:
    """Returns a GameResult if the message is a shared daily game result, otherwise None."""
    match = FOUND_PATTERN.search(content)
    if match:
        return GameResult(game=match.group("game"),
                          number=int(match.group("number")),
                          attempts=int(match.group("attempts")),
                          solved=True,
                          mode=match.group("mode").lower(),
                          difficulty=match.group("difficulty"),
                          grid=_extract_grid(content),
                          url=_extract_url(content))

    match = SCORE_PATTERN.search(content)
    if match:
        max_attempts = int(match.group("max"))
        solved = match.group("score").upper() != "X"
        grid = _extract_grid(content)
        if not grid:
            # A bare "Word 12 3/4" with no emoji grid is probably just chat
            return None
        return GameResult(game=match.group("game"),
                          number=int(re.sub(r"[,.]", "", match.group("number"))),
                          # Failures count as one more than the max so they rank below every solve
                          attempts=int(match.group("score")) if solved else max_attempts + 1,
                          solved=solved,
                          max_attempts=max_attempts,
                          difficulty="hard" if match.group("hard") else None,
                          grid=grid,
                          url=_extract_url(content))
    return None
