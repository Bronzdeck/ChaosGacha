import sys
from tkinter import *
from tkinter import messagebox
import random
import os
import re
import webbrowser
import subprocess
pgmode = 0
classicfamiliar = 0
scifi = 0

def read_file_with_weight(filename,avg,min,max): # Creates a list of the available gacha pulls within the rarity range
    elements = []
    weights = []
    rarities = []
    descriptions = []
    tempdescription = []
    weightsum = 0
    minrarity = float(min)
    avgrarity = float(avg)
    maxrarity = float(max)
    pgtext = "(Nsfw)"
    familiartext = "(Character)"
    scifitext = "(Tech)"
    if filename == 'random':
        filename = ['ability','item','familiar','trait', 'skill']
        filename = random.choice(filename)
    chosentype = filename.capitalize()
    filename += '.txt'
    filename = os.path.join("gachafiles", filename)
    with open(filename, 'r') as file:
        for line in file:
            match = re.match(r'^(\d+)\.(\S*)\s*(.*)', line) # Checks if the line starts with a number heading such as "23." or "167. "
            if match:
                parts = line.strip().split(',')
                element, rarity = parts[0], parts[1]
                #print(element, rarity)
                elements.append(element)
                weights.append(1 / (pow(4, abs(avgrarity - (float(rarity))))))  # Convert weight to integer
                if(float(rarity) <= maxrarity and minrarity < float(rarity)):
                    weightsum += (1 / (pow(4, abs(avgrarity - (float(rarity))))))
                rarities.append(float(rarity))
                if (tempdescription):
                    descriptions.append(' '.join(tempdescription).strip())
                    tempdescription = []
            else: # If the line doesn't start with a number heading it is a part of the description.
                if pgtext in line:
                    if pgmode:
                        elements.pop()
                        weights.pop()
                        rarities.pop()
                        continue
                    line = line.replace(pgtext, "")
                    #print("Replaced:" + line)
                if familiartext in line:
                    if classicfamiliar:
                        elements.pop()
                        weights.pop()
                        rarities.pop()
                        continue
                    line = line.replace(familiartext, "")
                if scifitext in line:
                    if scifi:
                        elements.pop()
                        weights.pop()
                        rarities.pop()
                        continue
                    line = line.replace(familiartext, "")
                tempdescription.append(line)
    if (tempdescription):
        descriptions.append(' '.join(tempdescription).strip())
        tempdescription = []
    return elements,weights,rarities,descriptions, weightsum, chosentype

def randomizer(min,max,avg,exponent):
    floatmax = float(max)
    floatmin = float(min)
    floatavg = float(avg)
    x = floatmin
    randarr = []
    weights = []
    while(x < floatmax):
        randarr.append(x)
        x+=0.1
        weights.append(1 / (pow(float(exponent), abs(floatavg - (float(x))))))  # Convert weight to integer
    rarity = random.choices(randarr, weights)
    total_weight = sum(weights)
    rarity[0] += 0.1
    return float(rarity[0])

def run_gacha(type,min,avg,max,pullcount): # type - gacha mode, min-avg-max - rarities
    elements, weights, rarities, descriptions, weightsum, chosentype = read_file_with_weight(type,avg,min,max)
    runcount = 0
