document.addEventListener('DOMContentLoaded', function () {
    document.body.addEventListener('click', function(event) {
        const target = event.target;
        if (event.target.classList.contains('editpost')) {
            handleEdit(target);
        } else if (event.target.classList.contains('cancel-btn')) {
            handleCancel(target);
        }
    });
});


function handleEdit(target) {
    const post_id = target.getAttribute('data-id');
    const content = document.querySelector(`#post-content-${post_id}`).textContent;
    const postDiv = document.querySelector(`#post-div-${post_id}`);
    const EditForm = `
        <form id="post_form">
            <div class="form-floating">
                <textarea class="form-control" id="post-content-${post_id}" style="height: 100px">${content}</textarea>
                <label for="floatingTextarea2">content</label>
            </div>
            <div class="d-flex justify-content-left mt-1">
                <button class="btn btn-primary submit-btn" id="submit-${post_id}" type="submit">Submit</button>
                <button class="btn btn-secondary ms-1 cancel-btn" id="cancel-${post_id}" data-id="${post_id}" type="button">Cancel</button>
            </div>
        </form>
    `;

    postDiv.dataset.backup = postDiv.innerHTML;
    postDiv.innerHTML = EditForm;

}

function handleCancel(target) {
    const id = target.getAttribute('data-id');
    const postDiv = document.querySelector(`#post-div-${id}`);
    if (postDiv.dataset.backup) {
        postDiv.innerHTML = postDiv.dataset.backup;
        delete postDiv.dataset.backup;
    }
}

