# Motion Graphics V3 — skill grátis para o Claude Code

Motion graphics feito por código, do roteiro ao MP4, no seu próprio computador. Você dá um assunto (uma história, uma
empresa, uma invenção, uma ideia) e o Claude monta o vídeo: narração, cada palavra caindo na tela no tempo da fala,
fotos reais recortadas, páginas de verdade com marca-texto, câmera que se mexe o tempo todo, transições e efeitos
sonoros.

Serve para vários tipos de motion e de vídeo: **Shorts (9:16)**, **vídeos longos (16:9)**, histórias, explicativos.
Você troca o assunto e as cores (mundos de papel, cinza, tinta, argila, céu…), e a skill monta o resto.

Ela saiu de vários vídeos que eu fiz no canal [@celticmatheus1](https://www.youtube.com/@celticmatheus1), e cada um
ensinou uma regra nova: o vídeo inteiro por código, o som e cada palavra no tempo da fala, e o método — estudar
referências quadro a quadro e **medir o próprio vídeo** (quadros parados, câmera, movimento) antes de entregar.

## O que você precisa
- [Claude Code](https://claude.com/claude-code)
- Node.js 22+ e ffmpeg
- ~1,5 GB livres (voz Kokoro, alinhamento de palavras e as ferramentas de análise rodam local, de graça)

## Como instalar (menos de 2 minutos + o download)
1. Baixe esta pasta (botão **Code → Download ZIP**) e coloque em `~/.claude/skills/motion-graphics-v3`
   (no Windows: `C:\Users\<você>\.claude\skills\motion-graphics-v3`).
2. Rode uma vez, no Git Bash ou no terminal:
   ```bash
   bash ~/.claude/skills/motion-graphics-v3/tools/setup.sh
   ```
   Ele instala as dependências, baixa o GSAP e gera os efeitos sonoros e as texturas **por código**.
3. Abra o Claude Code numa pasta vazia e peça, por exemplo:
   > Usa a skill motion graphics V3 e faz um Short de 45 s contando como nasceu a Nintendo.

## O que tem dentro
| pasta | o que é |
|---|---|
| `SKILL.md` | o método completo que o Claude segue (passo a passo, regras, checagens) |
| `NOTES.md` | regras aprendidas na prática (o que deu errado e como corrigir) |
| `reference/` | o estudo quadro a quadro das referências (só medidas e descrições, nenhum quadro de terceiros), os dispositivos visuais, o som e como achar imagens com licença |
| `kit/` | biblioteca de cenas (`v3lib.py`, `kit.js`, `kit.css`), fontes livres (OFL), texturas e efeitos sonoros gerados por código |
| `tools/` | voz, alinhamento palavra por palavra, mixagem, recorte de pessoas, medição de movimento (`motion_study.py`), geradores de som e textura |
| `example/` | o código de um filme de exemplo ("How Claude Was Born"); as fotos e vídeos dele não vêm junto |

## Dicas
- Todo número na tela fica legível por pelo menos 1 s; toda palavra falada aparece na tela.
- Peça para o Claude rodar `tools/motion_study.py` no render: a meta é **no máximo 30 % de quadros parados**.
- Toda imagem real usada no vídeo precisa de licença ou de uso justo; a skill anota cada fonte e licença.

## Créditos e licenças
- Skill, código e sons: Matheus ([@celticmatheus1](https://www.youtube.com/@celticmatheus1)) — licença MIT (`LICENSE`).
- Render: [HyperFrames](https://www.npmjs.com/package/hyperframes) (Apache-2.0) · animação: GSAP (licença "Standard
  No Charge", baixado pelo `setup.sh`, não vem no pacote) · voz: Kokoro (Apache-2.0).
- Fontes em `kit/fonts/`: Anton, Archivo Black, Herr Von Muellerhoff, Inter, Pinyon Script, Playfair Display, Space
  Grotesk e UnifrakturMaguntia — todas SIL Open Font License 1.1 (Google Fonts).
- O estilo foi estudado em reels públicos (Sharoz Media, Rida Visual, Rivinity, EarnEdits); aqui só ficam as
  medidas e descrições escritas, nenhum quadro, som ou imagem deles.
