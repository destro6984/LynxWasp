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
    var summm=$("#sumtopay").attr("value");
    $("#clientmoney").on("input", function () {
        var forclient= summm - $("#clientmoney").val();
        $('#clientchange').text(forclient+"zł");
    })
    // /end
});