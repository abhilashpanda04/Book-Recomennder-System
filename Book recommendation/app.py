from crypt import methods
from flask import Flask, render_template,request
import pickle
import pandas as pd
import numpy as np

popular_df=pickle.load(open('popular.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
similarity_score=pickle.load(open('similarity_score.pkl','rb'))

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                            book_name=popular_df['Book-Title'].tolist(),
                            author=popular_df['Book-Author'].tolist(),
                            image=popular_df['Image-URL-M'].tolist(),
                            votes=popular_df['Num-Rating'].tolist(),
                            ratings=popular_df['Avg-Rating'].tolist())


@app.route('/recommend')
def recommend_ui():
    return render_template(
                            'recommend.html',
    )


@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input=request.form.get('user_input')
    # return user_input
    try:
        index=np.where(pt.index==user_input)[0][0]
        distances=similarity_score[index]
        similar_items=sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1],reverse=True)[1:6]
        data=[]
        
        for i in similar_items:
            item=[]
#             print(pt.index[i[0]])
            temp_df=books[books['Book-Title']==pt.index[i[0]]]
            item.extend(temp_df.drop_duplicates('Book-Title')['Book-Title'].tolist())
            item.extend(temp_df.drop_duplicates('Book-Title')['Book-Author'].tolist())
            item.extend(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].tolist())
            data.append(item)
    except:
        data='book not found, can you check the spelling'
    # print(data)
    return render_template('recommend.html',data=data)


if  __name__== '__main__':
    app.run(debug=True)












