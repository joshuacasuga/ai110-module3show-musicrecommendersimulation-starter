# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

VibeMatch 1.0

---

## 2. Intended Use  

This is a small recommender built for a class project. You give it a few things you like, a genre, a mood, an energy level, and whether you like acoustic music, and it hands back the 5 songs from its list that fit you best. It also tells you why it picked each one.

It assumes you can describe your taste in those four simple terms, and that a good song is one that closely matches them. It is meant for learning and playing around, not for real listeners.

It should not be used to make real recommendations to actual users, to judge songs or artists, or as anything close to how a real app like Spotify works. The song list is tiny and made up, so any result is just a demo.

---

## 3. How the Model Works  

Every song starts with zero points and earns points for matching you. Matching your genre is worth the most. Matching your mood is worth less. Being close to your target energy adds some points, and the closer it is the more it gets. If you say you like acoustic music, gentle songs get a small bonus.

The song with the most points goes to the top. I kept the original starter scoring but tested changing the weights, and I settled back on the original mix where genre matters most.

---

## 4. Data  

The list has 18 songs. Each one has a title, artist, genre, mood, energy, tempo, and a few other traits. The scoring only really uses genre, mood, energy, and how acoustic the song is.

There are 15 genres and 14 moods, but most of them show up only once. Lofi and pop have the most songs. The list is small and hand-made, so a lot of real music taste is just missing.

---

## 5. Strengths  

It works best when someone has a clear, strong taste, like loud high-energy pop or calm low-energy lofi. Those people get lists that actually feel right.

It also does a good job keeping very different listeners apart. A party person and a study person never get the same songs. And it explains itself, so you can always see why a song showed up.

---

## 6. Limitations and Bias 

The biggest problem is that the song list is lopsided on energy. Most songs are either very high or very low energy, and only a few sit in the middle. Since energy is scored by how close a song is to what you want, someone who likes medium-energy music can never get a good match. So the system quietly favors people with extreme taste.

Genre makes it worse. Most genres only have one song, so most people get one real match and four filler songs. Only lofi and pop fans get a full, personal list. And because it only rewards the exact genre and mood you type in, it just echoes what you already like and never surprises you.

---

## 7. Evaluation  

I tested three listeners: a Happy Pop fan, a Chill Lofi fan, and a Deep Intense Rock fan. For each one I just looked at the top 5 and asked myself if it felt like something they'd actually want to hear.

The thing that surprised me most was Gym Hero. Someone asks for happy pop and Gym Hero, a loud workout song, shows up at number 2 even though its mood is intense, not happy. That happens because the system cares about genre first, energy second, and mood last. Gym Hero is pop and it's high energy, so those two wins beat the wrong mood. Basically it goes "it's pop and it's loud, close enough" and ignores the happy part.

Comparing the profiles side by side made the logic obvious. Pop and Lofi share no songs at all, which makes sense since they asked for opposite energy and different genres. Pop and Rock actually overlap a lot because they both wanted high energy, so they pull from the same pile of loud songs and the genre they picked just decides who gets the number 1 spot. Lofi and Rock are total opposites and share nothing, and Lofi leans even softer because that listener likes acoustic, which nudges the quiet guitar and piano songs up.

Overall two things stood out. Mood barely matters since it's the weakest signal, and people who want the same energy end up with weirdly similar lists even if they picked different genres.

---

## 8. Future Work  

If I kept going, here are a few things I would change.

First, I would fix the energy problem by adding more medium-energy songs so those listeners get real matches too. Second, I would let mood count for more, since right now it barely changes anything. Third, I would add a little variety to the top 5 so it can show you something new instead of just the same kind of song over and over.

---

## 9. Personal Reflection  

My biggest learning moment was realizing how much the weights control everything. Just changing how much genre or energy is worth completely reshuffled the results, and that made the whole idea of a recommender click for me.

AI tools helped me move fast, especially for setting up test profiles and spotting patterns in the data. But I still had to double-check the numbers myself, like counting how the songs were spread across energy levels, because it is easy to trust an answer that sounds right but isn't.

What surprised me most was how a simple points system can still feel like a real recommendation. There is no fancy math, it just adds up a few points, but the results still feel personal.

If I extended this, I would add a bigger and more balanced song list and try mixing in what similar listeners liked, so it could actually surprise people instead of just repeating their own taste back to them.
