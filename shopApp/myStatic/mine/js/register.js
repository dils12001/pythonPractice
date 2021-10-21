$(document).ready(function(){
    jQuery(document).ajaxSend(function(event, xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        function sameOrigin(url) {
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }
        function safeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });









    $('#account').focus(function(){
        $("#account_err").css("display", "none");
        $("#check_err").css("display", "none");
    });
    $('#account'). blur(function(){
        str = this.value
        if(str.length < 6 || str.length > 12){
            $("#account_err").css("display", "block");
        }

        $.post('/checkuserid/', {'userid': str}, function(returnData){
            if(returnData.status == 'error'){
                console.log(returnData.message)
                $("#check_err").css("display", "block");
            }
            else{
                console.log(returnData.message)
            }
        })
    });



    $('#pass').focus(function(){
        $("#pass_err").css("display", "none");
    });
    $('#pass'). blur(function(){
        str = this.value
        if(str.length < 8 || str.length > 16){
            $("#pass_err").css("display", "block");
        }
    });



    $('#passwd').focus(function(){
        $("#passwd_err").css("display", "none");
    });
    $('#passwd'). blur(function(){
        str = this.value
        if(str != $('#pass').val()){
            $("#passwd_err").css("display", "block");
        }
    });



})