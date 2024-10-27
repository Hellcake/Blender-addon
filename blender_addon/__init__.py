bl_info = {
    "name": "Scene Save Plugin Hellcake",
    "author": "Hellcake",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Scene Save",
    "description": "Save scene and send data to server",
    "category": "Scene",
}

import bpy
import requests
from datetime import datetime
import os
import tempfile

class SceneSavePanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Scene Save"
    bl_idname = "VIEW3D_PT_scene_save_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Scene Save'
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("scene.save_and_send", text="Save Scene", icon='FILE_TICK')

class SaveAndSendOperator(bpy.types.Operator):
    """Save scene and send data to server"""
    bl_idname = "scene.save_and_send"
    bl_label = "Save Scene"
    bl_description = "Save current scene and send data to server"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Получаем путь к текущему файлу blend
        blend_file_path = bpy.data.filepath
        
        # Если файл еще не сохранен, сохраняем его во временной директории
        if not blend_file_path:
            # Создаем временную директорию, если её нет
            temp_dir = os.path.join(tempfile.gettempdir(), "blender_saves")
            os.makedirs(temp_dir, exist_ok=True)
            
            # Генерируем имя файла с временной меткой
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            blend_file_path = os.path.join(temp_dir, f"scene_{timestamp}.blend")
            
            try:
                bpy.ops.wm.save_as_mainfile(filepath=blend_file_path)
                self.report({'INFO'}, f"File saved to: {blend_file_path}")
            except Exception as e:
                self.report({'ERROR'}, f"Error saving file: {str(e)}")
                return {'CANCELLED'}
        else:
            try:
                bpy.ops.wm.save_mainfile()
                self.report({'INFO'}, "File saved successfully")
            except Exception as e:
                self.report({'ERROR'}, f"Error saving file: {str(e)}")
                return {'CANCELLED'}
            
        # Получаем имя пользователя из системы или используем дефолтное
        username = os.getenv('USERNAME', 'default_user')  # Используем USERNAME вместо USER для Windows
        
        # Отправляем данные на сервер
        try:
            response = requests.post(
                'http://localhost:8000/api/save/',
                json={
                    'username': username,
                    'file_path': blend_file_path
                }
            )
            
            if response.status_code == 201:
                self.report({'INFO'}, "Scene saved and data sent successfully")
            else:
                self.report({'ERROR'}, f"Error sending data: {response.text}")
                
        except requests.exceptions.RequestException as e:
            self.report({'ERROR'}, f"Connection error: {str(e)}")
            return {'CANCELLED'}
            
        return {'FINISHED'}

# Список классов для регистрации
classes = (
    SceneSavePanel,
    SaveAndSendOperator,
)

def register():
    print("Registering Scene Save Plugin...")  # Отладочное сообщение
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
            print(f"Successfully registered {cls.__name__}")  # Отладочное сообщение
        except Exception as e:
            print(f"Error registering {cls.__name__}: {str(e)}")

def unregister():
    print("Unregistering Scene Save Plugin...")  # Отладочное сообщение
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
            print(f"Successfully unregistered {cls.__name__}")  # Отладочное сообщение
        except Exception as e:
            print(f"Error unregistering {cls.__name__}: {str(e)}")

if __name__ == "__main__":
    register()