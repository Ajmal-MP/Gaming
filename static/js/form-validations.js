$(document).ready(function(){
    $("#signup").validate({
      rules:{
        first_name:{
          required:true,
          minlength:4
        }, 
        last_name:{
          required:true,
          minlength:4
        },
        email:{
          required:true,
          email:true
        },
        mobile:{
          required:true,
          number:true,
          minlength:10,
          maxlength:11
        },
        password:{
          required:true,
          minlength:5
        },
        confirm_password : {
                  minlength : 5,
                  equalTo : "#password"
              }
      },
      messages :{
        first_name:{
          minlength:"Name should be atleast 3 charecters"
        },
        last_name:{
          minlength:"Name should be atleast 3 charecters"
        },
        confirm_password:{
          equalTo:"Password doesn't match"
        }
      }
    })
  })