import subprocess
import asyncio
import uuid
from shazamio import Shazam
import tqdm

# Função para gerar um nome de arquivo aleatório
def generate_random_filename(extension=".mp3"):
    return f"{uuid.uuid4()}{extension}"

# Função para baixar um trecho do áudio do stream e salvar como MP3
def download_audio_segment(stream_url, duration=20, output_file="output.mp3"):
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

async def get_related_tracks(track_id):
    shazam = Shazam()
    related = await shazam.related_tracks(track_id=track_id, limit=5)
    return related

async def main():
    # URL do stream
    stream_url = "https://stream.zeno.fm/yn65fsaurfhvv"

    # Gerar um nome de arquivo aleatório para o MP3
    output_file = generate_random_filename()

    # Baixar um trecho de 10 segundos do stream
    download_audio_segment(stream_url, duration=20, output_file=output_file)

    try:
        result = await identify_song(output_file)

        if 'track' in result:
            track = result['track']
            print(f"Id: {track['key']}")
            print(f"Title: {track['title']}")
            print(f"Artist: {track['subtitle']}")
            print(f"Album: {track.get('sections', [{}])[0].get('metadata', [{}])[0].get('text', 'N/A')}")
            print(f"Label: {track.get('sections', [{}])[0].get('metadata', [{}])[1].get('text', 'N/A')}")
            print(f"Released: {track.get('sections', [{}])[0].get('metadata', [{}])[2].get('text', 'N/A')}")
            print(f"Genre: {track.get('genres', {}).get('primary', 'N/A')}")
            print(f"Track URL: {track['url']}")
            print(f"Cover Art: {track['images']['coverart']}")

            # Obter e exibir músicas relacionadas
            related_tracks_data = await get_related_tracks(track['key'])

            if related_tracks_data and 'tracks' in related_tracks_data:  # Verifica se há músicas relacionadas
                related_tracks = related_tracks_data['tracks']  # Acesse a lista de faixas

                if related_tracks:  # Verifica se a lista não está vazia
                    print("\nMúsicas Relacionadas:")
                    for related_track in related_tracks:
                        print(f"- {related_track['title']} por {related_track['subtitle']}")
                else:
                    print("Nenhuma música relacionada encontrada.")
            else:
                print("A resposta da API não contém músicas relacionadas.")
        else:
            print("Música não identificada. Tente um trecho mais longo ou outro momento do stream.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    asyncio.run(main())
