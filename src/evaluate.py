"""
System Evaluation harness for the Music Recommender Simulation.

Runs the recommender against a battery of user profiles and prints the
top 5 results for each so the scoring logic can be inspected side by side.

Two groups of profiles are defined:

1. DISTINCT_PROFILES - three "normal" listeners with clearly different taste.
   These are the sanity checks: the results should look intuitively right.

2. ADVERSARIAL_PROFILES - edge cases designed to try to "trick" the scoring
   logic or surface unexpected behavior (conflicting preferences, values at
   the extremes of the 0-1 range, and genres/moods that do not exist in the
   catalog at all).

Run with:
    python -m src.evaluate
"""

try:
    from src.recommender import load_songs, recommend_songs
    from src.main import print_recommendations
except ImportError:
    from recommender import load_songs, recommend_songs
    from main import print_recommendations


# --- Group 1: three distinct, "normal" listeners -------------------------
DISTINCT_PROFILES = [
    (
        "High-Energy Pop",
        {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.90,
            "likes_acoustic": False,
        },
    ),
    (
        "Chill Lofi",
        {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.35,
            "likes_acoustic": True,
        },
    ),
    (
        "Deep Intense Rock",
        {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.90,
            "likes_acoustic": False,
        },
    ),
]


# --- Group 2: adversarial / edge-case listeners --------------------------
# Each entry pairs a profile with the hypothesis it is meant to test.
ADVERSARIAL_PROFILES = [
    (
        "Conflicting: high energy + sad mood",
        # Wants maximum energy but a melancholic mood. No song in the catalog
        # is both, so which signal "wins"? This probes whether energy or mood
        # dominates when they point in opposite directions.
        {
            "favorite_genre": "rock",
            "favorite_mood": "melancholic",
            "target_energy": 0.98,
            "likes_acoustic": False,
        },
    ),
    (
        "Unknown genre + unknown mood",
        # Neither the genre nor the mood exists in the catalog. Genre and mood
        # bonuses can never fire, so the entire ranking collapses onto energy
        # closeness alone. Does the system fail gracefully?
        {
            "favorite_genre": "polka",
            "favorite_mood": "euphoric",
            "target_energy": 0.50,
            "likes_acoustic": False,
        },
    ),
    (
        "Contradiction: loves acoustic but wants max energy",
        # Acoustic songs in this catalog are all low energy. Asking for both
        # near-1.0 energy AND acoustic feel pits the two rewards against each
        # other. The acoustic weight is tiny (0.5), so energy should win - but
        # is that what actually happens?
        {
            "favorite_genre": "folk",
            "favorite_mood": "melancholic",
            "target_energy": 1.00,
            "likes_acoustic": True,
        },
    ),
    (
        "Everything at zero",
        # Empty-ish taste: no meaningful genre/mood and target_energy=0.0.
        # Because energy is scored by closeness, this quietly rewards the
        # LOWEST-energy songs - an easy-to-miss side effect of the formula.
        {
            "favorite_genre": "",
            "favorite_mood": "",
            "target_energy": 0.00,
            "likes_acoustic": False,
        },
    ),
    (
        "Out-of-range energy target (1.5)",
        # target_energy is supposed to be on a 0-1 scale. Feeding it 1.5 makes
        # the energy_gap and the (1 - gap) term behave oddly. Does the score
        # still rank the highest-energy songs first, or does it break?
        {
            "favorite_genre": "edm",
            "favorite_mood": "energetic",
            "target_energy": 1.50,
            "likes_acoustic": False,
        },
    ),
]


def run_profile(label: str, user_prefs: dict, songs: list) -> None:
    """Prints a labeled header, then the top 5 recommendations for a profile."""
    banner = "#" * 60
    print(f"\n{banner}")
    print(f"# PROFILE: {label}")
    print(banner)
    recommendations = recommend_songs(user_prefs, songs, k=5)
    print_recommendations(user_prefs, recommendations)


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    print("\n\n########## GROUP 1: DISTINCT PROFILES ##########")
    for label, prefs in DISTINCT_PROFILES:
        run_profile(label, prefs, songs)

    print("\n\n########## GROUP 2: ADVERSARIAL / EDGE-CASE PROFILES ##########")
    for label, prefs in ADVERSARIAL_PROFILES:
        run_profile(label, prefs, songs)


if __name__ == "__main__":
    main()
