# GTC 2026 Schedule Planner — Agentic Runbook

> **Purpose:** This document is a self-contained instruction set for an AI agent to autonomously build a finalized GTC 2026 personal schedule. It contains all context, constraints, data locations, decision rules, and step-by-step tasks. No user interaction should be needed until the final review step.

---

## CONTEXT

The user is attending NVIDIA GTC 2026 (March 16–19, San Jose Convention Center). They have already selected 17 sessions ("Plan A") exported as a CSV. They want:

1. **Plan B alternates** — a curated backup session for each Plan A time slot
2. **A side-by-side comparison** in Markdown and CSV format for iteration
3. **A 1-page printable PDF-ready schedule** once choices are locked in
4. **An interactive HTML dashboard** as the final deliverable

---

## USER PREFERENCES & HARD CONSTRAINTS

### Interest Areas (priority order)
1. Robotics — Isaac Sim, Isaac ROS, Isaac Lab, GR00T
2. Physical AI — embodied agents, manipulation, sim-to-real
3. Computer Vision — VLMs, video analytics, Metropolis
4. NVIDIA Cosmos — world foundation models, synthetic data
5. NVIDIA Omniverse — digital twins, simulation
6. Agentic AI — long-horizon agents, reasoning
7. LLM evaluation / optimization — compression, deployment

### Decision Rules for Plan B Selection
- **DO NOT hallucinate session names.** Every Plan B session MUST come from verified catalog data (scraped JSONs or live catalog search).
- **Limit total Training Labs to 2–3 across the entire week.** Replace excess labs with talks, panels, or tutorials.
- **Prefer non-lab formats for Plan B:** talks > panels > tutorials > labs.
- **Same-day same-slot:** Plan B must occur on the SAME day and overlap the Plan A time window (±30 min OK).
- **Travel buffer:** Allow 20–30 min between consecutive sessions at different buildings.
- **No back-to-back heavy labs.** If Plan A has a lab, Plan B should be a talk or panel.
- **Networking slots are valid Plan B options** (Expo Hall sweeps, breakfast networking) — especially on Monday afternoon and Thursday afternoon.

### Daily Themes
- **Monday (Mar 16):** Foundations & Context. Highly applied coding labs (VLMs, Vision, Robotics) are welcome.
- **Tuesday (Mar 17):** Vision & Agents. Deep dive into VLA, synthetic data, enterprise agents.
- **Wednesday (Mar 18):** Scaling to Production. Surgical robots, humanoids (GR00T), edge panels.
- **Thursday (Mar 19):** Wrap-up & Travel. Avoid 4-hour hackathons if user has evening flight.

### Output Format Preferences
- Iterate using **Markdown tables** and **CSV files** (not HTML) until schedule is finalized
- Include **session URLs** in all iteration files (format: `https://www.nvidia.com/gtc/session-catalog/sessions/gtc26-{code_lowercase}/`)
- Include **daily strategy notes** at the top of every Markdown iteration file
- Final PDF should fit on **1 page** with columns: Time, Title, Brief Summary, Location

---

## DATA LOCATIONS

All files are in: `/Users/aloksh/Documents/sandbox/gtc_schedule_2026/`

### Source of Truth
| File | What it contains |
|------|-----------------|
| `current_schedule_gtc26.csv` | User's confirmed Plan A sessions (17 rows). Columns: Status, Session Title, Session Code, Date, Start Time, End Time, Room |
| `scraped/*.json` | 10 JSON files scraped from NVIDIA GTC catalog website |

### Scraped Files Detail
The `scraped/` directory contains:
- **6 individual session pages** (filenames contain `gtc26-{code}`): S82391, S81742, S81750, S81713, P81219, EX82385
- **4 catalog index pages** (contain listings of many sessions with partial data — titles, codes, brief descriptions, times)

### Session Data Structure in JSON Files
Each individual session JSON has:
- `metadata.title` — full session title
- `metadata.keywords` — includes session code, speaker names
- `metadata.description` or `metadata.og:description` — brief description
- `markdown` field — full page content including:
  - Time/date block: pattern `"Day, March DD  |  HH:MM a.m. - HH:MM p.m. PDT"`
  - Location: appears after the time/date block
  - Description: paragraph before `**Industry:**`
  - Technology keywords: after `**NVIDIA Technology:**`
  - Topic: after `**Topic:**`
  - Session type: between `"Back to Session Catalog"` and `"In-Person"`

### URL Format
```
https://www.nvidia.com/gtc/session-catalog/sessions/gtc26-{session_code_lowercase}/
```
Example: Code `S82391` → `https://www.nvidia.com/gtc/session-catalog/sessions/gtc26-s82391/`

---

## EXECUTION STEPS

### Phase 1: Environment Verification
```
ACTION: Run `python3 --version` to confirm terminal works.
EXPECTED: Python 3.x version string printed.
IF FAIL: Notify user that terminal is non-functional and ask them to verify.
```

### Phase 2: Extract Master Session Database
```
ACTION: Run `python3 extract_sessions_to_csv.py` in the workspace directory.
EXPECTED: Creates `all_gtc_sessions.csv` with columns: Session ID, Title, Type, Day/Date, Time, Topic, Keywords, Brief, Link.
VERIFY: Open `all_gtc_sessions.csv` and confirm it has rows with real session data.
NOTE: The script `extract_sessions_to_csv.py` already exists at the workspace root. It is ready to run with zero dependencies (stdlib only).
```

