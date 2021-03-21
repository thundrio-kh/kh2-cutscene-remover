import os, json, shutil
from kh2lib.kh2lib import kh2lib
lib = kh2lib()

TITLE = "KH2 Cutscene Remover"

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
    "description": """READ THIS FIRST
Removes all cutscenes from the game, which decreases load times considerably. Compatible with GOA mod. Report any bugs at https://github.com/thundrio-kh/kh2-cutscene-remover/issues
v1.0
KNOWN ISSUES: 
- If you fail a forced/boss fight, hitting continue will place you back in the fight (effectively a softlock if you can't beat the fight)
- The full screen popups where you acquire an item do not play, you still get the item though
- The following cutscenes are not currentlyremoved in order to prevent softlocks and be compatible with the GOA mod.
  * all cutscenes in Atlantica
  * The cutscenes before and after defeating the boss of Timeless River
  * The cutscene after selecting "Actually" when talking to Yen Sid in TT1
  * The cutscene after talking to the fairies in TT1 to change to KH2 Sora
  * The cutscene after the spinning cubes minigame in SP1
  * The cutscene after finishing the first forced fight in HB 1
  * The cutscene after talking to Leon in Ansems Study during HB 2 (When the secret room is revealed)
  * The cutscene in Garden of Assemblage when turning on the computer""",
    "title": TITLE,
    "assets": assets,
    "logo": "logo.png"
}
import yaml
yaml.dump(mod, open("mod.yml", "w"))