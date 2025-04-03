document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#follow').addEventListener('click', (event) => {
        event.preventDefault();
        main();
    })
})


function main() {
    const following_btn = document.querySelector('#follow')
    const user_profile = document.querySelector('#username').textContent;
    const visitor = document.getElementById('username').getAttribute('data-username');
    
    console.log(user_profile);
    console.log('visited by ', visitor)
    if (is_following(following_btn)) {
        // change the button theme and content
        following_btn.textContent = 'Unfollow';
        following_btn.classList.remove('btn-primary');
        following_btn.classList.add('btn-outline-success');
        toggle_follow(user_profile, visitor, 'Follow');
    } else {
        // change the button theme and content
        following_btn.textContent = 'Follow';
        following_btn.classList.remove('btn-outline-success');
        following_btn.classList.add('btn-outline-primary');
        toggle_follow(user_profile, visitor, 'Unfollow');
    }

}


function toggle_follow(user_profile, visitor, action) {
    fetch('/follow', {
        method: 'POST',
        body: JSON.stringify({
            follower: visitor,
            followed: user_profile,
            action: action
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
    })
    .catch(error => console.error('Error: ', error));
}

function is_following(btn) {
    if (btn.textContent === 'Follow') {
        return true;
    } else if (btn.textContent === 'Unfollow') {
        return false;
    }
}
