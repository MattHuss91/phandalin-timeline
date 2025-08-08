

# Loreweave: Phandalin Timeline
https://heroes-of-phandalin.streamlit.app/
> **A Future Echoes Project**
---
Loreweave is a self-hostable campaign database and timeline manager for tabletop RPGs, built with Python, Streamlit, and PostgreSQL. It’s designed to help Dungeon Masters (DMs) manage and present their campaign canon—characters, events, locations, and factions—on a custom 10-month fantasy calendar.

This project also serves as a portfolio piece to demonstrate my skills in:

- Relational data modeling and SQL schema design
- Python development and Streamlit UI design
- Product thinking and user experience planning

---

## Purpose and Audience

**For DMs/Admins**  
Loreweave provides an admin console for creating and editing campaign content. You can manage characters, events, locations, and factions, and link characters to events and factions to track appearances and memberships.

**For Players/Viewers**  
Players can browse the timeline and entity pages in read-only mode. The interface is designed to be clean and intuitive, with no risk of altering the data.

---

## Core Concepts

- **Custom Calendar Backbone**  
  Events are stored using day, month, year, and a calculated world_day value to support in-world chronological sorting and filtering.

- **Single Source of Truth**  
  Structured tables define characters, locations, and factions. Link tables record relationships like appearances and memberships.

- **Readable UI**  
  Forms and selectors show names to users while IDs are handled behind the scenes. Editing is restricted to admins.

---

## Tech Stack

- Python for core logic and data handling  
- Streamlit for the user interface  
- PostgreSQL for the relational database  
- psycopg2 for database connectivity

---
## Current Features

- Create and edit characters, events, locations, and factions  
- Link characters to events and factions  
- Custom calendar with sortable world_day field  
- Admin-only editing access  
- Location and event selectors show names; inserts use IDs

---

## Roadmap

Planned improvements include:

- Read-only views with cards and tables for players  
- Validation and protection against duplicate links  
- Improved event picker labels (Title — Location — Date)  
- Caching and loading spinners for performance  
- Indexing on foreign keys and world_day  
- Optional images/logos for locations and factions  
- Previews of related entities on each page

---

## Deployment and Usage

Loreweave is designed to be self-hostable. Other GMs can clone the repository, configure their database, and run their own instance to manage their campaigns.

> This project is intended for personal and portfolio use.

---

## About Me

I'm Matthew Husselbury, a data analyst with a background in storytelling, systems design, and user-focused development. Loreweave is a tool I built to support my own campaigns and to demonstrate how structured data and thoughtful design can enhance creative projects.

If you're interested in collaborating, using the tool, or just want to talk shop about data and storytelling, feel free to reach out.

© 2025 Matthew Husselbury. All rights reserved.  
**This repository is publicly visible but is not open source.**
