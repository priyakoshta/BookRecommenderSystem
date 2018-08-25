
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


books = pd.read_csv('/home/priya/Downloads/BookRecommenderSystem/BX-Books.csv', sep=';', error_bad_lines=False, encoding="latin-1")
books.columns = ['ISBN', 'bookTitle', 'bookAuthor', 'yearOfPublication', 'publisher', 'imageUrlS', 'imageUrlM', 'imageUrlL']


# In[3]:


users = pd.read_csv('/home/priya/Downloads/BookRecommenderSystem/BX-Users.csv', sep=';', error_bad_lines=False, encoding="latin-1")
users.columns= ['userID', 'Location', 'Age']


# In[4]:


ratings = pd.read_csv('/home/priya/Downloads/BookRecommenderSystem/BX-Book-Ratings.csv', sep=';', error_bad_lines=False, encoding="latin-1")
ratings.columns= ['userID', 'ISBN', 'bookRating']


# In[5]:


print(ratings.shape)


# In[6]:


ratings.columns


# In[7]:


ratings.head()


# In[8]:


plt.rc("font",size=15)
ratings.bookRating.value_counts(sort=False).plot(kind='bar')
plt.title("Rating Distribution\n")
plt.xlabel("Rating")
plt.ylabel("Count")
plt.savefig('/home/priya/Downloads/system1.png', bbox_inches="tight")
plt.show()


# In[9]:


print(books.shape)


# In[10]:


print(list(books.columns))


# In[11]:


books.head()


# In[12]:


print(users.shape)
print(list(users.columns))


# In[13]:


users.head()


# In[14]:


users.Age.hist(bins=[0,10,20,30,40,50,100])
plt.title("Age Distribution\n")
plt.xlabel("Age")
plt.ylabel("Count")
plt.savefig('/home/priya/Downloads/system2.png', bbox_inches="tight")
plt.show()


# In[15]:


rating_count = pd.DataFrame(ratings.groupby('ISBN')['bookRating'].count())
rating_count.sort_values('bookRating',ascending=False).head()


# In[16]:


most_rated_books = pd.DataFrame(['0971880107','0316666343','0385504209','0060928336','0312195516'], index=np.arange(5),columns=['ISBN'])
most_rated_books_summary = pd.merge(most_rated_books,books,on='ISBN')
most_rated_books_summary


# In[17]:


average_rating = pd.DataFrame(ratings.groupby('ISBN')['bookRating'].mean())
average_rating['ratingCount'] = pd.DataFrame(ratings.groupby('ISBN')['bookRating'].count())
average_rating.sort_values('ratingCount', ascending=False).head()


# In[18]:


counts1 = ratings['userID'].value_counts()
ratings = ratings[ratings['userID'].isin(counts1[counts1 >= 200].index)]
counts = ratings['bookRating'].value_counts()
ratings = ratings[ratings['bookRating'].isin(counts[counts >= 100].index)]


# In[19]:


ratings_pivot = ratings.pivot(index='userID', columns='ISBN').bookRating
userID = ratings_pivot.index
ISBN = ratings_pivot.columns
print(ratings_pivot.shape)
ratings_pivot.head()


# In[20]:


bones_ratings = ratings_pivot['0316666343']
similar_to_bones = ratings_pivot.corrwith(bones_ratings)
corr_bones = pd.DataFrame(similar_to_bones, columns=['pearsonR'])
corr_bones.dropna(inplace=True)
corr_summary = corr_bones.join(average_rating['ratingCount'])
corr_summary[corr_summary['ratingCount']>=300].sort_values('pearsonR', ascending=False).head(10)


# In[21]:


books_corr_to_bones = pd.DataFrame(['0312291639', '0316601950', '0446610038', '0446672211', '0385265700', '0345342968', '0060930535', '0375707972', '0684872153'], 
                                  index=np.arange(9), columns=['ISBN'])
corr_books = pd.merge(books_corr_to_bones, books, on='ISBN')
corr_books

