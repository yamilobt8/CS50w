document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#editpost').addEventListener('click', (event) => {
        event.preventDefault()
        const id = document.querySelector('#editpost').getAttribute('data-id');
        const content = document.querySelector('#post_content').textContent;
        edit_post(id, content);
    })
})


function edit_post(post_id, content) {

}