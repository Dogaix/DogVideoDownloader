import os
import re
import yt_dlp
from colorama import init, Fore, Style, Back

init(autoreset=True)
PATH = "./musicas"

def sucesso(msg):
    print(Fore.GREEN + Style.BRIGHT + "✔ " + msg)
def erro(msg):
    print(Fore.RED + Style.BRIGHT + "✖ " + msg)
def aviso(msg):
    print(Fore.YELLOW + Style.BRIGHT + "⚠ " + msg)
def info(msg):
    print(Fore.CYAN + "➜ " + msg)
def destaque(msg):
    print(Fore.WHITE + Back.BLUE + Style.BRIGHT + f" {msg} " + Style.RESET_ALL)
def linha():
    print(Fore.BLUE + "─" * 60)
def banner():
    print(Fore.GREEN + Style.BRIGHT)
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║  🐶  DOG VIDEO DOWNLOADER  🎵                             ║")
    print("╠═══════════════════════════════════════════════════════════╣")
    print(Fore.CYAN + "║" + Fore.WHITE + "  ✔  Download de vídeos em MP4" + Fore.CYAN + "                             ║")
    print(Fore.CYAN + "║" + Fore.WHITE + "  ✔  Download de músicas em MP3" + Fore.CYAN + "                            ║")
    print(Fore.CYAN + "║" + Fore.WHITE + "  ✔  Pesquisa automática no YouTube" + Fore.CYAN + "                        ║")
    print(Fore.CYAN + "║" + Fore.WHITE + "  ✔  Suporte para link ou nome da música" + Fore.CYAN + "                   ║")
    print(Fore.GREEN + "╚═══════════════════════════════════════════════════════════╝")
    print(Style.RESET_ALL)
def criar_pasta():
    if not os.path.exists(PATH):
        os.makedirs(PATH)
        sucesso(f"Pasta '{PATH}' criada com sucesso!")
def limpar_arquivos_anteriores():
    if os.path.exists(PATH):
        arquivos = [f for f in os.listdir(PATH) if os.path.isfile(os.path.join(PATH, f))]
        for arquivo in arquivos:
            os.remove(os.path.join(PATH, arquivo))
        sucesso(f"{len(arquivos)} arquivos anteriores foram deletados.")
def confirmar_limpeza():
    while True:
        resp = input(Fore.YELLOW + "Deseja deletar os arquivos anteriores? (S/N): " + Style.RESET_ALL).strip().lower()
        if resp in ['s', 'n']:
            return resp == 's'
        erro("Por favor, digite apenas S ou N.")
def escolher_formato():
    linha()
    print(Fore.WHITE + Style.BRIGHT + "O que deseja baixar?")
    print(Fore.CYAN + "   1) " + Fore.WHITE + "Vídeo (MP4)")
    print(Fore.CYAN + "   2) " + Fore.WHITE + "Áudio (MP3)")
    print(Fore.CYAN + "   3) " + Fore.WHITE + "Ambos (MP4 + MP3)")
    linha()
    while True:
        escolha = input(Fore.YELLOW + "Escolha (1/2/3): " + Style.RESET_ALL).strip()
        if escolha in ['1', '2', '3']:
            return escolha
        erro("Opção inválida. Escolha 1, 2 ou 3.")

class YouTubeDownloader:
    def __init__(self, caminho):
        self.caminho = caminho
    def baixar(self, url_ou_nome, formato):
        ydl_opts = {
            'outtmpl': os.path.join(self.caminho, '%(title)s.%(ext)s'),
            'ignoreerrors': True,
            'no_warnings': False,
            'quiet': False,
        }
        if formato == '1':  # Apenas vídeo
            ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            ydl_opts['merge_output_format'] = 'mp4'
            info("Baixando vídeo em MP4...")
        elif formato == '2':  # Apenas áudio
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
            info("Baixando áudio em MP3 (192kbps)...")
        elif formato == '3':  # Ambos
            info("Baixando vídeo + áudio separado...")
            self._baixar_video(url_ou_nome)
            self._baixar_audio(url_ou_nome)
            return
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url_ou_nome, download=True)
            return info_dict.get('title', 'Desconhecido')

    def _baixar_video(self, url):
        opts = {
            'outtmpl': os.path.join(self.caminho, '%(title)s [VIDEO].%(ext)s'),
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
    def _baixar_audio(self, url):
        opts = {
            'outtmpl': os.path.join(self.caminho, '%(title)s [AUDIO].%(ext)s'),
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
def buscar_link(nome):
    info("Procurando no YouTube...")
    busca_url = f"ytsearch:{nome}"

    with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
        try:
            resultado = ydl.extract_info(busca_url, download=False)

            if 'entries' in resultado and resultado['entries']:
                titulo_video = resultado['entries'][0].get('title', 'Sem título')
                info(f"Encontrado: {Fore.WHITE + Style.BRIGHT}{titulo_video}")
                return resultado['entries'][0]['webpage_url']
            else:
                erro("Nenhum vídeo encontrado.")
                return None

        except Exception as e:
            erro(f"Erro na busca: {e}")
            return None
def main():
    banner()  # Banner bonitin
    criar_pasta()

    if confirmar_limpeza():
        limpar_arquivos_anteriores()
    else:
        print("\n")
        aviso(" Continuando com os arquivos existentes...")
    linha()
    print("")
    entrada = input(
        Fore.YELLOW + Style.BRIGHT + 
        "➤ Digite o nome da música/vídeo ou o link do YouTube: " + 
        Style.RESET_ALL
    ).strip()

    formato     = escolher_formato()
    downloader  = YouTubeDownloader(PATH)
    padrao_link = re.compile(r'https?://(www\.)?(youtube\.com|youtu\.be)/')
   
    if padrao_link.search(entrada):
        url = entrada
        sucesso("Link detectado!")
    else:
        url = buscar_link(entrada)
        if not url:
            erro("Não foi possível encontrar o conteúdo.")
            return

    linha()
    destaque("🚀 INICIANDO DOWNLOAD...")
    linha()

    titulo_download = downloader.baixar(url, formato)

    print("\n" + "═" * 70)
    print(Fore.GREEN + Style.BRIGHT + " " * 18 + "✅ DOWNLOAD CONCLUÍDO COM SUCESSO! ✅")
    print("═" * 70 + "\n")
    print(Fore.WHITE + Style.BRIGHT + f"   📌 Título: {titulo_download}")
    print(Fore.CYAN + f"   📁 Pasta: {os.path.abspath(PATH)}")
    print(Fore.GREEN + f"   🎉 Arquivo(s) salvo(s) com sucesso!")
    print("═" * 70)

if __name__ == "__main__":
    main()