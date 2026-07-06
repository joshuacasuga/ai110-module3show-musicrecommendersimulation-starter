"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

# Import works whether you run `python -m src.main` (from the project root)
# or `python src/main.py`.
try:
    from src.recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


def print_recommendations(user_prefs: dict, recommendations: list) -> None:
    """Prints a clean, readable layout of the ranked recommendations."""
    acoustic = "yes" if user_prefs["likes_acoustic"] else "no"
    profile = (
        f"genre={user_prefs['favorite_genre']}, "
        f"mood={user_prefs['favorite_mood']}, "
        f"energy={user_prefs['target_energy']:.2f}, "
        f"acoustic={acoustic}"
    )

    line = "=" * 60
    print(f"\n{line}")
    print(f"  Top {len(recommendations)} Recommendations")
    print(f"  Profile: {profile}")
    print(line)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} - {song['artist']}")
        print(f"   Score: {score:.2f}")
        print("   Why:")
        # recommend_songs joins the scoring reasons with ", " - split them back
        # out so each reason gets its own bullet.
        for reason in explanation.split(", "):
            print(f"     - {reason}")

    print(f"\n{line}\n")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Default taste profile: a listener who wants upbeat, high-energy pop.
    # Each key is a target the recommender compares every song against.
    user_prefs = {
        "favorite_genre": "pop",      # exact-match bonus
        "favorite_mood": "happy",     # exact-match bonus
        "target_energy": 0.80,        # scored by closeness, not "higher is better"
        "likes_acoustic": False,      # rewards high acousticness (off here)
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)
    print_recommendations(user_prefs, recommendations)


if __name__ == "__main__":
    main()
