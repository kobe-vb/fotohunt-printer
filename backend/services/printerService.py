import os
import random

from escpos.printer import Network
from PIL import Image
from models.models import TaskRecord
from models.task import TaskResponse
from services.DummyPrinter import DummyPrinter
from services.img import prepare_image


class PrinterService:
    def __init__(self, ip, port=9100):
        self.ip = ip
        self.port = port

        self.use_real_printer = os.getenv("USE_PRINTER", "false") == "true"
        print(f"Using real printer: {self.use_real_printer}")

    def _connect(self):
        """Open een verse connectie per print-job (zoals in test.py), i.p.v.
        1 langlevende socket te hergebruiken voor de hele event-duur."""
        if self.use_real_printer:
            p = Network(self.ip, port=self.port)
        else:
            p = DummyPrinter()

        # init printer
        p.text("\x1b@")
        return p

    def _write_task(self, p, team_name: str, task: TaskResponse):
        # --- HEADER (team name groot) ---
        p.set(align="center", bold=True, double_height=True, double_width=True, underline=1)
        p.text(f"{team_name}\n")
        p.set(underline=0)
        p.text(f"opdracht {task.sequence_number}\n")
        p.set(normal_textsize=True)
        p.text(f"for {task.likes} likes\n")
        if abs(task.multiplier - 1) > 0.0001:
            p.text(f"x{task.multiplier}\n")

        # reset style
        p.set(bold=False, normal_textsize=True, align="left")

        if task.special_task_text is not None:
            p.text(f"• {task.special_task_text} ({task.special_task_likes})\n")
        else:
            p.text(f"• locatie: {task.location_text} ({task.location_likes})\n")
            p.text(f"• pose: {task.pose_text} ({task.pose_likes})\n")
            p.text(f"• object: {task.object_text} ({task.object_likes})")

        if len(task.extras) == 0:
            return

        p.text(f"\nextra's({task.bonus_likes}):\n")
        for extra in task.extras:
            p.text(f"  •({extra.likes}) {extra.text}\n")

    def print_task(self, team_name: str, task: TaskResponse):
        p = self._connect()
        try:
            self._write_task(p, team_name, task)
            p.cut()
        finally:
            p.close()

    def print_submission(self, team_name: str, task: TaskResponse):
        p = self._connect()
        try:
            self._write_task(p, team_name, task)
            p.set(align="center")
            print(task.photo_url)
            p.image(prepare_image(task.photo_url))
            p.cut()
        finally:
            p.close()

    def print_coins(self, team_name: str, coin_name: str):
        p = self._connect()
        try:
            p.set(align="center", bold=True, double_height=True, double_width=True, underline=1)
            p.text(f"{team_name}\n")
            p.set(underline=0)
            p.text(f"{coin_name}\n")
            p.cut()
        finally:
            p.close()
            
    def print_streek(self, team_name: str):
        p = self._connect()
        try:
            p.set(align="center", bold=True, double_height=True, double_width=True, underline=1)
            p.text(f"{team_name}\n")
            p.set(underline=0)
            streek, likes = get_random_Streek()
            p.text(f"{streek}({likes})\n")
            p.cut()
        finally:
            p.close()
            
def get_random_Streek():
    streek = [
        ("3 fotos met bal", 10),
        ("4 fotos met iemand in de lucht", 14),
        ("3 fotos met iemand in de lucht", 10),
        ("2 fotos 1 iemand handstand", 5),
        ("3 fotos 1 iemand handstand", 7),
        ("2 fotos met een leiding", 4),
        ("5 fotos met een leiding", 20),
        ("", ),
        
    ]
    return random.choice(streek)