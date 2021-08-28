$(document).ready(function(){
 console.log('hii')
   $("#username").keyup(function(){

      var username = $(this).val().trim();
      console.log(username)
      if(username != ' '){
         $.ajax({
            url: 'userexistcheck',
            type: 'post',
            cache: false,
            data: {username: username},
            success: function(response){
                alert("Success")
                $('#uname_response').html(response);

             }
         });
      }
      else{
         $("#uname_response").html("UserNameTooSmall");
      }


 });
$('#password').keyup(function() {
console.log("hello")
checkPasswordStrength($('#password').val())
});
 function checkPasswordStrength() {
            var number = /([0-9])/;
            var alphabets = /([a-zA-Z])/;
            var special_characters = /([~,!,@,#,$,%,^,&,*,-,_,+,=,?,>,<])/;
            if ($('#password').val().length < 6) {
                $('#password-strength-status').removeClass();
                $('#password-strength-status').addClass('weak-password');
                $('#password-strength-status').html("Weak");
            } else {
                if ($('#password').val().match(number) && $('#password').val().match(alphabets) && $('#password').val().match(special_characters)) {
                    $('#password-strength-status').removeClass();
                    $('#password-strength-status').addClass('strong-password');
                    $('#password-strength-status').html("Strong");
                } else {
                    $('#password-strength-status').removeClass();
                    $('#password-strength-status').addClass('medium-password');
                    $('#password-strength-status').html("Medium");
                }
            }
        }
 });
