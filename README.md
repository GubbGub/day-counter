# Day Counter Plan

A small macOS app that tracks my build plan for turning a found pool-heater control board (Hayward / Emerson, PIC16F73) into a days-since counter. Firmware written with XC8 will live in this repo as the project progresses.

## Run it from source

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Build the .app

```bash
./build.sh
```

This creates `dist/Day Counter Plan.app` and copies it to `/Applications`.

## Where things live

| What | Where |
|---|---|
| The plan (phases and tasks) | `ui/tasks.json` |
| The interface | `ui/index.html` |
| Your checkmarks | `~/Library/Application Support/DayCounterPlan/progress.json` (not in the repo) |

To add or change tasks, edit `ui/tasks.json` and rebuild. Give every task a unique `id`; checkmarks are matched by id, so existing progress is kept.

## Custom icon

Put a 1024×1024 PNG somewhere, then:

```bash
./make_icon.sh path/to/icon-1024.png
./build.sh
```