#    averagepull = 0
#    averagecheck = 0
    while runcount < pullcount:
        raritypull = randomizer(min,max,avg,4)
        #print(raritypull)
        filtered_rarities = [val for val in rarities if abs(val - raritypull) <= 0.2]
        filtered_elements = [elem for elem, val in zip(elements, rarities) if abs(val - raritypull) <= 0.2]
        filtered_weights = [weight for weight, val in zip(weights, rarities) if abs(val - raritypull) <= 0.2]
        filtered_descriptions = [description for description, val in zip(descriptions, rarities) if abs(val - raritypull) <= 0.2]
        #print( str(len(filtered_elements)) + ' ' + str(len(filtered_weights)) + ' ' + str(len(filtered_rarities)) + ' ' + str(len(filtered_descriptions)))
        #print(str(len(elements)) + ' ' + str(len(weights)) + ' ' + str(len(descriptions)) + ' ' + str(len(rarities)))
        if len(filtered_elements) == 0:
            continue
        index = random.choices(range(len(filtered_elements)), weights=filtered_weights)
        luckpercentage = 100 * filtered_weights[index[0]]/weightsum
        selected_element = filtered_elements[index[0]]
        selected_rarity = filtered_rarities[index[0]]
        selected_description = filtered_descriptions[index[0]]
        selected_description = selected_description.replace('#','')
        print(f"Selected element: {selected_element} with rarity: {selected_rarity} and {round(luckpercentage, 2)}% odds")
        if selected_rarity < 1.0:
            color = '#a39589'
            tier = 'Trash'
        elif selected_rarity < 2.0:
            color = '#9c7e5a'
            tier = 'Common'
        elif selected_rarity < 3.0:
            color = '#aed1d1'
            tier = 'Uncommon'
        elif selected_rarity < 4.0:
            color = '#11d939'
            tier = 'Rare'
        elif selected_rarity < 5.0 :
            color = '#1172d9'
            tier = 'Elite'
        elif selected_rarity < 6.0 :
            color = '#6811d9'
            tier = 'Epic'
        elif selected_rarity < 7.0:
            color = '#f7d40a'
            tier = 'Legendary'
        elif selected_rarity < 8.0 :
            color = '#fc61ff'
            tier = 'Mythical'
        elif selected_rarity < 9.0:
            color = '#ff8c00'
            tier = 'Divine'
        else:
            color = '#ff0000'
            tier = 'Transcendent'
        resultLabel.config(text=selected_element +  ' ' + str(selected_rarity) + ' (' + str(round(luckpercentage, 2)) + '%)', fg=color)
        headerLabel.config(text= '-'+tier+' ' + chosentype + '-', fg=color)
#        print("length of description : " + str(len(selected_description)))
        descriptionLabel.config(text=selected_description)
        runcount += 1
#        averagecheck += raritypull
#        averagepull += selected_rarity
#    averagepull = averagepull/pullcount
#    raritypull =averagecheck/pullcount
#    print("Average rarity: " + str(averagepull) + ' ' + str(raritypull))

def prepare_gacha():
    global activemode
    mode = activemode
    minvalue = float(min.get())
    maxvalue = float(max.get())
    avgvalue = float(w.get())
    run_gacha(mode,minvalue,avgvalue,maxvalue,1)

def select_mode(mode):
    global activemode
    abilityButton.configure(fg='#fff')
    itemButton.configure(fg='#fff')
    traitButton.configure(fg='#fff')
    skillButton.configure(fg='#fff')
    familiarButton.configure(fg='#fff')
    randomButton.configure(fg='#fff')
    if mode == "ability":
        abilityButton.configure(fg="#11d939")
        activemode = "ability"
    if mode == "item":
        itemButton.configure(fg="#11d939")
        activemode = "item"
    if mode == "trait":
        traitButton.configure(fg="#11d939")
        activemode = "trait"
    if mode == "skill":
        skillButton.configure(fg="#11d939")
        activemode = "skill"
    if mode == "familiar":
        familiarButton.configure(fg="#11d939")
        activemode = "familiar"
    if mode == "random":
        randomButton.configure(fg="#11d939")
        activemode = "random"

def select_preset(preset):
    w.configure(state='normal')
    min.configure(state='normal')
    max.configure(state='normal')
    w.delete(0, "end")
    w.insert(0, str(presetavg[preset]))
    min.delete(0, "end")
    min.insert(0, str(presetmin[preset]))
    max.delete(0, "end")
    max.insert(0, str(presetmax[preset]))
    min.configure(state='readonly')
    max.configure(state='readonly')
    w.configure(state='readonly')
    selectedLabel.configure(text='Selected: ' + presets[preset])

