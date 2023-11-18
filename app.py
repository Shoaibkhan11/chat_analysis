import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt



st.sidebar.title("WhatsApp chat analysis")

uploaded_file=st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df=preprocessor.preprocess(data)
    st.dataframe(df)
    #fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.remove("group notification")
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user=st.sidebar.selectbox("show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages=helper.fetch_messages(selected_user,df)
        num_words=helper.fetch_words(selected_user,df)
        num_media=helper.fetc_media(selected_user,df)
        num_links=helper.fetch_links(selected_user,df)
        st.title("Top Statistics of WhatsApp Chats")

        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Media Shared")
            st.title(num_media)
        with col4:
            st.header("Links Shared")
            st.title(num_links)
        if selected_user=="Overall":
            st.title("Most Busy User")
            x,busy_df=helper.most_busy_users(df)
            fig,ax=plt.subplots()
            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                st.pyplot(fig)

            with col2:
                st.dataframe(busy_df.rename(columns={'count':'percentage'}))

        st.title("Most Common Words")
        most_common_df=helper.most_common_words(selected_user,df)

        st.dataframe(most_common_df.rename(columns={0:"word",1:'count'}))

        fig,ax=plt.subplots()

        ax.bar(most_common_df[0],most_common_df[1],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        emoji_df=helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2=st.columns(2)

        with col1:
            st.dataframe(emoji_df.rename(columns={0:'emoji',1:'counts'}))

        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)


        st.title('Monthly Timeline Analysis')

        timeline=helper.monthly_timeline(selected_user,df)

        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        st.title("Daily Timeline Analysis")

        daily_timeline=helper.daily_timeline(selected_user,df)

        fig,ax=plt.subplots()

        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title('Activity Map')

        col1,col2=st.columns(2)

        with col1:
            st.header('Most Busy Days')
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)