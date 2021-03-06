function Paginator(total_pages){
    if(total_pages > 1){
        $('#pagination').html('<ul id="pagination-demo" class="pagination-sm"></ul>')
        $('#pagination-demo').twbsPagination({
            totalPages: total_pages,
            visiblePages: 7,
            first:'Первая',
            prev:'Предыдущая',
            last:'Последняя',
            next:'Следующая',
            onPageClick: function (event, page) {
                console.log('#-------------------- ' + 'page ' + page)
                ajaxCoinsSearch('False', page);
            }
        });
    }
    else if(total_pages == 0){
        $('#pagination').html('<h2>Данных не найдено</h2>')
    }
    else{
        $('#pagination').html('')
    }
}
