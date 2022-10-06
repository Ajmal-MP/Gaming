$(document).ready(function(){
  $("#image-form").validate({
    rules:{
          product_name:{
                        required:true,
                        minlength:2
                        }, 
          brand:{
            required:true,
            minlength:2
                },
            
                price:{
                  required:true, 
                },
                stock:{
                  min:0
                },
                product_description:{
                  minlength:10
                },
                product_offer:{
                  required:false,
                  min:0,
                  max:70,
                }
          },


    messages :{
              product_name:{
                            minlength:"Minimum 2 charecter needed",
                            },
              brand:{
                minlength:"Minimum 2 charecter needed",
              },
              price:{
                min:'Price must be posative number'
              },
              stock:{
                min:'Stock must be posative number'
              },
              product_description:{
                minlength:"Minimum 10 charecter needed", 
              },
              product_offer:{
                  min:'Offer must be posative number',
                  max:'Offer must be less than or equal 70%',
                }
              }
  })
})