def copy_description():
    temptxt = resultLabel.cget('text')
    cleaned_text = re.search(r'\.([^\d]+)\d+', temptxt)
    text = cleaned_text.group(1)
    text = text[:-1]
    text2 = headerLabel.cget('text')
    text2 = text2.replace("-","|")
    text2 = text2[1:]
    txt = '['+ text + ']\n' + '|Rarity: ' +  text2 + '\n' +  descriptionLabel.cget('text')
    subprocess.run("clip", input=txt.strip().encode('utf-8'), shell=True)

def toggle_logs():
    global logs_enabled
    global log_frame
    if logs_enabled:
        root.geometry("1024x668")
        if log_frame:
            log_frame.destroy()
            sys.stdout = original_stdout
        logs_enabled = False
    else:
        root.geometry("1624x668")
        enable_logs()
        logs_enabled = True

def enable_logs():
    global log_frame
    log_frame = Frame(root, bg="black")
    log_frame.pack(side=RIGHT, fill=Y)

    log_text = Text(log_frame, wrap=NONE, height=668, width=74, bg="#1f1f1f", fg="white", borderwidth=2)
    log_text.pack(fill=BOTH, expand=True)

    # Redirect print() to the log widget
    sys.stdout = TextRedirector(log_text)

class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(END, message)
        self.text_widget.see(END)  # Auto-scroll to latest log

    def flush(self):
        pass  # Needed for compatibility with sys.stdout

def open_settings():
    global settings_window
    global familiar_button
    global pg_button
    global scifi_button
    if settings_window and settings_window.winfo_exists():  # Check if window already exists
        settings_window.lift()  # Bring existing window to front
        return
    settings_window = Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("280x400")
    settings_window.configure(background='#1f1f1f', highlightbackground="#646464", highlightthickness=3)
    settings_window.resizable(False, False)
    logs_button = Button(settings_window, text='Enable Logs', width=12, command=lambda: toggle_logs(), font=(selectedfont, 12), background='#111', fg='#FFF')
    logs_button.place(x=138, y=40, in_=settings_window, anchor="center")
    text_options = ["Courier", "Arial", "Times New Roman", "Comic Sans MS", "Papyrus", "Wingdings"]
    if font_selection.get() == "":
        font_selection.set("Courier")
    font_menu = OptionMenu(settings_window, font_selection, *text_options)
    font_menu.place(x=138, y=100, in_=settings_window, anchor="center")
    font_menu.configure(pady=10, padx=30, background='#1f1f1f', activebackground='#1f1f1f', foreground='white', activeforeground='white')
    font_selection.trace_add("write", update_font)
    pg_button = Button(settings_window, text='PG Mode: Off', width=24, command=lambda: togglefilter("pgmode"), font=(selectedfont, 12), background='#111', fg='#FFF')
    pg_button.place(x=138, y=160, in_=settings_window, anchor="center")
    familiar_button = Button(settings_window, text='Classic Familiars: Off', width=24, command=lambda: togglefilter("classicfamiliar"), font=(selectedfont, 12), background='#111', fg='#FFF')
    familiar_button.place(x=138, y=200, in_=settings_window, anchor="center")
    scifi_button = Button(settings_window, text='No Scifi: Off', width=24, command=lambda: togglefilter("scifi"), font=(selectedfont, 12), background='#111', fg='#FFF')
    scifi_button.place(x=138, y=240, in_=settings_window, anchor="center")
    text_options = ["Courier", "Arial", "Times New Roman", "Comic Sans MS", "Papyrus", "Wingdings"]
    updateoptions()

def togglefilter(filtertype):
    global pgmode
    global classicfamiliar
    global scifi
    if filtertype == "pgmode":
        pgmode = pgmode ^ 1
    elif filtertype == "classicfamiliar":
        classicfamiliar = classicfamiliar ^ 1
    elif filtertype == "scifi":
        scifi = scifi ^ 1
    updateoptions()

