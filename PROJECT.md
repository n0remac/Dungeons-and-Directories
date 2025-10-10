# Dungeons and Directories - Project Documentation

## Overview

**Dungeons and Directories** is an innovative top-down dungeon crawler game where dungeon maps are procedurally generated based on folder structures on the player's computer. The game transforms the digital landscape of your file system into an explorable dungeon environment, creating a unique and personalized gaming experience.

## Purpose

The primary goal of this project is to create an engaging 2D dungeon crawler that leverages the unique concept of directory-based map generation. Instead of traditional procedural generation algorithms, the game reads a folder structure from the user's computer and translates it into playable dungeon levels, making each player's experience uniquely tied to their own file system.

## Technical Stack

### Core Technologies
- **Python 3.9+** - Primary programming language
- **Arcade 2.6.8** - 2D game development framework
- **Pymunk Physics Engine** - Physics simulation (integrated with Arcade)

### Development Tools
- **Git** - Version control
- **Virtual Environment (venv)** - Dependency isolation

## Architecture

The project follows a modular, object-oriented architecture organized into distinct components:

### Directory Structure

```
Dungeons-and-Directories/
├── run.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── constants/              # Configuration constants
│   ├── base.py            # Core game constants (sprites, physics)
│   └── screen.py          # Display settings
├── managers/               # Game system managers
│   ├── game_window.py     # Main game loop and window
│   └── physics.py         # Custom physics engine wrapper
├── game_objects/           # Game entities
│   ├── game_object.py     # Base game object class
│   ├── player.py          # Player character
│   └── level.py           # Level generation and management
└── resources/              # Game assets
    └── human.png          # Player sprite
```

### Core Components

#### 1. **Entry Point (`run.py`)**
   - Initializes the game window with configured dimensions
   - Sets up the main game loop using Arcade's runner
   - Entry point for the entire application

#### 2. **Game Window Manager (`managers/game_window.py`)**
   - **Purpose**: Central game loop controller
   - **Responsibilities**:
     - Window management and rendering
     - Input handling (keyboard and mouse)
     - Game state updates
     - Physics step coordination
     - Bullet shooting mechanics
   - **Key Features**:
     - Mouse-based directional shooting
     - WASD movement controls
     - Frame-by-frame physics updates

#### 3. **Physics Engine (`managers/physics.py`)**
   - **Purpose**: Custom wrapper around Pymunk physics engine
   - **Features**:
     - Top-down physics with configurable gravity
     - Collision detection and handling
     - Different physics properties for different object types
     - Collision callbacks for bullet interactions
   - **Physics Types**:
     - `STATIC` - Immovable walls
     - `DYNAMIC` - Movable objects (player, bullets, rocks, gems)
     - Configurable mass, friction, damping, and elasticity

#### 4. **Game Objects**

   **Base GameObject (`game_objects/game_object.py`)**
   - Extends Arcade's Sprite class
   - Foundation for all game entities

   **Player (`game_objects/player.py`)**
   - WASD movement with physics-based forces
   - Sprite rendering and animation
   - Input state tracking
   - Physics force application for smooth movement

   **Level (`game_objects/level.py`)**
   - Level generation and management
   - Sprite list organization (walls, rocks, gems)
   - Currently uses procedural placement
   - **Future**: Directory-based map generation (TODO in code)

#### 5. **Constants (`constants/`)**
   - **base.py**:
     - Sprite scaling and sizing
     - Movement speeds
     - Physics force magnitudes
   - **screen.py**:
     - Window dimensions
     - Game title

## Key Features

### Current Implementation
1. **Physics-Based Movement**
   - Smooth, force-based player movement
   - Realistic friction and damping
   - Collision detection with walls and objects

2. **Combat Mechanics**
   - Mouse-click directional shooting
   - Spacebar for fixed-direction bullets
   - Bullet-object collision with removal
   - Physics-driven projectiles

3. **Interactive Environment**
   - Movable rocks with realistic mass
   - Collectible gems and items
   - Static boundary walls
   - Varied environmental objects

