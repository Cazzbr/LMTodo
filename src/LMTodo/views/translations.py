import locale

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
    },
    "pt": {
        "add_task": "Adicionar Tarefa",
        "edit_task": "Editar Tarefa",
        "delete_task": "Excluir Tarefa",
        "mark_completed": "Marcar como Concluída",
        "mark_cancelled": "Marcar como Cancelada",
        "all_projects": "Todos os Projetos",
        "Task description": "Descrição da Tarefa",
        "All": "Todos",
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
    },
}

def get_system_language():
    """Detect the system language and return 'en' or 'pt'."""
    lang_code = locale.getdefaultlocale()[0]
    if lang_code.startswith("pt"):
        return "pt"
    return "en"

def translate(key):
    """Get the translation for the given key based on the system language."""
    lang = get_system_language()
    return translations.get(lang, {}).get(key, key)  # Default to key if translation is missing
