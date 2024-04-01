import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthProvider';
import PrivateRoute from './components/PrivateRoute'; // ログイン済みユーザーのみアクセス可能なRouteコンポーネント
import LoginPage from './pages/Login';
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

// ここから下は要修正。ログイン用
function App() {
  return (
    <AuthProvider>
      <Router>
        <Switch>
          <Route path="/login" component={LoginPage} />
          <PrivateRoute exact path="/" component={HomePage} />
        </Switch>
      </Router>
    </AuthProvider>
  );
}

export default App;

