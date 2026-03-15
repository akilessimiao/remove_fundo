from flask import Flask, request, send_file, jsonify
import tempfile
import os
import gc
from werkzeug.utils import secure_filename
from rembg import new_session, remove
from moviepy.editor import VideoFileClip, ColorClip, CompositeVideoClip, ImageClip
from PIL import Image
import numpy as np
import traceback

app = Flask(__name__)

@app.route('/')
def index():
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Arquivo index.html não encontrado no servidor", 500

@app.route('/process', methods=['POST'])
def process():
    try:
        if 'video' not in request.files or not request.files['video'].filename:
            return jsonify({"error": "Nenhum vídeo válido enviado"}), 400

        video_file = request.files['video']
        model_name = request.form.get('model', 'u2net_human_seg')
        bg_type = request.form.get('bg_type', 'transparente')
        bg_color_hex = request.form.get('bg_color', '#ffffff')

        with tempfile.TemporaryDirectory() as tmp:
            input_path = os.path.join(tmp, 'input.mp4')
            video_file.save(input_path)

            # Carrega vídeo com baixa resolução se possível para teste
            clip = VideoFileClip(input_path)

            # Cria sessão do modelo uma vez só
            session = new_session(model_name)

            def process_frame(frame):
                pil_img = Image.fromarray(frame)
                output = remove(pil_img, session=session, alpha_matting=True, alpha_matting_foreground_threshold=240)
                return np.array(output)

            processed_clip = clip.fl_image(process_frame)

            # Fundo
            if bg_type == 'custom-image' and 'bg_image' in request.files and request.files['bg_image'].filename:
                bg_file = request.files['bg_image']
                bg_path = os.path.join(tmp, 'bg.jpg')
                bg_file.save(bg_path)
                bg_clip = ImageClip(bg_path).set_duration(clip.duration).resize(height=clip.h)
                final = CompositeVideoClip([bg_clip, processed_clip.set_position("center")])
                out_ext = 'mp4'
            elif bg_type == 'transparente':
                final = processed_clip
                out_ext = 'mov'
            else:
                if bg_type == 'branco':
                    color = (255, 255, 255)
                elif bg_type == 'preto':
                    color = (0, 0, 0)
                else:
                    hex_c = bg_color_hex.lstrip('#')
                    color = tuple(int(hex_c[i:i+2], 16) for i in (0, 2, 4))
                bg_clip = ColorClip(size=clip.size, color=color, duration=clip.duration)
                final = CompositeVideoClip([bg_clip, processed_clip.set_position("center")])
                out_ext = 'mp4'

            out_path = os.path.join(tmp, f'output.{out_ext}')

            # Parâmetros otimizados para free tier (menos memória e mais rápido)
            write_params = {
                'codec': 'libx264' if out_ext == 'mp4' else 'png',  # png para alpha em mov
                'audio_codec': 'aac',
                'fps': clip.fps,
                'preset': 'ultrafast',
                'threads': 1,
                'logger': None,
                'bitrate': '1000k'  # Reduz tamanho/qualidade para economizar RAM
            }

            final.write_videofile(out_path, **write_params)

            # Libera tudo imediatamente
            clip.close()
            processed_clip.close()
            if 'final' in locals():
                final.close()
            gc.collect()

            return send_file(out_path, as_attachment=True, download_name=f'video_sem_fundo.{out_ext}')

    except Exception as e:
        error_msg = traceback.format_exc()
        print("ERRO NO PROCESSAMENTO:", error_msg)  # Aparece nos logs do Render
        return jsonify({"error": f"Erro interno: {str(e)}. Verifique se o vídeo é curto (<15s)."}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
