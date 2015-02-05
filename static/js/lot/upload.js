function upload(){
    field = document.getElementById('photo');
    if (field.files.length == 0) {
        console.log('Not');
        return;
    }

    var formdata = new FormData();
    for(var i = 0; i < field.files.length; i++){
        formdata.append('file_upload', field.files[i]);
    }



    $.ajax({
        url: '/shop/upload_file/',
        type: 'POST',
        data: formdata,
        processData: false,
        contentType: false,
        dataType: 'json',
        success: function(data){
            console.log('success!');
            console.log(data);
        }

    });
}