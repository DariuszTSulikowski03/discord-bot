# Discord Tournament Bot

This Discord bot manages a tournament by tracking user points, daily submissions, and providing useful commands such as ranking, coupon submission, and a points calculator.

## Features

- **Persistent Data Storage:** (In-memory for now; consider a database for production.)
- **Time Zone Handling:** Uses Warsaw time for daily submission limits.
- **Commands Include:**
  - `!kupon [punkty] [link]` – Submit a coupon.
  - `!ranking` – Show the top 10 users.
  - `!kalkulator [typ] [odds] [kwota]` – Calculate points.
  - `!podsumowanie` – Show tournament statistics (Admin only).
  - `!help` – List available commands.

## Setup

### Prerequisites

- Python 3.8+
- pip
- A Discord Bot Token

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/discord-tournament-bot.git
   cd discord-tournament-bot
