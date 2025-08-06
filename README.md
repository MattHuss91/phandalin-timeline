# Heroes of Phandalin: Campaign Timeline Viewer

An interactive web app built with Streamlit and SQLite to track the timeline of a custom D&D campaign. Players can explore story events through a custom calendar system with fantasy months and world dates.

> **A Future Echoes Project**

---

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
â”œâ”€â”€ .streamlit/
â”‚   â””â”€â”€ config.toml
â”œâ”€â”€ Home.py                  # Main homepage
â”œâ”€â”€ Timeline.py              # Interactive timeline page
â”œâ”€â”€ dnd_campaign.db          # SQLite database of campaign events
â”œâ”€â”€ requirements.txt         # Python dependencies
â””â”€â”€ README.md                # This file
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

## TTRPG Management Tool â€“ Feature Roadmap

| Version | Target Features                                                               | ETA         |
|---------|-------------------------------------------------------------------------------|-------------|
| **V1**  | Character bios and timeline viewer with login-based editing permissions       | âœ” Released  |
| **V2**  | Factions & Locations pages (bios, characters, related events, images)         | Septâ€“Oct    |
| **V3**  | Admin tool to add/edit all SQL data (events, locations, links) in one form    | Late 2025   |
| **V4**  | Interactive map integration for towns/regions with clickable event overlays   | Late 2025   |
| **V5**  | Blank version for public use with config options                              | 2026        |

---

### ðŸš€ Goals

- Organize and track your TTRPG campaigns
- Make information easily accessible for players
- Enable secure collaboration between DMs and players

---

Â© 2025 Matthew Husselbury. All rights reserved.  
**This repository is publicly visible but is not open source.**

You may view and learn from this code for personal use only.  
**Reproduction, modification, distribution, or commercial use is strictly prohibited** without the express written permission of the author.

**Loreweave** is a free TTRPG management tool developed by Matthew Husselbury.  
**Future Echoes** is the creative studio behind its design and development.