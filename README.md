# macOS Screen Time

A small macOS Terminal utility that shows how much time you’ve spent using your Mac on battery.

It shows your total time on battery and breaks it down into screen-on and screen-off time, so you can see how long you were actively using your Mac and how long it was running with the screen off.

The utility uses the built-in macOS `pmset` power-management log. It runs only when you launch it and does not run in the background or store any data.

## Example

```text
────────────────────────────────────
          Battery Usage
────────────────────────────────────

Battery Time:        22h 41m
Screen On Time:       8h 15m
Screen Off Time:     14h 25m

```

## Requirements

* Python 3
* Terminal

*Tested on: macOS 27 (Golden Gate).*

## Installation

1. [Download](https://github.com/Zhrkrpr/macos-screen-time/releases/download/v1.0/screen_time.py) `screen_time.py` from this repository.
2. Move the file to your home folder.

   In Finder, go to:

   **Macintosh HD → Users → YOUR-USERNAME**

   and place the file there.

   The file location should be:

```text
/Users/YOUR-USERNAME/screen_time.py
```

3. Open Terminal and make the script executable:

```bash
chmod +x ~/screen_time.py
```

4. Create the permanent `screen time` command:

```bash
unset -f screen 2>/dev/null; unhash screen 2>/dev/null; echo 'screen() { [[ "$1" == "time" ]] && "$HOME/screen_time.py"; }' >> ~/.zshrc; source ~/.zshrc
```

5. Run the script:

```bash
screen time
```

## Uninstallation

To remove the `screen time` command from your shell configuration:

```bash
sed -i '' '/^screen() {.*screen_time\.py.*}$/d' ~/.zshrc && source ~/.zshrc && unset -f screen
```

The script file itself is not removed. If you also want to delete it:

```bash
rm ~/screen_time.py
```
