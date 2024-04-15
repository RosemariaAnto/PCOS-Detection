var inputname = document.getElementById('name-rose');
var inputage = document.getElementById('age-rose');
var inputbmi = document.getElementById('bmi-rose');
var inputglu = document.getElementById('glu-rose');

function isString(value) {
    return typeof value === 'string' || value instanceof String;
}

function validateName() {
    let name = document.getElementById('pons-name').value;
    let errorContainer = document.getElementById('name-error');

    // Reset error message
    errorContainer.innerHTML = '';

    // If no input or string input is given,
    if (name.length === 0 || !name.match(/^[A-Za-z]/)) {
        errorContainer.innerHTML = '<div class="error-box">❌ Please enter a valid name</div>';
        return false;
    }

    // If input is a string
    if (name.match(/^[A-Za-z]*\s*/)) {
        errorContainer.innerHTML = ''; // Clear any previous error message
        return true;
    }
}

// function to do Age input validation 
function validateAge() {
    let age = document.getElementById('pons-age').value;
    let errorContainer = document.getElementById('inputage-error');

    // Reset error message
    errorContainer.innerHTML = '';

    if (age.length == 0) {
        errorContainer.innerHTML = '<div class="error-box">❌ Please enter age</div>';
        return false;
    }

    // If input is not a number 
    if (isNaN(age) || (age < 0) || (age > 110)) {
        errorContainer.innerHTML = '<div class="error-box">❌ Please enter a valid age</div>';
        return false;
    }

    errorContainer.innerHTML = '<i class="check fa fa-check"></i>';
    return true;
}






function validateBmi() {
    let bmi = document.getElementById('pons-bmi').value;
    let errorContainer = document.getElementById('inputbmi-error');

    // Reset error message
    errorContainer.innerHTML = '';


    if (bmi.length == 0) {
        errorContainer.innerHTML = '<div class="error-box">❌ Please enter BMI</div>';
        return false;
    }

    if (isNaN(bmi) || isNaN(bmi) || (bmi < 12) || (bmi > 200)) {
        errorContainer.innerHTML = '<div class="error-box">❌ BMI must be a valid number between 12 and 200</div>';
        return false;
    }

    errorContainer.innerHTML = '<i class="check fa fa-check"></i>';
    return true;
}




// function to do glucose input validation 
function validateGlu() {
    let glu = document.getElementById('pons-glu').value;
    let errorContainer = document.getElementById('inputglu-error');

    // Reset error message
    errorContainer.innerHTML = '';

    if (glu.length == 0) {
        errorContainer.innerHTML = '<div class="error-box">❌ Please enter avg glucose</div>';
        return false;
    }

    if (glu.length == 0 || isNaN(glu) || (glu < 20) || (glu > 600)) {
        errorContainer.innerHTML = '<div class="error-box">❌ Glucose must be a valid number between 20 and 600</div>';
        return false;
    }

    errorContainer.innerHTML = '<i class="check fa fa-check"></i>';
    return true;
}

function validateForm() {
    if (!validateName() || !validateAge() || !validateBmi() || !validateGlu()) {
        alert("Please fill out the form correctly !! ")
        return false;
    }
}