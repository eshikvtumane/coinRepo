function deleteSeries(elem){
        var series_id = elem.value;
        console.log(elem.parentNode.rowIndex);
        $.ajax({
            type: 'POST',
            url:'/user_image/series/delete/',
            data:{
                's_id': series_id
            },
            success:function(data){
                if(data == '200'){
                    $('tr[id="'+series_id+'"]').remove()
                }
                else{
                    console.log('Sheet');
                }
            }
        });
    }