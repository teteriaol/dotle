import requests
import json
import sqlite3

out = "filtered_hero_attributes.json"
json_url = "https://raw.githubusercontent.com/dotabuff/d2vpkr/master/dota/scripts/npc/npc_heroes.json"
db_name = "db.sqlite3"
table = "app_heroes"


def prepare_data(out=out, json_url=json_url):
    json_url = "https://raw.githubusercontent.com/dotabuff/d2vpkr/master/dota/scripts/npc/npc_heroes.json"
    response = requests.get(json_url)

    if response.status_code == 200:
        json_data = response.json()
        hero_attributes = []

        for hero_name, hero_data in json_data.get("DOTAHeroes", {}).items():
            if hero_name != "Version" and hero_name != "npc_dota_hero_base" and hero_data.get("Enabled") == "1":
                team_text = hero_data.get("Team")
                team_result = "Radiant" if team_text.strip().lower() == "good" else "Dire"

                attack_capabilities = hero_data.get("AttackCapabilities")
                attack_type = "Ranged" if "RANGED" in attack_capabilities else "Melee"

                similar_heroes = hero_data.get("SimilarHeroes")
                if not similar_heroes:
                    similar_heroes = "0,0,0"

                last_hit_challenge_rival = hero_data.get("LastHitChallengeRival")
                last_hit_challenge_rival_id = json_data["DOTAHeroes"].get(last_hit_challenge_rival, {}).get("HeroID", None)
                if not last_hit_challenge_rival_id:
                    last_hit_challenge_rival_id = "0"
                
                name_aliases = hero_data.get("NameAliases")
                if name_aliases:
                    name_aliases = name_aliases.replace(";", ",")
                else:
                    name_aliases = hero_data.get("workshop_guide_name")

                adj = hero_data.get("Adjectives")
                if not adj:
                    adj = {}
                if hero_name == 'npc_dota_hero_snapfire': # exception
                    adj['Female'] = '1'
                    adj = {'Female': adj['Female'], **adj}
                if 'Female' not in adj.keys():
                    adj['Male'] = '1'
                    adj = {'Male': adj['Male'], **adj}
                if 'Legs' not in adj.keys():
                    adj['Legs'] = '2'
                if 'BadTeeth' in adj.keys():
                    v = adj.pop('BadTeeth')
                    adj['Bad Teeth'] = v
                if 'NicePecs' in adj.keys():
                    v = adj.pop('NicePecs')
                    adj['Nice Pecs'] = v

                adj_order = [
                    "Male",
                    "Female",
                    "Legs",
                    "Wings",
                    "Horns",
                    "Steed",
                    "Nose",
                    "Fuzzy",
                    "Bearded",
                    "Bad Teeth",
                    "Cape",
                    "Nice Pecs",
                    "Potbelly",
                    "Parent",
                    "Arachnophobic",
                    "Undead",
                    "Aquatic",
                    "Demon",
                    "Spirit",
                    "Flying",
                    "Cute",
                    "Fiery",
                    "Icy",
                    "Blue",
                    "Red",
                    "Green"
                ]

                adj = dict(
                    sorted(
                        adj.items(),
                        key=lambda item: adj_order.index(item[0]) if item[0] in adj_order else float('inf')
                    )
                )

                attributes = {
                    "HeroID": hero_data.get("HeroID"),
                    "CodeName": hero_name,
                    "Name": hero_data.get("workshop_guide_name"),
                    "Role": hero_data.get("Role"),
                    "Rolelevels": hero_data.get("Rolelevels"),
                    "Team": team_result,
                    "AttackType": attack_type,
                    "SimilarHeroesID": similar_heroes,
                    "AttributePrimary": hero_data.get("AttributePrimary"),
                    "LastHitChallengeRivalID": last_hit_challenge_rival_id,
                    "NameAliases": name_aliases,
                    "Adjectives": adj,
                }
                hero_attributes.append(attributes)
        hero_attributes.sort(key=lambda x: x["Name"])

        hero_attributes_with_keys = {str(i): hero_attributes[i - 1] for i in range(1, len(hero_attributes) + 1)}

        with open(out, "w") as json_file:
            json.dump(hero_attributes_with_keys, json_file, indent=4)

        print(f"Filtered and sorted hero attributes saved as '{out}'.")
        return out

    else:
        print("Failed to fetch JSON data. Status code:", response.status_code)


def update_db(db_name=db_name,table=table,out=out):
    with open(out, "r") as json_file:
        hero_attributes = json.load(json_file)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f'DROP TABLE {table}')
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table} (
                        ID INTEGER PRIMARY KEY,
                        HeroID INTEGER,
                        CodeName TEXT,
                        Name TEXT,
                        Role TEXT,
                        Rolelevels TEXT,
                        Team TEXT,
                        AttackType TEXT,
                        SimilarHeroesID TEXT,
                        AttributePrimary TEXT,
                        LastHitChallengeRivalID INTEGER,
                        NameAliases TEXT,
                        Adjectives TEXT
                     )''')
    for key, attributes in hero_attributes.items():
        hero_id = int(attributes["HeroID"])
        last_hit_challenge_rival_id = int(attributes["LastHitChallengeRivalID"]) if attributes.get("LastHitChallengeRivalID") else None
        name_aliases = attributes["NameAliases"] if attributes.get("NameAliases") else None
        adjectives_json = json.dumps(attributes["Adjectives"])

        cursor.execute('''INSERT INTO app_heroes 
                          (ID, HeroID, CodeName, Name, Role, Rolelevels, Team, AttackType, SimilarHeroesID, AttributePrimary, LastHitChallengeRivalID, NameAliases, Adjectives) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                       (int(key), hero_id, attributes["CodeName"], attributes["Name"], attributes["Role"],
                        attributes["Rolelevels"], attributes["Team"], attributes["AttackType"],
                        attributes["SimilarHeroesID"], attributes["AttributePrimary"], last_hit_challenge_rival_id, name_aliases, adjectives_json))
    conn.commit()
    conn.close()

    print(f"Data inserted into SQLite database {db_name} with 'ID' and 'HeroID' columns.")

if __name__ == "__main__":
    prepare_data()
    update_db()