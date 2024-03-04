import sys
sys.path.insert(8,r'C:\Users\Call me Jimmy\Desktop\Anyao Real\Stuff')
from Stuff.util import db
import pandas as pd
import pickle



    #Preprocessing jarnman
bookList = db()

customer_book_comment = db(name='test')
customer_book_comment.query('SELECT * FROM  DATA_AI', True)
df = customer_book_comment.intoPD()



### load model ###
model = pickle.load(open(r"model\ModelJarnman\JarnmanRecmodel.pkl", 'rb'))


def content_based_filtering_KNN(Book_name):

    Book_name = Book_name
    Bid = bookList.matchBookName(Book_name)

    if Bid in df['BID'].values:

        user_book_df = df.pivot_table(index=['BID'],columns=['CID'],values=['RATING']).fillna(0)

        # creating sparace matrix
        book_index= user_book_df.index.to_list().index(Bid)
        distances, indices = model.kneighbors(user_book_df.iloc[book_index,:].values.reshape(1,-1), n_neighbors =6)
        books_recommend = []
        for i in range(1, len(indices.flatten())):
            books_recommend.append(user_book_df.index[indices.flatten()[i]])
        books_recommend = [bookList.matchBookBID(i) for i in books_recommend]
        return books_recommend

def callUrlFunction(Book_name):
    url = bookList.query(f"SELECT PIC_URL FROM Book WHERE LOWER(BID) = LOWER('{bookList.matchBookName(Book_name)}')")[0][0]
    return url

def showInfoFunction(Book_name):
    book_info = bookList.query(f"SELECT BNAME, PUBLISHER, TYPEDATE, TYPEROUND, TOTALPAGES, OVERALL_RATING FROM Book WHERE LOWER(BID) = LOWER('{bookList.matchBookName(Book_name)}')")[0]
    Book_info_dict = {'name' : book_info[0],
                      'publisher' : book_info[1],
                      'first_publish_year' : book_info[2],
                      'edition' : book_info[3],
                      'pages' : book_info[4],
                      'rating' : book_info[5]}
    return Book_info_dict

if __name__ == '__main__':
    print(showInfoFunction('cosmos'))