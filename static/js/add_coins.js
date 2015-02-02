$(document).ready(function(){
        $('#showForm').click(function(){
                $('#addCoinInfo').stop().show('slow');
            });
    }
);

function deleteCoinInfo(elem){
        var coin_id = elem.value;

        $.ajax({
            type: 'POST',
            url:'/user_image/coininfo/change/',
            data:{
                'c_id': coin_id
            },
            dataType: 'json',
            success:function(data){
                console.log(data);
                if(data != '500'){
                    tr = 'tr[id='+ coin_id + ']'
                    $(tr).remove();
                }
                else{
                    console.log('Sheet');
                }
            }
        });
    }

    function quantityRefresh(elem){
        var coin = elem.value;
        var quantity = document.getElementById('q-'+coin).value;
        console.log(quantity);

        img_id = '#btn-' + coin;
        console.log('======');
        $(img_id).attr('src', '/static/gif/ajax-loader.gif');
        console.log('======');

        $.ajax({
            type: 'GET',
            url: '/user_image/coininfo/change/',
            data:{
                'quantity': quantity,
                'coin': coin
            },
            success: function(data){
                if(data != 500){
                    console.log('OK');
                    infoPopup('#popup');
                }
                else{
                    console.log('Fail');
                    infoPopup('#popup-error');
                }

                $(img_id).attr('src', '/static/gif/refresh.png');
            }
        });
    }

    function infoPopup(id){
        $(id).delay(100).fadeIn();
        $(id).delay(2000).fadeOut(1000);
    }