# Factory Game 🏭

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/a9830512-5af2-43ef-a0e8-a17abd680bf7" />


A lightweight, terminal-based factory simulation game built with Python and the [Textual](https://github.com/Textualize/textual) TUI framework. Build production lines,  process materials, and make "money"!

---

## Features ✨

* **Interactive Terminal UI:** Powered by Textual with a sleek split-panel layout.
* **Factory Grid:** A 23x16 building area with visual item tracking and machine states.
* **Machines & Production:**
  * **Depot (`🪨`):** Automatically mines and outputs raw rocks.
  * **Furnace (`🔥`):** Smelts raw rocks into bricks.
  * **Press (`⚙️`):** Presses bricks into high-value gems.
  * **Seller (`💰`):** Converts processed goods into cold hard cash.
  * **Conveyor (`➡️`):** Transports items across the grid in four rotatable directions.
* **Simulation Engine:** Real-time tick system handling item transportation, production queues, and inventory buffers.

---

## Installation 📦

Make sure you have Python 3.8+ installed, then install the required dependencies:

```bash
pip install textual rich
```

if this isnt obvious, its vibecoded but i will be making HUMAN updates, and HUMAN edits to this game.
