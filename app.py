import os
import streamlit as st # Create a secrets.toml file in /.streamlit and add your Open_AI api key
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI

from tempfile import NamedTemporaryFile
from src.helpers import extract_song_artist_pairs
from src.spotify import generate_song_suggestions
from src.tools import ImageCaptionTool
# , ObjectDetectionTool

os.environ['KMP_DUPLICATE_LIB_OK']='True'

### initialize agent #########
tools = [ImageCaptionTool()]

llm = ChatOpenAI(
    openai_api_key=st.secrets["OPENAI_API_KEY"],
    temperature=0.1,
    model_name="gpt-3.5-turbo"
)

agent = initialize_agent(
    agent="zero-shot-react-description",
    tools=tools,
    llm=llm,
    max_iterations=5,
    verbose=True,
    early_stopping_method='generate'
)

# set title
st.title('Pick an Image to generate Songs Recommendations')

# set header
st.header("Please upload an image")

# upload file
file = st.file_uploader("", type=["jpeg", "jpg", "png"])

if file:
    # display image
    st.image(file, use_column_width=True)

    # text input
    preset_question = "Can you please recommend me three songs based on this image?"

    ### compute agent response ###
    with NamedTemporaryFile(dir='.') as f:
        f.write(file.getbuffer())
        image_path = f.name

        # write agent response
        if preset_question and preset_question != "":
            with st.spinner(text="In progress..."):
                response = agent.run('{}, this is the image path: {}'.format(preset_question, image_path))
                st.write(response)
                song_artist_pairs = extract_song_artist_pairs(response)
                generate_song_suggestions(song_artist_pairs)