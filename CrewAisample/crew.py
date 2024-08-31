from crewai import Crew, Agent, Task, Process
from crewai_tools import PDFSearchTool
from langchain_openai import ChatOpenAI
import os 
from dotenv import load_dotenv
load_dotenv()
llm = ChatOpenAI(
    api_key=os.getenv("api_key")
)
files = [
    {
        "name":"2024Q1",
        "path":"D:/Deepesh/PoCs/crewaisample/docs/2024Q1.pdf"
    },
    {
        "name":"2024Q2",
        "path":"D:/Deepesh/PoCs/crewaisample/docs/2024Q2.pdf"
    }
]
for file in files:
    pdf = file['path']
searchtool = PDFSearchTool(
    pdf = pdf,
    config = dict(
        llm = dict(
            provider = "openai",
            config = dict(
                api_key = os.getenv('openai_api_key')
            )
        ),
        embedder = dict(
            provider = "openai",
            config = dict(
                api_key = os.getenv('openai_api_key')
            )
        )
    )
)
processdocagent = Agent(
    role = "PDF Loader",
    goal = "To load and split the documents in a given directory into chunks and store the embedidngs in a Chroma Vector database directory defined.",
    backstory = "The agent is designed to load the documents in a directory, split them into chunks and store the embeddings in a Vector Database",
    llm = llm,
    verbose = True,
    allow_delegation = False,
    tools = [searchtool]
)

compareagent = Agent(
    role = "Comaparison Agent",
    goal = "Compare and find out the difference in details of documents the and list down the differences in a markdown table with the column names as the common entity names and the rows as the details from the documents",
    backstory = "The agent is designed to compare the details of documents and find out the difference between the document details.",
    llm = llm,
    verbose = True,
    allow_delegation = False,
)

processdoc = Task(
    description ="Load and split the documents in the directory using Document Loader.",
    agent = processdocagent,
    allow_multiple_outputs = False,
    expected_output = "All the details from the documents stored as embeddings in vector database"
)
compare = Task (
    description = f"""Compare the details and find out the difference between the documents present in the retrieved documents from the vector store. Make use of the details extracted from the documents and follow the below steps:
    1. Explain the differences between the details present in the documents with respect to common details extracted from the documents.
    2. List out the differences in structured markdown table with the column names as the common entity names and the rows as the details from the documents.,
    3. Do not add any extra details that are not present in the documents and make sure the differences are accurate.
    4. Maintain the structure of the table and do not change the order of the columns or rows.""",
    agent = compareagent,
    allow_multiple_outputs = False,
    expected_output = "The detailed differences between the documents that are invoices present in the retrieved documents in a markdown table format with the column names as the common entity names and the rows as the details from the documents.",
    context = [processdoc]
) 

comaprecrew = Crew(
    agents = [processdocagent, compareagent],
    tasks = [processdoc, compare],
    verbose = True,
    process = Process.sequential,
    share_crew = False
)
result = comaprecrew.kickoff()