document.addEventListener('DOMContentLoaded', function () {
    const user_profile = document.querySelector('#username').textContent;
    UpdateFollowStats(user_profile);
    document.querySelector('#follow').addEventListener('click', (event) => {
        event.preventDefault();
        main();
    })
})


function main() {
    const following_btn = document.querySelector('#follow')
    const user_profile = document.querySelector('#username').textContent;
    const visitor = document.getElementById('username').getAttribute('data-username');
    
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
    UpdateFollowStats(user_profile)
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
        UpdateFollowStats(user_profile);
    })
    .catch(error => console.error('Error: ', error));
}

function UpdateFollowStats(username) {
    fetch(`/follow_stats/${username}`)
    .then(response => response.json())
    .then(data => {
        console.log('API Response:', data);  
        const followers = data.followers;
        const followings = data.followings;

        // update the followers and followings count
        document.querySelector('#followers_count').textContent = followers;
        document.querySelector('#followings_count').textContent = followings;
    })
    .catch(error => console.error('Error Fetching follow stats: ', error));
}

function is_following(btn) {
    if (btn.textContent === 'Follow') {
        return true;
    } else if (btn.textContent === 'Unfollow') {
        return false;
    }
}