function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
}

function displayError(message) {
    $("#error").html(message);
}

function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        c = cookies[i].trim();
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length);
        }
    }
    return "unknown";
}

function addComment(post_id) {
    id = post_id;
    // console.log(id);
    itemTextElement = $('#id_comment_input_text_'+id+'');
    itemTextValue   = encodeURIComponent(itemTextElement.val());
    // console.log(itemTextValue);
    // console.log(id);
    // Clear input box and old error message (if any)
    itemTextElement.val('');
    displayError('');

    $.ajax({
        url: "socialnetwork/add-comment/" + id,
        type: "POST",
        data: "comment_text="+itemTextValue+"&post_ref="+id+"&csrfmiddlewaretoken="+getCSRFToken(),
        dataType : "json",
        success: function(response) {
            if (Array.isArray(response)) {
                updateComment(response);
            } else {
                displayError(response.error);
            }
        }
    });
}

function updateComment(commments) {
    // Adds each new todo-list item to the list (only if it's not already here)
    // $(".comment").remove();

    $(commments).each(function() {
        // my_id = "id_comment_text_" + this.pk;
        comment_list_id = "#id_comment_list_" + this.fields.post_ref;
        // console.log(comment_list_id);
        console.log("Time of comment:")
        console.log(this.fields.comment_date_time);
        commment = this.fields.comment_text;

        $(comment_list_id).append(
            '<div class="comment">' +
                '<p>' +
                '<i>' + 'Comment by：' +
                '<a id="id_comment_profile_" '+this.pk+' href="/myProfile/' + this.fields.user_id+ '">'+
                 this.fields.user_name +
                 '</a>' +
                 '</i>' +
                '<span id="id_comment_text_'+this.pk+'">' +
                 '  ' +  commment +
                '</span>' +
                '<span id="id_comment_date_time_"'+this.pk+'>' +
                '<i>' +
                "   -- " + translateTime(this.fields.comment_date_time) +
                '</i>' +
                '</span>' +
                '</p>' +
                '<input type = "hidden" class="ref_hidden_time" value =' + this.fields.comment_date_time + '>' +
            '</div>'
        );
    });

}

function updateAll(response) {
    posts = response.posts;
    commments = response.comments;
    // console.log(posts)
    $(posts).each(function () {
        console.log("update post");
        let post_text = this.post_input_text;
        // console.log(post_text);
        let post_id = this.id;
        // console.log(post_id);
        let poster_id = this.poster_user_id;
        // console.log(poster_id);
        let poster_name = this.poster_name;
        let check_post_id = "id_post_text_" + post_id;
        console.log(check_post_id);
        if (document.getElementById(check_post_id) == null) {
            $('#post_block').prepend(
                '<div class="post">' +
                '<tr>' +
                '<td>' +
                '<i>' +
                '<span>' +
                'Post by ' +
                '</span>' +
                '<a id="id_post_profile_" ' + post_id + ' href="/myProfile/' + poster_id + '">' + poster_name +
                '</a>' +
                ': ' +
                '</i>' +
                '<span id="id_post_text_" ' + post_id + '>' + post_text + '</span>' +
                '<span>' + '<i>' + ' -- ' + translateTime(this.date) + '</i>' + '</span>' +
                '</td>' +
                '<tr class="comment_content">' +
                '<td colspan="3">' +
                '<p>' + '<span>' + 'Comment: ' + '</span>' +
                '<label for="id_comment_input_text_' + post_id + '">' +
                '</label>' +
                ' ' +
                '<input id="id_comment_input_text_' + post_id + '" class="post_comment">' +
                '<button type="submit" class="comment_button" id="id_comment_button_' + post_id + '" onclick="addComment(' + post_id + ')">' +
                'Submit' +
                '</button>' +
                '</p>' +
                '<ol id="id_comment_list_' + post_id + '">' +
                '</ol>' +
                '<input type = "hidden" class="ref_hidden_time" value =' + this.date + '>' +
                '</td>' +
                '</tr>' +
                '</div>'
            );
             $( document ).on( "click", ".comment_button", {para: this.id},function (event) {addComment(event.data.para);});
        };
    })

    $(commments).each(function() {
        // console.log(this.comment_date_time)
        // my_id = "id_comment_text_" + this.pk;
        let comment_list_id = "#id_comment_list_" + this.post_ref;
        // console.log(comment_list_id);
        // console.log(this.comment_text);
        let commment = this.comment_text;
        let check_comment_id = "id_comment_text_" + this.pk;

        console .log("update comment");
        $(comment_list_id).append(
            '<div class="comment">' +
            '<p>' +
            '<i>' + 'Comment by：' +
            '<a id="id_comment_profile_" ' + this.pk + ' href="/myProfile/' + this.user_id + '">' +
            this.user_name +
            '</a>' +
            '</i>' +
            '<span id="id_comment_text_' + this.pk + '">' +
            '  ' + commment +
            '</span>' +
            '<span id="id_comment_date_time_"' + this.pk + '>' +
            '<i>' +
            "   -- " + translateTime(this.comment_date_time) +
            '</i>' +
            '</span>' +
            '</p>' +
            '<input type = "hidden" class="ref_hidden_time" value =' + this.comment_date_time + '>' +
            '</div>'
        );

    });
}

function callUpdate() {
    let time_list_obj = $(".ref_hidden_time");
    let time = "2000-01-01T00:00:00.000000";
    let time_list = [];
    if (time_list_obj.length >= 1) {
        for (let i = 0; i <= time_list_obj.length-1; i++) {
            time_list.push(time_list_obj[i].value);
            // console.log(time_list_obj[i].value)
        }
        time = time_list.sort()[time_list.length - 1];
    }
    // console.log(time_list.length);
    // console.log("Current time");
    // console.log(time);
    $.ajax({
        url: "/socialnetwork/refresh-follower?last_refresh=" + time,
        dataType: "json",
        success: updateAll
    });
}

function translateTime(targetDate) {
    let date = new Date(targetDate);
    let Y = date.getFullYear()+' ';
    let M = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + '/';
    let D = (date.getDate() < 10 ? '0'+(date.getDate()) : date.getDate()) + '/';
    let h = (date.getHours()%12 < 10 ? '0'+(date.getHours()%12) : date.getHours()%12) + ':';
    let m = (date.getMinutes() < 10 ? '0'+(date.getMinutes()) : date.getMinutes()) + ':';
    let s = (date.getSeconds() < 10 ? '0'+(date.getSeconds()) : date.getSeconds());
    let amOrpm = date.getHours() >= 12 ? ' PM' : ' AM';
    // console.log(Y+M+D+h+m+s+amOrpm);
    return M+D+Y+h+m+s+amOrpm;
}

// The index.html does not load the list, so we call getList()
// as soon as page is finished loading
window.onload = callUpdate;

// causes list to be re-fetched every 5 seconds
window.setInterval(callUpdate, 5000);


