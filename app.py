from flask import Flask, request, send_file
import tempfile
import os
from werkzeug.utils import secure_filename
from rembg import new_session, remove
from moviepy.editor import VideoFileClip, ColorClip, CompositeVideoClip, ImageClip
from PIL import Image
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return open('index.html', 'r', encoding='utf-8').read()

@app.route('/process', methods=['POST'])
def process():
    if 'video' not in request.files:
        return "Nenhum vídeo enviado", 400

    video_file = request.files['video']
    model_name = request.form['model']
    bg_type = request.form.get('bg_type', 'transparente')
    bg_color_hex = request.form.get('bg_color', '#ffffff')

    with tempfile.TemporaryDirectory() as tmp:
        input_path = os.path.join(tmp, 'input.mp4')
        video_file.save(input_path)

        clip = VideoFileClip(input_path)
        session = new_session(model_name)

        def process_frame(frame):
            pil_img = Image.fromarray(frame)
            output = remove(pil_img, session=session)
            return np.array(output)

        processed_clip = clip.fl_image(process_frame)

        if bg_type == 'custom-image' and 'bg_image' in request.files and request.files['bg_image'].filename:
            bg_file = request.files['bg_image']
            bg_path = os.path.join(tmp, 'bg.' + bg_file.filename.rsplit('.', 1)[-1])
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

        if out_ext == 'mov':
            final.write_videofile(out_path, codec='prores_ks', audio_codec='aac', fps=clip.fps, preset='medium')
        else:
            final.write_videofile(out_path, codec='libx264', audio_codec='aac', fps=clip.fps, preset='medium')

        return send_file(out_path, as_attachment=True, download_name=f'video_tanque_digital.{out_ext}')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
