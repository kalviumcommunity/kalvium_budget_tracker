import './App.css'
import Auth from './components/Auth';
import { Route, Routes } from "react-router-dom";

import UserDetails from './components/UserDetails';

function App() {
  return (
    <div className="App">
    <Routes>
      <Route path="/" element={<Auth />} />
      <Route path="/user_details" element={<UserDetails />} />
    </Routes>
    </div>
  );
}

export default App;
