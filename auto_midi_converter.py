**Descrição:** O cérebro do projeto. É o código Python que faz a mágica.
**Instrução:** Clique em "Add file" > "Create new file" > Nomeie como `auto_midi_converter.py` > Cole o conteúdo abaixo:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎹 AUTO MIDI CONVERTER v2.0 - MINT EDITION
Transforma um link do YouTube em MIDI de alta qualidade.
Automatiza: Download + Conversão MP3 + Transcrição MIDI

Compatível com Linux Mint 22 (Ubuntu 24.04 base)
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Cores para o terminal ficar legal
class Cores:
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    AZUL = '\033[94m'
    CIANO = '\033[96m'
    RESET = '\033[0m'
    NEGRITO = '\033[1m'
    FUNDO_AZUL = '\033[44m'

def imprimir(msg, tipo="info"):
    """Imprime mensagens coloridas no terminal"""
    if tipo == "sucesso":
        print(f"{Cores.VERDE}✅ {msg}{Cores.RESET}")
    elif tipo == "erro":
        print(f"{Cores.VERMELHO}❌ {msg}{Cores.RESET}")
    elif tipo == "aviso":
        print(f"{Cores.AMARELO}⚠️  {msg}{Cores.RESET}")
    elif tipo == "info":
        print(f"{Cores.AZUL}ℹ️  {msg}{Cores.RESET}")
    elif tipo == "titulo":
        print(f"\n{Cores.NEGRITO}{Cores.CIANO}{'='*70}{Cores.RESET}")
        print(f"{Cores.NEGRITO}{Cores.CIANO}🎹  {msg}{Cores.RESET}")
        print(f"{Cores.NEGRITO}{Cores.CIANO}{'='*70}{Cores.RESET}\n")
    elif tipo == "etapa":
        print(f"\n{Cores.NEGRITO}{Cores.FUNDO_AZUL} ▶️  {msg}{Cores.RESET}\n")

def verificar_dependencias():
    """Verifica se as ferramentas necessárias estão instaladas"""
    imprimir("Verificando ferramentas necessárias...", "info")
    print()
    
    ferramentas = {
        "yt-dlp": "yt-dlp --version",
        "ffmpeg": "ffmpeg -version",
        "librosa": "python3 -c 'import librosa'",
        "piano_transcription_inference": "python3 -c 'from piano_transcription_inference import PianoTranscription'"
    }
    
    faltam = []
    
    for nome, comando in ferramentas.items():
        try:
            subprocess.run(comando, shell=True, capture_output=True, timeout=5, check=True)
            imprimir(f"{nome}: ✓ Instalado", "sucesso")
        except:
            imprimir(f"{nome}: ✗ NÃO ENCONTRADO", "erro")
            faltam.append(nome)
    
    if faltam:
        print()
        imprimir("Faltam instalar algumas dependências:", "aviso")
        print("\nExecute estes comandos no terminal:\n")
        print(f"{Cores.NEGRITO}sudo apt update{Cores.RESET}")
        print(f"{Cores.NEGRITO}sudo apt install ffmpeg yt-dlp python3-pip -y{Cores.RESET}")
        print(f"{Cores.NEGRITO}pip install piano_transcription_inference librosa{Cores.RESET}\n")
        return False
    
    print()
    imprimir("Todas as ferramentas estão prontas!", "sucesso")
    return True

def baixar_youtube(url_youtube, pasta_trabalho):
    """Baixa o vídeo do YouTube usando yt-dlp"""
    imprimir("Conectando ao YouTube e baixando o vídeo...", "etapa")
    
    # Sanitiza a pasta
    pasta_trabalho = Path(pasta_trabalho)
    pasta_trabalho.mkdir(parents=True, exist_ok=True)
    
    # Template de nome para o yt-dlp
    template_saida = str(pasta_trabalho / "%(title)s.%(ext)s")
    
    cmd = [
        "yt-dlp",
        "-f", "best[ext=mp4]/best",
        "-o", template_saida,
        "--quiet",
        "--progress",
        url_youtube
    ]
    
    try:
        print(f"  Rodando: {' '.join(cmd[:3])} [URL]\n")
        resultado = subprocess.run(cmd, capture_output=False, text=True, timeout=900)
        
        if resultado.returncode != 0:
            imprimir("Erro ao baixar do YouTube", "erro")
            return None
        
        # Encontra o arquivo baixado
        arquivos = list(pasta_trabalho.glob("*"))
        videos = [f for f in arquivos if f.suffix.lower() in ['.mp4', '.webm', '.mkv', '.mov', '.flv']]
        
        if videos:
            arquivo_video = sorted(videos, key=lambda p: p.stat().st_mtime, reverse=True)[0]
            tamanho_mb = arquivo_video.stat().st_size / (1024 * 1024)
            imprimir(f"✓ Vídeo baixado: {arquivo_video.name} ({tamanho_mb:.1f} MB)", "sucesso")
            return str(arquivo_video)
        else:
            imprimir("Arquivo de vídeo não encontrado após download", "erro")
            return None
            
    except subprocess.TimeoutExpired:
        imprimir("Timeout: Vídeo muito grande ou conexão lenta demais", "erro")
        return None
    except KeyboardInterrupt:
        imprimir("Download cancelado pelo usuário", "aviso")
        return None
    except Exception as e:
        imprimir(f"Erro inesperado: {str(e)}", "erro")
        return None

