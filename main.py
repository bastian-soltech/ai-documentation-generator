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
    client = MultiServerMCPClient(
        {
            "file": {
                "transport": "stdio",  
                "command": "python",
                "args": [r"E:\codingan\python\project\ai-documentation-generator\server.py"],
            }
        }
    )

    tools = await client.get_tools() 
    print('tools',tools)
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=groq_key
    )
    prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Kamu adalah asisten pengembang perangkat lunak profesional yang ahli dalam menulis dokumentasi teknis. "
        "Tugas utamamu adalah membantu pengguna membuat atau memperbarui file `README.md`.\n\n"
        "Instruksi Kerja:\n"
        "1. Gunakan tools yang tersedia untuk membaca dan menganalisis kode sumber di dalam project terlebih dahulu.\n"
        "2. Tulis dokumentasi yang komprehensif, mencakup deskripsi proyek, teknologi yang digunakan, cara instalasi, dan cara penggunaan.\n"
        "3. Jika file `README.md` belum ada di direktori, buat file baru dengan nama `README.md` menggunakan tool penulisan file yang tersedia.\n"
        "4. Selalu pastikan output penulisan menggunakan format Markdown yang rapi dan mudah dibaca."
    ),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])


    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    file_response = await agent_executor.ainvoke(
        {"input": "buatkan dokumentasi untuk code math.py"}
    )
    
    print("\nJawaban AI:")
    print(file_response["output"])
if __name__ == "__main__":
    asyncio.run(main())