// <-----------------Not being used--------------->
//
//const form = document.getElementById('email-form');
//const form_file = document.getElementById('form-file')
//
//if (form_file){
//    form_file.addEventListener("change", function() {
//        for( const file in form_file.files ) {
//            if (file.size > 300 * 1024) {
//                alert('{file.name} is too big. Max file size is 300KB!!')
//            }
//        }
//    })
//}
//
//form.addEventListener("submit", e => {
//
//    e.preventDefault();
//
//    var url = 'http://localhost:8090/send-email/'
//    var formData = new FormData()
//
//    from = document.getElementById('form-from').value;
//    to = document.getElementById('form-to').value;
//    subject = document.getElementById('form-subject').value;
//    body = document.getElementById('form-body').value;
//    file = form_file.files[0]
//
//    formData.append("from", from)
//    formData.append("to", to)
//    formData.append("subject", subject)
//    formData.append("body", body)
//    formData.append("file", file, file.name)
//
//    console.log(formData)
//
//    const xhr = new XMLHttpRequest();
//
//    xhr.open("POST", url, false);
//    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
////    xhr.setRequestHeader("Content-type", "application/json");
//    xhr.setRequestHeader("Accept", "application/json");
//    xhr.send(formData);
//
//    if (xhr.status === 200) {
//        console.log(xhr.responseText);
//        alert("Email has been send successfully!!")
//    }
//    else {
//        alert("Some Exception Occurred. Please try again later.")
//    }
//
//})

