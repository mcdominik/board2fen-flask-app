from flask import Flask, render_template, send_from_directory, url_for, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_uploads import UploadSet, IMAGES, configure_uploads 
from wtforms import SubmitField
from board_to_fen.predict import get_fen_from_image
import secrets
import os
from random import randint


app = Flask(__name__)
app.config["SECRET_KEY"] = str(secrets.SystemRandom().getrandbits(128))
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


class UploadFrom(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos,'only images are allowed'),
            FileRequired('file field should not be empty')  ,
        ],    
    )
    submit = SubmitField('Get FEN')


@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)


next_move = ''
can_castle =''
@app.route('/', methods=['GET','POST'])
def get_fen():
    for file in os.listdir('uploads'):
        os.remove(f'uploads/{file}') 
    form = UploadFrom()
    fen = ''
    if form.is_submitted():
        filename = photos.save(request.files["photo"], name=f'{str(randint(0,1000000))}.png')
        print(filename)
        file_url = url_for('get_file', filename=filename)
        path = f'./uploads/{filename}'
        fen = get_fen_from_image(path)
        print(f'fen: {fen}')
    else:
        file_url = None  
    return render_template('index.html', form=form, file_url=file_url, fen=fen)


@app.route('/full', methods=['GET','POST'])
def get_full_fen():
    form = UploadFrom()
    # print(f'photos path: {photos.path}')
    # # print(f'moj log: {photos.save(request.files["photo"])}')
    # filename = photos.save(request.files["photo"])
    # print(f'filename: {filename}')


    #     # filename = photos.save(form.photo.data)
    # file_url = url_for('get_file', filename=filename)
    # print(f'file url to: {file_url}')
    # return render_template('index.html', form=form, file_url=file_url)
    fen = ''
    if form.is_submitted():
        filename = photos.save(request.files["photo"])

        # filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)
        path = f'./uploads/{filename}'
        fen = get_fen_from_image(path)
        print(f'fen: {fen}')
    else:
        file_url = None
    

    next_move_white = request.form.get("next-move-white", False)
    next_move_black = request.form.get("next-move-black", False)
    castle_white_short = request.form.get("castle-white-short", False)
    castle_white_long = request.form.get("castle-white-long", False)
    castle_black_short = request.form.get("castle-black-short", False)
    castle_black_long = request.form.get("castle-black-long", False)
    full_move_number = request.form.get("full-move-number", False)
    half_move_number = request.form.get("half-move-number", False)
    en_passant = request.form.get("en-passant", False)
    global next_move
    if next_move_white == '' and next_move_black == False:
        next_move = 'w'
    if next_move_black == '' and next_move_white == False:
        next_move = 'b'

    global can_castle
    if castle_white_short == '':
        can_castle+='K'
    if castle_white_short == False:
        can_castle+='-'
    if castle_white_long == '':
        can_castle+='Q'
    if castle_white_long == False:
        can_castle+='-'
    if castle_black_short == '':
        can_castle+='k'
    if castle_black_short == False:
        can_castle+='-'
    if castle_black_long == '':
        can_castle+='q'
    if castle_black_long == False:
        can_castle+='-'

    if en_passant == '':
        en_passant+='-'
    fen = f'{fen} {next_move} {can_castle} {en_passant} {half_move_number} {full_move_number}'
    print(fen)

    # next_w = request.form['next-move-white']
    print(f'en pass:{en_passant}')
    print(f'next black:{next_move_black}')
    print(f'next white:{next_move_white}')
    print(f'castle white L:{castle_white_short}')
    print(f'castle white S:{castle_white_long}')
    print(f'castle black L:{castle_black_short}')
    print(f'castle black S:{castle_black_long}')
    print(f'half move:{half_move_number}')
    print(f'full move:{full_move_number}')

    # print(f'next w:{next_w}')
    return render_template('full.html', form=form, file_url=file_url, fen=fen)


if __name__ == '__main__':
    app.run(debug=True)
