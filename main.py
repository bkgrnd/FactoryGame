# ==========================================
# FACTORY GAME (FACTORIO LITE)
# ==========================================

from enum import Enum
from typing import List, Optional, Any, Callable
from textual.app import App, ComposeResult
from textual.widgets import Input, RichLog, Static, Header
from textual.containers import Horizontal, Vertical
from rich.text import Text

# ==========================================
# STUFF AND THINGS (ITEMS & DIRS)
# ==========================================

class Item(Enum):
    # The different types of items that can be moved and processed in the factory
    ROCK = "🪨"
    SMELTED = "🧱"
    PRESSED = "💎"

ITEM_PRICES = {
    Item.ROCK: 1,
    Item.SMELTED: 2,
    Item.PRESSED: 3
}

class Direction(Enum):
    # Cardinal directions used for machine output and conveyor movement
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

# ==========================================
# MACHINES
# ==========================================

class Machine:
    def __init__(self, name: str, base_emoji: str):
        self.name = name
        self._base_emoji = base_emoji
        self.direction = Direction.RIGHT  
        self.input_buffer: List[Item] = []   # Items waiting to be processed inside this machine
        self.output_buffer: List[Item] = []  # Finished items waiting to leave this machine
        self.max_input = 1
        self.max_output = 1

    @property
    def emoji(self) -> str:
        return self._base_emoji

    def display_3x3(self) -> List[str]:
        # Generates the 3x3 visual block representation of the machine for the UI grid
        top, bottom, left, right = " ┌┐ ", " └┘ ", " ", " "
        if self.direction == Direction.UP: top = " ⇡⇡ "
        elif self.direction == Direction.DOWN: bottom = " ⇣⇣ "
        elif self.direction == Direction.LEFT: left = "⇠"
        elif self.direction == Direction.RIGHT: right = "⇢"
        return [top, f"{left}{self.emoji}{right}", bottom]

    def rotate(self) -> None:
        # Changes the direction the machine outputs items (rotates clockwise)
        dirs = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        self.direction = dirs[(dirs.index(self.direction) + 1) % 4]

    def can_accept(self, item: Item) -> bool:
        # Checks if this machine has room to take in a new item
        return False

    def accept(self, item: Item, current_tick: int) -> None:
        # Puts an incoming item into the machine's input storage
        self.input_buffer.append(item)

    def process(self, current_tick: int, game_state: Any, log: Callable[[str], None]) -> None:
        # Main logic loop for what the machine does on every game tick
        pass

    def peek_output(self, current_tick: int) -> Optional[Item]:
        # Looks at the first finished item ready to leave without removing it yet
        return self.output_buffer[0] if self.output_buffer else None

    def pop_output(self) -> None:
        # Permanently removes/takes out the finished item once it successfully moves to a neighbor
        if self.output_buffer:
            self.output_buffer.pop(0)


class Conveyor(Machine):
    def __init__(self):
        super().__init__("Conveyor", "➡️")
        self.item: Optional[Item] = None
        self.arrival_tick: int = -1

    @property
    def emoji(self) -> str:
        return {Direction.UP: "⬆️", Direction.RIGHT: "➡️", Direction.DOWN: "⬇️", Direction.LEFT: "⬅️"}[self.direction]

    def display_3x3(self) -> List[str]:
        i = self.item.value if self.item else "  "
        if self.direction == Direction.UP: return [f" {i} ", f" {self.emoji} ", "    "]
        if self.direction == Direction.DOWN: return ["    ", f" {self.emoji} ", f" {i} "]
        if self.direction == Direction.RIGHT: return ["    ", f"{self.emoji}{i}", "    "]
        if self.direction == Direction.LEFT: return ["    ", f"{i}{self.emoji}", "    "]
        return ["    ", "    ", "    "]

    def can_accept(self, item: Item) -> bool:
        # A conveyor can only take an item if it's completely empty
        return self.item is None

    def accept(self, item: Item, current_tick: int) -> None:
        # Places the item onto the belt and records the exact tick it arrived
        self.item = item
        self.arrival_tick = current_tick  

    def peek_output(self, current_tick: int) -> Optional[Item]:
        # Only lets the item move forward if a tick has passed since it landed here
        return self.item if self.item and current_tick > self.arrival_tick else None

    def pop_output(self) -> None:
        # Clears the item off the conveyor once it moves to the next cell
        self.item = None


class Depot(Machine):
    def __init__(self):
        super().__init__("Depot", "🪨")
        self.last_gen = 0
        self.max_output = 999999

    def process(self, current_tick: int, game_state: Any, log: Callable[[str], None]) -> None:
        # Automatically spawns a raw rock item every 3 ticks
        if current_tick - self.last_gen >= 3:
            self.output_buffer.append(Item.ROCK)
            self.last_gen = current_tick


