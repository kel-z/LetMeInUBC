const submit = document.querySelector(".submit")
const w = document.getElementById('w');
const s = document.getElementById('s');
const session = document.getElementById('sess');
const ongeInput = document.getElementById('ongeInput');
const onge = document.getElementById('onge')
const submitForm = document.getElementById('submitform');
const postForm = document.getElementById('post-form');

const xhr = new XMLHttpRequest();

let sess = 0;
let onlyGeneral = true;

w.addEventListener('click', function(e) {
    s.classList.remove("active");
    w.classList.add("active");
    // session.selectedIndex = '0';
    sess = 0;
});

s.addEventListener('click', function(e) {
    w.classList.remove("active");
    s.classList.add("active");
    // session.selectedIndex = '1';
    sess = 1;
})


ongeInput.addEventListener('click', function(e) {
    if (onlyGeneral) {
        onlyGeneral = false;
        ongeInput.classList.remove('active');
    } else {
        onlyGeneral = true;
        ongeInput.classList.add('active');
    }
})


// submit.addEventListener('click', function(e) {
//     document.getElementById('year').value = document.getElementById('yearInput').value;
//     document.getElementById('dept').value = document.getElementById('deptInput').value;
//     document.getElementById('cnum').value = document.getElementById('cnumInput').value;
//     document.getElementById('sect').value = document.getElementById('sectInput').value;
//     document.getElementById('sms').value = document.getElementById('smsInput').value;
//     document.getElementById('email').value = document.getElementById('emailInput').value;

//     // submitForm.click();
// });

function create_post() {
    console.log("create post is working!") // sanity check
    $.ajax({
        url : "", // the endpoint
        type : "POST", // http method
        data : {'session' : sess === 0 ? 'W' : 'S',
                'year' : document.getElementById('yearInput').value,
                'dept' : document.getElementById('deptInput').value,
                'course' : document.getElementById('cnumInput').value,
                'section' : document.getElementById('sectInput').value,
                'only_general' : onlyGeneral,
                'sms' : document.getElementById('smsInput').value,
                'email' : document.getElementById('emailInput').value}, // data sent with the post request

        // handle a successful response
        success : function(json) {
            // $('#post-text').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            $('#result').html("<h3 id='success'>Success! We'll let you know when there's a seat available.</h3>");
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#result').html("<h3 id='error'>" + xhr.responseText + "</h3>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

postForm.addEventListener('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    create_post();
});