*This activity has been created as part of the 42 curriculum by nalayyou, mjabarin.*


## Description

This project is a recreation of the classic Pac-Man arcade game, developed in Python.

The player controls Pac-Man through procedurally generated mazes, collecting Pacgums and Super-Pacgums while avoiding four ghosts. Super-Pacgums temporarily make ghosts frightened and edible.

The project focuses on object-oriented programming, modular architecture, game logic, maze generation, configuration management, and persistent highscores.

## Features

* Pac-Man movement with keyboard controls
* Procedurally generated mazes
* Pacgums and Super-Pacgums
* Four ghosts with different behaviours
* Frightened ghost mode
* Multiple levels
* Lives and scoring system
* Persistent top-10 highscores
* Main menu and instructions
* Pause, victory, and game-over screens
* Configuration file
* Cheat mode for testing

## Requirements

* Python 3.10+
* Required project dependencies
* Assigned A-Maze-ing maze generator

The project follows the required Python, Flake8, MyPy, type-hinting, and documentation guidelines.

## Installation

Clone the repository and install the dependencies:

```bash
git clone <repository-url>
cd <repository-directory>
make install
```

## Usage

The game is launched with one configuration file:

```bash
python3 pac-man.py config.json
```

The configuration file uses JSON and supports comments beginning with `#`. Invalid configuration values are handled using safe defaults.

### Controls

| Key       | Action     |
| --------- | ---------- |
|  `↑` | Move up    |
|  `↓` | Move down  |
|  `←` | Move left  |
|  `→` | Move right |
| `esc`       | Pause      |

## Configuration

The configuration file controls game parameters such as:

```json
{
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}
```

## Highscore

The game maintains a persistent **top-10 highscore table**.

Scores are saved between game sessions and players can enter their name when the game ends. Player names are limited to 10 alphanumeric characters and spaces, as required by the subject.

## Maze Generation

The project uses the assigned **A-Maze-ing** package to generate the mazes.

The package is used without modification. The first level uses a fixed seed, while subsequent levels use randomly generated mazes.

## Implementation

The game is divided into separate modules responsible for:

* Game and level management
* Player movement
* Ghosts and ghost behaviours
* Maze handling
* Pacgums and Super-Pacgums
* Collision detection
* Scoring
* Configuration
* Highscores
* User interface

Ghost behaviours are separated from the main Ghost class, allowing different behaviours such as chasing and frightened movement to be implemented independently.

## General Software Architecture

The main components communicate approximately as follows:

```text
                 Game
                  |
       +----------+----------+
       |          |          |
    Player      Ghosts      Maze
       |          |
       |      +---+---+
       |      |       |
       |    Chase  Frightened
       |      |
       +------+------+
              |
          Collision
              |
           Scoring
              |
          Highscores
```

This modular structure keeps game logic separated and makes individual components easier to maintain and test.

## Project Management

The project was developed collaboratively by **nalayyou** and **mjabarin**.

Project management documentation, including planning, task distribution, progress tracking, testing, and technical decisions, is available in:

```text
<project-management-directory>
```

The subject requires this documentation to be included in a dedicated project-management directory.

## Resources

* Python documentation
* Documentation for the graphical library used
* A-Maze-ing package documentation
* 42 Pac-Man project subject

AI tools were used as a development aid for understanding concepts, debugging, discussing implementations, and improving documentation. All generated suggestions were reviewed, tested, and adapted by the project members.

The 42 subject specifically requires students to understand and critically review AI-generated content.

