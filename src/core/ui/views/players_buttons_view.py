from typing import TYPE_CHECKING

import discord

from src.core.ui.embeds import build_team_selection_embed
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

            # Total de picks realizados (excluindo os próprios capitães que já estão nas listas)
            picks_made = (
                len(self.cog.current_match.attacking_team)
                - 1
                + len(self.cog.current_match.defending_team)
                - 1
            )

            # Ordem personalizada: F: 1,3,5,8 | S: 2,4,6,7
            pick_index = picks_made + 1  # 1-based
            first_turn_indices = {1, 3, 5, 8}
            is_first_turn_now = pick_index in first_turn_indices

            first_captain = self.cog.current_match.attacking_captain
            second_captain = self.cog.current_match.defending_captain

            current_turn_captain = (
                first_captain if is_first_turn_now else second_captain
            )

            # Bloqueia a inteRação de quem não é o capitão da vez
            if interaction.user.id != current_turn_captain.discord_id:
                # Se for capitao, mas fora de turno
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
                # Se não for capitao
                await interaction.response.send_message(
                    "Apenas capitães podem escolher jogadores.",
                    ephemeral=True,
                    delete_after=5,
                )
                return

            # Aplica a escolha ao time correto
            if is_first_turn_now:
                self.cog.current_match.attacking_team.append(player)
            else:
                self.cog.current_match.defending_team.append(player)

            # Atualiza a flag de turno para refletir o próximo pick, mantendo compatibilidade
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

            # Se chegamos ao último pick, desabilita todos os botões
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
