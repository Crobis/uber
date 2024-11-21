import '../css/editor.css';
import '../css/app.css';

const csrfToken = document.currentScript.dataset.csrftoken;

htmx.on('htmx:configRequest', (event) => {
    if (csrfToken) {
        event.detail.headers['x-csrftoken'] = csrfToken;
    }
});

console.log('csrfToken', csrfToken)
