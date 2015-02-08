$(document).ready(function(){

    $('#btnAdd').click(function(){
        series_id = $('#series').val();
        series_name = $('#series option:selected').text();
        country_id = $('#id').html();

        $.ajax({
            type: 'POST',
            url: '/user/ajax/add/series/',
            data: {
                'series_id':series_id,
                'country_id':country_id
            },
            success: function(data){
                console.log(data);

                html = '<tr class="bg-info" id='+ series_id +'><td class="flag">';
                html += '<img src="/static/photo/gold_coin.jpg"></td><td>';
                html += '<a href="' + series_id + '">' + series_name + '</a>';
                html += '</td><td>';
                html += '<a href="' + series_id + '" class="btn btn-primary">Перейти</a>';
                html += '</td><td>';
                html += '<button class="btn btn-danger" value="' + series_id + '" onclick="deleteSeries(this);">Удалить</button>';
                html += '</td></tr>';

                if(data == '200'){
                    console.log('Object exists')
                }
                else{
                    if(document.getElementById('tbl_series')){
                        $('#tbl_series').append(html).show('slow');
                    }
                    else{
                        html = '<table id="tbl_series" class="table">' + html + '</table>';
                        $('#usr_series').html(html);
                        console.log(html)
                    }
                }

                $('#series :selected').remove().trigger('chosen:updated');
                $('#series :selected').val('').trigger('chosen:updated');
            }
        });
    });

});

function deleteSeries(elem){
        var series_id = elem.value;

        $.ajax({
            type: 'POST',
            url:'/user/series/delete/',
            data:{
                's_id': series_id
            },
            dataType: 'json',
            success:function(data){
                console.log(data[0]['fields']['series_name']);
                if(data != '500'){
                    tr = 'tr[id='+ series_id + ']';
                    $(tr).remove();
                    $('#series').append('<option value="'+ series_id +'">'+ data[0]['fields']['series_name'] +'</option>').trigger('chosen:updated');
                }
                else{
                    console.log('Sheet');
                }
            }
        });
    }