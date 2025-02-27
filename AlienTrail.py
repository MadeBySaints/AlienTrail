import random

def main():
    print("Welcome to Alien Trail! Your mission is to reach the distant colony.")
    crew = 5
    fuel = 100
    food = 100
    ship_integrity = 100
    distance = 1000  # Distance to colony
    credits = 50  # Currency for trade
    
    while distance > 0 and crew > 0 and ship_integrity > 0:
        print(f"\nStatus: Crew: {crew}, Fuel: {fuel}, Food: {food}, Ship: {ship_integrity}, Distance: {distance}, Credits: {credits}")
        action = input("Do you want to (1) travel, (2) rest, (3) check supplies, (4) search for food, (5) refuel, (6) explore wreckage, (7) trade? ").strip()
        
        if action == "1":
            travel = random.randint(50, 150)
            distance -= travel
            fuel_loss = random.randint(10, 30)
            food_loss = random.randint(5, 20)
            fuel = max(0, fuel - fuel_loss)
            food = max(0, food - food_loss)
            
            event = random.choice(["nothing", "asteroid", "alien", "trade", "distress call", "space anomaly", "derelict ship", "solar flare"])
            
            if event == "asteroid":
                damage = random.randint(5, 20)
                ship_integrity = max(0, ship_integrity - damage)
                print(f"You hit an asteroid field! Ship takes {damage}% damage.")
            elif event == "alien":
                fight = input("Aliens attack! Do you (1) fight or (2) flee? ").strip()
                if fight == "1":
                    if random.random() > 0.5:
                        print("You defeated the aliens!")
                        credits += random.randint(10, 30)
                    else:
                        damage = random.randint(10, 30)
                        ship_integrity = max(0, ship_integrity - damage)
                        print(f"The aliens damaged your ship! Ship takes {damage}% damage.")
                else:
                    print("You escaped, but wasted fuel.")
                    fuel = max(0, fuel - 10)
            elif event == "trade":
                print("You found a space station and resupplied.")
                fuel += 20
                food += 20
            elif event == "distress call":
                help_ship = input("A ship needs help! Do you assist? (y/n) ").strip().lower()
                if help_ship == "y":
                    if random.random() > 0.5:
                        print("They were grateful and gave you supplies!")
                        fuel += 15
                        food += 15
                    else:
                        damage = random.randint(10, 25)
                        ship_integrity = max(0, ship_integrity - damage)
                        print(f"It was a trap! Pirates attacked! Ship takes {damage}% damage.")
            elif event == "space anomaly":
                damage = random.randint(5, 15)
                ship_integrity = max(0, ship_integrity - damage)
                print(f"You encounter a strange anomaly. Some systems malfunction! Ship takes {damage}% damage.")
            elif event == "derelict ship":
                print("You discover a derelict ship and scavenge supplies.")
                fuel += random.randint(5, 20)
                food += random.randint(5, 20)
                credits += random.randint(10, 40)
            elif event == "solar flare":
                damage = random.randint(10, 20)
                ship_integrity = max(0, ship_integrity - damage)
                fuel = max(0, fuel - random.randint(5, 10))
                print(f"A solar flare disrupts your systems and damages the ship! Ship takes {damage}% damage.")
            else:
                print("The journey continues uneventfully.")
        
        elif action == "2":
            print("You rest and recover.")
            food = max(0, food - random.randint(5, 10))
        
        elif action == "3":
            print(f"Supplies: Fuel: {fuel}, Food: {food}, Ship Integrity: {ship_integrity}, Credits: {credits}")
        
        elif action == "4":
            found_food = random.randint(0, 20)
            food += found_food
            print(f"You found {found_food} units of food.")
        
        elif action == "5":
            found_fuel = random.randint(0, 20)
            fuel += found_fuel
            print(f"You found {found_fuel} units of fuel.")
        
        elif action == "6":
            print("You explore the wreckage of a destroyed ship...")
            if random.random() > 0.5:
                found_supplies = random.randint(10, 30)
                fuel += found_supplies
                print(f"You salvaged {found_supplies} units of fuel.")
            else:
                damage = random.randint(10, 25)
                ship_integrity = max(0, ship_integrity - damage)
                print(f"The wreckage was unstable and exploded! Ship takes {damage}% damage.")
        
        elif action == "7":
            if credits >= 10:
                print("You purchase supplies.")
                fuel += 10
                food += 10
                ship_integrity += 5
                credits -= 10
            else:
                print("You don’t have enough credits to trade.")
        
        if food <= 0:
            print("Your crew starved!")
            break
        if fuel <= 0:
            print("You're stranded in space!")
            break
        if ship_integrity <= 0:
            print("Your ship is destroyed!")
            break
    
    if distance <= 0:
        print("Congratulations! You reached the colony!")
    else:
        print("Mission failed. Game over.")

if __name__ == "__main__":
    main()
