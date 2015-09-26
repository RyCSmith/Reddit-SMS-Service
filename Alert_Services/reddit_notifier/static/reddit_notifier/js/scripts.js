//Sends an ajax request and updates the DOM with the returned message.
function send_message_request() {
    $.ajax({
        url : "get_subreddit_post/",
        type : "POST", 
        data : {phone_number : $('#phone_number')[0].value, subreddit_name : $('#subreddit_name')[0].value},

        success : function(json) {
            $('#alert_message_box').html("<div>" + json.result + "</div>");
        },

        error : function(xhr,errmsg,err) {
            $('#alert_message_box').html("<div>An unknown error occurred. Check console for message. :(</div>");
            console.log(xhr.status + ": " + xhr.responseText); 
        }
    });
    $('#phone_number').val("");
    $('#subreddit_name').val("");
};

// Fetches CSRF token to be placed in the request
function getCSRFtoken() {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, 10) == ('csrftoken=')) {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
}

//Prepares request with django's required CSRF token.
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCSRFtoken());
    }
});