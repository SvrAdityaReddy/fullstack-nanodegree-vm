#
# Database access functions for the web forum.
# 

import time
import psycopg2
import bleach

## Database connection
#DB = psycopg2.connect("dbname=forum");
i=0
#cur = DB.cursor();

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    #posts = [{'content': str(row[1]), 'time': str(row[0])} for row in DB]
    #posts.sort(key=lambda row: row['time'], reverse=True)
    DB = psycopg2.connect("dbname=forum");
    cur=DB.cursor();
    cur.execute("SELECT content,time from posts order by time Desc");
    rows = cur.fetchall();
    DB.close();
    posts = [{'content': str(row[0]), 'time': str(row[1])} for row in rows]
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    DB = psycopg2.connect("dbname=forum");
    cur = DB.cursor();
    t = time.strftime('%c', time.localtime())
    cont=str(bleach.clean(content));
    global i
    #type(t);
    cur.execute("INSERT INTO posts (content,time,id) VALUES(%s,%s,%s)" , (cont,t,i+1,));
    DB.commit();
    i=i+1;
    cur.execute("UPDATE posts set content='Cheese!' where content like '%spam%'");
    cur.execute("UPDATE posts set content='Cheese!' where content like '%<script>%'");
    DB.commit();
    DB.close();
    #t = time.strftime('%c', time.localtime())
    #DB.append((t, content))
