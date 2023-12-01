## Image generation

Text to image generation app using Open AI's DALL-E and open source HuggingFace Diffusers.
HuggingFace Diffusers require an NVIDIA GPU with Cuda and pytorch compiled with Cuda.

![](img/diffusers-astronout.png)

Source: [AI Image Generation Streamlit App](https://www.youtube.com/watch?v=17oHPkhgCuk)

Using:
- [streamlit](https://github.com/streamlit/streamlit) - build webapps in minutes
- [HuggingFace Diffusers](https://github.com/huggingface/diffusers) - state-of-the-art diffusion models for image and audio generation in PyTorch
- [OpenAI DALL-E](https://openai.com/dall-e-2) and [OpenAI Python Library](https://github.com/openai/openai-python)

Setup:

- go to [Pytorch website](https://pytorch.org/) and select the combo specific to your system. The command generated will be used the next steps.
![](img/pytorch-install.png)

- go to [NVidia CUDA Toolkit download page](https://developer.nvidia.com/cuda-toolkit-archive) and download the version of cuda, you selected above. Install it.
![](img/cuda-install.png)

- check cuda was installed by running this command
```
nvcc --version
```

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
streamlit run image_gen.py
```

- double check that torch and cuda are working as expected
![](image-generation/img/python-install-validation.png)
