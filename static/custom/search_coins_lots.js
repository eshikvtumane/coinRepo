$(document).ready(function(){
    $('#btn_search').click(function(){
        coin_name = $('#search').val()
        console.log(coin_name)
        $.ajax({
            type: 'GET',
            url: '/shop/coin_search/',
            data: {
                'name': coin_name
            },
            dataType: 'json',
            success: function(data){
                html = '<div>';
                coins = JSON.parse(data)
                coins.forEach(function(entry){
                    fields = entry['fields']

                    name = fields['coin_name'];
                    name_length = 20
                    if(name.length > name_length){ // for minimum length name coins
                        name = name.substring(0,name_length) + '...'
                    }


                    var id = entry['pk']
                    console.log(name)
                    href = '<a href="/coins/catalog/city/' + fields['country'] + '/' + id + '" title="' + fields['coin_name'] + '" target="_blank">'

                    denominal = "'" + fields['denominal'] + "'";
                    var array_attr = [id, fields['rate'], denominal, fields['country'],  "'" + name.replace("'", '').replace('"', '') + "'"];

                    html += href + '<div class="coins_view col-lg-3" align="center"><div class="coin_item"><img src="' + fields['photo_reverse'] + '" width="100px" height="100px"></div>';
                    html += '<div>' + href + name + '</a></div>';
                    html += '<div><label>' + fields['rate'] + ' ' + fields['denominal'] + '</label> </div>'
                    html += '<input type="button" onclick="addCoins(' + array_attr + ')" value="Добавить" class="btn btn-primary">'
                    html += '</div></a>';
                });
                html += '</div>'

                $('#result_box').html(html)
            }
        });
    });

    // очистка результатов поиска
    $('#clear_result').click(function(){
        $('#result_box').html('');
    });
});

function addCoins(coin_id, rate, denominal, country, name){
console.log('1')

    href = '/coins/catalog/city/' + country + '/' + coin_id + '" title="' + name + '" target="_blank"'
    pay_input = '<div class="input-group"><span class="input-group-addon">₽</span><input type="number" min="1" value="1" id="pay-' + coin_id + '" class="form-control"></div>'

    row = '<tr id=' + coin_id + '>';
    row += '<td><a href="' + href + '">' + name + '</a></td>';
    row += '<td>' + rate + ' ' + denominal + '</td>';
    row += '<td><input type="number" min="1" value="1" id="quantity-' + coin_id + '" class="form-control"></td>';
    row += '<td>' + pay_input + '</td>';
    row += '<td><input type="button" value="Убрать" onclick="deleteItem('+ coin_id +')" class="btn btn-danger"></td>';
    row += '</tr>';

    $('#tbl_add_coins').append(row);
}

function clearResult(){
    $('#clear_result').html('');
}

function deleteItem(id){
    console.log(id);
    var row = document.getElementById(id);
    row.parentNode.removeChild(row);
}
