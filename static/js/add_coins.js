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
            url:'/user/coininfo/change/',
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

        $.ajax({
            type: 'GET',
            url: '/user/coininfo/change/',
            data:{
                'quantity': quantity,
                'coin': coin
            },
            success: function(data){
                if(data != 500){
                    console.log('OK');
                }
                else{
                    console.log('Fail');
                }
            }
        });
    }