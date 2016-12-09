$( document ).ready(function() {
	$(".like-unlike").click(function(e) {
		//this obtains values put into html file
		// post_id = $(this).data('postId')
		// author_id = $(this).data('authorId')

		var data = new Object();
		data.postID = $(this).data('postId');
		data.authorID = $(this).data('authorId');
		data.contentType = $(this).data('contentType');
		// post_like_form = $('like-unlike-form')
		// post_like_form.find('.postID-field').val(post_id)
		// post_like_form.find('.authorID-field').val(author_id)

		console.log(data);
		//make POST request for like
		$.ajax({
			url: '/likes/forms/like_unlike',
			data: JSON.stringify(data),
			type: 'POST',
			contentType: 'application/json;charset=UTF-8',
			success: function(response) {
				    $("#counter").html(response.count);
				    $("#like-button").html(response.like_button);
			},
			error: function(error) {
				console.log(error);
				alert(error)
			}
		});

	});

});