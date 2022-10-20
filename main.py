import requests, json, sys, time
from os.path import exists, isdir, isfile, join
from os import walk
from random import uniform, shuffle
from colorama import Fore, init

init(autoreset=True)

if exists('token.txt'):
    print(f'{Fore.GREEN}+{Fore.RESET} Token found')
    with open('token.txt') as fd:
        token = fd.read().rstrip()
else:
    sys.exit(f'{Fore.RED}-{Fore.RESET} Token not found, please create a file named "token.txt" and put your discord token in there')

# creates a session, speeds up performance and re-uses connections
session = requests.Session()

def clear() -> None:
    """
    clear() -> nothing

    Clears the screen, thats it

    :returns None: Nothing
    """

    print('\033c', end='')

def change(status_msg: str) -> bool:
    """
    change(new status message) -> status

    Changes the status of the user

    :param status_msg str: new status message
    :returns bool: True if no errors occurred, False if otherwise
    """

    body = json.dumps({
        "custom_status": {
            "text": status_msg
        }
    })

    try:
        req = session.patch(
            'https://discordapp.com/api/v9/users/@me/settings',
            headers={
                "Authorization": token, 
                "Content-Type": "application/json"
            },
            data=body
        )

        return req.status_code == 200
    except Exception:
        return False

def parse(arg: str) -> list:
    """
    parse(file, lines or directory) -> lines

    Parses all lines from the command line

    :param arg str: File, folder or single string
    :returns list: List of lines
    """

    lines = []
    if exists(arg):
        if isdir(arg):
            print(f'{Fore.GREEN}{Fore.GREEN}+{Fore.RESET}{Fore.RESET} Parsing directory: {arg}')

            for root, _, files in walk(arg):
                for file in files:
                    fpath = join(root, file)

                    print(f'  {Fore.GREEN}+{Fore.RESET} Parsing file: {file}')
                    with open(fpath) as fd:
                        [lines.append(line.rstrip())
                         for line in fd.readlines()]
        
        elif isfile(arg):
            print(f'{Fore.GREEN}+{Fore.RESET} Parsing file: {arg}')
            with open(arg) as fd:
                [lines.append(line.rstrip())
                 for line in fd.readlines()]
    else:
        print(f'{Fore.GREEN}+{Fore.RESET} Parsing lines')
        [lines.append(x)
         for x in arg.split('|')]
    
    return lines

if __name__ == '__main__':
    clear()

    args = sys.argv[1:]
    running = True

    shuffle_lines = False
    if '--shuffle' in args or '--s' in args:
        shuffle_lines = True

    # parse arguments
    lines = []
    for arg in args:
        if not arg.startswith('--'): # skips arguments
            lines += parse(arg)
    
    print(f'{Fore.GREEN}+{Fore.RESET} Loaded {str(len(lines))} lines.')
    if shuffle_lines:
        shuffle(lines)
        print(f'{Fore.GREEN}+{Fore.RESET} Shuffle mode enabled')

    print('')
    while running:
        if shuffle_lines:
            shuffle(lines)

        for line in lines:
            try:
                status = change(line)

                if status:
                    print(f'{Fore.GREEN}+{Fore.RESET} Status changed: {line}')

                else:
                    print(f'{Fore.RED}-{Fore.RESET} Failed to change status to: {line}')

                time.sleep(uniform(4, 8))

            except KeyboardInterrupt:
                running = False; break
            
            except Exception as e:
                print(f'{Fore.RED}-{Fore.RESET} Exception occurred: {str(e).rstrip()}')
                running = False; break
    
    print('')