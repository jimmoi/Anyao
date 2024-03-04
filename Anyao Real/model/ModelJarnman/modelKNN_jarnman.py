import sys
sys.path.insert(8,r'C:\Users\Call me Jimmy\Desktop\Anyao Real\Stuff')
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from Stuff.util import db
from joblib import dump, load
import pickle

################  Query data to train model  ################
customer_book_comment = db(name='test')
customer_book_comment.query('SELECT * FROM  DATA_AI', True)
df = customer_book_comment.intoPD()




################  Train model  ################
user_book_df = df.pivot_table(index=['BID'], columns=['CID'], values=['RATING']).fillna(0)
# creating sparace matrix
user_book_df_matrix = csr_matrix(user_book_df.values)
model_knn = NearestNeighbors(metric="cosine", algorithm="brute")
model_knn.fit(user_book_df_matrix)

filename = 'JarnmanRecmodel.pkl'
pickle.dump(model_knn, open(filename, 'wb'))


