import locale
import os
from models.parser import TodoConfigParser

# Cache config parser instance
_config_parser = None
def get_config_parser():
    global _config_parser
    if _config_parser is None:
        _config_parser = TodoConfigParser()
    return _config_parser

# Translation dictionaries
translations = {
    "en": {
        "add_task": "Add Task",
        "edit_task": "Edit Task",
        "delete_task": "Delete Task",
        "mark_completed": "Mark as Completed",
        "mark_cancelled": "Mark as Cancelled",
        "all_projects": "All Projects",
        "Task description": "Task description",
        "All": "All",
        "On Time": "On Time",
        "Overdue": "Overdue",
        "Open": "Open",
        "Finished": "Finished",
        "Cancelled": "Cancelled",
        "Created": "Created",
        "Due": "Due",
        "Closed": "Closed",
        "Status": "Status",
        "open": "Open",
        "complete": "Complete",
        "cancelled": "Cancelled",
        "Add Task": "Add Task",
        "Add": "Add",
        "Edit Task": "Edit Task",
        "Save": "Save",
        "Delete task": "Delete task",
        "Delete": "Delete",
        "Cancel": "Cancel",
        "This action can't be undone.": "This action can't be undone.",
        "Enter project name:": "Enter project name:",
        "Edit project name:": "Edit project name:",
        "Delete project": "Delete project",
        "Add Project": "Add Project",
        "Edit Project": "Edit Project",
        "Delete Project": "Delete Project",
        "Mark as Completed": "Mark as Completed",
        "Mark as Cancelled": "Mark as Cancelled",
        "Open Configurations": "Toggle Configurations Panel",
        "Todo App": "Todo App",
        # Settings panel keys
        "Settings": "Settings",
        "Default Language:": "Default Language:",
        "Default Task Filter:": "Default Task Filter:",
        "Default Project:": "Default Project:",
        "Database Path:": "Database Path:",
        "Change": "Change",
        "System Default": "System Default",
        "English": "English",
        "Brazilian Portuguese": "Brazilian Portuguese",
        "All Projects": "All Projects",
        "Move Database": "Move Database",
        "Do you want to move the current database to the new location?\n\n": "Do you want to move the current database to the new location?\n\n",
        "Warning: If you press 'No', a new database will be created at the new location, and all current information will be unavailable.": "Warning: If you press 'No', a new database will be created at the new location, and all current information will be unavailable.",
        "Failed to move database": "Failed to move database",
        "Database location updated successfully.": "Database location updated successfully.",
        "Error": "Error",
        "Success": "Success",
        # Shortcut labels and messages
        "Shortcut Configuration:": "Shortcut Configuration:",
        "Add Project Shortcut:": "Add Project Shortcut:",
        "Edit Project Shortcut:": "Edit Project Shortcut:",
        "Delete Project Shortcut:": "Delete Project Shortcut:",
        "Add Task Shortcut:": "Add Task Shortcut:",
        "Edit Task Shortcut:": "Edit Task Shortcut:",
        "Remove Task Shortcut:": "Remove Task Shortcut:",
        "Mark Completed Shortcut:": "Mark Completed Shortcut:",
        "Mark Canceled Shortcut:": "Mark Canceled Shortcut:",
        "All Projects Shortcut:": "All Projects Shortcut:",
        "Config Panel Shortcut:": "Config Panel Shortcut:",
        "Filter All Shortcut:": "Filter All Shortcut:",
        "On-Time Shortcut:": "On-Time Shortcut:",
        "Overdue Shortcut:": "Overdue Shortcut:",
        "Filter Active Shortcut:": "Filter Active Shortcut:",
        "Filter Completed Shortcut:": "Filter Completed Shortcut:",
        "Filter Canceled Shortcut:": "Filter Canceled Shortcut:",
        "Select Project Shortcut:": "Select Project Shortcut:",
        "Select Tasks Shortcut:": "Select Tasks Shortcut:",
        "Shortcut cannot be empty.": "Shortcut cannot be empty.",
        "Invalid shortcut format.": "Invalid shortcut format.",
        "Shortcut already used by '{act}'.": "Shortcut already used by '{act}'.",
    },
    "pt": {
        "add_task": "Adicionar Tarefa",
        "edit_task": "Editar Tarefa",
        "delete_task": "Excluir Tarefa",
        "mark_completed": "Marcar como Concluída",
        "mark_cancelled": "Marcar como Cancelada",
        "all_projects": "Todos os Projetos",
        "Task description": "Descrição da Tarefa",
        "All": "Todas",
        "On Time": "No Prazo",
        "Overdue": "Atrasadas",
        "Open": "Abertas",
        "Finished": "Concluídas",
        "Cancelled": "Canceladas",
        "Created": "Criado",
        "Due": "Prazo",
        "Closed": "Fechado",
        "Status": "Status",
        "open": "Aberto",
        "complete": "Concluído",
        "cancelled": "Cancelado",
        "Add Task": "Adicionar Tarefa",
        "Add": "Adicionar",
        "Edit Task": "Editar Tarefa",
        "Save": "Salvar",
        "Delete Task": "Excluir tarefa",
        "Delete": "Excluir",
        "Cancel": "Cancelar",
        "This action can't be undone.": "Esta ação não pode ser desfeita.",
        "Enter project name:": "Digite o nome do projeto:",
        "Edit project name:": "Editar o nome do projeto:",
        "Delete project": "Excluir projeto",
        "Add Project": "Adicionar Projeto",
        "Edit Project": "Editar Projeto",
        "Delete Project": "Excluir Projeto",
        "Mark as Completed": "Marcar como Concluída",
        "Mark as Cancelled": "Marcar como Cancelada",
        "Open Configurations": "Alternar Painel de Configurações",
        "Todo App": "Aplicativo de Tarefas",
        # Settings panel keys
        "Settings": "Configurações",
        "Default Language:": "Idioma Padrão:",
        "Default Task Filter:": "Filtro de Tarefas Padrão:",
        "Default Project:": "Projeto Padrão:",
        "Database Path:": "Caminho do Banco de Dados:",
        "Change": "Alterar",
        "System Default": "Padrão do Sistema",
        "English": "Inglês",
        "Brazilian Portuguese": "Português Brasileiro",
        "All Projects": "Todos os Projetos",
        "Move Database": "Mover Banco de Dados",
        "Do you want to move the current database to the new location?\n\n": "Deseja mover o banco de dados atual para o novo local?\n\n",
        "Warning: If you press 'No', a new database will be created at the new location, and all current information will be unavailable.": "Atenção: Se você pressionar 'Não', um novo banco de dados será criado no novo local e todas as informações atuais ficarão indisponíveis.",
        "Failed to move database": "Falha ao mover o banco de dados",
        "Database location updated successfully.": "Localização do banco de dados atualizada com sucesso.",
        "Error": "Erro",
        "Success": "Sucesso",
        # Shortcut labels and messages
        "Shortcut Configuration:": "Configuração de Atalhos:",
        "Add Project Shortcut:": "Adicionar Projeto:",
        "Edit Project Shortcut:": "Editar Projeto:",
        "Delete Project Shortcut:": "Excluir Projeto:",
        "Add Task Shortcut:": "Adicionar Tarefa:",
        "Edit Task Shortcut:": "Editar Tarefa:",
        "Remove Task Shortcut:": "Remover Tarefa:",
        "Mark Completed Shortcut:": "Marcar Concluída:",
        "Mark Canceled Shortcut:": "Marcar Cancelada:",
        "All Projects Shortcut:": "Todos os Projetos:",
        "Config Panel Shortcut:": "Painel de Configurações:",
        "Filter All Shortcut:": "Filtrar Todos:",
        "On-Time Shortcut:": "No Prazo:",
        "Overdue Shortcut:": "Atrasadas:",
        "Filter Active Shortcut:": "Filtrar Ativas:",
        "Filter Completed Shortcut:": "Filtrar Concluídas:",
        "Filter Canceled Shortcut:": "Filtrar Canceladas:",
        "Select Project Shortcut:": "Selecionar Projeto:",
        "Select Tasks Shortcut:": "Selecionar Tarefas:",
        "Shortcut cannot be empty.": "O atalho não pode ficar vazio.",
        "Invalid shortcut format.": "Formato de atalho inválido.",
        "Shortcut already used by '{act}'.": "Atalho já usado por '{act}'.",
    },
}

def get_system_language():
    """Detect the system language and return 'en' or 'pt'."""
    lang_code = locale.getdefaultlocale()[0]
    if lang_code and lang_code.startswith("pt"):
        return "pt"
    return "en"

def translate(key):
    """Get the translation for the given key based on the system language."""
    # Try to get language from config
    config = get_config_parser()
    lang_setting = config.get("General", "default_language", fallback="System Default")
    if lang_setting == "System Default":
        lang = get_system_language()
    elif lang_setting == "English":
        lang = "en"
    elif lang_setting == "Brazilian Portuguese":
        lang = "pt"
    else:
        lang = get_system_language()
    return translations.get(lang, {}).get(key, key)  # Default to key if translation is missing
