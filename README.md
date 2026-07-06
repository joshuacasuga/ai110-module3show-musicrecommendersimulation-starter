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

## System Evaluation

To stress-test the scoring logic I built a small evaluation harness,
[`src/evaluate.py`](src/evaluate.py), and ran it with:

```bash
python -m src.evaluate
```

It runs two groups of profiles. **Group 1** is three distinct "normal"
listeners that should produce intuitive results. **Group 2** is a set of
**adversarial / edge-case** profiles I designed (in a separate "System
Evaluation" chat) specifically to try to trick the scoring logic — profiles
with conflicting preferences, values pushed to the edges of the 0–1 range, and
genres/moods that do not exist in the catalog at all.

### Group 1 — Distinct profiles

**High-Energy Pop** (`genre=pop, mood=happy, energy=0.90, acoustic=no`)

```
############################################################
# PROFILE: High-Energy Pop
############################################################

============================================================
  Top 5 Recommendations
  Profile: genre=pop, mood=happy, energy=0.90, acoustic=no
============================================================

1. Sunrise City - Neon Echo
   Score: 4.38
   Why:
     - genre match (pop) (+2.0)
     - mood match (happy) (+1.0)
     - energy close to target (+1.38)

2. Gym Hero - Max Pulse
   Score: 3.46
   Why:
     - genre match (pop) (+2.0)
     - energy close to target (+1.46)

3. Rooftop Lights - Indigo Parade
   Score: 2.29
   Why:
     - mood match (happy) (+1.0)
     - energy close to target (+1.29)

4. Storm Runner - Voltline
   Score: 1.48
   Why:
     - energy close to target (+1.48)

5. Neon Overdrive - Pulsewidth
   Score: 1.41
   Why:
     - energy close to target (+1.41)

============================================================
```

**Chill Lofi** (`genre=lofi, mood=chill, energy=0.35, acoustic=yes`)

```
############################################################
# PROFILE: Chill Lofi
############################################################

============================================================
  Top 5 Recommendations
  Profile: genre=lofi, mood=chill, energy=0.35, acoustic=yes
============================================================

1. Library Rain - Paper Lanterns
   Score: 4.93
   Why:
     - genre match (lofi) (+2.0)
     - mood match (chill) (+1.0)
     - energy close to target (+1.50)
     - acoustic feel (+0.43)

2. Midnight Coding - LoRoom
   Score: 4.75
   Why:
     - genre match (lofi) (+2.0)
     - mood match (chill) (+1.0)
     - energy close to target (+1.40)
     - acoustic feel (+0.35)

3. Focus Flow - LoRoom
   Score: 3.81
   Why:
     - genre match (lofi) (+2.0)
     - energy close to target (+1.42)
     - acoustic feel (+0.39)

4. Spacewalk Thoughts - Orbit Bloom
   Score: 2.85
   Why:
     - mood match (chill) (+1.0)
     - energy close to target (+1.40)
     - acoustic feel (+0.46)

5. Coffee Shop Stories - Slow Stereo
   Score: 1.92
   Why:
     - energy close to target (+1.47)
     - acoustic feel (+0.45)

============================================================
```

**Deep Intense Rock** (`genre=rock, mood=intense, energy=0.90, acoustic=no`)

```
############################################################
# PROFILE: Deep Intense Rock
############################################################

============================================================
  Top 5 Recommendations
  Profile: genre=rock, mood=intense, energy=0.90, acoustic=no
============================================================

1. Storm Runner - Voltline
   Score: 4.48
   Why:
     - genre match (rock) (+2.0)
     - mood match (intense) (+1.0)
     - energy close to target (+1.48)

2. Gym Hero - Max Pulse
   Score: 2.46
   Why:
     - mood match (intense) (+1.0)
     - energy close to target (+1.46)

3. Neon Overdrive - Pulsewidth
   Score: 1.41
   Why:
     - energy close to target (+1.41)

4. Iron Verdict - Ashen Crown
   Score: 1.38
   Why:
     - energy close to target (+1.38)

5. Sunrise City - Neon Echo
   Score: 1.38
   Why:
     - energy close to target (+1.38)

============================================================
```

All three look right: the on-genre, on-mood, on-energy song wins each time,
and the tail is filled by songs that match on energy alone.

### Group 2 — Adversarial / edge-case profiles

**Conflicting: high energy + sad mood** (`rock / melancholic / 0.98`) — asks
for maximum energy but a sad mood. No song is both.

```
############################################################
# PROFILE: Conflicting: high energy + sad mood
############################################################

============================================================
  Top 5 Recommendations
  Profile: genre=rock, mood=melancholic, energy=0.98, acoustic=no
============================================================

1. Storm Runner - Voltline
   Score: 3.40
   Why:
     - genre match (rock) (+2.0)
     - energy close to target (+1.40)

2. Iron Verdict - Ashen Crown
   Score: 1.50
   Why:
     - energy close to target (+1.50)

3. Paper Boats - Wren & Willow
   Score: 1.48
   Why:
     - mood match (melancholic) (+1.0)
     - energy close to target (+0.48)

4. Neon Overdrive - Pulsewidth
   Score: 1.47
   Why:
     - energy close to target (+1.47)

5. Gym Hero - Max Pulse
   Score: 1.43
   Why:
     - energy close to target (+1.43)

============================================================
```

> **Finding:** the genuinely *melancholic* song (Paper Boats) is buried at #3.
> Genre + energy (worth up to 3.5 combined) overwhelm the single mood point, so
> when a user's mood conflicts with their energy target, mood is effectively
> ignored. The "sad" request produced a loud, aggressive playlist.

**Unknown genre + unknown mood** (`polka / euphoric / 0.50`) — neither value
exists in the catalog.

```
############################################################
# PROFILE: Unknown genre + unknown mood
############################################################

============================================================
  Top 5 Recommendations
  Profile: genre=polka, mood=euphoric, energy=0.50, acoustic=no
============================================================

1. Dusty Backroads - Hollow Pines
   Score: 1.50
   Why:
     - energy close to target (+1.50)

2. Velvet Hours - Sable Rose
   Score: 1.42
   Why:
     - energy close to target (+1.42)

3. Island Time - Palm Signal
   Score: 1.38
   Why:
     - energy close to target (+1.38)

4. Midnight Coding - LoRoom
   Score: 1.38
   Why:
     - energy close to target (+1.38)

5. Focus Flow - LoRoom
   Score: 1.35
   Why:
     - energy close to target (+1.35)

============================================================
```

> **Finding:** the system fails *gracefully*. With no genre or mood matches
> possible, the ranking collapses onto energy closeness alone and still returns
> five results — but it silently presents them as confident recommendations
> even though it matched *nothing* the user actually asked for.

**Contradiction: loves acoustic but wants max energy** (`folk / melancholic /
1.00 / acoustic=yes`) — acoustic songs in this catalog are all low-energy.

```
############################################################
# PROFILE: Contradiction: loves acoustic but wants max energy
############################################################

============================================================
  Top 5 Recommendations
  Profile: genre=folk, mood=melancholic, energy=1.00, acoustic=yes
============================================================

1. Paper Boats - Wren & Willow
   Score: 3.90
   Why:
     - genre match (folk) (+2.0)
     - mood match (melancholic) (+1.0)
     - energy close to target (+0.45)
     - acoustic feel (+0.45)

2. Iron Verdict - Ashen Crown
   Score: 1.49
   Why:
     - energy close to target (+1.47)
     - acoustic feel (+0.02)

3. Neon Overdrive - Pulsewidth
   Score: 1.45
   Why:
     - energy close to target (+1.44)
     - acoustic feel (+0.01)

4. Gym Hero - Max Pulse
   Score: 1.42
   Why:
     - energy close to target (+1.40)
     - acoustic feel (+0.03)

5. Storm Runner - Voltline
   Score: 1.42
   Why:
     - energy close to target (+1.40)
     - acoustic feel (+0.05)

============================================================
```

> **Finding:** the genre + mood match (3.0 points) dominates so completely that
> the energy target barely matters for the winner. But notice #2–#5: the
> acoustic bonus is scaled by the song's *own* acousticness, so loud metal/EDM
> tracks (acousticness ≈ 0.03) get an almost-zero acoustic reward. "Likes
> acoustic" quietly does nothing for a high-energy listener — the two
> preferences never actually combine.

**Everything at zero** (`genre="", mood="", energy=0.00`) — an essentially
empty taste profile.

```
############################################################
# PROFILE: Everything at zero
############################################################

============================================================
  Top 5 Recommendations
  Profile: genre=, mood=, energy=0.00, acoustic=no
============================================================

1. Morning Adagio - String Theory
   Score: 1.17
   Why:
     - energy close to target (+1.17)

2. Spacewalk Thoughts - Orbit Bloom
   Score: 1.08
   Why:
     - energy close to target (+1.08)

3. Paper Boats - Wren & Willow
   Score: 1.05
   Why:
     - energy close to target (+1.05)

4. Library Rain - Paper Lanterns
   Score: 0.98
   Why:
     - energy close to target (+0.98)

5. Coffee Shop Stories - Slow Stereo
   Score: 0.95
   Why:
     - energy close to target (+0.95)

============================================================
```

> **Finding:** an empty profile is *not* neutral. Because energy is scored by
> closeness, `target_energy=0.0` quietly becomes a preference for the
> **lowest-energy songs** in the catalog. The system never says "I don't have
> enough to go on" — it confidently recommends the calmest tracks.

**Out-of-range energy target (1.5)** (`edm / energetic / 1.50`) — feeds a value
outside the intended 0–1 range.

```
############################################################
# PROFILE: Out-of-range energy target (1.5)
############################################################

============================================================
  Top 5 Recommendations
  Profile: genre=edm, mood=energetic, energy=1.50, acoustic=no
============================================================

1. Neon Overdrive - Pulsewidth
   Score: 3.69
   Why:
     - genre match (edm) (+2.0)
     - mood match (energetic) (+1.0)
     - energy close to target (+0.69)

2. Iron Verdict - Ashen Crown
   Score: 0.72
   Why:
     - energy close to target (+0.72)

3. Gym Hero - Max Pulse
   Score: 0.65
   Why:
     - energy close to target (+0.65)

4. Storm Runner - Voltline
   Score: 0.61
   Why:
     - energy close to target (+0.61)

5. Sunrise City - Neon Echo
   Score: 0.48
   Why:
     - energy close to target (+0.48)

============================================================
```

> **Finding:** no crash, and the ordering is still sensible (highest-energy
> first). But the formula `1.5 * (1 - energy_gap)` is never clamped, so an even
> larger target (e.g. 3.0) would start producing *negative* energy points and
> could invert the ranking. There is no input validation on `target_energy`.

### What surprised me

- **Mood is the weakest link.** Whenever mood conflicts with genre or energy it
  gets silently overruled — a "sad" request can return an aggressive playlist.
- **The system is never uncertain.** Empty, unknown, and out-of-range inputs all
  produce five confident-looking recommendations. It has no notion of "I can't
  match this," which is the most important safety gap for a real product.
- **Two preferences can cancel out.** "Likes acoustic" + high energy means the
  acoustic bonus is scaled to near zero, so the flag has no practical effect.

---

## Experiments You Tried

### Weight Shift — double energy, halve genre

To test how sensitive the rankings are to the genre bonus, I doubled the energy
weight (`ENERGY_MAX_POINTS` 1.5 → 3.0) and halved the genre weight
(`GENRE_MATCH_POINTS` 2.0 → 1.0) in [`src/recommender.py`](src/recommender.py),
then re-ran `python -m src.main` on the default `pop / happy / 0.80` profile.

**Math check:** energy points are `3.0 * (1 - energy_gap)`. For valid inputs the
gap stays in `[0, 1]`, so energy points stay in `[0, 3.0]` — always non-negative,
never larger than the weight. The max possible total moves from 5.0 to 5.5. No
division, no negatives introduced, and both starter tests still pass.

**Before (genre=2.0, energy=1.5):**

```
1. Sunrise City - Neon Echo        Score: 4.47   (genre +2.0, mood +1.0, energy +1.47)
2. Gym Hero - Max Pulse            Score: 3.30   (genre +2.0, energy +1.30)
3. Rooftop Lights - Indigo Parade  Score: 2.44   (mood +1.0, energy +1.44)
4. Concrete Kings - Blocktype      Score: 1.50   (energy +1.50)
5. Night Drive Loop - Neon Echo    Score: 1.42   (energy +1.42)
```

**After (genre=1.0, energy=3.0):**

```
============================================================
  Top 5 Recommendations
  Profile: genre=pop, mood=happy, energy=0.80, acoustic=no
============================================================

1. Sunrise City - Neon Echo
   Score: 4.94
   Why:
     - genre match (pop) (+1.0)
     - mood match (happy) (+1.0)
     - energy close to target (+2.94)

2. Rooftop Lights - Indigo Parade
   Score: 3.88
   Why:
     - mood match (happy) (+1.0)
     - energy close to target (+2.88)

3. Gym Hero - Max Pulse
   Score: 3.61
   Why:
     - genre match (pop) (+1.0)
     - energy close to target (+2.61)

4. Concrete Kings - Blocktype
   Score: 3.00
   Why:
     - energy close to target (+3.00)

5. Night Drive Loop - Neon Echo
   Score: 2.85
   Why:
     - energy close to target (+2.85)

============================================================
```

**More accurate, or just different?** *Just different — and arguably slightly
worse for this listener.* The #1 pick (Sunrise City) is unchanged because it wins
on every signal. The real change is #2/#3 swapping: **Rooftop Lights** (an *indie
pop* song, so no genre match, but mood=happy and energy 0.76 ≈ target 0.80) leaps
over **Gym Hero** (an actual *pop* match whose mood=intense and energy 0.93 is
further off). With genre and mood now weighted equally and energy dominating, an
off-genre song can out-rank a true genre match purely on vibe. For a listener who
explicitly named "pop," pushing a non-pop song up the list is not obviously *more*
accurate — it just shifts the system from "genre-anchored" to "energy-anchored."
The experiment confirms genre was doing most of the ranking work before.

> **Revert:** set `GENRE_MATCH_POINTS = 2.0` and `ENERGY_MAX_POINTS = 1.5` in
> [`src/recommender.py`](src/recommender.py) to return to the original recipe.

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



