import subprocess
import asyncio
from shazamio import Shazam

# Função para baixar um trecho do áudio do stream e salvar como MP3
def download_audio_segment(stream_url, duration=15, output_file="output.mp3"):
    try:
        # Comando para baixar e converter o áudio
        command = [
            'ffmpeg', 
            '-i', stream_url, 
            '-t', str(duration), 
            '-f', 'mp3', 
            output_file
        ]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao baixar o áudio: {e}")

# Função para identificar a música
async def identify_song(file_path):
    shazam = Shazam()
    out = await shazam.recognize(file_path)
    return out

# URL do stream
stream_url = "https://stream.zeno.fm/yn65fsaurfhvv"

# Baixar um trecho de 10 segundos do stream
download_audio_segment(stream_url, duration=10, output_file="output.mp3")

# Identificar a música no trecho baixado
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

result = loop.run_until_complete(identify_song("output.mp3"))

# Exibir o resultado
print(result)
