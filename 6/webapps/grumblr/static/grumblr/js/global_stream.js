$(document).ready(function(){
	// update global_stream and follower page every five seconds
	$(".reply-box").hide();
	setInterval(
		function(){
			if ($("#stream").text() == "globalUpdate" || $("#stream").text() == "Follower"){
				$.get("/update-global-stream", {'time':$("#update_time").text()}, function(data){
					$("#update_time").text(data['update_time']);
					var grumblrs = data['grumblrs'];
					for (g_num in grumblrs){
						var g = grumblrs[g_num];
						if ($("#stream").text() == "Follower") {
							if(g.myfollower == 'notFollower') {break;}
						}
						var html = '<div class="single" id = "post-'+g.gid+ '">\
      								<div class="div5">\
      								<a href="/OtherProfile/'+ g.user_id+'"><img src="/media/avatar/'+ g.user_id+' " alt="no image"  <a href="/grumblr/OtherProfile/'+ g.user_id+'" >'+ g.user_username +'</a><br/>\
        							<input class="time" type="text" value=" ' +g.time+ '">\
        							<br/>\
        							<textarea class="textarea1" name="text" readonly>'+ g.content +'</textarea>\
        							</div>';
						html += '<div>\
						         <ul class="faceul">\
						         <li>\
									<button type="button" class="btn btn-primary btn-xs update-reply-btn" flag="update" data="'+ g.gid +'">\
										<span class="glyphicon glyphicon-pencil"></span>\
										<span>Reply</span>\
										</button>\
										</li> ';
						html += '<li>\
									<button type="button" class="btn btn-primary btn-xs like-btn" pid="'+ g.gid +'">\
										<span class="glyphicon glyphicon-thumbs-up"></span>\
										<span>Like</span>\
										</button>';
						html += '</li>\
								</ul>\
							</div>\
						</div>';
						$("#post-list").prepend(html);
						// bind reply btn event listener
						bindReplyBtnListener(".update-reply-btn[data="+ g.gid +"]");

					}
				});
			}
		},
		5000);
		bindReplyBtnListener(".reply-btn");
		bindSubmitReplyBtnListener(".submit-reply-btn");
});
//Listen the reply button
function bindReplyBtnListener(selector) {
	$(selector).click(function(){
	//Listen the reply button which is updated
	if($(this).attr("flag")=="update"){
		var grumblr_id = $(this).attr("data");
		$(".reply-box").hide();
		showReplyComment(grumblr_id);
		var cookie = getCookie("csrftoken");
	 	var html = '<div class="reply-box" data=" '+grumblr_id+'">\
        			<div class="arrow"></div>\
          			<ul id="reply-list-'+grumblr_id+'" class="list-unstyled"></ul>\
                    <div id="your-reply">\
                    <span >Enter your reply:</span>\
                    <p class="bg-danger" id="reply-err-'+grumblr_id+'"></p>\
                    <input id="reply-text-'+grumblr_id+'" name="text" type="text" class="form-control" placeholder="add your comment">\
                    <button class="submit-reply-btn btn btn-primary btn-xs pull-right" cookie="'+cookie+'" flag="update" data="'+grumblr_id+'">Submit</button>\
                    </div>\
            		</div>';
		$("#post-"+grumblr_id).after(html);
		bindSubmitReplyBtnListener(".submit-reply-btn[data="+grumblr_id+"]");
	//Listen the reply button in the html
	}else{
		var clicked = $(this).attr("data")
		$(".reply-box").hide();
    	var replyContainer = $("div[data="+clicked+"]");
    	showReplyComment(clicked);
    	replyContainer.show();
    }
	});
}
//Listen the comment submit button
function bindSubmitReplyBtnListener(selector){
	$(selector).click(function(event){
	//Listen the submit button which is updated by js
	if($(this).attr("flag")=="update"){
		console.log("here");
		var grumblr_id = $(this).attr("data");
        var text = $("#reply-text-"+grumblr_id).val();
        var csrf = $(this).attr("cookie");
        $.post("/reply-comment", {'text':text, 'grumblr_id':grumblr_id, 'csrfmiddlewaretoken':csrf}, function(data){
            // if there is some error, show it
			if (data != "success"){
				$("#reply-err-"+poster_id).html(data);
				$("#reply-err-"+poster_id).show();
			}
			// show the new comments list
			else {
			    showReplyComment(grumblr_id);
				$("#reply-text-"+grumblr_id).val("");
			}
		});
		//Listen the reply button in the html
	}else{
		// do not post by form
		event.preventDefault();
		var grumblr_id = $(this).attr("data");
		var text = $("#reply-text-"+grumblr_id).val();
		var csrf = $('#comment-form-'+grumblr_id).children('input[name="csrfmiddlewaretoken"]').val();

		// try to send post request to add a comment
		$.post($("#comment-form-"+grumblr_id).attr("action"), {'text':text, 'grumblr_id':grumblr_id, 'csrfmiddlewaretoken':csrf}, function(data){
			// if there is some error, show it
			if (data != "success"){
				$("#reply-err-"+grumblr_id).html('<span class="glyphicon glyphicon-exclamation-sign"></span> ' + data);
				$("#reply-err-"+grumblr_id).show();
			}
			// show the new comments list
			else {
				showReplyComment(grumblr_id);
				$("#reply-text-"+grumblr_id).val("");
			}
		});
	   }
	});
}
//Show comment list
function showReplyComment(grumblr_id) {
	$("#reply-err-"+grumblr_id).hide();
	$.get('/get-comment/' + grumblr_id, function(data){
		$('#reply-list-'+grumblr_id).empty();
		var comments = data['comments'];
		for (cid in comments){
		var html='<div class="comment">\
      				<a href="OtherProfile/'+ comments[cid].userId+'"><img src="/media/avatar/'+ comments[cid].userId+' " alt="no image"  <a href="/grumblr/OtherProfile/'+ comments[cid].userId+'" >'+ comments[cid].username +'</a><br/>\
        			<input class="time" type="text" value=" ' +comments[cid].timestamp+ '">\
        			<br/>\
        			<textarea class="textarea1" name="text" readonly>'+ comments[cid].content +'</textarea>\
        		  </div>';
			$('#reply-list-'+ grumblr_id).append(html);
		}
	});
}
//Learn from W3C school to obtain the cookie
function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
    }
    return "";
}