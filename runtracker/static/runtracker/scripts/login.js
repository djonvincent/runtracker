$(document).ready(function() {
   $('.ui.form').form({
      fields :{
         email: {
            identifier: 'email',
            rules : [
               {
                  type: 'email',
                  prompt: 'Please enter a valid e-mail address'
               }
            ]
         },
         password: {
            identifier: 'password',
            rules: [
               {
                  type: 'empty',
                  prompt: 'Please enter your password'
               }
            ]
         }
      }
   });
});
