function showEditComment(event) {
    comment_id = event.target.getAttribute('data-edit_comment_btn')
    if (comment_id != null){
        var comment = document.getElementById('comment '+comment_id)
        var edit_comment_form = document.getElementById(
            'edit_comment_form_container '+comment_id
        )
        comment.style.display = "none";
        edit_comment_form.style.display = "block";
        // 
        var form_method_type = document.getElementById('method_type '+ comment_id)
        form_method_type.value = "PATCH"
        // 
        var comment_text = document.getElementById("comment_text "+comment_id).innerHTML;
        var comment_textarea = document.getElementById('comment_textarea '+ comment_id);
        comment_textarea.value = comment_text;
        comment_textarea.focus();
        // 
        // var comment_id_input = document.getElementById("comment_id "+ comment_id)
        // comment_id_input.value = comment_id
    };
};
function deleteComment(event) {
    comment_id = event.target.getAttribute('data-delete_comment_btn')
    if (comment_id != null) {
        delete_alert = confirm("Do you want to delete comment?");
        if (delete_alert == true) {
        var form = document.getElementById('edit_comment_form ' + comment_id)
        var form_method_type = document.getElementById('method_type '+ comment_id)
        form_method_type.value = "DELETE";
        var form_submit = document.getElementById('edit_comment_submit '+comment_id)
        form_submit.click()
        }
        else{
            return;
        }
    };
};

function hideEditComment(event) {
    comment_id = event.target.getAttribute('data-cancel_comment_btn')
    if (comment_id != null) {
        var comment = document.getElementById('comment '+comment_id)
        var edit_comment_form = document.getElementById('edit_comment_form_container '+ comment_id)
        comment.style.display = "block";
        edit_comment_form.style.display = "none";
    };
};
function editCommentFormErrors(event) {
    var comments = document.querySelectorAll("[id*='comment ']");
    for ( var i = 0; i < comments.length; i++) {
        var comment = comments[i]
        comment.style.display = "block"
    };
    var comments_forms = document.querySelectorAll("[id*='edit_comment_form_container ']");
    for ( var i = 0; i < comments_forms.length; i++) {
        var comment_form = comments_forms[i]
        comment_form.style.display = "none"
    };
    var edit_comment_form_error = document.getElementById('edit_comment_form_error')
    if (edit_comment_form_error != null) {
        var comment_id = edit_comment_form_error.getAttribute('comment_id')
        var comment = document.getElementById('comment '+comment_id)
        var edit_comment_form = document.getElementById('edit_comment_form_container '+ comment_id)
        comment.style.display = "none";
        edit_comment_form.style.display = "block";
        var comment_textarea = document.getElementById('comment_textarea '+comment_id)
        comment_textarea.focus()
        

    }
    else {
        var comments = document.querySelectorAll("[id*='comment ']");
        for ( var i = 0; i < comments.length; i++) {
            var comment = comments[i]
            comment.style.display = "block"

        };
        var comments_forms = document.querySelectorAll("[id*='edit_comment_form_container ']");
        for ( var i = 0; i < comments_forms.length; i++) {
            var comment_form = comments_forms[i]
            comment_form.style.display = "none"

        };
    };
};
function editCommentBtn() {
    var comments = document.getElementById('comments');
    comments.addEventListener("click", showEditComment, false);
};
function deleteCommentBtn() {
    var comments = document.getElementById('comments');
    comments.addEventListener("click", deleteComment, false);
};
function cancelCommentBtn() {
    var comments = document.getElementById('comments'); 
    comments.addEventListener("click", hideEditComment, false);   
};
window.addEventListener("load", editCommentFormErrors, false);