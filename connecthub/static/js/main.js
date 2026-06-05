// ==================== AUTO HIDE MESSAGES ====================
document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.message');
    messages.forEach(function(message) {
        setTimeout(function() {
            message.style.transition = 'opacity 0.5s';
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 500);
        }, 3000);
    });
});

// ==================== LIKE POST WITH AJAX ====================
function likePost(postId, button) {
    fetch('/like-post/' + postId + '/', {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .then(response => response.json())
    .then(data => {
        const likesCount = button.querySelector('.likes-count');
        if (data.liked) {
            button.innerHTML = '❤️ <span class="likes-count">' + data.likes_count + '</span>';
            button.classList.add('liked');
        } else {
            button.innerHTML = '🤍 <span class="likes-count">' + data.likes_count + '</span>';
            button.classList.remove('liked');
        }
    })
    .catch(error => {
        console.log('Error:', error);
        // Fallback - reload page
        window.location.reload();
    });
}

// ==================== IMAGE PREVIEW ====================
function previewImage(input) {
    const preview = document.getElementById('imagePreview');
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.innerHTML = '<img src="' + e.target.result + '">';
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// ==================== FORM VALIDATION ====================
const registerForm = document.querySelector('.auth-form');
if (registerForm) {
    registerForm.addEventListener('submit', function(e) {
        const password = registerForm.querySelector('[name="password"]');
        const confirmPassword = registerForm.querySelector('[name="confirm_password"]');

        if (password && confirmPassword) {
            if (password.value !== confirmPassword.value) {
                e.preventDefault();
                alert('Passwords do not match!');
                confirmPassword.focus();
                return;
            }
            if (password.value.length < 6) {
                e.preventDefault();
                alert('Password must be at least 6 characters!');
                password.focus();
                return;
            }
        }
    });
}

// ==================== NAVBAR ACTIVE LINK ====================
const currentPath = window.location.pathname;
const navLinks = document.querySelectorAll('.nav-links a');
navLinks.forEach(function(link) {
    if (link.getAttribute('href') === currentPath) {
        link.style.borderBottom = '2px solid white';
        link.style.paddingBottom = '3px';
    }
});

// ==================== COMMENT FORM VALIDATION ====================
const commentForm = document.querySelector('.comment-form');
if (commentForm) {
    commentForm.addEventListener('submit', function(e) {
        const commentInput = commentForm.querySelector('[name="comment_text"]');
        if (commentInput.value.trim() === '') {
            e.preventDefault();
            alert('Comment cannot be empty!');
            commentInput.focus();
        }
    });
}