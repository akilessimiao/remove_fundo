
# Tanque Digital 🎸✨

**Remova o fundo de vídeos automaticamente com IA** – ideal para clipes de baixista, performances musicais, TikTok ou qualquer conteúdo com pessoa em movimento.

Interface web moderna (dark mode neon) + processamento 100% local via rembg + moviepy.  
Funciona offline no seu PC ou deploy grátis no Render.com.

![Demo Screenshot](https://via.placeholder.com/800x450/1a1a2e/70d0ff?text=Tanque+Digital+Demo)  
*(Substitua por screenshot real do app rodando)*

## Funcionalidades

- Upload de vídeo (MP4, etc.)
- Vários modelos de IA para remoção de fundo (melhor para humanos: `u2net_human_seg`, `birefnet-portrait`, `isnet-general-use`)
- Opções de fundo:
  - Transparente (exporta .mov com canal alpha)
  - Branco puro
  - Preto puro
  - Cor estática personalizada (color picker)
  - Upload de imagem de fundo (JPEG/PNG)
- Barra de progresso animada
- Download direto do vídeo processado
- Interface tech/neon inspirada em apps digitais modernos (Natal/RN vibe 2026)

## Tecnologias

- **Frontend**: HTML + CSS (dark mode gradiente) + JavaScript vanilla
- **Backend**: Flask (Python)
- **IA de remoção de fundo**: [rembg](https://github.com/danielgatis/rembg) (U²-Net, IS-Net, BiRefNet...)
- **Processamento de vídeo**: [moviepy](https://zulko.github.io/moviepy/)
- **Deploy grátis**: Render.com (free tier)

## Como rodar localmente

### Pré-requisitos
- Python 3.9+
- FFmpeg instalado (necessário para moviepy)
  - Windows: baixe em https://ffmpeg.org/download.html
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt install ffmpeg`

### Passos

1. Clone o repositório
   ```bash
   git clone https://github.com/SEU_USUARIO/tanque-digital.git
   cd tanque-digital
   ```

2. Crie ambiente virtual (recomendado)
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```

3. Instale dependências
   ```bash
   pip install -r requirements.txt
   ```

4. Rode o app
   ```bash
   python app.py
   ```

5. Abra no navegador: http://127.0.0.1:5000

## Deploy grátis no Render.com (recomendado)

1. Crie conta grátis em https://render.com (use login com GitHub)
2. No dashboard → New → Web Service
3. Conecte seu repositório GitHub
4. Configure:
   - **Name**: tanque-digital
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free
5. Clique em **Create Web Service**
6. Aguarde 3–5 minutos → seu app estará em https://tanque-digital.onrender.com (ou nome que escolheu)

**Dica**: No free tier, o app "dorme" após 15 min de inatividade → acorda em ~20 segundos na próxima visita.

## Modelos de IA recomendados

| Modelo                  | Melhor para                  | Velocidade | Precisão em pessoas/instrumentos |
|-------------------------|------------------------------|------------|----------------------------------|
| u2net_human_seg         | Pessoas + instrumentos       | Média      | ⭐⭐⭐⭐⭐                           |
| birefnet-portrait       | Performances / retratos      | Média-Alta | ⭐⭐⭐⭐⭐                           |
| isnet-general-use       | Uso geral preciso (2025+)    | Média      | ⭐⭐⭐⭐                            |
| u2net                   | Equilíbrio clássico          | Média      | ⭐⭐⭐⭐                            |
| silueta / u2netp        | Rápido / leve                | Rápida     | ⭐⭐⭐                             |

Recomendação para baixista: comece com **u2net_human_seg** ou **birefnet-portrait**.

## Limitações conhecidas

- Vídeos longos (>1 min) podem demorar muito no free tier ou PC sem GPU
- Bordas em movimentos rápidos (mãos no baixo) podem precisar de refinamento manual depois
- Não suporta vídeos muito grandes (limite prático ~100 MB)

## Contribuições

Sinta-se à vontade para abrir issues ou pull requests!  
Ideias bem-vindas: GPU support (onnxruntime-gpu), mais modelos, preview do vídeo, etc.

## Licença

MIT License – use como quiser, mas mantenha o crédito ao Tanque Digital se possível 😉

Feito em Natal/RN com 💙 e IA  
LDT NET • 2026

```

### Como melhorar ainda mais (opcional)

1. Adicione um screenshot real:
   - Abra o app → tire print da tela → suba como `demo.png` no repo
   - Atualize a linha `![Demo Screenshot](demo.png)`

2. Adicione badge do Render:
   - Após deploy, pegue o badge no Render e adicione no topo:
     ```markdown
     [![Deployed on Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)
     ```

3. Crie seção "Demo Online":
   ```markdown
   ## Demo Online
   Teste agora: https://tanque-digital.onrender.com
   ```

Pronto!  🚀
