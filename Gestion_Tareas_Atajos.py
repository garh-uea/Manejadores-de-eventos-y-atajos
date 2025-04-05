import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

# Clase para crear mensajes emergentes para los botones
class MensajeEmergente:
    def __init__(self, elemento, texto):
        self.elemento = elemento
        self.texto = texto
        self.ventana_emergente = None
        self.elemento.bind("<Enter>", self.mostrar_mensaje)
        self.elemento.bind("<Leave>", self.ocultar_mensaje)

    def mostrar_mensaje(self, evento=None):
        # Obtiene la posición del widget
        x, y, _, _ = self.elemento.bbox("insert")
        x += self.elemento.winfo_rootx() + 25
        y += self.elemento.winfo_rooty() + 25

        # Crea una ventana emergente
        self.ventana_emergente = tk.Toplevel(self.elemento)
        self.ventana_emergente.wm_overrideredirect(True)  # Elimina bordes de ventana
        self.ventana_emergente.wm_geometry(f"+{x}+{y}")

        # Crea una etiqueta con el texto del mensaje
        etiqueta = ttk.Label(self.ventana_emergente, text=self.texto, background="#ffffe0", relief="solid",
                             borderwidth=1)
        etiqueta.pack()

    def ocultar_mensaje(self, evento=None):
        # Destruye el mensaje cuando el ratón sale del elemento
        if self.ventana_emergente:
            self.ventana_emergente.destroy()
            self.ventana_emergente = None


