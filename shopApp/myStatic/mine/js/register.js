$(document).ready(function(){
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