import sys
sys.path.insert(8,r'C:\Users\Call me Jimmy\Desktop\Anyao Real\Stuff')
from Stuff.util import db
import pandas as pd
import pickle

from PIL import Image
import matplotlib.pyplot as plt
import requests


    #Preprocessing jarnman
bookList = db()

customer_book_comment = db(name='test')
customer_book_comment.query('SELECT * FROM  DATA_AI', True)
df = customer_book_comment.intoPD()



### load model ###
model = pickle.load(open(r"model\ModelJarnman\JarnmanRecmodel.pkl", 'rb'))


def content_based_filtering_KNN():
    random = pd.Series(df['BID'].unique()).sample(2).values
    print('For example : ')
    for i in random:
        print('➤',bookList.matchBookBID(i))
    print('\n')
    Book_name = input("What book have you just read?\n :")
    Bid = bookList.matchBookName(Book_name)

    if Bid in df['BID'].values:

        user_book_df = df.pivot_table(index=['BID'],columns=['CID'],values=['RATING']).fillna(0)

        # creating sparace matrix
        book_index= user_book_df.index.to_list().index(Bid)
        distances, indices = model.kneighbors(user_book_df.iloc[book_index,:].values.reshape(1,-1), n_neighbors =6)
        books_recommend = []
        for i in range(1, len(indices.flatten())):
            books_recommend.append(user_book_df.index[indices.flatten()[i]])
        print(f'\nAfter you read {Book_name} You may also like these books')
        for i in range(len(books_recommend)):
            if not(books_recommend[i] == Bid):
                print(f"{i+1}.  {bookList.matchBookBID(books_recommend[i])}")
        print('\n')
        return books_recommend
    else:
        print("Can't find book in dataset, please check spelling")


if __name__ == '__main__':

    while(True):
        rec_lst = content_based_filtering_KNN()
        if rec_lst:
            choice = input('Show info? example : 1,2 / n (no)')
            if choice:
                _index = [int(i)-1 for i in choice.split(',')]
                for i in _index:
                    bid = rec_lst[i]
                    # book_detail = [i for i in bookList.data if i[0].lower()==bid.lower()][0]
                    book_detail = bookList.query(f"SELECT BNAME, PUBLISHER, TYPEDATE, TYPEROUND, TOTALPAGES, OVERALL_RATING FROM Book WHERE LOWER(BID) = LOWER('{bid}')")[0]
                    print(book_detail)
                    print(f'Name : {book_detail[0]}')
                    print(f'\tPublishier : {book_detail[1]}')
                    print(f'\tFirst Publish Year: {book_detail[2]}')
                    print(f'\tEdition : {book_detail[3]}')
                    print(f'\tPages : {book_detail[4]}')
                    print(f'\tRating : {book_detail[5]}', end= '\n\n')

                fig, axs = plt.subplots(1, len(_index),figsize=(18,5))
                _j = 0
                for i in [int(i)-1 for i in choice.split(',')]:
                    bname, url = bookList.query(f"SELECT BNAME, PIC_URL FROM Book WHERE LOWER(BID) = LOWER('{rec_lst[i]}')")[0]
                    try:
                        im = Image.open(requests.get(url, stream=True).raw)
                    except:
                        im = Image.open("Screenshot 2023-06-16 071247.png")
                    axs[_j].imshow(im)
                    axs[_j].axis("off")
                    axs[_j].set_title(f'{bname}',
                                        y=-0.1,
                                        color="red",
                                        fontsize=15)
                    _j+=1
                    fig.show()

        ans = input('Continue? (y/n)')
        if not((ans == 'y') or (ans == 'Y')):
            break