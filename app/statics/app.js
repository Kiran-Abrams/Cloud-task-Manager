
const taskForm = document.getElementById("task-form");
const taskTitle = document.getElementById("task-title");
const taskDescription = document.getElementById("task-description");
const taskList = document.getElementById("task-list");
const taskCount = document.getElementById("task-count");
const formMessage = document.getElementById("form-message");
const connectionStatus = document.getElementById("connection-status");
const refreshButton = document.getElementById("refresh-button");

async function apiRequest(url, options = {}) {
    const response = await fetch(url, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {})
        }
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(data.error || `Request failed (${response.status})`);
    }

    return data;
}

async function checkHealth() {
    try {
        await apiRequest("/health");
        connectionStatus.textContent = "Services connected";
        connectionStatus.className = "status online";
    } catch {
        connectionStatus.textContent = "Service unavailable";
        connectionStatus.className = "status offline";
    }
}

function createTextElement(tag, className, text) {
    const element = document.createElement(tag);
    element.className = className;
    element.textContent = text;
    return element;
}

function renderTasks(tasks) {
    taskList.replaceChildren();

    const completedCount = tasks.filter(task => task.completed).length;
    taskCount.textContent =
        `${tasks.length} task${tasks.length === 1 ? "" : "s"} · ` +
        `${completedCount} completed`;

    if (tasks.length === 0) {
        taskList.append(
            createTextElement("p", "empty-state", "No tasks yet. Add your first task above.")
        );
        return;
    }

    for (const task of tasks) {
        const card = document.createElement("article");
        card.className = `task-card${task.completed ? " completed" : ""}`;

        const content = document.createElement("div");
        content.className = "task-content";

        content.append(
            createTextElement("h3", "task-title", task.title)
        );

        if (task.description) {
            content.append(
                createTextElement("p", "task-description", task.description)
            );
        }

        const actions = document.createElement("div");
        actions.className = "task-actions";

        const toggleButton = document.createElement("button");
        toggleButton.type = "button";
        toggleButton.className = "secondary";
        toggleButton.textContent = task.completed ? "Mark active" : "Complete";
        toggleButton.addEventListener("click", async () => {
            toggleButton.disabled = true;
            try {
                await apiRequest(`/api/tasks/${task.id}`, {
                    method: "PATCH",
                    body: JSON.stringify({ completed: !task.completed })
                });
                await loadTasks();
            } catch (error) {
                alert(error.message);
                toggleButton.disabled = false;
            }
        });

        const deleteButton = document.createElement("button");
        deleteButton.type = "button";
        deleteButton.className = "delete";
        deleteButton.textContent = "Delete";
        deleteButton.addEventListener("click", async () => {
            if (!confirm(`Delete "${task.title}"?`)) return;

            deleteButton.disabled = true;
            try {
                await apiRequest(`/api/tasks/${task.id}`, {
                    method: "DELETE"
                });
                await loadTasks();
            } catch (error) {
                alert(error.message);
                deleteButton.disabled = false;
            }
        });

        actions.append(toggleButton, deleteButton);
        card.append(content, actions);
        taskList.append(card);
    }
}

async function loadTasks() {
    refreshButton.disabled = true;
    taskCount.textContent = "Loading tasks...";

    try {
        const tasks = await apiRequest("/api/tasks");
        renderTasks(tasks);
    } catch (error) {
        taskList.replaceChildren(
            createTextElement("p", "empty-state", error.message)
        );
        taskCount.textContent = "Could not load tasks.";
    } finally {
        refreshButton.disabled = false;
    }
}

taskForm.addEventListener("submit", async event => {
    event.preventDefault();
    formMessage.textContent = "";

    const submitButton = taskForm.querySelector('button[type="submit"]');
    submitButton.disabled = true;

    try {
        await apiRequest("/api/tasks", {
            method: "POST",
            body: JSON.stringify({
                title: taskTitle.value.trim(),
                description: taskDescription.value.trim()
            })
        });

        taskForm.reset();
        formMessage.textContent = "";
        await loadTasks();
        taskTitle.focus();
    } catch (error) {
        formMessage.textContent = error.message;
    } finally {
        submitButton.disabled = false;
    }
});

refreshButton.addEventListener("click", loadTasks);

checkHealth();
loadTasks();
