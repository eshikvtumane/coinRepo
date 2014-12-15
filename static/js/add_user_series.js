$(document).ready(function(){
    $('#btnAdd').click(function(){
        console.log('1');
        series_id = $('#series').val();
        series_name = $('#series option:selected').text()
        country_id = $('#id').html()

        $.ajax({
            type: 'POST',
            url: '/user/ajax/add/series/',
            data: {
                'series_id':series_id,
                'country_id':country_id
            },
            success: function(data){
                console.log(data)

                html = '<tr class="bg-info"><td class="flag">'
                html += '<img src="/static/photo/gold_coin.jpg"></td><td>'
                html += '<a href="' + series_id + '">' + series_name + '</a>'
                html += '</td><td>'
                html += '<a href="' + series_id + '" class="btn btn-primary">Перейти</a>'
                html += '</td><td>'
                html += '<a href="" class="btn btn-danger">Удалить</a>'
                html += '</td></tr>'

                if(data == '200'){
                    console.log('Object exists')
                }
                else{
                    if(document.getElementById('tbl_series')){
                        $('#tbl_series').append(html).show('slow');
                    }
                    else{
                        html = '<table id="tbl_series" class="table">' + html + '</table>'
                        $('#usr_series').html(html);
                        console.log(html)
                    }
                }

            }
        });
    });
});