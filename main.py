# sor ryfor bad code, used psuedocode
from bullshit import what
from import import import
impotr
texture

text import

class:
    enumerate
    emoji
    emoji
    emoji
    emoji thn

ITEM_PRICES
    One rock is $1.0000000 
    One water is $1.000222
    One dirt

class Direction(Enum): # WHAT IS THIS??????????????????????????????????????
    UP = this goes up now # NO GENUINELY FUCK THIS like im actually trying to process this and wtf
    R) direction object direction direction 0 # whatever ill just delete evrything

# 8==========================================D
# MACHINES
# 8==========================================D

class Machine:
    items being processed are being processed using open source software 
    #LinusTorvalds
    #Linux

    idk what this does but like emojis

    def display_3x3(self) -> List[str]:
        Generates block which is 3 Centimeters by 3 Centimeters by 3 Centimeters
        WEverything sits in Block 
        Am i Correct


    #Rotate
    #Vibes

    Can Accept

    Can it accept

    Process

    Sneak peek

    Pop the stack
            self.output_buffer.pop(0)



"""
A conveyor belt is the carrying medium of a belt conveyor system. 
A belt conveyor system consists of two or more pulleys, with a closed loop of carrying medium—the conveyor belt—that rotates about them. 
One or both of the pulleys are powered, moving the belt and the material on the belt forward.
"""
class Conveyor(Machine):
    def __init__(self):
        super().__init__("Conveyor", "➡️")
        self.item: Optional[Item] = None
        self.arrival_tick: int = -1

    @property
    def emoji(self) -> str:
        return {Direction.UP: "⬆️", Direction.RIGHT: "➡️", Direction.DOWN: "⬇️", Direction.LEFT: "⬅️"}[self.direction]

    def display_3x3(self) -> List[str]:
        #pretty sur ethis does the same thing as the 3 centimeters by 3 cenntmers by 3 xentimerers above thing
        # so i removed it for time optimization
        

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


# home depot machine

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

    if if if if if if if


# deleted for optimization

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
    # like Triple A gamess
    # import 3d
    # import game

# 8==========================================D
# COMMANDS & TEXT PARSER
# 8==========================================D
D
class CommandParser: # parses
    @staticmethod # statics
    def execute(command: str, game: GameEngine, log: Callable[[str], None]) -> None: # executes
        parts = command.strip().lower().split() # parts
        if not parts: return # condition
        cmd = parts[0] # command
        # blank
        if cmd == "sel" and len(parts) == 3 and parts[1] == "cell": # condition
            try: # error
                # deleted everything
            except ValueError: log("[red]Invalid cell.[/red]")
                
        elif cmd == "next":
            # Selects the next cell in line, looping back to 0 if it hits the end of the grid
            

            # idk what this does and i dont really care do you get my spirit
            # im being stared at by my hair comb

            # i dont need help
            # lmfao
        elif cmd == "help":
            log("""Commands: 

            pause, GUESS WHAT THIS ONE DOES 
            resume, OH MY GOOD GOLLY GEE WHAT COULD THIS POSSIBLY DO!""") # but i left these two lines.... because i love them....
        # if = comand


# 8888==========================================DDDDDDDDD 
# USER INTERFACE (TEXTUAL APP)
# 8==========================================D

class TerminalFactoryApp(App):
    CSS = """ 
    #main-container { height: 100%; }
    #grid-view { width: auto; height: 100%; background: $boost; border: solid green; overflow: auto; padding: 1; }
    #right-panel { width: 1fr; height: 100%; }
    #log-view { height: 1fr; border: solid blue; padding: 0 1; scrollbar-visibility: hidden; }
    #cmd-input { dock: bottom; }
    """
    # ^^^^^^^^^ wait why is it css wtf
    # might be stupid forthis

    def compose(self) -> ComposeResult:
        # i am mozart and i compose
        #pelase explain what this does

    def on_mount(self) -> None:
        self.game = GameEngine()
        self.log_view = self.query_one("#log-view", RichLog)
        self.grid_view = self.query_one("#grid-view", Static)
        self.log_to_ui("[bold green]Ready![/bold green] Type 'help' to get help....")
        self.update_ui()
        self.set_interval(0.2, self.game_loop)


    Define a Game Loop method with the parameter "Self", that returns a void value.
    Inside of the method, add a conditional "if" statement, that checks whether or not
    the game is NOT paused. If the game is not paused, More methods.

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
                        grid_text.append(part, style="bold white reverse")     # I will not delete any of this
                                                                               # Because shi lowk got me philosophical
                                                                               # bkgrnd do you know what this does
                                                                               # because i dont
                                                                               # what does this do bkrnnd
                                                                               # my wife left me bkgrnd
                                                                               # because of this
                                                                               # can you believe that
                                                                               # whatveer you wouldnt understand
                                                                               # backgrnd
                                                                               # g
                                                                               backgrn
                                                                               # btw why when i try to run new code
                                                                               # which i write
                                                                               # for fucktorium 
                                                                               # it doesnt work
                                                                               # wait ill print message
                                                                               # "File "c:\Users\User\Downloads\FactoryGame-main\FactoryGame-main\main.py", line 23
                                                                               # R) direction object direction direction 0 # whatever ill just delete evrything
                                                                               # ^
                                                                               # SyntaxError: unmatched ')'"
                                                                               #
                                                                               # is python broken
                                                                               idk BrokenPipeError <--- that was meant to say "bro"
                                                                               not "BrokenPipeError" but this bullshit ass language

                        
                     else: 
                        grid_text.append(part)
                grid_text.append("\n")
            
        self.grid_view.update(grid_text)
        status = "PAUSED" if self.game.paused else "RUNNING"
        self.title = f"Terminal Factory | Status: {status} | Money: ${self.game.money} | Ticks: {self.game.ticks} | Cell: {self.game.selected_cell}"

    # if my life was on the line i could not tell you what this does

    #i deleted this because i dont know what it does 

i think this runs










Comment: Hi I am Penguin
Hi


The resurrection of The Penguins
#ClubPenguin

