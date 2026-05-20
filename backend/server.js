const express = require("express");
const cors = require("cors");
const { spawn } = require("child_process");

const app = express();

app.use(cors());
app.use(express.json());

app.post("/bestmove", (req, res) => {

    const { fen } = req.body;

    const python = spawn("py", [
        "../engine/main.py",
        fen
    ]);

    let result = "";

    python.stdout.on("data", (data) => {
        result += data.toString();
    });

    python.stderr.on("data", (data) => {
        console.error(data.toString());
    });

    python.on("close", () => {

        res.json({
            move: result.trim()
        });

    });

});

app.listen(3001, () => {
    console.log("Server running on port 3001");
});