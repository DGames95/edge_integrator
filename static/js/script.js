let currentTask = null;

window.onload = requestNewTask()

function gaussianFunction(x) {
    return Math.exp(-Math.pow(x, 2));
}

function requestNewTask() {
    // Check if a current task already exists
    if (currentTask) {
        console.log("A task is already in progress. Finish it before requesting a new one.");
        return;
    }
    fetch('/get_task')
        .then(response => {
            if (!response.ok) {
                throw new Error('No tasks available');
            }
            return response.json();
        })
        .then(task => {
            currentTask = task;
            console.log("Received new task:", task);
        })
        .catch(error => {
            console.error(error.message);
        });

    updateTaskDisplay()
}

function cancelTask() {
    fetch('/cancel_task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(currentTask)  // send the currentTask as the payload
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error cancelling the task');
        }
        return response.json();
    })
    .then(message => {
        console.log(message); // Log the success message
        currentTask = null; // Reset the currentTask
    })
    .catch(error => {
        console.error(error.message);
    });
}

function computeIntegral(a, b) {
    // Config
    const n = 10000; // Number of steps
    const h = (b - a) / n;
    let result = 0;
    let x = a;

    // RK4 step function
    function rk4Step(x, h, func) {
        const k1 = h * func(x);
        const k2 = h * func(x + 0.5 * k1);
        const k3 = h * func(x + 0.5 * k2);
        const k4 = h * func(x + k3);
        return (k1 + 2 * k2 + 2 * k3 + k4) / 6;
    }

    // Integrate using RK4
    for (let i = 0; i < n; i++) {
        result += rk4Step(x, h, gaussianFunction);
        x += h;
    }

    return result;
}

function sendResultToServer() {
    if (!currentTask) {
        console.error("No task assigned.");
        return;
    }
    const result = computeIntegral(currentTask.a, currentTask.b);

    fetch('/store_result', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ result: result, task: currentTask}),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        currentTask = null; // prevent reject
        requestNewTask();  // Request a new task after sending the result
    })
    .catch(error => {
        console.error("Error sending result:", error);
    });
}

function updateTaskDisplay() {
    const taskDisplay = document.getElementById('taskDisplay');
    if (currentTask != null) {
        taskDisplay.textContent = `Task: ${JSON.stringify(currentTask)}`;
    } else {
        taskDisplay.textContent = 'No current task';
    }
}

document.addEventListener('DOMContentLoaded', updateTaskDisplay);
