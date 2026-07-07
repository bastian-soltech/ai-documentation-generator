import os
from mcp.server.fastmcp import FastMCP

# 1. Inisialisasi FastMCP Server
mcp = FastMCP("Secure File Reader")

# Tentukan folder aman yang boleh diakses oleh AI
ALLOWED_DIRECTORY = os.path.abspath("./workspace")

def is_safe_path(path: str) -> bool:
    """Memastikan AI tidak melakukan Path Traversal (membaca file di luar folder izin)"""
    target_path = os.path.abspath(os.path.join(ALLOWED_DIRECTORY, path))
    return target_path.startswith(ALLOWED_DIRECTORY)

# 2. Daftarkan fungsi sebagai Tool yang bisa dipanggil oleh AI
@mcp.tool()
def read_local_file(relative_path: str) -> str:
    """
    Membaca isi dari sebuah file teks di dalam folder workspace berdasarkan relative path-nya.
    Gunakan tool ini jika kamu perlu memeriksa kode, config, atau dokumentasi.
    """
    if not is_safe_path(relative_path):
        return "Error: Akses ditolak. Anda tidak diizinkan membaca file di luar folder workspace."
        
    full_path = os.path.join(ALLOWED_DIRECTORY, relative_path)
    
    if not os.path.exists(full_path):
        return f"Error: File '{relative_path}' tidak ditemukan."
        
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error saat membaca file: {str(e)}"

if __name__ == "__main__":
    # 3. Jalankan server menggunakan transport STDIO (standar untuk AI client seperti Claude Desktop)
      mcp.run(transport="stdio")