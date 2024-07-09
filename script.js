document.addEventListener('DOMContentLoaded', () => {
    const encryptBtn = document.getElementById('encrypt-btn');
    const decryptBtn = document.getElementById('decrypt-btn');
    const exitBtn = document.getElementById('exit-btn');
    const formContainer = document.getElementById('form-container');
    const fileForm = document.getElementById('file-form');
    const output = document.getElementById('output');

    let mode = '';

    encryptBtn.addEventListener('click', () => {
        mode = 'encrypt';
        showForm();
    });

    decryptBtn.addEventListener('click', () => {
        mode = 'decrypt';
        showForm();
    });

    exitBtn.addEventListener('click', () => {
        window.close();
    });

    fileForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const filename = document.getElementById('filename').value;
        const url = mode === 'encrypt' ? '/encrypt' : '/decrypt';
        const response = await fetch(`http://localhost:5000${url}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ filename })
        });

        const result = await response.json();
        output.textContent = result.message;
        formContainer.style.display = 'none';
    });

    function showForm() {
        formContainer.style.display = 'block';
        output.textContent = '';
    }
});
