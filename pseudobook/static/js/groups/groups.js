$( document ).ready(function() {
  $(document).on('click', '.make-comment', function() {
      post_id = $(this).data('post-id')
      author_id = $(this).data('author-id')

      make_comment_form = $('#make-comment-form')
      make_comment_form.find('.postID-field').val(post_id)
      make_comment_form.find('.authorID-field').val(author_id)

      $('#make-comment-modal').modal('toggle');
      
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
          console.log("success push")
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
});





