document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#post').addEventListener('submit', (event) => {
        event.preventDefault();
        create_post();
    });
});

function create_post(){
    const content = document.querySelector('#content').value;
    fetch('/posts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            content: content
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
    });
}