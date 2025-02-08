// Edit Comment Button
$(document).ready(function () {
    $(document).on("click", ".edit-btn", function () {
        const $editBtn = $(this);
        const commentId = $editBtn.data("id");
        const dataType = $editBtn.data("type");

        let $commentContainer;
        if (dataType === "comment") {
            $commentContainer = $editBtn.closest('.comment-btn-container');
        } else if (dataType === "reply") {
            $commentContainer = $editBtn.closest('.nested-comment-btn-container');
        }

        const $originalContent = $(`#content-${commentId}`);
        const $textarea = $(`#textarea-${commentId}`);
        const $editBtnGroup = $editBtn.closest('.comment-btn-container, .nested-comment-btn-container').find(".edit-comment-btn-group").first();
        const $commentDotIcon = $commentContainer.closest('.comment-btn-container, .nested-comment-btn-container').find(".comment-dot-icon").first();
        const $replyIcon = $commentContainer.closest('.comment-btn-container, .nested-comment-btn-container').find(".reply-button").first();

        // Extract replied username and content
        const contentText = $originalContent.text();
        const usernameRegex = /^@([a-zA-Z0-9_.]+)/;
        const match = contentText.match(usernameRegex);

        let repliedAuthor = "";
        let content = contentText;

        if (match) {
            repliedAuthor = `${match[0]}  `;
            content = contentText.slice(repliedAuthor.length).trim();
        }

        // Set textarea value and height
        $textarea.val(repliedAuthor + content.replace(/<br\s*\/?>/gi, "\n")).css("height", "auto");
        setTimeout(() => {
            $textarea.css("height", `${$textarea[0].scrollHeight}px`);
            $textarea.focus();
        });

        // Prevent removal of replied username
        $textarea.off("input").on("input", function () {
            if (!$textarea.val().startsWith(repliedAuthor)) {
                $textarea.val(repliedAuthor + $textarea.val().slice(repliedAuthor.length));
            }
        });

        // Show/Hide relevant elements
        $commentDotIcon.addClass("hidden");
        $replyIcon.addClass("hidden");
        $textarea.removeClass("hidden");
        $editBtnGroup.removeClass("hidden");
        $originalContent.addClass("hidden");
        $commentContainer.addClass("edit-mode");
    });
});

// Cancel Editing Comment Button
$(document).ready(function () {
    $(document).on("click", ".edit.cancel-btn", function () {
        const $cancelBtn = $(this);
        const commentId = $cancelBtn.data("id");
        const dataType = $cancelBtn.data("type");

        let $commentContainer;
        if (dataType === "comment") {
            $commentContainer = $cancelBtn.closest('.comment-btn-container');
        } else if (dataType === "reply") {
            $commentContainer = $cancelBtn.closest('.nested-comment-btn-container');
        }

        const $originalContent = $(`#content-${commentId}`);
        const $textarea = $(`#textarea-${commentId}`);
        const $editBtnGroup = $commentContainer.closest('.comment-btn-container, .nested-comment-btn-container').find(".edit-comment-btn-group").first();
        const $commentDotIcon = $commentContainer.closest('.comment-btn-container, .nested-comment-btn-container').find(".comment-dot-icon").first();
        const $replyIcon = $commentContainer.closest('.comment-btn-container, .nested-comment-btn-container').find(".reply-button").first();

        // Reset textarea value and height
        $textarea.val($originalContent.text().replace(/<br\s*\/?>/gi, "\n")).css("height", "auto");

        // Show/Hide relevant elements
        $editBtnGroup.addClass("hidden");
        $replyIcon.removeClass("hidden");
        $originalContent.removeClass("hidden");
        $textarea.addClass("hidden");
        $commentDotIcon.removeClass("hidden");
        $commentContainer.removeClass('edit-mode');
    });
});

