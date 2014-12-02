$(document).ready(function(){
    $('#btnSearch').click(function(){
        console.log('Start Ajax ...');
        $.ajax({
            type:'POST',
            url:'/coins/catalog/search/',
            data:{
                'csrfmiddlewaretoken': $('input[csrfmiddlewaretoken]').val(),
                'name' : $('#search_box').val(),
                'series':$('#series').val()
            },
            success:function(data){
                console.log('Print result:');
                console.log(data);
                console.log('End operation.:');
                $('#result_box').html(data)
            }
        });
    });
});