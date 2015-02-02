$(document).ready(function(){
    $('#btnAdd').click(function(){
        console.log('1');
        var elem = $('#countries')
        country_id = elem.val();

        $.ajax({
            type: 'POST',
            url: '/user_image/ajax/add/country/',
            data: { 'country_id':country_id },
            dataType: 'json',
            success: function(data){
                console.log(data)
                try{
                    fields = data[0]['fields']
                    pk = data[0]['pk'];
                    html = '<tr class="bg-info" id="'+ pk +'"><td class="flag">'
                    html += '<img src="/media/' + fields['country_flag'] + '"></td><td>'
                    html += '<a href="' + pk + '">' + fields['country_name'] + '</a>'
                    html += '</td><td>'
                    html += '<a href="' + pk + '" class="btn btn-primary">Перейти</a>'
                    html += '</td><td>'
                    html += '<button class="btn btn-danger" value="' + pk + '" onclick="deleteCountry(this);">Удалить</button>'
                    html += '</td></tr>'

                    if(document.getElementById('tbl_country')){
                        $('#tbl_country').append(html).show('slow');
                    }
                    else{
                        html = '<table id="tbl_country" class="table">' + html + '</table>'
                        $('#usr_countries').html(html);
                        console.log(html)
                    }

                    $('#countries :selected').remove().trigger('chosen:updated');
                    elem.val('').trigger('chosen:updated');
                }
                catch(e){
                    console.log('Object exists')
                }

            }
        });
    });

});


    function deleteCountry(elem){
        var country_id = elem.value;
        console.log(country_id);
        $.ajax({
            type: 'POST',
            url:'/user_image/country/delete/',
            data:{
                'c_id': country_id
            },
            dataType: 'json',
            success:function(data){
                console.log(data[0]['fields']['country_name']);
                if(data != '500'){
                    tr = 'tr[id='+ country_id + ']'
                    label = 'label[id=' + country_id + ']'
                    $(tr).remove();
                    $('#countries').append('<option value="'+ country_id +'">'+ data[0]['fields']['country_name'] +'</option>').trigger('chosen:updated');
                }
                else{
                    console.log('Sheet');
                }
            }
        });
    }