class GestorTareas:
    def __init__(self, root):
        # Inicialización de la ventana principal
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("620x480")
        self.root.resizable(True, True)

        # Variables para almacenar datos de entrada
        self.var_nueva_tarea = tk.StringVar()
        self.var_categoria = tk.StringVar()

        # Configuración inicial de la interfaz
        self._crear_widgets()
        self._configurar_estilos()
        self._configurar_atajos()

    def _configurar_estilos(self):
        # Configuración de estilos para los widgets
        estilo = ttk.Style()
        estilo.configure("TButton", padding=5, relief="flat", font=("Arial", 10))
        estilo.configure("TLabel", font=("Arial", 10))
        estilo.configure("TFrame", background="#f0f0f0")
        estilo.configure("TCombobox", padding=5)

    def _configurar_atajos(self):
        # Configuración de atajos de teclado para las funciones principales
        self.root.bind("<Alt-c>", lambda event: self.marcar_completada())  # Alt+C para marcar como completada
        self.root.bind("<Delete>", lambda event: self.eliminar_tarea())  # Delete para eliminar tarea
        self.root.bind("<Escape>", lambda event: self.root.quit())  # Escape para salir
        self.root.bind("<Alt-e>", lambda event: self.editar_tarea())  # Alt+E para editar tarea

    def _crear_widgets(self):
        # Creación del frame principal
        frame_principal = ttk.Frame(self.root, padding="10")
        frame_principal.pack(fill=tk.BOTH, expand=True)

        # Título de la aplicación
        lbl_titulo = ttk.Label(frame_principal, text="Gestor de Tareas", font=("Arial", 16, "bold"))
        lbl_titulo.pack(pady=10)

        # Frame para la entrada de nuevas tareas
        frame_entrada = ttk.Frame(frame_principal)
        frame_entrada.pack(fill=tk.X, pady=5)

        lbl_nueva_tarea = ttk.Label(frame_entrada, text="Nueva tarea:")
        lbl_nueva_tarea.pack(side=tk.LEFT, padx=5)

        # Campo de entrada para la tarea
        entrada_tarea = ttk.Entry(frame_entrada, textvariable=self.var_nueva_tarea, width=30)
        entrada_tarea.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        entrada_tarea.bind("<Return>", self.añadir_tarea)  # Enter para añadir tarea
        entrada_tarea.focus()  # Foco inicial en el campo de entrada

        # Frame para opciones adicionales (categoría, fecha)
        frame_opciones = ttk.Frame(frame_principal)
        frame_opciones.pack(fill=tk.X, pady=5)

        # Menú desplegable para categorías
        categorias = ["Educativa", "Familiar", "Salud", "Laboral", "Deportiva", "Viajes"]
        self.var_categoria.set("Seleccione categoria")
        menu_categorias = ttk.Combobox(frame_opciones, textvariable=self.var_categoria, values=categorias,
                                       state="readonly")
        menu_categorias.pack(side=tk.LEFT, padx=5)

        # Selector de fecha
        self.fecha_tarea = DateEntry(frame_opciones, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.fecha_tarea.pack(side=tk.LEFT, padx=5)

        # Botón para añadir tarea
        btn_añadir = ttk.Button(frame_opciones, text="Añadir Tarea", command=self.añadir_tarea)
        btn_añadir.pack(side=tk.LEFT, padx=5)

        # Frame para la lista de tareas
        frame_lista = ttk.LabelFrame(frame_principal, text="Tareas Pendientes", padding="5")
        frame_lista.pack(fill=tk.BOTH, expand=True, pady=10)

        # Configuración del TreeView para mostrar las tareas
        columnas = ("estado", "tarea", "categoria", "fecha")
        self.tree_tareas = ttk.Treeview(frame_lista, columns=columnas, show="headings", selectmode="browse")
        self.tree_tareas.heading("estado", text="Estado")
        self.tree_tareas.heading("tarea", text="Tarea")
        self.tree_tareas.heading("categoria", text="Categoría")
        self.tree_tareas.heading("fecha", text="Fecha")

        # Configuración del ancho de las columnas
        self.tree_tareas.column("estado", width=100, anchor=tk.CENTER)
        self.tree_tareas.column("tarea", width=200)
        self.tree_tareas.column("categoria", width=100, anchor=tk.CENTER)
        self.tree_tareas.column("fecha", width=100, anchor=tk.CENTER)

        self.tree_tareas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Barra de desplazamiento para la lista de tareas
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tree_tareas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_tareas.configure(yscrollcommand=scrollbar.set)

        # Frame para los botones de acción
        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(fill=tk.X, pady=5)

        # Botón para marcar tarea como completada
        btn_completar = ttk.Button(frame_botones, text="Marcar como Completada", command=self.marcar_completada)
        btn_completar.pack(side=tk.LEFT, padx=5)
        # Añadir Mensaje Emergente para mostrar el atajo de teclado
        MensajeEmergente(btn_completar, "Atajo: Alt+C")

        # Botón para editar tarea
        btn_editar = ttk.Button(frame_botones, text="Editar Tarea", command=self.editar_tarea)
        btn_editar.pack(side=tk.LEFT, padx=5)
        # Añadir Mensaje Emergente para mostrar el atajo de teclado
        MensajeEmergente(btn_editar, "Atajo: Alt+E")

        # Botón para eliminar tarea
        btn_eliminar = ttk.Button(frame_botones, text="Eliminar Tarea", command=self.eliminar_tarea)
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        # Añadir Mensaje Emergente para mostrar el atajo de teclado
        MensajeEmergente(btn_eliminar, "Atajo: Delete")

    def añadir_tarea(self, event=None):
        # Obtener datos de la nueva tarea
        texto_tarea = self.var_nueva_tarea.get().strip()
        categoria = self.var_categoria.get()
        fecha = self.fecha_tarea.get()

        # Validar que se haya ingresado texto para la tarea
        if not texto_tarea:
            messagebox.showwarning("Advertencia", "Por favor, ingrese una tarea.")
            return

        # Insertar la nueva tarea en el TreeView
        self.tree_tareas.insert("", tk.END, values=("Pendiente", texto_tarea, categoria, fecha), tags=("pendiente",))
        self.tree_tareas.tag_configure("pendiente", background="#ffdddd")  # Fondo rojo claro para tareas pendientes
        self.var_nueva_tarea.set("")  # Limpiar el campo de entrada

    def marcar_completada(self):
        # Obtener la tarea seleccionada
        seleccion = self.tree_tareas.selection()
        if not seleccion:
            messagebox.showinfo("Información", "Por favor, seleccione una tarea.")
            return

        # Cambiar el estado de la tarea a "Completada"
        item = seleccion[0]
        valores = self.tree_tareas.item(item, "values")
        self.tree_tareas.item(item, values=("Completada", valores[1], valores[2], valores[3]), tags=("completada",))
        self.tree_tareas.tag_configure("completada", background="#d0ffd0")  # Fondo verde claro para tareas completadas

    def editar_tarea(self):
        # Obtener la tarea seleccionada
        seleccion = self.tree_tareas.selection()
        if not seleccion:
            messagebox.showinfo("Información", "Por favor, seleccione una tarea.")
            return

        # Cargar los datos de la tarea en los campos de entrada
        item = seleccion[0]
        valores = self.tree_tareas.item(item, "values")
        self.var_nueva_tarea.set(valores[1])
        self.var_categoria.set(valores[2])
        self.fecha_tarea.set_date(valores[3])

        # Eliminar la tarea del TreeView para ser reemplazada
        self.tree_tareas.delete(item)

    def eliminar_tarea(self):
        # Obtener la tarea seleccionada
        seleccion = self.tree_tareas.selection()
        if seleccion:
            # Confirmar la eliminación
            if messagebox.askyesno("Confirmación", "¿Está seguro de que desea eliminar esta tarea?"):
                self.tree_tareas.delete(seleccion[0])

# Iniciar la aplicación
ventana = tk.Tk()
app = GestorTareas(ventana)
ventana.mainloop()