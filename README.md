# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Apps like Spotify and YouTube figure out what you'll like next in two main ways. One is by looking at other people: if someone with taste like yours loved a song, it'll probably suggest it to you too. The other is by looking at the songs themselves: if you like fast, upbeat music, it finds more songs that sound that way. Big platforms mix both.

My version only does the second one. It doesn't know anything about other users. It just looks at the qualities of each song and finds the ones that best match what a person says they like. I care most about matching the overall vibe: how energetic a song is, how happy it sounds, whether it feels acoustic, and its genre and mood. And instead of just picking the "highest energy" songs, it picks the ones closest to what the user actually wants.

What each Song stores: id, title, and artist are just for labeling. The parts I actually use to compare songs are genre, mood, energy, tempo, valence (how positive it sounds), danceability, and acousticness.

What the User Profile stores: the user keeps it simple with their favorite genre, their favorite mood, the energy level they're going for, and whether or not they like acoustic songs.

The profile is smaller than a song on purpose. A person doesn't rate every little detail, they just give a few preferences, and the recommender does the work of matching songs to them.

My Algorithm Recipe

Every song starts at 0 points, and I add points as it matches what the user wants. A genre match is worth 2 points. A mood match is worth 1 point. Then I give up to 1.5 points for how close the song's energy is to the user's target, so a perfect match gets the full amount and it fades toward 0 the further off it is. Finally, if the user likes acoustic music, I add a little based on how acoustic the song is, up to half a point. I add all of that up and recommend the songs with the highest totals.

I made genre worth twice as much as mood on purpose. Genre feels like the most reliable sign of what someone actually likes, while mood is more about how they feel that day and changes a lot. So a pop fan asking for pop will almost always get pop first, and mood mostly just reorders things within that. Energy is a good tie-breaker, and acoustic is the smallest weight so it only nudges close calls.

Biases I expect

Because genre is the heaviest weight, the system probably over-prioritizes genre and misses great songs that match the user's mood but happen to be in a different genre. Someone who loves chill music might get an okay song from their favorite genre ranked above a genuinely chill song from a genre they didn't name.

It also just reinforces what the user already likes, since it only matches on the genre and mood they typed in, so it can't really surprise them with something new. And if the catalog is mostly one genre, a user who likes a rarer genre has very few songs that can ever score well, so their results end up thin.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Below is a sample run for the default "pop / happy" profile (`python -m src.main`):

```
============================================================
  Top 5 Recommendations
  Profile: genre=pop, mood=happy, energy=0.80, acoustic=no
============================================================

1. Sunrise City - Neon Echo
   Score: 4.47
   Why:
     - genre match (pop) (+2.0)
     - mood match (happy) (+1.0)
     - energy close to target (+1.47)

2. Gym Hero - Max Pulse
   Score: 3.30
   Why:
     - genre match (pop) (+2.0)
     - energy close to target (+1.30)

3. Rooftop Lights - Indigo Parade
   Score: 2.44
   Why:
     - mood match (happy) (+1.0)
     - energy close to target (+1.44)

4. Concrete Kings - Blocktype
   Score: 1.50
   Why:
     - energy close to target (+1.50)

5. Night Drive Loop - Neon Echo
   Score: 1.42
   Why:
     - energy close to target (+1.42)

============================================================
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



