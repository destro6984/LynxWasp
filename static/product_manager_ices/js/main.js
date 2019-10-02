$(function () {
// open popup window to add new message
    $('#checkout').click(function (e) {
        $('.bg-modal').css('display', 'flex')
    });

    $('.close').click(function () {
        $('.bg-modal').css('display', 'none')
    });
    // end


    //calculator for counting change
    var summm = $("#sumtopay").attr("value");
    $("#clientmoney").on("input", function () {
        var forclient = summm - $("#clientmoney").val();
        $('#clientchange').text(forclient + "zł");
    });
    // /end

    // quantity
    var quantity = $('.count');
    $('.plus').on('click', function () {
        quantity.val(parseInt(quantity.val()) + 1);
    });
    $('.minus').on('click', function () {
        quantity.val(parseInt(quantity.val()) - 1);
    });
// end
// adding scope by adding flavoures
    console.log($("#scoope").prev("input[name='ice']"));
    console.log("asdf")


    var type_ice_s = $("#scoope").prev("input[name='ice']").change(function (event) {
        if (type_ice_s.is(":checked")) {
            $('input[name=flavour]').click(function (event) {
                var input_flavour = $('input[name=flavour]:checked').length;
                $('.count').attr('value', input_flavour);

            });
        }
    });
    // adding thai ice
    var type_ice = $("#Thai").prev("input[name='ice']").change(function (event) {
        if (type_ice.is(":checked")) {
            $('input[name=flavour]').click(function (event) {
                $('.count').attr('value', 1);

            });
        }
    });
// reset checkboxe after change
    $(".radio-toolbar input[name=ice]").change(function (event) {
        $('input[name=flavour]').prop("checked", false);
        $('.count').attr('value', 1);
    });


// end


})
;