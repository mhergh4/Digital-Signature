function registerUser() {
    var username = document.getElementById("username").value;
    var signatureData = document.getElementById("signatureData").value;

    var formData = new FormData();
    formData.append("username", username); // Добавляем значение username в FormData
    formData.append("data", signatureData);

    fetch('http://localhost:8080', {  
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(signatureResult => {
        document.getElementById("userInfo").innerText = username;
        document.getElementById("signatureResult").innerText = signatureResult;
        document.getElementById("signatureInfo").style.display = "block";
        document.getElementById("signatureImage").src = "data:image/png;base64," + signatureResult; 
    })
    .catch(error => console.error('Error:', error));
}
