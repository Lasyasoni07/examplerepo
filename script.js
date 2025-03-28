let todoItemsContainer = document.getElementById("todoItemsContainer");
let addTodoButton = document.getElementById("addTodoButton");

let todoList = JSON.parse(localStorage.getItem("todoList")) || [];

let todosCount = parseInt(localStorage.getItem("todosCount")) || 0;

function saveTodos() {
    localStorage.setItem("todoList", JSON.stringify(todoList));
    localStorage.setItem("todosCount", todosCount);
}

function onTodoStatusChange(checkboxId, labelId, uniqueNo) {
    let checkboxElement = document.getElementById(checkboxId);
    let labelElement = document.getElementById(labelId);
    
    labelElement.classList.toggle('checked');

    let todo = todoList.find(todo => todo.uniqueNo === uniqueNo);
    if (todo) {
        todo.completed = checkboxElement.checked;
        saveTodos();
    }
}

function onDeleteTodo(todoId, uniqueNo) {
    let todoElement = document.getElementById(todoId);
    todoItemsContainer.removeChild(todoElement);

    todoList = todoList.filter(todo => todo.uniqueNo !== uniqueNo);
    saveTodos();
}

function onEditTodo(labelId, uniqueNo) {
    let labelElement = document.getElementById(labelId);
    let todo = todoList.find(todo => todo.uniqueNo === uniqueNo);
    
    if (!todo) return;

    let inputElement = document.createElement("input");
    inputElement.type = "text";
    inputElement.value = todo.text;
    inputElement.classList.add("edit-todo-input");

    labelElement.replaceWith(inputElement);
    inputElement.focus();

    inputElement.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            let newText = inputElement.value.trim();
            if (newText === "") {
                alert("Task cannot be empty");
                return;
            }
            todo.text = newText;
            saveTodos();

            let newLabelElement = document.createElement("label");
            newLabelElement.setAttribute("for", "checkbox" + uniqueNo);
            newLabelElement.id = labelId;
            newLabelElement.classList.add("checkbox-label");
            newLabelElement.textContent = newText;
            inputElement.replaceWith(newLabelElement);
        }
    });

    inputElement.addEventListener("blur", function() {
        let newText = inputElement.value.trim();
        if (newText === "") {
            newText = todo.text; 
        }
        todo.text = newText;
        saveTodos();

        let newLabelElement = document.createElement("label");
        newLabelElement.setAttribute("for", "checkbox" + uniqueNo);
        newLabelElement.id = labelId;
        newLabelElement.classList.add("checkbox-label");
        newLabelElement.textContent = newText;
        inputElement.replaceWith(newLabelElement);
    });
}

function createAndAppendTodo(todo) {
    let todoId = 'todo' + todo.uniqueNo;
    let checkboxId = 'checkbox' + todo.uniqueNo;
    let labelId = 'label' + todo.uniqueNo;

    let todoElement = document.createElement("li");
    todoElement.classList.add("todo-item-container", "d-flex", "flex-row");
    todoElement.id = todoId;
    todoItemsContainer.appendChild(todoElement);

    let inputElement = document.createElement("input");
    inputElement.type = "checkbox";
    inputElement.id = checkboxId;
    inputElement.checked = todo.completed || false;

    inputElement.onclick = function() {
        onTodoStatusChange(checkboxId, labelId, todo.uniqueNo);
    };

    inputElement.classList.add("checkbox-input");
    todoElement.appendChild(inputElement);

    let labelContainer = document.createElement("div");
    labelContainer.classList.add("label-container", "d-flex", "flex-row");
    todoElement.appendChild(labelContainer);

    let labelElement = document.createElement("label");
    labelElement.setAttribute("for", checkboxId);
    labelElement.id = labelId;
    labelElement.classList.add("checkbox-label");
    labelElement.textContent = todo.text;
    if (todo.completed) {
        labelElement.classList.add("checked");
    }
    labelContainer.appendChild(labelElement);

    let actionContainer = document.createElement("div");
    actionContainer.classList.add("delete-icon-container");
    labelContainer.appendChild(actionContainer);

    let editIcon = document.createElement("i");
    editIcon.classList.add("fas", "fa-edit", "edit-icon");
    editIcon.onclick = function () {
        onEditTodo(labelId, todo.uniqueNo);
    };
    actionContainer.appendChild(editIcon);

    let deleteIcon = document.createElement("i");
    deleteIcon.classList.add("far", "fa-trash-alt", "delete-icon");
    deleteIcon.onclick = function () {
        onDeleteTodo(todoId, todo.uniqueNo);
    };
    actionContainer.appendChild(deleteIcon);
}

for (let todo of todoList) {
    createAndAppendTodo(todo);
}

function onAddTodo() {
    let userInputElement = document.getElementById("todoUserInput");
    let userInputValue = userInputElement.value.trim();

    if (userInputValue === "") {
        alert("Enter a valid task");
        return;
    }

    todosCount += 1;

    let newTodo = {
        text: userInputValue,
        uniqueNo: todosCount,
        completed: false
    };

    todoList.push(newTodo);
    saveTodos(); 

    createAndAppendTodo(newTodo);
    userInputElement.value = "";
}

addTodoButton.onclick = function () {
    onAddTodo();
};
