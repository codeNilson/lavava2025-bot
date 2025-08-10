from discord.ui import View, Select
import discord


class MapSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Haven", value="Haven"),
            discord.SelectOption(label="Icebox", value="Icebox"),
            discord.SelectOption(label="Pearl", value="Pearl"),
            discord.SelectOption(label="Sunset", value="Sunset"),
            discord.SelectOption(label="Lotus", value="Lotus"),
            discord.SelectOption(label="Abyss", value="Abyss"),
            discord.SelectOption(label="Breeze", value="Breeze"),
            discord.SelectOption(label="Bind", value="Bind"),
            discord.SelectOption(label="Fracture", value="Fracture"),
            discord.SelectOption(label="Split", value="Split"),
            discord.SelectOption(label="Ascent", value="Ascent"),
        ]
        super().__init__(
            placeholder="Escolha uma mapa para **BANIR**",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Você escolheu: {self.values[0]}", ephemeral=True
        )


class SelectMapView(View):
    def __init__(self, message: discord.Message | None = None, timeout=180):
        super().__init__(timeout=timeout)
        self.message: discord.Message | None = message
        self.add_item(MapSelect())
