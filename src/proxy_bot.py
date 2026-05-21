# Liberías 
import discord
import asyncio
import os

# Funciones del Agente
from discord import app_commands
from src.agent import auditar_evidencia_cientifica

# Variables de entorno
from dotenv import load_dotenv
load_dotenv()

# Configuración de Intents básicos para el bot
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Token del bot
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

@client.event
async def on_ready():
    # Sincroniza los comandos de barra (Slash Commands) con Discord
    await tree.sync()
    print(f"AI Kids Proxy Bot en línea como: {client.user}")

# Comando Subir Dato: Aquí es donde los alumnos interactúan con el bot para enviar su evidencia científica.
@tree.command(
    name="subir_dato", 
    description="Envía una evidencia científica a la DAO AI Kids Peru"
)
@app_commands.describe(
    descripcion="¿Qué encontraste? Ejemplo: 'Muestra de agua del río Rímac con sedimento'",
    wallet="Tu dirección de Pali Wallet (Syscoin) para recibir tu SBT",
    evidencia="Sube la foto o imagen de tu investigación escolar"
)
async def subir_dato(
    interaction: discord.Interaction, 
    descripcion: str, 
    wallet: str, 
    evidencia: discord.Attachment
):
    # Validación rápida en el Proxy: Asegurar que sea una imagen
    if not evidencia.content_type or not evidencia.content_type.startswith("image/"):
        await interaction.response.send_message(
            "Error: El archivo adjunto debe ser una imagen válida (PNG/JPG).", 
            ephemeral=True
        )
        return

    # Aplazar respuesta: La IA tarda más de 3 segundos :C
    await interaction.response.defer(ephemeral=False) # Esto evita que Discord lance un error de timeout.
    
    # Información del "payload"
    payload = {
        "alumno_discord": str(interaction.user),
        "alumno_id": interaction.user.id,
        "descripcion": descripcion,
        "wallet": wallet,
        "imagen_url": evidencia.url  # Discord nos da la URL de la imagen guardada en sus servidores
    }

    # Mensaje de progreso para el alumno
    await interaction.followup.send(
        f"**¡Datos recibidos, {interaction.user.mention}!**\n"
        f"Enviando evidencia al *Agente Auditor* para validación científica..."
    )

    # Conexión con el Agente: 
    try:
        # Pasamos los datos del payload a la función del agente
        veredicto = await asyncio.to_thread(
            auditar_evidencia_cientifica, 
            payload["descripcion"], 
            payload["imagen_url"]
        )
        
        estado = veredicto.get("aprobado", False)
        motivo = veredicto.get("motivo", "Error al procesar el motivo.")
        
        # Guardamos el veredicto 
        payload["auditoria_aprobada"] = estado
        payload["auditoria_motivo"] = motivo

        # Tarjeta visual para Discord
        if estado:
            color = discord.Color.green()
            titulo = "VALIDACIÓN EXITOSA: EVIDENCIA APROBADA"
            w = payload["wallet"]
            mensaje_sbt = f"Emitiendo **Pasaporte STEM SBT** a la wallet `{w[:6]}...{w[-4:]}` en zkSyscoin."
            
            # Próximamente: Aquí es donde llamaríamos a la función de minting del SBT
            # ejecutar_mint_sbt(payload) 
        else:
            color = discord.Color.red()
            titulo = "ALERTA: EVIDENCIA RECHAZADA"
            mensaje_sbt = "La emisión del SBT ha sido bloqueada de acuerdo al protocolo de la DAO."

        embed = discord.Embed(title=titulo, color=color)
        embed.add_field(name="Científico Ciudadano", value=payload["alumno_discord"], inline=True)
        embed.add_field(name="Estado DAO", value=mensaje_sbt, inline=False)
        embed.add_field(name="Veredicto del Agente IA", value=f"*{motivo}*", inline=False)
        embed.set_image(url=payload["imagen_url"])
        
        await interaction.followup.send(embed=embed)

    except Exception as e:
        await interaction.followup.send(f"Hubo un problema crítico: {str(e)}")

# Ejecutar el bot
if __name__ == "__main__":
    client.run(DISCORD_TOKEN)