🎹 AUTO MIDI CONVERTER v2.0 - Edição Linux Mint
Transforma vídeos do YouTube em arquivos MIDI de alta qualidade automaticamente!

Este projeto foi preparado para rodar perfeitamente no Linux Mint 22. Ele baixa o vídeo, converte o áudio e usa Inteligência Artificial para transcrever as notas do piano.

✨ O Que Ele Faz?
-Baixa vídeos do YouTube (ex: tutoriais de piano, Synthesia)
-Extrai o áudio em MP3
-Transcreve para MIDI usando IA (ByteDance Piano Transcription)
-Organiza tudo na pasta ~/ProjetosMidi

🚀 Instalação Rápida (Linux Mint 22)
Abra o Terminal (Ctrl+Alt+T) e rode estes 3 comandos, um por vez:

1) Instalar dependências do sistema 
sudo apt update 
sudo apt install ffmpeg yt-dlp python3-pip git -y

2) Instalar a Inteligência Artificial 
pip install piano_transcription_inference librosa

3) Baixar este projeto 

git clone https://github.com/camathias/auto-midi-converter.git 

cd auto-midi-converter

🎹 Como Usar Entre na pasta do projeto (se já não estiver): 
cd auto-midi-converter

Execute o conversor: 
python3 auto_midi_converter.py

Cole o link do YouTube quando pedir.

Dica: Use vídeos do tipo "Piano Tutorial" ou "Synthesia" para melhores resultados.

Aguarde! (A transcrição pode levar de 2 a 10 minutos dependendo do seu computador).

📂 Seu arquivo MIDI estará em: ~/ProjetosMidi/downloads/

🛠️ Solução de Problemas
Se algo der errado, rode nosso script de verificação: 
bash test_dependencies.sh

Ele vai te dizer exatamente o que está faltando instalar!

📝 Licença Este projeto usa a PolyForm Noncommercial License 1.0.0.

✅ Você PODE: Estudar, modificar e usar para projetos pessoais. 
❌ Você NÃO PODE: Vender ou usar para fins comerciais.

Desenvolvido para fins educacionais.
