import streamlit as st
import preprocess,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Chat Analyser")
st.sidebar.title("Chat-Analyzer")
up_file = st.sidebar.file_uploader("Choose a file")
if up_file is not None:
    d = up_file.getvalue()
    data = d.decode("utf-8")
    df = preprocess.preprocess(data)
    s_list=df['sender'].unique().tolist()
    s_list.sort()
    s_list.insert(0,"Overall")
    user=st.sidebar.selectbox("Show Analysis for:",s_list)

    if st.sidebar.button("Show Analysis"):

        st.title("Top Statistics")
        num,words,media,links=helper.fetch_stats(user,df)
        c1,c2,c3,c4=st.columns(4)
        with c1:
            st.header("Total Messages")
            st.title(num)
        with c2:
            st.header("Total Words")
            st.title(words)
        with c3:
            st.header("Total Media")
            st.title(media)
        with c4:
            st.header("Total Links")
            st.title(links)

        st.title("Monthly Message Graph")
        timeline=helper.timeline(user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Activity Map")
        c1,c2=st.columns(2)
        with c1:
            st.header("Most Active Days")
            busy_day=helper.active_days(user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='orange')
            st.pyplot(fig)
        with c2:
            st.header("Most Active Months")
            busy_month=helper.active_months(user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='orange')
            st.pyplot(fig)
        
        st.title("Weekly Activity Heatmap")
        user_map=helper.period(user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_map)
        st.pyplot(fig)

        if user=='Overall':
            st.title("Most Active Users:")
            c1,c2=st.columns(2)
            x,newdf=helper.most_active(df)
            fig,ax=plt.subplots()
            with c1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with c2:
                st.dataframe(newdf)

        st.title("Word Cloud")
        df_wc,df_word=helper.create_cloud(user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        st.title("Most Common Words")
        fig,ax=plt.subplots()
        ax.barh(df_word[0],df_word[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        e_df=helper.emoji_c(user,df)
        if e_df.shape[0]!=0:
            st.title("Most Common Emoji")
            c1,c2=st.columns(2)
            with c1:
                st.dataframe(e_df)
            with c2:
                fig,ax=plt.subplots()
                ax.pie(e_df[1].head(),labels=e_df[0].head(),autopct="%0.2f")
                st.pyplot(fig)
