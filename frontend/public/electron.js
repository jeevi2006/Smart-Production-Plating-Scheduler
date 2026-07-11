const { app, BrowserWindow } = require("electron");
const { spawn } = require("child_process");
const path = require("path");
const axios = require("axios");

let backend;

function createWindow() {

    const win = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true
        }
    });

    if (app.isPackaged) {

        // Production
        win.loadFile(
            path.join(__dirname, "..", "build", "index.html")
        );

    } else {

        // Development
        win.loadURL("http://localhost:3000");

        // Uncomment only for debugging
        // win.webContents.openDevTools();
    }
}

app.whenReady().then(async () => {

    let backendExe;

    if (app.isPackaged) {

        backendExe = path.join(
            process.resourcesPath,
            "backend",
            "main.dist",
            "main.exe"
        );

    } else {

        backendExe = path.join(
            __dirname,
            "..",
            "..",
            "backend",
            "main.dist",
            "main.exe"
        );
    }

    console.log("Backend :", backendExe);

    backend = spawn(backendExe, [], {
        cwd: path.dirname(backendExe),
        windowsHide: true
    });

    backend.stdout.on("data", (data) => {
        console.log(data.toString());
    });

    backend.stderr.on("data", (data) => {
        console.error(data.toString());
    });

    backend.on("error", (err) => {
        console.error("Backend Error :", err);
    });

    backend.on("close", (code) => {
        console.log("Backend Closed :", code);
    });

    // Wait until backend starts
    for (let i = 0; i < 20; i++) {

        try {

            await axios.get(
                "http://127.0.0.1:8001/license-status"
            );

            console.log("Backend Ready");

            createWindow();

            return;

        } catch {

            await new Promise(resolve =>
                setTimeout(resolve, 500)
            );

        }
    }

    console.log("Backend Failed To Start");

});

app.on("window-all-closed", () => {

    if (backend) {

        backend.kill();

    }

    if (process.platform !== "darwin") {

        app.quit();

    }
});

app.on("activate", () => {

    if (BrowserWindow.getAllWindows().length === 0) {

        createWindow();

    }
});