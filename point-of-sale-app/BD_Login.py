import sqlite3

class modelo():
    def __init__(self):
        self.conexion = sqlite3.connect(r"C:\sqlite3\Bases\17126976.db")

    def muestra_Usuarios(self):
        self.cursor_conexion = self.conexion.cursor()
        sintax_sql = '''SELECT * FROM USUARIOS'''
        self.cursor_conexion.execute(sintax_sql)
        tabla_usuarios = self.cursor_conexion.fetchall()
        print(tabla_usuarios)  
        self.cursor_conexion.close()
        return tabla_usuarios

    def muestra_usuario_login(self, nickName, contraseña):
        self.cursor_conexion = self.conexion.cursor()
        sintax_sql = '''SELECT * FROM USUARIOS WHERE NICKNAME == ? AND CONTRASEÑA == ?'''  
        self.cursor_conexion.execute(sintax_sql, (nickName, contraseña))
        tabla_usuarios = self.cursor_conexion.fetchall()
        self.cursor_conexion.close()
        return tabla_usuarios

    def muestra_usuario_login_pass(self, usuario):
        self.cursor_conexion = self.conexion.cursor()
        sintax_sql = '''SELECT * FROM USUARIOS WHERE NICKNAME = ?'''
        self.cursor_conexion.execute(sintax_sql, (usuario,))
        tabla_usuarios = self.cursor_conexion.fetchall()
        self.cursor_conexion.close()
        return tabla_usuarios

    def inserta_usuario(self, nombre, ap_paterno, ap_materno, usu, contraseña, correo, telefono):  
	    self.cursor_conexion = self.conexion.cursor()
	    sintax_sql = '''INSERT INTO USUARIOS ("NOMBRE(S)", "APELLIDO_PATERNO", "APELLIDO_MATERNO", "NICKNAME", "CONTRASEÑA", "CORREO", "ESTATUS", "TELEFONO") VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
	    self.cursor_conexion.execute(sintax_sql, (nombre, ap_paterno, ap_materno, usu, contraseña, correo, 1, telefono))  
	    self.conexion.commit()
	    self.cursor_conexion.close()