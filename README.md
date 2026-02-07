# 🔧 Austryx's Dotfiles

A collection of configuration files and setup scripts to create a cozy, efficient, and aesthetically pleasing terminal environment.

![Wallpaper Preview](wallpapers/Pictures/wallpaper1.png)

## ✨ Features

* **Shell:** [Zsh](https://www.zsh.org/) because bash is what your grandpa uses.
* **Prompt:** [Starship](https://starship.rs/) cross-shell prompt customized with the **Catppuccin Macchiato** palette.
* **Plugins:**
    * `zsh-autosuggestions`: Fish-like autosuggestions for Zsh.
    * `zsh-syntax-highlighting`: Syntax highlighting for commands as you type.
* **Theme:** Consistent **Catppuccin** theming across shell and terminal. Subject to change.
* **Management:** Uses [GNU Stow](https://www.gnu.org/software/stow/) for easy dotfile symlinking. 

## 🚀 Installation

You can install these dotfiles using the automated Python script or by following the manual steps below.

### Option 1: The Installer (Recommended) 🐍

This automated script handles dependencies, backups, and symlinking.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/austryx/dotfiles.git](https://github.com/austryx/dotfiles.git) ~/dotfiles
    cd ~/dotfiles
    ```

2.  **Run the installer:**
    ```bash
    python3 install.py
    ```

### Option 2: Manual Installation

If you prefer to do things yourself or don't have Python installed, follow these steps.

1.  **Install Dependencies:**
    You will need `git`, `stow`, `zsh`, and `curl` installed via your system's package manager (e.g., `apt`, `pacman`, `brew`).
    
    You also need to install [Starship](https://starship.rs/):
    ```bash
    curl -sS [https://starship.rs/install.sh](https://starship.rs/install.sh) | sh
    ```

2.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/austryx/dotfiles.git](https://github.com/austryx/dotfiles.git) ~/dotfiles
    cd ~/dotfiles
    ```

3.  **Update Submodules:**
    This downloads the Zsh plugins and themes.
    ```bash
    git submodule update --init --recursive
    ```

4.  **Stow Configurations:**
    Use GNU Stow to symlink the configuration folders to your home directory. The `--adopt` flag allows Stow to overwrite existing files if necessary.
    ```bash
    stow --adopt -v -t ~ zsh starship wallpapers
    ```
    *Note: This will link `.zshrc`, `.config/starship.toml`, and your wallpapers.*

5.  **Change Default Shell:**
    Set Zsh as your default shell.
    ```bash
    chsh -s $(which zsh)
    ```

6.  **Restart:**
    Log out and back in, or restart your terminal to see the changes.

## 📂 What's Included

| Component | Description | Location |
| :--- | :--- | :--- |
| **Zsh** | Shell configuration, plugins, and environment variables. | `zsh/.zshrc` |
| **Starship** | High-performance, customizable prompt. | `starship/.config/starship.toml` |
| **Kitty** | Fast, feature-rich GPU-based terminal. | `.config/kitty/` (via submodule) |
| **Wallpapers** | A collection of wallpapers to match the aesthetic. | `wallpapers/Pictures/` |

## 🛠️ Customization

* **Colors:** The primary color scheme is **Catppuccin Macchiato**. You can adjust colors in `starship/.config/starship.toml`.
* **Shell:** To add more Zsh plugins, update the `.gitmodules` file or manually clone them into `zsh/.config/zsh/plugins/`.

## 🔄 Updates

To update your dotfiles and pull the latest changes from the repository (including submodules):

```bash
cd ~/dotfiles
git pull
git submodule update --init --recursive
# Re-run stow to link any new files
stow --adopt -v -t ~ zsh starship wallpapers
