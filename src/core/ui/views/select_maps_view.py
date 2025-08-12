import random
from typing import Optional, override, Any

import discord
from discord.ui import View, Select

# UI components for map ban selection


class MapSelect(Select):
    def __init__(self):
        self.maps = {
            "Haven",
            "Icebox",
            "Pearl",
            "Sunset",
            "Lotus",
            "Abyss",
            "Breeze",
            "Bind",
            "Fracture",
            "Split",
            "Ascent",
        }

        options = [discord.SelectOption(label=m, value=m) for m in sorted(self.maps)]
        super().__init__(
            placeholder="Escolha um mapa para BANIR",
            min_values=1,
            max_values=1,
            options=options,
        )
        # Captains' ban choices
        self.captains_choices: dict[str, Optional[str]] = {
            "first_captain_choice": None,
            "second_captain_choice": None,
        }

    @override
    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        first_captain = self.view.cog.current_match.attacking_captain  # type: ignore
        second_captain = self.view.cog.current_match.defending_captain  # type: ignore

        if user.id == first_captain.discord_id:
            choice = self.values[0]
            self.captains_choices["first_captain_choice"] = choice
            await interaction.response.send_message(
                f"**{user.name}** escolheu **{choice}** para banir.",
                delete_after=5,
                ephemeral=True,
            )

        elif user.id == second_captain.discord_id:
            choice = self.values[0]
            self.captains_choices["second_captain_choice"] = choice
            await interaction.response.send_message(
                f"**{user.name}** escolheu **{choice}** para banir.",
                delete_after=5,
                ephemeral=True,
            )

        if (
            self.captains_choices["first_captain_choice"]
            and self.captains_choices["second_captain_choice"]
        ):
            first_choice = self.captains_choices["first_captain_choice"]
            second_choice = self.captains_choices["second_captain_choice"]

            remaining = [m for m in self.maps if m not in (first_choice, second_choice)]
            selected_map = random.choice(remaining)

            self.view.cog.current_match.selected_map = selected_map  # type: ignore

            if self.view:
                self.view.stop()

    @override
    async def interaction_check(  # pylint: disable=arguments-differ
        self, interaction: discord.Interaction
    ) -> bool:
        user = interaction.user

        first_captain = self.view.cog.current_match.attacking_captain  # type: ignore
        second_captain = self.view.cog.current_match.defending_captain  # type: ignore

        if user.id not in (first_captain.discord_id, second_captain.discord_id):
            await interaction.response.send_message(
                "Apenas os capitães podem escolher mapas.",
                ephemeral=True,
                delete_after=5,
            )
            return False
        return True


class SelectMapView(View):
    def __init__(self, cog: Any, message: discord.Message | None = None, timeout: int = 180) -> None:
        super().__init__(timeout=timeout)
        self.cog = cog
        self.message = message
        self.add_item(MapSelect())
