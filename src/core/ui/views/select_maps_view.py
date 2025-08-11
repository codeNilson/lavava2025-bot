import random
from typing import Optional, override, TYPE_CHECKING
from discord.ui import View, Select
import discord

if TYPE_CHECKING:
    from src.core.cogs.match import MatchCog


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

        options = [discord.SelectOption(label=m, value=m) for m in self.maps]
        super().__init__(
            placeholder="Escolha uma mapa para **BANIR**",
            min_values=1,
            max_values=1,
            options=options,
        )

        self.captains_choices: dict[str, Optional[str]] = {
            "first_captain_choice": None,
            "second_captain_choicer": None,
        }

    @override
    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        first_captain = self.view.cog.current_match.first_captain  # type:ignore
        second_captain = self.view.cog.current_match.second_captain  # type:ignore

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
            self.captains_choices["second_captain_choicer"] = choice
            await interaction.response.send_message(
                f"**{user.name}** escolheu **{choice}** para banir.",
                delete_after=5,
                ephemeral=True,
            )

        if (
            self.captains_choices["first_captain_choice"]
            and self.captains_choices["second_captain_choicer"]
        ):
            first_choice = self.captains_choices["first_captain_choice"]
            second_choice = self.captains_choices["second_captain_choicer"]

            map_choose = random.choice(
                [m for m in self.maps if m not in (first_choice, second_choice)]
            )

            self.view.cog.current_match.map_choose = map_choose  # type:ignore

            if self.view:
                print("Stopping view after map selection.")
                self.view.stop()

    @override
    async def interaction_check(  # pylint: disable=arguments-differ
        self, interaction: discord.Interaction
    ) -> bool:
        user = interaction.user

        first_captain = self.view.cog.current_match.first_captain  # type:ignore
        second_captain = self.view.cog.current_match.second_captain  # type:ignore

        if user.id not in (first_captain.discord_id, second_captain.discord_id):
            await interaction.response.send_message(
                "Apenas os capitães podem escolher mapas.",
            )
            return False
        return True


class SelectMapView(View):
    def __init__(
        self,
        cog: "MatchCog",
        message: discord.Message | None = None,
        timeout=180,
    ):
        super().__init__(timeout=timeout)
        self.cog: "MatchCog" = cog
        self.message: discord.Message | None = message
        self.add_item(MapSelect())
