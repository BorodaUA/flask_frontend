function showEditComment(event) {
    comment_id = event.target.getAttribute('data-edit_comment_btn')
    if (comment_id != null){
        var comment = document.getElementById('comment '+comment_id)
        var edit_comment_form = document.getElementById('edit_comment_form '+comment_id)
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
        var comment_id_input = document.getElementById("comment_id "+ comment_id)
        comment_id_input.value = comment_id
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
        form.submit()
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
