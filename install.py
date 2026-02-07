# Disclaimer: This installation script was partially generated with AI.
"""
✨ DOTFILES INSTALLER ✨
---------------------------------
"""

import os
import random
import shutil
import subprocess
import sys
import threading
import time


# --- 🎨 THEME & COLORS ---
class Style:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    # Bright Foreground
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

    ICONS = {
        "ok": "✅",
        "fail": "❌",
        "info": "ℹ️",
        "rocket": "🚀",
        "pkg": "📦",
        "link": "🔗",
        "shell": "🐚",
        "star": "🌟",
    }


# --- 🎬 ANIMATION ENGINE ---
class Spinner:
    """A fun loading spinner that runs in a separate thread."""

    def __init__(self, message="Processing...", color=Style.CYAN):
        self.message = message
        self.color = color
        self.stop_running = False
        self.thread = None
        self.frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def _animate(self):
        idx = 0
        while not self.stop_running:
            frame = self.frames[idx % len(self.frames)]
            sys.stdout.write(f"\r{self.color}{frame} {self.message}{Style.RESET}")
            sys.stdout.flush()
            time.sleep(0.08)
            idx += 1

    def start(self):
        self.stop_running = False
        self.thread = threading.Thread(target=self._animate)
        self.thread.start()

    def success(self, end_message="Done!"):
        self.stop_running = True
        # FIX: Check if thread exists before joining to prevent AttributeError
        if self.thread is not None and self.thread.is_alive():
            self.thread.join()
        sys.stdout.write(
            f"\r{Style.GREEN}{Style.ICONS['ok']} {end_message:<50}{Style.RESET}\n"
        )
        sys.stdout.flush()

    def fail(self, end_message="Failed!"):
        self.stop_running = True
        # FIX: Check if thread exists before joining
        if self.thread is not None and self.thread.is_alive():
            self.thread.join()
        sys.stdout.write(
            f"\r{Style.RED}{Style.ICONS['fail']} {end_message:<50}{Style.RESET}\n"
        )
        sys.stdout.flush()


def type_writer(text, speed=0.02, color=Style.WHITE):
    """Prints text one character at a time."""
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed + random.uniform(-0.01, 0.01))
    sys.stdout.write(Style.RESET + "\n")


def print_banner():
    """Prints a custom Austryx banner."""
    # Custom ASCII Art for "Austryx"
    banner = [
        "    _              _                    ",
        "   / \   _   _ ___| |_ _ __ _   ___  __ ",
        "  / _ \ | | | / __| __| '__| | | \ \/ / ",
        " / ___ \| |_| \__ \ |_| |  | |_| |>  <  ",
        "/_/   \_\__,_|___/\__|_|   \__, /_/\_\ ",
        "                           |___/        ",
    ]
    colors = [
        Style.RED,
        Style.YELLOW,
        Style.GREEN,
        Style.CYAN,
        Style.BLUE,
        Style.MAGENTA,
    ]

    print("\n")
    for line in banner:
        line_color = random.choice(colors)
        print(f"{line_color}{Style.BOLD}{line}{Style.RESET}")
    print(f"\n{Style.DIM}{' ' * 10}v2.0 • The Austryx Edition{Style.RESET}\n")
    time.sleep(0.5)


# --- 🛠️ UTILITIES ---


