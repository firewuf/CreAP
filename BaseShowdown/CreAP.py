# import requests
import urllib.request as req
from pathlib import Path
VERSION = 1.0
TARGET = 'https://raw.githubusercontent.com/smogon/pokemon-showdown/master/data/'


class Event:
    def __init__(self):
        self.generation = 9
        self.level = 50
        self.gender = ""
        self.nature = ""
        self.perfectIVs = 0
        self.abilities = []
        self.moves = []
        self.isHidden = True
        self.shiny = 0


class Poke:
    def __init__(self):
        self.num = -1
        self.name = ""
        self.internalName = ""
        self.types = []
        self.baseStats = {}
        for stat in ["hp", "atk", "def", "spa", "spd", "spe"]:
            self.baseStats[stat] = 1
        self.abilities = {}
        self.abilities["0"] = "noability"
        self.heightm = 1
        self.weightkg = 1
        self.color = "Red"
        self.eggGroups = []
        self.evos = []
        self.prevo = ""
        self.evoType = ""
        self.evoItem = ""
        self.evoLevel = 0
        self.evoCondition = ""
        self.genderRatio = {"M": 0.5, "F": 0.5}
        self.learnset = {"levelUp": {}, "Tutor/TM": [], "Event": {}, "Egg": {}}
        self.events = []
        self.gender = ""
        self.evoRegion = ""
        self.eventOnly = False

    def update_name(self, newname: str):
        self.name = newname
        self.internalName = newname.lower().replace(" ", "")

    def set_stat(self, stat: str, value: int):
        self.baseStats[stat] = value

    def add_move(self, move: str, method: str, additional: str or int or None):
        # if method == "Event":
        # self.learnset["Event"].append(move)
        if method == "Tutor/TM":
            self.learnset["Tutor/TM"].append(move)
        if method == "levelUp":
            if not additional in self.learnset["levelUp"].keys():
                self.learnset["levelUp"][additional] = []
            self.learnset["levelUp"][additional].append(move)
        if method == "Egg":
            if not move in self.learnset["Egg"].keys():
                self.learnset["Egg"][move] = []
            self.learnset["Egg"][move].append(additional)

    def update_gender_ratio(self, ratio: float):
        self.genderRatio["M"] = ratio
        self.genderRatio["F"] = 1 - ratio

    def update_stats(self, hp, atk, deff, spa, spd, spe):
        self.baseStats["hp"] = hp
        self.baseStats["atk"] = atk
        self.baseStats["def"] = deff
        self.baseStats["spa"] = spa
        self.baseStats["spd"] = spd
        self.baseStats["spe"] = spe

    def assign_event_moves(self):
        newdict = {}
        for i in range(len(self.events)):
            for move in self.events[i].moves:
                if not move in newdict.keys():
                    newdict[move] = []
                newdict[move].append(str(self.events[i].generation) + "S" + str(i))
        self.learnset["Event"] = newdict

    def add_event(self, level: int, gender: str, nature: str, perfectIVs: int, abilities: list[str], moves: list[str],
                  isHidden: bool, shiny: int):
        event = Event()
        event.level = level
        event.gender = gender
        event.nature = nature
        event.perfectIVs = perfectIVs
        event.abilities = abilities
        event.moves = moves
        event.isHidden = isHidden
        event.shiny = shiny
        self.events.append(event)
        self.assign_event_moves()

    def create_code(self) -> str:
        ret = ""
        ret += self.internalName + ": {\n"
        ret += "num: -1,\n"
        ret += "name: \"" + self.name + "\",\n"
        ret += "types: " + str(self.types).replace("'", "\"") + ",\n"
        if self.genderRatio["M"] != 0.5 and self.gender == "":
            ret += "genderRatio: " + str(self.genderRatio).replace("'", "") + ",\n"
        if self.gender != "":
            ret += "gender: \"" + self.gender + "\",\n"
        ret += "baseStats: " + str(self.baseStats).replace("'", "") + ",\n"
        ret += "abilities: {0: \"" + self.abilities["0"] +"\""
        if "1" in self.abilities.keys():
            ret+=", 1: \""+self.abilities["1"] +"\""
        if "H" in self.abilities.keys():
            ret+=", H: \""+self.abilities["H"]+"\""
        if "S" in self.abilities.keys():
            ret+=", S: \""+self.abilities["S"]+"\""
        ret+="},\n"
        ret += "heightm: " + str(self.heightm) + ",\n"
        ret += "weightkg: " + str(self.weightkg) + ",\n"
        ret += "color: \"" + self.color + "\",\n"
        if self.prevo != "":
            ret += "prevo: \"" + self.prevo + "\",\n"
        if self.evoLevel != 0:
            ret += "evoLevel: " + str(self.evoLevel) + ",\n"
        if self.evoType != "":
            ret += "prevo: \"" + self.evoType + "\",\n"
        if self.evoItem != "":
            ret += "prevo: \"" + self.evoItem + "\",\n"
        if self.evoCondition != "":
            ret += "prevo: \"" + self.evoCondition + "\",\n"
        if self.evoRegion != "":
            ret += "prevo: \"" + self.evoRegion + "\",\n"
        if len(self.evos) > 0:
            ret += "evos: " + str(self.evos).replace("'", "\"") + ",\n"
        ret += "eggGroups: " + str(self.eggGroups).replace("'", "\"") + ",\n"

        ret += "},"
        return ret

    def create_full_move_dict(self) -> dict:
        ret = {}
        self.assign_event_moves()
        # {"levelUp": {}, "Tutor/TM": [], "Event": {}, "Egg": {}}
        for move in self.learnset["Tutor/TM"]:
            if move not in ret.keys():
                ret[move] = []
            ret[move].append("9M")
        for level in self.learnset["levelUp"].keys():
            for move in self.learnset["levelUp"][level]:
                if move not in ret.keys():
                    ret[move] = []
                ret[move].append("9L" + str(level))
        for move in self.learnset["Egg"].keys():
            if move not in ret.keys():
                ret[move] = []
            ret[move].append("9E")
        for move in self.learnset["Event"].keys():
            if move not in ret.keys():
                ret[move] = []
            for value in self.learnset["Event"][move]:
                ret[move].append(value)
        return ret

    def create_move_code(self) -> str:
        fulllearnset = self.create_full_move_dict()
        # print(fulllearnset)
        ret = ""
        ret += self.internalName + ": {\nlearnset: {\n"
        for key in sorted(fulllearnset.keys()):
            ret += key + ": " + str(fulllearnset[key]).replace("'", "\"") + ",\n"
        ret += "},\n"
        if len(self.events) > 0:
            ret += "eventData: [\n"
            for event in self.events:
                ret += "{generation: " + str(event.generation) + ", level: " + str(event.level)
                if event.shiny == 1:
                    ret += ", shiny: 1"
                if event.gender != "":
                    ret += ", gender: " + event.gender
                if event.nature != "":
                    ret += ", nature: " + event.nature
                if event.perfectIVs != 0:
                    ret += ", perfectIVs: " + str(event.perfectIVs)
                if event.isHidden:
                    ret += ", isHidden: true"
                ret += ", moves: " + str(event.moves).replace("'", "\"")
                ret += ", pokeball: \"cherishball\"},\n"
            ret += "],\n"
        if self.eventOnly:
            ret += "eventOnly: true,\n"
        ret += "},"
        return ret


