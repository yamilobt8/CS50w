document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.editpost').forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            const id = event.target.getAttribute('data-id');
            const content = document.querySelector(`#post-content-${id}`).textContent;
            const postContentDiv = document.querySelector(`#post-div-${id}`);
            edit_post(id, content, postContentDiv);
        })
    })
})


function edit_post(post_id, content, postDiv) {
    const EditForm = `
        <form id="post_form">
            <div class="form-floating">
                <textarea class="form-control" id="post-content-${post_id}" style="height: 100px"></textarea>
                <label for="floatingTextarea2">content</label>
            </div>
            <div class="d-flex justify-content-left mt-1">
                <button class="btn btn-primary"  id="submit" type="submit">Submit</button>
                <button class="btn btn-secondary ms-1" id="cancel" type="submit">Cancel</button>
            </div>
        </form>
    `
    const backup = postDiv.innerHTML;
    postDiv.innerHTML = EditForm;
    console.log('content: ', content)
    document.querySelector(`#post-content-${post_id}`).textContent = content;
    
    // handle cancel button
    document.querySelector('#cancel').addEventListener('click', (event) => {
        event.preventDefault();
        postDiv.innerHTML = backup;
    })
    // handle submit button
}
