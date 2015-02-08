$(document).ready(function(){

    $("#psw_reset_form").submit(function(e){
        e.preventDefault();
        current_password = $("#current_password").val();
        new_password = $("#new_password").val();

        $.ajax({
            type:'POST',
            url:'/user/info/reset_password/',
            data: {
                 'current_password':current_password,
                 'new_password' : new_password

            },
            success:function(data){
                if (data == "1"){
                    $("#result").html("Пароль успешно изменён!");
                }

                else{
                    $("<div>Текущий пароль введён неверно! </div>").insertAfter("#result").fadeOut(3000);

                }
            }


        })

    })
});