// Save Editing Comment Button
$(document).ready(function () {
    $(document).on("click", ".edit.save-btn", function () {
        const $saveBtn = $(this);
        const commentId = $saveBtn.data("id");
        const dataType = $saveBtn.data("type");

        let $commentContainer;
        if (dataType === "comment") {
            $commentContainer = $saveBtn.closest('.comment-btn-container');
        } else if (dataType === "reply") {
            $commentContainer = $saveBtn.closest('.nested-comment-btn-container');
        }

        const $originalContent = $(`#content-${commentId}`);
        const $textarea = $(`#textarea-${commentId}`);
        const $editBtnGroup = $commentContainer.closest('.comment-btn-container, .nested-comment-btn-container').find(".edit-comment-btn-group").first();
        const $commentDotIcon = $commentContainer.closest('.comment-btn-container, .nested-comment-btn-container').find(".comment-dot-icon").first();
        const $replyIcon = $commentContainer.closest('.comment-btn-container, .nested-comment-btn-container').find(".reply-button").first();
        const updatedContent = $textarea.val();

        // Fetch CSRF token
        const csrfToken = $('[name=csrfmiddlewaretoken]').val();

        // Send fetch request
        $.ajax({
            url: `/comments/edit/${commentId}`,
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken },
            contentType: 'application/json',
            data: JSON.stringify({ content: updatedContent }),
            success: function (data) {
                if (data.success) {
                    $originalContent.text(updatedContent);
                    $editBtnGroup.addClass("hidden");
                    $replyIcon.removeClass("hidden");
                    $originalContent.removeClass("hidden");
                    $textarea.addClass("hidden");
                    $commentDotIcon.removeClass("hidden");
                    $commentContainer.removeClass("edit-mode");
                } else {
                    alert("Error: " + data.error);
                }
            },
            error: function () {
                alert("There was an error while updating the comment.");
            }
        });
    });
});

//Report
document.addEventListener("DOMContentLoaded", function () {
    const reportButtons = document.querySelectorAll('.report-button');
    const reportModal = document.getElementById('report-modal');
    const closeReportModal = document.getElementById('closeReportModal');
    const reportedLink = document.getElementById('reported-link');
    const reportedComment = document.getElementById('reported-comment');
    const reportForm = document.querySelector('#report-modal form');
    const reportContent = document.querySelector('.report-content');

    reportButtons.forEach(button => {
        button.addEventListener("click", function() {
            const dataSlug = this.getAttribute('data-slug');
            const dataContent = this.getAttribute('data-content')
            const dataAuthor = this.getAttribute('data-author')

            if (this.closest('.comment')) {
                reportedComment.value = `#${dataAuthor} - ${dataContent}`;
                reportedLink.value = `http://127.0.0.1:8000/posts/${dataSlug}`;
            } else {
                reportedComment.value = `${dataAuthor}'s Post`
                reportedLink.value = `http://127.0.0.1:8000/posts/${dataSlug}`;
            }

            reportModal.style.display = 'block';

        });
    });

    closeReportModal.onclick = function() {
        reportModal.style.display = 'none';
        reportContent.style.height = 'auto';
        reportForm.reset();
    };

    reportModal.addEventListener('click', function(event) {
        if (event.target === reportModal) {
            reportModal.style.display = 'none';
            reportContent.style.height = 'auto';
            reportForm.reset();
        }
    });
});

// Delete Comment
document.addEventListener("DOMContentLoaded", function() {
    const deleteCommentButtons = document.querySelectorAll(".delete-comment-button");
    const deletePostButtons = document.querySelectorAll(".delete-btn");
    const deleteModal = document.getElementById("delete-modal");
    const closeDeleteModal = document.getElementById('close-delete-btn');
    const deleteForm = document.querySelector('#delete-modal form');

    deleteCommentButtons.forEach(button => {
        button.addEventListener("click", function() {
            const commentId = this.getAttribute("data-comment-id");
            const action = `/comments/delete/${commentId}`;
            deleteForm.setAttribute("action", action);
            deleteModal.style.display = 'block';
        });
    });

    // Delete Post
    deletePostButtons.forEach(button => {
        button.addEventListener("click", function() {
            const postId = this.getAttribute("data-post-id");
            const slug = this.getAttribute("data-post-slug");
            const action = `/posts/${slug}/delete/${postId}`;
            deleteForm.setAttribute("action", action);
            deleteModal.style.display = 'block';
        });
    });

    closeDeleteModal.onclick = function() {
        deleteModal.style.display = 'none';
        deleteForm.reset();
    };

    deleteModal.addEventListener('click', function (event) {
        if (event.target === deleteModal) {
            deleteModal.style.display = 'none';
            deleteForm.reset();
        }
    })
});

