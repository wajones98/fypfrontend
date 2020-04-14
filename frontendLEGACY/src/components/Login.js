import React, {useState} from 'react'
import Axios from 'axios';
import M from 'materialize-css'

export default function Login() {

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
       

    function validateForm() {
        return email.length > 0 && password.length > 0;
    }
    
    async function getData() {
        const response = await Axios.post(
            'http://192.168.0.22:8080/auth/login',
            { 'Email': email, 'Password': password },
            { headers: {'Content-Type': 'application/json'} }
        )
        localStorage.setItem('SessionId', response.data.Message);
    };

    function handleSubmit(e) {
        e.preventDefault();
        getData()
    }

    return (
        <div className="Login">
            <form onSubmit={handleSubmit}>
                <div className="row">
                    <div className="input-field col s12">
                        <input id="email" type="email" className="validate" value = {email} onChange={e => setEmail(e.target.value)}/>
                        <label htmlFor="email">Email</label>
                    </div>
                </div>
                <div className="row">
                    <div className="input-field col s12">
                        <input id="password" type="password" className="validate" value = {password} onChange={e => setPassword(e.target.value)}/>
                        <label htmlFor="password">Password</label>
                    </div>
                </div>
                <button type="submit" disabled={!validateForm()} className="waves-effect waves-light btn-large">Login</button>
            </form>
        </div>
    )
}
