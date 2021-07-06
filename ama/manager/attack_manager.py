#!/usr/bin/env python3
#
# Script to manage attack process
#
# Status:
#
# Maintainer: glozanoa <glozanoa@uni.pe>

from queue import Queue


from .cracking_process import CrackingProcess, ProcessStatus


class AttackManager:
    SUBMITTED_ATTACKS = 0

    def __init__(self):
        self.pending = Queue()
        self.processing = [] # [CrackingProcess, ...]
        self.completed = [] # [CrackingProcess, ...]

    def submit(self, group=None, target=None, name=None, args=(), kwargs={}, depends:List[int] = []):
        AttackManager.SUBMITTED_ATTACKS += 1
        process_id = AttackManager.SUBMITTED_ATTACKS
        print("[*] Submitting cracking process: {process_id}")

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

        cp = CrackingProcess(process_id, group, target, name, args, kwargs, dependency_process)
        if all_found: # all dependencies were found
            self.pending.put(cp)
        else:
            print("[-] Dependencies wasn't found.")
            print("[-] Avoid processing cracking process {process_id}")


    def process(self):
        while True:
            while not self.pending.empty():
                cracking_process = self.pending.get()
                cracking_process.start()
                self.processing.append(cracking_process)


            # check if any cracking process were processed
            updated_processing = self.processing
            for cracking_process in self.processing:
                if cracking_process.status() == ProcessStatus.COMPLETED:
                    cracking_process.join()
                    updated_processing.remove(cracking_process)
                    self.completed.append(cracking_process)

            self.processing = updated_processing


    def report(self, show_completed_process:bool = False, show_pending_process:bool = False):
        status = {'processing': []}

        for processing_process in self.processing:
            status['processing'].append(processing_process.info())

        if show_completed_process:
            status['completed'] = []
            for completed_process in self.completed:
                status['completed'].append(processing_process.info())

        if show_pending_process:
            status['pending'] = []
            for completed_process in self.pending.queue:
                status['pending'].append(processing_process.info())

        return status
