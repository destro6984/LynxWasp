$(function () {
  //calculator for counting change
  var sumToPay = $("#sumtopay").attr("value");
  $("#clientmoney").on("input", function () {
    var forClient = sumToPay - $("#clientmoney").val();
    $("#clientchange").text(forClient + "zł");
  });
  // /end

  // quantity
  var quantity = $(".count");
  $(".plus").on("click", function () {
    quantity.attr("value", parseInt(quantity.val()) + 1);
  });
  $(".minus").on("click", function () {
    quantity.attr("value", parseInt(quantity.val()) - 1);
  });
  // end
  // Adding ices
  var input_name_ice = $("input[name='ice']");
  var input_name_flavour = $("input[name=flavour]");

  input_name_ice.on("change", function () {
    // reset checkbox after change
    resetCount();

    input_name_flavour.on("click", addIce);
  });

  function resetCount() {
    input_name_flavour.prop("checked", false);
    $(".count").attr("value", 1);
    input_name_flavour.prop("disabled", false);
  }
  function addIce() {
    // adding thai ice
    if ($("#THAI").prev("input[name='ice']").is(":checked")) {
      $(".count").attr("value", 1);
      // only 3 flavoures can be picked for Thai ice
      if ($("input[name=flavour]:checked").length >= 3) {
        $(":checkbox:not(:checked)").prop("disabled", true);
      } else {
        input_name_flavour.prop("disabled", false);
      }
    }
    // adding scope depending on flavours number
    else if ($("#SCOOPE").prev("input[name='ice']").is(":checked")) {
      var input_flavour = $("input[name=flavour]:checked").length;
      $(".count").attr("value", input_flavour);
    }
  }

  // end
  // change number to status detail view
  sts = $(".statusoforder");
  switch (sts.text()) {
    case "1":
      sts.text("Started");
      break;
    case "2":
      sts.text("Postponed");
      break;
    case "3":
      sts.text("Finished");
      break;
  }
  // end
  // #Setting crsf token  for all ajax form django docs.#

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  var csrftoken = getCookie("csrftoken");

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  }

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
  });

  // end#
});
