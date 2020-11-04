function showEditStory(event) {
  var story_id = event.target.getAttribute('data-edit_story_btn');
  if (story_id != null) {
    var story = document.getElementById("story " + story_id);
    var edit_story_form = document.getElementById("edit_story_form " + story_id);
    // 
    var story_title = document.getElementById("story_title "+ story_id).innerText;
    var story_text = document.getElementById("story_text "+ story_id).innerText;
    var story_url = document.getElementById("story_url "+ story_id).getAttribute('href');
    var story_score = document.getElementById("story_score "+ story_id).innerText;
    
    var form_story_title_input = document.getElementById('form_story_title '+ story_id);
    var form_story_url_input = document.getElementById('form_story_url '+ story_id);
    var form_story_text_input = document.getElementById('form_story_text '+ story_id);
    var form_method_type = document.getElementById("form_story_method_type "+ story_id);
    
    form_story_title_input.value = story_title
    form_story_url_input.value = story_url
    form_story_text_input.value = story_text
    // 
    story.style.display = "none";
    edit_story_form.style.display = "block";
    form_story_title_input.focus();
  };
};
function hideEditStory(event) {
  var story_id = event.target.getAttribute('data-cancel_story_btn');
  if (story_id != null) {
    var story = document.getElementById("story " + story_id);
    var edit_story_form = document.getElementById("edit_story_form " + story_id);
    edit_story_form.style.display = "none";
    story.style.display = "block";
  };
};
function deleteStory(event){
  var story_id = event.target.getAttribute('data-delete_story_btn');
  if (story_id != null) {
    var form = document.getElementsByClassName("story_form " + story_id)
    var form_method_type = document.getElementById("form_method_type "+ story_id);
    delete_alert = confirm("Do you want to delete story?");
    if (delete_alert == true) {
      form_method_type.value = "DELETE"
    }
    else {
      return false
    }
  };
};
function editStoryBtn () {
  var container = document.getElementById("container");
  container.addEventListener("click", showEditStory, false);
};
function cancelStoryBtn() {
  var container = document.getElementById("container");
  container.addEventListener("click", hideEditStory, false);  
};
function deleteStoryBtn () {
  var container = document.getElementById("container");
  container.addEventListener("click", deleteStory, false);
};