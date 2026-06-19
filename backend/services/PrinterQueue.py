import asyncio
from dataclasses import dataclass
from typing import Any

from fastapi import Request
from models import TaskRecord
from services.printer import PrinterService


@dataclass
class PrintJob:
    type: str
    team_name: str
    data: Any

class PrinterQueue:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.printer: PrinterService = PrinterService("192.168.1.99")

    async def print_task(self, team_name: str, task: TaskRecord):
        await self.queue.put(PrintJob(type="new_task", team_name=team_name, data=task))
    
    async def print_submission(self, team_name: str, task: TaskRecord):
        await self.queue.put(PrintJob(type="submission", team_name=team_name, data=task))
        
    async def print_coins(self, team_name: str, coin_name: str):
        await self.queue.put(PrintJob(type="coins", team_name=team_name, data=coin_name))

    def _do_print(self, job: PrintJob):
        if job.type == "new_task":
            self.printer.print_task(job.team_name, job.data)
        elif job.type == "submission":
            self.printer.print_submission(job.team_name, job.data)
        elif job.type == "coins":
            self.printer.print_coins(job.team_name, job.data)
        else:
            print(f"Unknown print job type: {job.type}")
            
    async def worker(self):
        """TODO: Start deze als asyncio background task bij app startup."""
        while True:
            job = await self.queue.get()
            try:
                self._do_print(job)
            except Exception as e:
                print(f"Error processing print job: {e}")
            finally:
                self.queue.task_done()


def get_printer_Queue(request: Request) -> PrinterQueue:
    return request.app.state.printerQueue
   