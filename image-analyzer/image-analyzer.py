import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import streamlit as st


def analyze_image(image, question):
    torch.device('cuda')

    #Create model and tokenizer
    model = AutoModelForCausalLM.from_pretrained("MILVLG/imp-v1-3b", 
                                                torch_dtype = torch.float16, 
                                                device_map = "cuda:0", 
                                                trust_remote_code = True)

    tokenizer = AutoTokenizer.from_pretrained("MILVLG/imp-v1-3b", trust_remote_code = True)

    #Set inputs
    text = """A chat between a curious user and an artificial intelligence assistant. 
    The assistant gives helpful, detailed, and polite answers to the user's questions. 
    USER: <image>\n.{question}
    ASSISTANT:""".format(question=question)    

    input_ids = tokenizer(text, return_tensors='pt').input_ids
    input_ids = input_ids.to('cuda')
    image_tensor = model.image_preprocess(image)

    #Generate the answer
    output_ids = model.generate(
        input_ids,
        max_new_tokens=300,
        images=image_tensor,
        use_cache=True)[0]

    return tokenizer.decode(output_ids[input_ids.shape[1]:], skip_special_tokens=True).strip()


st.title("Image Question Answering App")

# Upload image
uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_image is not None:
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

# Collect question
question = st.text_input("Enter your question:")

# Ask button
if st.button("Ask"):    
    image = Image.open(uploaded_image)
    answer = analyze_image(image, question)
    st.text_area(label="Answer", value = answer, height=100)

