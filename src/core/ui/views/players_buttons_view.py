from typing import TYPE_CHECKING

import discord

from src.core.ui.embeds import choose_captains_embed
from src.models.player_model import Player

if TYPE_CHECKING:
    from src.core.cogs.match import MatchCog


class PlayersButtonsView(discord.ui.View):
    """View for player buttons in the match context."""

    def __init__(self, cog: "MatchCog", timeout=180):
        super().__init__(timeout=timeout)
        self.cog = cog
        self.message: discord.Message | None = None

    async def on_timeout(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True

    async def add_player_button(self, player: Player):
        """Add a button for a player."""

        # Skip adding button for captains
        if player in (
            self.cog.current_match.first_captain,
            self.cog.current_match.second_captain,
        ):
            return

        button = discord.ui.Button(
            label=player.username,
            style=discord.ButtonStyle.primary,
            custom_id=player.username,
        )

        async def button_callback(interaction: discord.Interaction):

            if (
                not self.cog.current_match.first_captain
                or not self.cog.current_match.second_captain
            ):
                await interaction.response.send_message(
                    "Nenhum capitão foi escolhido ainda.",
                    ephemeral=True,
                    delete_after=30,
                )
                return

            if (
                interaction.user.id == self.cog.current_match.first_captain.discord_id
                and self.cog.current_match.is_first_captain_turn
            ):
                self.cog.current_match.first_captain_team.append(player)
            elif (
                interaction.user.id == self.cog.current_match.second_captain.discord_id
                and not self.cog.current_match.is_first_captain_turn
            ):
                self.cog.current_match.second_captain_team.append(player)
            elif interaction.user.id in (
                self.cog.current_match.first_captain.discord_id,
                self.cog.current_match.second_captain.discord_id,
            ):
                await interaction.response.send_message(
                    "Ainda não é sua vez de escolher.",
                    ephemeral=True,
                    delete_after=5,
                )
                return

            else:
                await interaction.response.send_message(
                    "Apenas capitães podem escolher jogadores.",
                    ephemeral=True,
                    delete_after=5,
                )
                return

            # Altera a vez do capitão
            self.cog.current_match.is_first_captain_turn = (
                not self.cog.current_match.is_first_captain_turn
            )

            for button in self.children:
                if not isinstance(button, discord.ui.Button):
                    return
                if button.custom_id == player.username:
                    button.disabled = True
                    button.style = discord.ButtonStyle.secondary

            await interaction.response.edit_message(
                embed=choose_captains_embed(
                    self.cog.current_match.first_captain_team,
                    self.cog.current_match.second_captain_team,
                ),
                view=self,
            )

        button.callback = button_callback
        self.add_item(button)
