import random
import json

with open("final_database_v1.json") as f:
    data = json.load(f)
    
num = random.randint(0, len(data))

random_data = data[num]['description']
print(random_data)