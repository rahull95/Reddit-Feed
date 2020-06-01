import praw
import pandas as pd
import numpy as np
import smtplib


reddit = praw.Reddit(client_id='******', \
                     client_secret='******', \
                     user_agent='Scraping', \
                     username='******', \
                     password='******')

#Subreddits to scrape data from
list_subreddits = ['MachineLearning','dataisbeautiful','todayilearned','aww','worldnews','soccer']


#Iterate through subreddits and get the top 5 hot posts by score
posts_df = pd.DataFrame()
for sub_reddit in list_subreddits:
    posts_sub = []
    top = reddit.subreddit(sub_reddit).hot(limit=50)
    for post in top:
        posts_sub.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])

    posts_sub = pd.DataFrame(posts_sub,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
    posts_sub = posts_sub.sort_values(by=['score','num_comments'], ascending=False)
    posts_sub = posts_sub.reset_index(drop=True)
    posts_sub = posts_sub.head(5)
    posts_df = posts_df.append(posts_sub)
    

#Selecting only columns that are needed
columns_needed = ['title','subreddit','url']
posts_df1 = posts_df[columns_needed]


#Change Datatype
reddit_feed = ''
text_list = []
for index, row in posts_df1.iterrows():
    sub_text = "Subreddit: " + row['subreddit']
    title_text = 'Title: ' + row['title']
    url_text = 'URL: ' + row['url']
    text_row = '\n'.join([sub_text, title_text, url_text])
    
    text_list.append(text_row)

reddit_feed = '\n\n'.join(text_list)


#Sending an email with the curated feed
smtp_obj = smtplib.SMTP('smtp.gmail.com',587)
smtp_obj.connect("smtp.gmail.com",587)
smtp_obj.ehlo()
smtp_obj.starttls()
smtp_obj.login('rahul95sivakumar@gmail.com', "******")

sender = 'rahul95sivakumar@gmail.com'
destination = 'rahul95siva@gmail.com'

subject = 'Curated Reddit Feed'
message = 'Subject: {0} \n\n\nFeed: {1}'.format(subject,reddit_feed)
smtp_obj.sendmail(sender, destination, message.encode('utf-8'))

smtp_obj.quit()



