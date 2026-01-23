"""Highscore management: read/write top-N highscores to highscores.json"""
import speler-naam
from dataclasses import dataclass, asdict
from typing import List, Optional
import json
import os
import tempfile

DEFAULT_FILE = "highscores.json"
DEFAULT_TOP_N = 10


@dataclass(order=True)
class Entry:
    score: int
    name: str

    def to_dict(self):
        return {"name": self.name, "score": self.score}


class HighscoreManager:
    def __init__(self, path: str = DEFAULT_FILE, top_n: int = DEFAULT_TOP_N):
        self.path = path
        self.top_n = top_n
        self._scores: List[Entry] = []
        self.load()

    def load(self) -> None:
        if not os.path.exists(self.path):
            self._scores = []
            return
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            self._scores = [Entry(score=item["score"], name=item["name"]) for item in raw]
            # ensure sorted (highest first)
            self._scores.sort(reverse=True)
            self._scores = self._scores[: self.top_n]
        except Exception:
            # on any read/parse error, start fresh to avoid crashes
            self._scores = []

    def save(self) -> None:
        # write atomically
        tmp_fd, tmp_path = tempfile.mkstemp(prefix="hs_", suffix=".json", dir=os.path.dirname(self.path) or ".")
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                json.dump([e.to_dict() for e in self._scores], f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, self.path)
        finally:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

    def add_score(self, name: str, score: int) -> None:
        entry = Entry(score=score, name=name)
        self._scores.append(entry)
        self._scores.sort(reverse=True)
        self._scores = self._scores[: self.top_n]
        self.save()

    def add_from_player(self, player) -> None:
        """Accepts a player-like object with attributes `name` and `score` (or `get_name()`, `get_score()`)."""
        name = getattr(player, "name", None)
        score = getattr(player, "score", None)
        if name is None or score is None:
            # try methods
            if callable(getattr(player, "get_name", None)):
                name = player.get_name()
            if callable(getattr(player, "get_score", None)):
                score = player.get_score()
        if name is None or score is None:
            raise ValueError("player must provide name and score attributes or get_name/get_score methods")
        self.add_score(name, int(score))

    def get_top(self, n: Optional[int] = None) -> List[Entry]:
        n = n or self.top_n
        return list(self._scores[:n])

    def formatted(self, n: Optional[int] = None) -> str:
        lines = []
        for i, e in enumerate(self.get_top(n), start=1):
            lines.append(f"{i:2d}. {e.name} - {e.score}")
        return "\n".join(lines)


if __name__ == "__main__":
    # simple demo
    mgr = HighscoreManager()
    mgr.add_score("Alice", 120)
    mgr.add_score("Bob", 95)
    mgr.add_score("Carol", 135)
    print("Top scores:")
    print(mgr.formatted())
