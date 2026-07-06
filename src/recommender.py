import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# --- Scoring weights (my "Algorithm Recipe" from Phase 2 / the README) ---
# (The weight-shift sensitivity experiment is documented in the README; the
#  weights below are reverted to the original recipe.)
GENRE_MATCH_POINTS = 2.0   # genre is the most reliable signal of taste
MOOD_MATCH_POINTS = 1.0    # mood matters, but changes day to day
ENERGY_MAX_POINTS = 1.5    # awarded by closeness to target energy, not "higher is better"
ACOUSTIC_MAX_POINTS = 0.5  # smallest weight: only nudges close calls

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k Songs for a user, ranked highest score first."""
        # Reuse the same scoring recipe as the functional API by scoring each
        # Song, then returning the top k Songs sorted highest-first.
        ranked = sorted(
            self.songs,
            key=lambda song: score_song(_prefs_to_dict(user), _song_to_dict(song))[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a one-line, human-readable reason why a song was recommended."""
        score, reasons = score_song(_prefs_to_dict(user), _song_to_dict(song))
        if not reasons:
            return f"{song.title} scored {score:.2f} with no strong matches."
        return f"{song.title} scored {score:.2f} because: " + ", ".join(reasons)


def _song_to_dict(song: Song) -> Dict:
    """Adapts a Song dataclass to the dict shape score_song() expects."""
    return {
        "genre": song.genre,
        "mood": song.mood,
        "energy": song.energy,
        "acousticness": song.acousticness,
    }


def _prefs_to_dict(user: UserProfile) -> Dict:
    """Adapts a UserProfile dataclass to the dict shape score_song() expects."""
    return {
        "favorite_genre": user.favorite_genre,
        "favorite_mood": user.favorite_mood,
        "target_energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
    }

# Columns that hold numbers so we can do math on them later.
INT_FIELDS = ("id",)
FLOAT_FIELDS = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file into a list of dictionaries.

    Numeric columns are converted from strings to int/float so that later
    steps (like scoring on energy closeness) can do arithmetic on them.
    Required by src/main.py
    """
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in INT_FIELDS:
                row[field] = int(row[field])
            for field in FLOAT_FIELDS:
                row[field] = float(row[field])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.

    Returns a (score, reasons) tuple, where `reasons` is a human-readable
    list explaining every point that was awarded (e.g. "genre match (+2.0)").
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons: List[str] = []

    # Genre match: the heaviest weight, since genre is the most reliable signal.
    if song["genre"] == user_prefs["favorite_genre"]:
        score += GENRE_MATCH_POINTS
        reasons.append(f"genre match ({song['genre']}) (+{GENRE_MATCH_POINTS})")

    # Mood match: matters, but worth half of genre.
    if song["mood"] == user_prefs["favorite_mood"]:
        score += MOOD_MATCH_POINTS
        reasons.append(f"mood match ({song['mood']}) (+{MOOD_MATCH_POINTS})")

    # Energy closeness: full points for a perfect match, fading toward 0 the
    # further the song's energy is from the target (both are on a 0-1 scale).
    energy_gap = abs(song["energy"] - user_prefs["target_energy"])
    energy_points = ENERGY_MAX_POINTS * (1 - energy_gap)
    if energy_points > 0:
        score += energy_points
        reasons.append(f"energy close to target (+{energy_points:.2f})")

    # Acoustic preference: only rewarded if the user likes acoustic songs,
    # scaled by how acoustic the song actually is. The smallest weight.
    if user_prefs.get("likes_acoustic"):
        acoustic_points = ACOUSTIC_MAX_POINTS * song["acousticness"]
        score += acoustic_points
        reasons.append(f"acoustic feel (+{acoustic_points:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Ranks every song with score_song() and returns the top `k`.

    Returns a list of (song_dict, score, explanation) tuples, sorted from
    highest score to lowest. Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "no strong matches"
        scored.append((song, score, explanation))

    # sorted() returns a NEW list and leaves `scored` untouched; .sort() would
    # instead reorder the list in place and return None. We want a fresh ranked
    # list here, so sorted() is the clearer choice. key pulls the numeric score
    # (index 1) out of each tuple; reverse=True puts the highest scores first.
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return ranked[:k]
