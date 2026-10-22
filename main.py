"""SomaiyaSat Downlink Planner - tkinter window + SQLite + website.
Run:  python main.py      (standard Python only; on Linux install python3-tk)"""

import random
import tkinter as tk
from tkinter import ttk, messagebox

import website
from database import Database
from models import MODES, PacketError


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SomaiyaSat Downlink Planner")
        self.geometry("760x560")
        self.db = Database()

        tk.Label(self, text="SomaiyaSat Downlink Planner", font=("Arial", 18, "bold")).pack(pady=8)
        self.signal = tk.Label(self, text="Signal: run a pass to measure it", font=("Arial", 12))
        self.signal.pack()

        form = tk.Frame(self)
        form.pack(pady=10)
        self.mode = tk.StringVar(value="TT&C")
        self.size = tk.StringVar(value="200")
        self.urgency = tk.StringVar(value="3")
        tk.Label(form, text="Mode").grid(row=0, column=0)
        ttk.Combobox(form, textvariable=self.mode, values=list(MODES), width=8, state="readonly").grid(row=1, column=0, padx=5)
        tk.Label(form, text="Size (bytes)").grid(row=0, column=1)
        tk.Entry(form, textvariable=self.size, width=10).grid(row=1, column=1, padx=5)
        tk.Label(form, text="Urgency (1-5)").grid(row=0, column=2)
        tk.Spinbox(form, from_=1, to=5, textvariable=self.urgency, width=5).grid(row=1, column=2, padx=5)
        tk.Button(form, text="Add Packet", command=self.add_packet).grid(row=1, column=3, padx=8)
        tk.Button(form, text="Random 6", command=self.add_random).grid(row=1, column=4)

        columns = ("id", "mode", "size", "urgency", "status", "reason")
        self.table = ttk.Treeview(self, columns=columns, show="headings", height=12)
        for name in columns:
            self.table.heading(name, text=name.upper())
            self.table.column(name, width=240 if name == "reason" else 80, anchor="center")
        self.table.tag_configure("SENT", background="#bbf7d0")
        self.table.tag_configure("DEFERRED", background="#fed7aa")
        self.table.pack(padx=10, fill="both", expand=True)

        buttons = tk.Frame(self)
        buttons.pack(pady=8)
        tk.Button(buttons, text="Run Ground Pass", bg="#38bdf8", command=self.run_pass).pack(side="left", padx=5)
        tk.Button(buttons, text="Build Website", bg="#86efac", command=self.build_website).pack(side="left", padx=5)
        tk.Button(buttons, text="Clear All", command=self.clear).pack(side="left", padx=5)
        self.message = tk.Label(self, text="Add packets, then run a ground pass.")
        self.message.pack(pady=4)
        self.refresh()

    def refresh(self):
        self.table.delete(*self.table.get_children())
        for row in self.db.packets():
            self.table.insert("", "end", values=row, tags=(row[4],))

    def add_packet(self):
        try:                                                       # exception handling
            packet = MODES[self.mode.get()](int(self.size.get()), int(self.urgency.get()))
            self.db.add(packet.mode, packet.size, packet.urgency)
        except PacketError as error:
            messagebox.showerror("Wrong value", str(error))
        except ValueError:
            messagebox.showerror("Wrong value", "Enter whole numbers only")
        self.refresh()

    def add_random(self):
        for _ in range(6):
            self.db.add(random.choice(list(MODES)), random.randint(100, 1500), random.randint(1, 5))
        self.refresh()

    def run_pass(self, window=60):
        link = random.randint(20, 100)                                    # today's signal
        waiting = list(filter(lambda r: r[4] != "SENT", self.db.packets()))
        packets = [(r[0], MODES[r[1]](r[2], r[3])) for r in waiting]
        if not packets:
            messagebox.showinfo("Nothing to send", "There are no waiting packets.")
            return
        packets.sort(key=lambda item: item[1].priority(), reverse=True)   # polymorphism
        left, sent = window, 0
        for pid, packet in packets:
            seconds = packet.tx_time(link)
            if link < packet.min_link():
                self.db.update(pid, "DEFERRED", f"signal {link}% is below the needed {packet.min_link()}%")
            elif seconds > left:
                self.db.update(pid, "DEFERRED", f"needs {seconds}s but only {left:.0f}s left")
            else:
                left -= seconds
                sent += 1
                self.db.update(pid, "SENT", f"sent in {seconds}s")
        self.db.add_pass(link, sent, len(packets) - sent, round(left))
        colour = "green" if link >= 60 else "orange" if link >= 35 else "red"
        self.signal.config(text=f"Signal: {link}%", fg=colour)
        self.message.config(text=f"Pass done: {sent} sent, {len(packets) - sent} deferred, {left:.0f}s left")
        self.refresh()

    def build_website(self):
        path = website.build(self.db)
        self.message.config(text="Website saved and opened: " + path)

    def clear(self):
        if messagebox.askyesno("Clear", "Delete all packets and history?"):
            self.db.clear()
            self.refresh()


if __name__ == "__main__":
    App().mainloop()
