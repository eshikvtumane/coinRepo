$(document).ready(function(){
    $('#addCoins').click(function(){

        console.log();
    // считываем выбранные значения из select
        $('#load').stop().show('slow');
        var coins = []
        var select = $('#select_coins :selected');
        var select_two = $('select[class="chosen-select"]');

        // Проверка (Добавить все монеты или некоторые)
        if(document.getElementById('allCoins').checked){
            $('#select_coins option').each(function(i, selected){
                value = selected['value'];
                if(value != -1){
                    coins[i] = parseInt(value);
                }
            });
            select_two.empty().trigger('chosen:update')
        }
        else{
            $('#select_coins :selected').each(function(i, selected){
                coins[i] = parseInt(selected['value']);
                console.log(coins[i]);
            });
        }


        // отправляем данные на сервер
        json = JSON.stringify(coins)
        $.ajax({
            type: 'POST',
            url: '/user/ajax/add/coins/',
            data: {
                'coins': json,
                'id': parseInt($('#series_id').html())
            },
            dataType: 'json',
            success: function(data){
                console.log(data);

                // добавляем монеты на страницу

                table_row = ''
                data.forEach(function(fields, i){
                    html = '<tr class="bg-info" id=' + fields['pk'] + '><td class="flag">'
                    html += '<img src="' + fields['fields']['photo_reverse'] + '"></td><td>'
                    html += '<a href="' + fields['pk'] + '">' + fields['fields']['coin_name'] + '</a>'
                    html += '</td><td>'
                    html += '<a href="' + fields['pk'] + '" class="btn btn-primary">Перейти</a>'
                    html += '</td><td>'
                    html += '<button class="btn btn-danger" value="'+ fields['pk'] + '" onclick="deleteCountry(this);">Удалить</button>'
                    html += '</td></tr>'

                    table_row += html
                });

                if(document.getElementById('tbl_coins')){
                    $('#tbl_coins').append(table_row);
                }
                else{
                    result = '<table id="tbl_coins" class="table">' + table_row + '</table>'
                    $('#usr_coins').html(result)
                }

                // удаляем выбранные монеты из select
                select.remove().trigger('liszt:updated');
                select_two.val('').trigger('liszt:updated');
                select_two.attr("text", "selected").trigger('chosen:updated');
                $('#load').stop().hide('slow')


            }
        });
    });
});

function deleteCountry(elem){
        var coin_id = elem.value;
        console.log(coin_id);
        $.ajax({
            type: 'POST',
            url:'/user/coin/delete/',
            data:{
                'c_id': coin_id
            },
            dataType: 'json',
            success:function(data){
                console.log(data[0]['fields']['coin_name']);
                if(data != '500'){
                    tr = 'tr[id='+ coin_id + ']'
                    $(tr).remove();
                    $('#select_coins').append('<option value="'+ coin_id +'">'+ data[0]['fields']['coin_name'] +'</option>').trigger('chosen:updated');
                }
                else{
                    console.log('Sheet');
                }
            }
        });
    }