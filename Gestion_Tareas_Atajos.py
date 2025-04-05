import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

# Variables globales para los widgets principales
var_nueva_tarea = None
var_categoria = None
fecha_tarea = None
tree_tareas = None


# Función para mostrar un mensaje emergente al pasar el cursor
def mostrar_mensaje(evento, widget, texto):
    global ventana_emergente
    # Obtiene posición del widget
    x, y, _, _ = widget.bbox("insert")
    x += widget.winfo_rootx() + 25
    y += widget.winfo_rooty() + 25

    # Crea una nueva ventana sin bordes
    ventana_emergente = tk.Toplevel(widget)
    ventana_emergente.wm_overrideredirect(True)
    ventana_emergente.wm_geometry(f"+{x}+{y}")

    # Muestra el texto dentro de la ventana emergente
    etiqueta = ttk.Label(ventana_emergente, text=texto, background="#ffffe0", relief="solid", borderwidth=1)
    etiqueta.pack()


# Función para ocultar el mensaje emergente cuando el cursor sale
def ocultar_mensaje(evento):
    global ventana_emergente
    if ventana_emergente:
        ventana_emergente.destroy()
        ventana_emergente = None


# Función para aplicar estilos a los widgets
def configurar_estilos():
    estilo = ttk.Style()
    estilo.configure("TButton", padding=5, relief="flat", font=("Arial", 10))
    estilo.configure("TLabel", font=("Arial", 10))
    estilo.configure("TFrame", background="#f0f0f0")
    estilo.configure("TCombobox", padding=5)


# Función que asigna atajos de teclado a funciones específicas
def configurar_atajos(root):
    root.bind("<Alt-c>", lambda event: marcar_completada())
    root.bind("<Delete>", lambda event: eliminar_tarea())
    root.bind("<Escape>", lambda event: root.quit())
    root.bind("<Alt-e>", lambda event: editar_tarea())


# Función para añadir mensaje emergente a un widget
def añadir_mensaje_emergente(widget, texto):
    widget.bind("<Enter>", lambda e: mostrar_mensaje(e, widget, texto))
    widget.bind("<Leave>", ocultar_mensaje)


# Función para añadir una nueva tarea a la lista
def añadir_tarea(event=None):
    texto = var_nueva_tarea.get().strip()  # Obtiene texto de entrada
    categoria = var_categoria.get()  # Obtiene categoría seleccionada
    fecha = fecha_tarea.get()  # Obtiene la fecha seleccionada

    # Validación: si el campo de texto está vacío, muestra advertencia
    if not texto:
        messagebox.showwarning("Advertencia", "Por favor, ingrese una tarea.")
        return

    # Inserta una nueva fila en el Treeview
    tree_tareas.insert("", tk.END, values=("Pendiente", texto, categoria, fecha), tags=("pendiente",))
    tree_tareas.tag_configure("pendiente", background="#ffdddd")  # Aplica color a las tareas pendientes
    var_nueva_tarea.set("")  # Limpia el campo de entrada


# Función para marcar una tarea como completada
def marcar_completada():
    seleccion = tree_tareas.selection()  # Obtiene la tarea seleccionada
    if not seleccion:
        messagebox.showinfo("Información", "Por favor, seleccione una tarea.")
        return

    item = seleccion[0]
    valores = tree_tareas.item(item, "values")
    # Actualiza el estado a "Completada"
    tree_tareas.item(item, values=("Completada", valores[1], valores[2], valores[3]), tags=("completada",))
    tree_tareas.tag_configure("completada", background="#d0ffd0")  # Aplica color a tareas completadas


# Función para editar una tarea existente
def editar_tarea():
    seleccion = tree_tareas.selection()
    if not seleccion:
        messagebox.showinfo("Información", "Por favor, seleccione una tarea.")
        return
    item = seleccion[0]
    valores = tree_tareas.item(item, "values")

    # Rellena los campos con los valores actuales de la tarea
    var_nueva_tarea.set(valores[1])
    var_categoria.set(valores[2])
    fecha_tarea.set_date(valores[3])

    # Elimina la tarea para reemplazarla luego
    tree_tareas.delete(item)


# Función para eliminar una tarea seleccionada
def eliminar_tarea():
    seleccion = tree_tareas.selection()
    if seleccion:
        if messagebox.askyesno("Confirmación", "¿Está seguro de que desea eliminar esta tarea?"):
            tree_tareas.delete(seleccion[0])  # Elimina la fila seleccionada