### Phase 3: Assess Data Sufficiency
```
ACTION: Count the number of valid sessions in `all_gtc_sessions.csv`.
DECISION POINT:
  - IF >= 30 sessions across all days → Proceed to Phase 4.
  - IF < 30 sessions → We need more data. Proceed to Phase 3B.
```

### Phase 3B: Scrape Additional Sessions (if needed)
```
ACTION: Search the NVIDIA GTC catalog for sessions matching user interests.
TARGETS: Search catalog pages filtered by:
  - Topic: Robotics, Computer Vision, Agentic AI
  - Key Themes: Physical AI and Robotics
  - Session Type: Talk, Panel, Tutorial (NOT Training Labs unless directly Isaac/Cosmos related)
  - In-Person only
TOOL: Use browser or `read_url_content` to fetch:
  https://www.nvidia.com/gtc/session-catalog/?topics=Robotics&formats=In-Person
  https://www.nvidia.com/gtc/session-catalog/?topics=Computer+Vision+%2F+Video+Analytics&formats=In-Person
  https://www.nvidia.com/gtc/session-catalog/?keyThemes=Physical+AI+and+Robotics&formats=In-Person
ACTION: Parse resulting pages for session titles, codes, times, and descriptions.
ACTION: Append new sessions to `all_gtc_sessions.csv`.
```

### Phase 4: Select Plan B Alternates
```
ACTION: For each of the 17 Plan A time slots in `current_schedule_gtc26.csv`:
  1. Filter `all_gtc_sessions.csv` for sessions on the SAME DAY.
  2. Find sessions whose time overlaps the Plan A slot (±30 min tolerance).
  3. Rank by relevance to user interests (see preference list above).
  4. Apply the decision rules (no back-to-back labs, prefer talks/panels, etc.).
  5. Select the top candidate as Plan B.
  6. For slots with no viable catalog match, use "Expo Hall / Networking" or "Open Slot" as Plan B.
OUTPUT: Write `plan_b_verified.csv` with columns: Date, Time, Plan A Code, Plan A Title, Plan B Code, Plan B Title, Plan B Type, Plan B Link, Selection Rationale.
```

### Phase 5: Generate Iteration 2 Files
```
ACTION: Create `gtc2026_schedule_iteration_2.md` with:
  - Daily strategy section at the top
  - Side-by-side table per day: Time | Location | Plan A | Plan B
  - All session titles are hyperlinked to their GTC URLs
  - Brief (1-line) description for each session
ACTION: Create `gtc2026_schedule_iteration_2.csv` with:
  - Columns: Date, Time, Location, Plan A Title, Plan A Type, Plan A URL, Plan B Title, Plan B Type, Plan B URL
VERIFY: Every Plan B title exists in `all_gtc_sessions.csv` or is explicitly "Networking/Open Slot".
VERIFY: Every URL resolves (check format matches pattern, don't need to test HTTP).
```

### Phase 6: Notify User for Review
```
ACTION: Use notify_user to present `gtc2026_schedule_iteration_2.md` for review.
MESSAGE: "Iteration 2 is ready with verified Plan B alternates. Please review and tell me which slots to lock in. Once you've chosen Plan A or B for each slot, I'll generate the 1-page printable and the final dashboard."
BLOCKED: Wait for user feedback.
```

### Phase 7: Generate Final 1-Page Printable Schedule
```
TRIGGER: User has confirmed final choices for all slots.
ACTION: Create `gtc2026_final_schedule.md` with ONLY the chosen sessions:
  - Title: "My GTC 2026 Schedule"
  - Compact table with columns: Time | Session | Summary | Location
  - Grouped by day with minimal whitespace
  - Designed to fit on a single printed page
ACTION: Create `gtc2026_final_schedule.csv` with the same data.
```

### Phase 8: Generate Final HTML Dashboard
```
ACTION: Update `generate_dashboard.py` to read from `gtc2026_final_schedule.csv`.
ACTION: Remove all hardcoded alternates dictionary — read everything from CSVs.
ACTION: Run `python3 generate_dashboard.py` to produce final `dashboard.html`.
VERIFY: Open dashboard in browser and confirm all links work.
```

---

## ANTI-PATTERNS TO AVOID

1. **NEVER invent session titles.** If a session doesn't exist in the CSV/JSON data, do not fabricate one.
2. **NEVER reuse the same URL for multiple Plan B sessions.** Each session has a unique code and URL.
3. **NEVER place a session on a day it doesn't actually occur.** Always verify the day/date from source data.
4. **DO NOT run long-running operations without progress feedback.** Always add print statements or progress bars to scripts.
5. **DO NOT modify `current_schedule_gtc26.csv`.** It is the user's source of truth and should only be read, never written.
6. **SAVE all scripts to the workspace directory** (`/Users/aloksh/Documents/sandbox/gtc_schedule_2026/`), never to `/tmp/`.

---

## SUCCESS CRITERIA

The task is complete when:
- [ ] `all_gtc_sessions.csv` exists with verified session data
- [ ] `gtc2026_schedule_iteration_2.md` + `.csv` exist with verified (non-hallucinated) Plan B alternates
- [ ] User has reviewed and approved final slot choices
- [ ] `gtc2026_final_schedule.md` exists as a 1-page printable format
- [ ] `dashboard.html` is regenerated from verified data
- [ ] All Plan B session URLs are unique and correctly formatted
