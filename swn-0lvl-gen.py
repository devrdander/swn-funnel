import random
import PIL
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import argparse
from fpdf import FPDF
import os

#Background Table and quick skills
background = dict()
background[1] = ['Barbarian', 'Survive', 'Notice', '(Stab, Shoot, or Punch)']
background[2] = ['Clergy', 'Talk', 'Perform', 'Know']
background[3] = ['Courtesan', 'Perform', 'Notice', 'Connect']
background[4] = ['Criminal', 'Sneak', 'Connect', 'Talk']
background[5] = ['Dilettante', 'Connect', 'Know', 'Talk']
background[6] = ['Entertainer', 'Perform', 'Talk', 'Connect']
background[7] = ['Merchant', 'Trade', 'Talk', 'Connect']
background[8] = ['Noble', 'Lead', 'Connect', 'Administer']
background[9] = ['Official', 'Administer', 'Talk', 'Connect']
background[10] = ['Peasant', 'Exert', 'Sneak', 'Survive']
background[11] = ['Physician', 'Heal', 'Know', 'Notice']
background[12] = ['Pilot', 'Pilot', 'Fix', 'Shoot or Trade']
background[13] = ['Politician', 'Talk', 'Lead', 'Connect']
background[14] = ['Scholar', 'Know', 'Connect', 'Administer']
background[15] = ['Soldier', '(Stab, Shoot, or Punch)', 'Exert', 'Survive']
background[16] = ['Spacer', 'Fix', 'Pilot', 'Program']
background[17] = ['Technician', 'Fix', 'Exert', 'Notice']
background[18] = ['Thug', '(Stab, Shoot, or Punch)', 'Talk', 'Connect']
background[19] = ['Vagabond', 'Survive', 'Sneak', 'Notice']
background[20] = ['Worker', 'Connect', 'Exert', 'Work']

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num', type=int, default=1, help="Number of Characters to Create", required=False)
    parser.add_argument('--incbg', type=str, help="List of Backgrounds to Include. ex: --incbg 1,4,7", required=False)
    parser.add_argument('--excbg', type=str, help="List of Backgrounds to Exclude. ex: --excbg 2,9,14", required=False)
    parser.add_argument('--listbg', action="store_true", required=False, help='Only List Backgrounds')
    parser.add_argument('--p2up', action="store_true", required=False, help='Generate PDF with 2 sheets per page')
    parser.add_argument('--p4up', action="store_true", required=False, help='Generate PDF with 4 sheets per page')
    return parser.parse_args()

def addTxt(width, height, msg, size, font_fname):
    #font_fname = "./Gayatri.ttf"
    font_size = size
    font = ImageFont.truetype(font_fname, font_size)
    W, H = (width,height)
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(msg, font=font)
    draw.text((W-(w/2),H-(h/2)), msg, font=font, fill='rgb(0, 0, 0)')
    return

def genStat(statName, width, height, save):
    statValue = random.randint(1,6)+random.randint(1,6)+random.randint(1,6)
    if statValue < 4:
        statMod = -2
    elif statValue < 8:
        statMod = -1
    elif statValue < 14:
        statMod = 0
    elif statValue < 18:
        statMod = 1
    else:
        statMod = 2
    addTxt(width, height, str(statValue), 75, "./Gayatri.ttf")
    if statMod > 0:
        addTxt(width+130, height, '+' + str(statMod), 50, "./Gayatri.ttf")
    else:
        addTxt(width+130, height, str(statMod), 50, "./Gayatri.ttf")
    #Set AC
    if statName is 'DEX':
        addTxt(555, 315, str(baseac+statMod), 75, "./Gayatri.ttf")
    if statName is 'CON':
        hp = random.randint(1,hitdie)+statMod
        if hp < 1:
            hp = 1
        addTxt(1968, 277, str(hp), 75, "./Gayatri.ttf")
    #Set Save
    if save < statMod:
        save = statMod

    return save

