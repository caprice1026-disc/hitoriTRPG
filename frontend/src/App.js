import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Home from './pages/Home';
import GamePage from './pages/Game';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route path="/" exact>
            <Home />
          </Route>
          <Route path="/game">
            <GamePage />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;

