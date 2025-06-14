import tkinter as tk
from tkinter import messagebox
import random
from tkinter import font as tkfont
import time

class GameConfig:
    # Game configuration
    MAX_FUEL = 150
    MAX_FOOD = 150
    MAX_SHIP_INTEGRITY = 100
    STARTING_DISTANCE = 1500
    
    # Starting resources
    STARTING_CREW = 3
    STARTING_FUEL = 100
    STARTING_FOOD = 100
    STARTING_CREDITS = 75
    STARTING_SHIP_PARTS = 1
    
    # Crew settings
    CREW_HIRE_COST = 25
    CREW_HIRE_CHANCE = 0.6
    CREW_HIRE_MAX = 8
    
    # Cooldown timers (in seconds)
    COOLDOWN_SEARCH_FOOD = 30
    COOLDOWN_REFUEL = 30
    COOLDOWN_HIRE_CREW = 60
    COOLDOWN_EXPLORE_WRECKAGE = 45
    COOLDOWN_REST = 20
    COOLDOWN_TRADE = 30
    COOLDOWN_REPAIR_SHIP = 45
    COOLDOWN_SELL_ITEMS = 15
    
    # Action cooldowns dictionary
    COOLDOWNS = {
        "search_food": COOLDOWN_SEARCH_FOOD,
        "refuel": COOLDOWN_REFUEL,
        "hire_crew": COOLDOWN_HIRE_CREW,
        "explore_wreckage": COOLDOWN_EXPLORE_WRECKAGE,
        "rest": COOLDOWN_REST,
        "trade": COOLDOWN_TRADE,
        "repair_ship": COOLDOWN_REPAIR_SHIP,
        "sell_items": COOLDOWN_SELL_ITEMS
    }
    
    # Food search risks
    FOOD_SEARCH_CREW_LOSS_CHANCE = 0.1
    FOOD_SEARCH_CREW_LOSS_MESSAGE = "Oh no! A crew member was lost during the food search!"
    
    # Resource gathering
    MAX_FOOD_FIND = 25
    MAX_FUEL_FIND = 25
    MIN_RESOURCE_FIND = 5
    
    # Resting mechanics
    REST_FOOD_COST = (5, 10)
    REST_REPAIR_MIN = 1
    REST_REPAIR_MAX = 5
    
    # Travel settings
    TRAVEL_FUEL_COST = (10, 30)
    TRAVEL_FOOD_COST = (5, 20)
    TRAVEL_DISTANCE = (50, 150)
    
    # Wreckage exploration
    WRECKAGE_SUCCESS_RATE = 0.5
    WRECKAGE_DAMAGE = (10, 25)
    
    # Credit earning
    CREDITS_FROM_ENEMIES = (5, 25)
    CREDITS_FROM_SALVAGE = (10, 50)
    ITEM_SELL_VALUES = {
        "alien artifact": 40,
        "quantum battery": 25,
        "dark matter shard": 30,
        "nano medkit": 35,
        "ship parts": 20
    }
    RANDOM_CREDITS_CHANCE = 0.2
    
    # Encounter probabilities
    ENCOUNTER_PROBABILITIES = {
        "asteroid": 0.2,
        "enemy": 0.25,
        "anomaly": 0.15,
        "solar flare": 0.1,
        "derelict ship": 0.15
    }
    
    # Item drop rates
    ITEM_DROP_RATES = {
        "alien artifact": 0.2,
        "quantum battery": 0.3,
        "dark matter shard": 0.25,
        "nano medkit": 0.15,
        "ship parts": 0.1
    }
    
    # Trading
    TRADE_COST = 10
    TRADE_FUEL_GAIN = 15
    TRADE_FOOD_GAIN = 15
    TRADE_REPAIR_GAIN = 5
    
    # Enemies
    ENEMIES = [
        {"name": "Space Pirate", "damage": (10, 25), "drop": "alien artifact", "weight": 3},
        {"name": "Void Beast", "damage": (15, 30), "drop": "dark matter shard", "weight": 2},
        {"name": "Malfunctioning Drone", "damage": (5, 20), "drop": "quantum battery", "weight": 4},
    ]

class AlienTrailGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Alien Trail")
        self.last_action_times = {}
        self.game_active = True
        self.configure_styles()
        self.create_widgets()
        self.restart_game()
        
        # Action to button mapping
        self.action_to_button = {
            "search_food": "Search for Food",
            "refuel": "Refuel",
            "hire_crew": "Hire Crew",
            "explore_wreckage": "Explore Wreckage",
            "rest": "Rest",
            "trade": "Trade",
            "repair_ship": "Repair Ship",
            "sell_items": "Sell Items"
        }
        
        self.root.after(1000, self.update_cooldowns)

    def is_game_active(self):
        """Check if game should continue"""
        return (self.fuel > 0 
                and self.crew > 0 
                and self.ship_integrity > 0 
                and self.distance > 0
                and self.game_active)

    def configure_styles(self):
        self.title_font = tkfont.Font(family="Courier", size=12, weight="bold")
        self.status_font = tkfont.Font(family="Courier", size=10)
        self.message_font = tkfont.Font(family="Courier", size=10)
        
        self.colors = {
            "bg": "#0a0a0a",
            "fg": "#00ff00",
            "status_bg": "#121212",
            "critical": "#ff5555",
            "warning": "#ffff55",
            "good": "#55ff55",
            "highlight": "#00ffff",
            "disabled": "#555555"
        }

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.status_box = tk.Text(
            self.main_frame,
            height=15,
            width=80,
            bg=self.colors["bg"],
            fg=self.colors["fg"],
            font=self.message_font,
            padx=10,
            pady=10,
            wrap=tk.WORD,
            insertbackground=self.colors["fg"],
            selectbackground=self.colors["highlight"]
        )
        self.status_box.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.button_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        self.button_frame.pack(fill=tk.X)

        self.buttons = {}
        actions = [
            ("Travel", self.travel),
            ("Rest", self.rest),
            ("Check Supplies", self.check_supplies),
            ("Search for Food", self.search_food),
            ("Refuel", self.refuel),
            ("Hire Crew", self.hire_crew),
            ("Explore Wreckage", self.explore_wreckage),
            ("Trade", self.trade),
            ("Sell Items", self.sell_items),
            ("Repair Ship", self.repair_ship),
            ("Restart Game", self.restart_game)
        ]
        
        for i, (name, command) in enumerate(actions):
            btn = tk.Button(
                self.button_frame,
                text=name,
                command=command,
                bg="#222222",
                fg=self.colors["fg"],
                activebackground="#333333",
                activeforeground=self.colors["good"],
                relief=tk.RAISED,
                borderwidth=2,
                font=self.status_font
            )
            btn.grid(row=i//4, column=i%4, padx=5, pady=5, sticky="ew")
            self.buttons[name] = btn

        for i in range(4):
            self.button_frame.grid_columnconfigure(i, weight=1)

    def update_cooldowns(self):
        """Update button states and cooldown timers"""
        if not self.is_game_active():
            for btn in self.buttons.values():
                if btn["text"] != "Restart Game":
                    btn.config(state=tk.DISABLED, fg=self.colors["disabled"])
            return
            
        for action_name, cooldown in GameConfig.COOLDOWNS.items():
            btn_name = self.action_to_button.get(action_name)
            if btn_name and btn_name in self.buttons:
                remaining = self.check_cooldown(action_name)
                if remaining > 0:
                    self.buttons[btn_name].config(
                        state=tk.DISABLED,
                        text=f"{btn_name} ({int(remaining)}s)",
                        fg=self.colors["disabled"]
                    )
                else:
                    self.buttons[btn_name].config(
                        state=tk.NORMAL,
                        text=btn_name,
                        fg=self.colors["fg"]
                    )
        self.root.after(1000, self.update_cooldowns)

    def check_cooldown(self, action_name):
        if action_name not in self.last_action_times:
            return 0
        elapsed = time.time() - self.last_action_times[action_name]
        cooldown = GameConfig.COOLDOWNS.get(action_name, 0)
        return max(0, cooldown - elapsed)

    def can_perform_action(self, action_name):
        if not self.is_game_active():
            return False
        remaining = self.check_cooldown(action_name)
        if remaining > 0:
            return False
        self.last_action_times[action_name] = time.time()
        return True

    def display(self, msg):
        self.status_box.config(state=tk.NORMAL)
        self.status_box.delete("1.0", tk.END)
        self.status_box.insert(tk.END, "EVENT LOG:\n", "header")
        self.status_box.insert(tk.END, "═" * 70 + "\n", "divider")
        self.status_box.insert(tk.END, msg + "\n\n", "message")
        
        if not hasattr(self, '_restarting'):
            self.update_status()
        self.status_box.config(state=tk.DISABLED)
        self.status_box.see(tk.END)

    def update_status(self):
        self.status_box.config(state=tk.NORMAL)
        
        if self.status_box.get("1.0", tk.END).count("\n") > 20:
            self.status_box.delete("1.0", "5.0")
        
        self.status_box.insert(tk.END, "\nSHIP STATUS:\n", "header")
        self.status_box.insert(tk.END, "═" * 70 + "\n", "divider")
        
        status_lines = [
            self.format_status("Crew Members:", self.crew, 1, GameConfig.CREW_HIRE_MAX),
            self.format_status("Fuel:", self.fuel, 30, GameConfig.MAX_FUEL),
            self.format_status("Food:", self.food, 30, GameConfig.MAX_FOOD),
            self.format_status("Ship Integrity:", self.ship_integrity, 30, GameConfig.MAX_SHIP_INTEGRITY),
            f"Distance to Colony: {self.distance}/{GameConfig.STARTING_DISTANCE} units",
            f"Credits: {self.credits}",
            "Inventory: " + ", ".join(f"{k}:{v}" for k,v in self.inventory.items() if v > 0)
        ]
        
        for line in status_lines:
            self.status_box.insert(tk.END, line + "\n")
        
        self.status_box.config(state=tk.DISABLED)
        self.status_box.see(tk.END)

    def format_status(self, label, value, warn_thresh=0, max_value=100):
        if value <= warn_thresh:
            color = "critical"
        elif value <= warn_thresh * 2:
            color = "warning"
        else:
            color = "good"
        
        if max_value > 10:
            percentage = (value / max_value) * 100
            bar_length = int(percentage // 10)
            bar = " [" + "■" * bar_length + "□" * (10 - bar_length) + "]"
            return f"{label:15} {value:3}/{max_value} {bar}"
        else:
            return f"{label:15} {value:3}"

    def restart_game(self):
        self._restarting = True
        self.game_active = True
        
        self.crew = GameConfig.STARTING_CREW
        self.fuel = GameConfig.STARTING_FUEL
        self.food = GameConfig.STARTING_FOOD
        self.ship_integrity = GameConfig.MAX_SHIP_INTEGRITY
        self.distance = GameConfig.STARTING_DISTANCE
        self.credits = GameConfig.STARTING_CREDITS
        self.inventory = {"ship parts": GameConfig.STARTING_SHIP_PARTS}
        self.item_list = list(GameConfig.ITEM_DROP_RATES.keys())
        self.enemy_list = GameConfig.ENEMIES
        self.last_action_times = {}
        
        self.display("╔══════════════════════════════╗\n"
                    "║   WELCOME TO ALIEN TRAIL!    ║\n"
                    "╚══════════════════════════════╝\n\n"
                    f"Your mission is to travel {GameConfig.STARTING_DISTANCE} units.\n"
                    f"Starting with {GameConfig.STARTING_CREW} crew, {GameConfig.STARTING_FUEL} fuel, "
                    f"and {GameConfig.STARTING_CREDITS} credits.\n\n"
                    "Good luck, Captain!")
        
        del self._restarting
        self.update_status()

    def game_over(self, msg):
        self.game_active = False
        messagebox.showinfo("GAME OVER", msg)
        self.display(f"GAME OVER: {msg}\n\nPress 'Restart Game' to play again.")

    def travel(self):
        if not self.is_game_active():
            return
            
        if self.fuel <= 0:
            self.game_over("You're stranded in space with no fuel!")
            return
        
        fuel_cost = random.randint(*GameConfig.TRAVEL_FUEL_COST)
        food_cost = random.randint(*GameConfig.TRAVEL_FOOD_COST)
        travel_distance = random.randint(*GameConfig.TRAVEL_DISTANCE)
        
        self.distance -= travel_distance
        self.fuel = max(0, self.fuel - fuel_cost)
        self.food = max(0, self.food - food_cost)
        
        if self.fuel <= 0:
            self.game_over("You've run out of fuel and are stranded in space!")
            return
        
        if random.random() < GameConfig.RANDOM_CREDITS_CHANCE:
            found_credits = random.randint(5, 20)
            self.credits += found_credits
            self.display(f"You traveled {travel_distance} units.\n"
                        f"Found {found_credits} credits floating in space!\n"
                        f"Used {fuel_cost} fuel and {food_cost} food.")
        else:
            self.display(f"You traveled {travel_distance} units through space.\n"
                       f"Used {fuel_cost} fuel and {food_cost} food.")
        
        self.random_event()
        
        if self.distance <= 0:
            self.display("Congratulations! You reached the colony!")
        elif self.crew <= 0:
            self.game_over("Your crew perished!")
        elif self.ship_integrity <= 0:
            self.game_over("Your ship has been destroyed!")

    def rest(self):
        if not self.is_game_active():
            return
            
        if not self.can_perform_action("rest"):
            return
            
        food_cost = random.randint(*GameConfig.REST_FOOD_COST)
        if self.food < food_cost:
            self.display(f"Need at least {food_cost} food to rest!")
            return
            
        self.food -= food_cost
        repair = random.randint(GameConfig.REST_REPAIR_MIN, GameConfig.REST_REPAIR_MAX)
        actual_repair = min(repair, GameConfig.MAX_SHIP_INTEGRITY - self.ship_integrity)
        
        if actual_repair > 0:
            self.ship_integrity += actual_repair
            self.display(f"Rested for a while. Used {food_cost} food. "
                       f"Ship repaired +{actual_repair}%.")
        else:
            self.display(f"Rested for a while. Used {food_cost} food. "
                       "Ship is already at maximum integrity.")

    def check_supplies(self):
        self.display("Current Supplies and Inventory:")

    def search_food(self):
        if not self.is_game_active():
            return
            
        if not self.can_perform_action("search_food"):
            return
            
        if self.food >= GameConfig.MAX_FOOD:
            self.display("Food storage is full!")
            return
            
        # Check for crew loss (can't lose last crew member)
        if (random.random() < GameConfig.FOOD_SEARCH_CREW_LOSS_CHANCE and 
            self.crew > 1):
            self.crew -= 1
            self.display(GameConfig.FOOD_SEARCH_CREW_LOSS_MESSAGE)
            return
            
        found = random.randint(GameConfig.MIN_RESOURCE_FIND, GameConfig.MAX_FOOD_FIND)
        actual_gain = min(found, GameConfig.MAX_FOOD - self.food)
        self.food += actual_gain
        self.display(f"You found {actual_gain} units of food.")

    def refuel(self):
        if not self.is_game_active():
            return
            
        if self.fuel <= 0:
            self.display("Too late! You're already stranded in space!")
            return
            
        if not self.can_perform_action("refuel"):
            return
            
        if self.fuel >= GameConfig.MAX_FUEL:
            self.display("Fuel tanks are full!")
            return
            
        found = random.randint(GameConfig.MIN_RESOURCE_FIND, GameConfig.MAX_FUEL_FIND)
        actual_gain = min(found, GameConfig.MAX_FUEL - self.fuel)
        self.fuel += actual_gain
        self.display(f"You collected {actual_gain} units of fuel.")

    def hire_crew(self):
        if not self.is_game_active():
            return
            
        if not self.can_perform_action("hire_crew"):
            return
            
        if self.crew >= GameConfig.CREW_HIRE_MAX:
            self.display(f"Can't hire more crew! Maximum is {GameConfig.CREW_HIRE_MAX}.")
            return
            
        if self.credits < GameConfig.CREW_HIRE_COST:
            self.display(f"Need {GameConfig.CREW_HIRE_COST} credits to hire crew!")
            return
            
        if random.random() <= GameConfig.CREW_HIRE_CHANCE:
            self.crew += 1
            self.credits -= GameConfig.CREW_HIRE_COST
            self.display(f"Hired a new crew member for {GameConfig.CREW_HIRE_COST} credits!")
        else:
            self.display("No available crew found at this location. "
                       "You keep your credits.")

    def explore_wreckage(self):
        if not self.is_game_active():
            return
            
        if not self.can_perform_action("explore_wreckage"):
            return
            
        if random.random() <= GameConfig.WRECKAGE_SUCCESS_RATE:
            part = random.choices(
                list(GameConfig.ITEM_DROP_RATES.keys()),
                weights=GameConfig.ITEM_DROP_RATES.values(),
                k=1
            )[0]
            self.inventory[part] = self.inventory.get(part, 0) + 1
            self.display(f"You found a {part} in the wreckage!")
        else:
            damage = random.randint(*GameConfig.WRECKAGE_DAMAGE)
            self.ship_integrity = max(0, self.ship_integrity - damage)
            self.display(f"The wreckage exploded! Ship takes {damage}% damage.")
            if self.ship_integrity <= 0:
                self.game_over("Your ship has been destroyed!")

    def trade(self):
        if not self.is_game_active():
            return
            
        if not self.can_perform_action("trade"):
            return
            
        if self.credits < GameConfig.TRADE_COST:
            self.display(f"You need {GameConfig.TRADE_COST} credits to trade.")
            return
            
        self.fuel = min(GameConfig.MAX_FUEL, self.fuel + GameConfig.TRADE_FUEL_GAIN)
        self.food = min(GameConfig.MAX_FOOD, self.food + GameConfig.TRADE_FOOD_GAIN)
        self.ship_integrity = min(GameConfig.MAX_SHIP_INTEGRITY, 
                                self.ship_integrity + GameConfig.TRADE_REPAIR_GAIN)
        self.credits -= GameConfig.TRADE_COST
        self.display(f"Traded {GameConfig.TRADE_COST} credits for supplies:\n"
                   f"+{GameConfig.TRADE_FUEL_GAIN} fuel, +{GameConfig.TRADE_FOOD_GAIN} food, "
                   f"+{GameConfig.TRADE_REPAIR_GAIN}% ship integrity")

    def sell_items(self):
        if not self.is_game_active():
            return
            
        if not self.can_perform_action("sell_items"):
            return
            
        if not any(v > 0 for v in self.inventory.values()):
            self.display("You have nothing to sell!")
            return
        
        sale_report = []
        total = 0
        for item, count in list(self.inventory.items()):
            if count > 0 and item in GameConfig.ITEM_SELL_VALUES:
                value = GameConfig.ITEM_SELL_VALUES[item]
                sale_total = value * count
                total += sale_total
                sale_report.append(f"Sold {count} {item} for {sale_total} credits")
                self.inventory[item] = 0
        
        if total > 0:
            self.credits += total
            sale_report.append(f"\nTotal earned: {total} credits")
            self.display("Sale Complete:\n" + "\n".join(sale_report))
        else:
            self.display("You have no sellable items!")

    def repair_ship(self):
        if not self.is_game_active():
            return
            
        if not self.can_perform_action("repair_ship"):
            return
            
        parts = self.inventory.get("ship parts", 0)
        if parts <= 0:
            self.display("No ship parts available to repair.")
            return
            
        if self.ship_integrity >= GameConfig.MAX_SHIP_INTEGRITY:
            self.display("Ship is already at maximum integrity!")
            return
            
        used = min(parts, 5)
        repair_amount = used * 5
        actual_repair = min(repair_amount, GameConfig.MAX_SHIP_INTEGRITY - self.ship_integrity)
        
        self.ship_integrity += actual_repair
        self.inventory["ship parts"] -= used
        self.display(f"Repaired ship with {used} parts (+{actual_repair}%).")

    def random_event(self):
        nothing_chance = 1 - sum(GameConfig.ENCOUNTER_PROBABILITIES.values())
        events = list(GameConfig.ENCOUNTER_PROBABILITIES.keys()) + ["nothing"]
        weights = list(GameConfig.ENCOUNTER_PROBABILITIES.values()) + [nothing_chance]
        event = random.choices(events, weights=weights, k=1)[0]
        
        if event == "asteroid":
            damage = random.randint(5, 20)
            self.ship_integrity = max(0, self.ship_integrity - damage)
            self.display(f"You hit an asteroid! Ship takes {damage}% damage.")
        elif event == "enemy":
            enemy = random.choices(
                self.enemy_list,
                weights=[e.get("weight", 1) for e in self.enemy_list],
                k=1
            )[0]
            damage = random.randint(*enemy["damage"])
            self.ship_integrity = max(0, self.ship_integrity - damage)
            self.inventory[enemy["drop"]] = self.inventory.get(enemy["drop"], 0) + 1
            credits_gained = random.randint(*GameConfig.CREDITS_FROM_ENEMIES)
            self.credits += credits_gained
            self.display(
                f"You fought a {enemy['name']}! Ship took {damage}% damage.\n"
                f"Gained a {enemy['drop']} and {credits_gained} credits!"
            )
        elif event == "anomaly":
            damage = random.randint(5, 15)
            self.ship_integrity = max(0, self.ship_integrity - damage)
            self.display("A space anomaly disrupted your systems! Ship takes damage.")
        elif event == "solar flare":
            damage = random.randint(10, 20)
            self.ship_integrity = max(0, self.ship_integrity - damage)
            fuel_loss = random.randint(5, 10)
            self.fuel = max(0, self.fuel - fuel_loss)
            self.display(f"Solar flare! Systems damaged ({damage}%) and lost {fuel_loss} fuel.")
        elif event == "derelict ship":
            if random.random() < 0.5:
                item = random.choices(
                    list(GameConfig.ITEM_DROP_RATES.keys()),
                    weights=GameConfig.ITEM_DROP_RATES.values(),
                    k=1
                )[0]
                self.inventory[item] = self.inventory.get(item, 0) + 1
                self.display(f"You scavenged a derelict ship and found: {item}")
            else:
                credits_gained = random.randint(*GameConfig.CREDITS_FROM_SALVAGE)
                self.credits += credits_gained
                self.display(f"You found an abandoned cargo hold with {credits_gained} credits!")
        else:
            self.display("The journey continues uneventfully.")

root = tk.Tk()
try:
    root.iconbitmap(default='')
except:
    pass
root.minsize(750, 600)

game = AlienTrailGame(root)

game.status_box.tag_config("header", foreground="#00ffff", font=game.title_font)
game.status_box.tag_config("divider", foreground="#555555")
game.status_box.tag_config("message", font=game.message_font)
game.status_box.tag_config("critical", foreground=game.colors["critical"])
game.status_box.tag_config("warning", foreground=game.colors["warning"])
game.status_box.tag_config("good", foreground=game.colors["good"])

root.mainloop()