import subprocess
import re
import glob
import os
import shutil
import time

from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.core import PromptTemplate
from llama_index.core.node_parser import CodeSplitter, MarkdownNodeParser
from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core.indices.vector_store.base import VectorStoreIndex
from llama_index.embeddings.fastembed import FastEmbedEmbedding
import qdrant_client

# setting up the llm
llm=Ollama(model="qwen2.5:14b-instruct-q4_1", request_timeout=300.0)
Settings.llm = llm
# setting up the embedding model
Settings.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-base-en-v1.5")

# utility functions
repos_folder = "repos"
# create folder if does not exists
if not os.path.exists(repos_folder):
    os.makedirs(repos_folder)

def parse_github_url(url):
    pattern = r"https://github\.com/([^/]+)/([^/]+)"
    match = re.match(pattern, url)
    return match.groups() if match else (None, None)

def clone_github_repo(repo_url, repo):    
    try:
        print('Cloning the repo ...')
        result = subprocess.run(["git", "clone", repo_url, f"{repos_folder}/{repo}"], check=True, text=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone repository: {e}")
        return None
    
def validate_owner_repo(owner, repo):
    return bool(owner) and bool(repo)

def parse_docs_by_file_types(ext, language, input_dir_path):
    try:
        files = glob.glob(f"{input_dir_path}/**/*{ext}", recursive=True)
        if len(files) > 0:
            loader = SimpleDirectoryReader(input_dir=input_dir_path, required_exts=[ext], recursive=True)
            docs = loader.load_data()
            
            parser = ( MarkdownNodeParser() if ext == ".md" else CodeSplitter.from_defaults(language=language) )
            return parser.get_nodes_from_documents(docs)
        else:
            print(f"No files found with extension {ext}")
            return []
    except Exception as e:
        print(f'Exception {e} occurred while parsing docs into nodes of file type {ext}')
        return []
    
def create_index(nodes):
    # Delete the entire database directory
    vector_store_path = "qdrant_cc_db"
    if os.path.exists(vector_store_path):
        shutil.rmtree(vector_store_path)
    print("Creating a new index ...")
    start_time = time.time()
    # Create a local Qdrant vector store
    client = qdrant_client.QdrantClient(path=vector_store_path)
    vector_store = QdrantVectorStore(client=client, collection_name="code_collection")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex(nodes, storage_context = storage_context)
    end_time = time.time()
    
    elapsed_time = end_time - start_time
    print(f"The operation took {elapsed_time:.4f} seconds to complete.")
    
    # Get the collection info
    collection_info = client.get_collection("code_collection")
    print(f"Number of vector embeddings in the index: {collection_info.points_count}")
    return index

# setup a query engine
def setup_query_engine(github_url):
    owner, repo = parse_github_url(github_url)   
    
    if validate_owner_repo(owner, repo):
        input_dir_path = f"{repos_folder}/{repo}"
        if os.path.exists(input_dir_path):
           pass
        else:
            clone_github_repo(github_url, repo)
        
        try:
            file_types = {
                ".md": "markdown",
                ".cs": "c_sharp",
                ".yml": "yaml",
                ".yaml": "yaml",
                ".tf": "hcl",
            }
            
            nodes = []
            for ext, language in file_types.items():
                nodes += parse_docs_by_file_types(ext, language, input_dir_path)
                
            index = create_index(nodes)
            
            query_engine = index.as_query_engine(similarity_top_k=4)
            
            qa_prompt_tmpl_str = (
            "Context information is below.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "Given the context information above I want you to think step by step to answer the query in a crisp manner, in case you don't know the answer say 'I don't know!'.\n"
            "Query: {query_str}\n"
            "Answer: "
            )

            qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)
            
            query_engine.update_prompts(
                {"response_synthesizer:text_qa_template": qa_prompt_tmpl}
            )

            if nodes:
                print("Data loaded successfully!!")
                print("Ready to chat!!")
            else:
                print("No data found, check if the repository is not empty!")
            
            return query_engine
            
        except Exception as e:
            print(f"An error occurred: {e}")    
    else:
        print('Invalid github repo, try again!')
        return None
        
if __name__ == "__main__":
    
    github_url = "https://github.com/MarianBusila/CleanArchitecture"
    query_engine = setup_query_engine(github_url=github_url)   

    while True:
        question = input("Enter your question (or 'exit' to quit): ")
        
        if question.lower() == 'exit':
            print("Exiting the program. Goodbye!")
            break
        
        response = query_engine.query(question)
        print(str(response))
        print()  # Add a blank line for better readability