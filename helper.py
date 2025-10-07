from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(user,df):
    if user!='Overall':
        df=df[df['sender']==user]
    num=df.shape[0]
    words=[]
    for message in df['message']:
        words.extend(message.split())
    media=df[df['message']=='<Media omitted>'].shape[0]
    extractor=URLExtract()
    links=[]
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    return num,len(words),media,len(links)

def most_active(df):
    x=df['sender'].value_counts().head(6)
    df=round((df['sender'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'sender':'name','count':'percent'})
    return x,df

def create_cloud(user,df):
    if user!='Overall':
        df=df[df['sender']==user]
    df=df[df['message']!='<Media omitted>']
    df=df[df['message']!='This message was deleted']
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    def remove_stop(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words and word!='<this' and word!='edited>' and word!='message':
                y.append(word)
        return " ".join(y)
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df['message'].apply(remove_stop)
    df_wc=wc.generate(df['message'].str.cat(sep=" "))
    words=[]
    for message in df['message']:
        for word in message.lower().split():
            if word not in stop_words and word!='<this' and word!='edited>' and word!='message':
                words.append(word)
    df_word=pd.DataFrame(Counter(words).most_common(20))
    return df_wc,df_word

def emoji_c(user,df):
    if user!='Overall':
        df=df[df['sender']==user]
    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])
    e_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return e_df

def timeline(user,df):
    if user!='Overall':
        df=df[df['sender']==user]
    timeline = df.groupby(['year','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(str(timeline['month'][i])+"-"+str(timeline['year'][i]))
    timeline['time']=time
    return timeline

def active_days(user,df):
    if user!='Overall':
        df=df[df['sender']==user]
    return df['day_name'].value_counts()

def active_months(user,df):
    if user!='Overall':
        df=df[df['sender']==user]
    return df['month'].value_counts()

def period(user,df):
    if user!='Overall':
        df=df[df['sender']==user]
    act_map=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return act_map
