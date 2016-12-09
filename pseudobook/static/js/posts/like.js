$( document ).ready(function() {
	$(document).on('click', '.like-unlike', function() {
		postID = $(this).data('post-id');
		parentID = $(this).data('parent-id');
		authorID = $(this).data('author-id');
		contentType = $(this).data('content-type');
		user_has_liked = $(this).data('user-has-liked');

		var like_counter;
		var like_button;
		var like_unlike_container;

		if (contentType === 'po') {
			post_div = $('#post-' + parentID)
			like_counter = post_div.find(".like-counter:first")
			like_button = post_div.find(".like-unlike:first")
			like_unlike_container = post_div.find(".like-unlike-container:first")
		}
		else {
			comment_div = $('#comment-' + parentID)
			like_counter = comment_div.find(".like-counter")
			like_button = comment_div.find(".like-unlike")
			like_unlike_container = comment_div.find(".like-unlike-container")
		}

		num_likes = parseInt(like_counter.html())
		if (user_has_liked === "True") { num_likes -- }
		else { num_likes ++ }

		like_unlike_form = $('#like-unlike-form')
      	like_unlike_form.find('.parentID-field').val(parentID)
      	like_unlike_form.find('.authorID-field').val(authorID)
      	like_unlike_form.find('.contentType-field').val(contentType)

      	console.log(contentType)

		//make POST request for like
		$.ajax({
			url: '/likes/forms/like_unlike',
			data: $(like_unlike_form).serialize(),
			type: 'POST',
			success: function(response) {
			    like_counter.html(num_likes);
			    like_unlike_container.replaceWith(response);
			},
			error: function(error) {
				console.log(error);
				alert(error)
			}
		});
	});
});