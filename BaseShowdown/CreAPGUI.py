import CreAP
import tkinter as tk
from tkinter import ttk
from sys import exit

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


class GUI:
    def __init__(self):
        self.moves = CreAP.moves_to_dict()
        self.abilities = CreAP.abilities_to_dict()
        self.names_to_moves = {}
        for key in self.moves.keys():
            self.names_to_moves[self.moves[key]["name"]] = key
        self.names_to_abilities = {}
        for key in self.abilities.keys():
            self.names_to_abilities[self.abilities[key]["name"]] = key
        self.curr = CreAP.Poke()
        self.root = tk.Tk()
        self.root.geometry("600x700")
        self.root.title("CreAP for base Showdown")
        self.label = tk.Label(self.root, text="CreAP by Moth", font=('Ink Free', 18))
        self.label.pack()
        self.label2 = tk.Label(self.root, text="Version 1.0", font=('Arial', 10))
        self.label2.pack()
        self.menubar = tk.Menu(self.root)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Close", command= lambda: exit())
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Reload Files", command=CreAP.refresh_files)
        self.menubar.add_cascade(menu=self.filemenu, label="Options")
        self.root.config(menu=self.menubar)

        self.buttonframe = tk.Frame(self.root)
        self.buttonframe.columnconfigure(0, weight=5)
        self.buttonframe.columnconfigure(1, weight=5)
        self.buttonframe.columnconfigure(2, weight=5)
        self.buttonframe.columnconfigure(3, weight=5)
        self.buttonframe.columnconfigure(4, weight=5)
        self.buttonframe.columnconfigure(5, weight=5)
        self.buttonframe.columnconfigure(6, weight=5)

        self.nameLabel = tk.Label(self.buttonframe, text="Name:", font=('Arial', 10))
        self.nameLabel.grid(row=0, column=0)
        self.nameEntry = tk.Entry(self.buttonframe, font=("Arial", 10), width=14)
        self.nameEntry.grid(row=0, column=1)
        self.nameEntry.bind("<KeyRelease>", self.update_name)

        self.typeLabel = tk.Label(self.buttonframe, text="Types:", font=('Arial', 10))
        self.typeLabel.grid(row=1, column=0)
        self.t1 = tk.StringVar()
        self.t2 = tk.StringVar()
        self.type1 = ttk.Combobox(self.buttonframe, textvariable=self.t1, width=10)
        self.type1['values'] = (
            "Normal", "Grass", "Fire", "Water", "Electric", "Psychic", "Ice", "Fighting", "Flying", "Poison", "Ground",
            "Rock", "Bug", "Dragon", "Ghost", "Dark", "Steel", "Fairy")
        self.type1.grid(row=1, column=1)
        self.type2 = ttk.Combobox(self.buttonframe, textvariable=self.t2, width=10)
        self.type2['values'] = (
            "", "Normal", "Grass", "Fire", "Water", "Electric", "Psychic", "Ice", "Fighting", "Flying", "Poison",
            "Ground",
            "Rock", "Bug", "Dragon", "Ghost", "Dark", "Steel", "Fairy")
        self.type2.grid(row=1, column=2)
        self.type1.bind('<<ComboboxSelected>>', self.update_types)
        self.type2.bind('<<ComboboxSelected>>', self.update_types)

        self.statsLabel = tk.Label(self.buttonframe, text="Stats:", font=("Arial", 10))
        self.statsLabel.grid(row=2, column=0)
        self.hpLabel = tk.Label(self.buttonframe, text="HP:", font=("Arial", 10))
        self.hpLabel.grid(row=2, column=1)
        self.hpspin = tk.Spinbox(self.buttonframe, from_=1, to=255, width=4, command=self.update_stats)
        self.hpspin.grid(row=2, column=2)
        self.hpspin.bind("<KeyRelease>", self.update_stats)
        self.atkLabel = tk.Label(self.buttonframe, text="Attack:", font=("Arial", 10))
        self.atkLabel.grid(row=2, column=3)
        self.atkspin = tk.Spinbox(self.buttonframe, from_=1, to=255, width=4, command=self.update_stats)
        self.atkspin.grid(row=2, column=4)
        self.atkspin.bind("<KeyRelease>", self.update_stats)
        self.defLabel = tk.Label(self.buttonframe, text="Defense:", font=("Arial", 10))
        self.defLabel.grid(row=2, column=5)
        self.defspin = tk.Spinbox(self.buttonframe, from_=1, to=255, width=4, command=self.update_stats)
        self.defspin.grid(row=2, column=6)
        self.defspin.bind("<KeyRelease>", self.update_stats)
        self.spaLabel = tk.Label(self.buttonframe, text="Special Attack:", font=("Arial", 10))
        self.spaLabel.grid(row=3, column=1)
        self.spaspin = tk.Spinbox(self.buttonframe, from_=1, to=255, width=4, command=self.update_stats)
        self.spaspin.grid(row=3, column=2)
        self.spaspin.bind("<KeyRelease>", self.update_stats)
        self.spdLabel = tk.Label(self.buttonframe, text="Special Defense:", font=("Arial", 10))
        self.spdLabel.grid(row=3, column=3)
        self.spdspin = tk.Spinbox(self.buttonframe, from_=1, to=255, width=4, command=self.update_stats)
        self.spdspin.grid(row=3, column=4)
        self.spdspin.bind("<KeyRelease>", self.update_stats)
        self.speLabel = tk.Label(self.buttonframe, text="Speed:", font=("Arial", 10))
        self.speLabel.grid(row=3, column=5)
        self.spespin = tk.Spinbox(self.buttonframe, from_=1, to=255, width=4, command=self.update_stats)
        self.spespin.grid(row=3, column=6)
        self.spespin.bind("<KeyRelease>", self.update_stats)

        self.abilityLabel = tk.Label(self.buttonframe, text="Abilities:", font=("Arial", 10))
        self.abilityLabel.grid(row=4, column=0)
        self.abilitylist = [self.abilities[key]["name"][1:-2] for key in self.abilities.keys()]
        # print(self.abilitylist)
        self.ab1 = tk.StringVar()
        self.ab2 = tk.StringVar()
        self.abH = tk.StringVar()
        self.ability1Label = tk.Label(self.buttonframe, text="Ability 1:", font=("Arial", 10))
        self.ability1Label.grid(row=4, column=1)
        self.ability1 = ttk.Combobox(self.buttonframe, textvariable=self.ab1, width=18)
        self.ability1.grid(row=4, column=2)
        self.ability1['values'] = tuple(self.abilitylist)
        self.ability1.current(0)
        self.ability1.bind('<KeyRelease>', self.check_ability_input)
        self.ability2Label = tk.Label(self.buttonframe, text="Ability 2:", font=("Arial", 10))
        self.ability2Label.grid(row=4, column=3)
        self.ability2 = ttk.Combobox(self.buttonframe, textvariable=self.ab2, width=18)
        self.ability2.grid(row=4, column=4)
        self.ability2['values'] = tuple(self.abilitylist)
        self.ability2.current(0)
        self.ability2.bind('<KeyRelease>', self.check_ability_input)
        self.abilityHLabel = tk.Label(self.buttonframe, text="Hidden Ability:", font=("Arial", 10))
        self.abilityHLabel.grid(row=5, column=1)
        self.abilityHidden = ttk.Combobox(self.buttonframe, textvariable=self.abH, width=18)
        self.abilityHidden.grid(row=5, column=2)
        self.abilityHidden['values'] = tuple(self.abilitylist)
        self.abilityHidden.current(0)
        self.abilityHidden.bind('<KeyRelease>', self.check_ability_input)
        self.ability1.bind('<<ComboboxSelected>>', self.update_abilities)
        self.ability2.bind('<<ComboboxSelected>>', self.update_abilities)
        self.abilityHidden.bind('<<ComboboxSelected>>', self.update_abilities)

        self.moveLabel = tk.Label(self.buttonframe, text="Moves:", font=("Arial", 10))
        self.moveLabel.grid(row=6, column=0)
        self.moveframe = ScrollableFrame(self.buttonframe)
        self.innerframe = tk.Frame(self.moveframe.scrollable_frame)
        self.innerframe.columnconfigure(0, weight=1)
        self.innerframe.columnconfigure(1, weight=1)
        self.innerframe.columnconfigure(2, weight=1)
        self.innerframe.pack(padx=10, fill="both")
        self.update_move_canvas()
        self.moveframe.grid(row=7, column=0, columnspan=7, sticky="EW")

        self.otherlabel = tk.Label(self.buttonframe, text="Other: ", font=("Arial", 10))
        self.otherlabel.grid(row=8, column=0)
        self.heightlabel = tk.Label(self.buttonframe, text="Height (M):", font=("Arial", 10))
        self.heightlabel.grid(row=9, column=1)
        self.heightEntry = tk.Entry(self.buttonframe, font=("Arial", 10), width=6)
        self.heightEntry.grid(row=9, column=2)
        self.heightEntry.bind("<KeyRelease>", self.update_other)
        self.weightlabel = tk.Label(self.buttonframe, text="Weight (KG):", font=("Arial", 10))
        self.weightlabel.grid(row=9, column=3)
        self.weightEntry = tk.Entry(self.buttonframe, font=("Arial", 10), width=6)
        self.weightEntry.grid(row=9, column=4)
        self.weightEntry.bind("<KeyRelease>", self.update_other)
        self.colorLabel = tk.Label(self.buttonframe, text="Color:", font=("Arial", 10))
        self.colorLabel.grid(row=9, column=5)
        self.color = tk.StringVar()
        self.colorBox = ttk.Combobox(self.buttonframe, textvariable=self.color, width=10)
        self.colorBox['values'] = (
            "Red", "Blue", "Yellow", "Green", "Black", "Brown", "Purple", "Gray", "White", "Pink")
        self.colorBox.bind('<<ComboboxSelected>>', self.update_other)
        self.colorBox.grid(row=9, column=6)
        self.colorBox.current(0)
        self.eggLabel = tk.Label(self.buttonframe, text="Egg Groups:", font=("Arial", 10))
        self.eggLabel.grid(row=10, column=1)
        self.egg1 = tk.StringVar()
        self.egg1Box = ttk.Combobox(self.buttonframe, textvariable=self.egg1, width=14)
        self.egg1Box['values'] = (
            "Monster", "Human-Like", "Water 1", "Water 3", "Bug", "Mineral", "Flying", "Amorphous", "Field", "Water 2",
            "Fairy", "Grass", "Dragon", "Undiscovered")
        self.egg1Box.bind('<<ComboboxSelected>>', self.update_other)
        self.egg1Box.grid(row=10, column=2)
        self.egg1Box.current(13)
        self.egg2 = tk.StringVar()
        self.egg2Box = ttk.Combobox(self.buttonframe, textvariable=self.egg2, width=14)
        self.egg2Box['values'] = (
            "",
            "Monster", "Human-Like", "Water 1", "Water 3", "Bug", "Mineral", "Flying", "Amorphous", "Field", "Water 2",
            "Fairy", "Grass", "Dragon")
        self.egg2Box.bind('<<ComboboxSelected>>', self.update_other)
        self.egg2Box.grid(row=10, column=3)
        self.egg2Box.current(0)

        self.createCode = tk.Button(self.buttonframe, text="Generate Code", command=self.create_code)
        self.createCode.grid(row=11, column=5, columnspan=2)
        self.code = tk.StringVar()
        self.codeBox = tk.Text(self.buttonframe, font=("Arial", 10))
        self.codeBox.grid(row=12, column=0, columnspan=7)
        self.codeBox.insert(tk.END, "Click on Generate Code to generate the code for this Fakemon.")
        self.codeBox.config(state='disabled')

        self.buttonframe.pack(fill="both")

    def start(self):
        self.update_move_canvas()
        self.root.mainloop()

    def update_name(self, event):
        self.curr.update_name(self.nameEntry.get())
        print(self.curr.name)
        print(self.curr.internalName)

    def update_types(self, event):
        self.curr.types = []
        self.curr.types.append(self.t1.get())
        if self.t2.get() != "":
            self.curr.types.append(self.t2.get())
        print(self.curr.types)

    def update_stats(self, event=None):
        self.curr.update_stats(int(self.hpspin.get()), int(self.atkspin.get()), int(self.defspin.get()),
                               int(self.spaspin.get()), int(self.spdspin.get()), int(self.spespin.get()))
        print(self.curr.baseStats)

    def update_abilities(self, event):
        self.curr.abilities = {}
        self.curr.abilities["0"] = self.ab1.get()
        if self.ab2.get() != "No Ability":
            self.curr.abilities["1"] = self.ab2.get()
        if self.abH.get() != "No Ability":
            self.curr.abilities["H"] = self.abH.get()
        print(self.curr.abilities)

    def update_move_canvas(self):
        for widget in self.innerframe.grid_slaves():
            widget.grid_remove()
        currrow = 0
        ttk.Label(self.innerframe, text="Level Up", width=20).grid(row=0, column=0, sticky="W")
        ttk.Label(self.innerframe, text="", width=20).grid(row=0, column=1, sticky="EW")
        ttk.Button(self.innerframe, text="Add Move", width=10, command=self.add_level_move).grid(row=0, column=2,
                                                                                                 sticky="E")
        currrow += 1
        for i in sorted(self.curr.learnset["levelUp"].keys()):
            for j in sorted(self.curr.learnset["levelUp"][i]):
                ttk.Label(self.innerframe, text=self.moves[j]["name"][1:-1], width=20).grid(row=currrow, column=0,
                                                                                            sticky="W")
                ttk.Label(self.innerframe, text="Level: " + str(i), width=60).grid(row=currrow, column=1, sticky="EW")
                ttk.Button(self.innerframe, text="x", width=1, command=lambda: self.remove_move(j, "levelUp", i)).grid(
                    row=currrow, column=2, sticky="E")
                currrow += 1
        ttk.Label(self.innerframe, text="TM, Tutor, or Egg", width=20).grid(row=currrow, column=0, sticky="W")
        ttk.Label(self.innerframe, text="", width=60).grid(row=currrow, column=1, sticky="EW")
        ttk.Button(self.innerframe, text="Add Move", width=10, command=self.add_other_move).grid(row=currrow, column=2,
                                                                                                 sticky="E")
        currrow += 1
        for a in sorted(self.curr.learnset["Tutor/TM"]):
            ttk.Label(self.innerframe, text=self.moves[a]["name"][1:-1], width=20).grid(row=currrow, column=0,
                                                                                        sticky="W")
            ttk.Label(self.innerframe, text="", width=60).grid(row=currrow, column=1, sticky="EW")
            ttk.Button(self.innerframe, text="x", width=1, command=lambda: self.remove_move(a, "Tutor/TM", None)).grid(
                row=currrow, column=2, sticky="E")
            currrow += 1
        for b in sorted(self.curr.learnset["Egg"].keys()):
            ttk.Label(self.innerframe, text=self.moves[b]["name"][1:-1], width=20).grid(row=currrow, column=0,
                                                                                        sticky="W")
            ttk.Label(self.innerframe, text="", width=60).grid(row=currrow, column=1, sticky="EW")
            ttk.Button(self.innerframe, text="x", width=1, command=lambda: self.remove_move(b, "Egg", None)).grid(
                row=currrow, column=2, sticky="E")
            currrow += 1
        # for i in self.curr.learnset["Event"].keys():
        #    ttk.Label(self.innerframe, text=self.moves[i]["name"][1:-1], width=20).grid(row=currrow, column=0, sticky="W")
        #    ttk.Label(self.innerframe, text="", width=60).grid(row=currrow, column=1, sticky="EW")
        #    ttk.Button(self.innerframe, text="x", width=1).grid(row=currrow, column=2, sticky="E")
        #    currrow += 1

    def remove_move(self, name: str, source: str, additional: int or None):
        if source == "levelUp":
            self.curr.learnset["levelUp"][additional].remove(name)
            if len(self.curr.learnset["levelUp"][additional]) == 0:
                del self.curr.learnset["levelUp"][additional]
        if source == "Tutor/TM":
            self.curr.learnset["Tutor/TM"].remove(name)
        if source == "Egg":
            del self.curr.learnset["Egg"][name]
        self.update_move_canvas()

    def add_level_move(self):
        def check_move_input(event):
            value = event.widget.get()

            if value == '':
                movebox['values'] = movelist
            else:
                data = []
                for item in movelist:
                    if item.lower().startswith(value.lower()):
                        data.append(item)

                movebox['values'] = data

        tempgui = tk.Tk()
        tempgui.geometry("300x100")
        tempgui.title("Add Level Up Move")
        grid = tk.Frame(tempgui)
        grid.pack(fill="both")
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        grid.columnconfigure(2, weight=1)
        grid.columnconfigure(3, weight=1)
        label1 = tk.Label(grid, text="Move: ")
        label1.grid(row=0, column=0)
        label2 = tk.Label(grid, text="Level: ")
        label2.grid(row=0, column=3)
        levnum = tk.IntVar(tempgui)
        levnum.set(1)
        print(levnum.get())
        level = tk.Spinbox(grid, from_=0, to=100, width=4, textvariable=levnum)
        level.grid(row=0, column=4)
        print(levnum.get())
        move = tk.StringVar()
        movebox = ttk.Combobox(grid, textvariable=move, width=20)
        movebox.grid(row=0, column=2)
        movelist = [self.moves[key]["name"][1:-1] for key in self.moves.keys()]
        movebox['values'] = movelist
        movebox.bind('<KeyRelease>', check_move_input)
        submit = tk.Button(grid, text="Add", command=lambda: [
            self.curr.add_move(self.names_to_moves["\"" + movebox.get() + "\""], "levelUp", int(level.get())),
            self.update_move_canvas(), tempgui.destroy()])
        submit.grid(row=1, column=0)
        tempgui.mainloop()

    def add_other_move(self):
        def check_move_input(event):
            value = event.widget.get()

            if value == '':
                movebox['values'] = movelist
            else:
                data = []
                for item in movelist:
                    if item.lower().startswith(value.lower()):
                        data.append(item)

                movebox['values'] = data

        tempgui = tk.Tk()
        tempgui.geometry("300x100")
        tempgui.title("Add Level Up Move")
        grid = tk.Frame(tempgui)
        grid.pack(fill="both")
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        label1 = tk.Label(grid, text="Move: ")
        label1.grid(row=0, column=0)
        move = tk.StringVar()
        movebox = ttk.Combobox(grid, textvariable=move, width=20)
        movebox.grid(row=0, column=2)
        movelist = [self.moves[key]["name"][1:-1] for key in self.moves.keys()]
        movebox['values'] = movelist
        movebox.bind('<KeyRelease>', check_move_input)
        submit = tk.Button(grid, text="Add", command=lambda: [
            self.curr.add_move(self.names_to_moves["\"" + movebox.get() + "\""], "Tutor/TM", None),
            self.update_move_canvas(), tempgui.destroy()])
        submit.grid(row=1, column=0)

    def check_ability_input(self, event):
        value = event.widget.get()

        if value == '':
            event.widget['values'] = self.abilitylist
        else:
            data = []
            for item in self.abilitylist:
                if item.lower().startswith(value.lower()):
                    data.append(item)

            event.widget['values'] = data

    def update_other(self, event):
        if self.heightEntry.get() != "":
            self.curr.heightm = int(self.heightEntry.get())
        if self.weightEntry.get() != "":
            self.curr.weightkg = int(self.weightEntry.get())
        self.curr.color = self.colorBox.get()
        self.curr.eggGroups = []
        self.curr.eggGroups.append(self.egg1Box.get())
        if self.egg2Box.get() != "":
            self.curr.eggGroups.append(self.egg2Box.get())
        print(self.curr.create_code())

    def create_code(self):
        c = ""
        c += self.curr.create_code() + "\n\n" + self.curr.create_move_code() + "\n"
        self.codeBox.config(state='normal')
        self.codeBox.delete("1.0", tk.END)
        self.codeBox.insert(tk.END, c)
        self.codeBox.config(state='disabled')


if __name__ == "__main__":
    gui = GUI()
    gui.start()
