import flet as ft
import sqlite3
import datetime

# --- BASE DE DATOS ---
def inicializar_bd():
    conn = sqlite3.connect("obra_unssx.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            item TEXT,
            avance TEXT,
            clima TEXT
        )
    """)
    conn.commit()
    conn.close()

def guardar_registro(fecha, item, avance, clima):
    conn = sqlite3.connect("obra_unssx.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO diario (fecha, item, avance, clima) VALUES (?, ?, ?, ?)",
                   (fecha, item, avance, clima))
    conn.commit()
    conn.close()

def obtener_registros():
    conn = sqlite3.connect("obra_unssx.db")
    cursor = conn.cursor()
    cursor.execute("SELECT fecha, item, avance, clima FROM diario ORDER BY id DESC")
    datos = cursor.fetchall()
    conn.close()
    return datos

# --- INTERFAZ ---
def main(page: ft.Page):
    page.title = "Diario de Obra UNSXX - Jhulian"
    page.scroll = "auto"
    
    inicializar_bd()

    txt_item = ft.TextField(label="Item de Obra")
    txt_avance = ft.TextField(label="Avance / Personal")
    drop_clima = ft.Dropdown(
        label="Clima",
        options=[
            ft.dropdown.Option("Soleado"),
            ft.dropdown.Option("Nublado"),
            ft.dropdown.Option("Lluvia"),
            ft.dropdown.Option("Helada"),
        ],
        value="Soleado"
    )

    tabla_historial = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Item")),
            ft.DataColumn(ft.Text("Avance")),
            ft.DataColumn(ft.Text("Clima")),
        ],
        rows=[]
    )

    def actualizar_tabla():
        tabla_historial.rows.clear()
        for fila in obtener_registros():
            tabla_historial.rows.append(
                ft.DataRow(cells=[ft.DataCell(ft.Text(str(f))) for f in fila])
            )
        page.update()

    def click_guardar(e):
        if not txt_item.value or not txt_avance.value:
            page.snack_bar = ft.SnackBar(ft.Text("Faltan datos"))
            page.snack_bar.open = True
            page.update()
            return
        
        fecha = datetime.datetime.now().strftime("%d/%m/%Y")
        guardar_registro(fecha, txt_item.value, txt_avance.value, drop_clima.value)
        txt_item.value = ""
        txt_avance.value = ""
        actualizar_tabla()

    btn_guardar = ft.ElevatedButton(
        "Guardar Jornada", 
        icon="save", 
        on_click=click_guardar
    )

    page.add(
        ft.Text("CONTROL DIGITAL DE OBRA - UNSXX", size=25, weight="bold"),
        txt_item,
        txt_avance,
        drop_clima,
        btn_guardar,
        ft.Divider(),
        ft.Text("Historial:", weight="bold"),
        tabla_historial
    )
    
    actualizar_tabla()

if __name__ == "__main__":
    ft.app(target=main)