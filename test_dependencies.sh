#!/bin/bash
# Verificador de Dependências para Linux Mint 22

echo "🔍 Verificando se seu sistema está pronto..."
echo "-------------------------------------------"

ERROS=0

# Função para verificar comando
check_cmd() {
    if command -v $1 &> /dev/null; then
        echo -e "✅ $1: INSTALADO"
    else
        echo -e "❌ $1: FALTANDO"
        ERROS=$((ERROS+1))
    fi
}

# Verifica ferramentas do sistema
check_cmd "ffmpeg"
check_cmd "yt-dlp"
check_cmd "python3"

# Verifica bibliotecas Python
echo -n "🔍 Verificando bibliotecas Python... "
if python3 -c "import librosa, piano_transcription_inference" 2>/dev/null; then
    echo -e "✅ TUDO OK"
else
    echo -e "❌ FALTANDO (librosa ou piano_transcription)"
    ERROS=$((ERROS+1))
fi

echo "-------------------------------------------"
if [ $ERROS -eq 0 ]; then
    echo "🎉 PARABÉNS! Seu computador está pronto."
    echo "Rode: python3 auto_midi_converter.py"
else
    echo "⚠️  ATENÇÃO: Faltam instalar coisas."
    echo "Rode: sudo apt install ffmpeg yt-dlp python3-pip -y"
    echo "E depois: pip install piano_transcription_inference librosa"
fi
