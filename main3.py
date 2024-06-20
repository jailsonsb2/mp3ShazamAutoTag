import subprocess
import asyncio
import uuid
from shazamio import Shazam

# Função para gerar um nome de arquivo aleatório
def generate_random_filename(extension=".mp3"):
    return f"{uuid.uuid4()}{extension}"

# Função para baixar um trecho do áudio do stream e salvar como MP3
def download_audio_segment(stream_url, duration=10, output_file="output.mp3"):
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

async def main():
    # URL do stream
    stream_url = "https://stream.zeno.fm/yn65fsaurfhvv"

    # Gerar um nome de arquivo aleatório para o MP3
    output_file = generate_random_filename()

    # Baixar um trecho de 10 segundos do stream
    download_audio_segment(stream_url, duration=10, output_file=output_file)

    # Identificar a música no trecho baixado
    result = await identify_song(output_file)

    # Exibir o resultado formatado
    if 'track' in result:
        track = result['track']
        print(f"Title: {track['title']}")
        print(f"Artist: {track['subtitle']}")
        print(f"Album: {track.get('sections', [{}])[0].get('metadata', [{}])[0].get('text', 'N/A')}")
        print(f"Label: {track.get('sections', [{}])[0].get('metadata', [{}])[1].get('text', 'N/A')}")
        print(f"Released: {track.get('sections', [{}])[0].get('metadata', [{}])[2].get('text', 'N/A')}")
        print(f"Genre: {track.get('genres', {}).get('primary', 'N/A')}")
        print(f"Track URL: {track['url']}")
        print(f"Cover Art: {track['images']['coverart']}")
    else:
        print("Música não identificada.")

if __name__ == "__main__":
    asyncio.run(main())