// Dot pop up window
$(document).ready(function () {
    let openModal = null;
    $(document).ready(function() {
        $(document).on("click", ".dot-icon", function(event) {
            const $postActionsDiv = $(this).closest('div').find('.post-actions-modal');

            if (openModal && openModal[0] !== $postActionsDiv[0]) {
                openModal.addClass('hidden');
            }

            $postActionsDiv.toggleClass('hidden');

            if (!$postActionsDiv.hasClass('hidden')) {
                openModal = $postActionsDiv;
            } else {
                openModal = null;
            }

            event.stopPropagation();

            $(document).on('click', function (e) {
                if (!$postActionsDiv.is(e.target) && $postActionsDiv.has(e.target).length === 0 && !$(event.target).is('.dot-icon')) {
                    $postActionsDiv.addClass('hidden');
                    openModal = null;
                }
            });

            $postActionsDiv.find('.edit-btn, .report-button, .delete-btn, .delete-comment-button').on('click', function () {
                $postActionsDiv.addClass('hidden');
                openModal = null;
            });
        })
    });
});

// User Input Main Form
document.addEventListener("DOMContentLoaded", function () {
    const commentForms = document.querySelectorAll("#main-form");

    commentForms.forEach(function (form) {
        const textarea = form.querySelector('#main-form .comment-input');
        const commentBtnGroup= form.querySelector(".comment-btn-group");
        const cancelBtn= form.querySelector('#main-form .cancel-btn');
        const submitBtn= form.querySelector("#main-form .submit-btn");

        commentBtnGroup.classList.add("hidden");

        textarea.value = "";
        const initialHeight = textarea.scrollHeight + "px";
        textarea.style.height = initialHeight;

        textarea.addEventListener("input", function () {
            textarea.style.height = "auto";
            textarea.style.height = textarea.scrollHeight + "px";
        });

        textarea.addEventListener("focus", function () {
            commentBtnGroup.classList.remove("hidden");
        });

        cancelBtn.addEventListener("click", function () {
            commentBtnGroup.classList.add("hidden");
            textarea.value = "";
            textarea.style.height = initialHeight;
        });

        submitBtn.addEventListener("click", function () {
            commentBtnGroup.classList.add("hidden");
        });


    });
});

// User Input Reply Form
document.addEventListener('DOMContentLoaded', function () {
    $(document).ready(function() {
        $(document).on("click", ".reply-button", function() {
            const replyBtn = $(this);
            const commentId = replyBtn.data("id");
            const repliedAuthor = replyBtn.data("author");
            const repliedUsername = `@${repliedAuthor}  `;
            const dataNested = replyBtn.data("nested");
            const replyForm = $(`#reply-form-${commentId}`);
            const textarea = replyForm.find(".comment-input");
            const cancelBtn = replyForm.find(".cancel-btn");

            replyForm.removeClass("hidden");

            if (dataNested === "yes") {
                textarea.val(repliedUsername);
                textarea[0].setSelectionRange(textarea.val().length, textarea.val().length);
            } else {
                textarea.val("");
            }

            const initialHeight = textarea[0].scrollHeight + "px";
            textarea.css("height", initialHeight);

            if (dataNested === "yes") {
                textarea.off("input").on("input", function () {
                    if (!textarea.val().startsWith(repliedUsername)) {
                        textarea.val(repliedUsername);
                        textarea[0].setSelectionRange(textarea.val().length, textarea.val().length);
                    }
                    textarea.css("height", "auto");
                    textarea.css("height", textarea[0].scrollHeight + "px");
                });
            } else {
                textarea.off("input").on("input", function () {
                    textarea.css("height", "auto");
                    textarea.css("height", textarea[0].scrollHeight + "px");
                });
            }

            if (replyForm.is(":hidden")) {
                replyForm.removeAttr("hidden");
                textarea.css("height", textarea[0].scrollHeight + "px");
                textarea.focus();
            } else {
                replyForm.attr("hidden", "");
            }

            cancelBtn.on("click", function () {
                replyForm.attr("hidden", "");
                textarea.val("");
                textarea.css("height", initialHeight);
            });
        });
    });
});

// Looping Comments
document.addEventListener('DOMContentLoaded', function () {
    var infinite = new Waypoint.Infinite({
        element: $('.infinite-container')[0],
        offset: 'bottom-in-view',
        onBeforePageLoad: function () {
            $('.loading').show();
        },
        onAfterPageLoad: function () {
            $('.loading').hide();
        }
    });
});
