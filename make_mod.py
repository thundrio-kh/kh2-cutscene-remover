import os, json, shutil
from kh2lib.kh2lib import kh2lib
lib = kh2lib()

TITLE = "KH2 Cutscene Remover V0.5"

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
    "description": """Removes as many cutscenes as possible. Compatible with GOA mod. 
KNOWN BUGS: 
- If you fail a forced/boss fight, hitting continue will place you back in the fight (effectively a softlock if you can't beat the fight)
- The full screen popups where you acquire an item do not play, you still get the item though""",
    "title": TITLE,
    "assets": assets,
    "logo": "logo.png"
}
import yaml
yaml.dump(mod, open("mod.yml", "w"))