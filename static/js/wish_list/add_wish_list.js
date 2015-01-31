function addWishList(id){
    console.log(id);

    $.ajax({
        type: 'GET',
        url: '/coins/add_wish_list/',
        data:{
            'coin_id': id
        },
        success:function(data){
            if(data == '200'){
                $('#wish_list_btn').html('<label>Монета добавлена в список желаний</label>');
            }
            else{
                console.log('Server error');
                $('#error').html('<span>Произошла ошибка при добавлении монеты в список желаний. Пожалуйста, повторите операцию позднее.</span>');
            }
        }
    });
}