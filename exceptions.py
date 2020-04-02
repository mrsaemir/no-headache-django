class LinuxProgramNotInstalled(Exception):
    def __init__(self, program):
        self.program = program

    def __str__(self):
        return f"You need to install {self.program} first. \nRun: apt update && apt install {self.program}"



