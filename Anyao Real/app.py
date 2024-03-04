from flask import Flask, render_template, request, redirect, url_for
from webRec import content_based_filtering_KNN, callUrlFunction, showInfoFunction

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendations', methods=['POST'])
def recommendations():
    book_name = request.form['book_name']
    recommended_books = content_based_filtering_KNN(book_name)  # Assuming this function returns a list of recommended books
    return render_template('recommendations.html', recommended_books=recommended_books, callUrlFunction=callUrlFunction, url_for=url_for, redirect=redirect)

@app.route('/book_info/<book_name>')
def book_info(book_name):
    book_info = showInfoFunction(book_name)  # Assuming this function returns book info
    return render_template('book_info.html', book_info=book_info, callUrlFunction=callUrlFunction, url_for=url_for, redirect=redirect)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)