4. **Modular Architecture**
   - Clean separation of concerns
   - Extensible game object system
   - Configurable physics parameters

### Unique Features (Planned)

1. **Directory-Based Map Generation** ⭐
   - Transform folder structures into dungeon layouts
   - Each folder becomes a room or area
   - File types could determine room contents
   - Personalized dungeons based on user's file system

2. **Dynamic Level Scaling**
   - Dungeon complexity based on directory depth
   - Number of rooms correlates to folder count

## Game Flow

1. **Initialization**
   ```python
   run.py → MyWindow.__init__() → setup()
   ```
   - Create player and level instances
   - Initialize physics engine
   - Set up sprite lists

2. **Game Loop** (60 FPS)
   ```
   on_update() → physics.step() → on_draw()
   ```
   - Process input (keyboard/mouse)
   - Update game state
   - Apply physics
   - Render all sprites

3. **Input Processing**
   - **WASD**: Apply directional forces to player
   - **Mouse Click**: Shoot bullet toward cursor
   - **Spacebar**: Shoot bullet in fixed direction

## Physics System

### Object Types and Properties

| Object Type | Mass | Friction | Damping | Body Type | Special Properties |
|-------------|------|----------|---------|-----------|-------------------|
| Player      | 1.0  | 0.6      | 0.01    | DYNAMIC   | MOMENT_INF, max_velocity: 400 |
| Walls       | -    | 0.6      | -       | STATIC    | Immovable |
| Rocks       | 2.0  | 0.8      | 0.1     | DYNAMIC   | Pushable |
| Gems        | 0.5  | 0.8      | 0.4     | DYNAMIC   | Lightweight |
| Bullets     | 0.1-0.2 | 0.6   | 1.0     | DYNAMIC   | High elasticity (0.9) |

### Collision Handlers
- **Bullet → Rock**: Bullet removed, "Rock" printed
- **Bullet → Wall**: Bullet removed, "Wall" printed

## Future Enhancements

Based on code analysis and TODOs:

1. **Tiled Map Integration**
   - Replace procedural level generation with Tiled map editor
   - Enable visual level design

2. **Directory-to-Dungeon Implementation**
   - Core feature: folder structure parsing
   - Dynamic room generation from directories
   - File-based content population

3. **Gameplay Expansion**
   - Enemy AI and combat
   - Inventory system
   - Player progression/stats
   - Save/load functionality

4. **Polish**
   - Sound effects and music
   - Particle effects
   - Enhanced animations
   - UI/HUD elements

## Development Setup

### Prerequisites
- Python 3.9+
- Virtual environment support

### Installation

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```bash
python3.9 -m venv venv
venv/scripts/activate.bat
pip install -r requirements.txt
```

### Running the Game
```bash
python run.py
```

## Controls

- **W/A/S/D** - Move player (up/left/down/right)
- **Mouse Click** - Shoot bullet toward cursor
- **Spacebar** - Shoot bullet to the right

## Dependencies

```
arcade==2.6.8
```

The Arcade library includes:
- Sprite management
- Physics engine (Pymunk)
- Window management
- Input handling
- Resource loading

## Design Patterns

1. **Object-Oriented Design**
   - Inheritance hierarchy (GameObject → Player/Level)
   - Encapsulation of game logic

2. **Manager Pattern**
   - GameWindow manages game state
   - Physics manager handles simulation

3. **Component-Based Architecture**
   - Modular sprite lists
   - Separated rendering/update logic

4. **Event-Driven Input**
   - Key press/release callbacks
   - Mouse event handling

## Performance Considerations

- Sprite lists for efficient batch rendering
- Physics engine with configurable step rate
- Damping to prevent infinite acceleration
- Max velocity limits to prevent physics instability

## Project Status

**Current Phase**: Core mechanics implementation
**Next Milestone**: Directory-based map generation

The project currently has a solid foundation with working physics, player movement, and shooting mechanics. The unique directory-based dungeon generation feature is planned but not yet implemented (as noted in the TODO comment in `level.py`).
