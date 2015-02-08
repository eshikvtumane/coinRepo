$(document).ready(function(){
    $('#publish').click(function(){


        q_lots = $('#quantity_lots').val();
        desc = $('#description').val();

        table = document.getElementById('tbl_add_coins');

        items = Array();
        for(var i = 1; i < table.rows.length; i++){
            id = table.rows[i].id;
            quantity = $('#quantity-' + id).val();
            pay = $('#pay-' + id).val();
            if(!isNaN(parseInt(id)) && !isNaN(parseInt(quantity)) && !isNaN(parseInt(pay))){
                items.push({'id': id, 'quantity': quantity, 'pay': pay});
            }
            else{
                infoPopup('#error');
                return;
            }
console.log('11111');
        }
console.log('22222');
        // validate date
        if(q_lots == '' || desc == '' || items.length == 0){
            infoPopup('#error');
            return;
        }
console.log('33333');
        photo = document.getElementById('photo').files[0]
        console.log(photo);
        photo_arr = Array();

        var formData = new FormData();
        formData.append("file", JSON.stringify(photo));
        formData.append('quantity_lots', q_lots);
        formData.append('desc', desc);
        formData.append('items', JSON.stringify(items));

// add photo
        field = document.getElementById('photo');
        console.log(field.files.length);
        if (field.files.length != 0) {
            for(var i = 0; i < field.files.length; i++){
                formData.append('file', field.files[i]);
            }
        }

        console.log(formData);


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

