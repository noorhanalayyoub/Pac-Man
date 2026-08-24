import json
import sys

if len(sys.argv) > 1:
    file = sys.argv[1]
    f = open(file, "r")
    data = json.load(f)
    lives = data["lives"]
    points_per_pacgum = data["points_per_pacgum"]
    points_per_super_pacgum = data["points_per_super_pacgum"]
    points_per_ghost = data["points_per_ghost"]
    seed = data["seed"]
    level_max_time = data["level_max_time"]
    f.close()
else:
    print("\n \033[31m please provide a config file")
    exit(1)
