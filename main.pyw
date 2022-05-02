from tkinter import *
import os
from tkinter import messagebox

def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y - 40))

class Hauptfenster(Tk):

    def __init__(self):
        super().__init__()

        self.AUS = PhotoImage(file=os.path.join("Bilder/", "aus.png"))
        self.AUS_AKTIV = PhotoImage(file=os.path.join("Bilder/", "aus_aktiv.png"))
        self.ABBRECHEN = PhotoImage(file=os.path.join("Bilder/", "abbrechen.png"))
        self.ABBRECHEN_AKTIV = PhotoImage(file=os.path.join("Bilder/", "abbrechen_aktiv.png"))

        self.seconds = 10
        self.seconds_run = False
        self.abbruch = False

        self.geometry("400x550")
        self.resizable(0, 0)
        self.title("Shutdown")
        self.config(bg="#39AEA9")
        self.pack_propagate(0)
        #self.iconbitmap("Bilder/Logo.ico")

        self.info_lbl = Label(self, text="Den PC in", font="Arial 30", width=10, bg="#F9FFA4")
        self.info_lbl.pack(pady=10)

        self.sekunden_entry = Entry(self, relief='flat', width=5, font="Arial 30")
        self.sekunden_entry.pack()
        self.sekunden_entry.bind("<Return>", lambda e: self.run_shutdown(e))
        self.sekunden_entry.focus_set()

        self.sekunden_lbl = Label(self, text="Sekunden", font="Arial 30", width=10, bg="#F9FFA4")
        self.sekunden_lbl.pack(pady=10)

        self.aus_btn = Button(self, image=self.AUS, relief='flat', highlightthickness=0, bd=0, bg="#39AEA9", activebackground="#39AEA9", command=self.update_seconds)
        self.aus_btn.pack(ipadx=5, ipady=5, pady=30)
        self.aus_btn.bind("<Enter>", lambda e: self.change_image(e, widget=self.aus_btn, image=self.AUS_AKTIV))
        self.aus_btn.bind("<Leave>", lambda e: self.change_image(e, widget=self.aus_btn, image=self.AUS))

        self.shutdown_zeit = Label(self, text="-", font="Arial 30", width=5, bg="#F9FFA4")
        self.shutdown_zeit.pack()

        self.abbrechen_btn = Button(self, image=self.ABBRECHEN, relief='flat', highlightthickness=0, bd=0, bg="#39AEA9", activebackground="#39AEA9", command=self.abbrechen)
        self.abbrechen_btn.pack(ipadx=5, ipady=5, pady=30)
        self.abbrechen_btn.config(state="disabled")
        self.abbrechen_btn.bind("<Enter>", lambda e: self.change_image(e, widget=self.abbrechen_btn, image=self.ABBRECHEN_AKTIV))
        self.abbrechen_btn.bind("<Leave>", lambda e: self.change_image(e, widget=self.abbrechen_btn, image=self.ABBRECHEN))

    def run_shutdown(self, *event):
        if self.seconds_run != True:
            self.update_seconds()
        else:
            self.abbrechen()

    def abbrechen(self):
        self.abbruch = True
        self.abbrechen_btn.config(state="disabled")

    def change_image(self, *event, widget, image):
        widget.config(image=image)

    def ausschalten(self):
        os.system("shutdown /s /t 0")

    def update_seconds(self, *event):
        if self.seconds_run != True:
            if self.sekunden_entry.get() == "":
                messagebox.showerror("   Fehler", "Bitte eine ganze Zahl eingeben...", parent=self)
                return
            else:
                try:
                    self.seconds = int(self.sekunden_entry.get())
                except:
                    messagebox.showerror("   Fehler", "Bitte eine ganze Zahl eingeben...", parent=self)
                    return
                self.shutdown_zeit.config(text=self.seconds)
                self.seconds_run = True
                self.abbrechen_btn.config(state="normal")

            self.aus_btn.config(state="disabled")

        if self.seconds != 0 and self.abbruch != True:
            self.after(1000, self.update_seconds)
            self.seconds -= 1
            self.shutdown_zeit.config(text=self.seconds)
        elif self.seconds != 0 and self.abbruch == True:
            pass
        else:
            self.ausschalten()

        if self.abbruch == True:
            self.abbruch = False
            messagebox.showinfo("   Info", "Der Shutdown wurde abgebrochen...", parent=self)
            self.shutdown_zeit.config(text="-")
            self.aus_btn.config(state="normal")
            self.seconds_run = False
            return

window = Hauptfenster()
center(window)

window.mainloop()