# Función principal para construir la interfaz
def crear_interfaz(root):
    global var_nueva_tarea, var_categoria, fecha_tarea, tree_tareas

    # Configura ventana principal
    root.title("Gestor de Tareas")
    root.geometry("620x480")
    root.resizable(True, True)

    # Variables para los campos de entrada
    var_nueva_tarea = tk.StringVar()
    var_categoria = tk.StringVar()

    configurar_estilos()  # Aplica estilos visuales
    configurar_atajos(root)  # Asigna atajos de teclado

    frame_principal = ttk.Frame(root, padding="10")
    frame_principal.pack(fill=tk.BOTH, expand=True)

    # Título de la aplicación
    lbl_titulo = ttk.Label(frame_principal, text="Gestor de Tareas", font=("Arial", 16, "bold"))
    lbl_titulo.pack(pady=10)

    # Frame para ingresar nueva tarea
    frame_entrada = ttk.Frame(frame_principal)
    frame_entrada.pack(fill=tk.X, pady=5)

    ttk.Label(frame_entrada, text="Nueva tarea:").pack(side=tk.LEFT, padx=5)
    entrada_tarea = ttk.Entry(frame_entrada, textvariable=var_nueva_tarea, width=30)
    entrada_tarea.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    entrada_tarea.bind("<Return>", añadir_tarea)  # Presionar Enter agrega tarea
    entrada_tarea.focus()

    # Frame para categoría y fecha
    frame_opciones = ttk.Frame(frame_principal)
    frame_opciones.pack(fill=tk.X, pady=5)

    categorias = ["Educativa", "Familiar", "Salud", "Laboral", "Deportiva", "Viajes"]
    var_categoria.set("Seleccione categoria")
    menu_categorias = ttk.Combobox(frame_opciones, textvariable=var_categoria, values=categorias, state="readonly")
    menu_categorias.pack(side=tk.LEFT, padx=5)

    # Selector de fecha
    fecha_tarea = DateEntry(frame_opciones, width=12, background='darkblue', foreground='white', borderwidth=2)
    fecha_tarea.pack(side=tk.LEFT, padx=5)

    # Botón para añadir tarea
    btn_añadir = ttk.Button(frame_opciones, text="Añadir Tarea", command=añadir_tarea)
    btn_añadir.pack(side=tk.LEFT, padx=5)

    # Frame donde se muestran las tareas
    frame_lista = ttk.LabelFrame(frame_principal, text="Tareas Pendientes", padding="5")
    frame_lista.pack(fill=tk.BOTH, expand=True, pady=10)
    columnas = ("estado", "tarea", "categoria", "fecha")
    tree_tareas = ttk.Treeview(frame_lista, columns=columnas, show="headings", selectmode="browse")

    # Encabezados de columnas
    for col in columnas:
        tree_tareas.heading(col, text=col.capitalize())

    # Ajuste de ancho de columnas
    tree_tareas.column("estado", width=100, anchor=tk.CENTER)
    tree_tareas.column("tarea", width=200)
    tree_tareas.column("categoria", width=100, anchor=tk.CENTER)
    tree_tareas.column("fecha", width=100, anchor=tk.CENTER)
    tree_tareas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Barra de desplazamiento vertical
    scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=tree_tareas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree_tareas.configure(yscrollcommand=scrollbar.set)

    # Frame para botones de acción
    frame_botones = ttk.Frame(frame_principal)
    frame_botones.pack(fill=tk.X, pady=5)

    # Botón: marcar como completada
    btn_completar = ttk.Button(frame_botones, text="Marcar como Completada", command=marcar_completada)
    btn_completar.pack(side=tk.LEFT, padx=5)
    añadir_mensaje_emergente(btn_completar, "Atajo: Alt+C")

    # Botón: editar tarea
    btn_editar = ttk.Button(frame_botones, text="Editar Tarea", command=editar_tarea)
    btn_editar.pack(side=tk.LEFT, padx=5)
    añadir_mensaje_emergente(btn_editar, "Atajo: Alt+E")

    # Botón: eliminar tarea
    btn_eliminar = ttk.Button(frame_botones, text="Eliminar Tarea", command=eliminar_tarea)
    btn_eliminar.pack(side=tk.LEFT, padx=5)
    añadir_mensaje_emergente(btn_eliminar, "Atajo: Delete")


# Inicia la aplicación
ventana = tk.Tk()
crear_interfaz(ventana)
ventana.mainloop()