def run_cmd(command, shell=False, ignore_errors=False):
    """Runs a subprocess command silently."""
    try:
        subprocess.run(
            command,
            shell=shell,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        return ignore_errors


def check_installed(tool):
    return shutil.which(tool) is not None


# --- 🚀 TASKS ---


def task_install_packages():
    """Installs packages based on OS."""
    packages = ["git", "stow", "zsh", "curl"]
    missing = [p for p in packages if not check_installed(p)]

    if not missing:
        # We start and immediately success so the user sees the check happened
        s = Spinner(f"Checking dependencies...", Style.DIM)
        s.start()
        time.sleep(0.5)  # Fake work for visual flow
        s.success("All dependencies ready!")
        return

    s = Spinner(f"Installing missing stuff: {', '.join(missing)}", Style.YELLOW)
    s.start()

    success = False
    # Detect Package Manager
    if os.path.exists("/etc/arch-release"):
        success = run_cmd(["sudo", "pacman", "-S", "--noconfirm", "--needed"] + missing)
    elif os.path.exists("/etc/debian_version"):
        run_cmd(["sudo", "apt", "update"])
        success = run_cmd(["sudo", "apt", "install", "-y"] + missing)
    elif os.path.exists("/etc/fedora-release"):
        success = run_cmd(["sudo", "dnf", "install", "-y"] + missing)
    elif sys.platform == "darwin":
        if not check_installed("brew"):
            s.fail("Homebrew not found! Install it first.")
            return
        success = run_cmd(["brew", "install"] + missing)

    if success:
        s.success("Dependencies installed!")
    else:
        s.fail("Could not install dependencies. Check sudo?")
        sys.exit(1)


def task_install_starship():
    """Installs Starship prompt."""
    if check_installed("starship"):
        s = Spinner("Checking Starship...", Style.DIM)
        s.start()
        time.sleep(0.3)
        s.success("Starship is already ready for blast off!")
        return

    s = Spinner("Launching Starship installation...", Style.MAGENTA)
    s.start()
    cmd = "curl -sS https://starship.rs/install.sh | sh -s -- -y"
    if run_cmd(cmd, shell=True):
        s.success("Starship installed!")
    else:
        s.fail("Starship crashed on landing.")


def task_update_submodules():
    """Pulls git submodules."""
    if not os.path.exists(".gitmodules"):
        return

    s = Spinner("Summoning submodules (plugins & themes)...", Style.BLUE)
    s.start()
    # First try to init
    run_cmd(["git", "submodule", "init"], ignore_errors=True)
    if run_cmd(["git", "submodule", "update", "--init", "--recursive"]):
        s.success("Submodules summoned.")
    else:
        s.fail("Failed to summon submodules.")


def task_stow_dotfiles():
    """Stows specific folders."""
    folders = ["zsh", "starship", "wallpapers"]

    # Filter out folders that don't exist
    to_stow = [f for f in folders if os.path.isdir(f)]

    if not to_stow:
        print(f"{Style.YELLOW}No dotfile folders found to stow!{Style.RESET}")
        return

    print(f"\n{Style.BOLD}Linking Configuration Files:{Style.RESET}")
    for folder in to_stow:
        s = Spinner(f"   {Style.ICONS['link']}  Linking {folder}...", Style.CYAN)
        s.start()

        target = os.path.expanduser("~")

        # Using subprocess to call stow with --adopt to handle conflicts
        success = run_cmd(["stow", "--adopt", "-v", "-t", target, folder])

        if success:
            s.success(f"Linked {folder}")
        else:
            s.fail(f"Could not link {folder}")

    # Optional: clean up git changes caused by adoption
    # run_cmd(["git", "checkout", "."])


def task_change_shell():
    """Changes shell to Zsh."""
    current_shell = os.environ.get("SHELL", "")
    zsh_path = shutil.which("zsh")

    if zsh_path and current_shell != zsh_path:
        print(
            f"\n{Style.YELLOW}{Style.ICONS['shell']}  Shell change required.{Style.RESET}"
        )
        print(
            f"    {Style.DIM}Run this command manually if prompted: {Style.BOLD}chsh -s {zsh_path}{Style.RESET}"
        )
        try:
            subprocess.run(["chsh", "-s", zsh_path])
            print(f"{Style.GREEN}    Shell updated!{Style.RESET}")
        except Exception:
            print(f"{Style.RED}    Automatic shell change failed.{Style.RESET}")
    else:
        s = Spinner("Checking shell...", Style.DIM)
        s.start()
        time.sleep(0.3)
        s.success("Already using Zsh!")


# --- 🏁 ENTRY POINT ---


def main():
    try:
        # Clear screen
        os.system("cls" if os.name == "nt" else "clear")

        print_banner()
        type_writer("Welcome. Let's set up your environment.", speed=0.04)
        print("")

        if os.geteuid() != 0:
            pass

        task_install_packages()
        task_install_starship()
        task_update_submodules()
        task_stow_dotfiles()
        task_change_shell()

        print("\n" + "=" * 50)
        type_writer("✨ Setup Complete! ✨", speed=0.08, color=Style.GREEN)
        print(f"{Style.DIM}Time to restart your terminal.{Style.RESET}\n")

    except KeyboardInterrupt:
        print(
            f"\n\n{Style.RED}Mission failed, installation aborted. Bye! 👋{Style.RESET}"
        )
        sys.exit(130)


if __name__ == "__main__":
    main()
