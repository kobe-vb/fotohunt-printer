from escpos.printer import Network
from PIL import Image
from task import Task, Element


class PrinterService:
    def __init__(self, ip, port=9100):
        self.p = Network(ip, port=port)

        # init printer
        self.p.text("\x1b@")
    
    def _print_list_item(self, element: Element):
        self.p.text(f"  •({element.likes}) {element.text}\n")

    def print_task(self, team_name, id, task):

        # --- HEADER (team name groot) ---
        self.p.set(align="center", bold=True, double_height=True, double_width=True, underline=1)
        self.p.text(f"{team_name}\n")
        self.p.set(underline=0)
        self.p.text(f"opdracht {id}\n")
        self.p.set(normal_textsize=True)
        self.p.text(f"for {task.likes} likes\n")
        
        # reset style
        self.p.set(bold=False, normal_textsize=True, align="left")
        self.p.text(f"normale opdracht:\n")

        self._print_list_item(task.location)
        self._print_list_item(task.pose)
        self._print_list_item(task.object)

        if len(task.extras) == 0:
            self.p.cut()
            return
        
        self.p.text(f"\nextra's({task.bonus_likes}):\n")
        for extra in task.extras:
            self._print_list_item(extra)

        self.p.cut()
        

if __name__ == "__main__":
    printer = PrinterService("192.168.1.99")
    
    printer.print_task("de winnneraars", 0, Task(Element("locatie", 5), Element("pose", 3), Element("object", 2), (Element("extra1", 1), Element("extra2", 4))))
    # printer.print_task("de super lange naam gedoe hoe werkt dit?", Task())