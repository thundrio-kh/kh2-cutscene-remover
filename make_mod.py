import os, json, shutil
from kh2lib.kh2lib import kh2lib
lib = kh2lib()

TITLE = "KH2 Cutscene Remover V0.1"

arddir = os.path.join(os.getcwd(), "extracted_ards")
spawndir = os.path.join("spawnscripts")

assets = []

for ard in os.listdir(spawndir):
    programs = []
    for fn in os.listdir(os.path.join(spawndir, ard)):
        programs.append(os.path.join(spawndir, ard, fn))

        
    a = {
        "name": "ard/{}".format(ard),
        "method": "binarc",
        "source": [
            {
                "name": "evt",
                "type": "AreaDataScript",
                "method": "areadatascript",
                "source": [            
                    {
                        "name": programs[i].replace("\\", "/"),
                    }
                    for i in range(len(programs))
                ]
            }
        ]
    }

    assets.append(a)

mod = {
    "originalAuthor": "Thundrio",
    "description": "Removes as many cutscenes as possible. Should be compatible with GOA Randomizer. In beta, let me know of any issues.",
    "title": TITLE,
    "assets": assets,
    "logo": "logo.png"
}
import yaml
yaml.dump(mod, open("mod.yml", "w"))