def updateoptions():
    global settings_window
    global familiar_button
    global pg_button
    global scifi_button
    global pgmode
    global classicfamiliar
    global scifi
    if pgmode:
        pg_button.config(text="PG Mode: On")
    else:
        pg_button.config(text="PG Mode: Off")
    if classicfamiliar:
        familiar_button.config(text="Classic Familiars: On")
    else:
        familiar_button.config(text="Classic Familiars: Off")
    if scifi:
        scifi_button.config(text="No Scifi: On")
    else:
        scifi_button.config(text= "No Scifi: Off")

def update_font(*args):
    global selectedfont
    selectedfont = font_selection.get()
    resultLabel.config(font=(font_selection.get(), 24))
    descriptionLabel.config(font=(font_selection.get(), 15))
    headerLabel.config(font=(font_selection.get(), 12))
    optionLabel.config(font=(font_selection.get(), 12))
    copyLabel.config(font=(font_selection.get(), 12))
    editLabel.config(font=(font_selection.get(), 12))
    holderLabel.config(font=(font_selection.get(), 14))
    abilityButton.config(font=(font_selection.get(), 12))
    itemButton.config(font=(font_selection.get(), 12))
    traitButton.config(font=(font_selection.get(), 12))
    skillButton.config(font=(font_selection.get(), 12))
    familiarButton.config(font=(font_selection.get(), 12))
    randomButton.config(font=(font_selection.get(), 12))
    bronzeButton.config(font=(font_selection.get(), 12))
    silverButton.config(font=(font_selection.get(), 12))
    goldButton.config(font=(font_selection.get(), 12))
    platButton.config(font=(font_selection.get(), 12))
    diaButton.config(font=(font_selection.get(), 12))
    legendButton.config(font=(font_selection.get(), 12))
    mythButton.config(font=(font_selection.get(), 12))
    divineButton.config(font=(font_selection.get(), 12))
    return

def open_text():
    global activemode
    filename = activemode
    if filename == 'random':
        filename = ['ability.txt','item.txt','familiar.txt','trait.txt', 'skill.txt']
        filename = random.choice(filename)
    else:
        filename += '.txt'
    filename = os.path.join("gachafiles", filename)
    os.startfile(filename)

def open_patreon():
    webbrowser.open('www.patreon.com/BronzDeck')

root = Tk()
root.geometry("1024x668")
root.title('Chaos Gacha')
root.configure(background='#1f1f1f',highlightbackground="#646464",highlightthickness=3)
original_stdout = sys.stdout

font_selection = StringVar()
selectedfont = 'Courier'
v = IntVar()
resultLabel = Label(root, text="Result will appear here", pady=30, bg='#1f1f1f', fg='#FFF', font=(selectedfont, 24), wraplength=800)
resultLabel.place(x=512,y=60,in_=root, anchor="center")

descriptionLabel = Label(root, text="Description will appear here", pady=30, bg='#1f1f1f', fg='#FFF', font=(selectedfont, 15), wraplength=800)
descriptionLabel.place(x=512,y=120,in_=root, anchor="n")

headerLabel = Label(root, pady=0, bg='#1f1f1f', fg='#FFF', font=(selectedfont, 20), wraplength=800)
headerLabel.place(x=512,y=90,in_=root, anchor="n")

optionLabel = Label(root, text="Options", pady=30, bg='#1f1f1f', fg='#FFF', font=(selectedfont, 12), wraplength=800)
optionLabel.place(x=16,y=100,in_=root, anchor="w")

optionimage = PhotoImage(file="images/option.png")
setting_button = Button(root, image=optionimage, command=lambda:open_settings(), borderwidth=0, highlightthickness=0,activebackground='#1f1f1f',)
setting_button.place(x=20,y=20,in_=root)

editLabel = Label(root, text="Edit", pady=30, bg='#1f1f1f', fg='#FFF', font=(selectedfont, 12), wraplength=800)
editLabel.place(x=28,y=210,in_=root, anchor="w")

editimage = PhotoImage(file="images/edit.png")
edit_button = Button(root, image=editimage, command=lambda:open_text(), borderwidth=0, highlightthickness=0,activebackground='#1f1f1f')
edit_button.place(x=20,y=130,in_=root)

