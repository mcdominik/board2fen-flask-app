from flask import Flask, render_template, send_from_directory, url_for, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_uploads import UploadSet, IMAGES, configure_uploads 
from wtforms import SubmitField
from board_to_fen.predict import get_fen_from_image_path
import secrets
import os
from random import randint
import pathlib


app = Flask(__name__)
app.config["SECRET_KEY"] = str(secrets.SystemRandom().getrandbits(128))
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


class UploadFrom(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'only images are allowed'),
            FileRequired('file field should not be empty')  ,
        ],    
    )
    submit = SubmitField('Get FEN')

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

@app.route('/', methods=['GET','POST'])
def get_fen():
    for file in os.listdir('uploads'):
        os.remove(f'uploads/{file}') 
    form = UploadFrom()
    fen = ''
    if form.is_submitted():
        filename = photos.save(request.files["photo"], name=f'{str(randint(0,1000000))}.png')
        file_url = url_for('get_file', filename=filename)
        path = f'./uploads/{filename}'
        if request.form.get("invert", False) == 'on':
            fen = get_fen_from_image_path(path, black_view=True)
            print(f'fen [black view]: {fen}')     
        else:
            fen = get_fen_from_image_path(path)
            print(f'fen: {fen}')
    else:
        file_url = None  
    return render_template('index.html', form=form, file_url=file_url, fen=fen)


@app.route('/full', methods=['GET','POST'])
def get_full_fen():
    for file in os.listdir('uploads'):
        os.remove(f'uploads/{file}') 
    form = UploadFrom()
    fen = ''
    if form.is_submitted():
        filename = photos.save(request.files["photo"], name=f'{str(randint(0,1000000))}.png')
        file_url = url_for('get_file', filename=filename)
        path = f'./uploads/{filename}'
        fen = get_fen_from_image_path(path)
        print(f'fen: {fen}')
    else:
        file_url = None
    full_fen = squeeze_front_data(fen)
    return render_template('full.html', form=form, file_url=file_url, fen=full_fen)

def squeeze_front_data(fen):
    can_castle = ''
    next_move = ''
    next_move_white = request.form.get("next-move-white", False)
    next_move_black = request.form.get("next-move-black", False)
    castle_white_short = request.form.get("castle-white-short", False)
    castle_white_long = request.form.get("castle-white-long", False)
    castle_black_short = request.form.get("castle-black-short", False)
    castle_black_long = request.form.get("castle-black-long", False)
    full_move_number = request.form.get("full-move-number", False)
    half_move_number = request.form.get("half-move-number", False)
    en_passant = request.form.get("en-passant", False)
    if next_move_white == '' and next_move_black == False:
        next_move = 'w'
    elif next_move_black == '' and next_move_white == False:
        next_move = 'b'
    else:
        next_move = '?'
    if castle_white_short == '':
        can_castle+='K'
    else:
        can_castle+='-'
    if castle_white_long == '':
        can_castle+='Q'
    else:
        can_castle+='-'
    if castle_black_short == '':
        can_castle+='k'
    else:
        can_castle+='-'
    if castle_black_long == '':
        can_castle+='q'
    else:
        can_castle+='-'
    if en_passant == '':
        en_passant+='-'
    if half_move_number == '':
        half_move_number = '?'
    if full_move_number == '':
        full_move_number = '?'   
    full_fen = f'{fen} {next_move} {can_castle} {en_passant} {half_move_number} {full_move_number}'
    return full_fen
  

if __name__ == '__main__':
    pathlib.Path('uploads').mkdir(exist_ok=True) 
    # run production
    app.run(host='::',port=2137)

    #run development
    # app.run(debug=True)

