// Test用モジュール
import React from 'react';

const Button = ({ children, onClick }) =>
    <button onClick={onClick}>{children}</button>;

const EntryEMail = ({ onClick }) => (
    <div>
        <input type="email" defaultValue="" />
        <Button onClick={onClick}>登録</Button>
    </div>
);

export default EntryEMail;
