import flet as ft
import os
from background_remover import BackgroundRemover

class BackgroundRemoverApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.directory_path = None
        self.filename_list = []
        
        # Lista para guardar referencias a los textos que deben cambiar de tamaño
        self.responsive_texts = []
        
        self._setup_page()
        self._create_components()
        self._build_ui()
        
        # Ajuste inicial
        self._resize_text(None)

    def _setup_page(self):
        self.page.title = "Background Remover"
        self.page.bgcolor = "#5d58d7"
        
        # Dimensiones iniciales
        self.page.window.height = 950
        self.page.window.width = 600
        self.page.window.min_width = 400 
        
        # Habilitar scroll automático
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        # Conectamos el evento de cambio de tamaño
        self.page.on_resized = self._resize_text

    # --- HELPER PARA TEXTO RESPONSIVO ---
    def _create_resp_text(self, text, base_size, weight=None, color=None, italic=False, align=None):
        """Crea un texto y lo registra para ser redimensionado automáticamente."""
        txt_obj = ft.Text(
            value=text,
            size=base_size,
            weight=weight,
            color=color,
            italic=italic,
            text_align=align
        )
        self.responsive_texts.append({"obj": txt_obj, "base_size": base_size})
        return txt_obj

    def _create_components(self):
        self.default_folder_check = ft.Checkbox(
            label="Usar carpeta por defecto",
            value=False,
            on_change=self._checkbox_changed,
            check_color="#e94560",
            label_style=ft.TextStyle(color="#ffffff", size=14)
        )

        self.output_folder_textfield = ft.TextField(
            label="Carpeta de salida personalizada",
            autofocus=False,
            bgcolor="#16213e",
            color="#ffffff",
            border_color="#e94560",
            height=60,
            border_radius=10,
            content_padding=ft.padding.all(15),
            expand=True
        )

        self.file_picker = ft.FilePicker(on_result=self._pick_files_result)

        # Texto del botón (responsivo)
        self.txt_btn_pick = self._create_resp_text("Seleccionar Imagenes", 14, color="#ffffff")

        self.btn_pick_files = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.icons.CLOUD_UPLOAD, color="#ffffff"),
                self.txt_btn_pick
            ], alignment=ft.MainAxisAlignment.CENTER),
            on_click=lambda _: self.file_picker.pick_files(
                allow_multiple=True,
                allowed_extensions=["png", "jpg", "jpeg", "bmp", "webp"]
            ),
            bgcolor="#aa77c3",
            width=250, 
            height=50,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12)
            )
        )

        self.select_files_info = ft.Text(
            "Ningun archivo seleccionado",
            color="#a0a0a0",
            size=14,
            text_align=ft.TextAlign.CENTER
        )

        
        self.txt_btn_extract = self._create_resp_text("Remover fondo", 16, weight=ft.FontWeight.BOLD, color="#ffffff")

        self.btn_extract = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.icons.AUTO_FIX_HIGH, color="#ffffff"),
                self.txt_btn_extract
            ], alignment=ft.MainAxisAlignment.CENTER),
            on_click=self._process_images_ui,
            bgcolor="#e94560",
            height=60,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=15),
                elevation=8
            )
        )

        self.progress_bar = ft.ProgressBar(
            visible=False,
            color="#e94560",
            bgcolor="#16213e",
            height=8
        )

        self.progress_text = ft.Text(
            "",
            visible=False,
            color="#ffffff",
            size=14,
            text_align=ft.TextAlign.CENTER
        )

        self.page.overlay.append(self.file_picker)

    def _build_ui(self):
        # 1. Títulos Responsivos
        main_title = self._create_resp_text(
            "Background Remover", 
            base_size=32, 
            weight=ft.FontWeight.BOLD, 
            color="#ffffff", 
            align=ft.TextAlign.CENTER
        )
        
        sub_title = self._create_resp_text(
            "Elimina fondos de imagenes de forma rapida y sencilla",
            base_size=16,
            italic=True,
            color="#ffffff",
            align=ft.TextAlign.CENTER
        )

        header = ft.Column([
            main_title, 
            sub_title
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        # 2. Config Card
        title_config = self._create_resp_text("Configuracion", 18, ft.FontWeight.BOLD, "#ffffff")
        
        config_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.SETTINGS, color="#e94560", size=20),
                    title_config
                ], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=10),
                self.default_folder_check,
                ft.Container(height=10),
                ft.Row([self.output_folder_textfield]) 
            ], spacing=5),
            bgcolor="#16213e",
            padding=ft.padding.all(20),
            border_radius=15,
            border=ft.border.all(1, "#0f3460"),
        )

        # 3. Files Card
        title_files = self._create_resp_text("Selección de Archivos", 18, ft.FontWeight.BOLD, "#ffffff")
        
        files_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.IMAGE, color="#e94560", size=20),
                    title_files
                ], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=15),
                ft.Row([self.btn_pick_files], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=10),
                self.select_files_info,
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="#16213e",
            padding=ft.padding.all(20),
            border_radius=15,
            border=ft.border.all(1, "#0f3460"),
        )

        # 4. Process Card
        title_process = self._create_resp_text("Procesamiento", 18, ft.FontWeight.BOLD, "#ffffff")

        process_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.PSYCHOLOGY, color="#e94560", size=20),
                    title_process
                ], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=20),
                ft.Container(self.btn_extract, width=None, alignment=ft.alignment.center),
                ft.Container(height=15),
                self.progress_bar,
                ft.Container(height=10),
                self.progress_text
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="#16231e",
            padding=ft.padding.all(20),
            border_radius=15,
            border=ft.border.all(1, "#0f3460"),
        )

        # Layout Principal (Columna interna)
        main_layout = ft.Column(
            controls=[
                header,
                ft.Divider(height=20, color="transparent"),
                config_card,
                files_card,
                process_card,
            ],
            scroll=ft.ScrollMode.HIDDEN, 
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH, 
        )

        # Contenedor Maestro (Wrapper)
        self.responsive_container = ft.Container(
            content=main_layout,
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            alignment=ft.alignment.top_center,
        )

        self.page.add(self.responsive_container)

        # --REDIMENSIONAMIENTO 
    def _resize_text(self, e):
        # Ancho actual (fallback a 600 si es None al inicio)
        current_width = self.page.window.width if self.page.window.width else 600
        
        # --- CONTROL MANUAL DEL ANCHO MÁXIMO ---
        # Si la ventana es muy ancha (>850), fijamos el ancho del contenedor.
        # Si es pequeña, lo dejamos en None para que sea fluido.
        if current_width > 850:
            self.responsive_container.width = 850
        else:
            self.responsive_container.width = None 

        # --- ESCALADO DE TEXTO ---
        scale_factor = current_width / 600
        # Límites
        scale_factor = max(0.85, min(scale_factor, 1.25))

        for item in self.responsive_texts:
            text_obj = item["obj"]
            base_size = item["base_size"]
            new_size = base_size * scale_factor
            text_obj.size = int(new_size)
            
        self.page.update()

    def _checkbox_changed(self, e: ft.ControlEvent):
        self.output_folder_textfield.disabled = e.control.value
        self.output_folder_textfield.bgcolor = "#a2a2a4" if e.control.value else "#16213e"
        self.page.update()

    def _pick_files_result(self, e: ft.FilePickerResultEvent):
        if e.files:
            file_count = len(e.files)
            first_file_path = e.files[0].path
            self.directory_path = os.path.dirname(first_file_path)

            self.filename_list = [filename.name for filename in e.files]
            
            self.select_files_info.value = f"{file_count} Archivo(s) seleccionados\nCarpeta: {self.directory_path}"
            self.select_files_info.color = "#4caf50"
        else:
            self.select_files_info.value = f"Seleccion Cancelada"
            self.select_files_info.color = "#f44336"

        self.page.update()

    def _process_images_ui(self, e: ft.ControlEvent):
        self.progress_bar.visible = True
        self.progress_bar.value = 0
        self.progress_text.visible = True
        self.progress_text.value = "Iniciando procesamiento..."
        self.progress_text.color = "#ffffff"
        self.btn_extract.disabled = True
        self.btn_extract.bgcolor = "#666666"
        self.page.update()
        try:
            output_folder = 'Carpeta_Defecto' if self.default_folder_check.value else self.output_folder_textfield.value

            if not output_folder.strip() and not self.default_folder_check.value:
                    self._show_error("Por favor especifique una carpeta de salida")
                    return
                
            remover = BackgroundRemover(self.directory_path, output_folder)
            remover.process_images(self.filename_list, self._update_progress)

            self._show_success("Imagen procesada exitosamente")
        
        except Exception as e:
            self._show_error(f"Ha ocurrido un error: {e}")
        finally:
            self._reset_ui()
    
    def _update_progress(self, processed, total, current_file):
        progress = processed / total
        self.progress_bar.value = progress
        self.progress_text.value = f"Procesando: {current_file} ({processed}/{total})"
        self.page.update()

    def _reset_ui(self):
        self.btn_extract.disabled = False
        self.btn_extract.bgcolor = "#e94560"
        self.page.update()

    def _show_error(self, message):
        dlg = ft.AlertDialog(
            title=ft.Text("Error", color="#f44336"),
            content=ft.Text(message, color="#ffffff"),
            bgcolor="#16213e",
            actions=[
                ft.TextButton(
                    "OK",
                    on_click=lambda e: self.page.close(dlg),
                    style=ft.ButtonStyle(color="#e94560")
                )
            ]
        )
        self.page.open(dlg)

    def _show_success(self, message):
        dlg = ft.AlertDialog(
            title=ft.Text("Exito", color="#4caf50"),
            content=ft.Text(message, color="#ffffff"),
            bgcolor="#16213e",
            actions=[
                ft.TextButton(
                    "OK",
                    on_click=lambda e: self.page.close(dlg),
                    style=ft.ButtonStyle(color="#4caf50")
                )
            ]
        )
        self.page.open(dlg)

def main(page: ft.Page):
    obj = BackgroundRemoverApp(page)

ft.app(target=main)