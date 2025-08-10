---
author:
- "[Shuvam Banerji Seal](https://shuvam-banerji-seal.github.io/)"
date: 2025-08-09
title: SQL and Relational Algebra — Worked Examples
---

## Schema assumptions

We assume the following relations (attributes in parentheses):

- ANIME(anime_id, title, genre, release_year, studio_id)
- STUDIOS(studio_id, name, founded_year)
- CHARACTERS(char_id, name, role, anime_id)
- EPISODES(ep_id, anime_id, episode_number, title, air_date)

Unless stated otherwise, treat RA with set semantics and use DISTINCT in SQL where sets are intended.

---

### 1) Selection (σ)
- Task: Anime released after 2010
- RA: σ_{release_year > 2010}(ANIME)
- SQL:
```sql
SELECT *
FROM anime
WHERE release_year > 2010;
```

### 2) Projection (π)
- Task: Distinct genres
- RA: π_{genre}(ANIME)
- SQL:
```sql
SELECT DISTINCT genre
FROM anime;
```

### 3) Projection + Selection
- Task: Titles of Action anime
- RA: π_{title}( σ_{genre='Action'}(ANIME) )
- SQL:
```sql
SELECT title
FROM anime
WHERE genre = 'Action';
```

### 4) Rename (ρ)
- Task: Alias relations for readability
- RA: ρ_{A←ANIME}(ANIME) ⋈_{A.studio_id=S.studio_id} ρ_{S←STUDIOS}(STUDIOS)
- SQL:
```sql
SELECT A.title, S.name AS studio_name
FROM anime AS A
JOIN studios AS S ON S.studio_id = A.studio_id;
```

### 5) Cartesian product (×) then selection → Theta-join
- Task: Same as join but written in primitive ops
- RA: σ_{ANIME.studio_id=STUDIOS.studio_id}( ANIME × STUDIOS )
- SQL (prefer join):
```sql
SELECT a.title, s.name
FROM anime AS a
JOIN studios AS s ON s.studio_id = a.studio_id;
```

### 6) Natural join (⋈)
- Task: Characters with their anime titles
- RA: CHARACTERS ⋈_{CHARACTERS.anime_id=ANIME.anime_id} ANIME
- SQL:
```sql
SELECT c.name AS character_name, a.title AS anime_title
FROM characters AS c
JOIN anime AS a ON a.anime_id = c.anime_id;
```

### 7) Theta-join with predicate
- Task: Anime by studios founded before 2000
- RA: π_{title}( ANIME ⋈_{ANIME.studio_id=STUDIOS.studio_id ∧ founded_year<2000} STUDIOS )
- SQL:
```sql
SELECT a.title
FROM anime AS a
JOIN studios AS s ON s.studio_id = a.studio_id
WHERE s.founded_year < 2000;
```

### 8) Semi-join (⟕ or ⋉) — exists at least one
- Task: Anime that have at least one character
- RA: π_{anime_id}( ANIME ⋉ CHARACTERS )  where key is ANIME.anime_id = CHARACTERS.anime_id
- SQL (EXISTS):
```sql
SELECT a.*
FROM anime AS a
WHERE EXISTS (
  SELECT 1 FROM characters AS c WHERE c.anime_id = a.anime_id
);
```

### 9) Anti-join (left anti) — none exist
- Task: Anime with no episodes
- RA: ANIME ▷ EPISODES   (left anti-join on anime_id)
- SQL:
```sql
SELECT a.*
FROM anime AS a
LEFT JOIN episodes AS e ON e.anime_id = a.anime_id
WHERE e.anime_id IS NULL;
```

### 10) Aggregation (γ) — count per group
- Task: Number of characters per anime
- RA: γ_{anime_id; COUNT(*)→num_chars}(CHARACTERS)
- SQL:
```sql
SELECT anime_id, COUNT(*) AS num_chars
FROM characters
GROUP BY anime_id;
```

### 11) Aggregation with HAVING
- Task: Studios with 2+ anime
- RA: γ_{studio_id; COUNT(*)→n}(ANIME); σ_{n>=2}(...)
- SQL:
```sql
SELECT studio_id, COUNT(*) AS n
FROM anime
GROUP BY studio_id
HAVING COUNT(*) >= 2;
```

### 12) Union (∪)
- Task: Union of anime titles and character names (as names)
- RA: π_{title→name}(ANIME) ∪ π_{name}(CHARACTERS)
- SQL:
```sql
SELECT title AS name FROM anime
UNION
SELECT name FROM characters;
```

### 13) Difference (−)
- Task: Anime that have no characters
- RA: π_{anime_id}(ANIME) − π_{anime_id}(CHARACTERS)
- SQL (EXCEPT if available):
```sql
-- Standard SQL
SELECT DISTINCT a.anime_id
FROM anime AS a
EXCEPT
SELECT DISTINCT c.anime_id
FROM characters AS c;
```
- SQL (portable):
```sql
SELECT DISTINCT a.anime_id
FROM anime AS a
LEFT JOIN characters AS c ON c.anime_id = a.anime_id
WHERE c.anime_id IS NULL;
```

