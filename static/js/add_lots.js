$(document).ready(function(){
    $('#publish').click(function(){
        q_lots = $('#quantity_lots').val();
        desc = $('#description').val();
        console.log('1');

        table = document.getElementById('tbl_add_coins');

        items = Array();
        for(var i = 1; i < table.rows.length; i++){
            id = table.rows[i].id;
            quantity = $('#quantity-' + id).val();
            pay = $('#pay-' + id).val();
            items.push({'id': id, 'quantity': quantity, 'pay': pay});

        }

        photo = document.getElementById('photo').files;
        //delete photo.files['length'];
        //delete photo.files['item'];
        photo_arr = Array();
        for(var i = 0, f; f = photo[i]; i++){
            photo_arr.push(f);
        }


console.log(items);
        $.ajax({
            type: 'POST',
            url: '/shop/create_buy/',
            enctype: "multipart/form-data",
            data: {
                'quantity_lots': q_lots,
                'desc': desc,
                'items': JSON.stringify(items),
                'photo': JSON.stringify(photo_arr)
            },
            success: function(data){
                console.log(data);
            }
        });
    });
});

function getAjax(){

}