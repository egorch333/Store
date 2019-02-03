$(document).ready(function () {
    //Михаил
    var quantitiy = 0;
    $('.quantity-right-plus').click(function (e) {
        // Stop acting like a button
        e.preventDefault();
        // Get the field name
        var quantity = parseInt($('#quantity').val());
        // If is not undefined
        $('#quantity').val(quantity + 1);
        // Increment
    });

    $('.quantity-left-minus').click(function (e) {
        // Stop acting like a button
        e.preventDefault();
        // Get the field name
        var quantity = parseInt($('#quantity').val());
        // If is not undefined
        // Increment
        if (quantity > 0) {
            $('#quantity').val(quantity - 1);
        }
    });

    //мой для сортировки товров
    let csrftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
        headers: {"X-CSRFToken": csrftoken}
    });

    category = '';
    availability = 'True';

    $("#sort-category a").click(function () {
        console.log(this.value);
        console.log($(this).text());
        category = $(this).text();
    });

    $("#availability a").click(function () {
        console.log($(this).text());
        availability = $(this).text();
    });

    $("#sort-product").click(function () {
      //сортировка по фильтрам
      var data = {};
      data.category = category;
      data.price1 = +$("select#price-from option:selected").text();
      data.price2 = +$("select#price-to option:selected").text();
      data.availability = availability;
      data.url = "http://127.0.0.1:8000/sort-jquery/";

      $.ajax({
        url: this.url,
        type: "POST",
        data: data,
        success: (response) => {
            console.log('response', response);
            $("#product-list").empty();

            var i = 0;
            //циклом вывожу картинки
            while(i < response.length){
                var list = '<div class="col-md-4 text-center">\
                                <div class="product-entry">\
                                    <div class="product-img"\
                                         style="background-image: url(' + response[i].photo.image + ');">\
                                        <p class="tag"><span class="new">New</span></p>\
                                        <div class="cart">\
                                            <p>\
                                                <span class="addtocart"><a href="cart.html"><i class="icon-shopping-cart"></i></a></span>\
                                                <span><a href="product-detail.html"><i class="icon-eye"></i></a></span>\
                                                <span><a href="#"><i class="icon-heart3"></i></a></span>\
                                                <span><a href="add-to-wishlist.html"><i class="icon-bar-chart"></i></a></span>\
                                            </p>\
                                        </div>\
                                    </div>\
                                    <div class="desc">\
                                        <h3><a href="' + response[i].slug + '">' + response[i].title + '</a></h3>\
                                        <p class="price"><span>' + response[i].price + '</span></p>\
                                    </div>\
                                </div>\
                            </div>';

                $("#product-list").append(list);
                i++;
            }
        }
      })

      // блокировка перехода на другую страницу
      return false;
    });

});
