document.addEventListener('DOMContentLoaded',()=>{
    const return_home = document.getElementById('retn_home_btn');

    return_home.addEventListener('click',function(){
        window.location.href = "/visagpt/home";
    });

    const sign_out = document.getElementById('Sign_out_btn');

    sign_out.addEventListener('click',function(){
        window.location.href = "logout";
    });




    const profile = document.getElementById('profile');
    const profile_menu = document.querySelector('.profile_menu');

    profile.addEventListener('click',function(){
        if(profile_menu.style.display === "none"){
            profile_menu.style.display = "block";
        }
        else {
            profile_menu.style.display = "none";
        }
    });

    profile.addEventListener('mouseover',function(){
        if(profile_menu.style.display === "none"){
            profile_menu.style.display = "block";
        }
        else {
            profile_menu.style.display = "none";
        }
    });


    const edit_btn = document.getElementById('edit_btn');
    const cancel_btn = document.getElementById('Cancel_btn');
    const done_btn = document.getElementById('Done_btn');

    edit_btn.addEventListener('click',function(){
        var input = document.querySelectorAll('.profile_dtls input');
        console.log(input);
        input.forEach(function(item){
            item.disabled = false;
        });
        var country = document.getElementById('country');
        country.disabled = false;
        edit_btn.style.display = "none";
        cancel_btn.style.display = "block";
        done_btn.style.display = "block";
    });

    cancel_btn.addEventListener('click',function(){
        var input = document.querySelectorAll('.profile_dtls input');
        input.forEach(function(item){
            item.disabled = true;
        });
        var country = document.getElementById('country');
        country.disabled = true;
        edit_btn.style.display = "block";
        cancel_btn.style.display = "none";
        done_btn.style.display = "none";
    });

    done_btn.addEventListener('click',function(){

        fetch('/profile/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'user_name': document.getElementById('name').value,
                'email': document.getElementById('email').value,
                'phonenumber': document.getElementById('phonenumber').value,
                'country': document.getElementById('country').value,
            })
        }).then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            var input = document.querySelectorAll('.profile_dtls input');
            input.forEach(function(item){
                item.disabled = true;
            });
            var country = document.getElementById('country');
            country.disabled = true;
            edit_btn.style.display = "block";
            cancel_btn.style.display = "none";
            done_btn.style.display = "none";
        })
        
    });

});


