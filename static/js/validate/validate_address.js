function addressValidate(){
    region = document.forms['form_address']['region'].value;
    city = document.forms['form_address']['city'].value;
    street = document.forms['form_address']['street'].value;
    building = document.forms['form_address']['building'].value;
    flat = document.forms['form_address']['flat'].value;
    zip = document.forms['form_address']['zip'].value;

    elem_arr = [region, city, street, building, flat, zip];
    console.log(elem_arr);

    var elem;
    count_error = 0;
    for(index in elem_arr){
        console.log(elem_arr[index]);
        elem = elem_arr[index];
        if(elem == '' || elem == null){
            document.getElementsById('error').innerHTML = 'Проверьте правильность заполнения полей';
            return false;
        }
    }
    return true;
}