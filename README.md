# macOS Screen Time

A small macOS Terminal script that shows how long your Mac has been on battery and breaks that time down into screen-on and screen-off periods.

The script reads the existing macOS `pmset` power-management log. It does not run in the background and does not store any data.

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
