from banco.database import conectar, criar_tabelas
from telas.Iniciar import *
from telas.login import *

def main():
    conn = conectar()
    criar_tabelas(conn)
    
    app = App(conn)
    
    #app = Login(conn)
    app.mainloop()
    
    conn.close()
    
if __name__ == "__main__":
    main()
