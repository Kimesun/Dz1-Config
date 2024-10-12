import os
import tarfile
import datetime
import sys
import unittest
from ShellEmulator import ShellEmulator


class TestShellEmulator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.hostname = "test_host"
        cls.fs_archive = "test_fs.tar"
        cls.startup_script = "test_script.sh"
        # Create a tar file and a startup script for testing
        with tarfile.open(cls.fs_archive, "w") as tar:
            os.mkdir("virtual_fs")
            tar.add("virtual_fs")
        with open(cls.startup_script, "w") as f:
            f.write("ls\n")
            f.write("cd /\n")
            f.write("date\n")
            f.write("touch testfile\n")
            f.write("exit\n")

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.fs_archive)
        os.remove(cls.startup_script)
        os.rmdir("virtual_fs")

    def setUp(self):
        self.emulator = ShellEmulator(self.hostname, self.fs_archive, self.startup_script)
        self.emulator.load_filesystem()

    def test_ls(self):
        self.emulator.execute_command("ls")

    def test_cd(self):
        self.emulator.execute_command("cd /")
        self.assertEqual(self.emulator.resolve_path(self.emulator.current_dir), self.emulator.fs_root)

    def test_date(self):
        self.emulator.execute_command("date")

    def test_touch(self):
        self.emulator.execute_command("touch testfile")
        self.assertTrue(os.path.isfile(self.emulator.resolve_path("testfile")))

    # def test_run_startup_script(self):
    #     self.emulator.run_startup_script()


if __name__ == "__main__":
    unittest.main()
