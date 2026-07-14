import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Secure File Reader")
ALLOWED_DIRECTORY = os.path.abspath("./workspace")

def is_safe_path(path: str) -> bool:
    """Memastikan AI tidak melakukan Path Traversal (membaca file di luar folder izin)"""
    target_path = os.path.abspath(os.path.join(ALLOWED_DIRECTORY, path))
    return target_path.startswith(ALLOWED_DIRECTORY)

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
@mcp.tool()
def append_local_file(relative_path: str,text: str) -> str:
    """
  Menambahkan teks ke akhir file. Jika file belum ada, file baru akan dibuat secara otomatis.
    """
    if not is_safe_path(relative_path):
        return "Error: Akses ditolak. Anda tidak diizinkan membaca file di luar folder workspace."
    full_path = os.path.join(ALLOWED_DIRECTORY, relative_path)
    
    if not os.path.exists(full_path):
        return f"Error: File '{relative_path}' tidak ditemukan."
        
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "a", encoding="utf-8") as f:
            return f.write(text)
    except Exception as e:
        return f"Error saat mengedit file: {str(e)}"
    
@mcp.tool()
def write_local_file(relative_path: str, new_content: str) -> str:
    """
    Membuat file baru atau mengganti seluruh isi file yang sudah ada dengan konten baru.
    Sebaiknya gunakan read_local_file terlebih dahulu sebelum memanggil tool ini.
    """
    if not is_safe_path(relative_path):
        return "Error: Akses ditolak."

    full_path = os.path.join(ALLOWED_DIRECTORY, relative_path)

    if not os.path.isfile(full_path):
        return f"Error: File '{relative_path}' tidak ditemukan."

    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        return f"Berhasil memperbarui '{relative_path}'."

    except Exception as e:
        return f"Error saat menulis file: {e}"

if __name__ == "__main__":
      os.makedirs(ALLOWED_DIRECTORY, exist_ok=True)
      mcp.run(transport="stdio")