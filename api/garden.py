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

    return garden


def get_plant_type(streak):
    if streak >= 30: return "sunflower"
    if streak >= 21: return "blossom"
    if streak >= 11: return "tree"
    if streak >= 6:  return "cactus"
    return "sprout"


# --- SVG drawing functions ---
# Each one returns a raw SVG fragment (string) for that plant type.


def draw_sprout(streak, leaf_color, stem_color):
    capped      = min(streak, 5)
    stem_height = 20 + (capped * 20)
    stem_y_end  = 160 - stem_height

    parts  = f'<rect x="80" y="{stem_y_end}" width="8" height="{stem_height}" fill="{stem_color}" />'
    parts += f'<rect x="60" y="158" width="58" height="10" rx="4" fill="#795548" />'

    if capped >= 1:
        parts += f'<ellipse cx="100" cy="{stem_y_end + 20}" rx="18" ry="10" fill="{leaf_color}" transform="rotate(-30 100 {stem_y_end + 20})" />'
    if capped >= 2:
        parts += f'<ellipse cx="100" cy="{stem_y_end + 10}" rx="18" ry="10" fill="{leaf_color}" transform="rotate(30 100 {stem_y_end + 10})" />'
    if capped >= 3:
        parts += f'<ellipse cx="100" cy="{stem_y_end}" rx="20" ry="12" fill="{leaf_color}" />'
    if capped >= 4:
        parts += f'<circle cx="100" cy="{stem_y_end - 12}" r="14" fill="#e91e63" />'
    if capped >= 5:
        parts += f'<circle cx="100" cy="{stem_y_end - 12}" r="14" fill="#e91e63"><animate attributeName="r" values="14;17;14" dur="2s" repeatCount="indefinite" /></circle>'

    return parts

def draw_cactus(streak):
    cactus_stage = min(streak - 5, 5)

    parts  = '<rect x="95" y="100" width="12" height="60" fill="#2e7d32" />'
    parts += '<rect x="80" y="158" width="42" height="10" rx="4" fill="#795548" />'

    if cactus_stage >= 2:
        parts += '<rect x="62" y="110" width="10" height="30" fill="#2e7d32" />'
    if cactus_stage >= 3:
        parts += '<rect x="68" y="120" width="27" height="10" fill="#2e7d32" />'
    if cactus_stage >= 4:
        parts += '<rect x="130" y="118" width="10" height="30" fill="#2e7d32" />'
    if cactus_stage >= 5:
        parts += '<rect x="107" y="130" width="27" height="10" fill="#2e7d32" />'
        parts += '<circle cx="100" cy="98" r="6" fill="#a5d6a7" />'

    return parts

def draw_tree(streak):
    tree_stage = min(streak - 10, 5)

    parts  = '<rect x="94" y="120" width="14" height="40" fill="#5d4037" />'
    parts += '<rect x="72" y="158" width="58" height="10" rx="4" fill="#795548" />'

    if tree_stage >= 2:
        parts += '<ellipse cx="100" cy="105" rx="35" ry="30" fill="#388e3c" />'
    if tree_stage >= 3:
        parts += '<ellipse cx="75" cy="118" rx="22" ry="18" fill="#43a047" />'
    if tree_stage >= 4:
        parts += '<ellipse cx="125" cy="118" rx="22" ry="18" fill="#43a047" />'
    if tree_stage >= 5:
        parts += '<ellipse cx="100" cy="85" rx="25" ry="22" fill="#66bb6a" />'

    return parts

def draw_blossom(streak):
    blossom_stage = min(streak - 20, 5)

    parts  = '<rect x="94" y="120" width="14" height="40" fill="#5d4037" />'
    parts += '<rect x="72" y="158" width="58" height="10" rx="4" fill="#795548" />'

    if blossom_stage >= 2:
        parts += '<ellipse cx="100" cy="100" rx="38" ry="32" fill="#f8bbd0" />'
    if blossom_stage >= 3:
        parts += '<ellipse cx="72" cy="115" rx="24" ry="18" fill="#f48fb1" />'
        parts += '<ellipse cx="128" cy="115" rx="24" ry="18" fill="#f48fb1" />'
    if blossom_stage >= 4:
        parts += '<ellipse cx="100" cy="82" rx="26" ry="20" fill="#fce4ec" />'
    if blossom_stage >= 5:
        parts += '<circle cx="100" cy="95" r="8" fill="#ffeb3b" />'
        parts += '<circle cx="100" cy="95" r="8" fill="#ffeb3b"><animate attributeName="r" values="8;11;8" dur="3s" repeatCount="indefinite" /></circle>'

    return parts

def draw_sunflower(streak):
    sunflower_stage = min(streak - 29, 5)

    parts  = '<rect x="94" y="110" width="14" height="50" fill="#5d4037" />'
    parts += '<rect x="72" y="158" width="58" height="10" rx="4" fill="#795548" />'

    if sunflower_stage >= 2:
        parts += '<circle cx="100" cy="80" r="16" fill="#8d4e00" />'
    if sunflower_stage >= 3:
        parts += '<ellipse cx="100" cy="50" rx="8" ry="14" fill="#ffeb3b" />'
        parts += '<ellipse cx="100" cy="110" rx="8" ry="14" fill="#ffeb3b" />'
        parts += '<ellipse cx="70" cy="80" rx="14" ry="8" fill="#ffeb3b" />'
        parts += '<ellipse cx="130" cy="80" rx="14" ry="8" fill="#ffeb3b" />'
    if sunflower_stage >= 4:
        parts += '<ellipse cx="78" cy="58" rx="8" ry="14" fill="#ffeb3b" transform="rotate(-45 78 58)" />'
        parts += '<ellipse cx="122" cy="58" rx="8" ry="14" fill="#ffeb3b" transform="rotate(45 122 58)" />'
        parts += '<ellipse cx="78" cy="102" rx="8" ry="14" fill="#ffeb3b" transform="rotate(45 78 102)" />'
        parts += '<ellipse cx="122" cy="102" rx="8" ry="14" fill="#ffeb3b" transform="rotate(-45 122 102)" />'
    if sunflower_stage >= 5:
        parts += '<circle cx="100" cy="80" r="16" fill="#8d4e00" />'
        parts += '<circle cx="100" cy="80" r="8" fill="#5d3a00"><animate attributeName="r" values="8;10;8" dur="2s" repeatCount="indefinite" /></circle>'

    return parts


def draw_svg(garden):
    streak     = garden["streak"]
    wilting    = garden["wilting"]
    plant_type = get_plant_type(streak)

    leaf_color = "#4caf50" if not wilting else "#a0522d"
    stem_color = "#388e3c" if not wilting else "#8b6914"

    plants = {
        "sprout":    lambda: draw_sprout(streak, leaf_color, stem_color),
        "cactus":    lambda: draw_cactus(streak),
        "tree":      lambda: draw_tree(streak),
        "blossom":   lambda: draw_blossom(streak),
        "sunflower": lambda: draw_sunflower(streak),
    }

    plant = plants[plant_type]()

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="200" height="170" viewBox="0 0 200 170">
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