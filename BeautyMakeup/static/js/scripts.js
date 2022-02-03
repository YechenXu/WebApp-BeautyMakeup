$(document).ready(function () {
    $("#logo").click(function () {
        $("#logoText").toggle();
    });

    $(".messages li").fadeOut(3000, function (){
        $(this).remove();
    });

    // /*
    //     event handler for searching items
    //  */
    // $(document).on('click', '#search-box-button', function () {
    //
    //     var searchterm = $("#searchItem").val();
    //
    //     if (searchterm == "shine pink") {
    //         $("#search-box").attr("action", $("#search-box").attr(data-url1));
    //         $("#search-box").submit();     //提交ID为myform的表单
    //     }
    //     else {
    //         $("#search-box").attr("action", $("#search-box").attr(data-url));      //通过jquery为action属性赋值
    //         $("#search-box").submit();     //提交ID为myform的表单
    //     }
    //
    // });

    /*
        event handler for add new comment using Ajax
     */
    $(document).on('click', '#submitComment', function(){

        var title = $("#commentTitle").val();
        var comment = $("#comment").val();
        var item_id = $(this).attr('data-item-id');
        var ajax_url = $(this).attr('data-ajax-url')
        var username = $(this).attr('data-user-name')
        var user_url = $(this).attr('data-user-url')
        var edit_url = $('#all-comments').attr('data-edit-url')
        var delete_url = $('#all-comments').attr('data-delete-url')


        $.ajax({
            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                title: title,
                comment:comment,
                item_id:item_id
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType : "json",

            headers:{'X-CSRFToken': csrftoken},

            context:this
        })
          // Code to run if the request succeeds (is done);
          // The response is passed to the function
          .done(function( json ) {
              //create new comment
              if(json.success === 'success') {
                  var added_comment = $('<div class="comment-block"><hr/>\n <p class="title">' + title + '</p>\n' +
                      '  <p class="commentText">' + comment + '</p>\n' +
                      '  <p class="post-time">Posted now by <a href="' + user_url + '">' + username + '</a> </p>\n' +
                      ' <button class="edit-comment">Edit Comment</button> '+
                      '  <button class="submit-edit-comment" data-comment-id="'+ json.comment_id +'" data-ajax-url="'+ edit_url +'" style="display: none">Submit Edit</button>\n' +
                      '  <button class="delete-comment" data-comment-id="'+ json.comment_id +'" data-ajax-url="'+ delete_url +'">Delete Comment</button></div>');
                  if(json.comment_length === 1){
                      $('.no-comment').hide()
                  }
                  //insert the comment in the beginning of the comments list
                  $(added_comment).prependTo($('#all-comments'));

                  $('#commentTitle').val('')
                  $('#comment').val('')
              }
              else {
                  $('<p class="warning" style="color: red; font-size: 0.9em">* '+ json.error+'</p>').insertAfter($('#addComment')).fadeOut(3000,function (){
                      $(this).remove();
                  });
                  // alert("Error: " + json.error);
              }
          })
        // Code to run if the request fails; the raw request and
          // status codes are passed to the function
          .fail(function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem!" );
            console.log( "Error: " + errorThrown );
            console.log( "Status: " + status );
            // console.dir( xhr );
          })
          // Code to run regardless of success or failure;
          .always(function( xhr, status ) {
            // alert( "The request is complete!" );
          });

    });

    /*
        Delete comment using Ajax
     */
     $('#all-comments').on('click', '.delete-comment', function(){
        var comment_id = $(this).attr('data-comment-id');
        var ajax_url = $(this).attr('data-ajax-url');
        console.log(comment_id)


        $.ajax({
            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                comment_id:comment_id
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType : "json",

            headers:{'X-CSRFToken': csrftoken},

            context:this
        })
          // Code to run if the request succeeds (is done);
          // The response is passed to the function
          .done(function( json ) {
              if(json.success === 'success') {
                $(this).siblings().remove()
                if(json.comment_length === 0){
                    //if there is no comment in database
                    $('.no-comment').show()
                }
                $(this).parent('.comment-block').remove()
                $(this).remove()
              }
              else {
                  alert("Error: " + json.error);
              }
          })
          // Code to run if the request fails; the raw request and
          // status codes are passed to the function
          .fail(function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem!" );
            console.log( "Error: " + errorThrown );
            console.log( "Status: " + status );
            // console.dir( xhr );
          })
          // Code to run regardless of success or failure;
          .always(function( xhr, status ) {
            // alert( "The request is complete!" );
          });
    })

    /*
        Edit comment here
        First, change the title and comment content to input box
        Then show the update comment button, trigger update event
     */
    $('#all-comments').on('click', '.edit-comment', function(){
        var title = $(this).siblings('.title').text()
        var comment = $(this).siblings('.commentText').text()

        var update_title = $('<input type="text" class="update-comment-title" name="update-comment-title" value="'+ title +'" required/>')
        var update_content = $('<input type="text" class="update-comment-content" name="update-comment-title" value="'+ comment +'" required/>')

        $(this).siblings('.title').replaceWith(update_title)
        $(this).siblings('.commentText').replaceWith(update_content)

        $(this).siblings('.submit-edit-comment').show()
        $(this).hide()

    })

    /*
        Trigger the update comment event
     */
    $('#all-comments').on('click', '.submit-edit-comment', function(){

    // $("button.submit-edit-comment").click(function(){
        var updated_title = $('.update-comment-title').val()
        var updated_content = $('.update-comment-content').val()
        var comment_id = $(this).attr('data-comment-id');
        var ajax_url = $(this).attr('data-ajax-url');


        $.ajax({
            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                comment_id:comment_id,
                updated_title:updated_title,
                updated_content:updated_content
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType : "json",

            headers:{'X-CSRFToken': csrftoken},

            context:this
        })
          // Code to run if the request succeeds (is done);
          // The response is passed to the function
          .done(function( json ) {
              if(json.success === 'success') {
                  //replace with updated content
                  $(this).siblings('.update-comment-title').replaceWith('<p class="title">'+ updated_title +'</p>')
                  $(this).siblings('.update-comment-content').replaceWith('<p class="commentText">'+ updated_content +'</p>')
                  $(this).siblings('.edit-comment').show()
                  $(this).hide()
              }
              else {
                  alert("Error: " + json.error);
              }
          })
          // Code to run if the request fails; the raw request and
          // status codes are passed to the function
          .fail(function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem!" );
            console.log( "Error: " + errorThrown );
            console.log( "Status: " + status );
            // console.dir( xhr );
          })
          // Code to run regardless of success or failure;
          .always(function( xhr, status ) {
            // alert( "The request is complete!" );
          });
    });


    /*
        Sort the item based on the price and publish time.
     */

    $("#sortBy").on('change', function (){
        var sortOption = $(this).val();
        // console.log($(".itemBox").attr('data-item'));

        if(sortOption === 'priceH'){
            $(".itemBox").sort(sort_item).appendTo("#items");
            function sort_item(a,b){
                return parseInt($(b).children(".price").attr('data-item-price')) > parseInt($(a).children(".price").attr('data-item-price')) ? 1 : -1;
            }
        }
        else if(sortOption === 'priceL'){
            $(".itemBox").sort(sort_item).appendTo("#items");
            function sort_item(a,b){
                return parseInt($(b).children(".price").attr('data-item-price')) < parseInt($(a).children(".price").attr('data-item-price')) ? 1 : -1;
            }
        }
        else{
            $(".itemBox").sort(sort_item).appendTo("#items");
            function sort_item(a,b){
                return parseInt($(b).attr('data-created-date')) < parseInt($(a).attr('data-created-date')) ? 1 : -1;
            }
        }

    });


    function checkAvailability(){
        //check the checkbox condition
        var DeliverChecked = $('#checkDeliver').prop("checked");
        var PickupChecked = $('#checkPickup').prop("checked");

        //hide all the items
        $('.itemBox').each(function (){
            $(this).hide();
        });

        //show the items that was selected by check box
        if(DeliverChecked){
            $('.itemBox .availability').each(function (){
                if($(this).text().search('Deliver') >= 0){
                    $(this).parent().show();
                }
            });
        }
        if(PickupChecked){
            $('.itemBox .availability').each(function (){
                if($(this).text().search('Pickup') >= 0){
                    $(this).parent().show();
                }
            });
        }
    }

    $('#checkDeliver').click(function (){
        checkAvailability();
    });

    $('#checkPickup').click(function (){
        checkAvailability();
    });


    //check querystring
    // checkQueryString();

    $(document).on('click', '#deleteConfirmation', function(){
        var confirmation = confirm('Are you sure you want to delet this item?')
        if (confirmation){
            $(this).parent().submit();
        }
        else{
            return false;
        }
    });

    /*
        Event handler for change password
        First, hide the change-password button
        Then insert input box
     */
    $("button.change-password").click(function(){
        var new_password = $('<input type="password" id="new-password" name="password" placeholder="Enter password here." required/>')
        $('button.update-password').show()
        new_password.insertBefore($('button.update-password'));
        $(this).hide();
    });

    /*
        Update user's password with Ajax
     */
    $("button.update-password").click(function(){
        var username = $("#detail-info").attr('data-user-name')
        var new_password = $('#new-password').val()
        var ajax_url = $(this).attr('data-ajax-url')

        $.ajax({
            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                username: username,
                new_password:new_password
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType : "json",

            headers:{'X-CSRFToken': csrftoken},

            context:this
        })
          // Code to run if the request succeeds (is done);
          // The response is passed to the function
          .done(function( json ) {
              if(json.success === 'success') {
                  $('#new-password').remove();
                  $('button.update-password').hide();
                  $('button.change-password').show();
                  var successMsg = $('<p>Successfully changed password!</p>');
                  $(successMsg).insertAfter($('button.change-password')).fadeOut(3000,function (){
                      $(this).remove();
                  });
              }
              else {
                  alert("Error: " + json.error);
              }
          })
          // Code to run if the request fails; the raw request and
          // status codes are passed to the function
          .fail(function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem!" );
            console.log( "Error: " + errorThrown );
            console.log( "Status: " + status );
            // console.dir( xhr );
          })
          // Code to run regardless of success or failure;
          .always(function( xhr, status ) {
            // alert( "The request is complete!" );
          });

    });


    //event handler for update user's roles by admin using ajax
    $('#change-role').click(function () {
        $('#user-role').replaceWith("<select name=\"roleOption\" id=\"roleOption\">\n" +
            "\t    \t\t<option value=\"Admin\">Admin</option>\n" +
            "\t    \t\t<option value=\"Regular\">Regular</option>\n" +
            "\t    \t</select>")
        $('<button id="updateRole">Update Role</button>').insertBefore($('#change-role'))
        $('#change-role').hide()
    });


    $(document).on('click', '#updateRole', function(){
        var new_role = $('#roleOption option:selected').val();
        var username = $('#detail-info').attr('data-user-name')
        var ajax_url = $('#detail-info').attr('data-ajax-url')

        $.ajax({

            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                new_role: new_role,
                username:username
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType : "json",

            headers:{'X-CSRFToken': csrftoken},

            context:this
        })
          // Code to run if the request succeeds (is done);
          // The response is passed to the function
          .done(function( json ) {
              if(json.success == 'success'){
                  $('#roleOption').replaceWith('<td id="user-role">' + new_role + '</td>')
                  $('#updateRole').remove();
                  if(json.currentRole == 'Admin'){
                      $('#change-role').show();
                  }
              }
              else{
                  alert("Error: " + json.error);
              }

          })
          // Code to run if the request fails; the raw request and
          // status codes are passed to the function
          .fail(function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem!" );
            console.log( "Error: " + errorThrown );
            console.log( "Status: " + status );
          })
          // Code to run regardless of success or failure;
          .always(function( xhr, status ) {
            // alert( "The request is complete!" );
          });
    });

});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');