def converter_para_mp3(arquivo_video, pasta_trabalho):
    """Converte o vídeo para MP3 usando FFmpeg"""
    imprimir("Extraindo áudio e convertendo para MP3...", "etapa")
    
    nome_base = Path(arquivo_video).stem
    arquivo_mp3 = Path(pasta_trabalho) / f"{nome_base}.mp3"
    
    cmd = [
        "ffmpeg",
        "-i", arquivo_video,
        "-vn",
        "-acodec", "libmp3lame",
        "-q:a", "2",
        "-progress", "pipe:1",
        "-loglevel", "quiet",
        "-y",
        str(arquivo_mp3)
    ]
    
    try:
        print(f"  Processando áudio: {Path(arquivo_video).name}\n")
        resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        
        if resultado.returncode != 0 or not arquivo_mp3.exists():
            imprimir(f"Erro ao converter: {resultado.stderr[:200]}", "erro")
            return None
        
        tamanho_mb = arquivo_mp3.stat().st_size / (1024 * 1024)
        imprimir(f"✓ MP3 criado: {arquivo_mp3.name} ({tamanho_mb:.1f} MB)", "sucesso")
        return str(arquivo_mp3)
        
    except subprocess.TimeoutExpired:
        imprimir("Timeout na conversão (arquivo muito grande)", "erro")
        return None
    except KeyboardInterrupt:
        imprimir("Conversão cancelada", "aviso")
        return None
    except Exception as e:
        imprimir(f"Erro inesperado: {str(e)}", "erro")
        return None

def gerar_midi(arquivo_mp3, pasta_trabalho):
    """Transcreve o MP3 para MIDI usando modelo ByteDance (Piano Transcription)"""
    imprimir("Iniciando transcrição com IA (ByteDance Piano Transcription)...", "etapa")
    imprimir("⏱️  AVISO: Isso pode levar 2-10 minutos (dependendo do tamanho)", "aviso")
    imprimir("Processador estará em uso total. Seja paciente! ☕", "info")
    print()
    
    # Importa aqui para não dar erro se não estiver instalado
    try:
        import librosa
        from piano_transcription_inference import PianoTranscription, sample_rate
        print()
    except ImportError as e:
        imprimir(f"Bibliotecas Python não encontradas: {str(e)}", "erro")
        return None
    
    nome_base = Path(arquivo_mp3).stem
    arquivo_midi = Path(pasta_trabalho) / f"{nome_base}.mid"
    
    try:
        # Carrega o áudio
        print("  [1/3] Carregando arquivo de áudio...")
        audio, _ = librosa.load(arquivo_mp3, sr=sample_rate, mono=True)
        print(f"  ✓ Áudio carregado: {len(audio)} samples")
        
        # Inicia a transcrição
        print("  [2/3] Inicializando modelo de IA (ByteDance)...")
        transcriptor = PianoTranscription(device='cpu')
        print("  ✓ Modelo carregado. Processando...")
        
        # Transcreve (passa para o MIDI)
        print("  [3/3] Transcrevendo para MIDI (aguarde)...\n")
        transcriptor.transcribe(audio, str(arquivo_midi))
        
        tamanho_kb = arquivo_midi.stat().st_size / 1024
        imprimir(f"✓ MIDI gerado: {arquivo_midi.name} ({tamanho_kb:.1f} KB)", "sucesso")
        return str(arquivo_midi)
        
    except Exception as e:
        imprimir(f"Erro na transcrição: {str(e)}", "erro")
        return None

