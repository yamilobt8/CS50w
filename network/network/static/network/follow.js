document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#follow').addEventListener('click', (event) => {
        event.preventDefault();
        follow();
    })
})


function follow() {
    const following_btn = document.querySelector('#follow')
    // change the button theme and content
    following_btn.textContent = 'Unfollow';
    following_btn.classList.remove('btn-primary');
    following_btn.classList.add('btn-outline-success');
    // if the users follow put a post request to the backend changing the status
}
