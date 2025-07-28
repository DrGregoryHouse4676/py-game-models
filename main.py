import json
from django.utils import timezone
from db.models import Player, Race, Skill, Guild
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()


def main() -> None:
    with open("players.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for nickname, entry in data.items():
        race_data = entry["race"]
        race, _ = Race.objects.get_or_create(
            name=race_data["name"],
            defaults={"description": race_data.get("description", "")}
        )

        for skill_data in race_data.get("skills", []):
            Skill.objects.get_or_create(
                name=skill_data["name"],
                race=race,
                defaults={"bonus": skill_data.get("bonus", "")}
            )

        guild_data = entry.get("guild")
        guild = None
        if guild_data:
            guild, _ = Guild.objects.get_or_create(
                name=guild_data["name"],
                defaults={"description": guild_data.get("description")}
            )

        Player.objects.get_or_create(
            nickname=nickname,
            defaults={
                "email": entry.get("email", ""),
                "bio": entry.get("bio", ""),
                "race": race,
                "guild": guild,
                "created_at": timezone.now()
            }
        )


if __name__ == "__main__":
    main()
