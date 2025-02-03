import React from 'react';
import './Hero.css';

const Hero = ({ headline, introduction, heroImage }) => {
    headline = "Welcome to CodeOwl";
    introduction = "Easily query and explore software-related ontologies.";
    heroImage = "/home.png";
  return (
    <div className="container-fluid">
      <div className="hero-wrapper row flex-md-row flex-align-items-start">
        <div className="col-md-6 col-md">
          <div className="hero__content">
            <h1 className="hero__headline text-bg">{headline}</h1>
            <h3 className="hero__text">{introduction}</h3>
          </div>
        </div>
        <div className="col-md-6">
          <div className="hero__image">
            {/* inline style for width/height in React */}
            <img 
              src={heroImage} 
              alt="hero" 
              style={{ width: '10%', height: 'auto' }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;
