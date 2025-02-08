document.addEventListener("DOMContentLoaded", function () {
    const editEmailBtn = document.getElementById('edit-email-btn');
    const emailModal = document.getElementById('email-modal');
    const closeEmailModal = document.getElementById('close-email-modal');
    const emailInput = document.getElementById('id_email');

    const editPasswordBtn = document.getElementById('edit-password-btn');
    const passwordModal = document.getElementById('password-modal');
    const closePasswordModal = document.getElementById('close-password-modal');

    // Show modal when "Edit Email" button is clicked
    editEmailBtn.onclick = function() {
        emailModal.style.display = 'block';
    };

    // Close "Email" modal when the close button is clicked
    closeEmailModal.onclick = function() {
        emailModal.style.display = 'none';
        emailInput.value = '';
    };

    // Show modal when "Change Password" button is clicked
    editPasswordBtn.onclick = function() {
        passwordModal.style.display = 'block';
    };

    // Close "Password" modal when the close button is clicked
    closePasswordModal.onclick = function() {
        passwordModal.style.display = 'none';
    };
});


document.addEventListener("DOMContentLoaded", () => {
    const loadMoreButton = document.getElementById("load-more");

    if (loadMoreButton) {
        loadMoreButton.addEventListener("click", () => {
            const nextPage = loadMoreButton.dataset.nextPage;

            fetch(`/profile?page=${nextPage}`, {
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
                .then(response => response.json())
                .then(data => {
                    const reviewsContainer = document.getElementById("reviews-container");
                    reviewsContainer.innerHTML += data.reviews_html;

                    if (data.has_next) {
                        loadMoreButton.dataset.nextPage = data.next_page;
                    } else {
                        loadMoreButton.style.display = "none";
                    }
                })
                .catch(error => console.error("Error:", error));
        });
    }
});
