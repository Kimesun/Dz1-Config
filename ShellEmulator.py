import os
import tarfile
import datetime
import sys

class ShellEmulator:
    def __init__(self, hostname, fs_archive, startup_script):
        self.hostname = hostname
        self.fs_archive = fs_archive
        self.startup_script = startup_script
        self.current_dir = '/'
        self.fs = {}

    def load_filesystem(self):
        with tarfile.open(self.fs_archive, 'r') as tar:
            tar.extractall('/tmp/virtual_fs')
        self.fs_root = '/tmp/virtual_fs'

    def run_startup_script(self):
        with open(self.startup_script, 'r') as script:
            commands = script.readlines()
        for command in commands:
            self.execute_command(command.strip())

    def execute_command(self, command):
        parts = command.split()
        if not parts:
            return
        cmd = parts[0]
        args = parts[1:]

        if cmd == 'ls':
            self.ls(args)
        elif cmd == 'cd':
            self.cd(args)
        elif cmd == 'exit':
            sys.exit(0)
        elif cmd == 'date':
            self.date()
        elif cmd == 'touch':
            self.touch(args)
        else:
            print(f"Unknown command: {cmd}")

    def ls(self, args):
        path = self.resolve_path(args[0] if args else self.current_dir)
        if os.path.isdir(path):
            print("\n".join(os.listdir(path)))
        else:
            print(f"{path}: No such directory")

    def cd(self, args):
        if not args:
            return
        path = self.resolve_path(args[0])
        if os.path.isdir(path):
            if args[0] == '/':
                self.current_dir = '/'
            else:
                self.current_dir = path
        else:
            print(f"{path}: No such directory")

    def date(self):
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def touch(self, args):
        if not args:
            return
        path = self.resolve_path(args[0])
        with open(path, 'a'):
            os.utime(path, None)

    def resolve_path(self, path):
        if path == '/':
            return self.fs_root
        if path.startswith('/'):
            return os.path.join(self.fs_root, path.lstrip('/'))
        return os.path.join(self.fs_root, self.current_dir.lstrip('/'), path)

    def prompt(self):
        return f"{self.hostname}:{self.current_dir}$ "

    def run(self):
        self.load_filesystem()
        self.run_startup_script()
        while True:
            command = input(self.prompt())
            self.execute_command(command)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: shell_emulator.py <hostname> <fs_archive> <startup_script>")
        sys.exit(1)

    hostname = sys.argv[1]
    fs_archive = sys.argv[2]
    startup_script = sys.argv[3]

    emulator = ShellEmulator(hostname, fs_archive, startup_script)
    emulator.run()
