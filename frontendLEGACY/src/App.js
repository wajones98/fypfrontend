import React from 'react';
import './App.css';
import Login from 'components/Login';
import { Switch, Redirect, Route, BrowserRouter as Router } from 'react-router-dom';
import Browse from 'components/Browse';


function App() {
  let sessionId = null
  return (
    <div className="App">
      <Router>
        {sessionId === null ? <Redirect to='/login' /> : <Redirect to= '/browse'/>}
        <Switch>
          <Route path='/login' exact component = {Login} />
          <Route path='/browse' exact component = {Browse} />
        </Switch>
      </Router>
    </div>
  );
}


export default App;
