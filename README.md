# macOS Screen Time

A small macOS Terminal script that shows how long your Mac has been on battery and breaks that time down into screen-on and screen-off periods.

The script reads the existing macOS `pmset` power-management log. It does not run in the background and does not store any data.

## Example

```text
────────────────────────────────────
          Battery Session
────────────────────────────────────

Battery Time:        0h 16m
Screen On Time:       0h 16m
Screen Off Time:     0h 00m

────────────────────────────────────
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

---




## macOS Screen Time

### 🇺🇦 Українська версія
Невеликий скрипт для Terminal у macOS, який показує, скільки часу Mac працював від акумулятора, і розділяє цей час на періоди з увімкненим та вимкненим екраном.

Скрипт читає наявний системний журнал керування живленням macOS `pmset`. Він не працює у фоновому режимі та не зберігає жодних даних.

## Приклад

```text
────────────────────────────────────
          Battery Session
────────────────────────────────────

Battery Time:        0h 16m
Screen On Time:       0h 16m
Screen Off Time:     0h 00m

────────────────────────────────────
```

## Вимоги

* Python 3
* Terminal

*Протестовано на: macOS 27 (Golden Gate).*

## Встановлення

1. [Завантажте файл](https://github.com/Zhrkrpr/macos-screen-time/releases/download/v1.0/screen_time.py) `screen_time.py` із цього репозиторію.
2. Перемістіть файл у свою домашню папку.

   У Finder відкрийте:

   **Macintosh HD → Users → YOUR-USERNAME**

   і помістіть файл туди.

   Розташування файлу має бути:

```text
/Users/YOUR-USERNAME/screen_time.py
```

3. Відкрийте Terminal і зробіть скрипт виконуваним:

```bash
chmod +x ~/screen_time.py
```

4. Створіть постійну команду `screen time`:

```bash
unset -f screen 2>/dev/null; unhash screen 2>/dev/null; echo 'screen() { [[ "$1" == "time" ]] && "$HOME/screen_time.py"; }' >> ~/.zshrc; source ~/.zshrc
```

5. Запустіть скрипт:

```bash
screen time
```

## Видалення

Щоб видалити команду `screen time` із конфігурації оболонки:

```bash
sed -i '' '/^screen() {.*screen_time\.py.*}$/d' ~/.zshrc && source ~/.zshrc && unset -f screen
```

Сам файл скрипта при цьому не видаляється. Якщо ви також хочете видалити його:

```bash
rm ~/screen_time.py
```
