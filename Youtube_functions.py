from youtube_transcript_api import YouTubeTranscriptApi
from better_profanity import profanity
from pytube import YouTube
from moviepy.editor import *
import moviepy.editor as mp
from pydub import AudioSegment
mysp=__import__("my-voice-analysis")
from parselmouth.praat import call, run_file
import os

SAVE_VIDEO_PATH = "your_base_path/downloads/videos"
SAVE_TRANSCRIPT_PATH="your_base_path/downloads/transcripts"
SAVE_AUDIO_PATH="your_base_path/downloads/audios"

def clean_transcript(link):
    video_id=gen_id(link)

    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_generated_transcript(['en'])
    transcript=transcript.fetch()
    profanity.load_censor_words()
    for i in transcript:
        i['text']=profanity.censor(i['text'])
        
    title=get_title(link)

    if not os.path.exists(((os.path.join(SAVE_TRANSCRIPT_PATH,title))+'.txt')):
        file1=open(((os.path.join(SAVE_TRANSCRIPT_PATH,title))+'.txt'),'a')
        for line in transcript:
            text=line['text']
            start=line['start']
            duration=line['duration']
            inf=[text,start,duration]
            file1.writelines(str(inf))
            file1.write('\n')
        file1.close()
        print('Transcript saved to',((os.path.join(SAVE_TRANSCRIPT_PATH,title))+'.txt'))
    else:
        print('Transcript File Already Exists!')
        print()
        
    return transcript

    
def explicit_language_timestamps(transcript):
    time_stamps=list()
    j=0
    for i in transcript:
        if '****' in i['text']:
            time_stamps.append(i)
            j+=1
    return time_stamps

def gen_id(link):
    return (link.split('=')[1])


def default_tag(link):
    yt=YouTube(link)
    return yt.streams.first().itag

def get_title(link):
    yt = YouTube(link) 
    ori_title=yt.title
    title= [character for character in ori_title if character.isalnum() or character==' ']
    title = "".join(title)
    title=title.replace(' ','_')
    return title
    
def download_video(link,tag=18,vid_path=SAVE_VIDEO_PATH):
    yt = YouTube(link) 
    d_video = yt.streams.get_by_itag(tag)
    title=get_title(link)
    try: 
        #downloading the video 
        if not os.path.exists(os.path.join(vid_path,title)+'.mp4'):
            d_video.download(output_path=vid_path,filename=title) 
            print('Task Completed!') 
    except: 
        print("Some Error!") 
        
def audio_and_video(link,tag,aud_path=SAVE_AUDIO_PATH):
    title=get_title(link)
    yt=YouTube(link)
    download_video(link,tag)
    video = mp.VideoFileClip((os.path.join(SAVE_VIDEO_PATH,title)+'.mp4'))
    audio = video.audio
    if not os.path.exists(os.path.join(aud_path,title)+'.mp3'):
        audio.write_audiofile(os.path.join(aud_path,title)+'.mp3')

def audio_from_video(link,aud_path=SAVE_AUDIO_PATH):
    title=get_title(link)
    yt=YouTube(link)
    d_video = yt.streams.first()
    if not os.path.exists(os.path.join(SAVE_VIDEO_PATH,title)+'.mp4'):
        d_video.download(output_path=SAVE_VIDEO_PATH,filename=title) 
    video = mp.VideoFileClip((os.path.join(SAVE_VIDEO_PATH,title))+'.mp4')
    audio = video.audio
    if not os.path.exists(os.path.join(aud_path,title)+'.mp3'):
        audio.write_audiofile(os.path.join(aud_path,title)+'.mp3')
    os.remove((os.path.join(SAVE_VIDEO_PATH,title))+'.mp4')

def get_streams(link):
    yt=YouTube(link)
    streams=yt.streams.filter(file_extension='mp4',progressive=True)
    return streams

def audio_clean(link,aud_path=SAVE_AUDIO_PATH):
    f=explicit_language_timestamps(clean_transcript(link))
    title=get_title(link)
    song = AudioSegment.from_mp3(os.path.join(aud_path,title+'.mp3'))
    temp_path='downloads_yt/audios/temp_audio'
    song.export(os.path.join(temp_path,title+'.wav'), format="wav")
    p=os.path.join(temp_path,title) # Audio File title
    c="." # Path to the Audio_File directory (Python 3.7)
    rate_of_speech=myspsr(p,c)
    for i in f:
        i['text']=i['text'].replace('****','*** ')
        clip_start=i['start']*1000
        trans=i['text'].split()
        no_of_words=len(trans)
        index_of_word=trans.index("***")
        duration=(clip_start+(no_of_words/rate_of_speech*1000))-clip_start
        muted_clip=song[(clip_start+(duration/no_of_words)*index_of_word):(clip_start+(no_of_words/rate_of_speech*1000))]-100
        first_half=song[:(clip_start+(duration/no_of_words)*index_of_word)]
        second_half=song[(clip_start+(no_of_words/rate_of_speech*1000)):]
        song=first_half+muted_clip+second_half
    
    song.export(os.path.join(aud_path,title+'.mp3'),format="mp3")
    os.remove(os.path.join(temp_path,title+'.wav'))
    print("New audio saved at "+aud_path)


def reattach_audio(link,aud_path=SAVE_AUDIO_PATH,vid_path=SAVE_VIDEO_PATH):
    title=get_title(link)
    videoclip = VideoFileClip(os.path.join(vid_path,title+'.mp4'))
    audioclip = AudioFileClip(os.path.join(aud_path,title+'.mp3'))

    new_audioclip = CompositeAudioClip([audioclip])
    videoclip2 = videoclip.set_audio(AudioFileClip(os.path.join(aud_path,title+'.mp3')))
    videoclip2.write_videofile(os.path.join(vid_path,title+'_edited.mp4'),codec='libx264', 
      audio_codec='aac', 
      temp_audiofile='temp-audio.m4a', 
      remove_temp=True)
    print("Successful!")

def myspsr(m,p):
    sound=p+"/"+m+".wav"
    sourcerun=p+"/myspsolution.praat"
    path=p+"/"
    try:
        objects= run_file(sourcerun, -20, 2, 0.3, "yes",sound,path, 80, 400, 0.01, capture_output=True)
        print (objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
        z1=str( objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z2=z1.strip().split()
        z3=int(z2[2]) # will be the integer number 10
        z4=float(z2[3]) # will be the floating point number 8.3
        print ("rate_of_speech=",z3,"# syllables/sec original duration")
    except Exception as e:
        z3=0
        print ("Try again the sound of the audio was not clear",e)
    return z3