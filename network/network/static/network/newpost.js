document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#post').addEventListener('submit', (event) => {
        event.preventDefault();
        create_post();
    });
});

function create_post(){

    const contentField = document.querySelector('#content')
    const content = contentField.value.trim();

    if (!content) {
        alert("Post content can't be empty.");
        return;
    }

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
        if (result.message) {
            contentField.value = '';
            location.reload();
        } else {
            alert(result.error);
        }
    })
    .catch(error => console.error('Error: ', error));
}