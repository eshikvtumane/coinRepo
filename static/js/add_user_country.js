$(document).ready(function(){
    $('#btnAdd').click(function(){
        console.log('1');
        country_id = $('#countries').val();

        $.ajax({
            type: 'POST',
            url: '/user/ajax/add/country/',
            data: { 'country_id':country_id },
            dataType: 'json',
            success: function(data){
                console.log(data)
                try{
                    fields = data[0]['fields']
                    html = '<tr class="bg-info"><td>'
                    html += '<img src="' + fields['country_flag'] + '"></td><td>'
                    html += '<a href="/user/add/series/' + data['pk'] + '">' + fields['country_name'] + '</a>'
                    html += '</td><td>'
                    html += '<a href="" class="btn btn-primary">Перейти</a>'
                    html += '</td><td>'
                    html += '<a href="" class="btn btn-danger">Удалить</a>'
                    html += '</td></tr>'


                    if(document.getElementById('tbl_country')){
                        $('#tbl_country').append(html).show('slow');
                    }
                    else{
                        html = '<table id="tbl_country" class="table">' + html + '</table>'
                        $('#usr_countries').html(html);
                        console.log(html)
                    }
                }
                catch(e){
                    console.log('Object exists')
                }

            }
        });
    });
});