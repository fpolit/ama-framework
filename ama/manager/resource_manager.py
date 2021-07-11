#!/usr/bin/env python3
#
# Script to report allocated resource by a process
#
# Status:
#
# Maintainer: glozanoa <glozanoa@uni.pe>

from tabulate import tabulate
from typing import List
import psutil
import os

class ResourceManager:
    
    @staticmethod
    def allocated_resource(pid_processes:List[int]):
        processes = [psutil.Process(pid) for pid in pid_processes]

        allocate = {
            'global': {'CPU':0, 'MEMORY':0, 'THREADS':0},
            'process': {}
        }

        for process in processes:
            process_allocate = process.as_dict(attrs=['pid',
                                                    'username', 
                                                    'status',
                                                    'num_threads',
                                                    'cpu_percent',
                                                    'memory_percent',
                                                    'name'])
            allocate['process'][process.pid] = process_allocate
            
            allocate['global']['CPU'] += process_allocate['cpu_percent']
            allocate['global']['MEMORY'] += process_allocate['memory_percent']
            allocate['global']['THREADS'] += process_allocate['num_threads']
        
        return allocate

    @staticmethod
    def report(pid_processes:List[int], 
                columns:List[str] = ['pid',
                                    'username', 
                                    'status',
                                    'num_threads',
                                    'cpu_percent',
                                    'memory_percent',
                                    'name'], 
                report_temp:bool=True):
        allocated = ResourceManager.allocated_resource(pid_processes)

        width = os.get_terminal_size().columns
        medium_width = width//2
        line = "-"*width

        report_msg = f"{line}"

        temps = psutil.sensors_temperatures()
        if temps and report_temp:
            report_msg += f"\n{'Allocate Resource':<{medium_width}}{'Temperature':<{medium_width}}"

            temps = temps['coretemp']
            pkg = temps[0]
            report_msg += f"\n{'':<{medium_width}}{f'HIGH: {pkg.high} CRITICAL: {pkg.critical}':<{medium_width}}"

            temps = temps[1:]
            global_resource = list(allocated['global'].items())
            rows = max(len(global_resource), len(temps))

            if len(temps) < rows:
                temps += [None] * (rows - len(temps))
            else:
                global_resource += [(None, None)*(rows - len(global_resource))]

            for (resource, percent), temp in zip(global_resource, temps):
                if temp:
                    if resource or percent:
                        report_msg += f"\n{f'{resource:<8}: {percent}':<{medium_width}}{f'{temp.label}: {temp.current}':<{medium_width}}"
                    else:
                        report_msg += f"\n{'':<{medium_width}}{f'{temp.label}: {temp.current}':<{medium_width}}"
                else:
                    if resource or percent:
                        report_msg += f"\n{f'{resource:<8}: {percent}':<{medium_width}}{'':<{medium_width}}"
                    else:
                        report_msg += None
        else:
            report_msg += f"\n{'Allocate Resource':<{medium_width}}"
            for resource, percent in allocated['global'].items():
                report_msg += f"\n{f'{resource:<8}: {percent}':<{medium_width}}"

        report_msg += f"\n{line}"

        process_table = []
        for process in allocated['process'].values():
            row = []
            for column in columns:
                row.append(process[column])
            process_table.append(row)

        report_msg += tabulate(process_table, headers=columns)

        return report_msg
