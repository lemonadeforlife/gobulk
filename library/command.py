__all__ = ['custom_command', 'exclude_command', 'clear']
import os
import sys


def custom_command(com):
    if com.find(':') != -1:
        start, end, *ignore = com.split(':')
        if start == '':
            start_ep = None
        else:
            start_ep = int(start)
        if end == '':
            end_ep = None
        else:
            end_ep = int(end)
    else:
        try:
            start_ep = int(com)
            end_ep = int(com)
        except Exception:
            print(f'{com} is invalid')
            exit()
    return start_ep, end_ep


def exclude_command(com):
    exclude = []
    if com.find(',') != -1:
        for num in com.split(','):
            if num == '':
                continue
            elif num.find('-') != -1:
                num1, num2 = num.split('-')
                for n in range(int(num1), int(num2)+1):
                    exclude.append(n)
            else:
                try:
                    exclude.append(int(num))
                except Exception:
                    print(
                        f'Error::   Exclude Value: {num}\nWhich was ignored and continued')
    return sorted(set(exclude))


def clear():
    if sys.platform == 'linux' or sys.platform == 'darwin':
        os.system('clear')
    elif sys.platform == 'win32':
        os.system('cls')
