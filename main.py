from banco.database import conectar, criar_tabelas
from telas.Dashboard import *
import customtkinter as ctk

def main():
    conn = conectar()
    criar_tabelas(conn)
    
    app = App(conn)
    app.mainloop()
    
    conn.close()
    
if __name__ == "__main__":
    main()
