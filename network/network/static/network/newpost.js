document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#post').addEventListener('submit', (event) => {
        event.preventDefault();
        create_post();
    });
});

function create_post(){
    const content = document.querySelector('#content').value;
    const timestamp = new Date();

    console.log('post content: ', content);
    console.log('timestamp: ', timestamp.toLocaleString());
}