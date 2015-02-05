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

        photo = document.getElementById('photo').files[0]
        console.log(photo);
        photo_arr = Array();

        var formData = new FormData();
        formData.append("file", JSON.stringify(photo));
        formData.append('quantity_lots', q_lots);
        formData.append('desc', desc);
        formData.append('items', JSON.stringify(items));

        field = document.getElementById('photo');
        if (field.files.length != 0) {
            for(var i = 0; i < field.files.length; i++){
                formData.append('file', field.files[i]);
            }
        }

        console.log(formData);

        for(var i = 0, f; f = photo[i]; i++){
            photo_arr.push(f);
        }

        $.ajax({
            type: 'POST',
            url: '/shop/create_buy/',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data){
                console.log(data);
                if(data == '200'){
                    infoPopup('#success');
                }
                else{
                    infoPopup('#error');
                }
            }
        });
    });
});

    function infoPopup(id){
        $(id).delay(100).fadeIn();
        $(id).delay(2000).fadeOut(1000);
    }