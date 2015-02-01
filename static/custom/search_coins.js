$(document).ready(function(){
//search name coins with help whoosh
//https://github.com/bassjobsen/Bootstrap-3-Typeahead
//http://wadya.pp.ua/2013/01/23/%D0%B0%D0%B2%D1%82%D0%BE%D0%BA%D0%BE%D0%BC%D0%BF%D0%BB%D0%B8%D1%82-%D1%81-%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%D0%BC-ajax-%D0%BF%D1%80%D0%B8-%D0%BF%D0%BE/
    $('#search_name').typeahead({
        source:function(query, process){
        console.log('Query: ' + query);
            return $.ajax({
                        type:'GET',
                        url:'/coins/catalog/search/',
                        data:{
                            'search_name':query
                        },
                        dataType:'json',
                        success:function(data){
                            var name = Array();
                            data.forEach(function(entry){
                                name.push(entry['fields']['coin_name'])
                            });
                            arr_names = deleteDuplicate(name);
                            console.log(deleteDuplicate(arr_names));
                            return process(arr_names)
                        }
                    });
        },
        /*highlighter: function(item){
            console.log('Opa, working')
            var parts = item.split('_');
            parts.shift();
            return item;
        }*/
    });

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

// delete duplicate name coins in array
function deleteDuplicate(arr){
    var uniqueNames = [];
    $.each(arr, function(i, el){
        if($.inArray(el, uniqueNames) === -1) uniqueNames.push(el);
    });
    return uniqueNames
}
function ajaxCoinsSearch(first_search, number_page){ // first_search указывает, происходит загрузка контента при поиске или переходе меджу страницами
    $('#result_box').html('<img src="/static/gif/ajax-loader.gif">')
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
                'first_load' : first_search,
                'country':$('#country').html()
            },
            dataType: 'json',
            success:function(data){
                console.log('Print result:');
                console.log(data);
                console.log('End operation.:');

                // get data on server
                coins = JSON.parse(data[1]);

                // get quantity pages
                total_pages = data[0]
                console.log(first_search)
                if(first_search == 'True'){
                    Paginator(total_pages)
                }


                html = '<div>';
                coins.forEach(function(entry){
                    fields = entry['fields']

                    name = fields['coin_name'];
                    name_length = 20
                    if(name.length > name_length){ // for minimum length name coins
                        name = name.substring(0,name_length) + '...'
                    }

                    href = '<a href="' + entry['pk'] + '" title="' + fields['coin_name'] + '" target="_blank">'
                    html += href + '<div class="coins_view col-lg-3" align="center"><div class="coin_item"><img src="' + fields['photo_reverse'] + '" width="100px" height="100px"></div>';
                    html += '<div>' + href + name + '</a></div>';
                    html += '<div><label>' + fields['rate'] + ' ' + fields['denominal'] + '</label> </div></div></a>';
                });
                html += '</div>'

                $('#result_box').html(html)

            }
        });
}