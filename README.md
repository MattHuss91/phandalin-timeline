# Heroes of Phandalin: Campaign Timeline Viewer

An interactive web app built with Streamlit and SQLite to track the timeline of a custom D&D campaign. Players can explore story events through a custom calendar system with fantasy months and world dates.

## Features

- Filter events by in-world date using a slider
- Read short and full summaries for each event
- Uses a custom 10-month fantasy calendar (36-day months)
- Styled with thematic fonts and background

## Tech Stack

- Python
- Streamlit
- SQLite
- GitHub (version control and deployment)
- Streamlit Cloud (hosting)

## Project Structure

```
phandalin-timeline/
├── .streamlit/
│   └── config.toml
├── Home.py                  # Main homepage
├── Timeline.py              # Interactive timeline page
├── dnd_campaign.db          # SQLite database of campaign events
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Getting Started (Locally)

1. Clone the repo:
   ```bash
   git clone https://github.com/MattHuss91/phandalin-timeline.git
   cd phandalin-timeline
   ```

2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   streamlit run Home.py
   ```

## TTRPG Management Tool – Feature Roadmap

| Version | Target Features                                                               | ETA         |
|---------|-------------------------------------------------------------------------------|-------------|
| **V1**  | Character bios and timeline viewer with login-based editing permissions       | ✔ Released  |
| **V2**  | Factions & Locations pages (bios, characters, related events, images)         | Sept–Oct    |
| **V3**  | Admin tool to add/edit all SQL data (events, locations, links) in one form    | Late 2025   |
| **V4**  | Interactive map integration for towns/regions with clickable event overlays   | Late 2025   |
| **V5**  | Blank version for public use with config options                              | 2026        |
---

### Goals

- Organize and track your TTRPG campaigns
- Make information easily accessible for players
- Enable secure collaboration between DMs and players
