import json, os, random

# User Modifications
iteration = 10000 # How many iterations to run, Higher = more accurate but slower
rate_up4 = ["Collei", "Diona", "Fischl"] # Characters that can be rate-up in 4-star pools
# user.json is where the rest of the modifications are stored and can be configured by the user
# wanted_characters: Number of characters you want
# wanted_weapons: Number of weapons you want
# wishes: Number of wishes you have
# starglitter: Amount of starglitter you have
# character: Modifying Character wish related values
# 5pity: 5-star character pity counter
# 5guarantee: Whether the next 5-star character is guaranteed
# 4pity: 4-star character pity counter
# 4guarantee: Whether the next 4-star character is guaranteed
# weapon: Modifying Weapon wish related values
# 5pity: 5-star weapon pity counter
# 5guarantee: Whether the next 5-star weapon is guaranteed
# 4pity: 4-star weapon pity counter
# 4guarantee: Whether the next 4-star weapon is guaranteed
# radiance: Radiance level, 0-3 
# epitomized: Epitomised system, 
# standard: Standard banner characters and your constellations for them
# 4characters: 4-star characters and your constellations for them
# End of Modifications

with open("config.json", "r", encoding="utf-8") as f:
    conf = json.load(f)

total = {
    "completed": 0,
    "totalcpity": 0,
    "totalcharacters": 0,
    "totalwantedcharacters": 0,
    "totalwpity": 0,
    "totalweapons": 0,
    "totalwantedweapons": 0,
    "totalstarglitter": 0,
    "totalradiance": 0,
    "totalepitomized": 0
}

def roll_character(user_data, pool_name, reward_mid, reward_max, rateup=False):
    if rateup:
        key = random.choice(rate_up4)
    else:
        keys = list(user_data[pool_name].keys())
        while True:
            key = random.choice(keys)
            if key not in rate_up4:
                break
    value = user_data[pool_name][key]

    if value < 7:
        user_data[pool_name][key] += 1
        if value > 0:
            user_data["starglitter"] += reward_mid
    elif value == 7:
        user_data["starglitter"] += reward_max

def pity_calc(pool_name, user_data, user_name, star):
    return (conf[pool_name]["base"] + (conf[pool_name]["increase"] * (1 + user_data[user_name][star] - conf[pool_name]["start"]) if user_data[user_name][star] >= conf[pool_name]["start"] else 0))
