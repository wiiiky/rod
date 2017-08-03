$.getCookie = function(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.post = function(url, data, success, error){
  $.ajax({
    type: 'POST',
    url: url,
    data: JSON.stringify(data),
    contentType: 'application/json',
    dataType: 'json',
    success: success,
    error: error,
    beforeSend: function(xhr, settings) {
        var csrftoken = $.getCookie('csrftoken');
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
  })
}

$.get = function(url, success, error) {
  $.ajax({
    type: 'GET',
    url: url,
    dataType: 'json',
    success: success,
    error: error,
    beforeSend: function(xhr, settings) {
        var csrftoken = $.getCookie('csrftoken');
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
  })
}