### 14) Intersection (∩)
- Task: Anime IDs that appear in both anime and episodes
- RA: π_{anime_id}(ANIME) ∩ π_{anime_id}(EPISODES)
- SQL (INTERSECT if available):
```sql
SELECT DISTINCT anime_id FROM anime
INTERSECT
SELECT DISTINCT anime_id FROM episodes;
```
- SQL (portable):
```sql
SELECT DISTINCT a.anime_id
FROM anime AS a
JOIN episodes AS e USING (anime_id);
```

### 15) Join + filter + projection
- Task: Titles and episode 1 air dates
- RA: π_{title, air_date}( σ_{episode_number=1}( ANIME ⋈ EPISODES ) )
- SQL:
```sql
SELECT a.title, e.air_date
FROM anime AS a
JOIN episodes AS e ON e.anime_id = a.anime_id
WHERE e.episode_number = 1;
```

### 16) Outer join (left)
- Task: All studios with any anime titles if present
- RA (extended): STUDIOS ⟕_{studio_id} ANIME
- SQL:
```sql
SELECT s.name AS studio_name, a.title
FROM studios AS s
LEFT JOIN anime AS a ON a.studio_id = s.studio_id;
```

### 17) Distinct vs bag semantics
- Task: Genres (set vs bag)
- RA: π_{genre}(ANIME)
- SQL (set):
```sql
SELECT DISTINCT genre FROM anime;
```
- SQL (bag):
```sql
SELECT genre FROM anime;
```

### 18) Multi-join chain
- Task: Character names with their anime title and studio name
- RA: π_{c.name, a.title, s.name}( (CHARACTERS c ⋈ ANIME a) ⋈ STUDIOS s )
- SQL:
```sql
SELECT c.name AS character_name, a.title AS anime_title, s.name AS studio_name
FROM characters AS c
JOIN anime AS a ON a.anime_id = c.anime_id
JOIN studios AS s ON s.studio_id = a.studio_id;
```

### 19) Division (÷) — cover all required genres
- Task: Studios whose anime cover all genres in {'Fantasy','Action'}
- RA: π_{studio_id}( π_{studio_id,genre}(ANIME) ÷ REQUIRED_GENRES )
- SQL:
```sql
WITH required_genres(genre) AS (
  SELECT 'Fantasy' UNION ALL
  SELECT 'Action'
)
SELECT a.studio_id
FROM anime AS a
GROUP BY a.studio_id
HAVING COUNT(DISTINCT CASE WHEN a.genre IN (SELECT genre FROM required_genres) THEN a.genre END)
       = (SELECT COUNT(*) FROM required_genres);
```

### 20) Semi-join via IN
- Task: Anime that have any episode titled 'Pilot'
- RA: ANIME ⋉ σ_{title='Pilot'}(EPISODES)
- SQL:
```sql
SELECT *
FROM anime
WHERE anime_id IN (
  SELECT e.anime_id
  FROM episodes AS e
  WHERE e.title = 'Pilot'
);
```

### 21) Anti-join via NOT EXISTS
- Task: Studios with no anime after 2015
- RA: STUDIOS ▷ σ_{release_year>2015}(ANIME)
- SQL:
```sql
SELECT *
FROM studios AS s
WHERE NOT EXISTS (
  SELECT 1
  FROM anime AS a
  WHERE a.studio_id = s.studio_id
    AND a.release_year > 2015
);
```

### 22) Aggregation with multiple measures (γ)
- Task: Per studio: number of titles and latest release year
- RA: γ_{studio_id; COUNT(*)→n, MAX(release_year)→latest}(ANIME)
- SQL:
```sql
SELECT studio_id,
       COUNT(*) AS num_titles,
       MAX(release_year) AS latest_year
FROM anime
GROUP BY studio_id;
```

### 23) Self-join
- Task: Pairs of anime from the same studio
- RA: ρ_{A←ANIME}(ANIME) ⋈_{A.studio_id=B.studio_id ∧ A.anime_id<>B.anime_id} ρ_{B←ANIME}(ANIME)
- SQL:
```sql
SELECT A.title AS title1, B.title AS title2, A.studio_id
FROM anime AS A
JOIN anime AS B ON B.studio_id = A.studio_id AND B.anime_id <> A.anime_id;
```

### 24) Group filter on attribute and aggregate
- Task: Studios with average release year >= 2010 over Action anime only
- RA: γ_{studio_id; AVG(release_year)→avg_y}( σ_{genre='Action'}(ANIME) ); σ_{avg_y>=2010}(...)
- SQL:
```sql
SELECT studio_id, AVG(release_year) AS avg_y
FROM anime
WHERE genre = 'Action'
GROUP BY studio_id
HAVING AVG(release_year) >= 2010;
```

### 25) Projection after join
- Task: List distinct studio names that have characters named 'Chihiro'
- RA: π_{s.name}( σ_{c.name='Chihiro'}( (CHARACTERS c ⋈ ANIME a) ⋈ STUDIOS s ) )
- SQL:
```sql
SELECT DISTINCT s.name
FROM characters AS c
JOIN anime AS a ON a.anime_id = c.anime_id
JOIN studios AS s ON s.studio_id = a.studio_id
WHERE c.name = 'Chihiro';
```

---

Tips:
- Use explicit JOIN ... ON instead of comma joins.
- Remember DISTINCT when mapping π.
- When INTERSECT/EXCEPT are missing, use JOIN/NOT EXISTS idioms.
- Prefer aliases to disambiguate attributes after joins.
