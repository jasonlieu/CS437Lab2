document.onkeydown = updateKey;
document.onkeyup = resetKey;

const server_port = 65432;
const server_addr = "192.168.1.153";

const POLLING_INTERVAL = 2000
let pollingInterval = null

setInterval(function () {
            sendCommand("busy");
        }, POLLING_INTERVAL);

function sendCommand(command) {
    console.log(command)
    const net = require('net');
    const client = net.createConnection({port: server_port, host: server_addr}, () => {
        console.log("connected")
        client.write(`${command}`);
    });

    // get the data from the server
    client.on('data', (data) => {
        console.log(data.toString());
        displayData(data.toString())
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected');
    });


}

function updateKey(e) {
    e = e || window.event;
    if (e.keyCode === 87) {
        document.getElementById("upArrow").style.color = "green";
        sendCommand("forward");
    } else if (e.keyCode === 83) {
        document.getElementById("downArrow").style.color = "green";
        sendCommand("backward");
    } else if (e.keyCode === 65) {
        document.getElementById("leftArrow").style.color = "green";
        sendCommand("left");
    } else if (e.keyCode === 68) {
        document.getElementById("rightArrow").style.color = "green";
        sendCommand("right");
    }
}

function resetKey(e) {
    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";
}

function displayData(jsonData) {
    let data = JSON.parse(jsonData)
    if (data["action"] === "distance") {
        document.getElementById("distance").textContent = data["result"];
    }
    else if (data["action"] === "random") {
        document.getElementById("random").textContent = data["result"];
    }
    else if (data["action"] === "busy") {
        document.getElementById("busy").textContent = data["result"];
    }
}

function startPolling() {
    if (!pollingInterval) {
        pollingInterval = setInterval(function () {
            sendCommand("distance");
            sendCommand("random");
        }, POLLING_INTERVAL);
    }
}

function stopPolling() {
    if (pollingInterval) {
        clearInterval(pollingInterval)
        pollingInterval = null
    }
}