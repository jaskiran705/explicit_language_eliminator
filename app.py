import streamlit as st 
import Youtube_functions as yf
from validators.url import url
import os
import Download_path as dp

st.title('Your Personal YouTube ToolBox!')

st.sidebar.title('Select what do you want to do:')
down_or_clean=st.sidebar.radio("Select: ",("Download Audio or Video",
                                                    "Remove Profanity from video"))

link=st.text_input('Enter the URL of Youtube Video: ')
st.button('Check validity')
valid=url(link)
if valid and link:
    title=yf.get_title(link)
    streams=yf.get_streams(link)
    res ={}
    if down_or_clean=='Download Audio or Video':
        a_or_v=st.radio('Do you want to download: ',('Audio','Video'))
        if a_or_v=='Video':
            for i in streams:
                res[i.resolution]=i.itag
            tag = st.selectbox("Select Resolution",list(res.keys()))
            if tag!=None:
                home=st.text_input("Enter Name of home folder: ")
                if home:
                    path=st.radio("Select",dp.download_paths(home))
                    path=os.path.join(dp.get_home_path(home),path)
                    if path:
                        if st.button('Download video'):
                            yf.download_video(link=link,vid_path=path,tag=res[tag])
                            st.balloons()
                            st.success('VIDEO DOWNLOAD COMPLETE!')
                    else:
                        st.warning('Please Choose a Valid Path')
        else:
            home=st.text_input("Enter Name of home folder: ")
            if home:
                path=st.radio("Select",dp.download_paths(home))
                path=os.path.join(dp.get_home_path(home),path)
                if path:
                    if st.button('Download Audio'):
                        yf.audio_from_video(link=link,aud_path=path)
                        st.balloons()
                        st.success('AUDIO DOWNLOAD COMPLETE!')
                else:
                    st.warning('Please Choose a Valid Path')
    
    else: 
        streams=yf.get_streams(link)
        title=yf.get_title(link)
        for i in streams:
                res[i.resolution]=i.itag
        tag = st.selectbox("Select Resolution",list(res.keys()))
        go_clean=st.button("Clean Video")
        if tag!=None and go_clean:
            if not os.path.exists(os.path.join(yf.SAVE_VIDEO_PATH,title)+'_edited.mp4'):
                yf.audio_and_video(link,tag=res[tag])
                yf.audio_clean(link)
                yf.reattach_audio(link)
            st.success("Video is successfully cleaned!")
            st.balloons()
            vid_path=os.path.join(yf.SAVE_VIDEO_PATH,title+'_edited.mp4')
            if os.path.exists(vid_path):
                videofile=open(vid_path,'rb')
                st.video(videofile.read())
            else:
                st.error("Video not found"+vid_path)
                
        else:
            st.warning("Please select valid option")
        if os.path.exists(os.path.join('/Users/guldhillon/Digipodium/Explicit_Lang_Elim/',title)+'.TextGrid'):
            os.remove(os.path.join('/Users/guldhillon/Digipodium/Explicit_Lang_Elim/',title)+'.TextGrid')
else:
    st.warning("Please enter valid link")

