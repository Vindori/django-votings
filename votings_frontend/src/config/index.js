let url = '';

if (process.env.NODE_ENV === 'development') {
    url = 'localhost:8000';
} else {
    url = window.location.host;
}

const serverUrl = url;

const apiUrl = `http://${serverUrl}/api`;

export { apiUrl };