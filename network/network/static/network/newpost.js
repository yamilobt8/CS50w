document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#new_post').addEventListener('click', () => new_post(event));
    document.querySelector('#post').addEventListener('submit', () => create_post(event));
});

function new_post(){
    event.preventDefault();
    document.querySelector('#content').value = '';

}

function create_post(){
    const content = document.querySelector('#content').value;
}