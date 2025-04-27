#from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM as Ollama, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from sys import argv
import warnings


# set off warnings LangChainDeprecationWarning and UserWarning
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# 1. Create the model
embedding_model="all-minilm"#"mxbai-embed-large"#
llm = Ollama(model='llama3.2')
embeddings = OllamaEmbeddings(model=embedding_model)

# check file extension and use appropriate loader
if argv[1].endswith('.txt'):
  loader = TextLoader(argv[1])
elif argv[1].endswith('.pdf'):
  loader = PyPDFLoader(argv[1])
else:
  raise ValueError("Unsupported file type. Please provide a .txt or .pdf file.")

# 2. Load the context information and create a retriever
pages = loader.load_and_split()
store = DocArrayInMemorySearch.from_documents(pages, embedding=embeddings)
retriever = store.as_retriever()


# 3. Create the prompt template
template = """
* Answer the question based on the context provided if possible, but do not refer to template explicitly.
* If the question is not related to the context but you can answer it, then answer but remind the user:
 "the question is not related to the context, but I can answer it based on my training data".
* If you don't know the answer, say "I can't help with that".
Context: {context}
Question: {question}
"""


prompt = PromptTemplate.from_template(template)
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

previous_questions = ["\n"]
def get_previous_questions():
    return "\n".join(previous_questions)

# 4. Build the chain of operations
chain = (
    {
        'context': retriever | format_docs,
        'question': RunnablePassthrough(),
#        'question': lambda x: x['question'],
#        'previous_questions': lambda x: x['previous_questions'],
    }
    | prompt
    | llm
    | StrOutputParser()
)

# 5. Start asking questions and getting answers in a loop
i = 0
while True:
    question = input('What do you want to learn from the document?\n')
    if question.lower() == 'exit':
        print('Goodbye!')
        break
    elif question.strip() == '':
        print('Please ask a valid question.')
        continue
    i+=1
    print()
    print(chain.invoke(question))
    #print(chain.invoke({'question': question, 'previous_questions': get_previous_questions()}))
    #previous_questions.append(f"Q{i}: {question}")
    #print("Previously answered questions:")
    #for q in previous_questions:
    #    print(q)
    #print("______________________________")
    print()
