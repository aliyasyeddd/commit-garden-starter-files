import json
import os
import subprocess
from datetime import date, timedelta

# PATHS
BASE_DIR = os.path.dirname(__file__)
REPO = os.path.abspath(os.path.join(BASE_DIR, '..'))
GARDEN_FILE = os.path.join(BASE_DIR, '..', 'data', 'garden.json')
SVG_FILE = os.path.join(BASE_DIR, '..', 'data', 'garden.svg')

# DEFAULT GARDEN DATA
DEFAULT_GARDEN = {
    "streak": 0,
    "last_commit_date": None,
    "plant_stage": 0,
    "wilting": False,
    "total_commits": 0,
    "best_streak": 0,
    "daily_commits": 0
}


def load_garden():
    try:
        with open(GARDEN_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return DEFAULT_GARDEN.copy()


def save_garden(data):
    with open(GARDEN_FILE, "w") as f:
        json.dump(data, f, indent=2)


def update_streak(garden):
    """
    Updates streak, daily_commits, best_streak, plant_stage based on
    today's commit vs last_commit_date.
    """
    today = str(date.today())
    yesterday = str(date.today() - timedelta(days=1))
    last = garden.get("last_commit_date")

    # --- new-day reset for daily_commits (NEW in "after") ---
    # TODO: if last != today, reset garden["daily_commits"] = 0
    # TODO: increment garden["daily_commits"] += 1 regardless of branch below
    # NOTE: same-day short circuit below must come AFTER this, since
    # daily_commits needs to update even on repeat commits same day.

    if last == today:
        return garden

    if last == yesterday:
        garden["streak"] += 1
        garden["wilting"] = False
    elif last is None:
        garden["streak"] = 1
        garden["wilting"] = False
    else:
        garden["streak"] = 1
        garden["wilting"] = True

    garden["last_commit_date"] = today
    garden["total_commits"] = garden.get("total_commits", 0) + 1

    # TODO: garden["plant_stage"] = garden["streak"]   (was min(streak, 5) before —
    #       now plant TYPE handles capping via get_plant_type, not plant_stage)
    # TODO: garden["best_streak"] = max(garden.get("best_streak", 0), garden["streak"])  (NEW)

    return garden


def get_plant_type(streak):
    if streak >= 30: return "sunflower"
    if streak >= 21: return "blossom"
    if streak >= 11: return "tree"
    if streak >= 6:  return "cactus"
    return "sprout"


# --- SVG drawing functions ---
# Each one returns a raw SVG fragment (string) for that plant type.
# Only draw_sprout needs streak-based scaling; others are static shapes
# that can be filled in with fixed markup later.

def draw_sprout(streak, leaf_color, stem_color):
    stage = min(streak, 5)
    stem_height = 20 + (stage * 20)
    stem_y_end = 160 - stem_height
    leaves = ""

    if stage >= 1:
        leaves += f'<ellipse cx="100" cy="{stem_y_end + 20}" rx="18" ry="10" fill="{leaf_color}" transform="rotate(-30 100 {stem_y_end + 20})" />'
    if stage >= 2:
        leaves += f'<ellipse cx="100" cy="{stem_y_end + 10}" rx="18" ry="10" fill="{leaf_color}" transform="rotate(30 100 {stem_y_end + 10})" />'
    if stage >= 3:
        leaves += f'<ellipse cx="100" cy="{stem_y_end}" rx="20" ry="12" fill="{leaf_color}" />'
    if stage >= 4:
        leaves += f'<circle cx="100" cy="{stem_y_end - 12}" r="14" fill="#e91e63" />'
    if stage >= 5:
        leaves += f'<circle cx="100" cy="{stem_y_end - 12}" r="14" fill="#e91e63"><animate attributeName="r" values="14;17;14" dur="2s" repeatCount="indefinite" /></circle>'

    return f"""
  <rect x="80" y="{stem_y_end}" width="8" height="{stem_height}" fill="{stem_color}" />
  <rect x="60" y="158" width="58" height="10" rx="4" fill="#795548" />
  {leaves}"""


def draw_cactus():
    return """
  <rect x="95" y="80" width="12" height="80" fill="#2e7d32" />
  <rect x="68" y="100" width="27" height="10" fill="#2e7d32" />
  <rect x="62" y="90" width="10" height="30" fill="#2e7d32" />
  <rect x="107" y="110" width="27" height="10" fill="#2e7d32" />
  <rect x="130" y="98" width="10" height="30" fill="#2e7d32" />
  <rect x="80" y="158" width="42" height="10" rx="4" fill="#795548" />
  <circle cx="100" cy="78" r="6" fill="#a5d6a7" />"""


def draw_tree():
    return """
  <rect x="94" y="110" width="14" height="50" fill="#5d4037" />
  <ellipse cx="100" cy="90" rx="35" ry="30" fill="#388e3c" />
  <ellipse cx="75" cy="105" rx="22" ry="18" fill="#43a047" />
  <ellipse cx="125" cy="105" rx="22" ry="18" fill="#43a047" />
  <ellipse cx="100" cy="70" rx="25" ry="22" fill="#66bb6a" />
  <rect x="72" y="158" width="58" height="10" rx="4" fill="#795548" />"""


def draw_blossom():
    return """
  <rect x="94" y="110" width="14" height="50" fill="#5d4037" />
  <ellipse cx="100" cy="85" rx="38" ry="32" fill="#f8bbd0" />
  <ellipse cx="72" cy="102" rx="24" ry="18" fill="#f48fb1" />
  <ellipse cx="128" cy="102" rx="24" ry="18" fill="#f48fb1" />
  <ellipse cx="100" cy="68" rx="26" ry="20" fill="#fce4ec" />
  <circle cx="100" cy="80" r="8" fill="#ffeb3b" />
  <circle cx="100" cy="80" r="8" fill="#ffeb3b"><animate attributeName="r" values="8;11;8" dur="3s" repeatCount="indefinite" /></circle>
  <rect x="72" y="158" width="58" height="10" rx="4" fill="#795548" />"""


def draw_sunflower():
    return """
  <rect x="94" y="110" width="14" height="60" fill="#5d4037" />
  <rect x="72" y="168" width="58" height="10" rx="4" fill="#795548" />
  <circle cx="100" cy="75" r="28" fill="#ffeb3b" />
  <circle cx="100" cy="75" r="28" fill="#ffeb3b"><animate attributeName="r" values="28;32;28" dur="2s" repeatCount="indefinite" /></circle>
  <circle cx="100" cy="75" r="16" fill="#8d4e00" />
  <ellipse cx="100" cy="42" rx="8" ry="14" fill="#ffeb3b" />
  <ellipse cx="100" cy="108" rx="8" ry="14" fill="#ffeb3b" />
  <ellipse cx="67" cy="75" rx="14" ry="8" fill="#ffeb3b" />
  <ellipse cx="133" cy="75" rx="14" ry="8" fill="#ffeb3b" />
  <ellipse cx="77" cy="52" rx="8" ry="14" fill="#ffeb3b" transform="rotate(-45 77 52)" />
  <ellipse cx="123" cy="52" rx="8" ry="14" fill="#ffeb3b" transform="rotate(45 123 52)" />
  <ellipse cx="77" cy="98" rx="8" ry="14" fill="#ffeb3b" transform="rotate(45 77 98)" />
  <ellipse cx="123" cy="98" rx="8" ry="14" fill="#ffeb3b" transform="rotate(-45 123 98)" />"""


def draw_svg(garden):
    """
    Picks the right draw_* function via plant type, wraps result in
    the outer <svg> tag, and writes it to SVG_FILE.

    NOTE: earlier version rendered a "🔥 X day streak" text label and a
    wilt warning message ("💧 Missed a day — keep going!") directly on
    the SVG. Neither appears here — decide if that's intentional (moved
    to the frontend UI?) or something to re-add.
    """
    streak = garden["streak"]
    wilting = garden["wilting"]
    plant_type = get_plant_type(streak)

    leaf_color = "#4caf50" if not wilting else "#a0522d"
    stem_color = "#388e3c" if not wilting else "#8b6914"

    # Dict-of-functions dispatch so adding a new plant type later
    # doesn't require touching this function's control flow.
    plants = {
        "sprout": lambda: draw_sprout(streak, leaf_color, stem_color),
        "cactus": draw_cactus,
        "tree": draw_tree,
        "blossom": draw_blossom,
        "sunflower": draw_sunflower,
    }

    plant = plants[plant_type]()

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="200" height="170" viewBox="0 0 200 170">
  <rect x="0" y="0" width="200" height="170" fill="transparent" />
  {plant}
</svg>"""

    with open(SVG_FILE, "w", encoding="utf-8") as f:
        f.write(svg)


def stage_commit():
    subprocess.run(["git", "-C", REPO, "add", GARDEN_FILE, SVG_FILE], check=True)
    subprocess.run(
        ["git", "-C", REPO, "commit", "--no-verify", "-m", "garden updated"],
        capture_output=True
    )


def main():
    garden = load_garden()
    garden = update_streak(garden)
    save_garden(garden)
    draw_svg(garden)
    stage_commit()


if __name__ == "__main__":
    main()