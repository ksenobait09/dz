$(document).ready(function () {


    //работа с модалкой
    var modal = $('[data-remodal-id=modal]').remodal({closeOnConfirm: false, closeOnOutsideClick: false});

    $('#add_new_book_modal').click(function (e) {
        modal.open();
    });

    $(document).on('confirmation', '.remodal', function () {
        if ($.trim($('#new_name').val().toString()) == ''){
            alert('You must input name');
            return false;
        }
        if ($.trim($('#new_author').val().toString()) == ''){
            alert('You must input author');
            return false;
        }
        if ($.trim($('#new_description').val().toString()) == ''){
            alert('You must input description');
            return false;
        }

       $('#new_book_form').submit();

        /*$.post(
            '/add-book/',
            requestData,
            function(response){
                var ans = jQuery.parseJSON(response);
                if ( ans.error != undefined && ans.error != '' )
                {
                    $tbody.find('tr').addClass('notsave');
                    alert(ans.error);
                }
                else
                {
                    data.id = ans.addedid;
                    var $newTbody = $(rowTemplate(data));
                    $newTbody.insertBefore($tbody);
                    $newTbody.find('tr').addClass('saved');
                    $('.specmark-editor-add').removeClass('hide');
                    $('.specmark-editor-save').addClass('hide');
                    $tbody.remove();
                }
            }
        );*/
        modal.close();
    });

    $('.order , .remove-order').click(function (e) {
        var butt = e.currentTarget;
        var csrftoken = getCookie('csrftoken');

        function csrfSafeMethod(method) {// these HTTP methods do not require CSRF protection
           return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
        }
        });
        var state = ($(this).hasClass('order')) ? 'True': 'False';
        $.post(
            '/book/'+$(this).data('bookid'),
            {
                'state' : state
            },
            function(response){
                var ans = response;
                if ( ans == 'error' )
                {
                    alert(ans);
                }
                else
                {
                    $('.order , .remove-order').toggleClass('hide');
                    $('#users').text(ans);
                }
            }
        );

    });

    // using jQuery
    function getCookie(name) {
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

});