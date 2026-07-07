import json
from datetime import datetime


def save_report(
    source_playlist,
    target_playlist,
    matched,
    failed
):
    report = {
        "migration_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_playlist": source_playlist,
        "target_playlist": target_playlist,
        "matched_count": len(matched),
        "failed_count": len(failed),
        "matched_songs": matched,
        "failed_songs": failed,
    }

    filename = (
        f"reports/{source_playlist.replace(' ', '_')}_report.json"
    )

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    return filename