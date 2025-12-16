import sqlite3
import random

DB_FILENAME = "pokedex.db"


def create_database():
    conn = sqlite3.connect(DB_FILENAME)
    cur = conn.cursor()

    # -----------------------------------------------------
    # 1. Create Tables
    # -----------------------------------------------------

    # Table 1: Pokemon
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pokemon (
            pokedex_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type_1 TEXT NOT NULL,
            type_2 TEXT,
            base_hp INTEGER NOT NULL,
            is_legendary BOOLEAN DEFAULT 0
        );
    """)

    # Table 2: Moves
    cur.execute("""
        CREATE TABLE IF NOT EXISTS moves (
            move_id INTEGER PRIMARY KEY AUTOINCREMENT,
            move_name TEXT NOT NULL,
            move_type TEXT NOT NULL,
            power INTEGER,
            accuracy INTEGER
        );
    """)

    # Table 3: Learnset (Linking Table)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pokemon_moveset (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pokemon_id INTEGER NOT NULL,
            move_id INTEGER NOT NULL,
            FOREIGN KEY(pokemon_id) REFERENCES pokemon(pokedex_id),
            FOREIGN KEY(move_id) REFERENCES moves(move_id)
        );
    """)

    conn.commit()

    # -----------------------------------------------------
    # 2. The Pokemon Data (ID, Name, Type1, Type2, HP, Legendary)
    # -----------------------------------------------------
    # Type 2 is None if they don't have one.

    POKEMON_DATA = [
        (1, "Bulbasaur", "Grass", "Poison", 45, 0),
        (2, "Ivysaur", "Grass", "Poison", 60, 0),
        (3, "Venusaur", "Grass", "Poison", 80, 0),
        (4, "Charmander", "Fire", None, 39, 0),
        (5, "Charmeleon", "Fire", None, 58, 0),
        (6, "Charizard", "Fire", "Flying", 78, 0),
        (7, "Squirtle", "Water", None, 44, 0),
        (8, "Wartortle", "Water", None, 59, 0),
        (9, "Blastoise", "Water", None, 79, 0),
        (10, "Caterpie", "Bug", None, 45, 0),
        (11, "Metapod", "Bug", None, 50, 0),
        (12, "Butterfree", "Bug", "Flying", 60, 0),
        (13, "Weedle", "Bug", "Poison", 40, 0),
        (14, "Kakuna", "Bug", "Poison", 45, 0),
        (15, "Beedrill", "Bug", "Poison", 65, 0),
        (16, "Pidgey", "Normal", "Flying", 40, 0),
        (17, "Pidgeotto", "Normal", "Flying", 63, 0),
        (18, "Pidgeot", "Normal", "Flying", 83, 0),
        (19, "Rattata", "Normal", None, 30, 0),
        (20, "Raticate", "Normal", None, 55, 0),
        (21, "Spearow", "Normal", "Flying", 40, 0),
        (22, "Fearow", "Normal", "Flying", 65, 0),
        (23, "Ekans", "Poison", None, 35, 0),
        (24, "Arbok", "Poison", None, 60, 0),
        (25, "Pikachu", "Electric", None, 35, 0),
        (26, "Raichu", "Electric", None, 60, 0),
        (27, "Sandshrew", "Ground", None, 50, 0),
        (28, "Sandslash", "Ground", None, 75, 0),
        (29, "Nidoran♀", "Poison", None, 55, 0),
        (30, "Nidorina", "Poison", None, 70, 0),
        (31, "Nidoqueen", "Poison", "Ground", 90, 0),
        (32, "Nidoran♂", "Poison", None, 46, 0),
        (33, "Nidorino", "Poison", None, 61, 0),
        (34, "Nidoking", "Poison", "Ground", 81, 0),
        (35, "Clefairy", "Fairy", None, 70, 0),  # Retroactively Fairy
        (36, "Clefable", "Fairy", None, 95, 0),
        (37, "Vulpix", "Fire", None, 38, 0),
        (38, "Ninetales", "Fire", None, 73, 0),
        (39, "Jigglypuff", "Normal", "Fairy", 115, 0),
        (40, "Wigglytuff", "Normal", "Fairy", 140, 0),
        (41, "Zubat", "Poison", "Flying", 40, 0),
        (42, "Golbat", "Poison", "Flying", 75, 0),
        (43, "Oddish", "Grass", "Poison", 45, 0),
        (44, "Gloom", "Grass", "Poison", 60, 0),
        (45, "Vileplume", "Grass", "Poison", 75, 0),
        (46, "Paras", "Bug", "Grass", 35, 0),
        (47, "Parasect", "Bug", "Grass", 60, 0),
        (48, "Venonat", "Bug", "Poison", 60, 0),
        (49, "Venomoth", "Bug", "Poison", 70, 0),
        (50, "Diglett", "Ground", None, 10, 0),
        (51, "Dugtrio", "Ground", None, 35, 0),
        (52, "Meowth", "Normal", None, 40, 0),
        (53, "Persian", "Normal", None, 65, 0),
        (54, "Psyduck", "Water", None, 50, 0),
        (55, "Golduck", "Water", None, 80, 0),
        (56, "Mankey", "Fighting", None, 40, 0),
        (57, "Primeape", "Fighting", None, 65, 0),
        (58, "Growlithe", "Fire", None, 55, 0),
        (59, "Arcanine", "Fire", None, 90, 0),
        (60, "Poliwag", "Water", None, 40, 0),
        (61, "Poliwhirl", "Water", None, 65, 0),
        (62, "Poliwrath", "Water", "Fighting", 90, 0),
        (63, "Abra", "Psychic", None, 25, 0),
        (64, "Kadabra", "Psychic", None, 40, 0),
        (65, "Alakazam", "Psychic", None, 55, 0),
        (66, "Machop", "Fighting", None, 70, 0),
        (67, "Machoke", "Fighting", None, 80, 0),
        (68, "Machamp", "Fighting", None, 90, 0),
        (69, "Bellsprout", "Grass", "Poison", 50, 0),
        (70, "Weepinbell", "Grass", "Poison", 65, 0),
        (71, "Victreebel", "Grass", "Poison", 80, 0),
        (72, "Tentacool", "Water", "Poison", 40, 0),
        (73, "Tentacruel", "Water", "Poison", 80, 0),
        (74, "Geodude", "Rock", "Ground", 40, 0),
        (75, "Graveler", "Rock", "Ground", 55, 0),
        (76, "Golem", "Rock", "Ground", 80, 0),
        (77, "Ponyta", "Fire", None, 50, 0),
        (78, "Rapidash", "Fire", None, 65, 0),
        (79, "Slowpoke", "Water", "Psychic", 90, 0),
        (80, "Slowbro", "Water", "Psychic", 95, 0),
        (81, "Magnemite", "Electric", "Steel", 25, 0),
        (82, "Magneton", "Electric", "Steel", 50, 0),
        (83, "Farfetch'd", "Normal", "Flying", 52, 0),
        (84, "Doduo", "Normal", "Flying", 35, 0),
        (85, "Dodrio", "Normal", "Flying", 60, 0),
        (86, "Seel", "Water", None, 65, 0),
        (87, "Dewgong", "Water", "Ice", 90, 0),
        (88, "Grimer", "Poison", None, 80, 0),
        (89, "Muk", "Poison", None, 105, 0),
        (90, "Shellder", "Water", None, 30, 0),
        (91, "Cloyster", "Water", "Ice", 50, 0),
        (92, "Gastly", "Ghost", "Poison", 30, 0),
        (93, "Haunter", "Ghost", "Poison", 45, 0),
        (94, "Gengar", "Ghost", "Poison", 60, 0),
        (95, "Onix", "Rock", "Ground", 35, 0),
        (96, "Drowzee", "Psychic", None, 60, 0),
        (97, "Hypno", "Psychic", None, 85, 0),
        (98, "Krabby", "Water", None, 30, 0),
        (99, "Kingler", "Water", None, 55, 0),
        (100, "Voltorb", "Electric", None, 40, 0),
        (101, "Electrode", "Electric", None, 60, 0),
        (102, "Exeggcute", "Grass", "Psychic", 60, 0),
        (103, "Exeggutor", "Grass", "Psychic", 95, 0),
        (104, "Cubone", "Ground", None, 50, 0),
        (105, "Marowak", "Ground", None, 60, 0),
        (106, "Hitmonlee", "Fighting", None, 50, 0),
        (107, "Hitmonchan", "Fighting", None, 50, 0),
        (108, "Lickitung", "Normal", None, 90, 0),
        (109, "Koffing", "Poison", None, 40, 0),
        (110, "Weezing", "Poison", None, 65, 0),
        (111, "Rhyhorn", "Ground", "Rock", 80, 0),
        (112, "Rhydon", "Ground", "Rock", 105, 0),
        (113, "Chansey", "Normal", None, 250, 0),
        (114, "Tangela", "Grass", None, 65, 0),
        (115, "Kangaskhan", "Normal", None, 105, 0),
        (116, "Horsea", "Water", None, 30, 0),
        (117, "Seadra", "Water", None, 55, 0),
        (118, "Goldeen", "Water", None, 45, 0),
        (119, "Seaking", "Water", None, 80, 0),
        (120, "Staryu", "Water", None, 30, 0),
        (121, "Starmie", "Water", "Psychic", 60, 0),
        (122, "Mr. Mime", "Psychic", "Fairy", 40, 0),
        (123, "Scyther", "Bug", "Flying", 70, 0),
        (124, "Jynx", "Ice", "Psychic", 65, 0),
        (125, "Electabuzz", "Electric", None, 65, 0),
        (126, "Magmar", "Fire", None, 65, 0),
        (127, "Pinsir", "Bug", None, 65, 0),
        (128, "Tauros", "Normal", None, 75, 0),
        (129, "Magikarp", "Water", None, 20, 0),
        (130, "Gyarados", "Water", "Flying", 95, 0),
        (131, "Lapras", "Water", "Ice", 130, 0),
        (132, "Ditto", "Normal", None, 48, 0),
        (133, "Eevee", "Normal", None, 55, 0),
        (134, "Vaporeon", "Water", None, 130, 0),
        (135, "Jolteon", "Electric", None, 65, 0),
        (136, "Flareon", "Fire", None, 65, 0),
        (137, "Porygon", "Normal", None, 65, 0),
        (138, "Omanyte", "Rock", "Water", 35, 0),
        (139, "Omastar", "Rock", "Water", 70, 0),
        (140, "Kabuto", "Rock", "Water", 30, 0),
        (141, "Kabutops", "Rock", "Water", 60, 0),
        (142, "Aerodactyl", "Rock", "Flying", 80, 0),
        (143, "Snorlax", "Normal", None, 160, 0),
        (144, "Articuno", "Ice", "Flying", 90, 1),
        (145, "Zapdos", "Electric", "Flying", 90, 1),
        (146, "Moltres", "Fire", "Flying", 90, 1),
        (147, "Dratini", "Dragon", None, 41, 0),
        (148, "Dragonair", "Dragon", None, 61, 0),
        (149, "Dragonite", "Dragon", "Flying", 91, 0),
        (150, "Mewtwo", "Psychic", None, 106, 1),
        (151, "Mew", "Psychic", None, 100, 1)
    ]

    # Sample Moves (A mix of types)
    MOVES_DATA = [
        ("Tackle", "Normal", 40, 100), ("Scratch", "Normal", 40, 100), ("Body Slam", "Normal", 85, 100),
        ("Flamethrower", "Fire", 90, 100), ("Fire Blast", "Fire", 110, 85), ("Ember", "Fire", 40, 100),
        ("Water Gun", "Water", 40, 100), ("Surf", "Water", 90, 100), ("Hydro Pump", "Water", 110, 80),
        ("Vine Whip", "Grass", 45, 100), ("Razor Leaf", "Grass", 55, 95), ("Solar Beam", "Grass", 120, 100),
        ("Thunderbolt", "Electric", 90, 100), ("Thunder", "Electric", 110, 70), ("Thunder Wave", "Electric", 0, 90),
        ("Ice Beam", "Ice", 90, 100), ("Blizzard", "Ice", 110, 70), ("Aurora Beam", "Ice", 65, 100),
        ("Psychic", "Psychic", 90, 100), ("Hypnosis", "Psychic", 0, 60), ("Dream Eater", "Psychic", 100, 100),
        ("Earthquake", "Ground", 100, 100), ("Dig", "Ground", 80, 100), ("Fissure", "Ground", 0, 30),
        ("Rock Slide", "Rock", 75, 90), ("Rock Throw", "Rock", 50, 90),
        ("Fly", "Flying", 90, 95), ("Wing Attack", "Flying", 60, 100), ("Peck", "Flying", 35, 100),
        ("Double Kick", "Fighting", 30, 100), ("Seismic Toss", "Fighting", 0, 100), ("Submission", "Fighting", 80, 80),
        ("Shadow Ball", "Ghost", 80, 100), ("Lick", "Ghost", 30, 100),
        ("Dragon Rage", "Dragon", 0, 100),
        ("Hyper Beam", "Normal", 150, 90)
    ]

    # -----------------------------------------------------
    # 3. Insert Data
    # -----------------------------------------------------

    # Insert Pokemon
    cur.executemany(
        "INSERT INTO pokemon (pokedex_id, name, type_1, type_2, base_hp, is_legendary) VALUES (?, ?, ?, ?, ?, ?)",
        POKEMON_DATA
    )

    # Insert Moves
    cur.executemany(
        "INSERT INTO moves (move_name, move_type, power, accuracy) VALUES (?, ?, ?, ?)",
        MOVES_DATA
    )

    # Insert Random Learnsets (Assign 2-5 random moves to each Pokemon)

    cur.execute("SELECT move_id FROM moves")
    all_move_ids = [row[0] for row in cur.fetchall()]

    learnset_data = []
    for p_id in range(1, 152):
        # Give each pokemon 4 random moves from the list
        chosen_moves = random.sample(all_move_ids, random.randint(2, 5))
        for m_id in chosen_moves:
            learnset_data.append((p_id, m_id))

    cur.executemany(
        "INSERT INTO pokemon_moveset (pokemon_id, move_id) VALUES (?, ?)",
        learnset_data
    )

    conn.commit()
    conn.close()
    print(f"Database '{DB_FILENAME}' created successfully with accurate Stats/Types for all 151 Pokemon!")


if __name__ == "__main__":
    create_database()