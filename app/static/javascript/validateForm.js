
// Renvoi true si vide
const isEmpty = value => value === '' ? true : false;

// Renvoi true si la valeur est 0 
const isNull = value => parseInt(value) === 0  ? true : false;

// Affichage de l'erreur et mise en forme de l'input en fonction des erreurs
const showError = (input, message) => {
    // get the form-field element
    const formField = input.parentElement;
    // add the error class
    formField.classList.contains('success') ?? formField.classList.remove('success');
    formField.classList.add('error');

    // show the error message
    const error = formField.nextSibling;
    error.textContent = message;
};

const showSuccess = (input) => {
    const formField = input.parentElement;
    formField.classList.remove('error');
    formField.nextSibling.textContent = '';
}

// Vérification que la chaine ne contient que des chiffres
const isNumber = value => /^\d+$/.test(value);