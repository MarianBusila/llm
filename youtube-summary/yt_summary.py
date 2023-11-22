import streamlit as st
from pytube import YouTube
from haystack.nodes import PromptModel, PromptNode
from haystack.nodes.audio import WhisperTranscriber
from haystack.pipelines import Pipeline
import time
from model_add import LlamaCPPInvocationLayer

st.set_page_config(
    layout="wide",
    page_title="YouTube Summary"
)

def download_video(url):
    yt = YouTube(url)
    video = yt.streams.filter(abr='160kbps').last()
    return video.download()

def initialize_model(full_path):
    return PromptModel(
        model_name_or_path=full_path,
        invocation_layer_class=LlamaCPPInvocationLayer,
        use_gpu=False,
        max_length=512
        )

def initialize_prompt_node(model):
    summary_prompt = "deepset/summarization"
    return PromptNode(model_name_or_path = model, default_prompt_template = summary_prompt, use_gpu = False)

def transcribe_audio(file_path, prompt_node):
    whisper = WhisperTranscriber()
    pipeline = Pipeline()
    pipeline.add_node(component=whisper, name="whisper", inputs=["File"])
    pipeline.add_node(component=prompt_node, name="prompt", inputs=["whisper"])
    output = pipeline.run(file_paths=[file_path])
    return output

def main():
    st.title("YouTube Video Summarizer")
    st.markdown('<style>h1{color: orange; text-align: center;}</style>', unsafe_allow_html=True)
    st.subheader('Built with the Llama 2 🦙, Haystack, Streamlit and ❤️')
    st.markdown('<style>h3{color: pink;  text-align: center;}</style>', unsafe_allow_html=True)

    # Expander for app details
    with st.expander("About the App"):
        st.write("This app allows you to summarize while watching a YouTube video.")
        st.write("Enter a YouTube URL in the input box below and click 'Submit' to start.")

    youtube_url = st.text_input("YouTube video URL")
    if st.button("Submit") and youtube_url:
        file_path = download_video(youtube_url)

        full_path = "llama-2-7b-32k-instruct.Q4_K_S.gguf"
        model = initialize_model(full_path)        
        prompt_node = initialize_prompt_node(model)

        output = transcribe_audio(file_path, prompt_node)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.video(youtube_url)

        with col2:
            st.header("Summarization of YouTube Video")
            st.write(output)
            st.success(output["results"][0].split("\\n[INST]")[0])


if __name__ == "__main__":
    main()
