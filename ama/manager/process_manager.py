#!/usr/bin/env python3
#
# Script to manage submitted process
#
# Status:
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import sys

import os
import logging
from pathlib import Path
from typing import List
import time
from queue import Queue
#from contextlib import redirect_stdout

from ama.utils.redirect import RedirectOutput

from ama.utils.logger import Logger
from .process import Process, ProcessStatus


class ProcessManager:
    SUBMITTED_ATTACKS = 0

    def __init__(self,
                 logfile:str = None,
                 loglevel = logging.WARNING,
                 logformat:str = '[%(asctime)s] %(name)s - %(levelname)s - %(message)s'):

        self.pending = Queue()
        self.processing = [] # [CrackingProcess, ...]
        self.completed = [] # [CrackingProcess, ...]
        self.logger = None
        if logfile:
            self.logger = Logger(__name__, logfile=logfile, level=loglevel,
                                 logformat=logformat)
            self.logger.add_handler(handler_type=logging.FileHandler)
            self.logger.info("Init logger of ProcessManager class")

    def submit(self, group=None, target=None, name=None, args=(), kwargs={}, depends:List[int] = [],
               output:Path = None):
        #import pdb; pdb.set_trace()
        ProcessManager.SUBMITTED_ATTACKS += 1
        process_id = ProcessManager.SUBMITTED_ATTACKS

        if output is None:
            output = "ama-%j.out"

        # If %j was found (increment index to avoid overwrite generated files),
        # otherwise  simply overwirte (if exists) file
        if output.find("%j") != -1:
            output_path = output.replace('%j', str(process_id))
            while os.path.exists(output_path):
                ProcessManager.SUBMITTED_ATTACKS += 1
                process_id = ProcessManager.SUBMITTED_ATTACKS
                output_path = output.replace('%j', str(process_id))

            output = output_path

        name = name.replace('%j', str(process_id))


        if self.logger:
            self.logger.info(f"Creating process {process_id}: target={target}, name={name}, args={args}, kwargs={kwargs}, depends={depends}, output={output}")

        dependency_process = []
        all_found = True #True if all dependencies was found and False otherwise
        for depend in depends:
            dependency_found = False
            for completed_process in self.completed:
                if completed_process.id_process == depend:
                    dependency_process.append(completed_process)
                    dependency_found = True
                    break

            if not dependency_found:
                # depend wasn't find in completed process (searching in pending process)
                for pending_process in self.pending.queue:
                    if pending_process.id_process == depend:
                        dependency_process.append(pending_process)
                        dependency_found = True
                        break

            # depend wasn't submitted, so depends_found = False and break loop
            if not dependency_found:
                all_found = False
                break

        if all_found: # all dependencies were found
            cp = Process(process_id, group, target, name, args, kwargs, dependency_process, output=output)
            print(f"[*] Submitting process: {process_id}")
            self.pending.put(cp)
            if self.logger:
                self.logger.info(f"Submitting process {process_id}")
        else:
            print("[-] Dependencies wasn't found.")
            print(f"[-] Avoid processing cracking process {process_id}")
            if self.logger:
                self.logger.error(f"Not all dependencies were found for {process_id} process: dependencies={depends}")
        return process_id


    def kill(self, kill_processes:List[int]):
        import pdb; pdb.set_trace()

        for kill_process_id in kill_processes:
            was_killed = False
            for process in self.processing:
                if kill_process_id == process.id_process:
                    print(f"[*] Kill process {process.id_process}")
                    process.kill()
                    process.close()
                    was_killed = True

            if not was_killed:
                print(f"Process {kill_process_id} was not found in PROCESSING processes")


    def process(self):
        while True:
            while not self.pending.empty():
                cracking_process = self.pending.get()
                output_file = cracking_process.output
                if output_file: # redirect output to output_file
                    with RedirectOutput(output_file):
                        #print(f"(process function)sys.stdout: {sys.stdout}")
                        cracking_process.start()
                else:
                    cracking_process.start()

                self.processing.append(cracking_process)
                if self.logger:
                    self.logger.info(f"Processing process {cracking_process.id_process}")


            # check if any cracking process were processed
            updated_processing = self.processing
            for cracking_process in self.processing:
                status = cracking_process.status()
                if status in [ProcessStatus.COMPLETED, ProcessStatus.FAILED]:
                    cracking_process.join()
                    if self.logger:
                        self.logger.info(f"Process {cracking_process.id_process} was completed")
                    updated_processing.remove(cracking_process)
                    self.completed.append(cracking_process)

            self.processing = updated_processing
            time.sleep(0.01)



    def report(self, show_completed_process:bool = True, show_pending_process:bool = True):
        status = {'processing': []}

        for processing_process in self.processing:
            status['processing'].append(processing_process.info())

        if show_completed_process:
            status['completed'] = []
            for completed_process in self.completed:
                status['completed'].append(completed_process.info())

        if show_pending_process:
            status['pending'] = []
            for pending_process in self.pending.queue:
                status['pending'].append(pending_process.info())

        return status