class Furnace(Machine):
    def __init__(self):
        super().__init__("Furnace", "🔥")
        self.process_time = 2
        self.processing_item = None
        self.start_tick = 0

    def can_accept(self, item: Item) -> bool:
        # Furnaces only accept raw rocks and only if they aren't already full
        return item == Item.ROCK and len(self.input_buffer) < self.max_input

    def process(self, current_tick: int, game_state: Any, log: Callable[[str], None]) -> None:
        # Smelts raw rocks into bricks over a set amount of time
        if self.processing_item:
            if current_tick - self.start_tick >= self.process_time:
                if len(self.output_buffer) < self.max_output:
                    self.output_buffer.append(Item.SMELTED)
                    self.processing_item = None
        elif self.input_buffer:
            self.input_buffer.pop(0)
            self.processing_item = Item.ROCK
            self.start_tick = current_tick


class Press(Machine):
    def __init__(self):
        super().__init__("Press", "⚙️")
        self.process_time = 2
        self.processing_item = None
        self.start_tick = 0

    def can_accept(self, item: Item) -> bool:
        # Presses only accept smelted bricks and only if they have space
        return item == Item.SMELTED and len(self.input_buffer) < self.max_input

    def process(self, current_tick: int, game_state: Any, log: Callable[[str], None]) -> None:
        # Presses bricks into high-value gems over a set amount of time
        if self.processing_item:
            if current_tick - self.start_tick >= self.process_time:
                if len(self.output_buffer) < self.max_output:
                    self.output_buffer.append(Item.PRESSED)
                    self.processing_item = None
        elif self.input_buffer:
            self.input_buffer.pop(0)
            self.processing_item = Item.SMELTED
            self.start_tick = current_tick


class Seller(Machine):
    def __init__(self):
        super().__init__("Seller", "💰")

    def can_accept(self, item: Item) -> bool:
        # Sellers accept any finished item to convert into money
        return True

    def process(self, current_tick: int, game_state: Any, log: Callable[[str], None]) -> None:
        # Sells items currently sitting in the input buffer and adds cash to player balance
        while self.input_buffer:
            item = self.input_buffer.pop(0)
            price = ITEM_PRICES.get(item, 0)
            game_state.money += price
            log(f"[green]Sold {item.value} for ${price}![/green]")

# ==========================================
# THE MAP & GAME ENGINE
# ==========================================

class Cell:
    def __init__(self, cell_id: int):
        self.id = cell_id
        self.machine: Optional[Machine] = None


class FactoryGrid:
    def __init__(self, cols: int, rows: int):
        self.cols = cols
        self.rows = rows
        self.cells = [Cell(i) for i in range(cols * rows)]

    def get_neighbor(self, cell_id: int, direction: Direction) -> Optional[Cell]:
        # Finds and returns the adjacent grid cell in a given direction
        x, y = cell_id % self.cols, cell_id // self.cols
        dx, dy = direction.value
        nx, ny = x + dx, y + dy
        return self.cells[ny * self.cols + nx] if 0 <= nx < self.cols and 0 <= ny < self.rows else None


class GameEngine:
    def __init__(self):
        self.money = 0
        self.ticks = 0
        self.paused = False
        self.selected_cell = 0
        # Increased columns from 20 to 23 (+3 columns)
        self.grid = FactoryGrid(cols=23, rows=16)

    def tick(self, log_callback: Callable[[str], None]) -> None:
        # Advances the game simulation by one frame (runs machine actions and item transport)
        if self.paused: return
        self.ticks += 1
        
        # Step 1: Run internal production/logic for all machines
        for cell in self.grid.cells:
            if cell.machine: cell.machine.process(self.ticks, self, log_callback)
                
        # Step 2: Try moving items from machine outputs into adjacent machine inputs
        for cell in self.grid.cells:
            if cell.machine:
                item = cell.machine.peek_output(self.ticks)
                if item:
                    neighbor = self.grid.get_neighbor(cell.id, cell.machine.direction)
                    if neighbor and neighbor.machine and neighbor.machine.can_accept(item):
                        neighbor.machine.accept(item, self.ticks)
                        cell.machine.pop_output()

# ==========================================
# COMMANDS & TEXT PARSER
# ==========================================

