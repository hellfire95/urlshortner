from flask import  render_template, request, redirect, url_for, flash, abort, session,jsonify, Blueprint
import json
import os
from werkzeug.utils import secure_filename

bp = Blueprint('urlshort',__name__)

@bp.route('/')
def home():
    return render_template('home.html', codes=session.keys())

@bp.route('/your-url', methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        urls={}
        # let's check if we alredy have a short name for the site 
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)
        if request.form['code'] in urls.keys():
            flash('That short name has already been taken. Please select another naem.')
            return redirect(url_for('urlshort.home'))

        if 'url' in request.form.keys():
            urls[request.form['code']]={'url':request.form['url']}# if there is url then take url 
        else: # else for file is uploading, first we need to save the file and then save it in the url dictionary
            f= request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('/Users/arunattri/Desktop/url-shortner/urlshort/static/user_files/'+full_name)
            urls[request.form['code']]={'file':full_name}

        # urls[request.form['code']]={'url':request.form['url']} # we have a dictionary now save it in json
        with open('urls.json','w') as url_file:
            json.dump(urls,url_file)
            session[request.form['code']] = True
        return render_template('your_url.html', code=request.form['code'])
    else:
        # return redirect('/')
        return redirect(url_for('urlshort.home'))

# create a new route that will take variable name and give the user that they want as we have short names
@bp.route('/<string:code>') # it says look for after the first slash on the website any sort of string and put it in a variable called code
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json' )as urls_file :
            urls = json.load(urls_file)
            if code in urls.keys():
                # one more if statement to check if it is url or file
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static',filename='user_files/'+urls[code]['file']))

    return abort(404)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))