def get_ts(target: str, file: str) -> None:
    request = req.Request(target + file + '.ts')
    response = req.urlopen(request)
    f = open(file + ".ts", "w+")
    f.write(response.read().decode(encoding='utf-8'))
    f.write("Moth says end of file")
    response.close()


def refresh_files() -> None:
    get_ts(TARGET, "learnsets")
    get_ts(TARGET, "moves")
    get_ts(TARGET, "pokedex")
    get_ts(TARGET, "abilities")
    get_ts(TARGET, "items")
    get_ts(TARGET, "conditions")
    #get_ts(TARGET, "text/abilities")
    #get_ts(TARGET, "text/moves")


def moves_to_dict() -> dict:
    with open("moves.ts", "r+") as f:
        ret = {}
        line = f.readline().strip()
        # print(line)
        depth = 0
        while line != "Moth says end of file":
            # print(line)
            # print(currdict)
            # print(depth)
            if "{" in line and depth == 1:
                move = line.split(":", maxsplit=1)[0]
                ret[move] = {}
                # print(move)
            if depth == 2 and ":" in line:
                key = line.split(":")[0]
                element = line.split(":", maxsplit=1)[1].strip()
                if key in ["accuracy", "basePower", "category", "name", "pp", "priority", "flags", "secondary",
                           "target", "type", "boosts", "critRatio", "self"]:
                    if key == "secondary" or key == "self":
                        ret[move][key] = "TODO"
                    else:
                        ret[move][key] = element[0:-1]
                # print(key, element)
            depth += line.count("{")
            depth -= line.count("}")
            line = f.readline().strip()
            # print(line)
        return ret


