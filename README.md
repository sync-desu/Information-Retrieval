# Simple ChatBot using Information Retrieval

A simple ChatBot using the **Retrieval Augmented Generation** (*Information Retrieval*) technique. It is built using **LangChain**, **Ollama**, and **ChromaDB**.  
This ChatBot allows users to upload documents, stores them as embeddings, and answers questions based on the context of the documents.

---

## Features

- **Document Upload & Processing** - Extracts text data from any document and converts them into embeddings.
- **Contextual Retrieval** – **ChromaDB** is used to store the embeddings, and retrieve relevant chunks for any user query.
- **LLM-Powered Responses** – Uses **Ollama** hosted locally for generating accurate and context-aware answers.
- **Persistent Storage** – Keeps your documents and embeddings stored for future queries.
- **Interactive Chat Interface** – Simple web interface built using **Chainlit** to chat with your documents.

---

## Project Structure

```bash
root_dir/
├── src/
|   ├── engine/
|   |   └── __init__.py    # Contains the main Engine class responsible for handling context retrieval and passing to the language model, and also contains the DataManager class responsible for data extraction and storage.
|   ├── template/
|   |   └── __init__.py    # Contains a simple prompt template with system messages to guide the language model and improve factuality with respect to the context provided.
|   ├── vectorstore/       # You just have to make this folder, the file inside will be created automatically by the respective vectorstore library.
|   |   └── chroma.sqlite3
|   ├── __init__.py
|   └── config.py          # Contains a Config Dataclass essential to ensure reproducibility with a wide variety of models and database structures.
├── main.py                # Entry point for running the ChatBot, also contains the UI elements made using Chainlit.
├── README.md              # Project documentation (this file).
└── requirements.txt       # Project dependencies.
````

---

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/sync-desu/Information-Retrieval.git
   cd Information-Retrieval
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Additional dependencies**
    - Ensure the dependencies for the **Unstructured** library are also installed [from here.](https://pypi.org/project/unstructured/)
---

## Usage

Run the ChatBot with:

```bash
chainlit run main.py
```

Follow the prompts to upload documents and start asking questions!

---

## Dependencies

* [LangChain](https://python.langchain.com/)
* [Ollama](https://ollama.ai/)
* [ChromaDB](https://docs.trychroma.com/)
* [Unstructured](https://github.com/Unstructured-IO/unstructured) (for document parsing)

---

## Roadmap

* [ ] Chat history memory
* [ ] Authentication for multi-user access

---

## Contributing

Contributions, issues, and feature requests are welcome!
Feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.