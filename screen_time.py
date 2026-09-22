#!/usr/bin/env python3

import re
import subprocess
import sys
from datetime import datetime

SEPARATOR = "────────────────────────────────────"


def run_pmset_log():
    try:
        result = subprocess.run(
            ["pmset", "-g", "log"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error: could not read pmset log: {e}", file=sys.stderr)
        print("Помилка: не вдалося прочитати журнал pmset.", file=sys.stderr)
        sys.exit(1)


def get_current_power_source():
    try:
        result = subprocess.run(
            ["pmset", "-g", "batt"],
            capture_output=True,
            text=True,
            check=True,
        )
        output = result.stdout

        if "Now drawing from 'AC Power'" in output:
            return "AC"

        if "Now drawing from 'Battery Power'" in output:
            return "Battery"

    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    return None


def parse_timestamp(line):
    match = re.match(
        r"^\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})",
        line,
    )

    if not match:
        return None

    try:
        return datetime.strptime(
            match.group(1),
            "%Y-%m-%d %H:%M:%S",
        )
    except ValueError:
        return None


def find_latest_ac_to_battery(lines):
    events = []

    for line in lines:
        timestamp = parse_timestamp(line)

        if timestamp is None:
            continue

        if "Using AC" in line:
            events.append((timestamp, "AC"))
        elif "Using Batt" in line:
            events.append((timestamp, "Battery"))

    for i in range(len(events) - 1, -1, -1):
        timestamp, event = events[i]

        if event != "AC":
            continue

        for j in range(i + 1, len(events)):
            next_timestamp, next_event = events[j]

            if next_event == "Battery":
                return timestamp, next_timestamp

            if next_event == "AC":
                break

    return None


def find_initial_display_state(lines, battery_start):
    state = None

    for line in lines:
        timestamp = parse_timestamp(line)

        if timestamp is None:
            continue

        if timestamp > battery_start:
            break

        if "Display is turned on" in line:
            state = "on"
        elif "Display is turned off" in line:
            state = "off"

    return state


def calculate_screen_on_time(lines, battery_start, now):
    state = find_initial_display_state(lines, battery_start)

    if state is None:
        return None

    screen_on_seconds = 0
    last_timestamp = battery_start

    for line in lines:
        timestamp = parse_timestamp(line)

        if timestamp is None:
            continue

        if timestamp < battery_start:
            continue

        if timestamp > now:
            break

        if "Display is turned on" in line:
            if state == "off":
                last_timestamp = timestamp
                state = "on"

        elif "Display is turned off" in line:
            if state == "on":
                screen_on_seconds += (
                    timestamp - last_timestamp
                ).total_seconds()
                state = "off"
                last_timestamp = timestamp

    if state == "on":
        screen_on_seconds += (
            now - last_timestamp
        ).total_seconds()

    return max(0, screen_on_seconds)


def format_duration(seconds):
    minutes = int(seconds // 60)
    hours = minutes // 60
    minutes %= 60
    return f"{hours}h {minutes:02d}m"


def print_power_status():
    print()
    print("Power Status".center(len(SEPARATOR)))
    print(SEPARATOR)
    print()
    print("Mac is currently connected to power.")
    print()
    print("Screen time is calculated only for battery sessions.")
    print("Unplug your Mac and use it for a while,")
    print("then run this command again.")
    print()
    print("Стан живлення".center(len(SEPARATOR)))
    print(SEPARATOR)
    print()
    print("Mac зараз підключений до живлення.")
    print()
    print("Час роботи від акумулятора розраховується лише")
    print("для сеансів роботи від акумулятора.")
    print("Від'єднайте Mac від живлення, попрацюйте деякий час,")
    print("а потім запустіть цю команду ще раз.")
    print()


def print_battery_session(battery_seconds, screen_on_seconds, screen_off_seconds):
    print()
    print(SEPARATOR
    print("Screen Time".center(len(SEPARATOR)))
    print(SEPARATOR)
    print()
    print(f"{'Battery Time:':<21}{format_duration(battery_seconds)}")
    print(f"{'Screen On Time:':<21}{format_duration(screen_on_seconds)}")
    print(f"{'Screen Off Time:':<21}{format_duration(screen_off_seconds)}")
    print()

def print_transition_error():
    print(SEPARATOR)
    print("              Error")
    print(SEPARATOR)
    print()
    print("Could not determine the last AC → Battery transition from the available pmset history.")
    print()
    print("The required event may have already fallen out of the pmset log buffer.")
    print()
    print(SEPARATOR)
    print("             Помилка")
    print(SEPARATOR)
    print()
    print("Не вдалося визначити останній перехід з живлення від мережі на акумулятор.")
    print()
    print("Необхідна подія могла вже зникнути з доступного журналу pmset.")
    print()
    print(SEPARATOR)


def print_display_error():
    print(SEPARATOR)
    print("              Error")
    print(SEPARATOR)
    print()
    print("Could not determine the initial display state for the current battery session.")
    print()
    print("The required display event may not be available in the pmset log.")
    print()
    print(SEPARATOR)
    print("             Помилка")
    print(SEPARATOR)
    print()
    print("Не вдалося визначити початковий стан екрана для поточного сеансу роботи від акумулятора.")
    print()
    print("Необхідна подія стану екрана може бути відсутня в журналі pmset.")
    print()
    print(SEPARATOR)


def main():
    current_power = get_current_power_source()

    if current_power == "AC":
        print_power_status()
        return

    log = run_pmset_log()
    lines = log.splitlines()

    transition = find_latest_ac_to_battery(lines)

    if transition is None:
        print_transition_error()
        return

    _, battery_start = transition
    now = datetime.now()

    battery_seconds = max(
        0,
        (now - battery_start).total_seconds(),
    )

    screen_on_seconds = calculate_screen_on_time(
        lines,
        battery_start,
        now,
    )

    if screen_on_seconds is None:
        print_display_error()
        return

    screen_off_seconds = max(
        0,
        battery_seconds - screen_on_seconds,
    )

    print_battery_session(
        battery_seconds,
        screen_on_seconds,
        screen_off_seconds,
    )


if __name__ == "__main__":
    main()
