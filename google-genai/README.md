# Google GenAI Notebooks

A collection of notebooks to support the following whitepapers:
- [Foundational Large Language Models & Text Generation](https://www.kaggle.com/whitepaper-foundational-llm-and-text-generation)
- [Prompt Engineering](https://www.kaggle.com/whitepaper-prompt-engineering)
- [Embeddings & Vector Stores](https://www.kaggle.com/whitepaper-embeddings-and-vector-stores)
- [Agents](https://www.kaggle.com/whitepaper-agents)

Setup

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

- **prompting.ipynb** - contains examples of setting generation parameters, enum and json prompting, few shotp, Chain of Thought, ReAct, code generation, execution and explanation
- **evaluation.ipynb** - examples on how to use an LLM as an evaluator for answers provided by another LLM
- **qa_rag.ipynb** - RAG sample using ChromaDB
- **embeddings_sim_score.ipynb** - calculate similarity scores for embeddings
- **classification_embeddings_keras.ipynb** - classification using embeddings and Keras
- **function_calling.ipynb** - build a chat interface over a local database using Gemini API's automatic function calling
- **langgraph_agent.ipynb** - cafe ordering system using langgraph