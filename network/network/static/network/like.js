document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.like-btn').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const post_id = button.getAttribute('data-post-id');
            const likes_count = document.getElementById(`likes-count-${post_id}`);
            if (button.classList.contains('unliked')) {
                like_post(button, likes_count, post_id);
            } else if (button.classList.contains('liked')) {
                unlike_post(button, likes_count, post_id);
            }
        });
    });
});

function like_post(like_btn, likes_count, post_id) {
    like_btn.classList.remove('unliked');
    like_btn.classList.add('liked');
    likes_count.textContent = parseInt(likes_count.textContent) + 1;
    trigger_animation(like_btn, 'like');
}

function unlike_post(like_btn, likes_count, post_id) {
    like_btn.classList.remove('liked');
    like_btn.classList.add('unliked');
    likes_count.textContent = parseInt(likes_count.textContent) - 1;
    trigger_animation(like_btn, 'unlike');
}

function trigger_animation(like_btn, action) {
    like_btn.style.animation = 'none';
    void like_btn.offsetWidth;
    if (action === 'like') {
        like_btn.style.animation = 'like-animation 0.3s ease-in-out';
    } else {
        like_btn.style.animation = 'unlike-animation 0.3s ease-in-out';
    }
}