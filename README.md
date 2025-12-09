<div align="center">

![Alt Text](./assets/logo/terrashark.png)
# 🌊 TerraShark
### *Evolution Meets Emergence*

**A Python-powered ecosystem simulator where life writes its own story**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Docs](#-documentation) • [Contributing](#-contributing)

![Demo GIF](./assets/demo/simulation.gif)

</div>

---

## 🎯 What is TerraShark?

TerraShark simulates **emergent evolution** in procedurally generated worlds. Watch creatures adapt, mutate, and survive—or go extinct—based on inheritable traits like speed, vision, and metabolism. Built for researchers, game devs, and chaos lovers.

> **Note**: This is an experimental research project. Expect breaking changes.

---

## ✨ Features

### 🌍 World Generation
- Procedural heightmaps using Perlin/Simplex noise
- Dynamic biomes: forests, deserts, oceans, tundra
- Resource distribution (food, water, shelter)

### 🧬 Evolutionary Engine
- **Traits**: Speed, sight radius, energy efficiency, reproduction rate
- **Inheritance**: Mendelian genetics with random mutations
- **Natural Selection**: Survival based on fitness, not RNG

### 📊 Real-Time Analytics
- Population dynamics graphs
- Trait distribution heatmaps
- Event logs (births, deaths, mutations)
- CSV export for external analysis

### 🎮 Interactive Controls
- Pause/resume/speed up simulations
- Spawn custom creatures mid-run
- Toggle debug overlays

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Core** | Python 3.10+ |
| **Rendering** | Pygame |
| **Math** | NumPy, SciPy |
| **Visualization** | Matplotlib, Seaborn |
| **Terrain** | noise (Perlin), Pillow |

---

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- pip/pipenv/poetry

### Quick Start
#todo

## 🚀 Usage
#todo

## 📂 Project Structure
```plaintext
    TerraShark/
    ├── README.md
    ├── LICENSE
    ├── requirements.txt
    │
    ├── docs/               
    │   └── roadmap.md
    │
    ├── assets/              # Sprites, icons, images later
    │
    ├── tests/               # Add tests whenever needed
    │
    ├── data/               #all the data from simulation 
    │
    └── src/
        ├── main.py          # Entry point
        │
        ├── core/            # Core systems (terrain, world, config)
        │
        ├── entities/        # Bots/creatures (expand later)
        │
        ├── simulation/      # Logic controlling the world
        │
        ├──display/         #to display the thing happening behind the screen
        │
        └── DMS/         #data management system for storing and performing analysis on data
```

---

## 📖 Documentation
#todo


## 📜 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- [Pygame](https://www.pygame.org) for rendering
- [NumPy](https://numpy.org) for math wizardry
- [Perlin Noise](https://github.com/caseman/noise) for terrain
- Community contributors

---

<div align="center">

**⭐ Star this repo if TerraShark helped you!**

Made with 🔥 by the TerraShark Team

</div>