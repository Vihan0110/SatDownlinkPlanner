# 🛰️ Satellite Downlink Planner

A Python-based simulation of satellite communication downlinks, packet prioritization, and ground-pass transmission management,featuring a desktop application, SQLite database, and mission-report dashboard.

**Developed by:** Vihan Joshi  
**Technology:** Python · SQLite · Tkinter · HTML · CSS  
**Project type:** Academic Mini Project

---

## 📌 Overview

The Satellite Downlink Planner simulates how data packets can be prioritized and transmitted during limited satellite communication windows.

In real satellite communication systems, available transmission time and signal conditions can affect which packets are transmitted successfully. This project models a simplified version of that process, helping demonstrate object-oriented programming, database management, exception handling, and basic communication scheduling concepts.

## ✨ Features

- **Packet Management:** Add telemetry, image, and voice packets with configurable sizes and urgency levels.
- **Priority-Based Scheduling:** Process waiting packets according to their packet type and urgency.
- **Ground-Pass Simulation:** Simulate a communication pass with a randomly generated signal-strength value and a limited transmission window.
- **Transmission Status:** Track packets as `WAITING`, `SENT`, or `DEFERRED`.
- **SQLite Database:** Store packet details and ground-pass results locally.
- **Mission Report Dashboard:** Generate an HTML report containing packet statistics, transmission statuses, signal information, and ground-pass history.
- **Input Validation:** Handle invalid packet sizes, urgency values, and non-numeric input.
- **Object-Oriented Design:** Demonstrate abstraction, inheritance, polymorphism, and exception handling.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and simulation |
| Tkinter | Desktop graphical user interface |
| SQLite | Local database storage |
| HTML and CSS | Mission report dashboard |
| Python OOP | Packet models and scheduling behavior |

The project uses Python's standard library and does not require a third-party Python package for its core functionality.

## 📂 Project Structure

```text
SatDownlinkPlanner/
├── main.py          # Desktop application and simulation
├── models.py        # Packet classes, priorities and validation
├── database.py      # SQLite database operations
├── website.py       # HTML mission report generator
├── index.html       # HTML dashboard template
├── README.md        # Project documentation
├── .gitignore       # Files excluded from Git
└── satellite.db     # Local database, created at runtime
```

The report generator creates a `website/` directory and writes the generated report to `website/index.html`. The root-level `index.html` is the dashboard template.

## ⚙️ Getting Started

### Prerequisites

- Python 3.10 or newer recommended
- Windows, macOS, or Linux
- Tkinter available in your Python installation

### 1. Clone the repository

```bash
git clone https://github.com/Vihan0110/SatDownlinkPlanner.git
cd SatDownlinkPlanner
```

### 2. Run the application

```bash
python main.py
```

On some systems, use `python3 main.py` instead. On Linux, you may need to install the Tkinter package separately.

### 3. Use the application

1. Choose a packet mode: `TT&C`, `SSTV`, or `Voice`.
2. Enter the packet size in bytes and an urgency level from 1 to 5.
3. Click **Add Packet** to create a packet, or **Random 6** to add sample packets.
4. Click **Run Ground Pass** to simulate a transmission window.
5. Review packet statuses and transmission results.
6. Click **Build Website** to generate the mission report.
7. Open the generated `website/index.html` file in a browser.

**Note:** Signal strength and transmission results are simulated. This application does not connect to real satellites or calculate real orbital trajectories.

## 🧠 Object-Oriented Programming Concepts

- **Abstraction:** The base `Packet` class defines common behavior.
- **Inheritance:** `Telemetry`, `Image`, and `Voice` implement packet-specific behavior.
- **Polymorphism:** Packet types provide their own priority and minimum signal requirements.
- **Encapsulation:** Packet attributes and database operations are organized into classes.
- **Exception Handling:** Invalid input is handled using custom and built-in exceptions.

## 🗄️ Database Design

The SQLite database maintains two main tables:

- **`packets`** — stores packet mode, size, urgency, transmission status, and explanatory notes.
- **`passes`** — stores simulated signal strength, sent and deferred packet counts, and remaining transmission time.

The database is created automatically when the application starts.

## 🚀 Future Improvements

Potential enhancements include:

- An interactive dashboard with packet filtering and search.
- More advanced scheduling algorithms and performance comparisons.
- Configurable ground-station windows and transmission capacities.
- Automated unit tests and improved error handling.
- Charts for packet delivery rates and ground-pass performance.
- A web-based interface for managing simulations.

These are planned enhancements, not claims about features already implemented.

## 🎓 Learning Outcomes

This project provides practical experience with Python programming, object-oriented design, SQLite persistence, desktop GUI development, HTML report generation, and simulation of a simplified packet-transmission workflow.

## 👨‍💻 Author

**Vihan Joshi**

GitHub: [@Vihan0110](https://github.com/Vihan0110)

---

*An educational simulation project. It is intended for learning and demonstration, not operational satellite communication.*
