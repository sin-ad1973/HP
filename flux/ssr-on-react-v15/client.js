import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

const serverNowString = document.getElementById('server-now').getAttribute('data-server-now');
const now = new Date(parseInt(serverNowString, 10));

ReactDOM.render(
    <App renderedAt={now} />,
    document.getElementById('root')
);
