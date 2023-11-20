// App.js
import React, { useState } from 'react';
import FacebookLoginButton from './FacebookLoginButton';

const App = () => {
  const [accessToken, setAccessToken] = useState(null);

  const handleLogin = (token) => {
    setAccessToken(token);
  };

  return (
    <div>
      {!accessToken ? (
        <FacebookLoginButton onLogin={handleLogin} />
      ) : (
        <div>
          <p>Access Token: {accessToken}</p>
          {/* Add additional components or logic here after successful login */}
        </div>
      )}
    </div>
  );
};

export default App;