def p2up(path):
    dirListing = os.listdir(path)
    imgFiles = []
    for item in dirListing:
        if '.jpg' in item:
            imgFiles.append(path+'/'+item)

    pdf2 = FPDF('P', 'mm', 'Letter')
    items = len(imgFiles)
    for i in range(items):
        if i % 2 == 0:
            file1=imgFiles[i]
            file2=imgFiles[i+1]
            w = 170
            h = 131
            pdf2.add_page()
            pdf2.image(file1,23,8,w,h)
            pdf2.image(file2,23,140,w,h)
    pdf2.output("p2up.pdf", "F")
    print('Created p2up.pdf.')

def p4up(path):
    dirListing = os.listdir(path)
    imgFiles = []
    for item in dirListing:
        if '.jpg' in item:
            imgFiles.append(path+'/'+item)

    pdf4 = FPDF('L', 'mm', 'Letter')
    items = len(imgFiles)
    for i in range(items):
        if i % 4 == 0:
            file1=imgFiles[i]
            file2=imgFiles[i+1]
            file3=imgFiles[i+2]
            file4=imgFiles[i+3]
            w = 131
            h = 101
            pdf4.add_page()
            pdf4.image(file1,8,8,w,h)
            pdf4.image(file2,140,8,w,h)
            pdf4.image(file3,8,109,w,h)
            pdf4.image(file4,140,109,w,h)
    pdf4.output("p4up.pdf", "F")
    print('Created p4up.pdf.')

if __name__ == "__main__":
    args = parse_args()

    #Customize Background dictionary
    if args.incbg:
        incbg = [int(item) for item in args.incbg.split(',')]
        keypop=[]
        for key in background:
            if key not in incbg:
                keypop.append(key)
        for key in keypop:
            background.pop(key)
    elif args.excbg:
        excbg = [int(item) for item in args.excbg.split(',')]
        for key in excbg:
            background.pop(key)

    #Print List of Backgrounds
    if args.listbg:
        for k,v in background.items():
            print(str(k) + ' - ' + v[0] + ': ' + v[1] + ', ' + v[2] + ', ' + v[3])
    else:
        #Clean up old files:
        print('Cleaning up Old Files.')
        path = './out'
        clear=os.listdir(path)
        for item in clear:
            if item.endswith(".jpg"):
                os.remove(path + '/' + item)

        print('Generating Characters.')
        #Process Character Sheets
        for i in range(args.num):
            img = Image.open('lvl0-base.jpg')

            #Base Variables:
            hitdie = 4
            baseac = 10
            pSave = 0
            eSave = 0
            mSave = 0

            pSave = genStat('STR', 365, 692, pSave)
            pSave = genStat('CON', 365, 979, pSave)
            eSave = genStat('DEX', 295, 834, eSave)
            eSave = genStat('INT', 295, 1118, eSave)
            mSave = genStat('WIS', 365, 1262, mSave)
            mSave = genStat('CHA', 295, 1408, mSave)

            #Add Saves
            addTxt(780, 420, str(16-pSave), 75, "./Gayatri.ttf")
            addTxt(1020, 420, str(16-eSave), 75, "./Gayatri.ttf")
            addTxt(1264, 420, str(16-mSave), 75, "./Gayatri.ttf")

            #Generate BG and Skills
            bgnum = random.choice(list(background))
            value = background[bgnum]

            addTxt(1850, 151, value[0], 60, "./Crimson-Semibold.otf")
            addTxt(925, 690, value[1], 50, "./Crimson-Semibold.otf")
            addTxt(1312, 690, '0', 50, "./Gayatri.ttf")
            addTxt(925, 759, value[2], 50, "./Crimson-Semibold.otf")
            addTxt(1312, 759, '0', 50, "./Gayatri.ttf")
            addTxt(925, 832, value[3], 50, "./Crimson-Semibold.otf")
            addTxt(1312, 832, '0', 50, "./Gayatri.ttf")
            imgname = str(i) + value[0] + '.jpg'
            print('Generated: ' + imgname)
            img.save('out/' + imgname)

        #Create PDFs if Requested
        if args.p4up:
            print('Creating PDF with 4 Sheets Per Page')
            p4up(path)
        if args.p2up:
            print('Creating PDF with 2 Sheets Per Page')
            p2up(path)
