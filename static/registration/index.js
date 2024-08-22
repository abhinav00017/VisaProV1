document.addEventListener('DOMContentLoaded',  () => {
    const add_new_user = document.getElementById('new_user_form');
    console.log(add_new_user)

    add_new_user.addEventListener('submit',(event) => {
        event.preventDefault();
        const user_name = document.getElementById('user_name').value;
        const country = document.getElementById('country').value;
        
        console.log(user_name, country);

        if(user_name==='' || country === ''){
            alert('Username and country selection must not be empty.');
            return;
        }
    
        fetch('/profile/newuser', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_name, country, threads: [] })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            window.location.href = '/visagpt/home'; 
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    })


});