copyimage = PhotoImage(file="images/copy.png")
copyButton = Button(root, image=copyimage, command=lambda:copy_description(), borderwidth=0, highlightthickness=0,activebackground='#1f1f1f')
copyButton.place(x=25,y=240,in_=root)

copyLabel = Label(root, text="Copy", bg='#1f1f1f', fg='#FFF', font=(selectedfont, 12), wraplength=800)
copyLabel.place(x=32,y=320,in_=root, anchor="w")

patreonimage = PhotoImage(file="images/patreon.png")
patreonButton = Button(root, image=patreonimage, command=lambda:open_patreon(), borderwidth=0, highlightthickness=0,activebackground='#1f1f1f')
patreonButton.place(x=940,y=20,in_=root)

holderimage = PhotoImage(file="images/holder.png")
holder = Label(root, image=holderimage,borderwidth=0, highlightthickness=0)
holder.place(x=6,y=350,in_=root)

holderLabel = Label(root, text="Categories", bg='#212121', fg='#FFF', font=(selectedfont, 14))
holderLabel.place(x=116,y=375,in_=root, anchor="center")

buttonimage = PhotoImage(file="images/button.png")

abilityButton = Button(root, image=buttonimage, text='Abilities', compound="center", command=lambda:select_mode("ability"), background='#111', fg='#FFF', font=selectedfont, borderwidth=0)
abilityButton.place(x=23,y=400,in_=root)

itemButton = Button(root, image=buttonimage, text='Items', compound="center", command=lambda:select_mode("item"), background='#111', fg='#FFF', font=selectedfont, borderwidth=0)
itemButton.place(x=23,y=440,in_=root)

traitButton = Button(root, image=buttonimage, text='Traits', compound="center", command=lambda:select_mode("trait"), background='#111', fg='#FFF', font=selectedfont, borderwidth=0)
traitButton.place(x=23,y=480,in_=root)

skillButton = Button(root, image=buttonimage, text='Skills', compound="center", command=lambda:select_mode("skill"), background='#111', fg='#FFF', font=selectedfont, borderwidth=0)
skillButton.place(x=23,y=520,in_=root)

familiarButton = Button(root, image=buttonimage, text='Familiars', compound="center", command=lambda:select_mode("familiar"), background='#111', fg='#FFF', font=selectedfont, borderwidth=0)
familiarButton.place(x=23,y=560,in_=root)

randomButton = Button(root, image=buttonimage, text='Random', compound="center", command=lambda:select_mode("random"), background='#111', fg='#FFF', font=selectedfont, borderwidth=0)
randomButton.place(x=23,y=600,in_=root)

presets = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Legendary", "Mythical", "Divine"]
presetmin = [0.1, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]
presetavg = [1.3, 2.3, 3.3, 4.3, 5.3, 6.3, 7.3, 8.3]
presetmax = [3.3, 4.3, 5.3, 6.3, 7.3, 8.3, 9.3, 10.0]

presetimage = PhotoImage(file="images/holder.png")
holder2 = Label(root, image=holderimage,borderwidth=0, highlightthickness=0)
holder2.place(x=792,y=350,in_=root)

holderLabel = Label(root, text="Presets", bg='#212121', fg='#FFF', font=(selectedfont, 14))
holderLabel.place(x=902,y=375,in_=root, anchor="center")

bronzeImage = PhotoImage(file="images/bronze.png")
bronzeButton = Button(root, image=bronzeImage, text='Bronze', compound="center", command=lambda:select_preset(0), bg='#212121', font=(selectedfont, 11), borderwidth=0, activebackground='#1f1f1f')
bronzeButton.place(x=799,y=410,in_=root)

silverImage = PhotoImage(file="images/silver.png")
silverButton = Button(root, image=silverImage, text='Silver', compound="center", command=lambda:select_preset(1), bg='#212121', font=(selectedfont, 11), borderwidth=0, activebackground='#1f1f1f')
silverButton.place(x=905,y=410,in_=root)

