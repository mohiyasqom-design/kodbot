<div align="center">

# 🤖 KodBot

**Free Python Code Hosting, Deployment & Execution — Directly in Telegram**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/bots)
[![Open Source](https://img.shields.io/badge/Open%20Source-❤️-red?style=for-the-badge)](https://opensource.org/)
[![Active Development](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Codebase](https://img.shields.io/badge/Codebase-8%2C000%2B%20Lines-blue?style=for-the-badge)]()

<br/>

> **KodBot** is an open-source Telegram bot that gives every developer — student, hobbyist, or professional — a zero-infrastructure platform to host, deploy, and execute Python applications, entirely from within Telegram.

<br/>

[📖 Documentation](#installation) · [🚀 Features](#-features) · [📊 Statistics](#-project-statistics) · [🗺️ Roadmap](#-roadmap) · [🤝 Contributing](#-contributing)

</div>

---

## 📌 Table of Contents

- [About the Project](#-about-the-project)
- [Features](#-features)
- [Why KodBot](#-why-kodbot)
- [Project Statistics](#-project-statistics)
- [Architecture Overview](#-architecture-overview)
- [Installation](#-installation)
- [Usage](#-usage)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Maintainer](#-maintainer)

---

## 🧩 About the Project

KodBot eliminates the traditional barriers between writing code and running it in production. Instead of managing VPS instances, configuring Docker containers, or navigating cloud dashboards, users interact with a conversational Telegram interface to deploy fully functional Python applications in seconds.

Whether you are a student learning Python, an educator sharing automation scripts, or a developer prototyping a new idea, KodBot provides a consistent, reliable, and completely free execution environment — no credit card, no server setup, no friction.

The platform is built entirely in Python, backed by more than **8,000 lines** of carefully maintained code, and has already powered over **300 real deployments** for a growing community of **1,000+ active users**.

---

## ✨ Features

### 🚀 Deployment & Execution
- **One-command Python deployment** — Submit your script and KodBot handles the rest
- **Live execution environment** — Run Python code directly and receive output in real time
- **Persistent project hosting** — Your deployed applications remain available without intervention
- **Dependency management** — Automatic detection and installation of required packages

### 🛠️ Developer Experience
- **Telegram-native interface** — No web dashboard or CLI required; everything happens in chat
- **Project management panel** — Start, stop, restart, and monitor your deployments
- **Execution logs streaming** — View live stdout/stderr output from within Telegram
- **Multi-project support** — Manage multiple Python applications under a single account

### 🔐 Access & Administration
- **Subscription tier system** — Free and premium plans with configurable resource limits
- **Role-based admin panel** — Full control over users, projects, and platform settings
- **Broadcast system** — Platform-wide announcements with per-user delivery tracking
- **Ticket and support system** — In-bot user support with admin response capabilities

### 🏪 Ecosystem
- **Bot Store (Bazaar)** — Discover and deploy community-shared Python bots and scripts
- **Challenge system** — Gamified coding challenges with leaderboards
- **Lottery system** — Reward mechanics for active community members
- **Referral and invite tracking** — Growth tools built directly into the platform

---

## 💡 Why KodBot

| Problem | Traditional Solution | KodBot |
|---|---|---|
| Running a Python app 24/7 | Rent a VPS, configure SSH, manage uptime | Send your script to the bot |
| Sharing a working bot with others | Publish to GitHub, hope they set it up | Share via Bot Store in one click |
| Learning deployment as a beginner | Navigate AWS/GCP/Docker documentation | Type a command in Telegram |
| Getting execution logs | SSH into server, read log files | Streamed live in your chat window |
| Infrastructure cost | $5–$20/month minimum | Free |

KodBot is built on a core belief: **the gap between writing code and running it should be zero.** It is especially valuable for:

- 🎓 **Students and educators** — Run course projects without any DevOps knowledge
- 🔬 **Experimenters and researchers** — Quickly test ideas with no environment overhead
- 🤖 **Automation builders** — Deploy scrapers, schedulers, and notification bots effortlessly
- 🌍 **Developers in low-resource environments** — No need for expensive cloud accounts

---

## 📊 Project Statistics

<div align="center">

| Metric | Value |
|---|---|
| 📝 Lines of Code | 8,000+ |
| 🚀 Projects Deployed | 300+ |
| 👥 Active Users | ~1,000 and growing |
| 🔄 Release Cadence | Frequent updates |
| 🐍 Primary Language | Python |
| 📦 Bot Platform | Telegram Bot API |

</div>

The platform has seen consistent month-over-month growth in both user registrations and active deployments since its initial release, demonstrating strong product-market fit within the developer and student communities on Telegram.

---

## 🏛️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        Telegram API                         │
│              (Incoming updates & outgoing messages)         │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                      KodBot Core                            │
│                                                             │
│  ┌─────────────┐   ┌──────────────┐   ┌─────────────────┐  │
│  │   Update    │   │    State     │   │   Admin Panel   │  │
│  │  Dispatcher │──▶│   Machine    │   │   & Broadcast   │  │
│  └─────────────┘   └──────┬───────┘   └─────────────────┘  │
│                           │                                 │
│  ┌────────────────────────▼────────────────────────────┐   │
│  │               Feature Modules                        │   │
│  │                                                      │   │
│  │  [Deployment]  [Subscriptions]  [Challenges]        │   │
│  │  [Bot Store]   [Lottery]        [Tickets]           │   │
│  │  [Broadcast]   [Referrals]      [Log Streaming]     │   │
│  └────────────────────────┬────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────▼────────────────────────────┐   │
│  │           Data & Execution Layer                     │   │
│  │                                                      │   │
│  │        SQLite Database (persistent storage)          │   │
│  │        Subprocess Executor (code runner)             │   │
│  │        Shared HTTP Session (Telegram API calls)      │   │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Key design principles:**
- **Single-process architecture** with a robust watchdog auto-restart mechanism
- **Context manager-based database access** to prevent connection leaks
- **Exponential backoff** and HTTP 429 detection on all outbound API calls
- **Persisted settings** — platform configuration survives restarts without manual reconfiguration

---

## ⚙️ Installation

### Prerequisites

- Python 3.10 or higher
- A Telegram Bot Token (obtain from [@BotFather](https://t.me/BotFather))
- `pip` package manager

### 1. Clone the Repository

```bash
git clone https://github.com/mohiyasqom-design/kodbot.git
cd kodbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file in the project root:

```env
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_ID=your_telegram_user_id_here
DB_PATH=kodbot.db
```

### 4. Initialize the Database

```bash
python kodbot.py --init-db
```

### 5. Run the Bot

```bash
python kodbot.py
```

For production deployments, it is recommended to run KodBot under a process manager such as `systemd`, `supervisor`, or a cloud platform like [Railway](https://railway.app).

---

## 🖥️ Usage

Once the bot is running, users interact with it entirely through Telegram.

### For End Users

| Command / Action | Description |
|---|---|
| `/start` | Register and access the main menu |
| **Deploy a Project** | Upload your Python file and follow the prompts |
| **View My Bots** | Manage all your deployed applications |
| **Bot Store** | Browse and install community-shared scripts |
| **Challenges** | Join active coding challenges |
| **Support Ticket** | Open a support request with the team |

### For Administrators

Admins access an extended control panel directly in Telegram with capabilities including:

- User management and subscription control
- Platform-wide broadcast messages (text, image, file)
- Challenge and lottery creation and management
- Bot Store approval and moderation
- Real-time statistics and deployment logs

---

## 🗺️ Roadmap

The following features and improvements are planned for upcoming releases:

- [ ] **REST API layer** — Programmatic access to deployment and management functions
- [ ] **Multi-language support** — Expand execution environments beyond Python (Node.js, Go)
- [ ] **Web dashboard** — Optional browser-based UI alongside the Telegram interface
- [ ] **Webhook-based deployment triggers** — GitHub/GitLab push-to-deploy integration
- [ ] **Resource usage metrics** — Per-project CPU and memory reporting
- [ ] **Collaborative projects** — Multi-user access to shared deployments
- [ ] **Scheduled execution** — Cron-style scheduling for Python scripts
- [ ] **Internationalization (i18n)** — Full multi-language bot interface

Suggestions and feature requests from the community are always welcome. Please open an [Issue](https://github.com/mohiyasqom-design/kodbot/issues) to start the conversation.

---

## 🤝 Contributing

Contributions of all kinds are welcome and appreciated. KodBot is a community project and grows stronger with every pull request, bug report, and idea shared.

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature-name`
3. **Commit** your changes with a clear message: `git commit -m "feat: add your feature"`
4. **Push** to your branch: `git push origin feature/your-feature-name`
5. **Open a Pull Request** against the `main` branch

### Contribution Guidelines

- Follow [PEP 8](https://peps.python.org/pep-0008/) style conventions
- Write clear, descriptive commit messages
- Include comments for non-obvious logic
- Test your changes before submitting
- Update documentation where applicable

### Reporting Bugs

Please use the [GitHub Issues](https://github.com/mohiyasqom-design/kodbot/issues) tracker with the following information:
- A clear and descriptive title
- Steps to reproduce the behavior
- Expected vs. actual behavior
- Python version and operating system

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for full details.

You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, provided the original copyright notice and permission notice are included in all copies or substantial portions of the software.

---

## 👤 Maintainer

<div align="center">

**KodBot** is designed, developed, and actively maintained by:

### [@mohiyasqom-design](https://github.com/mohiyasqom-design)

*Primary developer, architect, and project lead*

<br/>

If you find this project useful, please consider giving it a ⭐ on GitHub — it helps others discover the project and motivates continued development.

<br/>

[![GitHub](https://img.shields.io/badge/GitHub-mohiyasqom--design-181717?style=for-the-badge&logo=github)](https://github.com/mohiyasqom-design)

</div>

---

<div align="center">

**Made with ❤️ for the open-source community**

*KodBot — Because running code should never be the hard part.*

</div>
