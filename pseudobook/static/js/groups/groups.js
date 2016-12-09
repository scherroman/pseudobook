$( document ).ready(function() {
  $(document).on('click', '.make-comment', function() {
      post_id = $(this).data('post-id')
      author_id = $(this).data('author-id')

      make_comment_form = $('#make-comment-form')
      make_comment_form.find('.postID-field').val(post_id)
      make_comment_form.find('.authorID-field').val(author_id)

      $('#make-comment-modal').on('shown.bs.modal', function () {
        $(this).find('.content-field').focus()
      })
      $('#make-comment-modal').modal('toggle');
  });

  $(document).on('click', '.rename-group', function() {
      user_id = $(this).data('user-id')
      group_id = $(this).data('group-id')

      rename_group_form = $('#rename-group-form')
      rename_group_form.find('.userID-field').val(user_id)
      rename_group_form.find('.groupID-field').val(group_id)

      $('#rename-group-modal').on('shown.bs.modal', function () {
        $(this).find('.content-field').focus()
      })
      $('#rename-group-modal').modal('toggle');
  });
  $(document).on('click', '#rename-group-submit', function() {
    rename_group_form = $('#rename-group-form')
    // userID = rename_group_form.find('.userID-field').val()
    // posts_div = $('#' + post_id)
    // comments_container_div = posts_div.find(".comments-container")
    // comments_div = posts_div.find(".comments")

    //Submit comment post
    $.ajax({
        url: '/groups/forms/rename_group',
        data: $(rename_group_form).serialize(),
        type: 'POST',
        success: function(response) {
          console.log(response)
          // comments_div.prepend(response)
          // comments_container_div.css('display', 'block')
        },
        error: function(error) {
            console.log(error);
            alert(error)
        },
        complete: function(data) {
          $('#rename-group-modal').modal('toggle');
          rename_group_form.find('.content-field').val("")
        }
    });
  });

  $(document).on('click', '.rename-group', function() {
      user_id = $(this).data('user-id')
      group_id = $(this).data('group-id')

      make_comment_form = $('#rename-group-form')
      make_comment_form.find('.userID-field').val(user_id)
      make_comment_form.find('.groupID-field').val(group_id)

      $('#rename-group-modal').on('shown.bs.modal', function () {
        $(this).find('.content-field').focus()
      })
      $('#rename-group-modal').modal('toggle');
  });
  $(document).on('click', '#make-comment-submit', function() {
    make_comment_form = $('#make-comment-form')
    post_id = make_comment_form.find('.postID-field').val()
    posts_div = $('#' + post_id)
    comments_container_div = posts_div.find(".comments-container")
    comments_div = posts_div.find(".comments")

    //Submit comment post
    $.ajax({
        url: '/groups/forms/make_comment',
        data: $(make_comment_form).serialize(),
        type: 'POST',
        success: function(response) {
          comments_div.prepend(response)
          comments_container_div.css('display', 'block')
        },
        error: function(error) {
            console.log(error);
            alert(error)
        },
        complete: function(data) {
          $('#make-comment-modal').modal('toggle');
          make_comment_form.find('.content-field').val("")
        }
    });
  });
  $(document).on('click', '.remove-comment', function() {
      comment_id = $(this).data('comment-id')
      comment_div = $(this).closest('div[class^="comment"]')
      comments_div = comment_div.closest('div[class^="comments"]')
      comments_container_div = comment_div.closest('div[class^="comments-container"]')

      remove_comment_form = $('#remove-comment-form')
      remove_comment_form.find('.commentID-field').val(comment_id)

      //Submit comment post
      $.ajax({
          url: '/groups/forms/remove_comment',
          data: $(remove_comment_form).serialize(),
          type: 'POST',
          success: function(response) {
            comment_div.remove()
            if (num_comments = comments_div.children('.comment').length === 0)  {
              comments_container_div.css('display', 'none')
            }
          },
          error: function(error) {
              console.log(error);
              alert(error)
          }
      });
  });

  $(document).on('click', '.edit-post', function() {
      post_id = $(this).data('post-id')
      posts_div = $('#' + post_id)
      content = posts_div.find('.post-text').html() 

      edit_post_form = $('#edit-post-form')
      edit_post_form.find('.postID-field').val(post_id)
      edit_post_form.find('.content-field').val(content)

      $('#edit-post-modal').on('shown.bs.modal', function () {
        $(this).find('.content-field').focus()
      })
      $('#edit-post-modal').modal('toggle');
  });
  $(document).on('click', '#edit-post-submit', function() {
    edit_post_form = $('#edit-post-form')
    new_content = edit_post_form.find('.content-field').val()
    post_id = edit_post_form.find('.postID-field').val()
    posts_div = $('#' + post_id)
    post_text = posts_div.find('.post-text')

    //Submit comment post
    $.ajax({
        url: '/groups/forms/edit_post_form',
        data: $(edit_post_form).serialize(),
        type: 'POST',
        success: function(response) {
          post_text.html(new_content)
        },
        error: function(error) {
            console.log(error);
            alert(error)
        },
        complete: function(data) {
          $('#edit-post-modal').modal('toggle');
        }
    });
  });

  $(document).on('click', '.edit-comment', function() {
      comment_id = $(this).data('comment-id')
      comments_div = $('#' + comment_id)
      content = comments_div.find('.comment-text').html() 

      edit_comment_form = $('#edit-comment-form')
      edit_comment_form.find('.commentID-field').val(comment_id)
      edit_comment_form.find('.content-field').val(content)

      $('#edit-comment-modal').on('shown.bs.modal', function () {
        $(this).find('.content-field').focus()
      })
      $('#edit-comment-modal').modal('toggle');
  });
  $(document).on('click', '#edit-comment-submit', function() {
    edit_comment_form = $('#edit-comment-form')
    new_content = edit_comment_form.find('.content-field').val()
    comment_id = edit_comment_form.find('.commentID-field').val()
    comments_div = $('#' + comment_id)
    comment_text = comments_div.find('.comment-text')

    //Submit comment comment
    $.ajax({
        url: '/groups/forms/edit_comment_form',
        data: $(edit_comment_form).serialize(),
        type: 'POST',
        success: function(response) {
          comment_text.html(new_content)
        },
        error: function(error) {
            console.log(error);
            alert(error)
        },
        complete: function(data) {
          $('#edit-comment-modal').modal('toggle');
        }
    });
  });
});





