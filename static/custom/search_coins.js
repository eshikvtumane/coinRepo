$(document).ready(function(){
    $('#btnSearch').click(function(){
        console.log('Start Ajax ...');
        ajaxCoinsSearch('True', 1);
    });

    $('#btnReset').click(function(){
        $('#search_name').val('');
        $('#search_number').val('');
        $('select[class="chosen-select"]').val('').trigger('liszt:updated');
        $('select[class="chosen-select"]').attr("text", "selected").trigger('chosen:updated');
    });
});

function ajaxCoinsSearch(first_search, number_page){ // first_search указывает, происходит загрузка контента при поиске или переходе меджу страницами
    $.ajax({
            type:'POST',
            url:'/coins/catalog/search/',
            data:{
                'csrfmiddlewaretoken': $('input[csrfmiddlewaretoken]').val(),
                'name' : $('#search_name').val(),
                'item_number' : $('#search_number').val(),
                'series':$('#series').val(),
                'qualities':$('#qualities').val(),
                'metals':$('#metals').val(),
                'page' : number_page,
                'first_load' : first_search
            },
            dataType: 'json',
            success:function(data){
                console.log('Print result:');
                console.log(data);
                console.log('End operation.:');

                // get data on server
                obj = JSON.parse(data[1]);

                // get quantity pages
                total_pages = data[0];
                console.log(first_search);
                if(first_search == 'True'){
                    Paginator(total_pages)
                }



                html = '<div>';
                coins.forEach(function(entry){
                    fields = entry['fields'];

                    name = fields['coin_name'];
                    name_length = 20
                    if(name.length > name_length){ // for minimum length name coins
                        name = name.substring(0,name_length) + '...'
                    }

                    html += '<div class="coins_view col-lg-3" align="center"><div class="coin_item"><img src="' + fields['photo_reverse'] + '" width="100px" height="100px"></div>';
                    html += '<div><a href="' + entry['pk'] + '" title="' + fields['coin_name'] + '"><label>' + name + '</a></label></div>';
                    html += '<div><label>' + fields['rate'] + ' ' + fields['denominal'] + '</label> </div></div>';
                });
                html += '</div>';

                $('#result_box').html(html)
            }
        });
}