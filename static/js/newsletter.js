// static/js/newsletter.js
document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('newsletter-form');
  const messageBox = document.getElementById('message-box');

  form.addEventListener('submit', function (event) {
    event.preventDefault(); 

    const formData = new FormData(form);

    fetch('/newsletter/', {
      method: 'POST',
      body: formData,
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      }
    })
    .then(response => response.json())
    .then(data => {
      console.log('Server response:', data);
      if (data.success){
        messageBox.innerHTML = `<p style='color: green;'>${data.success}</p>`;
        form.reset();
        form.style.display = "none";
      }else{
       messageBox.innerHTML = `<p style='color: red;'>Something went wrong, try again</p>`;
      }
    
    })
    .catch(error => {
      messageBox.innerHTML = `<p style="color: red;">Server error. Try again.</p>`;
      console.error("Error:", error);
    });
  });
});
