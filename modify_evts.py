# Extract everything if not extracted

# Check all the flags to make sure I don't set one used by the game
import os, json, shutil
from kh2lib.kh2lib import kh2lib
lib = kh2lib()

EXTRACT_ARDS=False


arddir = os.path.join(os.getcwd(), "extracted_ards")
if EXTRACT_ARDS:    
    if os.path.exists(arddir):
        shutil.rmtree(arddir)
    os.mkdir(arddir)

spawndir = os.path.join(os.getcwd(), "spawnscripts")
if os.path.exists(spawndir):
    shutil.rmtree(spawndir)
os.mkdir(spawndir)

ardinfo = {}
ignore_worlds = [
    "lm" # little mermaid is all cutscenes lol so it softlocks
]
ignore_ards = [
    "lk08.ard", # Entering jungle for second visit story crashes pcsx2
    "wi03.ard", # Beating WI causes the portal to not turn purple
    "dc05.ard", # Marluxias portal doesn't show up after beating WI
    "hb05.ard", # Causes you to be sent to SP instead of skipping it, and makes the HB portal send you to Data Demyx
    "tt32.ard", # Causes GOA Mod to not give out the weapons of each ally, preventing second visits from working
]
# These issues might all be related to GOA mod
# I need to know if there are any areas in the game where a mission starts without a cutscene beforehand
ignore_programs = {
    "tt27.ard": ["0x02"], # Talking to yen sid
    "tt28.ard": ["0x02"], # changing to kh2 sora
    "tr01.ard": ["0x33"], # causes entering SP the second time to go to data larxene
    "hb09.ard": ["0x33"], # causes first cutscene in merlin to not fire
    # "hb05.ard": ["0x02", "0x05", "0x06", "0x08"], # Causes you to be sent to SP instead of skipped, and makes demyx portal real
    "hb26.ard": ["0x01"] # Prevents the third chest from showing up in GOA
}

# I have a check to not skip cutscenes with type > 100 because those tend to signify menu events
# but sometimes (like with postgame cutscenes) these are real cutscenes that should be removed
always_remove = {
    "eh20.ard": [
        "0x4A" # postgame
    ]
}

custom_jumps = {
    "eh20.ard": {
        # Postgame
        "0x4A": '\tSetJump Type 5 World ES Area 0 Entrance 0 LocalSet 0 FadeType 16385\n'
    }
}

SKIPLINE = "	SetProgressFlag 0xFFF\n"
unskippable = []
ignored = []
def getCustomJump(ard, program,line):
    if ard in custom_jumps:
        if program in custom_jumps[ard]:
            print("custom jumping over: {}".format(line))
            return custom_jumps[ard][program]
    return False

def shouldIgnore(ard, program, eventtype):
    ignore = False
    if ard[:2] in ignore_worlds:
        ignore = True
    if ard in ignore_ards:
        ignore = True
    # NEEDED To make choosing weapons work
    if int(eventtype) >= 128:
        unskippable.append("{}-{}".format(ard,program))
        ignore = True
    if ard in ignore_programs:
        if program.strip() in ignore_programs[ard]:
            ignore = True
    if ard in always_remove:
        if program.strip() in always_remove[ard]:
            ignore = False
    if ignore:
        ignored.append("{}-{}".format(ard,program.strip()))
    return ignore

arddir_src = os.path.join(os.environ["USE_KH2_GITPATH"], "KH2", "ard")

last_asetting = ''
asettings = {}
eventtypes = []
for ard in os.listdir(arddir_src):
    fn = os.path.join(arddir_src, ard)

    out_pth = os.path.join(arddir, ard)
    if EXTRACT_ARDS:
        lib.editengine.bar_extract(fn, out_pth)
    
    evtname = None
    for f in [i for i in os.listdir(out_pth) if not i.endswith(".txt") and not i.endswith(".new")]:
        if f.startswith("evt."):
            evtname = f

    ardinfo[ard] = {
        "fn": fn,
        "out_pth": out_pth
    }
    if evtname == None:
        print("ARD {} has no evt".format(ard))
    else:
        evt_pth = os.path.join(out_pth, evtname)
        if EXTRACT_ARDS:
            lib.editengine.spawnscript_extract(evt_pth, evt_pth+".txt")
        
        lines = open(evt_pth+".txt")
        lines_new = []
        currentProgram = ''
        lines_program = []
        changesMade = False
        for line in lines:
            if line.startswith("Program"):
                if len(currentProgram) > 0:
                    if changesMade:
                        spawnscriptsdir = os.path.join(spawndir, ard)
                        if not os.path.exists(spawnscriptsdir):
                            os.mkdir(spawnscriptsdir)
                        programfn = os.path.join(spawnscriptsdir, "program-"+currentProgram.lower().replace(" ", "")[2:].strip())
                        for l in range(len(lines_program)):
                            settingline = lines_program[l]
                            # The barrels mission restarts always if the first settings argument is a 0, is it some kind of bitflag?
                            if False and "AreaSettings" in settingline:
                                settings = settingline.split(" ")
                                bitrep = "{0:b}".format(int(settings[1]))
                                if not bitrep[-1] == 1:
                                    
                                    newline = "AreaSettings {} {}".format(int(bitrep[:-1]+'1',2), settings[2])
                                    lines_program[l] = newline
                        with open(programfn, "w") as f:
                            f.write(''.join(lines_program))
                    lines_program = []
                    changesMade = False
                currentProgram = line.split(" ")[1]
            if len(currentProgram) > 0:
                if "SetEvent" in line:
                    eventtype = line.strip().split(" ")[3]
                    eventtypes.append("{} - {}".format(eventtype.zfill(3), ard))
                if "AreaSettings" in line:
                    setting = line.strip()
                    lastasetting = setting
                    if setting not in asettings:
                        asettings[setting] = 0
                    asettings[setting] += 1
                if "SetJump" in line:
                    customjump = getCustomJump(ard, currentProgram.strip(), line)
                if "SetEvent" in line and not shouldIgnore(ard, currentProgram, eventtype):
                        changesMade = True
                    #lines_program.append(SKIPLINE)
                    #lines_new.append(SKIPLINE)
                elif "SetJump" in line and customjump:
                    lines_program.append(customjump)
                    changesMade = True
                else:
                    lines_program.append(line)
                    lines_new.append(line)
        # Changes made here need to happen up above too
        if changesMade:
            spawnscriptsdir = os.path.join(spawndir, ard)
            if not os.path.exists(spawnscriptsdir):
                os.mkdir(spawnscriptsdir)
            programfn = os.path.join(spawnscriptsdir, "program-"+currentProgram.lower().replace(" ", "")[2:].strip())
            with open(programfn, "w") as f:
                f.write(''.join(lines_program))
        open(evt_pth+".txt.new","w").write("".join(lines_new))

print("The following were ignored")
print(ignored)
print(unskippable)
for aset in asettings:
    print("{}-{}".format(asettings[aset],aset))