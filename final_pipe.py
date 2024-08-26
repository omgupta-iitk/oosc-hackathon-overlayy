from final_llm import run
#from valid import valid
from scrape_new import begin, base_link
import json

def merge_json(json1, json2):
    merged = json1.copy()  # Start with a copy of the first JSON
    for key, value in json2.items():
        if key in merged:
            # Handle overlapping keys (e.g., by appending values)
            if isinstance(merged[key], list):
                merged[key].append(value)
            else:
                merged[key] = [merged[key], value]
        else:
            merged[key] = value
    return merged

begin() 
questions = run()

with open("links.json",'r') as file:
    data = json.load(file)


ques = {"url": base_link(),"questions":questions}
merged_json = merge_json(ques, data)
with open("output.json", "w") as json_file:
    json.dump(merged_json, json_file, indent=4)

#valid()
