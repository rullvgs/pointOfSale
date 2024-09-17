import sqlite3
import tkinter
from tkinter import messagebox as msg
import bcrypt
import random

class modelo():
    def __init__(self, app):
        self.conexion = sqlite3.connect(r"C:\sqlite3\Bases\17126976.db")
        self.app = app
        self.crear_tablas()
        self.agregar_usuario()

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
        sintax_sql = '''SELECT * FROM USUARIOS WHERE NICKNAME == '{}' '''.format(usuario)
        self.cursor_conexion.execute(sintax_sql)
        tabla_usuarios = self.cursor_conexion.fetchall()
        self.cursor_conexion.close()
        return tabla_usuarios

    def inserta_usuario(self, nombre, ap_paterno, ap_materno, usu, contraseña, correo, telefono, pregunta, respuesta):  
        self.cursor_conexion = self.conexion.cursor()
        
        mensajes_errores = []
        # Verificar si el nombre de usuario ya existe en la base de datos
        existe_usuario = self.cursor_conexion.execute("SELECT COUNT(*) FROM USUARIOS WHERE NICKNAME = ?", (usu,)).fetchone()[0]
        if existe_usuario > 0:
            mensajes_errores.append(f"Nombre de usuario '{usu}' ya está en uso.")

        # Verificar si el correo electrónico ya existe en la base de datos
        existe_correo = self.cursor_conexion.execute("SELECT COUNT(*) FROM USUARIOS WHERE CORREO = ?", (correo,)).fetchone()[0]
        if existe_correo > 0:
            mensajes_errores.append(f"Correo electrónico '{correo}' ya registrado.")

        # Verificar si el número de teléfono ya existe en la base de datos
        existe_telefono = self.cursor_conexion.execute("SELECT COUNT(*) FROM USUARIOS WHERE TELEFONO = ?", (telefono,)).fetchone()[0]
        if existe_telefono > 0:
            mensajes_errores.append(f"Número de teléfono '{telefono}' ya registrado.")

        if mensajes_errores:
            mensaje = ""
            mensaje += "\n".join(mensajes_errores)
            return mensaje[0:]

        # Si todo es único, proceder con la inserción
        sintax_sql = '''INSERT INTO USUARIOS ("NOMBRE(S)", "APELLIDO_PATERNO", "APELLIDO_MATERNO", "NICKNAME", "CONTRASEÑA", "CORREO", "ESTATUS", "TELEFONO", "PREGUNTAS", "RESPUESTAS") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        self.cursor_conexion.execute(sintax_sql, (nombre, ap_paterno, ap_materno, usu, contraseña, correo, 1, telefono, pregunta, respuesta))  
        self.conexion.commit()
        self.cursor_conexion.close()
        return "¡Registro exitoso!"


# ---------------------------_____________ REGISTRO VENTAS _____________---------------------------- #
    def obtener_equipos(self):
        self.cursor_conexion = self.conexion.cursor()

        sintax_sql = (''' SELECT NOMBRE_EQUIPO FROM EQUIPOS''')
        self.cursor_conexion.execute(sintax_sql)
        equipos = [row[0] for row in self.cursor_conexion.fetchall()]
        self.cursor_conexion.close()
        return equipos

    def obtener_usuarios(self, equipo):
        self.cursor_conexion = self.conexion.cursor()

        # Definir la consulta SQL
        consulta_sql = """
            SELECT INTEGRANTE
            FROM INTEGRANTES
            INNER JOIN EQUIPOS ON INTEGRANTES.ID_EQUIPO = EQUIPOS.ID_EQUIPO
            WHERE EQUIPOS.NOMBRE_EQUIPO = ?
        """
        # Ejecutar la consulta y obtener el resultado
        self.cursor_conexion.execute(consulta_sql, (equipo,))
        resultado = [row[0] for row in self.cursor_conexion.fetchall()]
        # Cerrar la conexión a la base de datos
        self.cursor_conexion.close()

        return resultado

    def obtener_conceptos(self):
        self.cursor_conexion = self.conexion.cursor()

        sintax_sql = (''' SELECT CONCEPTO FROM CONCEPTOS''')
        self.cursor_conexion.execute(sintax_sql)
        conceptos = [row[0] for row in self.cursor_conexion.fetchall()]
        self.cursor_conexion.close()
        return conceptos

    def obtener_subconceptos(self, concepto):
        self.cursor_conexion = self.conexion.cursor()

        # Conseguir el ID del concepto
        concepto_sql = '''SELECT ID_CONCEPTO FROM CONCEPTOS WHERE CONCEPTO = ?'''
        self.cursor_conexion.execute(concepto_sql, (concepto,))
        get_concepto = self.cursor_conexion.fetchone()

        if get_concepto is not None:  # Verificar si se encontró el concepto
            id_concepto = get_concepto[0]
            sintax_sql = '''SELECT SUBCONCEPTO FROM SUBCONCEPTOS WHERE ID_CONCEPTO = ?'''
            self.cursor_conexion.execute(sintax_sql, (id_concepto,))
            subconceptos = [row[0] for row in self.cursor_conexion.fetchall()]
            self.cursor_conexion.close()
            return subconceptos
        else:
            self.cursor_conexion.close()
            return []  # Retorna una lista vacía si no se encontró el concepto

    def insertar_equipo_venta(self, equipo):
        self.cursor_conexion = self.conexion.cursor()

        # Verificar si el equipo ya existe
        equipo_sql = '''SELECT ID_EQUIPO FROM EQUIPOS WHERE NOMBRE_EQUIPO = ?'''
        self.cursor_conexion.execute(equipo_sql, (equipo,))
        get_equipo = self.cursor_conexion.fetchone()

        if get_equipo:
            equipo_id = get_equipo[0]
        else:
            sintax_sql = '''INSERT INTO EQUIPOS (NOMBRE_EQUIPO) VALUES (?)'''
            self.cursor_conexion.execute(sintax_sql, (equipo,))
            self.conexion.commit()  # Para guardar los cambios en la base de datos
            msg.showinfo("Registro exitoso", "El equipo ha sido registrado exitosamente")

        # Actualizar la lista de equipos en el modelo
        self.equipos = self.obtener_equipos()  # Actualizar la lista de equipos
        self.cursor_conexion.close()

    def inserta_integrante_venta(self, integrante, equipo):
        self.cursor_conexion = self.conexion.cursor()

        # Conseguir el ID del equipo
        equipo_sql = '''SELECT ID_EQUIPO FROM EQUIPOS WHERE NOMBRE_EQUIPO = ?'''
        self.cursor_conexion.execute(equipo_sql, (equipo,))
        get_equipo = self.cursor_conexion.fetchone()
        id_equipo = get_equipo[0]

        # Verificar si el integrante ya existe en otro equipo
        integrante_sql = '''SELECT ID_INTEGRANTE FROM INTEGRANTES WHERE INTEGRANTE = ? AND ID_EQUIPO != ?'''
        self.cursor_conexion.execute(integrante_sql, (integrante, id_equipo))
        get_integrante = self.cursor_conexion.fetchone()

        if get_integrante:
            # El integrante ya está registrado en otro equipo
            msg.showerror("Error", "El integrante ya está registrado en otro equipo")
            resultado = False
        else:
            # Verificar si el integrante ya está registrado en el equipo especificado
            integrante_sql = '''SELECT ID_INTEGRANTE FROM INTEGRANTES WHERE INTEGRANTE = ? AND ID_EQUIPO = ?'''
            self.cursor_conexion.execute(integrante_sql, (integrante, id_equipo))
            get_integrante = self.cursor_conexion.fetchone()

            if get_integrante:                
                resultado = True
            else:
                # El integrante no está registrado en otro equipo ni en el equipo especificado
                sintax_sql = '''INSERT INTO INTEGRANTES (INTEGRANTE, ID_EQUIPO) VALUES (?, ?)'''
                self.cursor_conexion.execute(sintax_sql, (integrante, id_equipo))
                msg.showinfo("Registro exitoso", "El integrante ha sido registrado exitosamente")
                resultado = True

        self.conexion.commit()
        self.cursor_conexion.close()
        return resultado

    def inserta_concepto_venta(self, concepto):

        self.cursor_conexion = self.conexion.cursor()
        
        # Verificar si el concepto ya existe
        concepto_sql = '''SELECT ID_CONCEPTO FROM CONCEPTOS WHERE CONCEPTO = ?'''
        self.cursor_conexion.execute(concepto_sql, (concepto,))
        get_concepto = self.cursor_conexion.fetchone()

        if get_concepto:
            concepto_id = get_concepto[0]
        else:
            sintax_sql = '''INSERT INTO CONCEPTOS (CONCEPTO) VALUES (?)'''
            self.cursor_conexion.execute(sintax_sql, (concepto,))
            self.conexion.commit()  # Agregar esta línea para guardar los cambios en la base de datos
            msg.showinfo("Registro exitoso", "El conceto ha sido registrado exitosamente")

        # Actualizar la lista de equipos en el modelo
        self.conceptos = self.obtener_conceptos()  # Actualizar la lista de equipos
        self.cursor_conexion.close()

    def inserta_subconcepto_venta(self, subconcepto, concepto):
        self.cursor_conexion = self.conexion.cursor()

        # Conseguir el ID del concepto
        concepto_sql = '''SELECT ID_CONCEPTO FROM CONCEPTOS WHERE CONCEPTO = ?'''
        self.cursor_conexion.execute(concepto_sql, (concepto,))
        get_concepto = self.cursor_conexion.fetchone()
        concepto_id = get_concepto[0]

        # Verificar si el subconcepto ya existe
        subconcepto_sql = '''SELECT ID_SUBCONCEPTO FROM SUBCONCEPTOS WHERE SUBCONCEPTO = ?'''
        self.cursor_conexion.execute(subconcepto_sql, (subconcepto,))
        get_subconcepto = self.cursor_conexion.fetchone()

        if get_subconcepto:
            subconcepto_id = get_subconcepto[0]
        else:
            sintax_sql = '''INSERT INTO SUBCONCEPTOS (SUBCONCEPTO, ID_CONCEPTO) VALUES (?, ?)'''
            self.cursor_conexion.execute(sintax_sql, (subconcepto, concepto_id))
            msg.showinfo("Registro exitoso", "El subconceto ha sido registrado exitosamente")

        self.conexion.commit()
        self.cursor_conexion.close()

    def inserta_compras_venta(self, folio, fecha, integrante, concepto, subconcepto, cantidad, monto, monto_total):
        self.cursor_conexion = self.conexion.cursor()

        # Conseguir el ID del integrante
        integrante_sql = '''SELECT ID_INTEGRANTE FROM INTEGRANTES WHERE INTEGRANTE = ?'''
        self.cursor_conexion.execute(integrante_sql, (integrante,))
        get_integrante = self.cursor_conexion.fetchone()
        id_integrante = get_integrante[0]

        # Conseguir el ID del concepto
        concepto_sql = '''SELECT ID_CONCEPTO FROM CONCEPTOS WHERE CONCEPTO = ?'''
        self.cursor_conexion.execute(concepto_sql, (concepto,))
        get_concepto = self.cursor_conexion.fetchone()
        concepto_id = get_concepto[0]

        # Conseguir el ID del subconcepto
        subconcepto_sql = '''SELECT ID_SUBCONCEPTO FROM SUBCONCEPTOS WHERE SUBCONCEPTO = ?'''
        self.cursor_conexion.execute(subconcepto_sql, (subconcepto,))
        get_subconcepto = self.cursor_conexion.fetchone()
        subconcepto_id = get_subconcepto[0]


        sintax_sql = ''' INSERT INTO COMPRAS ("FOLIO", "FECHA", "ID_INTEGRANTE", "ID_CONCEPTO", "ID_SUBCONCEPTO", "CANTIDAD", "MONTO", "MONTO_TOTAL") VALUES(?, ?, ?, ?, ?, ?, ?, ?)'''
        self.cursor_conexion.execute(sintax_sql, (folio, fecha, id_integrante, concepto_id, subconcepto_id, cantidad, monto, monto_total))
        self.conexion.commit()
        self.cursor_conexion.close()

    def muestra_ventas(self,fecha):
        self.cursor_conexion = self.conexion.cursor()

        ## Conseguir el ID del equipo
        #equipo_sql = '''SELECT ID_EQUIPO FROM EQUIPOS WHERE NOMBRE_EQUIPO = ?'''
        #self.cursor_conexion.execute(equipo_sql, (equipo,))
        #get_equipo = self.cursor_conexion.fetchone()
        #id_equipo = get_equipo[0]

        sintax_sql = '''SELECT COMPRAS.ID_COMPRA, COMPRAS.FECHA, COMPRAS.FOLIO, INTEGRANTES.INTEGRANTE, CONCEPTOS.CONCEPTO,
                         SUBCONCEPTOS.SUBCONCEPTO, COMPRAS.CANTIDAD, COMPRAS.MONTO, COMPRAS.MONTO_TOTAL
                    FROM COMPRAS
                    INNER JOIN INTEGRANTES ON COMPRAS.ID_INTEGRANTE = INTEGRANTES.ID_INTEGRANTE
                    INNER JOIN CONCEPTOS ON COMPRAS.ID_CONCEPTO = CONCEPTOS.ID_CONCEPTO
                    INNER JOIN SUBCONCEPTOS ON COMPRAS.ID_SUBCONCEPTO = SUBCONCEPTOS.ID_SUBCONCEPTO
                    WHERE COMPRAS.FECHA = ?'''

        self.cursor_conexion.execute(sintax_sql, (fecha,))
        tabla_compras = self.cursor_conexion.fetchall()
        self.cursor_conexion.close()
        return tabla_compras

    def sum_monto_integrante(self, fecha, integrante):
        self.cursor_conexion = self.conexion.cursor()

        # Definir la consulta SQL
        consulta_sql = """
            SELECT SUM(MONTO_TOTAL) FROM COMPRAS
            INNER JOIN INTEGRANTES ON COMPRAS.ID_INTEGRANTE = INTEGRANTES.ID_INTEGRANTE
            WHERE INTEGRANTES.INTEGRANTE = ? AND COMPRAS.FECHA = ?
        """

        # Ejecutar la consulta y obtener el resultado
        self.cursor_conexion.execute(consulta_sql, (integrante, fecha))
        resultado = self.cursor_conexion.fetchone()

        # Verificar si se encontró un resultado
        if resultado is None:
            monto_total = 0
        else:
            monto_total = resultado[0]
        # Cerrar el cursor
        self.cursor_conexion.close()
        return monto_total

    def importe_total_equipo(self, fecha, equipo):
        self.cursor_conexion = self.conexion.cursor()

        # Definir la consulta SQL
        consulta_sql = """
            SELECT SUM(MONTO_TOTAL) FROM COMPRAS
            INNER JOIN INTEGRANTES ON COMPRAS.ID_INTEGRANTE = INTEGRANTES.ID_INTEGRANTE
            INNER JOIN EQUIPOS ON INTEGRANTES.ID_EQUIPO = EQUIPOS.ID_EQUIPO
            WHERE EQUIPOS.NOMBRE_EQUIPO = ? AND COMPRAS.FECHA = ?
        """
        # Ejecutar la consulta y obtener el resultado
        self.cursor_conexion.execute(consulta_sql, (equipo, fecha))
        resultado = self.cursor_conexion.fetchone()

        # Verificar si se encontró un resultado
        if resultado is None:
            monto_total = 0
        else:
            monto_total = resultado[0]

        # Cerrar el cursor
        self.cursor_conexion.close()
        return monto_total

    def buscar_ingreso_total(self, fecha):
        self.cursor_conexion = self.conexion.cursor()
        sintax_sql = ''' SELECT SUM(MONTO_TOTAL) FROM COMPRAS WHERE FECHA = ?'''
        self.cursor_conexion.execute(sintax_sql, (fecha,))
        ingreso_total = self.cursor_conexion.fetchone()
        if ingreso_total:
            ingresos = ingreso_total[0]

        else:
            ingresos = 0
        self.cursor_conexion.close()
        return ingresos

    def cargar_ultimo_folio(self):
        self.cursor_conexion = self.conexion.cursor()
        sintax_sql = '''SELECT MAX(CAST(FOLIO AS INTEGER)) FROM COMPRAS'''
        self.cursor_conexion.execute(sintax_sql)
        resultado = self.cursor_conexion.fetchone()[0]
        if resultado is not None:
            self.cursor_conexion.close()
            return resultado + 1
        else:
            self.cursor_conexion.close()
            return 1

    def cargar_equipo(self, integrante):
        self.cursor_conexion = self.conexion.cursor()

        sintax_sql = '''
            SELECT EQUIPOS.NOMBRE_EQUIPO
            FROM EQUIPOS
            INNER JOIN INTEGRANTES ON EQUIPOS.ID_EQUIPO = INTEGRANTES.ID_EQUIPO
            WHERE INTEGRANTES.INTEGRANTE = ?
        '''
        self.cursor_conexion.execute(sintax_sql, (integrante,))
        equipo = self.cursor_conexion.fetchone()

        if equipo:
            nombre_equipo = equipo[0]
            self.cursor_conexion.close()
            return nombre_equipo            
        else:
            self.cursor_conexion.close()
            return None

    def actualizar_ventas(self, id_compra, fecha, folio, nombre_integrante, conceptos, subconcepto, cantidad_producto, monto, precio_final):
        self.cursor_conexion = self.conexion.cursor()

        # Conseguir el ID del integrante
        integrante_sql = '''SELECT ID_INTEGRANTE FROM INTEGRANTES WHERE INTEGRANTE = ?'''
        self.cursor_conexion.execute(integrante_sql, (nombre_integrante,))
        get_integrante = self.cursor_conexion.fetchone()
        id_integrante = get_integrante[0]

        # Conseguir el ID del concepto
        concepto_sql = '''SELECT ID_CONCEPTO FROM CONCEPTOS WHERE CONCEPTO = ?'''
        self.cursor_conexion.execute(concepto_sql, (conceptos,))
        get_concepto = self.cursor_conexion.fetchone()
        concepto_id = get_concepto[0]

        # Conseguir el ID del subconcepto
        subconcepto_sql = '''SELECT ID_SUBCONCEPTO FROM SUBCONCEPTOS WHERE SUBCONCEPTO = ?'''
        self.cursor_conexion.execute(subconcepto_sql, (subconcepto,))
        get_subconcepto = self.cursor_conexion.fetchone()
        subconcepto_id = get_subconcepto[0]


        sintax_sql = '''UPDATE COMPRAS
                        SET ID_INTEGRANTE = ?,
                            ID_CONCEPTO = ?,
                            ID_SUBCONCEPTO = ?,
                            CANTIDAD = ?,
                            MONTO = ?,
                            MONTO_TOTAL = ?
                        WHERE ID_COMPRA = ? AND FECHA = ?'''

        datos = (id_integrante, concepto_id, subconcepto_id, cantidad_producto, monto, precio_final, id_compra, fecha)
        self.cursor_conexion.execute(sintax_sql, datos)
        # Confirmar los cambios y aplicarlos permanentemente
        self.conexion.commit()
        self.cursor_conexion.close()
            

# ----------------------------------- CONSULTA DE LAS VENTANAS DE EGRESOS ----------------------------------- #


    def inserta_pagos(self, comprobante, fecha, concepto, categoria, cantidad_producto, precio_unitario, precio_final):
        self.cursor_conexion = self.conexion.cursor()

        # Obtener el ID de la categoría
        categoria_sql = '''SELECT ID_CATEGORIA FROM CATEGORIAS WHERE categoria = ?'''
        self.cursor_conexion.execute(categoria_sql, (categoria,))
        get_categoria = self.cursor_conexion.fetchone()
        id_categoria = get_categoria[0]

        # Insertar datos en la tabla EGRESOS
        consulta_sql = '''INSERT INTO EGRESOS (COMPROBANTE, FECHA, CONCEPTO, ID_CATEGORIA, CANTIDAD_PRODUCTO, PRECIO_UNITARIO, PRECIO_FINAL)
            VALUES (?, ?, ?, ?, ?, ?, ?)'''
        # Ejecutar la consulta
        self.cursor_conexion.execute(consulta_sql, (comprobante, fecha, concepto, id_categoria, cantidad_producto, precio_unitario, precio_final))
        self.conexion.commit()
        self.cursor_conexion.close()

    def muestra_compras(self, fecha):
        self.cursor_conexion = self.conexion.cursor()

        # Definir la consulta SQL para obtener los datos de las compras con la categoría
        consulta_sql = ''' SELECT EGRESOS.ID_EGRESO, EGRESOS.COMPROBANTE, EGRESOS.FECHA, EGRESOS.CONCEPTO, CATEGORIAS.CATEGORIA,
                   EGRESOS.CANTIDAD_PRODUCTO, EGRESOS.PRECIO_UNITARIO, EGRESOS.PRECIO_FINAL
            FROM EGRESOS
            INNER JOIN CATEGORIAS ON EGRESOS.ID_CATEGORIA = CATEGORIAS.ID_CATEGORIA
            WHERE EGRESOS.FECHA = ? '''
        
        # Ejecutar la consulta y obtener los datos de las compras con la categoría
        self.cursor_conexion.execute(consulta_sql, (fecha,))
        compras = self.cursor_conexion.fetchall()

        self.cursor_conexion.close()
        return compras

    def obtener_conceptos_egresos(self):
        self.cursor_conexion = self.conexion.cursor()

        sintax_sql = '''SELECT DISTINCT CONCEPTO FROM EGRESOS'''
        self.cursor_conexion.execute(sintax_sql)
        conceptos = [row[0] for row in self.cursor_conexion.fetchall()]

        self.cursor_conexion.close()
        return conceptos

    def obtener_egresos(self, fecha):
        self.cursor_conexion = self.conexion.cursor()

        sintax_sql = ''' SELECT SUM(PRECIO_FINAL) FROM EGRESOS WHERE FECHA = ?'''
        self.cursor_conexion.execute(sintax_sql, (fecha,))
        egreso = self.cursor_conexion.fetchone()
        #print("Valor de egreso:", egreso)

        # Verificar si se encontró un resultado
        if egreso is None or egreso[0] is None:
            total_egresos = 0
        else:
            total_egresos = egreso[0]
        # Cerrar el cursor
        self.cursor_conexion.close()
        return total_egresos

    def cargar_ultimo_comprobante(self):
        self.cursor_conexion = self.conexion.cursor()
        sintax_sql = '''SELECT MAX(CAST(COMPROBANTE AS INTEGER)) FROM EGRESOS'''
        self.cursor_conexion.execute(sintax_sql)
        resultado = self.cursor_conexion.fetchone()[0]

        if resultado is not None:
            self.cursor_conexion.close()
            return resultado + 1
        else:
            self.cursor_conexion.close()
            return 1

    def actualizar_egresos(self, id_egreso, comprobante, fecha, concepto, categoria, cantidad_producto, precio_unitario, precio_final):
        self.cursor_conexion = self.conexion.cursor()

        id_sql = '''SELECT ID_CATEGORIA FROM CATEGORIAS WHERE CATEGORIA = ?'''
        self.cursor_conexion.execute(id_sql, (categoria,))
        id_categoria = self.cursor_conexion.fetchone()[0]

        sintax_sql = ''' UPDATE EGRESOS SET FECHA = ?, CONCEPTO = ?, ID_CATEGORIA = ?, CANTIDAD_PRODUCTO = ?, 
                         PRECIO_UNITARIO = ?, PRECIO_FINAL = ? WHERE ID_EGRESO = ? AND COMPROBANTE = ?'''

        self.cursor_conexion.execute(sintax_sql, (fecha, concepto, id_categoria, cantidad_producto, precio_unitario, precio_final, id_egreso, comprobante))
        self.conexion.commit()
        self.cursor_conexion.close()       


#_______________________----------- TABLA DE INGRESOS ----------------------- ____________________ #

    def obtener_datos_por_fecha(self, fecha):
        self.cursor_conexion = self.conexion.cursor()

        # Consulta para obtener los datos por fecha
        sintax_sql = '''SELECT  MONTOS_EQUIPO.FECHA,
                                EQUIPOS.NOMBRE_EQUIPO,
                                MONTOS_EQUIPO.MONTO_TOTAL AS MONTO_TOTAL_EQUIPO,
                                INTEGRANTES.INTEGRANTE,
                                MONTOS_INTEGRANTE.MONTO_TOTAL AS MONTO_TOTAL_INTEGRANTE
                            FROM 
                                MONTOS_EQUIPO
                            JOIN 
                                EQUIPOS ON MONTOS_EQUIPO.ID_EQUIPO = EQUIPOS.ID_EQUIPO
                            JOIN 
                                INTEGRANTES ON EQUIPOS.ID_EQUIPO = INTEGRANTES.ID_EQUIPO
                            JOIN 
                                MONTOS_INTEGRANTE ON INTEGRANTES.ID_INTEGRANTE = MONTOS_INTEGRANTE.ID_INTEGRANTE AND MONTOS_EQUIPO.FECHA = MONTOS_INTEGRANTE.FECHA
                            WHERE 
                                MONTOS_EQUIPO.FECHA = ?
                            ORDER BY 
                                EQUIPOS.NOMBRE_EQUIPO, INTEGRANTES.INTEGRANTE; '''

        self.cursor_conexion.execute(sintax_sql, (fecha,))
        datos = self.cursor_conexion.fetchall()

        self.cursor_conexion.close()
        return datos


    def obtener_datos(self):
        self.cursor_conexion = self.conexion.cursor()

        # Consulta para obtener los datos por fecha
        sintax_sql = '''SELECT  MONTOS_EQUIPO.FECHA,
                                EQUIPOS.NOMBRE_EQUIPO,
                                MONTOS_EQUIPO.MONTO_TOTAL AS MONTO_TOTAL_EQUIPO,
                                INTEGRANTES.INTEGRANTE,
                                MONTOS_INTEGRANTE.MONTO_TOTAL AS MONTO_TOTAL_INTEGRANTE
                            FROM 
                                MONTOS_EQUIPO
                            JOIN 
                                EQUIPOS ON MONTOS_EQUIPO.ID_EQUIPO = EQUIPOS.ID_EQUIPO
                            JOIN 
                                INTEGRANTES ON EQUIPOS.ID_EQUIPO = INTEGRANTES.ID_EQUIPO
                            JOIN 
                                MONTOS_INTEGRANTE ON INTEGRANTES.ID_INTEGRANTE = MONTOS_INTEGRANTE.ID_INTEGRANTE 
                                                AND MONTOS_EQUIPO.FECHA = MONTOS_INTEGRANTE.FECHA
                            ORDER BY 
                                MONTOS_EQUIPO.FECHA, EQUIPOS.NOMBRE_EQUIPO DESC; '''

        self.cursor_conexion.execute(sintax_sql)
        datos = self.cursor_conexion.fetchall()

        self.cursor_conexion.close()
        return datos

    def ingresos_totales(self):
        self.cursor_conexion = self.conexion.cursor()
        sintax_sql = ''' SELECT SUM(MONTO_TOTAL) FROM COMPRAS'''
        self.cursor_conexion.execute(sintax_sql)
        ingreso_total = self.cursor_conexion.fetchone()
        if ingreso_total:
            ingresos = ingreso_total[0]

        else:
            ingresos = 0
        self.cursor_conexion.close()
        return ingresos

    def muestra_ventas_sin_fecha(self):
        self.cursor_conexion = self.conexion.cursor()

        ## Conseguir el ID del equipo
        #equipo_sql = '''SELECT ID_EQUIPO FROM EQUIPOS WHERE NOMBRE_EQUIPO = ?'''
        #self.cursor_conexion.execute(equipo_sql, (equipo,))
        #get_equipo = self.cursor_conexion.fetchone()
        #id_equipo = get_equipo[0]

        sintax_sql = '''SELECT COMPRAS.ID_COMPRA, COMPRAS.FECHA, COMPRAS.FOLIO, INTEGRANTES.INTEGRANTE, CONCEPTOS.CONCEPTO,
                         SUBCONCEPTOS.SUBCONCEPTO, COMPRAS.CANTIDAD, COMPRAS.MONTO, COMPRAS.MONTO_TOTAL
                    FROM COMPRAS
                    INNER JOIN INTEGRANTES ON COMPRAS.ID_INTEGRANTE = INTEGRANTES.ID_INTEGRANTE
                    INNER JOIN CONCEPTOS ON COMPRAS.ID_CONCEPTO = CONCEPTOS.ID_CONCEPTO
                    INNER JOIN SUBCONCEPTOS ON COMPRAS.ID_SUBCONCEPTO = SUBCONCEPTOS.ID_SUBCONCEPTO '''

        self.cursor_conexion.execute(sintax_sql)
        tabla_compras = self.cursor_conexion.fetchall()
        self.cursor_conexion.close()
        return tabla_compras


    def muestra_compras_integrantes(self, equipo):
        self.cursor_conexion = self.conexion.cursor()

        #Conseguir el ID del equipo
        equipo_sql = '''SELECT ID_EQUIPO FROM EQUIPOS WHERE NOMBRE_EQUIPO = ?'''
        self.cursor_conexion.execute(equipo_sql, (equipo,))
        get_equipo = self.cursor_conexion.fetchone()
        id_equipo = get_equipo[0]

        sintax_sql = '''SELECT COMPRAS.ID_COMPRA, COMPRAS.FECHA, COMPRAS.FOLIO, INTEGRANTES.INTEGRANTE, CONCEPTOS.CONCEPTO,
                         SUBCONCEPTOS.SUBCONCEPTO, COMPRAS.CANTIDAD, COMPRAS.MONTO, COMPRAS.MONTO_TOTAL
                    FROM COMPRAS
                        INNER JOIN INTEGRANTES ON COMPRAS.ID_INTEGRANTE = INTEGRANTES.ID_INTEGRANTE
                        INNER JOIN CONCEPTOS ON COMPRAS.ID_CONCEPTO = CONCEPTOS.ID_CONCEPTO
                        INNER JOIN SUBCONCEPTOS ON COMPRAS.ID_SUBCONCEPTO = SUBCONCEPTOS.ID_SUBCONCEPTO 
                        WHERE INTEGRANTES.ID_EQUIPO = ?
                    ORDER BY 
                            COMPRAS.FECHA DESC; '''
        self.cursor_conexion.execute(sintax_sql, (id_equipo,))
        tabla_compras = self.cursor_conexion.fetchall()
        self.cursor_conexion.close()
        return tabla_compras


#__________________________---------------------- TABLA EGRESOS -----------------------________________________

    def muestra_todos_egresos(self):
        self.cursor_conexion = self.conexion.cursor()

        # Definir la consulta SQL para obtener los datos de las compras con la categoría
        consulta_sql = ''' SELECT EGRESOS.COMPROBANTE, EGRESOS.FECHA, CATEGORIAS.CATEGORIA, EGRESOS.CONCEPTO,
                   EGRESOS.CANTIDAD_PRODUCTO, EGRESOS.PRECIO_UNITARIO, EGRESOS.PRECIO_FINAL
            FROM EGRESOS
            INNER JOIN CATEGORIAS ON EGRESOS.ID_CATEGORIA = CATEGORIAS.ID_CATEGORIA'''
        
        # Ejecutar la consulta y obtener los datos de las compras con la categoría
        self.cursor_conexion.execute(consulta_sql)
        compras = self.cursor_conexion.fetchall()

        self.cursor_conexion.close()
        return compras

    def obtener_egresos_totales(self):
        self.cursor_conexion = self.conexion.cursor()

        sintax_sql = ''' SELECT SUM(PRECIO_FINAL) FROM EGRESOS '''
        self.cursor_conexion.execute(sintax_sql)
        egreso = self.cursor_conexion.fetchone()
        #print("Valor de egreso:", egreso)

        # Verificar si se encontró un resultado
        if egreso is None:
            monto_total = 0
        else:
            total_egresos = egreso[0]
            # Cerrar el cursor
            self.cursor_conexion.close()
            return total_egresos


#---------------------------------------________ PERFIL USUARIO _________ -------------------------------------- #

    def eliminar_usuario(self, usuario):
        self.cursor_conexion = self.conexion.cursor()

        # Conseguir el ID del integrante
        integrante_sql = '''SELECT ID_INTEGRANTE FROM INTEGRANTES WHERE INTEGRANTE = ?'''
        self.cursor_conexion.execute(integrante_sql, (usuario,))
        get_integrante = self.cursor_conexion.fetchone()
        id_integrante = get_integrante[0]

        # Eliminar las filas relacionadas en COMPRAS
        compras_sql = ''' DELETE FROM COMPRAS WHERE ID_INTEGRANTE = ?'''
        self.cursor_conexion.execute(compras_sql, (id_integrante,))

        # Eliminar las filas relacionadas en MONTOS_INTEGRANTE
        montos_integrantes_sql = ''' DELETE FROM MONTOS_INTEGRANTE WHERE ID_INTEGRANTE = ?'''
        self.cursor_conexion.execute(montos_integrantes_sql, (id_integrante,))

        integrante_sql = ''' DELETE FROM INTEGRANTES WHERE ID_INTEGRANTE = ?'''
        self.cursor_conexion.execute(integrante_sql, (id_integrante,))

        self.conexion.commit()
        self.cursor_conexion.close()
        msg.showinfo("Operación exitosa", "Se ha eliminado al usuario exitosamente")

        return resultado

    def eliminar_equipo(self, equipo):
        self.cursor_conexion = self.conexion.cursor()

        # Conseguir el ID del equipo
        equipo_sql = '''SELECT ID_EQUIPO FROM EQUIPOS WHERE NOMBRE_EQUIPO = ?'''
        self.cursor_conexion.execute(equipo_sql, (equipo,))
        get_equipo = self.cursor_conexion.fetchone()
        id_equipo = get_equipo[0]

        # Eliminar las filas relacionadas en la tabla MONTOS_INTEGRANTES
        montos_integrantes_sql = '''DELETE FROM MONTOS_INTEGRANTE WHERE ID_INTEGRANTE IN (SELECT ID_INTEGRANTE FROM INTEGRANTES WHERE ID_EQUIPO = ?)'''
        self.cursor_conexion.execute(montos_integrantes_sql, (id_equipo,))

        # Eliminar las filas relacionadas en la tabla COMPRAS
        compras_sql = '''DELETE FROM COMPRAS WHERE ID_INTEGRANTE IN (SELECT ID_INTEGRANTE FROM INTEGRANTES WHERE ID_EQUIPO = ?)'''
        self.cursor_conexion.execute(compras_sql, (id_equipo,))

        # Eliminar las filas relacionadas en la tabla INTEGRANTES
        integrantes_sql = '''DELETE FROM INTEGRANTES WHERE ID_EQUIPO = ?'''
        self.cursor_conexion.execute(integrantes_sql, (id_equipo,))

        # Eliminar la fila en la tabla MONTOS_EQUIPO
        montos_equipo_sql = ''' DELETE FROM MONTOS_EQUIPO WHERE ID_EQUIPO = ?'''
        self.cursor_conexion.execute(montos_equipo_sql, (id_equipo,))

        # Eliminar la fila en la tabla EQUIPOS
        equipos_sql = '''DELETE FROM EQUIPOS WHERE ID_EQUIPO = ?'''
        self.cursor_conexion.execute(equipos_sql, (id_equipo,))

        self.conexion.commit()
        self.cursor_conexion.close()
        msg.showinfo("Operación exitosa", "Se ha eliminado al equipo de forma exitosa")


    def actualiza_nombre(self, nombre, usuario):

        self.cursor_conexion = self.conexion.cursor()
        sintax_sql = '''UPDATE USUARIOS 
                        SET     "NOMBRE(S)" = ?
                        WHERE NICKNAME= ? '''
        self.cursor_conexion.execute(sintax_sql,(nombre, usuario))
        self.conexion.commit()
        self.cursor_conexion.close()

    def actualiza_apellido_pa(self, ap_paterno, usuario):
        self.cursor_conexion = self.conexion.cursor()
        sintax_sql = '''UPDATE USUARIOS 
                        SET    APELLIDO_PATERNO = ?
                        WHERE NICKNAME = ? '''
        self.cursor_conexion.execute(sintax_sql, (ap_paterno, usuario))
        self.conexion.commit()
        self.cursor_conexion.close()

    def actualiza_apellido_ma(self, ap_materno, usuario):
        self.cursor_conexion = self.conexion.cursor()
        sintax_sql = '''UPDATE USUARIOS 
                        SET    APELLIDO_MATERNO = ?
                        WHERE NICKNAME = ? '''
        self.cursor_conexion.execute(sintax_sql, (ap_materno, usuario))
        self.conexion.commit()
        self.cursor_conexion.close()

    def actualiza_usuario(self, usuario, usuario2):
        self.cursor_conexion = self.conexion.cursor()
        # Verificar si el nombre de usuario ya existe en la base de datos
        existe_usuario = self.cursor_conexion.execute("SELECT COUNT(*) FROM USUARIOS WHERE NICKNAME = ?", (usuario2,)).fetchone()[0]
        if existe_usuario > 0:
            msg.showerror("Error", f"Nombre de usuario '{usuario2}' ya está en uso.")
            self.cursor_conexion.close()
            return False
        else:
            sintax_sql = '''UPDATE USUARIOS 
                            SET    NICKNAME = ?
                            WHERE NICKNAME = ? '''
            self.cursor_conexion.execute(sintax_sql, (usuario2, usuario))
            self.conexion.commit()
            self.cursor_conexion.close()
            return True
            msg.showinfo('Operación exitosa', 'Los datos se han modificado exitosamente')

    def actualiza_correo(self, correo, usuario):
        self.cursor_conexion = self.conexion.cursor()
        sintax_sql = '''UPDATE USUARIOS 
                        SET    CORREO = ?
                        WHERE NICKNAME = ? '''
        self.cursor_conexion.execute(sintax_sql, (correo, usuario))
        self.conexion.commit()
        self.cursor_conexion.close()

    def actualiza_telefono(self, telefono, usuario):
        self.cursor_conexion = self.conexion.cursor()
        sintax_sql = '''UPDATE USUARIOS 
                        SET TELEFONO = ?
                        WHERE NICKNAME = ? '''
        self.cursor_conexion.execute(sintax_sql, (telefono, usuario))
        self.conexion.commit()
        self.cursor_conexion.close()

    def obtener_contraseña(self, usuario):
        self.cursor_conexion = self.conexion.cursor()

        sintax_sql = '''SELECT CONTRASEÑA FROM USUARIOS
                        WHERE NICKNAME = ?'''
        self.cursor_conexion.execute(sintax_sql, (usuario,))
        hashed_password = self.cursor_conexion.fetchone()[0]
        self.cursor_conexion.close()
        return hashed_password

    def actualiza_contraseña(self, contraseña, usuario):
        self.cursor_conexion = self.conexion.cursor()

        sintax_sql = '''UPDATE  USUARIOS
                    SET  CONTRASEÑA = ?
                    WHERE NICKNAME = ?'''

        self.cursor_conexion.execute(sintax_sql, (contraseña, usuario))
        self.conexion.commit()
        self.cursor_conexion.close()

    def obtener_datos_usuario(self, usuario):
        self.cursor_conexion = self.conexion.cursor()
        sintax_sql = '''SELECT "NOMBRE(S)", APELLIDO_PATERNO, APELLIDO_MATERNO, NICKNAME, CORREO, TELEFONO
                       FROM USUARIOS
                       WHERE NICKNAME = ?'''
        self.cursor_conexion.execute(sintax_sql, (usuario,))
        datos_usuario = self.cursor_conexion.fetchone()
        self.cursor_conexion.close()
        return datos_usuario

#--------------------------------------______ MODIFICAR CONTRASEÑA _______ --------------------------------------- #
    def verificar_respuesta(self, respuesta, usuario, pregunta):
        self.cursor_conexion = self.conexion.cursor()

        usuario_sql = ''' SELECT RESPUESTAS FROM USUARIOS WHERE NICKNAME = ? AND PREGUNTAS = ?'''
        self.cursor_conexion.execute(usuario_sql, (usuario,pregunta))
        respuestaa = self.cursor_conexion.fetchone()
        if respuestaa is None:
            msg.showerror("Error", 'Verifica que los datos sean correctos!')
        else:
            # Comparar las respuestas
            if respuestaa and respuestaa[0] == respuesta:
                return True
            else:
                msg.showerror("Error", 'Verifica que los datos sean correctos!')
                return False

        self.cursor_conexion.close()



##----------------------- CREAR TABLAS ----------------------
    def crear_tablas(self):
        self.cursor_conexion = self.conexion.cursor()

        # Ejecutar el código SQL para crear las tablas
        self.cursor_conexion.execute('''
            CREATE TABLE IF NOT EXISTS "CATEGORIAS" (
                "ID_CATEGORIA"  INTEGER NOT NULL UNIQUE,
                "CATEGORIA" TEXT NOT NULL UNIQUE,
                PRIMARY KEY("ID_CATEGORIA" AUTOINCREMENT)
            );
        ''')

        self.cursor_conexion.execute('''
            CREATE TABLE IF NOT EXISTS "COMPRAS" (
                "ID_COMPRA"    INTEGER UNIQUE,
                "FECHA"    NUMERIC NOT NULL,
                "FOLIO"    TEXT NOT NULL,
                "ID_INTEGRANTE"    INTEGER,
                "ID_CONCEPTO"    INTEGER,
                "ID_SUBCONCEPTO"    INTEGER NOT NULL,
                "CANTIDAD"    INTEGER NOT NULL,
                "MONTO"    REAL NOT NULL,
                "MONTO_TOTAL"    REAL NOT NULL,
                FOREIGN KEY("ID_SUBCONCEPTO") REFERENCES "SUBCONCEPTOS"("ID_SUBCONCEPTO"),
                FOREIGN KEY("ID_INTEGRANTE") REFERENCES "INTEGRANTES"("ID_INTEGRANTE"),
                FOREIGN KEY("ID_CONCEPTO") REFERENCES "CONCEPTOS"("ID_CONCEPTO"),
                PRIMARY KEY("ID_COMPRA" AUTOINCREMENT)
            );
        ''')

        self.cursor_conexion.execute('''
            CREATE TABLE IF NOT EXISTS "CONCEPTOS" (
                "ID_CONCEPTO"   INTEGER NOT NULL,
                "CONCEPTO"  TEXT NOT NULL,
                PRIMARY KEY("ID_CONCEPTO" AUTOINCREMENT)
            );
        ''')


        self.cursor_conexion.execute('''
            CREATE TABLE IF NOT EXISTS "EGRESOS" (
                "ID_EGRESO" INTEGER NOT NULL,
                "COMPROBANTE"   TEXT NOT NULL,
                "FECHA" TEXT NOT NULL,
                "CONCEPTO"  TEXT NOT NULL,
                "ID_CATEGORIA"  INTEGER NOT NULL,
                "CANTIDAD_PRODUCTO" INTEGER NOT NULL,
                "PRECIO_UNITARIO"   REAL NOT NULL,
                "PRECIO_FINAL"  REAL NOT NULL,
                PRIMARY KEY("ID_EGRESO" AUTOINCREMENT),
                FOREIGN KEY("ID_CATEGORIA") REFERENCES "CATEGORIAS"("ID_CATEGORIA")
            );
        ''')

        self.cursor_conexion.execute('''
            CREATE TABLE IF NOT EXISTS "INGRESOS_TOTALES" (
                "FECHA" INTEGER,
                "INGRESO_TOTAL" REAL NOT NULL
            );
        ''')


        self.cursor_conexion.execute('''
            CREATE TABLE IF NOT EXISTS "INTEGRANTES" (
                "ID_INTEGRANTE" INTEGER NOT NULL,
                "INTEGRANTE"    TEXT,
                "ID_EQUIPO" INTEGER,
                PRIMARY KEY("ID_INTEGRANTE" AUTOINCREMENT),
                FOREIGN KEY("ID_EQUIPO") REFERENCES "EQUIPOS"("ID_EQUIPO")
            );
        ''')


        self.cursor_conexion.execute('''
            CREATE TABLE IF NOT EXISTS "MONTOS_EQUIPO" (
                "ID_EQUIPO" INTEGER,
                "FECHA" TEXT,
                "MONTO_TOTAL"   REAL,
                FOREIGN KEY("ID_EQUIPO") REFERENCES "EQUIPOS"("ID_EQUIPO"),
                PRIMARY KEY("ID_EQUIPO","FECHA")
            );
        ''')


        self.cursor_conexion.execute('''
            CREATE TABLE IF NOT EXISTS "MONTOS_INTEGRANTE" (
                "FECHA" TEXT,
                "ID_EQUIPO" INTEGER,
                "ID_INTEGRANTE" INTEGER,
                "MONTO_TOTAL"   REAL,
                PRIMARY KEY("ID_INTEGRANTE","FECHA"),
                FOREIGN KEY("ID_INTEGRANTE") REFERENCES "INTEGRANTES"("ID_INTEGRANTE"),
                FOREIGN KEY("ID_EQUIPO") REFERENCES "EQUIPOS"("ID_EQUIPO")
            );
        ''')


        self.cursor_conexion.execute('''
            CREATE TABLE IF NOT EXISTS "SUBCONCEPTOS" (
                "ID_SUBCONCEPTO"    INTEGER NOT NULL,
                "SUBCONCEPTO"   TEXT,
                "ID_CONCEPTO"   INTEGER,
                FOREIGN KEY("ID_CONCEPTO") REFERENCES "CONCEPTOS"("ID_CONCEPTO"),
                PRIMARY KEY("ID_SUBCONCEPTO" AUTOINCREMENT)
            );
        ''')

        self.cursor_conexion.execute('''
            CREATE TABLE IF NOT EXISTS "EQUIPOS" (
                "ID_EQUIPO" INTEGER NOT NULL,
                "NOMBRE_EQUIPO" TEXT NOT NULL,
                PRIMARY KEY("ID_EQUIPO" AUTOINCREMENT)
            );
        ''')

        self.cursor_conexion.execute('''
            CREATE TABLE IF NOT EXISTS "USUARIOS" (
                "ID_USUARIOS"   INTEGER NOT NULL,
                "NOMBRE(S)" TEXT,
                "APELLIDO_PATERNO"  TEXT,
                "APELLIDO_MATERNO"  TEXT,
                "NICKNAME"  TEXT UNIQUE,
                "CONTRASEÑA"    TEXT,
                "CORREO"    TEXT,
                "ESTATUS"   INTEGER,
                "TELEFONO"  INTEGER,
                "RESPUESTAS"    TEXT,
                "PREGUNTAS" INTEGER,
                PRIMARY KEY("ID_USUARIOS" AUTOINCREMENT)
            );
        ''')

        self.cursor_conexion.execute('DROP TRIGGER IF EXISTS "main"."insertar_monto_integrante";')
        self.cursor_conexion.execute('''CREATE TRIGGER insertar_monto_integrante
            AFTER INSERT ON COMPRAS
            FOR EACH ROW
            BEGIN
                -- Verificar si ya existe una fila con el mismo ID_INTEGRANTE y FECHA
                SELECT ID_INTEGRANTE, FECHA FROM MONTOS_INTEGRANTE
                WHERE ID_INTEGRANTE = NEW.ID_INTEGRANTE AND FECHA = NEW.FECHA;

                -- Si ya existe una fila con el mismo ID_INTEGRANTE y FECHA, actualizarla
                UPDATE MONTOS_INTEGRANTE
                SET MONTO_TOTAL = MONTO_TOTAL + NEW.MONTO_TOTAL
                WHERE ID_INTEGRANTE = NEW.ID_INTEGRANTE AND FECHA = NEW.FECHA;

                -- Si no existe una fila con el mismo ID_INTEGRANTE y FECHA, insertar una nueva fila
                INSERT INTO MONTOS_INTEGRANTE (FECHA, ID_EQUIPO, ID_INTEGRANTE, MONTO_TOTAL)
                SELECT NEW.FECHA, INTEGRANTES.ID_EQUIPO, NEW.ID_INTEGRANTE, SUM(NEW.MONTO_TOTAL)
                FROM INTEGRANTES
                WHERE INTEGRANTES.ID_INTEGRANTE = NEW.ID_INTEGRANTE AND NOT EXISTS (
                    SELECT 1 FROM MONTOS_INTEGRANTE
                    WHERE ID_INTEGRANTE = NEW.ID_INTEGRANTE AND FECHA = NEW.FECHA
                )
                GROUP BY NEW.FECHA, INTEGRANTES.ID_EQUIPO, NEW.ID_INTEGRANTE;
            END;
        ''')


        self.cursor_conexion.execute('DROP TRIGGER IF EXISTS "main"."insertar_monto_equipo";')
        self.cursor_conexion.execute('''
            CREATE TRIGGER insertar_monto_equipo
            AFTER INSERT ON COMPRAS
            FOR EACH ROW
            BEGIN
                -- Verificar si ya existe una fila con el mismo ID_EQUIPO y FECHA
                SELECT ID_EQUIPO, FECHA FROM MONTOS_EQUIPO
                WHERE ID_EQUIPO = (SELECT ID_EQUIPO FROM INTEGRANTES WHERE ID_INTEGRANTE = NEW.ID_INTEGRANTE) AND FECHA = NEW.FECHA;

                -- Si ya existe una fila con el mismo ID_EQUIPO y FECHA, actualizarla
                UPDATE MONTOS_EQUIPO
                SET MONTO_TOTAL = MONTO_TOTAL + NEW.MONTO_TOTAL
                WHERE ID_EQUIPO = (SELECT ID_EQUIPO FROM INTEGRANTES WHERE ID_INTEGRANTE = NEW.ID_INTEGRANTE) AND FECHA = NEW.FECHA;

                -- Si no existe una fila con el mismo ID_EQUIPO y FECHA, insertar una nueva fila
                INSERT INTO MONTOS_EQUIPO (FECHA, ID_EQUIPO, MONTO_TOTAL)
                SELECT NEW.FECHA, INTEGRANTES.ID_EQUIPO, SUM(NEW.MONTO_TOTAL)
                FROM INTEGRANTES
                WHERE INTEGRANTES.ID_INTEGRANTE = NEW.ID_INTEGRANTE AND NOT EXISTS (
                    SELECT 1 FROM MONTOS_EQUIPO
                    WHERE ID_EQUIPO = INTEGRANTES.ID_EQUIPO AND FECHA = NEW.FECHA
                )
                GROUP BY NEW.FECHA, INTEGRANTES.ID_EQUIPO;
            END;
        ''')


        self.cursor_conexion.execute('DROP TRIGGER IF EXISTS "main"."insertar_ingresos_totales";')
        self.cursor_conexion.execute('''
            CREATE TRIGGER insertar_ingresos_totales
            AFTER INSERT ON COMPRAS
            BEGIN
                -- Actualizar o insertar en la tabla INGRESOS_TOTALES
                UPDATE INGRESOS_TOTALES SET INGRESO_TOTAL = (SELECT SUM(MONTO_TOTAL) FROM COMPRAS WHERE FECHA = NEW.FECHA) WHERE FECHA = NEW.FECHA;
                INSERT INTO INGRESOS_TOTALES (FECHA, INGRESO_TOTAL)
                SELECT NEW.FECHA, SUM(MONTO_TOTAL)
                FROM COMPRAS
                WHERE NOT EXISTS (
                    SELECT 1 FROM INGRESOS_TOTALES
                    WHERE FECHA = NEW.FECHA
                )
                GROUP BY NEW.FECHA;
            END;
        ''')


        self.cursor_conexion.execute('DROP TRIGGER IF EXISTS "main"."actualizar_monto_integrante";')
        self.cursor_conexion.execute('''
            CREATE TRIGGER actualizar_monto_integrante
            AFTER UPDATE ON COMPRAS
            FOR EACH ROW
            BEGIN
                -- Actualizar el monto total del integrante para la fecha antigua y el integrante antiguo
                UPDATE MONTOS_INTEGRANTE
                SET MONTO_TOTAL = MONTO_TOTAL - OLD.MONTO_TOTAL
                WHERE ID_INTEGRANTE = OLD.ID_INTEGRANTE AND FECHA = OLD.FECHA;

                -- Actualizar el monto total del integrante para la nueva fecha y el nuevo integrante
                UPDATE MONTOS_INTEGRANTE
                SET MONTO_TOTAL = MONTO_TOTAL + NEW.MONTO_TOTAL
                WHERE ID_INTEGRANTE = NEW.ID_INTEGRANTE AND FECHA = NEW.FECHA;
            END;
        ''')


        self.cursor_conexion.execute('DROP TRIGGER IF EXISTS "main"."actualizar_monto_equipo";')
        self.cursor_conexion.execute('''
            CREATE TRIGGER actualizar_monto_equipo
            AFTER UPDATE ON COMPRAS
            FOR EACH ROW
            BEGIN
                -- Actualizar el monto total del equipo para la fecha antigua y el integrante antiguo
                UPDATE MONTOS_EQUIPO
                SET MONTO_TOTAL = MONTO_TOTAL - OLD.MONTO_TOTAL
                WHERE ID_EQUIPO = (SELECT ID_EQUIPO FROM INTEGRANTES WHERE ID_INTEGRANTE = OLD.ID_INTEGRANTE) AND FECHA = OLD.FECHA;

                -- Actualizar el monto total del equipo para la nueva fecha y el nuevo integrante
                UPDATE MONTOS_EQUIPO
                SET MONTO_TOTAL = MONTO_TOTAL + NEW.MONTO_TOTAL
                WHERE ID_EQUIPO = (SELECT ID_EQUIPO FROM INTEGRANTES WHERE ID_INTEGRANTE = NEW.ID_INTEGRANTE) AND FECHA = NEW.FECHA;
            END;
        ''')


        self.cursor_conexion.execute('DROP TRIGGER IF EXISTS "main"."actualizar_ingresos_totales";')
        self.cursor_conexion.execute('''
            CREATE TRIGGER actualizar_ingresos_totales
            AFTER UPDATE ON COMPRAS
            BEGIN
                UPDATE INGRESOS_TOTALES
                SET INGRESO_TOTAL = (SELECT COALESCE(SUM(MONTO_TOTAL), 0) FROM COMPRAS WHERE FECHA = NEW.FECHA)
                WHERE FECHA = NEW.FECHA;
            END;
        ''')


        # Guardar los cambios
        self.conexion.commit()
        #self.agregar_usuario()
        self.insertar_categorias()
        self.cursor_conexion.close()

    def insertar_categorias(self):
        # Verificar si la categoría 'Compras' ya existe en la tabla
        self.cursor_conexion.execute("SELECT * FROM CATEGORIAS WHERE CATEGORIA = 'Compras'")
        result = self.cursor_conexion.fetchone()

        # Si no existe, insertarla
        if result is None:
            self.cursor_conexion.execute("INSERT INTO CATEGORIAS (CATEGORIA) VALUES ('Compras')")

        # Verificar si la categoría 'Servicios' ya existe en la tabla
        self.cursor_conexion.execute("SELECT * FROM CATEGORIAS WHERE CATEGORIA = 'Servicios'")
        result = self.cursor_conexion.fetchone()

        # Si no existe, insertarla
        if result is None:
            self.cursor_conexion.execute("INSERT INTO CATEGORIAS (CATEGORIA) VALUES ('Servicios')")

    def agregar_usuario(self):
        # Intentar leer el valor del archivo de control
        try:
            with open('control.txt', 'r') as f:
                control = f.read().strip()
        except FileNotFoundError:
            # Si el archivo no existe, asumir que la función no se ha ejecutado antes
            control = 'False'
        
        # Verificar si la función ya se ha ejecutado antes
        if control == 'True':
            return
        
        self.cursor_conexion = self.conexion.cursor()
        usuario = 'lsoriano'
        contraseña = '1234567890'
        # Verificar si el usuario ya existe
        self.cursor_conexion.execute("SELECT * FROM USUARIOS WHERE NICKNAME=?", (usuario,))
        if self.cursor_conexion.fetchone() is not None:
            return

        # Convertimos la contraseña en un arreglo de bytes
        bytes = contraseña.encode('utf-8')
        # Generamos salt
        salt = bcrypt.gensalt()
        # Hacemos el Hash a la contraseña
        resultado = bcrypt.hashpw(bytes, salt)

        # Generar datos aleatorios para los demás campos
        nombre = "Luis Arturo"
        apellido1 = "Soriano"
        apellido2 = "Avendaño"
        email = f"{apellido1}.{apellido2}@gmail.com"
        status = 1
        numero = random.randint(1000000000, 9999999999)
        respuesta = "Respuesta" + str(random.randint(1, 100))
        pregunta = random.randint(1, 10)

        # Insertar el usuario en la tabla
        self.cursor_conexion.execute("INSERT INTO USUARIOS ('NOMBRE(S)', APELLIDO_PATERNO, APELLIDO_MATERNO, NICKNAME, CONTRASEÑA, CORREO, ESTATUS, TELEFONO, RESPUESTAS, PREGUNTAS) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (nombre, apellido1, apellido2, usuario, resultado, email, status, numero, respuesta, pregunta))
        self.conexion.commit()
        self.cursor_conexion.close()
        
        # Cambiar el valor en el archivo de control a True
        with open('control.txt', 'w') as f:
            f.write('True')


