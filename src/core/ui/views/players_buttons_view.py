from typing import TYPE_CHECKING

import discord

from src.core.ui.embeds import build_team_selection_embed
from src.models.player_model import Player

if TYPE_CHECKING:
    from src.core.cogs.match import MatchCog


class PlayersButtonsView(discord.ui.View):
    """View for player buttons in the match context."""

    def __init__(self, cog: "MatchCog", timeout=180):
        super().__init__(timeout=5)
        self.cog = cog
        self.message: discord.Message | None = None

    async def on_timeout(self):
        # for child in self.children:
        #     if isinstance(child, discord.ui.Button):
        #         child.disabled = True
        if self.message:

            timeout_embed = discord.Embed(
                title="⏰ Tempo Esgotado",
                description="O tempo para escolher os jogadores expirou.",
                color=discord.Color.orange(),
            )

            await self.message.edit(embed=timeout_embed, view=None)

    async def add_player_button(self, player: Player):
        """Add a button for a player."""

        # Skip adding button for captains
        if player in (
            self.cog.current_match.attacking_captain,
            self.cog.current_match.defending_captain,
        ):
            return

        button = discord.ui.Button(
            label=player.username,
            style=discord.ButtonStyle.primary,
            custom_id=player.username,
        )

        async def button_callback(interaction: discord.Interaction):

            if (
                not self.cog.current_match.attacking_captain
                or not self.cog.current_match.defending_captain
            ):
                await interaction.response.send_message(
                    "Nenhum capitão foi escolhido ainda.",
                    ephemeral=True,
                    delete_after=30,
                )
                return

            # Total picks made (excluding the captains already present in the team lists)
            picks_made = (
                len(self.cog.current_match.attacking_team)
                - 1
                + len(self.cog.current_match.defending_team)
                - 1
            )

            # Custom pick order: First captain at picks 1,3,5,8 | Second captain at picks 2,4,6,7
            pick_index = picks_made + 1  # 1-based
            first_turn_indices = {1, 3, 5, 8}
            is_first_turn_now = pick_index in first_turn_indices

            first_captain = self.cog.current_match.attacking_captain
            second_captain = self.cog.current_match.defending_captain

            current_turn_captain = (
                first_captain if is_first_turn_now else second_captain
            )

            # Block interaction from users who are not the current-turn captain
            if interaction.user.id != current_turn_captain.discord_id:
                # If user is a captain but it's not their turn
                if interaction.user.id in (
                    first_captain.discord_id,
                    second_captain.discord_id,
                ):
                    await interaction.response.send_message(
                        "Ainda não é sua vez de escolher.",
                        ephemeral=True,
                        delete_after=5,
                    )
                    return
                # If user is not a captain
                await interaction.response.send_message(
                    "Apenas capitães podem escolher jogadores.",
                    ephemeral=True,
                    delete_after=5,
                )
                return

            # Apply the pick to the correct team
            if is_first_turn_now:
                self.cog.current_match.attacking_team.append(player)
            else:
                self.cog.current_match.defending_team.append(player)

            # Update the turn flag to reflect the next pick, keeping compatibility
            new_picks_made = picks_made + 1
            next_pick_index = new_picks_made + 1
            self.cog.current_match.is_attacking_captain_turn = (
                next_pick_index in first_turn_indices
            )

            for button in self.children:
                if not isinstance(button, discord.ui.Button):
                    continue
                if button.custom_id == player.username:
                    button.disabled = True
                    button.style = discord.ButtonStyle.secondary

            # If we've reached the last pick, disable all buttons
            if new_picks_made >= 8:
                for button in self.children:
                    if isinstance(button, discord.ui.Button):
                        button.disabled = True
                        button.style = discord.ButtonStyle.secondary
                self.stop()

            await interaction.response.edit_message(
                embed=build_team_selection_embed(
                    self.cog.current_match.attacking_team,
                    self.cog.current_match.defending_team,
                ),
                view=self,
            )

        button.callback = button_callback
        self.add_item(button)
