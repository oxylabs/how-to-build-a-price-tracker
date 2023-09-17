const express = require('express');
const { spawn } = require('child_process');

const app = express();
const port = process.env.PORT || 3000;

app.use(express.static('public'));
app.use(express.json());

app.get('/call-python-script', (req, res) => {
    const pythonProcess = spawn('python3', ['script.py']);

    pythonProcess.stdout.on('data', (data) => {
        const htmlTable = data.toString();
        res.send(htmlTable);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(data.toString());
        res.status(500).send('Error executing Python script');
    });

    pythonProcess.on('close', (code) => {
        console.log(`Python script process exited with code ${code}`);
    });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
