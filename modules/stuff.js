(function() {
    'use strict';
    // Your code here...
    const loginButton = document.querySelector('#loginButton');
    if(loginButton) {
    console.log('SDP')
    setTimeout(()=>{
        document.querySelector('#username').value = 'Jim';
        document.querySelector('#password').value = 'password';

        loginButton.click();},0)
    }
    const forms = [...document.querySelectorAll('form.form div.divLogin div#wrapper div.content .css_controls')]

    if(forms.length === 2) {
      console.log('ILS');

       setTimeout(()=>{
           [firstName, lastName, password] = forms;
           firstname.value = 'James Immanuel'
           lastName.value = 'Magsino'
           password.value = '9961';

        document.querySelector('input#btnLogin').click();},0)
    }
    

})();