goldImage = PhotoImage(file="images/gold.png")
goldButton = Button(root, image=goldImage, text='Gold', compound="center", command=lambda:select_preset(2), bg='#212121', font=(selectedfont, 11), borderwidth=0, activebackground='#1f1f1f')
goldButton.place(x=799,y=460,in_=root)

platImage = PhotoImage(file="images/platinum.png")
platButton = Button(root, image=platImage, text='Platinum', compound="center", command=lambda:select_preset(3), bg='#212121', font=(selectedfont, 11), borderwidth=0, activebackground='#1f1f1f')
platButton.place(x=905,y=460,in_=root)

diaImage = PhotoImage(file="images/diamond.png")
diaButton = Button(root, image=diaImage, text='Diamond', compound="center", command=lambda:select_preset(4), bg='#212121', font=(selectedfont, 11), borderwidth=0, activebackground='#1f1f1f')
diaButton.place(x=799,y=510,in_=root)

legendImage = PhotoImage(file="images/legendary.png")
legendButton = Button(root, image=legendImage, text='Legendary', compound="center", command=lambda:select_preset(5), bg='#212121', font=(selectedfont, 11), borderwidth=0, activebackground='#1f1f1f')
legendButton.place(x=905,y=510,in_=root)

mythImage = PhotoImage(file="images/mythical.png")
mythButton = Button(root, image=mythImage, text='Mythical', compound="center", command=lambda:select_preset(6), bg='#212121', font=(selectedfont, 11), borderwidth=0, activebackground='#1f1f1f')
mythButton.place(x=799,y=560,in_=root)

divineImage = PhotoImage(file="images/divine.png")
divineButton = Button(root, image=divineImage, text='Divine', compound="center", command=lambda:select_preset(7), bg='#212121', font=(selectedfont, 11), borderwidth=0, activebackground='#1f1f1f')
divineButton.place(x=905,y=560,in_=root)

selectedLabel = Label(root, text="Current: Bronze", bg='#212121', fg='#FFF', font=(selectedfont, 12))
selectedLabel.place(x=800,y=610,in_=root)

bottomImage = PhotoImage(file="images/downborder.png")
bottom = Label(root, image=bottomImage,borderwidth=0, highlightthickness=0)
bottom.place(x=512,y=632,in_=root, anchor="center")

rollButton1 = Button(root, text='Roll', width=12, command=lambda:prepare_gacha(), font=(selectedfont, 30), background='#111', fg='#FFF')
rollButton1.place(x=512,y=500,in_=root, anchor="center")

w = Spinbox(root, from_=0.0, to=10.0, format="%.1f",increment=0.1, width=4, relief="sunken", repeatdelay=500, repeatinterval=100,font=(selectedfont, 12), bg="#212121", fg="#111", state="readonly")
min = Spinbox(root, from_=0.0, to=10.0, format="%.1f",increment=0.1, width=4, relief="sunken", repeatdelay=500, repeatinterval=100,font=(selectedfont, 12), bg="#212121", fg="#111", state="readonly")
max = Spinbox(root, from_=0.0, to=10.0, format="%.1f",increment=0.1, width=4, relief="sunken", repeatdelay=500, repeatinterval=100,font=(selectedfont, 12), bg="#212121", fg="#111", state="readonly")
label1 = Label(root, text="Average: ", background='#212121', fg='#FFF', font=18)
label1.place(x=440, y=620, in_=root)
w.place(x=520, y=620, in_=root)
label2 = Label(root, text="Minimum: ", background='#212121', fg='#FFF', font=18)
label2.place(x=290, y=620, in_=root)
min.place(x=370, y=620, in_=root)
label3 = Label(root, text="Maximum: ", background='#212121', fg='#FFF', font=18)
label3.place(x=590, y=620, in_=root)
max.place(x=670, y=620, in_=root)
w.delete(0,"end")
w.insert(0,1.3)
min.delete(0,"end")
min.insert(0,0.0)
max.delete(0,"end")
max.insert(0,4.3)
select_mode("ability")
select_preset(0)
logs_enabled = False
settings_window = False

mainloop()
