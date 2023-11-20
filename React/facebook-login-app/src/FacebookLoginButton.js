// FacebookLoginButton.js
import React from 'react';
import FacebookLogin from 'react-facebook-login';
import './FacebookLoginButton.css';

const FacebookLoginButton = ({ onLogin }) => {
  const responseFacebook = (response) => {
    // 'response' contains the Facebook user data including access token
    onLogin(response.accessToken);
  };

  return (
    <div className="centered-button">
      <FacebookLogin
        appId="494536885328838"
        autoLoad={false}
        fields="publish_pages,business_management,ads_management,pages_show_list,pages_read_engagement,pages_manage_metadata,pages_read_user_content,pages_manage_ads,pages_manage_posts,pages_manage_engagement"
        callback={responseFacebook}
        scope="public_profile,email,instagram_basic"
        icon="fa-facebook"
      />
    </div>
  );
};

export default FacebookLoginButton;

