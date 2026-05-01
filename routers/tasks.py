from fastapi import APIRouter

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

tasks = []
task_counter = 1 # simula um ID unico

@router.post('', status_code=201) # cria objetos
def create_task(task: dict):
    global task_counter
    new_task = {
        "id": task_counter,
        "title": task['title'],
        "done": False
    }
    tasks.append(new_task)
    task_counter += 1
    return new_task

@router.get("") # sem id especifico, retorna tudo
def get_tasks():
    return tasks

@router.get('/{task_id}') # lê informações, retorna ID especifico
def get_task(task_id: int):
    for task in tasks:
        if task['id'] == task_id:
            return task
    return {"error": "Task not found"}

@router.put("/{task_id}") # atualiza, update
def update_task(task_id: int, updated: dict):
    for task in tasks:
        if task['id'] == task_id:
            task['title'] = updated.get('title', task['title']) # .get = método de dicts, serve pra pegar um valor sem dar errro caso a chave não exista
            task['done'] = updated.get('done', task['done'])
            return task
    return {"error": "Task not found"}

@router.delete('/{task_id}', status_code=204)
def delete_task(task_id: int):
    global tasks
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            return
    return {"error": "Task not found"}