def limpar_arquivos_temporarios(pasta_trabalho, manter_midi=True):
    """Remove arquivos temporários para economizar espaço"""
    imprimir("Limpando arquivos temporários...", "info")
    
    try:
        removidos = 0
        for arquivo in Path(pasta_trabalho).glob("*"):
            if manter_midi and arquivo.suffix.lower() == ".mid":
                continue
            if arquivo.suffix.lower() in [".mp4", ".webm", ".mkv", ".mov", ".mp3", ".flv"]:
                arquivo.unlink()
                print(f"  • Removido: {arquivo.name}")
                removidos += 1
        
        if removidos > 0:
            imprimir(f"✓ Limpeza concluída ({removidos} arquivos removidos)", "sucesso")
    except Exception as e:
        imprimir(f"Erro ao limpar: {str(e)}", "aviso")

def main():
    """Função principal"""
    try:
        # Cabeçalho
        imprimir("AUTO MIDI CONVERTER v2.0 - YouTube → MIDI", "titulo")
        
        # Valida dependências
        if not verificar_dependencias():
            imprimir("\nInstale as dependências listadas acima e tente novamente!", "erro")
            sys.exit(1)
        
        # Pede o link
        print("\n" + "="*70)
        print("Cole o link do YouTube (ex: https://www.youtube.com/watch?v=...)")
        print("Dica: Use vídeos 'Piano Tutorial' ou 'Synthesia' para melhor qualidade")
        print("="*70)
        print()
        url = input(f"{Cores.NEGRITO}🔗 Link do YouTube: {Cores.RESET}").strip()
        
        if not url:
            imprimir("Link vazio! Encerrando.", "erro")
            sys.exit(1)
        
        # Valida URL
        if "youtube.com" not in url and "youtu.be" not in url:
            imprimir("URL não parece ser um link do YouTube válido!", "erro")
            sys.exit(1)
        
        # Cria pasta de trabalho
        pasta_trabalho = Path.home() / "ProjetosMidi" / "downloads"
        pasta_trabalho.mkdir(parents=True, exist_ok=True)
        
        imprimir(f"Pasta de trabalho: {pasta_trabalho}", "info")
        print()
        
        inicio = time.time()
        
        try:
            # PASSO 1: Baixar
            arquivo_video = baixar_youtube(url, str(pasta_trabalho))
            if not arquivo_video:
                raise Exception("Falha ao baixar do YouTube")
            
            time.sleep(1)
            
            # PASSO 2: Converter para MP3
            arquivo_mp3 = converter_para_mp3(arquivo_video, str(pasta_trabalho))
            if not arquivo_mp3:
                raise Exception("Falha na conversão para MP3")
            
            time.sleep(1)
            
            # PASSO 3: Gerar MIDI
            arquivo_midi = gerar_midi(arquivo_mp3, str(pasta_trabalho))
            if not arquivo_midi:
                raise Exception("Falha na transcrição MIDI")
            
            print()
            
            # Limpeza opcional
            print("Deseja remover os arquivos temporários (vídeo e MP3)?")
            print("(Isso economiza espaço, mantendo apenas o MIDI)")
            resposta = input(f"{Cores.NEGRITO}Digite 's' para sim ou 'n' para não: {Cores.RESET}").strip().lower()
            if resposta == 's':
                limpar_arquivos_temporarios(str(pasta_trabalho), manter_midi=True)
            
            # Resumo final
            tempo_total = time.time() - inicio
            minutos = int(tempo_total // 60)
            segundos = int(tempo_total % 60)
            
            print()
            imprimir("🎉 SUCESSO! TUDO PRONTO! 🎉", "titulo")
            print(f"{Cores.VERDE}✅ Arquivo MIDI criado com sucesso!{Cores.RESET}\n")
            print(f"📁 Localização: {Cores.NEGRITO}{arquivo_midi}{Cores.RESET}\n")
            print(f"⏱️  Tempo total: {minutos}m {segundos}s\n")
            print("📖 Próximas ações:")
            print("  1. Abra o arquivo em MuseScore para ver a partitura")
            print("  2. Use em Reaper para editar")
            print("  3. Importe em Synthesia para aprender a tocar\n")
            print(f"{Cores.CIANO}Obrigado por usar Auto MIDI Converter! 🎹{Cores.RESET}\n")
            
        except Exception as e:
            imprimir(f"Erro fatal: {str(e)}", "erro")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print()
        imprimir("Operação cancelada pelo usuário", "aviso")
        sys.exit(0)
    except Exception as e:
        print()
        imprimir(f"Erro inesperado: {str(e)}", "erro")
        sys.exit(1)

if __name__ == "__main__":
    main()
