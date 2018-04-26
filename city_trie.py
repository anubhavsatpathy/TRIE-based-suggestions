import json
from pprint import pprint
import sys

data = json.load(open("city_list.json"))
compare_data = json.dumps(json.load(open("ty_city_list.json")))
d = json.dumps(data)
#pprint(data)
city_list = []
for i in range(len(data["data"]["raw"])):
    city_list.append((data["data"]["raw"][i]["details"]["name"].lower(),data["data"]["raw"][i]['display_name']))
pprint("Total number of city names : " + str(len(city_list)))
#pprint(city_list)
trie = {name[0][0]:{} for name in city_list}
resp = {"success" : True}
for name, display in city_list:
    current_dict = trie
    for i in range(len(name)):
        if name[i] in current_dict.keys():
            current_dict = current_dict[name[i]]
        else:
            current_dict[name[i]] = {}
            if i == (len(name)- 1):
                current_dict[name[i]]["end"] = True
                current_dict[name[i]]["count"] = 0
                current_dict[name[i]]["disp"] = display
            current_dict = current_dict[name[i]]

resp["data"] = trie
res = json.dumps(resp)
json.dump(resp,open("trie_json.json",'w'))
def add_search_count(city_name):
    current_dict = trie
    for i in range(len(city_name)):
        if city_name[i] not in current_dict.keys():
            return "Name not present"
        else:
            current_dict = current_dict[city_name[i]]
            if i == (len(city_name)-1):
                current_dict["count"] += 1


def retreive_suggestions(prefix):
    current_dict = trie
    for ch in prefix:
        if ch not in current_dict:
            return []
        else:
            current_dict = current_dict[ch]
    is_word(current_dict)

suggestions = []

def is_word(d):
    if "end" in d.keys():
        suggestions.append((d["disp"],d["count"]))
        return None
    else:
        for k in d.keys():
            is_word(d[k])

print("TRIE for the letter c")
pprint(trie["c"])
add_search_count("bengaluru")


retreive_suggestions("ben")
print(suggestions)
#retreive_suggestions("mys")
print(type(compare_data))
print(sys.getsizeof(compare_data))
print(type(res))
print(sys.getsizeof(res))