class CommandParser:
    @staticmethod
    def execute(command: str, game: GameEngine, log: Callable[[str], None]) -> None:
        parts = command.strip().lower().split()
        if not parts: return
        cmd = parts[0]
        
        if cmd == "sel" and len(parts) == 3 and parts[1] == "cell":
            try:
                cid = int(parts[2])
                if 0 <= cid < len(game.grid.cells):
                    game.selected_cell = cid
                    log(f"Selected cell {cid}.")
                else: log("[red]Invalid cell.[/red]")
            except ValueError: log("[red]Invalid cell.[/red]")
                
        elif cmd == "next":
            # Selects the next cell in line, looping back to 0 if it hits the end of the grid
            game.selected_cell = (game.selected_cell + 1) % len(game.grid.cells)
            log(f"Selected cell {game.selected_cell}.")

        elif cmd == "set" and len(parts) == 2:
            mtype = parts[1]
            cell = game.grid.cells[game.selected_cell]
            if cell.machine:
                log("[red]Cell already occupied.[/red]")
                return
            
            machines = {"depot": Depot, "furnace": Furnace, "press": Press, "seller": Seller, "conveyor": Conveyor}
            if mtype in machines:
                cell.machine = machines[mtype]()
                log(f"Placed {mtype.title()} at cell {game.selected_cell}.")
            else:
                log("[red]Unknown machine type.[/red]")

        elif cmd == "rotate":
            cell = game.grid.cells[game.selected_cell]
            if cell.machine:
                cell.machine.rotate()
                log(f"Rotated {cell.machine.name}. Now outputs: {cell.machine.direction.name}")
            else: log("[red]No machine here to rotate.[/red]")
            
        elif cmd == "remove":
            game.grid.cells[game.selected_cell].machine = None
            log(f"Removed machine on cell {game.selected_cell}.")
            
        elif cmd == "help":
            log("""Commands: 
            sel cell <id>, lets you select cell
            next, selects the next cell
            set <depot|furnace|press|seller|conveyor>, sets the sell
            rotate, rotates the cell
            remove, removes the machine on the cell
            amirich, shows how many coins you have
            tick, manual tick
            pause, GUESS WHAT THIS ONE DOES
            resume, OH MY GOOD GOLLY GEE WHAT COULD THIS POSSIBLY DO!""")
        elif cmd == "amirich": log(f"Current Money: ${game.money}")
        elif cmd == "tick": game.tick(log); log("Manual tick.")
        elif cmd == "pause": game.paused = True; log("paused.")
        elif cmd == "resume": game.paused = False; log("resumed.")
        else: log("[red]Unknown command.[/red]")

# ==========================================
# USER INTERFACE (TEXTUAL APP)
# ==========================================

class TerminalFactoryApp(App):
    CSS = """
    #main-container { height: 100%; }
    #grid-view { width: auto; height: 100%; background: $boost; border: solid green; overflow: auto; padding: 1; }
    #right-panel { width: 1fr; height: 100%; }
    #log-view { height: 1fr; border: solid blue; padding: 0 1; scrollbar-visibility: hidden; }
    #cmd-input { dock: bottom; }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="main-container"):
            yield Static(id="grid-view")
            with Vertical(id="right-panel"):
                yield RichLog(id="log-view", highlight=True, markup=True)
                yield Input(placeholder="Type 'help' to get help...", id="cmd-input")

    def on_mount(self) -> None:
        self.game = GameEngine()
        self.log_view = self.query_one("#log-view", RichLog)
        self.grid_view = self.query_one("#grid-view", Static)
        self.log_to_ui("[bold green]Ready![/bold green] Type 'help' to get help....")
        self.update_ui()
        self.set_interval(0.2, self.game_loop)

    def game_loop(self) -> None:
        if not self.game.paused:
            self.game.tick(self.log_to_ui)
            self.update_ui()

    def update_ui(self) -> None:
        # Redraws the expanded game grid interface on the screen
        grid_text = Text()
        for row in range(self.game.grid.rows):
            for line_idx in range(3):
                for col in range(self.game.grid.cols):
                    cell = self.game.grid.cells[row * self.game.grid.cols + col]
                    lines = cell.machine.display_3x3() if cell.machine else ["    ", " ·  ", "    "]
                    part = lines[line_idx]
                    
                    if cell.id == self.game.selected_cell:
                        grid_text.append(part, style="bold white reverse")
                    else:
                        grid_text.append(part)
                grid_text.append("\n")
            
        self.grid_view.update(grid_text)
        status = "PAUSED" if self.game.paused else "RUNNING"
        self.title = f"Terminal Factory | Status: {status} | Money: ${self.game.money} | Ticks: {self.game.ticks} | Cell: {self.game.selected_cell}"

    def log_to_ui(self, message: str) -> None:
        self.log_view.write(message)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        cmd = event.value
        if cmd.strip():
            self.log_to_ui(f"> {cmd}")
            CommandParser.execute(cmd, self.game, self.log_to_ui)
        self.query_one(Input).value = ""
        self.update_ui()

if __name__ == "__main__":
    TerminalFactoryApp().run()
