const New_Chat_Button = document.getElementById('New_Chat');
const Sign_Up_Button = document.getElementById("Sign_Up")
const Sign_In_Button = document.getElementById('Sign_In');
const Submit_Button = document.getElementById('Submit');
const Log_Out_Button = document.getElementById('Log_Out');
const Register_Button = document.getElementById('register');
const New_Chat_Refresh = document.getElementById('New_Chat_Refresh');

if(New_Chat_Button){
    New_Chat_Button.addEventListener('click', () => {
        window.location.href = '/new_chat';
    
    });

}

if(New_Chat_Refresh){
    New_Chat_Refresh.addEventListener('click' , () =>{
        window.location.href='/new_chat';
    });
}


if(Sign_Up_Button){
        Sign_Up_Button.addEventListener('click', () => {
            window.location.href = "/sign_up";

     });
}

if(Sign_In_Button){
    Sign_In_Button.addEventListener('click', () => {
        window.location.href = "/sign_in";

 });
}



if(Submit_Button){
    Submit_Button.addEventListener('click', () => {

        window.location.href = "/user_home";
    });
    

}



if(Log_Out_Button){
    Log_Out_Button.addEventListener('click' , () => {
        window.location.href = "/logout";
        
    });

}



if(Register_Button){
    Register_Button.addEventListener('click' , () =>{ 
        window.location.href = "/user_home";
    
    })

}



document.addEventListener('DOMContentLoaded',function(){

    const toggleButton = document.getElementById('Light_Modes');
    const body = document.body;

    if(toggleButton){
    toggleButton.addEventListener('click',function(){
        body.classList.toggle('dark_mode'); /*dark mode sınıfını aç kapa yapar */
        if(body.classList.contains('dark_mode'))
        {
            toggleButton.textContent='Dark Mode';
        }
        else {
            toggleButton.textContent = 'Light Mode';
        }



    });
}
});
