import flet as ft

def main(page: ft.Page):
    page.title = "Control de Materiales"
    page.window_width = 650
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # --- COMPONENTES ---
    txt_material = ft.TextField(label="Material", width=200)
    txt_ingreso = ft.TextField(label="Ingreso", width=100, value="0")
    txt_salida = ft.TextField(label="Salida", width=100, value="0")
    
    # Definimos la tabla
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Material")),
            ft.DataColumn(ft.Text("Ingreso")),
            ft.DataColumn(ft.Text("Salida")),
            ft.DataColumn(ft.Text("Stock")),
        ],
        rows=[]
    )

    # --- FUNCIONES DE LÓGICA ---

    def agregar_material(e):
        try:
            neto = float(txt_ingreso.value) - float(txt_salida.value)
            nueva_fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(txt_material.value)),
                    ft.DataCell(ft.Text(txt_ingreso.value)),
                    ft.DataCell(ft.Text(txt_salida.value)),
                    ft.DataCell(ft.Text(str(neto))),
                ]
            )
            tabla.rows.append(nueva_fila)
            # Limpiamos campos
            txt_material.value = ""
            txt_ingreso.value = "0"
            txt_salida.value = "0"
            page.update()
        except ValueError:
            pass

    def borrar_ultimo(e):
        if tabla.rows:
            tabla.rows.pop() # Elimina el último elemento de la lista
            page.update()

    def limpiar_todo(e):
        tabla.rows.clear() # Vacía la lista por completo
        page.update()

    # --- BOTONES ---
    btn_add = ft.ElevatedButton("Agregar", icon=ft.Icons.ADD, on_click=agregar_material)
    btn_delete = ft.TextButton("Borrar Último", icon=ft.Icons.DELETE_OUTLINE, on_click=borrar_ultimo, icon_color="red")
    btn_clear = ft.TextButton("Limpiar Tabla", icon=ft.Icons.CLEAR_ALL, on_click=limpiar_todo)

    # --- DISEÑO ---
    page.add(
        ft.Text("Gestión de Almacén", size=25, weight="bold"),
        ft.Row([txt_material, txt_ingreso, txt_salida]),
        ft.Row([btn_add, btn_delete, btn_clear], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        ft.Column([tabla], scroll=ft.ScrollMode.ALWAYS, expand=True)
    )

if __name__ == "__main__":
    ft.app(target=main)