original_iterations = iteration
while iteration > 0:
    iteration -= 1
    user_file = "user.json"
    base_file = "base.json"
    file_to_load = user_file if os.path.exists(user_file) else base_file
    with open(file_to_load, "r", encoding="utf-8") as f:
        user_data = json.load(f)

    cdone = 0
    wdone = 0
    starglitter_wishes = 0
    while True:
        while user_data["wishes"] > 0:
            user_data["wishes"] -= 1
            pull = random.randint(1, 1000)
            if cdone < user_data["wanted_characters"]:
                if pull <= pity_calc("5char", user_data, "character", "5pity"):
                    total["totalcpity"] += user_data["character"]["5pity"]
                    total["totalcharacters"] += 1
                    user_data["character"]["4pity"] += 1
                    user_data["character"]["5pity"] = 0
                    if (random.randint(0,1) and not user_data["character"]["5guarantee"]):
                        if (user_data['radiance'] == 3) or (user_data['radiance'] == 2 and random.randint(1,4) < 4) or (user_data['radiance'] <= 1 and random.randint(0,1)):
                            total["totalradiance"] += 1
                            user_data["character"]["5guarantee"] = False
                            user_data["radiance"] = 0
                            if cdone > 0:
                                user_data["starglitter"] += 10
                            cdone += 1
                        else:
                            user_data["character"]["5guarantee"] = True
                            user_data["radiance"] += 1
                            roll_character(user_data, "standard", 10, 25)
                    else:
                        user_data["character"]["5guarantee"] = False
                        if cdone > 0:
                            user_data["starglitter"] += 10
                        cdone += 1
                elif pull <= pity_calc("4char", user_data, "character", "4pity"):
                    user_data["character"]["5pity"] += 1
                    user_data["character"]["4pity"] = 0
                    if (random.randint(0,1) and not user_data["character"]["4guarantee"]):
                        user_data["character"]["4guarantee"] = True
                        if random.randint(0,1):
                            roll_character(user_data, "4characters", 2, 10)
                        else:
                            user_data["starglitter"] += 2
                    else:
                        user_data["character"]["4guarantee"] = False
                        roll_character(user_data, "4characters", 2, 10, True)
                else:
                    user_data["character"]["5pity"] += 1
                    user_data["character"]["4pity"] += 1
            elif wdone < user_data["wanted_weapons"]:
                if pull <= pity_calc("5weap", user_data, "weapon", "5pity"):
                    total["totalwpity"] += user_data["weapon"]["5pity"]
                    total["totalweapons"] += 1
                    user_data["weapon"]["4pity"] += 1
                    user_data["weapon"]["5pity"] = 0
                    if user_data["epitomized"]:
                        total["totalepitomized"] += 1
                        user_data["weapon"]["epitomized"] = False
                        wdone += 1
                        continue
                    if (random.randint(1,4) == 4 and not user_data["weapon"]["5guarantee"]):
                        user_data["weapon"]["5guarantee"] = True
                        user_data["epitomized"] = True
                        user_data["starglitter"] += 10
                    else:
                        user_data["weapon"]["5guarantee"] = False
                        user_data["starglitter"] += 10
                        if random.randint(0,1):
                            wdone += 1
                        else:
                            user_data["epitomized"] = True
                elif pull <= pity_calc("4weap", user_data, "weapon", "4pity"):
                    user_data["weapon"]["5pity"] += 1
                    user_data["weapon"]["4pity"] = 0
                    if random.randint(1,4) == 4:
                        if random.randint(0,1):
                            roll_character(user_data, "4characters", 2, 10)
                            continue
                    user_data["starglitter"] += 2
                else:
                    user_data["weapon"]["5pity"] += 1
                    user_data["weapon"]["4pity"] += 1
        extra_wishes = user_data["starglitter"] // 10
        user_data["wishes"] += extra_wishes
        user_data["starglitter"] -= extra_wishes * 10
        starglitter_wishes += extra_wishes
        
        if not user_data["wishes"] or cdone == user_data["wanted_characters"] and wdone == user_data["wanted_weapons"]:
            
            if cdone == user_data["wanted_characters"] and wdone == user_data["wanted_weapons"]:
                total["completed"] += 1
            total["totalwantedcharacters"] += cdone
            total["totalwantedweapons"] += wdone
            total["totalstarglitter"] += starglitter_wishes
            break
user_file = "user.json"
base_file = "base.json"
file_to_load = user_file if os.path.exists(user_file) else base_file
with open(file_to_load, "r", encoding="utf-8") as f:
    user_data = json.load(f)
print(f"""Total C{user_data["wanted_characters"]-1}R{user_data["wanted_weapons"]}: {total["completed"]}
Iterations: {original_iterations}
Chances: {total["completed"] / original_iterations * 100}%
Average Starglitter Wishes: {total["totalstarglitter"] / (original_iterations + 1)}
Average 5-Star Character Pity: {total["totalcpity"] / total["totalcharacters"]}
Average 5-Star Wanted Character Pity: {total["totalcpity"]/total["totalwantedcharacters"]}
Average Radiance: {total["totalradiance"] / original_iterations}
Average 5-Star Weapon Pity: {total["totalwpity"] / total["totalweapons"]}
Average 5-Star Wanted Weapon Pity: {total["totalwpity"] / total["totalwantedweapons"]}
Average Optimized: {total["totalepitomized"] / original_iterations}
Total Wishes: {user_data["wishes"]}
Character Goals: {user_data["wanted_characters"]}
Starting Character Pity: {user_data["character"]["5pity"]}
Starting Character Guarantee: {user_data["character"]["5guarantee"]}
Starting Character Radiance: {user_data["radiance"]}
Weapon Goals: {user_data["wanted_weapons"]}
Starting Weapon Pity: {user_data["weapon"]["5pity"]}
Starting Weapon Guarantee: {user_data["weapon"]["5guarantee"]}
Starting Weapon Epitomized: {user_data["epitomized"]}
""")
