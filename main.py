import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient  
from langchain_classic.agents.agent import  AgentExecutor
from langchain_classic.agents import create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
import os

from dotenv import load_dotenv

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
from langchain_groq import ChatGroq

async def main():
    # 1. Inisialisasi MCP Client
    client = MultiServerMCPClient(
        {
            "file": {
                "transport": "stdio",  
                "command": "python",
                "args": [r"E:\codingan\python\project\ai-documentation-generator\server.py"],
            }
        }
    )

    # PERBAIKAN 1: Wajib initialize sebelum mengambil tools
    tools = await client.get_tools() 
    print('tools',tools)
    # 2. Inisialisasi LLM
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=groq_key
    )

    # PERBAIKAN 2: Membuat Prompt Template standar untuk Agent
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Kamu adalah asisten pengembang yang efisien. Gunakan tools yang tersedia untuk membaca isi file."),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    # PERBAIKAN 3: Menggunakan eksekutor agen standar LangChain
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # PERBAIKAN 4: Format input menggunakan "input"
    file_response = await agent_executor.ainvoke(
        {"input": "apa isi file test.py"}
    )
    
    print("\nJawaban AI:")
    print(file_response["output"])

    # Selalu tutup koneksi client setelah selesai
  
if __name__ == "__main__":
    asyncio.run(main())