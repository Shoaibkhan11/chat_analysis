from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji
def fetch_messages(selected_user,df):
    if selected_user=='Overall':
        return df.shape[0]
    else:
        return df[df['user']==selected_user].shape[0]


def fetch_words(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    words = []
    for i in df['message']:
        words.extend(i.split())
    return len(words)

def fetc_media(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    return df[df['message']=='<Media omitted>\n'].shape[0]

def fetch_links(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    links=[]
    extract=URLExtract()
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return len(links)


def most_busy_users(df):
    x=df['user'].value_counts().head()
    ans_df=round((df['user'].value_counts()/df['user'].shape[0])*100,2).reset_index().rename(columns={'index':'percentage','user':'name'})
    return x,ans_df


def most_common_words(selected_user,df):
    f=open("stop_hinglish.txt","r")
    stop_words=f.read()
    f.close()

    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    temp=df[df['message']!="<Media omitted>\n"]
    temp=temp[temp['user']!='group notification']

    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    ans_df=pd.DataFrame(Counter(words).most_common(25))

    return ans_df

def emoji_helper(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    ans_df=pd.DataFrame(Counter(emojis).most_common())

    return ans_df


def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    df['month_num']=df['date'].dt.month
    timeline=df.groupby(['year','month_num','month'])['message'].count().reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(str(timeline.iloc[i]['month'])+'-'+str(timeline.iloc[i]['year']))
    timeline['time']=time

    return timeline

def daily_timeline(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]

    df['only_date']=df['date'].dt.date
    daily_timeline=df.groupby('only_date')['message'].count().reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]

    df['day_name']=df['date'].dt.day_name()

    ans_df=df['day_name'].value_counts()

    return ans_df


def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]

    ans_df=df['month'].value_counts()

    return ans_df

def activity_heatmap(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]

    period=[]
    for hour in df['hour']:
        if hour==23:
            period.append(str(hour)+'-'+'00')
        elif hour==0:
            period.append('00'+'-'+str(hour+1))
        else:
            period.append(str(hour)+'-'+str(hour+1))
    df['period']=period
    ans_df=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count')
    return ans_df
