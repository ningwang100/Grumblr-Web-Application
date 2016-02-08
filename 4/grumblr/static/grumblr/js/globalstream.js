// set reply box y offset
yOffset = 60;

$(document).ready(function(){
	$("#reply-box").hide();
	$("#nav-list").hide();

	// bind nav dropdown list event listener
	bindNavListListener();

	// bind reply btn event listener
	$(".reply-btn").click(function(){
		var replyBox = $("#reply-box");
		var showing = replyBox.attr("data");
		var clicked = $(this).attr("data");
		// if "close" btn is clicked
		if(clicked == showing){
			replyBox.attr("data", -1);
			replyBox.fadeOut(200);
			$(this).html('<span class="glyphicon glyphicon-pencil"></span> Reply');
			$("#post-box").fadeIn(200);
		} else {
			// if reply box is not showing, show it
			if(showing == -1){
				showReplyBox(clicked);
			}
			// if reply box is showing and another reply button is clicked
			else {
				$("button[data=" + showing + "]").html('<span class="glyphicon glyphicon-pencil"></span> Reply');
				$(replyBox).fadeOut(200, function(){showReplyBox(clicked);});
			}
		}
	});

	// bind dislike btn event listener
	$(".like-btn").click(function(){
		var span = $(this).children("span:nth-child(3)");
		var pid = $(this).attr("pid");
		var count = parseInt(span.text());
		$.get("/grumblr/like/" + pid, function(data){
			// if dislike
			if(data == "+1"){
				span.text(count + 1);
				span.removeClass("hide");
			}
			// if undo dislike
			if(data == "-1"){
				span.text(count - 1);
				if(count == 1)
					span.addClass("hide");
			}
		})
	});
});


function showReplyBox(gid){
	// hide the add-new-grumblr box
	$("#post-box").fadeOut(200);

	var clickedBtn = $("button[data=" + gid + "]");
	var replyBox = $("#reply-box");
	var y = clickedBtn.parent().parent().parent().offset().top;

	// try to get comments via AJAX
	$.get('/grumblr/get-comments/' + gid, function(data){
		$('#reply-list').empty();
		var comments = data['comments'];
		for (cid in comments){
			var html = "<li><p><a class='user-name' href='/view-profile/"+ comments[cid].uid +"'>" + comments[cid].nickname + "</a>: " + comments[cid].text + "</p></li>";
			$('#reply-list').append(html);
		}

		clickedBtn.html('<span class="glyphicon glyphicon-pencil"></span> Close');
		$(replyBox).css({right:16, top:(y - yOffset)});
		$(replyBox).fadeIn(200);
		$(replyBox).attr("data", gid);

		$("#reply-gid").val(gid);
	});
}

// bind the nav dropdown menu listener
function bindNavListListener(){
	$("#account-btn").hover(function(){
		$("#nav-list").slideDown(200);
	}, 						function(){
		$("#nav-list").slideUp(200);
	});
}