from escpos.printer import Network
from PIL import Image
from models import TaskRecord

class DummyPrinter:
    def text(self, text):
        print(text, end="")

    def cut(self):
        print("--- CUT ---")

    def set(self, **kwargs):
        pass

class PrinterService:
    def __init__(self, ip, port=9100):
        
        real_printer = False
        if real_printer:
            self.p = Network(ip, port=port)
        else:
            self.p = DummyPrinter()

        # init printer
        self.p.text("\x1b@")
        

    def print_task(self, team_name: str, task: TaskRecord, self_cutting: bool = True):

        # --- HEADER (team name groot) ---
        self.p.set(align="center", bold=True, double_height=True, double_width=True, underline=1)
        self.p.text(f"{team_name}\n")
        self.p.set(underline=0)
        self.p.text(f"opdracht {task.sequence_number}\n")
        self.p.set(normal_textsize=True)
        self.p.text(f"for {task.likes} likes\n")
        
        # reset style
        self.p.set(bold=False, normal_textsize=True, align="left")
        self.p.text(f"normale opdracht:\n")

        self.p.text(f"• locatie: {task.location_text} ({task.location_likes})\n")
        self.p.text(f"• pose: {task.pose_text} ({task.pose_likes})\n")
        self.p.text(f"• object: {task.object_text} ({task.object_likes})")

        if len(task.extras) == 0:
            if self_cutting:
                self.p.cut()
            return
        
        self.p.text(f"\nextra's({task.bonus_likes}):\n")
        for extra in task.extras:
            self.p.text(f"  •({extra['likes']}) {extra['text']}\n")

        if self_cutting:
            self.p.cut()
    
    def print_submission(self, team_name: str, task: TaskRecord):
        self.print_task(team_name, task, self_cutting=False)
        self.p.text(f"foto: {task.photo_url}")
        self.p.cut()
    
    def print_coins(self, team_name: str, coin_name: str):
        self.p.set(align="center", bold=True, double_height=True, double_width=True, underline=1)
        self.p.text(f"{team_name}\n")
        self.p.set(underline=0)
        self.p.text(f"{coin_name}\n")
        self.p.cut()