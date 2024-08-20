$(document).ready(function() {
  $("#login-form").submit(function(event) {
    event.preventDefault();
    $.ajax({
        type: "POST",
        url: "/api/login_ajax/",
        data: $(this).serialize(),
        success: function(response) {
            if (response.success) {
                window.location.href = "/classic/";
            } else {
                $("#error-message").text(response.message);
            }
        }
    });
  });
  const passwordInput = $('.password-field');
  const passwordLogin = $('.password-login');
  const togglePassword = $('.toggle-password');
  const togglePasswordLogin = $('.toggle-password-login');
  const emailInput = document.getElementById('id_email')
  const password1 = document.getElementById('id_password1');
  const password2 = document.getElementById('id_password2');
  const password = document.getElementById('id_logpassword');
  const regButton = document.querySelector('.form-panel.two').querySelector('button');
  const observer = new MutationObserver(function(mutationsList, observer) {

    for (const mutation of mutationsList) {
        if (mutation.type === 'attributes' && mutation.attributeName === 'disabled') {
            if (regButton.disabled) {
                regButton.innerText = 'ENTERED DATA IS INCORRECT'
            } else {
              regButton.innerText = 'REGISTER'
            }
        }
    }
});

observer.observe(regButton, { attributes: true });



  emailInput.addEventListener("keyup", (e) => {
    if (!emailInput.value.includes('@') && !emailInput.value.includes('.'))  {
      emailInput.style.outline = '3px solid rgb(154, 86, 75)';
      regButton.disabled = true;
    }
    else if (emailInput.value.includes('@') && emailInput.value.includes('.')) {
      emailInput.style.outline = '0px';
      regButton.disabled = false;
    }
  });
  password1.addEventListener('keyup', (e)=>{
    if (password1.value.length <4) {
      password1.style.outline = '3px solid rgb(154, 86, 75)';
      regButton.disabled = true;
    } else {
      password1.style.outline = '0px';
      regButton.disabled = false;
    }
  });

  password.addEventListener('keyup', (e)=>{
    if (password.value.length <4) {
      password.style.outline = '3px solid rgb(154, 86, 75)';
    } else {
      password.style.outline = '0px';
    }
  });


  password2.addEventListener('keyup', (e)=> {
    if (password2.value.length <4) {
      password2.style.outline = '3px solid rgb(154, 86, 75)';
      regButton.disabled = true;
    } else {
      password2.style.outline = '0px';
      regButton.disabled = false;
    }
    if (password2.value != password1.value) {
      password1.style.outline = '3px solid rgb(154, 86, 75)';
      password2.style.outline = '3px solid rgb(154, 86, 75)';
      regButton.disabled = true;
    }
    else {
      password1.style.outline = '0px';
      password2.style.outline = '0px';
      regButton.disabled = false;
    }
  });

  togglePassword.click(function() {
    if (passwordInput.attr('type') === 'password') {
        passwordInput.attr('type', 'text');
        togglePassword.text('Hide');
    } else {
        passwordInput.attr('type', 'password');
        togglePassword.text('Show');
    }
  });

  togglePasswordLogin.click(function() {
    if (passwordLogin.attr('type') === 'password') {
      passwordLogin.attr('type', 'text');
      togglePasswordLogin.text('Hide');
    } else {
        passwordInput.attr('type', 'password');
        togglePasswordLogin.text('Show');
    }
  });

    $(".menu__login").click(function () {
        $(".overlays").fadeIn();
        $(".form").slideDown();
      });
    
      $(".overlays").click(function (event) {
        if ($(event.target).hasClass('overlays')) {
            $(".form").slideUp();
            $(".overlays").fadeOut();
        }
    });
    $(".profile__login").click(function () {
        $(".overlays").fadeIn();
        $(".form").slideDown();
      });
    
      $(".overlays").click(function (event) {
        if ($(event.target).hasClass('overlays')) {
            $(".form").slideUp();
            $(".overlays").fadeOut();
        }
    });
    
    var panelOne = 420;
      panelTwo = 570;
   
    $('.form-panel.two').not('.form-panel.two.active').on('click', function(e) {
      
  
      $('.form-toggle').addClass('visible');
      $('.form-panel.one').addClass('hidden');
      $('.form-panel.two').addClass('active');
      $('.form').animate({
        'height': panelTwo
      }, 200);
    });
  
    $('.form-toggle').on('click', function(e) {
      $(this).removeClass('visible');
      $('.form-panel.one').removeClass('hidden');
      $('.form-panel.two').removeClass('active');
      $('.form').animate({
        'height': panelOne
      }, 200);
    });
  });