def abilities_to_dict() -> dict:
    with open("abilities.ts", "r+") as f:
        ret = {}
        line = f.readline().strip()
        # print(line)
        depth = 0
        while line != "Moth says end of file":
            # print(line)
            # print(currdict)
            # print(depth)
            if "{" in line and depth == 1:
                ability = line.split(":", maxsplit=1)[0]
                ret[ability] = {}
                # print(ability)
            if depth == 2 and ":" in line:
                key = line.split(":")[0]
                element = line.split(":", maxsplit=1)[1].strip()
                if key in ["name", "flags", "rating"]:
                    if key == "secondary" or key == "self":
                        ret[ability][key] = "TODO"
                    else:
                        ret[ability][key] = element
                # print(key, element)
            depth += line.count("{")
            depth -= line.count("}")
            line = f.readline().strip()
            # print(line)
        return ret


class Filtereq:
    def __init__(self, target, thresh):
        self.target = target
        self.thresh = thresh

    def filter(self, keys: list, dic: dict) -> list:
        return [key for key in keys if dic[key][self.target] == self.thresh]


class Filterless:
    def __init__(self, target, thresh):
        self.target = target
        self.thresh = thresh

    def filter(self, keys: list, dic: dict) -> list:
        ret = []
        for key in keys:
            try:
                if float(dic[key][self.target]) <= self.thresh:
                    ret.append(key)
            except:
                pass
        return ret


class Filtermore:
    def __init__(self, target, thresh):
        self.target = target
        self.thresh = thresh

    def filter(self, keys: list, dic: dict) -> list:
        ret = []
        for key in keys:
            try:
                if float(dic[key][self.target]) >= self.thresh:
                    ret.append(key)
            except:
                pass
        return ret


def multifilter(keys: list, dic: dict, filters: list["Filter"]) -> list:
    for i in filters:
        keys = i.filter(keys, dic)
    return keys


if not (Path("abilities.ts").exists() and Path("conditions.ts").exists() and Path("items.ts").exists() and Path(
        "learnsets.ts").exists() and Path("moves.ts").exists() and Path("pokedex.ts").exists()):
    print("files missing, redownloading all")
    refresh_files()
print("CreAP by Moth, use responsibly")

if __name__ == "__main__":
    moves = moves_to_dict()
    abilities = abilities_to_dict()
    bulba = Poke()
    bulba.update_name("Bulbasaur")
    bulba.types.append("Grass")
    bulba.types.append("Poison")
    bulba.update_gender_ratio(0.875)
    bulba.update_stats(45, 49, 49, 65, 65, 45)
    bulba.abilities["0"] = "Overgrow"
    bulba.abilities["H"] = "Chlorophyll"
    bulba.heightm = 0.7
    bulba.weightkg = 6.9
    bulba.color = "Green"
    bulba.evos.append("Ivysaur")
    bulba.eggGroups.append("Monster")
    bulba.eggGroups.append("Grass")
    print(bulba.create_code())
    print("")
    bulba.add_event(5, "M", "", 0, ["Overgrow"], ["explosion", "dracometeor"], False, 1)
    bulba.add_move("tackle", "levelUp", 1)
    bulba.add_move("growl", "levelUp", 1)
    bulba.add_move("vinewhip", "levelUp", 5)
    bulba.add_move("outrage", "Egg", "Salamence")
    bulba.add_move("outrage", "Egg", "Bagon")
    bulba.add_move("earthquake", "Tutor/TM", None)
    bulba.add_move("vinewhip", "Tutor/TM", None)
    # print(bulba.events[0])
    # print(bulba.learnset)
    print(bulba.create_move_code())
    print("")
    # print(moves['airslash'])
    # print(abilities["flashfire"])
    for i in multifilter(list(moves.keys()), moves,
                         [Filtereq("type", "\"Grass\""), Filtermore("basePower", 80), Filterless("accuracy", 95)]):
        print(i)
